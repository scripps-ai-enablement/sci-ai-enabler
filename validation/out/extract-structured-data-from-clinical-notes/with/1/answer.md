File writes aren't being permitted in this sandbox, so I'll deliver the complete solution inline instead — you can drop each block into files in your own environment.

## The answer, in one line

This matches a validated recipe in the sci-ai-enabler catalog: **use Claude Code alone** (no MCP/Skill needed) to run a fixed codebook against your notes folder, forcing structured output with a verbatim evidence quote on every cell, then commit the whole thing as a script + provenance record rather than a chat transcript.

- **Evidence label:** Validated — Chen et al. (2026) benchmarked Claude 3.5 Sonnet on 100 interstitial-lung-disease notes at 96.2% accuracy (matching human clinicians); Bhayana et al. (2025) hit F1=0.983 on oncologic parameter extraction with radiologists preferring the LLM output 89% vs 5%.
- **Availability:** Fully open (Claude Code + Anthropic API only, no special access needed).
- **Compute:** Laptop-sufficient — ~1–2 sec/note, ~$0.001–0.01/note, a few hundred notes finish in minutes.
- **Why not a lower rung:** plain prompting in a chat window (rung 1 with no artifact) can't give you a rerunnable, auditable pipeline — you need the extraction *and* the citation *and* the script committed together, which is what this recipe's structure buys you.

## Assumptions I'm making (state these back to yourself before running)

1. **Note storage:** one plain-text file per note under `./notes/`, plus a `notes_manifest.csv` mapping `note_id → patient_id, filepath, note_date, note_type` (pathology / oncology_consult / progress / nursing) — because a manifest is more robust than parsing patient/date out of filenames, and you said "one or more notes per patient," so you need an explicit note→patient join.
2. **Cohort:** mixed solid-tumor oncology, not one cancer type — so `diagnosis` uses a small controlled vocabulary with an `Other (specify verbatim)` escape hatch rather than a full ICD-O-3 table.
3. **Biomarker:** I picked PD-L1 as the concrete example (broadly relevant, immunotherapy-actionable across tumor types) — swap the name in `codebook.md` for whatever your registry actually tracks (HER2, EGFR, ALK, MSI...).
4. **Stage:** AJCC overall stage group (I–IV), not full TNM — if notes only give TNM, that's marked `Unknown/Not documented` with the raw TNM string preserved in the evidence quote for a human to regroup.
5. **Prior lines of therapy:** a "line" = a distinct systemic regimen stopped/changed for progression or intolerance, not each cycle.
6. **Tech stack:** Python 3.11+, `anthropic` SDK, `pandas`, `pyyaml` — no database, CSV/JSONL outputs.

## 1. `codebook.md` — the fixed rulebook (single source of truth)

This is both the human-readable rulebook and the machine-readable schema (the script parses the YAML block). Version-control this file; every registry run should cite its SHA256.

```markdown
# Registry Codebook

**Assumption:** mixed solid-tumor oncology cohort. Swap `diagnosis.allowed_values`, the biomarker
name, and `acute_symptoms.allowed_values` for your actual cohort.

​```yaml
schema_version: 1
variables:
  diagnosis:
    type: categorical
    multi_label: false
    allowed_values:
      - "Invasive ductal carcinoma"
      - "Invasive lobular carcinoma"
      - "Adenocarcinoma NOS"
      - "Squamous cell carcinoma"
      - "Small cell carcinoma"
      - "Non-small cell carcinoma NOS"
      - "Other (specify verbatim in evidence_quote)"
      - "Not documented"
  stage:
    type: categorical
    multi_label: false
    allowed_values: ["I", "II", "III", "IV", "Unknown/Not documented"]
  prior_lines_of_therapy:
    type: categorical
    multi_label: false
    allowed_values: ["0", "1", "2", "3+", "Unknown/Not documented"]
  biomarker_status:
    type: categorical
    multi_label: false
    biomarker_name: "PD-L1"   # swap for HER2 / EGFR / ALK / MSI / your actual biomarker
    allowed_values: ["Positive", "Negative", "Equivocal", "Not tested", "Not applicable", "Not documented"]
  acute_symptoms:
    type: categorical
    multi_label: true
    allowed_values:
      - "Fever"
      - "Dyspnea"
      - "Chest pain"
      - "Altered mental status"
      - "Severe/uncontrolled pain"
      - "Active bleeding"
      - "Hypotension/shock"
      - "Seizure"
      - "Other (specify verbatim in evidence_quote)"
​```

## Abstraction rules

### General
- Every variable is addressed for every note, even when the answer is "not mentioned" — a missing
  row is a pipeline bug, not a valid "no data" signal.
- `evidence_quote` must be a **verbatim sentence/clause copied from the note**, not a paraphrase.
  The pipeline mechanically rejects rows whose quote doesn't appear in the source text (hallucination
  guard — see script).
- Status values: `found`, `negated` (explicitly denied — keep the row), `not_mentioned`,
  `not_applicable`.

### `diagnosis` / `stage`
- Priority order when notes disagree: pathology report > oncology consult > progress note >
  nursing/triage note. A later progress note repeating an old diagnosis never outranks the pathology
  report that established it.
- `stage` = AJCC overall stage group (I–IV). TNM-only mentions → `Unknown/Not documented`, with the
  raw TNM string preserved in the evidence quote.

### `prior_lines_of_therapy`
- A "line" = a distinct systemic regimen stopped/changed due to progression or intolerance — not
  each cycle. Count only regimens completed/discontinued *before* the index note's date.
- If regimen boundaries are ambiguous, take the lower bound and append `[ambiguous count]` to the
  evidence context so it surfaces in review.

### `biomarker_status`
- `Not tested`: clinically relevant, not (yet) performed or no resulted value in any note.
- `Not applicable`: note explicitly states testing doesn't apply to this histology.
- `Not documented`: no mention at all.

### `acute_symptoms`
- Multi-label: one extraction row per symptom the note *actively addresses* (positive or negated).
  No row = not_mentioned by construction.
- Negated symptoms ("denies chest pain") are excluded from the positive list but kept in
  `records.jsonl` with status `negated` for audit.

## Cross-note conflict resolution (same patient, same variable)
1. Prefer the most recent note by `note_date`.
2. For `diagnosis`/`stage`, apply note-type priority *before* recency.
3. If two notes of equal priority and the same/indeterminate date disagree, do not auto-pick — mark
   `CONFLICT` in `registry.csv` and list both citations in `conflicts.csv` for human adjudication.

## Not documented vs. not applicable
- `Not documented`: in scope, no supporting statement anywhere in the patient's notes.
- `Not applicable`: explicitly out of scope given documented clinical context (used for
  `biomarker_status`; other variables here are always in scope).
```

## 2. `notes_manifest.csv` — the note→patient join

```csv
patient_id,note_id,filepath,note_date,note_type
P001,P001_N1,notes/P001_N1.txt,2026-02-03,pathology
P001,P001_N2,notes/P001_N2.txt,2026-03-15,oncology_consult
P001,P001_N3,notes/P001_N3.txt,2026-05-01,progress
P002,P002_N1,notes/P002_N1.txt,2026-01-20,oncology_consult
```

## 3. `extract_registry.py` — the reusable, rerunnable pipeline

```python
#!/usr/bin/env python3
"""Extract a codebook-defined registry from de-identified clinical notes, with
per-cell provenance. Usage:
    python extract_registry.py extract   --manifest notes_manifest.csv --codebook codebook.md
    python extract_registry.py aggregate --manifest notes_manifest.csv --codebook codebook.md
    python extract_registry.py validate-gold --gold gold.csv
"""
import argparse, csv, hashlib, json, os, re, sys
from collections import defaultdict
from datetime import datetime, timezone

import yaml

MODEL = "claude-sonnet-5"
NOTE_TYPE_PRIORITY = {"pathology": 0, "oncology_consult": 1, "progress": 2, "nursing": 3}


def load_codebook(path):
    text = open(path, encoding="utf-8").read()
    m = re.search(r"```yaml\n(.*?)\n```", text, re.S)
    if not m:
        sys.exit(f"No yaml schema block found in {path}")
    schema = yaml.safe_load(m.group(1))
    return schema["variables"], text, hashlib.sha256(text.encode()).hexdigest()


def build_tool_schema(variables):
    return {
        "name": "submit_note_extraction",
        "description": "Record every codebook variable this note addresses, with a verbatim citation.",
        "input_schema": {
            "type": "object",
            "properties": {
                "note_id": {"type": "string"},
                "extractions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "variable": {"type": "string", "enum": list(variables.keys())},
                            "value": {"type": "string"},
                            "status": {
                                "type": "string",
                                "enum": ["found", "negated", "not_mentioned", "not_applicable"],
                            },
                            "evidence_quote": {"type": "string"},
                        },
                        "required": ["variable", "value", "status", "evidence_quote"],
                    },
                },
            },
            "required": ["note_id", "extractions"],
        },
    }


def normalize(s):
    return re.sub(r"\s+", " ", s).strip().lower()


def call_claude(client, codebook_text, note_id, note_text, tool_schema):
    resp = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        system=(
            "You are abstracting one clinical note against a fixed codebook. "
            "Follow every rule in the codebook exactly. Quote evidence verbatim — "
            "copy characters directly from the note, do not paraphrase.\n\n" + codebook_text
        ),
        tools=[tool_schema],
        tool_choice={"type": "tool", "name": "submit_note_extraction"},
        messages=[{"role": "user", "content": f"note_id: {note_id}\n\n{note_text}"}],
    )
    for block in resp.content:
        if block.type == "tool_use":
            return block.input
    sys.exit(f"No tool_use block returned for {note_id}")


def extract(args):
    variables, codebook_text, codebook_hash = load_codebook(args.codebook)
    tool_schema = build_tool_schema(variables)

    import anthropic
    client = anthropic.Anthropic()

    rows = []
    counts = defaultdict(lambda: defaultdict(int))
    with open(args.manifest, newline="", encoding="utf-8") as f:
        manifest_rows = list(csv.DictReader(f))

    for m in manifest_rows:
        note_text = open(m["filepath"], encoding="utf-8").read()
        result = call_claude(client, codebook_text, m["note_id"], note_text, tool_schema)
        for ext in result["extractions"]:
            var = variables.get(ext["variable"])
            issues = []
            if var and var.get("allowed_values") and ext["status"] in ("found", "negated"):
                if ext["value"] not in var["allowed_values"]:
                    issues.append("invalid_value")
            if ext["status"] in ("found", "negated") and ext["evidence_quote"]:
                if normalize(ext["evidence_quote"]) not in normalize(note_text):
                    issues.append("quote_mismatch")  # citation didn't come from this note verbatim
            row = {
                "patient_id": m["patient_id"],
                "note_id": m["note_id"],
                "note_date": m["note_date"],
                "note_type": m["note_type"],
                "variable": ext["variable"],
                "value": ext["value"],
                "status": "needs_review" if issues else ext["status"],
                "evidence_quote": ext["evidence_quote"],
                "issues": issues,
            }
            rows.append(row)
            counts[ext["variable"]][row["status"]] += 1

    with open("records.jsonl", "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")

    provenance = {
        "model": MODEL,
        "codebook_sha256": codebook_hash,
        "note_count": len(manifest_rows),
        "run_utc": datetime.now(timezone.utc).isoformat(),
        "extraction_counts": counts,
    }
    with open("provenance.json", "w", encoding="utf-8") as f:
        json.dump(provenance, f, indent=2)
    print(f"Wrote records.jsonl ({len(rows)} rows) and provenance.json")


def aggregate(args):
    variables, _, _ = load_codebook(args.codebook)
    with open(args.manifest, newline="", encoding="utf-8") as f:
        note_meta = {m["note_id"]: m for m in csv.DictReader(f)}

    records = [json.loads(l) for l in open("records.jsonl", encoding="utf-8")]
    by_patient_var = defaultdict(list)
    for r in records:
        by_patient_var[(r["patient_id"], r["variable"])].append(r)

    def sort_key(r):
        nt = note_meta[r["note_id"]]["note_type"]
        return (NOTE_TYPE_PRIORITY.get(nt, 99), r["note_date"])  # priority first, then chronology

    conflicts = []
    registry = defaultdict(dict)
    symptom_rows = []

    for (patient_id, variable), recs in by_patient_var.items():
        var_def = variables[variable]
        if var_def.get("multi_label"):
            positives = {r["value"]: r for r in recs if r["status"] == "found"}
            registry[patient_id][variable] = "; ".join(sorted(positives)) or "None documented"
            for val, r in positives.items():
                symptom_rows.append({**r, "patient_id": patient_id})
            continue

        found = [r for r in recs if r["status"] == "found"]
        if not found:
            registry[patient_id][variable] = "Not documented"
            continue

        is_priority_var = variable in ("diagnosis", "stage")
        found.sort(key=sort_key if is_priority_var else (lambda r: r["note_date"]), reverse=True)
        top_rank = sort_key(found[0]) if is_priority_var else found[0]["note_date"]
        top_tier = [r for r in found if (sort_key(r) if is_priority_var else r["note_date"]) == top_rank]
        distinct_values = {r["value"] for r in top_tier}

        if len(distinct_values) > 1:
            registry[patient_id][variable] = "CONFLICT"
            conflicts.append({"patient_id": patient_id, "variable": variable, "candidates": top_tier})
        else:
            winner = top_tier[0]
            registry[patient_id][variable] = winner["value"]
            registry[patient_id][f"{variable}_note_id"] = winner["note_id"]
            registry[patient_id][f"{variable}_evidence_quote"] = winner["evidence_quote"]

    fieldnames = ["patient_id"] + [
        c for v in variables for c in (
            [v] if variables[v].get("multi_label") else [v, f"{v}_note_id", f"{v}_evidence_quote"]
        )
    ]
    with open("registry.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for patient_id, row in registry.items():
            w.writerow({"patient_id": patient_id, **row})

    with open("symptoms_evidence.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["patient_id", "note_id", "value", "evidence_quote"])
        w.writeheader()
        for r in symptom_rows:
            w.writerow({k: r[k] for k in w.fieldnames})

    with open("conflicts.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["patient_id", "variable", "note_id", "value", "evidence_quote"])
        w.writeheader()
        for c in conflicts:
            for cand in c["candidates"]:
                w.writerow({"patient_id": c["patient_id"], "variable": c["variable"],
                            "note_id": cand["note_id"], "value": cand["value"],
                            "evidence_quote": cand["evidence_quote"]})

    print(f"Wrote registry.csv ({len(registry)} patients), "
          f"symptoms_evidence.csv ({len(symptom_rows)} rows), "
          f"conflicts.csv ({len(conflicts)} conflicts)")


def validate_gold(args):
    gold = list(csv.DictReader(open(args.gold, encoding="utf-8")))
    registry = {r["patient_id"]: r for r in csv.DictReader(open("registry.csv", encoding="utf-8"))}
    variables = [c for c in gold[0] if c != "patient_id"]
    report = {}
    for var in variables:
        correct = total = 0
        for g in gold:
            pid = g["patient_id"]
            if pid not in registry:
                continue
            total += 1
            if registry[pid].get(var, "").strip().lower() == g[var].strip().lower():
                correct += 1
        report[var] = {"n": total, "accuracy": round(correct / total, 3) if total else None}
    prov = json.load(open("provenance.json", encoding="utf-8"))
    prov["gold_validation"] = {"gold_file": args.gold, "n_gold_notes": len(gold), "per_variable": report}
    json.dump(prov, open("provenance.json", "w", encoding="utf-8"), indent=2)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    for name, fn in [("extract", extract), ("aggregate", aggregate), ("validate-gold", validate_gold)]:
        sp = sub.add_parser(name)
        sp.add_argument("--manifest", default="notes_manifest.csv")
        sp.add_argument("--codebook", default="codebook.md")
        sp.add_argument("--gold")
        sp.set_defaults(func=fn)
    args = p.parse_args()
    args.func(args)
```

```text
# requirements.txt
anthropic>=0.40
pyyaml>=6.0
```

## How traceability actually holds up

- Every cell in `registry.csv` carries a `<variable>_note_id` and `<variable>_evidence_quote` column pointing at the exact source sentence — for multi-label `acute_symptoms`, the per-symptom citations live in `symptoms_evidence.csv` since one cell can't hold N citations.
- The script doesn't trust Claude's citation on faith: `normalize(quote) not in normalize(note_text)` catches paraphrased or fabricated quotes and reroutes the row to `status=needs_review` instead of silently writing a plausible-looking but unverifiable cell. This is the load-bearing check for "traceable" — without it you have a citation-shaped string, not a citation.
- `records.jsonl` is the full, ungrouped audit trail (every note × every variable, including `not_mentioned` and `negated` rows); `registry.csv` is the flattened, human-facing view. Never delete the former.

## Rerunnability

- `codebook.md` is the single source of truth — plain text, diffable, version-controlled. Changing a rule means editing this file, not re-prompting by hand.
- `provenance.json` records the model ID, the codebook's SHA256, note count, run timestamp, and per-variable status counts — so a rerun after a codebook edit is a diffable, auditable event, not a silent replacement.
- Rerun end-to-end anytime with `python extract_registry.py extract && python extract_registry.py aggregate`. Note: LLM outputs are not byte-reproducible run-to-run — the provenance pinning (model ID + codebook hash) is what makes a run *auditable and re-attemptable*, not bit-identical. If you need stricter reproducibility, pin a dated model snapshot ID instead of a rolling alias.

## Validation strategy (no gold labels exist yet)

1. Pull a **random 20–30 note sample** (stratify by note_type/diagnosis if your cohort is skewed) and have a clinician manually abstract just those against the same `codebook.md` into `gold.csv` (same column names as `registry.csv`).
2. Run `python extract_registry.py validate-gold --gold gold.csv` — appends per-variable accuracy to `provenance.json`. Published benchmarks on comparable oncology-note extraction land at 96–98% accuracy / F1≈0.98, so treat anything markedly lower on your data as a signal to sharpen the codebook wording (usually the fix, per Bhayana et al. and Chen et al., is disambiguating the rule text, not the model).
3. Independent of gold-labeling, triage every row the pipeline itself flagged: `status=needs_review` (quote mismatch or invalid value) and every row in `conflicts.csv` — these are exactly the cells where the model told you it's unsure, so review them first regardless of overall accuracy.
4. Re-run validation after every non-trivial codebook edit; commit the resulting `provenance.json` alongside `registry.csv` so anyone reading the table later can see what was checked and when.

## Caveats

- This registry is a research artifact, not a clinical record — a clinician needs to sign off before any of it feeds patient care decisions.
- The pipeline needs `ANTHROPIC_API_KEY` set and network access; confirm your institution's data-use agreement and API tier cover the sensitivity level of your (de-identified) notes before running real data through it.
- If you'd like this harmonized further — mapping the free-text `diagnosis`/`biomarker` values to ICD-11/SNOMED codes — that's a second, separable recipe (`harmonize-clinical-terms-to-standard-codes`, via a terminology MCP) layered on top of `registry.csv`, not a reason to complicate this pipeline.

Since this composition matches an existing curated recipe rather than surfacing a gap, there's nothing to file to the knowledge-base curators this time — you're set to run this as-is.