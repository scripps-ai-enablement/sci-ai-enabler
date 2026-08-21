## Architecture

The core idea: don't let a model "fill in a spreadsheet." Make it emit **evidence-linked assertions** (note_id + verbatim quote + value), verify each quote actually exists in the source text, and only then materialize the wide registry table as a *derived, regenerable view* of that evidence. The pipeline itself — codebook, prompts, model version, code — is versioned, so re-running it on the same notes reproduces the same table byte-for-byte.

Concretely, five artifacts, each a first-class file, not a one-off:

```
notes_manifest.csv      # note_id, patient_id, note_date, note_type, filepath
codebook.yaml           # fields, allowed values, abstraction rules, multiplicity, conflict-resolution
extraction_schema.json  # the JSON Schema the model is forced to fill (generated from codebook.yaml)
evidence.parquet        # long table: one row per (patient, field, value, note_id, quote) — the source of truth
registry.csv            # wide table: one row per patient — a *pivot* of evidence.parquet, never hand-edited
run_manifest.jsonl      # one line per run: codebook hash, prompt hash, model id, timestamp, notes hash
```

**Assumption** (since I don't have your actual folder): notes are plain-text files, one or more per patient, and you have or can build a manifest CSV mapping `note_id → patient_id, note_date, note_type, filepath`. If your notes are PDFs, add an OCR/text-extraction step before this pipeline and keep the extracted plain text as the thing offsets/quotes are checked against — never the PDF.

---

## 1. Codebook as data, not tribal knowledge

```yaml
# codebook.yaml
version: "2026-07-30.1"
fields:
  diagnosis:
    multiplicity: single
    allowed_values: [NSCLC, SCLC, "Breast cancer - HR+/HER2-", "Breast cancer - HER2+", "Not documented"]
    rule: >
      Use the most specific histology/subtype documented in any note for this patient.
      If notes conflict, prefer the most recent pathology-confirmed diagnosis over a
      clinical impression.

  stage:
    multiplicity: single
    allowed_values: ["I", "II", "III", "IV", "Not documented"]
    rule: "Use AJCC 8th edition staging as stated in the note. Do not infer stage from metastasis language alone."

  prior_lines_of_therapy:
    multiplicity: list
    rule: >
      Each entry is a distinct systemic regimen with a start (and stop, if stated) date.
      Radiation/surgery alone do not count as a systemic line.

  biomarker_status:
    multiplicity: list
    allowed_values: ["EGFR+", "EGFR-", "ALK+", "ALK-", "PD-L1 TPS>=50%", "PD-L1 TPS<1%", "Not tested"]

  acute_symptoms:
    multiplicity: list
    rule: "Only symptoms documented as present at the time of the note (not 'denies', not historical)."
```

Every field also implicitly requires, from the pipeline (not from the analyst re-typing it every time): a value, the `note_id` it came from, and a verbatim quoted span. This is enforced structurally in step 2, not left to prompt discipline.

---

## 2. Force evidence at the schema level

Use tool-use / forced structured output so the model *cannot* return a bare value — it can only call a tool whose schema requires citation:

```python
EXTRACTION_TOOL = {
    "name": "record_field",
    "input_schema": {
        "type": "object",
        "required": ["field", "value", "note_id", "quote", "confidence"],
        "properties": {
            "field": {"type": "string"},
            "value": {"type": "string"},
            "note_id": {"type": "string"},
            "quote": {"type": "string", "description": "Verbatim sentence(s) copied exactly from the note, no paraphrase"},
            "confidence": {"enum": ["high", "medium", "low"]},
        },
    },
}
```

For each patient, concatenate their notes with visible `[[NOTE_ID: n017]]` markers, send the codebook rule for one field (or a small related group of fields) at a time, and require one `record_field` tool call per asserted value — including an explicit "Not documented" value with no quote required when nothing supports the field. Splitting by field (rather than asking for all six fields in one giant call) reduces cross-field contamination and makes retries cheap. Use `temperature=0` for reproducibility. Model choice: Claude Sonnet 5 is the right default for this — good instruction-following on constrained vocab tasks at a fraction of Opus cost; escalate only ambiguous/low-confidence cases to Opus 5 as a second pass rather than running everything on the expensive model.

---

## 3. Verify every quote against the source — this is the traceability guarantee

A citation is worthless if it's fabricated. After extraction, mechanically check each quote is an actual substring of that `note_id`'s text (normalize whitespace/case, allow minor punctuation drift, but reject anything that isn't a real match):

```python
import re

def verify_quote(note_text: str, quote: str, fuzz: bool = True) -> tuple[bool, tuple[int,int] | None]:
    norm = lambda s: re.sub(r"\s+", " ", s).strip()
    hay, needle = norm(note_text), norm(quote)
    idx = hay.find(needle)
    if idx == -1 and fuzz:
        # allow a small edit-distance fallback for OCR/whitespace noise, still require high similarity
        from difflib import SequenceMatcher
        best = max(
            ((m.start(), SequenceMatcher(None, needle, hay[m.start():m.start()+len(needle)]).ratio())
             for m in re.finditer(re.escape(needle[:20]), hay)),
            default=(None, 0), key=lambda x: x[1],
        )
        if best[1] > 0.9:
            idx = best[0]
    return (idx != -1), ((idx, idx + len(needle)) if idx != -1 else None)
```

Any extraction whose quote fails verification is **never silently dropped or silently trusted** — it's flagged `ungrounded` and routed to a human review queue instead of entering the registry. This one check is what turns "an LLM read some notes" into an auditable process: you can report, for any given run, exactly what fraction of cells are grounded-verbatim vs. needing review.

---

## 4. Evidence table, then a derived registry — never edit the registry by hand

```
evidence.parquet columns:
  patient_id, field, value, note_id, note_date, quote, char_start, char_end,
  confidence, grounded (bool), run_id, model, prompt_version
```

The wide registry is a pure function of this table plus the codebook's conflict-resolution rule (e.g., "most recent note wins" for `stage`, "union across notes" for `prior_lines_of_therapy` and `acute_symptoms`). Because it's a deterministic pivot, you can regenerate `registry.csv` any time without re-running the LLM, and every cell can carry a footnote reference back to its evidence row(s) — e.g. export as CSV-with-sidecar or an HTML table where each cell is a tooltip/link to `(note_id, quote)`.

```python
def build_registry(evidence_df, codebook):
    rows = {}
    for patient_id, grp in evidence_df.groupby("patient_id"):
        row = {"patient_id": patient_id}
        for field, rule in codebook["fields"].items():
            fgrp = grp[(grp.field == field) & (grp.grounded)]
            if rule["multiplicity"] == "list":
                row[field] = sorted(set(fgrp.value))
                row[f"{field}__evidence"] = list(zip(fgrp.note_id, fgrp.quote))
            else:
                latest = fgrp.sort_values("note_date").tail(1)
                row[field] = latest.value.iloc[0] if len(latest) else "Not documented"
                row[f"{field}__evidence"] = (latest.note_id.iloc[0], latest.quote.iloc[0]) if len(latest) else None
        rows[patient_id] = row
    return rows
```

---

## 5. Make the whole thing rerunnable, not "something a person did once"

- **Version everything that affects output**: `codebook.yaml` hash, extraction prompt template hash, model id/version, and a hash of the notes manifest go into `run_manifest.jsonl` for every run. Same three inputs → byte-identical `evidence.parquet`.
- **Idempotent by note**: key extraction calls by `(note_id, field, codebook_version, model)` and cache results, so re-running after adding 20 new notes only calls the model on those 20, not the whole corpus.
- **Pipeline is a script, checked into version control** (a `Makefile` or a few Python scripts: `01_extract.py`, `02_verify.py`, `03_build_registry.py`), not a notebook someone ran interactively. Anyone can do `make registry` and get the current table from the current notes + current codebook.
- **Gold-standard check before trusting a run**: manually double-abstract ~20–30 notes yourself once, store as `gold.csv`, and run a small script that reports field-level agreement (exact match rate, and separately, quote-grounding rate) any time the codebook, prompt, or model changes. This is your regression test for the extraction pipeline itself.
- **Human review queue**: anything `ungrounded`, `confidence: low`, or with conflicting values across notes for a `single`-multiplicity field gets written to a `needs_review.csv` with the competing quotes side by side, instead of being resolved silently by a rule the analyst never sees.

---

## Practical notes

- Since notes are already de-identified, using the Anthropic API directly is reasonable, but confirm with whoever owns your data-use agreement/IRB protocol whether "de-identified" per your institution's standard is compatible with sending text to a third-party API at all — that's a policy question, not a technical one, and worth a five-minute check before you run this on real patient text at scale.
- Cost/scale: a few hundred patients × ~5 fields × a couple notes each is a small job (low thousands of API calls) — well within interactive budget on Sonnet 5; no need for batch processing unless the corpus is much larger, though the Message Batches API is a good fit if you want to run this unattended overnight for cost savings.
- Don't skip step 3. The single most common failure mode in "LLM extracts data from documents" projects is a plausible-sounding quote that isn't actually in the source — the verification step is what makes "traceable to the specific note ID and quoted sentence" true rather than aspirational.