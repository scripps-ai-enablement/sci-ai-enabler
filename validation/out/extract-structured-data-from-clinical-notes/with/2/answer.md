Write access isn't granted in this sandbox, so I'll give you the complete scaffold inline — copy each block into the file named above it. This is the full "Extract Structured Variables from Free-Text Clinical Notes" recipe (evidence: **Validated** — Chen et al. 2026 report 96.2% accuracy for Claude 3.5 Sonnet on binary clinical-variable extraction, matching human clinicians; Bhayana et al. 2025 report F1=0.983 on 10 oncologic parameters from 200 EHR notes — but those numbers are for *their* codebooks and notes, not yours; step 5 below is how you get your own number). Availability: fully open, no MCP/plugin needed. Compute: laptop, ~$0.001–0.11/note, a few hundred notes in minutes.

## Architecture

```
notes/                      your de-identified .txt notes (input, unchanged)
codebook.yaml                the spec — versioned, drives everything downstream
extract_registry.py          committed extraction script (the reproducible artifact)
reconcile.py                 note-level records -> one row per patient, conflict-flagged
validate_gold.py             accuracy/F1 against a clinician-abstracted subset
requirements.txt             pinned environment
records.jsonl                one row per (note, field) — the audit trail
registry.csv                 one row per patient — the deliverable table
provenance.json              what ran, on what, with what result
```

Two extraction granularities matter here because you have multiple notes per patient: extract at the **note** level first (so every value stays pinned to one `note_id`), then **reconcile** to the patient level as a separate, auditable step that surfaces conflicts instead of silently picking one.

### 1. `codebook.yaml` — the spec

```yaml
# Version-control this file. Its SHA256 goes into provenance.json on every run,
# so a change in abstraction rules is auditable against past registries.
version: 1
fields:
  diagnosis:
    type: categorical
    allowed_values:
      - "NSCLC - adenocarcinoma"
      - "NSCLC - squamous cell"
      - "NSCLC - NOS"
      - "SCLC"
      - "other/unspecified"
    extraction_rule: >
      The primary oncologic diagnosis as explicitly stated by the treating
      clinician. Use "other/unspecified" if a cancer diagnosis is present but
      doesn't map to the listed histologies. Never infer histology from
      treatment alone (e.g. don't infer NSCLC just because osimertinib is
      mentioned).

  stage:
    type: categorical
    allowed_values: ["I", "II", "III", "IV", "not staged"]
    extraction_rule: >
      Overall clinical/pathologic stage GROUP at the time of this note
      (AJCC-style, not full TNM). If only TNM is given, do not derive the
      group yourself — mark "not staged" for human review.

  prior_lines_of_therapy:
    type: numeric
    unit: count
    extraction_rule: >
      Integer count of distinct systemic regimens before the therapy
      discussed in this note. A regimen switch counts as one line; a dose
      change or cycle continuation does not. If treatment history isn't
      discussed, mark not_mentioned — never estimate from time since diagnosis.

  egfr_status:
    type: categorical
    allowed_values: ["positive", "negative", "not tested", "pending"]
    extraction_rule: >
      EGFR mutation test result as stated in the text. "pending" only if the
      note explicitly says testing was sent and result isn't back.

  acute_symptoms:
    type: multi_select
    allowed_values:
      - "dyspnea"
      - "chest pain"
      - "fever"
      - "hemoptysis"
      - "altered mental status"
      - "hypotension"
    extraction_rule: >
      Symptoms explicitly documented as present AT THIS ENCOUNTER (HPI, ROS,
      exam) — not past medical history. Every listed symptom gets its own
      found/negated/not_mentioned status: "denies fever, denies hemoptysis"
      must mark those negated, not omitted.
```

Swap in your real fields/values — this file is the contract everything below enforces against, and the thing your clinician reviewer signs off on.

### 2. `extract_registry.py` — the committed extraction script

Key design choices, and why:
- **Forced tool-call output**, not free text — Claude must call a schema-shaped tool, so `evidence_quote`/`status` fields can't be skipped or reformatted differently note to note.
- **Post-hoc quote verification** — after the model returns, the script checks that `evidence_quote` is an actual (whitespace-normalized) substring of the source note. If it isn't, the script overrides the status to `quote_unverified` regardless of what the model claimed — this is what makes "traceable to a quoted sentence" a guarantee enforced by code, not a request made to the model.
- **Never infer past `not_mentioned`** — the codebook rule text plus a system-prompt instruction forbid guessing; `null` + `not_mentioned` is the required output when the note is silent.

```python
#!/usr/bin/env python3
"""Extract codebook-defined variables from clinical notes into records.jsonl.
Usage: python extract_registry.py --notes-dir notes/ --codebook codebook.yaml
"""
import argparse, hashlib, json, re, sys
from pathlib import Path
from datetime import datetime, timezone

import yaml
from anthropic import Anthropic

MODEL = "claude-sonnet-5"  # pin explicitly; record in provenance.json


def load_codebook(path):
    text = Path(path).read_text()
    sha256 = hashlib.sha256(text.encode()).hexdigest()
    return yaml.safe_load(text), sha256


def parse_note(path):
    """Notes start with '# patient_id: X' and '# note_id: Y' header lines,
    followed by a blank line, then free text. Falls back to filename
    'patientid_noteid.txt' if headers are absent."""
    raw = path.read_text()
    m_pid = re.search(r"^#\s*patient_id:\s*(\S+)", raw, re.MULTILINE)
    m_nid = re.search(r"^#\s*note_id:\s*(\S+)", raw, re.MULTILINE)
    if m_pid and m_nid:
        body = re.sub(r"^#.*\n", "", raw, flags=re.MULTILINE).strip()
        return m_pid.group(1), m_nid.group(1), body
    stem = path.stem
    if "_" not in stem:
        raise ValueError(f"{path}: no header lines and no '_' in filename to split patient_id/note_id")
    pid, nid = stem.split("_", 1)
    return pid, nid, raw.strip()


def build_tool_schema(codebook):
    props = {}
    for name, spec in codebook["fields"].items():
        if spec["type"] == "multi_select":
            props[name] = {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "symptom": {"type": "string", "enum": spec["allowed_values"]},
                        "status": {"type": "string", "enum": ["found", "negated", "not_mentioned"]},
                        "evidence_quote": {"type": ["string", "null"]},
                    },
                    "required": ["symptom", "status", "evidence_quote"],
                },
            }
        else:
            value_type = {"categorical": "string", "numeric": "number"}[spec["type"]]
            props[name] = {
                "type": "object",
                "properties": {
                    "value": {"type": [value_type, "null"]},
                    "status": {"type": "string", "enum": ["found", "negated", "not_mentioned"]},
                    "evidence_quote": {"type": ["string", "null"]},
                },
                "required": ["value", "status", "evidence_quote"],
            }
    return {
        "name": "record_extraction",
        "description": "Structured extraction of codebook variables from one clinical note.",
        "input_schema": {"type": "object", "properties": props, "required": list(props)},
    }


def build_system_prompt(codebook):
    lines = [
        "You are abstracting structured data from ONE de-identified clinical note",
        "for a research registry. Follow these rules exactly:",
        "- Use ONLY the allowed values given for each field. Never invent a value.",
        "- If the note does not explicitly state something, set status=not_mentioned",
        "  and value=null. Do not infer from context, treatment choice, or typical",
        "  disease course.",
        "- If the note explicitly denies/rules something out, set status=negated.",
        "- Every non-null value AND every negated finding must carry an",
        "  evidence_quote that is a VERBATIM sentence or clause copied from the",
        "  note text — not a paraphrase, not a summary.",
        "",
        "Codebook:",
    ]
    for name, spec in codebook["fields"].items():
        lines.append(f"\nField: {name} ({spec['type']})")
        if "allowed_values" in spec:
            lines.append(f"  Allowed values: {spec['allowed_values']}")
        lines.append(f"  Rule: {spec['extraction_rule'].strip()}")
    return "\n".join(lines)


def normalize(s):
    return re.sub(r"\s+", " ", s or "").strip().lower()


def verify_quote(quote, note_text):
    return bool(quote) and normalize(quote) in normalize(note_text)


def extract_note(client, codebook, tool_schema, system_prompt, note_text):
    resp = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        system=system_prompt,
        tools=[tool_schema],
        tool_choice={"type": "tool", "name": "record_extraction"},
        messages=[{"role": "user", "content": f"<note>\n{note_text}\n</note>"}],
    )
    for block in resp.content:
        if block.type == "tool_use":
            return block.input
    raise RuntimeError("model did not return a tool_use block")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--notes-dir", default="notes")
    ap.add_argument("--codebook", default="codebook.yaml")
    ap.add_argument("--out", default="records.jsonl")
    args = ap.parse_args()

    codebook, codebook_sha = load_codebook(args.codebook)
    tool_schema = build_tool_schema(codebook)
    system_prompt = build_system_prompt(codebook)
    client = Anthropic()

    note_paths = sorted(Path(args.notes_dir).glob("*.txt"))
    if not note_paths:
        sys.exit(f"no .txt files found in {args.notes_dir}")

    counts = {}
    with open(args.out, "w") as out_f:
        for path in note_paths:
            patient_id, note_id, note_text = parse_note(path)
            note_sha = hashlib.sha256(note_text.encode()).hexdigest()
            result = extract_note(client, codebook, tool_schema, system_prompt, note_text)

            for field_name, spec in codebook["fields"].items():
                field_result = result.get(field_name)
                if spec["type"] == "multi_select":
                    for item in field_result or []:
                        verified = verify_quote(item.get("evidence_quote"), note_text)
                        status = item["status"] if verified or item["status"] == "not_mentioned" else "quote_unverified"
                        row = {
                            "patient_id": patient_id, "note_id": note_id, "note_sha256": note_sha,
                            "field": field_name, "sub_value": item["symptom"],
                            "status": status, "evidence_quote": item.get("evidence_quote"),
                            "quote_verified": verified,
                        }
                        out_f.write(json.dumps(row) + "\n")
                        counts.setdefault(f"{field_name}:{item['symptom']}", {}).setdefault(status, 0)
                        counts[f"{field_name}:{item['symptom']}"][status] += 1
                else:
                    verified = verify_quote(field_result.get("evidence_quote"), note_text)
                    status = field_result["status"] if verified or field_result["status"] == "not_mentioned" else "quote_unverified"
                    row = {
                        "patient_id": patient_id, "note_id": note_id, "note_sha256": note_sha,
                        "field": field_name, "value": field_result["value"],
                        "status": status, "evidence_quote": field_result.get("evidence_quote"),
                        "quote_verified": verified,
                    }
                    out_f.write(json.dumps(row) + "\n")
                    counts.setdefault(field_name, {}).setdefault(status, 0)
                    counts[field_name][status] += 1

    provenance = {
        "model": MODEL,
        "codebook_sha256": codebook_sha,
        "notes_processed": len(note_paths),
        "run_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "per_field_status_counts": counts,
    }
    Path("provenance.json").write_text(json.dumps(provenance, indent=2))
    print(f"wrote {args.out} and provenance.json from {len(note_paths)} notes")


if __name__ == "__main__":
    main()
```

### 3. `reconcile.py` — note-level records → one row per patient

```python
#!/usr/bin/env python3
"""Collapse records.jsonl (one row per note x field) into registry.csv
(one row per patient), flagging any field where notes for the same
patient disagree instead of silently picking one."""
import json, sys
from collections import defaultdict
import pandas as pd

def reconcile(records_path="records.jsonl", out_path="registry.csv"):
    by_patient_field = defaultdict(list)
    for line in open(records_path):
        r = json.loads(line)
        key = (r["patient_id"], r["field"], r.get("sub_value"))
        by_patient_field[key].append(r)

    rows = defaultdict(dict)
    review_flags = defaultdict(list)

    for (patient_id, field, sub_value), recs in by_patient_field.items():
        col = f"{field}__{sub_value}" if sub_value else field
        found = [r for r in recs if r["status"] == "found"]
        unverified = [r for r in recs if r["status"] == "quote_unverified"]
        distinct_values = {r.get("value") for r in found}

        if unverified:
            review_flags[patient_id].append(f"{col}: quote failed verification (note {unverified[0]['note_id']})")
            rows[patient_id][col] = None
        elif len(distinct_values) > 1:
            review_flags[patient_id].append(
                f"{col}: conflicting values across notes -> " +
                "; ".join(f"{r['value']} ({r['note_id']})" for r in found)
            )
            rows[patient_id][col] = None
        elif found:
            rows[patient_id][col] = found[0]["value"]
            rows[patient_id][f"{col}__note_id"] = found[0]["note_id"]
            rows[patient_id][f"{col}__evidence"] = found[0]["evidence_quote"]
        else:
            negated = [r for r in recs if r["status"] == "negated"]
            rows[patient_id][col] = "negated" if negated else None

    for patient_id, flags in review_flags.items():
        rows[patient_id]["_review_needed"] = " | ".join(flags)

    df = pd.DataFrame.from_dict(rows, orient="index").sort_index()
    df.index.name = "patient_id"
    df.to_csv(out_path)
    print(f"wrote {out_path}: {len(df)} patients, "
          f"{sum(1 for f in review_flags.values() if f)} flagged for review")

if __name__ == "__main__":
    reconcile()
```

### 4. `validate_gold.py` — the step that earns trust for *your* codebook

The Chen/Bhayana numbers above are evidence the *task* works on Claude; they say nothing about your notes' style or your codebook's edge cases. Have a clinician manually abstract 20–30 notes into `gold.csv` (same columns as `registry.csv`), then:

```python
#!/usr/bin/env python3
"""Compare registry.csv against a clinician-abstracted gold.csv subset;
append per-field accuracy to provenance.json."""
import json
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score

def validate(registry_path="registry.csv", gold_path="gold.csv"):
    reg = pd.read_csv(registry_path).set_index("patient_id")
    gold = pd.read_csv(gold_path).set_index("patient_id")
    common = reg.index.intersection(gold.index)
    metrics = {}
    for col in gold.columns:
        if col not in reg.columns:
            continue
        y_true = gold.loc[common, col].astype(str)
        y_pred = reg.loc[common, col].astype(str)
        metrics[col] = {
            "accuracy": round(accuracy_score(y_true, y_pred), 4),
            "n": len(common),
        }
        if y_true.nunique() <= 10:
            metrics[col]["f1_macro"] = round(f1_score(y_true, y_pred, average="macro"), 4)

    prov = json.load(open("provenance.json"))
    prov["gold_validation"] = metrics
    json.dump(prov, open("provenance.json", "w"), indent=2)
    print(json.dumps(metrics, indent=2))

if __name__ == "__main__":
    validate()
```

### 5. `requirements.txt`

```
anthropic>=0.40
pyyaml
pandas
scikit-learn
```
After first install, run `pip freeze > requirements.lock.txt` and commit the lock file — that's the actual pin, not the loose spec above.

### 6. Run order

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=...
python extract_registry.py --notes-dir notes/ --codebook codebook.yaml
python reconcile.py
python validate_gold.py   # after a clinician fills gold.csv for 20-30 notes
git add codebook.yaml extract_registry.py reconcile.py validate_gold.py \
        requirements.txt requirements.lock.txt records.jsonl registry.csv provenance.json
git commit -m "clinical registry extraction run"
```

Everything downstream of `codebook.yaml` is deterministic given the same notes + same model version, and every cell in `registry.csv` links back through `records.jsonl` to a `note_id`, a `note_sha256`, and a verbatim `evidence_quote` — verified by code against the source text, not just asserted by the model. `_review_needed` in `registry.csv` is your human-review queue: cross-note conflicts and failed quote verifications land there instead of being silently resolved.

**Optional convenience wrapper** — a `.claude/commands/run-extraction.md` that just shells out to `python extract_registry.py && python reconcile.py` so you can type `/run-extraction` after adding new notes. That's a shortcut to re-invoke the pipeline, not the reproducible record itself — the committed script + lock file + `provenance.json` are what actually make a run auditable and repeatable.

**What I didn't do**: this sandbox has no file-write permission and no notes/API key, so I couldn't create these files or run them against real input — you'll need to paste them in and run the commands above yourself. Also decide your model/data-tier question (BAA / zero-retention) before pointing this at real notes; that's an institutional call, not a technical one.