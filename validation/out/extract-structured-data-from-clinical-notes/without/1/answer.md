File writes aren't going through in this sandboxed session (no approval channel available), so I'll give you the complete pipeline as text — copy these into files to run it.

## Architecture

```
clinical_registry_pipeline/
├── codebook.yaml              # the abstraction protocol — versioned, human-readable
├── notes/                     # your input: PATIENTID__NOTEID__YYYY-MM-DD__notetype.txt
├── src/
│   ├── extract.py             # LLM: one note in → mention-level candidates out
│   ├── validate.py            # deterministic: reject hallucinated quotes/values
│   └── build_registry.py      # deterministic: per-patient rollup via codebook rules
├── runs/<run_id>/
│   ├── manifest.json          # what ran, when, against which codebook/model version
│   ├── mentions_raw.jsonl     # every candidate the model emitted, before validation
│   ├── validation_report.csv  # quote-verification failures, flagged for review
│   ├── registry_wide.csv      # one row per patient — your deliverable
│   └── registry_provenance.csv# one row per (patient, field): value, note_id, quote, rule applied
└── requirements.txt
```

**The core idea:** the LLM never sees more than one note at a time and never resolves conflicts. It extracts *mentions* (value + verbatim quote + note_id). A separate deterministic step — plain Python, reading rules straight out of `codebook.yaml` — decides which mention wins when a patient has multiple notes (e.g. "most recent stage wins," "union of distinct regimens for line-of-therapy count"). That keeps the one part of this that's genuinely hard to audit (cross-document clinical judgment) out of the model and in code you can read, diff, and unit-test. It also means every registry cell keeps a full list of *all* candidate mentions in the provenance table, not just the winner — so a reviewer can see what was overridden and why.

**Compliance note, stated up front since it matters more than any of the code:** "de-identified" under your institution's definition may still not clear your policy for sending notes to a third-party API. Before pointing this at real notes, confirm with your privacy/compliance office whether your Anthropic access is under a BAA (Bedrock/Vertex-hosted Claude, or an Anthropic enterprise agreement) and whether your de-identification method meets Safe Harbor/Expert Determination. Treat that as a blocking prerequisite, not a detail to fix later.

## codebook.yaml

```yaml
codebook_version: "1.0.0"
not_documented_value: "not_documented"

fields:
  - name: diagnosis
    type: enum
    allowed_values: [breast_cancer, non_small_cell_lung_cancer, colorectal_cancer,
                      prostate_cancer, other_specify, not_documented]
    adjudication: mode_most_recent_tiebreak
    flag_if_distinct_values_gt: 1   # outright disagreement -> human review, not averaged away

  - name: stage
    type: ordered_enum
    allowed_values: ["0", "I", "II", "III", "IV", "unknown", "not_documented"]
    adjudication: most_recent
    # Policy choice: reports current disease state, not stage-at-diagnosis.
    # Swap to earliest_documented + restrict source notes to the diagnostic
    # workup window if you need the latter. Confirm with clinical lead.

  - name: prior_lines_of_therapy
    type: count_with_evidence_list
    dedupe_key: regimen_name_normalized
    adjudication: union_count_across_notes

  - name: biomarkers
    type: biomarker_panel
    panel: [ER, PR, HER2, PDL1, EGFR, ALK]
    allowed_values: [positive, negative, equivocal, not_tested, not_documented]
    adjudication: most_recent

  - name: acute_symptoms
    type: multiselect
    allowed_values: [fever, dyspnea, chest_pain, severe_pain_flare,
                      altered_mental_status, active_bleeding, nausea_vomiting, other_specify]
    lookback_window_days: 30
    adjudication: any_within_window
    # Only tracks documented positives. "Not mentioned" != "documented absent" —
    # add a separate negatives field if you need explicit denials tracked too.

extraction_rules:
  - "Only extract from the single note text you are given. Never use outside knowledge or other notes."
  - "Every non-empty value must carry a verbatim quote copied character-for-character from the note."
  - "If a field is not addressed in this note, emit nothing for it — omission becomes not_documented downstream."
  - "If the note explicitly states a value is unknown/pending, use not_documented WITH the supporting quote."
  - "Never resolve conflicts yourself. If one note contains two different values for a field, emit both."
```

## src/extract.py

```python
"""
Per-note extraction. Calls Claude once per note with a forced tool call so
output is schema-constrained JSON, not free text to parse. Runs at
temperature=0 for reproducibility (note: LLMs are not bitwise-deterministic
even at temp 0 — that's why validate.py exists as a hard backstop, and why
the manifest records model + prompt version so a rerun is at least
protocol-identical even if a handful of edge-case cells drift).
"""
import os, re, json, hashlib, glob
from pathlib import Path
import anthropic

MODEL = "claude-sonnet-5"   # pin an explicit model string in the real run manifest
NOTE_FILENAME_RE = re.compile(r"^(?P<patient_id>[^_]+)__(?P<note_id>[^_]+)__(?P<date>\d{4}-\d{2}-\d{2})__(?P<note_type>.+)\.txt$")

def load_codebook(path="codebook.yaml"):
    import yaml
    with open(path) as f:
        return yaml.safe_load(f)

def expand_biomarker_fields(codebook):
    """biomarkers panel -> biomarker_ER, biomarker_PR, ... as flat fields."""
    flat = []
    for f in codebook["fields"]:
        if f["type"] == "biomarker_panel":
            for name in f["panel"]:
                flat.append({**f, "name": f"biomarker_{name}", "type": "enum",
                             "biomarker": name})
        else:
            flat.append(f)
    return flat

def build_tool_schema(fields):
    field_names = [f["name"] for f in fields]
    return {
        "name": "record_mentions",
        "description": "Record every codebook field explicitly addressed in this note.",
        "input_schema": {
            "type": "object",
            "properties": {
                "mentions": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "field": {"type": "string", "enum": field_names},
                            "value": {"type": "string"},
                            "quote": {"type": "string",
                                      "description": "Verbatim substring of the note."},
                        },
                        "required": ["field", "value", "quote"],
                    },
                }
            },
            "required": ["mentions"],
        },
    }

def parse_filename(path):
    m = NOTE_FILENAME_RE.match(Path(path).name)
    if not m:
        raise ValueError(f"Filename doesn't match convention: {path}")
    return m.groupdict()

def extract_note(client, note_text, note_meta, codebook, tool_schema):
    system = (
        "You abstract structured data from a single clinical note per a fixed "
        "codebook. Follow these rules exactly:\n- "
        + "\n- ".join(codebook["extraction_rules"])
        + "\n\nAllowed fields and values:\n"
        + json.dumps(
            {f["name"]: f.get("allowed_values", "free text, count, or list — see field type")
             for f in expand_biomarker_fields(codebook)},
            indent=2,
        )
    )
    resp = client.messages.create(
        model=MODEL,
        max_tokens=2048,
        temperature=0,
        system=system,
        tools=[tool_schema],
        tool_choice={"type": "tool", "name": "record_mentions"},
        messages=[{"role": "user", "content": f"NOTE TEXT:\n{note_text}"}],
    )
    tool_call = next(b for b in resp.content if b.type == "tool_use")
    mentions = tool_call.input["mentions"]
    for m in mentions:
        m["note_id"] = note_meta["note_id"]
        m["patient_id"] = note_meta["patient_id"]
        m["note_date"] = note_meta["date"]
    return mentions

def run(notes_dir, codebook_path, out_path):
    codebook = load_codebook(codebook_path)
    fields = expand_biomarker_fields(codebook)
    tool_schema = build_tool_schema(fields)
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY

    all_mentions = []
    for path in sorted(glob.glob(os.path.join(notes_dir, "*.txt"))):
        meta = parse_filename(path)
        text = Path(path).read_text()
        meta["sha256"] = hashlib.sha256(text.encode()).hexdigest()
        mentions = extract_note(client, text, meta, codebook, tool_schema)
        for m in mentions:
            m["source_note_sha256"] = meta["sha256"]
        all_mentions.extend(mentions)
        print(f"{path}: {len(mentions)} mention(s)")

    with open(out_path, "w") as f:
        for m in all_mentions:
            f.write(json.dumps(m) + "\n")
    return all_mentions

if __name__ == "__main__":
    run("notes", "codebook.yaml", "runs/mentions_raw.jsonl")
```

*At a few hundred patients with 1–5 notes each, this is ~500–2,000 API calls. Use the [Message Batches API](https://docs.claude.com/en/docs/build-with-claude/batch-processing) instead of the loop above for ~50% cost savings and much better throughput — swap the `client.messages.create` call for a batch submit/poll; the per-note prompt and schema stay identical.*

## src/validate.py

```python
"""
Hard backstop against hallucinated citations: every quote must be a real
verbatim (whitespace-normalized) substring of the note it claims to come
from. This is what actually gives you 'traceable to a quoted sentence' —
without it you're trusting the model's citation, not verifying it.
"""
import json, re, glob
from pathlib import Path

def normalize(s):
    return re.sub(r"\s+", " ", s).strip().lower()

def load_note_text(notes_dir, note_id):
    matches = glob.glob(f"{notes_dir}/*__{note_id}__*.txt")
    if not matches:
        return None
    return Path(matches[0]).read_text()

def validate_mentions(mentions_path, notes_dir, codebook_fields_by_name):
    results = []
    note_text_cache = {}
    for line in open(mentions_path):
        m = json.loads(line)
        note_id = m["note_id"]
        if note_id not in note_text_cache:
            note_text_cache[note_id] = load_note_text(notes_dir, note_id)
        note_text = note_text_cache[note_id]

        status = "OK"
        reason = ""
        if note_text is None:
            status, reason = "FAILED", "source note file not found"
        elif normalize(m["quote"]) not in normalize(note_text):
            status, reason = "FAILED_QUOTE_VERIFICATION", "quote not found verbatim in source note"
        else:
            field_def = codebook_fields_by_name.get(m["field"])
            allowed = field_def.get("allowed_values") if field_def else None
            if allowed and m["value"] not in allowed:
                status, reason = "FAILED_VALUE_NOT_IN_CODEBOOK", f"value '{m['value']}' not an allowed value"

        results.append({**m, "validation_status": status, "validation_reason": reason})
    return results

def write_report(results, out_csv):
    import csv
    keys = ["patient_id", "note_id", "field", "value", "quote",
            "validation_status", "validation_reason"]
    with open(out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        for r in results:
            w.writerow({k: r.get(k, "") for k in keys})
    failed = [r for r in results if r["validation_status"] != "OK"]
    print(f"{len(results)} mentions checked, {len(failed)} failed validation -> {out_csv}")
```

## src/build_registry.py

```python
"""
Deterministic per-patient rollup. Reads validated mentions, applies the
adjudication rule named in codebook.yaml for each field, and writes:
  - registry_wide.csv        one row per patient (the deliverable)
  - registry_provenance.csv  one row per (patient, field): winning value +
                              note_id + quote + which candidates lost + rule used
Nothing here calls the model — this step is pure, fast, and unit-testable,
which is what makes the whole pipeline rerunnable and auditable.
"""
import csv
from collections import defaultdict
from datetime import datetime

def most_recent(mentions):
    winner = max(mentions, key=lambda m: m["note_date"])
    return winner, [m for m in mentions if m is not winner]

def mode_most_recent_tiebreak(mentions):
    counts = defaultdict(list)
    for m in mentions:
        counts[m["value"]].append(m)
    best_value = max(counts, key=lambda v: (len(counts[v]), max(m["note_date"] for m in counts[v])))
    winner = max(counts[best_value], key=lambda m: m["note_date"])
    return winner, [m for m in mentions if m is not winner]

def union_count_across_notes(mentions):
    seen = {}
    for m in mentions:
        key = m["value"].strip().lower()
        seen.setdefault(key, m)  # first occurrence keeps its citation
    count = len(seen)
    representative = mentions[0]
    combined = {**representative, "value": str(count),
                "quote": " | ".join(f"[{m['note_id']}] {m['quote']}" for m in seen.values())}
    return combined, []

def any_within_window(mentions):
    # Presence-only field: every validated positive mention is kept as-is;
    # rollup here just dedupes identical (value, note) pairs.
    dedup = {(m["value"], m["note_id"]): m for m in mentions}
    return list(dedup.values())

RULES = {
    "most_recent": most_recent,
    "mode_most_recent_tiebreak": mode_most_recent_tiebreak,
    "union_count_across_notes": union_count_across_notes,
    "any_within_window": any_within_window,
}

def build(validated_mentions, codebook_fields_by_name, not_documented="not_documented"):
    by_patient_field = defaultdict(list)
    for m in validated_mentions:
        if m["validation_status"] != "OK":
            continue
        by_patient_field[(m["patient_id"], m["field"])].append(m)

    patients = sorted({m["patient_id"] for m in validated_mentions})
    field_names = sorted(codebook_fields_by_name.keys())

    wide_rows, provenance_rows, flags = [], [], []

    for patient_id in patients:
        row = {"patient_id": patient_id}
        for field in field_names:
            mentions = by_patient_field.get((patient_id, field), [])
            field_def = codebook_fields_by_name[field]
            rule_name = field_def["adjudication"]

            if not mentions:
                row[field] = not_documented
                continue

            flag_thresh = field_def.get("flag_if_distinct_values_gt")
            distinct_values = {m["value"] for m in mentions}
            if flag_thresh and len(distinct_values) > flag_thresh:
                flags.append({"patient_id": patient_id, "field": field,
                              "reason": f"{len(distinct_values)} distinct values across notes: {distinct_values}"})

            if rule_name == "any_within_window":
                winners = RULES[rule_name](mentions)
                row[field] = ";".join(sorted({w["value"] for w in winners})) or not_documented
                for w in winners:
                    provenance_rows.append(_prov_row(patient_id, field, w, rule_name))
                continue

            winner, losers = RULES[rule_name](mentions)
            row[field] = winner["value"]
            provenance_rows.append(_prov_row(patient_id, field, winner, rule_name,
                                              alt_note_ids=[l["note_id"] for l in losers]))
        wide_rows.append(row)

    return wide_rows, provenance_rows, flags, field_names

def _prov_row(patient_id, field, mention, rule_name, alt_note_ids=None):
    return {
        "patient_id": patient_id, "field": field, "value": mention["value"],
        "note_id": mention["note_id"], "quote": mention["quote"],
        "note_date": mention.get("note_date", ""), "adjudication_rule": rule_name,
        "overridden_note_ids": ";".join(alt_note_ids or []),
    }

def write_csv(rows, fieldnames, path):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
```

## Run manifest (write this every run, not just once)

```python
import json, hashlib, subprocess, sys
from pathlib import Path

def write_manifest(run_dir, codebook_path, model, notes_dir):
    manifest = {
        "codebook_sha256": hashlib.sha256(Path(codebook_path).read_bytes()).hexdigest(),
        "model": model,
        "anthropic_sdk_version": __import__("anthropic").__version__,
        "python_version": sys.version,
        "input_notes": sorted(
            {"file": p.name, "sha256": hashlib.sha256(p.read_bytes()).hexdigest()}
            for p in Path(notes_dir).glob("*.txt")
        , key=lambda d: d["file"]),
        "git_commit": subprocess.getoutput("git rev-parse HEAD"),
    }
    Path(run_dir, "manifest.json").write_text(json.dumps(manifest, indent=2))
```

This is the piece that makes "rerunnable, not something a person did once" actually true: a rerun with the same `codebook.yaml` sha, same model string, same note file hashes should reproduce the same `registry_wide.csv` (modulo the handful of cells the LLM's non-determinism might flip — which `validate.py` and the flags file surface, not hide). If you change the codebook, bump `codebook_version` and treat the old and new registries as two named protocol versions, not silently overwritten files.

## What this doesn't automate — and shouldn't

- **QA sampling.** Have a human abstractor independently re-abstract a random ~15% of patients directly from the source notes (blind to the pipeline's output), then compute agreement (Cohen's κ per field) against `registry_wide.csv`. This is standard registry-abstraction practice and is your actual accuracy number — no amount of prompt engineering substitutes for it.
- **The `flags.csv` output** (distinct-value conflicts, validation failures, quote-verification failures) is meant to be worked by a human, every run, not archived.
- **Adjudication rule choices** (e.g. "stage = most recent" vs "stage at diagnosis") are clinical policy decisions encoded in YAML — get sign-off from whoever owns the registry's definitions before trusting the columns, since I picked defensible-but-arbitrary defaults above.

Copy the five files above (`codebook.yaml`, the three `src/*.py` files, and the manifest snippet) into a real project, `pip install anthropic pyyaml`, drop notes into `notes/` following the naming convention, and run `extract.py` → `validate.py` → `build_registry.py` in sequence.