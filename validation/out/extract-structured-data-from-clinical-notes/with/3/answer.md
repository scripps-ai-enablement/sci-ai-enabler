Writing files isn't authorized in this session, so I'll deliver the complete solution inline instead — you can save these as files yourself. Everything below is grounded in the catalog's `extract-structured-data-from-clinical-notes` recipe (**Evidence: Validated** — 96.2% accuracy vs. 3-physician consensus on ILD notes; F1=0.983 across 10 parameters on a 200-note oncology cohort; **Availability: fully open**, Claude Code + Anthropic API key only; **Compute: laptop**, ~$0.001–0.11/note), extended with concrete answers to the open questions in your request.

## Why rung 1 (Claude Code + a script), not a Skill/MCP/multi-tool system

This is pure text-in → structured-value-out extraction against a codebook you already own. There's no external database to query and no multi-stage lifecycle (that's what would push it to rung 3/4, e.g. if you also needed ICD-11/SNOMED coding — the separate `harmonize-clinical-terms-to-standard-codes` recipe, deliberately kept out of this step so codes aren't hallucinated alongside the extraction). A well-specified prompt plus a thin driver script is the whole job.

**Assumptions I'm making** (state these back to me if wrong, but I'm giving you a complete design regardless):
- Notes are plain text files, one folder per patient (some patients have >1 note): `notes/<patient_id>/<note_id>.txt`.
- Registry columns, concretized: `diagnosis`, `stage`, `prior_lines_of_therapy`, three biomarkers (`egfr_status`, `alk_status`, `pdl1_status`), and five acute symptoms — a plausible thoracic-oncology registry. Swap these for your real variables; the mechanism doesn't change.
- You have `ANTHROPIC_API_KEY` set and are allowed to send de-identified notes to the API under your institution's data-use agreement (the recipe flags this as a governance prerequisite, not something the pipeline itself can verify).

## 1. `codebook.md` — the single source of truth

The variable list, allowed values, and abstraction rules live in one version-controlled markdown table. The script parses this table directly rather than duplicating it in code, so there is exactly one place to change a rule.

```markdown
# Clinical Registry Codebook
version: 1.0.0
last_updated: 2026-07-30

## Global extraction rules (apply to every variable)
- status ∈ {found, negated, not_mentioned}.
- evidence_quote must be a verbatim sentence/clause from the note — never a paraphrase —
  and is null only when status = not_mentioned.
- value must be one of the variable's allowed_values (or an integer for numeric variables).
- Never infer a value from context that isn't itself stated (e.g. don't infer Stage IV from
  "liver metastases" unless the note also states the stage).
- Set needs_review = true with a one-line review_reason whenever the note has conflicting
  statements about this variable, the value doesn't cleanly map to an allowed value, or the
  evidence is ambiguous. When in doubt, flag rather than guess.

## Variables
| variable | type | allowed_values | rule |
|---|---|---|---|
| diagnosis | categorical | NSCLC\|SCLC\|breast_cancer\|colorectal_cancer\|other | Primary oncologic diagnosis as explicitly stated by the treating physician. If a real diagnosis isn't in this list, use `other` and still quote the exact term. |
| stage | categorical | I\|II\|III\|IV\|unknown | Clinical/pathologic stage only if explicitly documented. Do not derive from metastasis/nodal mentions alone. |
| prior_lines_of_therapy | numeric | integer >= 0 | Count of distinct prior systemic regimens before the one discussed in this note. "Second-line" implies 1 prior line. Don't count planned/future therapy. |
| egfr_status | categorical | positive\|negative\|not_tested\|indeterminate | EGFR result as stated. not_tested ≠ negative. |
| alk_status | categorical | positive\|negative\|not_tested\|indeterminate | ALK result as stated. |
| pdl1_status | categorical | negative_lt1pct\|low_1_49pct\|high_ge50pct\|not_tested | Bucket an explicitly stated PD-L1 TPS%: <1 / 1-49 / ≥50. |
| symptom_dyspnea | binary | present\|absent\|not_mentioned | Current/acute (this visit or preceding 24-72h) — not a resolved/historical symptom. |
| symptom_fever | binary | present\|absent\|not_mentioned | Same recency rule. |
| symptom_chest_pain | binary | present\|absent\|not_mentioned | Same recency rule. |
| symptom_hemoptysis | binary | present\|absent\|not_mentioned | Same recency rule. |
| symptom_fatigue | binary | present\|absent\|not_mentioned | Same recency rule. |
```

To change abstraction logic later: edit this table, bump the version, re-run the pipeline, diff `registry.csv` against the last committed version before trusting it. Nothing else needs to change.

## 2. Extraction schema (per note, not per patient)

Run extraction **per note file**, not per patient — that's what makes every cell traceable to a specific `note_id` even when a patient has several notes, and it's what lets you detect when two notes about the same patient disagree. Force the model into a tool call so output is always well-formed JSON, never prose to parse:

```python
def build_tool_schema(variables):
    props = {}
    for v in variables:
        val_type = {"numeric": "integer"}.get(v["type"], "string")
        val_schema = {"type": [val_type, "null"]}
        if v["allowed_values"]:
            val_schema = {"type": ["string", "null"], "enum": v["allowed_values"] + [None]}
        props[v["name"]] = {
            "type": "object",
            "properties": {
                "value": val_schema,
                "evidence_quote": {"type": ["string", "null"]},
                "status": {"type": "string", "enum": ["found", "negated", "not_mentioned"]},
                "needs_review": {"type": "boolean"},
                "review_reason": {"type": ["string", "null"]},
            },
            "required": ["value", "evidence_quote", "status", "needs_review", "review_reason"],
        }
    return {
        "name": "extract_registry_row",
        "description": "Extract one clinical note's variables per the codebook.",
        "input_schema": {
            "type": "object",
            "properties": {"note_id": {"type": "string"}, **props},
            "required": ["note_id"] + [v["name"] for v in variables],
        },
    }
```

## 3. `extract_registry.py` — the committed, rerunnable driver

```python
#!/usr/bin/env python3
"""Extract registry variables from clinical notes per codebook.md. Rerunnable end to end."""
import argparse, csv, hashlib, json, re, sys, time
from pathlib import Path
from anthropic import Anthropic

MODEL = "claude-sonnet-5"

def parse_codebook(path: Path):
    text = path.read_text()
    rows = re.findall(r"^\|\s*(\w[\w_]*)\s*\|\s*(\w+)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|$",
                       text, re.MULTILINE)
    variables = []
    for name, vtype, allowed, rule in rows:
        if name in ("variable", "---"):
            continue
        allowed_values = allowed.split("|") if vtype != "numeric" else None
        variables.append({"name": name, "type": vtype, "allowed_values": allowed_values, "rule": rule})
    return variables

def build_system_prompt(codebook_text, variables):
    return (
        "You are abstracting one clinical note into structured registry variables. "
        "Follow this codebook exactly — do not use knowledge outside the note, "
        "do not infer unstated values, and quote verbatim evidence for every non-null value.\n\n"
        f"{codebook_text}\n\n"
        "Call extract_registry_row exactly once for this note."
    )

def extract_note(client, note_id, note_text, system_prompt, tool_schema):
    resp = client.messages.create(
        model=MODEL, max_tokens=2048, temperature=0,
        system=system_prompt,
        tools=[tool_schema],
        tool_choice={"type": "tool", "name": "extract_registry_row"},
        messages=[{"role": "user", "content": f"note_id: {note_id}\n\n{note_text}"}],
    )
    for block in resp.content:
        if block.type == "tool_use":
            return block.input
    raise RuntimeError(f"No tool_use block returned for {note_id}")

def validate_record(record, variables):
    """Belt-and-suspenders: never trust the model's enum adherence blindly."""
    for v in variables:
        field = record.get(v["name"], {})
        if v["allowed_values"] and field.get("value") not in (v["allowed_values"] + [None]):
            field["needs_review"] = True
            field["review_reason"] = f"value '{field.get('value')}' not in codebook allowed_values"
    return record

def aggregate_patient(patient_id, note_records, variables):
    """Collapse multiple notes -> one registry row; flag cross-note conflicts."""
    row = {"patient_id": patient_id}
    for v in variables:
        name = v["name"]
        found = [(r["note_id"], r[name]) for r in note_records if r[name]["status"] == "found"]
        distinct_values = {val["value"] for _, val in found}
        if len(distinct_values) > 1:
            row[f"{name}_value"] = None
            row[f"{name}_needs_review"] = True
            row[f"{name}_review_reason"] = "conflicting values across notes: " + \
                "; ".join(f"{nid}={val['value']}" for nid, val in found)
            row[f"{name}_note_id"] = ";".join(nid for nid, _ in found)
            row[f"{name}_evidence_quote"] = " | ".join(val["evidence_quote"] or "" for _, val in found)
        elif found:
            nid, val = found[0]
            row[f"{name}_value"] = val["value"]
            row[f"{name}_needs_review"] = val["needs_review"]
            row[f"{name}_review_reason"] = val["review_reason"]
            row[f"{name}_note_id"] = nid
            row[f"{name}_evidence_quote"] = val["evidence_quote"]
        else:
            row[f"{name}_value"] = None
            row[f"{name}_needs_review"] = False
            row[f"{name}_review_reason"] = None
            row[f"{name}_note_id"] = None
            row[f"{name}_evidence_quote"] = None
    return row

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--notes-dir", type=Path, default=Path("notes"))
    ap.add_argument("--codebook", type=Path, default=Path("codebook.md"))
    ap.add_argument("--out-jsonl", type=Path, default=Path("records.jsonl"))
    ap.add_argument("--out-csv", type=Path, default=Path("registry.csv"))
    ap.add_argument("--provenance", type=Path, default=Path("provenance.json"))
    args = ap.parse_args()

    codebook_text = args.codebook.read_text()
    codebook_hash = hashlib.sha256(codebook_text.encode()).hexdigest()
    variables = parse_codebook(args.codebook)
    tool_schema = build_tool_schema(variables)
    system_prompt = build_system_prompt(codebook_text, variables)

    client = Anthropic()
    per_patient = {}
    note_count = 0
    var_found_counts = {v["name"]: 0 for v in variables}

    with args.out_jsonl.open("w") as jsonl_out:
        for patient_dir in sorted(args.notes_dir.iterdir()):
            if not patient_dir.is_dir():
                continue
            patient_id = patient_dir.name
            per_patient.setdefault(patient_id, [])
            for note_path in sorted(patient_dir.glob("*.txt")):
                note_id = note_path.stem
                record = extract_note(client, note_id, note_path.read_text(), system_prompt, tool_schema)
                record = validate_record(record, variables)
                record["patient_id"] = patient_id
                jsonl_out.write(json.dumps(record) + "\n")
                per_patient[patient_id].append(record)
                note_count += 1
                for v in variables:
                    if record[v["name"]]["status"] == "found":
                        var_found_counts[v["name"]] += 1
                time.sleep(0.2)  # keep well under rate limits for a few-hundred-note run

    rows = [aggregate_patient(pid, recs, variables) for pid, recs in per_patient.items()]
    fieldnames = list(rows[0].keys()) if rows else []
    with args.out_csv.open("w", newline="") as csv_out:
        writer = csv.DictWriter(csv_out, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    provenance = {
        "model": MODEL,
        "codebook_path": str(args.codebook),
        "codebook_sha256": codebook_hash,
        "notes_processed": note_count,
        "patients_processed": len(per_patient),
        "variable_found_counts": var_found_counts,
        "needs_review_rows": sum(
            1 for r in rows for v in variables if r.get(f"{v['name']}_needs_review")
        ),
        "run_timestamp_note": "fill in at run time (e.g. `date -u +%FT%TZ`); "
                               "not generated in-script to keep runs byte-reproducible for diffing",
    }
    args.provenance.write_text(json.dumps(provenance, indent=2))
    print(f"Wrote {args.out_jsonl}, {args.out_csv}, {args.provenance}", file=sys.stderr)

if __name__ == "__main__":
    main()
```

`build_tool_schema` is the function shown in section 2 — put it above `main()` in the same file.

```
# requirements.txt
anthropic==0.69.0
```
(pin whatever's current when you set this up — `pip freeze | grep anthropic` after install, commit the exact version.)

Run it with:
```
python extract_registry.py --notes-dir notes/ --codebook codebook.md
```

That's the whole "rerunnable" story: same codebook + same notes + `temperature=0` + a pinned model id and SDK version → the same `registry.csv`, and re-running after a codebook edit or a new batch of notes is the identical command.

## 4. Traceability — where it actually lives

Every non-null cell in `registry.csv` has three sibling columns: `<var>_note_id`, `<var>_evidence_quote`, `<var>_needs_review`. So `diagnosis_value=NSCLC` sits next to `diagnosis_note_id=2026-03-01-oncology-followup` and `diagnosis_evidence_quote="Patient has metastatic NSCLC, adenocarcinoma subtype."` — anyone auditing the table clicks straight to the source sentence. `records.jsonl` keeps the full per-note record (including `not_mentioned`/`negated` variables that don't survive into the flattened CSV) as the underlying audit trail.

## 5. Handling ambiguity, missing data, and conflicts (your requirement 4)

- **Missing**: `status = not_mentioned`, `value = null` — distinct from a documented negative (`status = negated`, e.g. "EGFR wild-type").
- **Ambiguous within one note**: the codebook's global rule instructs the model to set `needs_review = true` with a `review_reason` rather than guessing (e.g., two different stage mentions in one note, or a symptom described in hedged language).
- **Conflicting across a patient's multiple notes**: `aggregate_patient()` explicitly detects when notes disagree on a `found` value, sets `<var>_needs_review = true`, and records both source note IDs and both quotes in the review reason — this is the case a single-note pipeline silently drops.
- **Codebook-schema violations**: `validate_record()` re-checks every value against `allowed_values` server-side rather than trusting the model's enum adherence, flagging anything that slips through.

Downstream, filter `registry.csv` on any `*_needs_review == True` column and route those rows to a human abstractor — that's your review queue, not a failure state.

## 6. QA against a gold standard

Before trusting this on the full cohort, have a clinician manually abstract 20–30 notes independent of the pipeline into a `gold_standard.csv` with the same column names. Then:

```python
import pandas as pd
pred = pd.read_csv("registry.csv").set_index("patient_id")
gold = pd.read_csv("gold_standard.csv").set_index("patient_id")
for var in ["diagnosis", "stage", "prior_lines_of_therapy", "egfr_status", "alk_status", "pdl1_status"]:
    col = f"{var}_value"
    common = pred.index.intersection(gold.index)
    accuracy = (pred.loc[common, col] == gold.loc[common, var]).mean()
    print(f"{var}: accuracy={accuracy:.3f} n={len(common)}")
```
Record per-variable accuracy/F1 in `provenance.json` (add a `gold_validation` key) before the registry is used for any analysis or publication. The published evidence for this recipe (96.2% accuracy on binary ILD variables; F1=0.983 across 10 oncology parameters) is a prior on plausibility, not a substitute for validating your own codebook and notes — different institutions' note styles and a different variable mix can shift these numbers.

## 7. What to commit to version control

`codebook.md`, `extract_registry.py`, `requirements.txt`, `records.jsonl`, `registry.csv`, `gold_standard.csv`, `provenance.json`. That bundle is the reproducible artifact — anyone can re-derive `registry.csv` from `notes/` + `codebook.md` + the pinned script/dependency versions, and `provenance.json` (model id, codebook hash, per-variable found-counts, gold-set accuracy) is what an auditor or reviewer checks first.

## If you outgrow this

Once the registry needs to merge with other cohorts or feed a common data model, layer the separate `harmonize-clinical-terms-to-standard-codes` recipe on top (Medical Terminologies MCP → ICD-11/SNOMED/RxNorm) as a second, independently auditable step — don't fold coding into the extraction prompt itself, since that's exactly how code hallucination creeps in.