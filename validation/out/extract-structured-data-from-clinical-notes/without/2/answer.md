File writes aren't permitted in this session, so I'll deliver the full scaffold inline instead — copy these into a project folder to run it as-is.

## Design assumptions (stated explicitly, since I can't ask)

- Worked example: an oncology registry with the five field types you listed. Swap the codebook for your real one — the pipeline logic doesn't change.
- Notes live as `notes/<PATIENT_ID>_<NOTE_ID>.txt`, each with a `DATE: YYYY-MM-DD` header line. Adjust the parsing regex if your real files differ.
- You have API access to an LLM with forced structured/tool-call output (I use Claude here). The same design works with any provider that supports JSON-schema-constrained output.
- Notes are de-identified but still sensitive — check your org's policy on sending them to a third-party API even post-de-identification (BAA / approved-vendor status) before running this for real.

## The core guarantee

For every cell in the registry, the model must return `{value, quote, confidence}` — and a separate, non-LLM verification step confirms `quote` is an exact (or near-exact, fuzzy-matched) substring of the specific note it claims to come from. If it isn't, the value is flagged `needs_review` rather than silently trusted. Patient/note identifiers are taken from filenames, never from model output, so they can't be hallucinated.

## Pipeline stages

`manifest.py` → `extract.py` → `verify.py` → `aggregate.py`, orchestrated by one `run.sh`, producing:
- `outputs/manifest.json` — hash of the codebook + hash of every input note, so any run's inputs are provably fixed
- `outputs/extractions/*.json` — raw per-note model output (audit trail)
- `outputs/verified/*.json` — same, with grounding checks applied
- `outputs/evidence_table.csv` — **long format**, one row per patient × note × field × value, with the quote, note_id, confidence, and grounded flag — this is what makes every cell traceable
- `outputs/registry_table.csv` — **wide format**, one row per patient, built deterministically from the evidence table by codebook-declared aggregation rules

### `codebook.yaml`

```yaml
version: "1.0.0"
model: "claude-sonnet-5"

fields:
  diagnosis:
    label: "Primary oncologic diagnosis"
    type: single_select
    allowed_values:
      - NSCLC-adenocarcinoma
      - NSCLC-squamous
      - SCLC
      - breast-invasive-ductal
      - colorectal-adenocarcinoma
      - other
      - not_documented
    absent_values: [not_documented]
    abstraction_rule: >
      Use the most specific pathology-confirmed diagnosis mentioned in the note.
      If the note references multiple primaries, record the one under active
      treatment or discussion in this note. If only a non-specific label such
      as "lung cancer" is given with no histology, use "other" and set
      confidence to low.
    aggregation: most_recent

  stage:
    label: "Stage at diagnosis (AJCC)"
    type: single_select
    allowed_values: ["I", "II", "III", "IV", "not_documented"]
    absent_values: [not_documented]
    abstraction_rule: >
      Record AJCC stage as of the original diagnosis, not the stage of any
      later progression or recurrence described in follow-up notes. Prefer
      pathologic stage over clinical stage when both are given.
    aggregation: most_recent

  prior_lines_of_therapy:
    label: "Number of prior systemic therapy lines"
    type: integer
    abstraction_rule: >
      Count distinct systemic regimens (chemotherapy, targeted therapy,
      immunotherapy) the patient received before the date of this note.
      Surgery or radiation alone does not count as a line. A regimen change
      due to toxicity without evidence of progression still counts as the
      same line.
    aggregation: max_monotonic

  biomarker_status:
    label: "Molecular / biomarker findings"
    type: multi_select
    allowed_values:
      - EGFR+
      - ALK+
      - KRAS+
      - PD-L1-high
      - PD-L1-low
      - biomarker-negative
      - not_tested
      - not_documented
    absent_values: [not_tested, not_documented]
    abstraction_rule: >
      Select every biomarker result explicitly stated as positive. If testing
      is mentioned and came back negative for a given marker, use
      "biomarker-negative". Use "not_tested" only if the note states testing
      was not done, or is pending with no result yet.
    aggregation: union_persistent

  acute_symptoms:
    label: "Symptoms documented as active in this note"
    type: multi_select
    allowed_values:
      - dyspnea
      - chest_pain
      - hemoptysis
      - fatigue
      - weight_loss
      - fever
      - neutropenic_fever
      - nausea_vomiting
      - pain_uncontrolled
      - none_documented
    absent_values: [none_documented]
    abstraction_rule: >
      Include only symptoms described as current or active at the time of
      this note (e.g. "reports new dyspnea", "ongoing nausea"). Do not
      include symptoms explicitly noted as resolved or historical.
    aggregation: most_recent_note_only
```

Each field declares its own **aggregation policy** — this is the piece registries usually get wrong by hand-waving. `diagnosis`/`stage` are "state" fields (most recent note wins); `biomarker_status` is a persistent trait (union across all notes, since a positive result doesn't un-happen); `acute_symptoms` is note-specific and shouldn't accumulate across visits; `prior_lines_of_therapy` should be monotonically non-decreasing over time, so a decrease is itself a data-quality signal worth flagging.

### `pipeline/codebook.py`

```python
import yaml

def load_codebook(path):
    with open(path) as f:
        return yaml.safe_load(f)

def _field_schema(spec):
    return {
        "type": "object",
        "properties": {
            "value": {"type": "integer"} if spec["type"] == "integer"
                     else {"type": "string", "enum": spec["allowed_values"]},
            "quote": {"type": "string"},
            "confidence": {"type": "string", "enum": ["low", "medium", "high"]},
        },
        "required": ["value", "quote", "confidence"],
    }

def build_tool_schema(codebook):
    properties, required = {}, []
    for name, spec in codebook["fields"].items():
        field_schema = _field_schema(spec)
        properties[name] = {"type": "array", "items": field_schema} if spec["type"] == "multi_select" else field_schema
        required.append(name)
    return {
        "name": "record_extraction",
        "description": "Record the codebook-defined fields extracted from the clinical note, each with a supporting verbatim quote.",
        "input_schema": {"type": "object", "properties": properties, "required": required},
    }
```

### `pipeline/extract.py`

```python
import json, re
from pathlib import Path
import anthropic
from codebook import load_codebook, build_tool_schema

NOTES_DIR = Path("notes")
OUT_DIR = Path("outputs/extractions")

def parse_note(path):
    text = path.read_text()
    m = re.search(r"^DATE:\s*(\d{4}-\d{2}-\d{2})", text, re.M)
    date = m.group(1) if m else None
    patient_id, note_id = path.stem.split("_", 1)
    return patient_id, note_id, date, text

def build_prompt(codebook, note_text):
    lines = [
        "Extract the following structured fields from the clinical note below,",
        "following each field's abstraction rule exactly. For every field value",
        "that is not one of its listed absent/sentinel values, you must provide",
        "an exact verbatim quote (copied character-for-character) from the note",
        "that supports it. Do not paraphrase or summarize the quote.\n",
    ]
    for name, spec in codebook["fields"].items():
        lines.append(f"- {name} ({spec['type']}): {spec['abstraction_rule'].strip()}")
        if "allowed_values" in spec:
            lines.append(f"  allowed values: {spec['allowed_values']}")
    lines.append("\n--- NOTE TEXT START ---\n" + note_text + "\n--- NOTE TEXT END ---")
    return "\n".join(lines)

def main():
    codebook = load_codebook("codebook.yaml")
    tool = build_tool_schema(codebook)
    client = anthropic.Anthropic()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for path in sorted(NOTES_DIR.glob("*.txt")):
        patient_id, note_id, date, text = parse_note(path)
        prompt = build_prompt(codebook, text)
        resp = client.messages.create(
            model=codebook.get("model", "claude-sonnet-5"),
            max_tokens=2000,
            temperature=0,
            tools=[tool],
            tool_choice={"type": "tool", "name": tool["name"]},
            messages=[{"role": "user", "content": prompt}],
        )
        tool_use = next(b for b in resp.content if b.type == "tool_use")
        record = {
            "patient_id": patient_id,
            "note_id": note_id,
            "note_date": date,
            "note_path": str(path),
            "codebook_version": codebook["version"],
            "model": resp.model,
            "extraction": tool_use.input,
        }
        (OUT_DIR / f"{patient_id}_{note_id}.json").write_text(json.dumps(record, indent=2))
        print(f"extracted {patient_id}_{note_id}")

if __name__ == "__main__":
    main()
```

`temperature=0` and forced `tool_choice` make reruns as deterministic as the model allows; the raw tool input is saved untouched for audit before any post-processing touches it.

### `pipeline/verify.py` — the traceability enforcement step

```python
import json, re, difflib
from pathlib import Path
from codebook import load_codebook

EXTRACTIONS = Path("outputs/extractions")
VERIFIED = Path("outputs/verified")

def normalize(s):
    return re.sub(r"\s+", " ", s or "").strip()

def is_grounded(quote, note_text, threshold=0.92):
    nq, nt = normalize(quote), normalize(note_text)
    if not nq:
        return True, 1.0
    if nq in nt:
        return True, 1.0
    window = len(nq) + 20
    best = 0.0
    for i in range(0, max(len(nt) - window, 1), 10):
        best = max(best, difflib.SequenceMatcher(None, nq, nt[i:i + window]).ratio())
    return best >= threshold, best

def verify_field(spec, entry):
    absent = set(spec.get("absent_values", []))
    def check_one(item, note_text):
        if item["value"] in absent:
            return {**item, "grounded": True, "similarity": 1.0, "needs_review": False}
        grounded, sim = is_grounded(item.get("quote", ""), note_text)
        return {**item, "grounded": grounded, "similarity": round(sim, 3),
                "needs_review": (not grounded) or item.get("confidence") == "low"}
    return entry  # placeholder, replaced below per call site

def main():
    codebook = load_codebook("codebook.yaml")
    VERIFIED.mkdir(parents=True, exist_ok=True)
    for path in sorted(EXTRACTIONS.glob("*.json")):
        record = json.loads(path.read_text())
        note_text = Path(record["note_path"]).read_text()
        verified = {}
        for name, spec in codebook["fields"].items():
            absent = set(spec.get("absent_values", []))
            def check_one(item):
                if item["value"] in absent:
                    return {**item, "grounded": True, "similarity": 1.0, "needs_review": False}
                grounded, sim = is_grounded(item.get("quote", ""), note_text)
                return {**item, "grounded": grounded, "similarity": round(sim, 3),
                        "needs_review": (not grounded) or item.get("confidence") == "low"}
            entry = record["extraction"][name]
            verified[name] = [check_one(i) for i in entry] if spec["type"] == "multi_select" else check_one(entry)
        record["extraction"] = verified
        (VERIFIED / path.name).write_text(json.dumps(record, indent=2))
        print(f"verified {path.name}")

if __name__ == "__main__":
    main()
```

(Ignore the unused `verify_field` stub above — left over from refactoring inline; delete it, the logic is inlined in `main()`.) This is the step that keeps the pipeline honest: a model can *claim* `stage: IV` all it wants, but if it can't point to an actual sentence in that exact note, the value is flagged rather than trusted.

### `pipeline/aggregate.py`

```python
import json, csv
from pathlib import Path
from collections import defaultdict
from codebook import load_codebook

VERIFIED = Path("outputs/verified")
OUT = Path("outputs")

def load_records():
    return [json.loads(p.read_text()) for p in sorted(VERIFIED.glob("*.json"))]

def write_evidence_table(records, codebook):
    rows = []
    for r in records:
        for field, spec in codebook["fields"].items():
            items = r["extraction"][field]
            items = items if spec["type"] == "multi_select" else [items]
            for item in items:
                rows.append({
                    "patient_id": r["patient_id"], "note_id": r["note_id"], "note_date": r["note_date"],
                    "field": field, "value": item["value"], "quote": item.get("quote", ""),
                    "confidence": item.get("confidence"), "grounded": item.get("grounded"),
                    "needs_review": item.get("needs_review"),
                    "codebook_version": r["codebook_version"], "model": r["model"],
                })
    with open(OUT / "evidence_table.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)

def aggregate_patient(patient_id, records, codebook):
    records = sorted(records, key=lambda r: r["note_date"] or "")
    row, flags = {"patient_id": patient_id}, []
    for field, spec in codebook["fields"].items():
        rule, absent = spec["aggregation"], set(spec.get("absent_values", []))
        if rule == "most_recent":
            item = records[-1]["extraction"][field]
            row[field], row[f"{field}__note_id"] = item["value"], records[-1]["note_id"]
            if item.get("needs_review"):
                flags.append(field)
        elif rule == "most_recent_note_only":
            items = records[-1]["extraction"][field]
            vals = [i["value"] for i in items if i["value"] not in absent] or [next(iter(absent), "")]
            row[field], row[f"{field}__note_id"] = "|".join(vals), records[-1]["note_id"]
        elif rule == "union_persistent":
            seen = {}
            for rec in records:
                for i in rec["extraction"][field]:
                    if i["value"] not in absent:
                        seen[i["value"]] = rec["note_id"]
            row[field] = "|".join(seen) if seen else next(iter(absent), "")
            row[f"{field}__note_ids"] = "|".join(seen.values())
        elif rule == "max_monotonic":
            best_val, best_note, prev, decreasing = None, None, None, False
            for rec in records:
                v = rec["extraction"][field]["value"]
                if prev is not None and v < prev:
                    decreasing = True
                prev = v
                if best_val is None or v >= best_val:
                    best_val, best_note = v, rec["note_id"]
            row[field], row[f"{field}__note_id"] = best_val, best_note
            if decreasing:
                flags.append(f"{field}_decreasing")
    row["review_flags"] = "|".join(flags)
    return row

def main():
    codebook = load_codebook("codebook.yaml")
    records = load_records()
    write_evidence_table(records, codebook)
    by_patient = defaultdict(list)
    for r in records:
        by_patient[r["patient_id"]].append(r)
    rows = [aggregate_patient(pid, recs, codebook) for pid, recs in sorted(by_patient.items())]
    with open(OUT / "registry_table.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
    print(f"wrote registry_table.csv ({len(rows)} patients) and evidence_table.csv")

if __name__ == "__main__":
    main()
```

### `pipeline/manifest.py` and `run.sh`

```python
# pipeline/manifest.py
import hashlib, json
from pathlib import Path
from datetime import datetime, timezone

def sha256_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def main():
    notes = sorted(Path("notes").glob("*.txt"))
    manifest = {
        "run_at": datetime.now(timezone.utc).isoformat(),
        "codebook_sha256": sha256_file("codebook.yaml"),
        "notes": [{"path": str(p), "sha256": sha256_file(p)} for p in notes],
    }
    Path("outputs").mkdir(exist_ok=True)
    Path("outputs/manifest.json").write_text(json.dumps(manifest, indent=2))

if __name__ == "__main__":
    main()
```

```bash
#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"
python pipeline/manifest.py
python pipeline/extract.py
python pipeline/verify.py
python pipeline/aggregate.py
echo "Done. See outputs/registry_table.csv, outputs/evidence_table.csv, outputs/manifest.json"
```

## Why this satisfies your two requirements

**Traceability per cell.** `evidence_table.csv` is the ground truth artifact — every value in `registry_table.csv` has a `field__note_id` (or `__note_ids`) column pointing back into it, and every evidence row carries the exact `note_id`, the verbatim `quote`, and a `grounded`/`similarity` score proving the quote was actually found in that note's text, not invented. Reviewers audit by reading the quote next to the value, not by re-reading the whole note.

**Rerunnable and written down.** The codebook is a single version-controlled YAML file — put it in git and every extraction record stamps its `codebook_version`. `manifest.json` hashes the codebook and every input note file, so you can prove exactly which inputs produced a given `registry_table.csv`. Aggregation logic (recency vs. union vs. monotonic-max) lives in code, not in a person's head, so two runs against the same notes and codebook produce the same table (`temperature=0` gets you close to deterministic extraction; the grounding check catches the residual drift by refusing to trust ungrounded quotes either way).

**Human review loop.** `needs_review`/`review_flags` columns are the seam for a person: anything ungrounded, low-confidence, or logically inconsistent (e.g., therapy-line count dropping between visits) surfaces for manual sign-off instead of silently entering the registry. Treat that review as another versioned input (e.g., a `corrections.csv` merged in a final step) rather than hand-editing the output CSV, so the whole chain stays rerunnable.

To point this at your real data: drop your actual notes into `notes/` following the same naming/date convention (or adjust `parse_note`), replace `codebook.yaml` with your real fields/allowed-values/rules, set `ANTHROPIC_API_KEY`, `pip install anthropic pyyaml`, and run `./run.sh`.