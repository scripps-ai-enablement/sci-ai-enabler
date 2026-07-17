---
title: 'Reproducible example: glycosylation-altering variants'
parent: All recipes
grand_parent: Recipes
nav_exclude: true
permalink: /recipes/examples/glyco-variants/
---

# Reproducible example — interpreting glycosylation-altering variants

This is the reference *artifact* for the recipe
[Interpret variants that gain or lose glycosylation sites](../../items/interpret-glycosylation-altering-variants.html).
It demonstrates the principle the cookbook asks every recipe to follow:

> **The durable record of an AI-assisted analysis is committed code plus a
> pinned environment and a provenance record — not a chat transcript.**

An assistant (Claude) may author or edit `glyco_variants.py` for you. What you
keep, cite, and re-run six months later is this directory. See the guide page
[Reproducible, provenance-tracked AI analysis](../../../guide/advanced/reproducibility.html).

The recipe's BCO step is **required**, so every run emits an IEEE-2791
BioCompute Object (`glyco_run.bco.json`) alongside the results, validated against
the bundled 2791 JSON schema.

## What's here

| File | Role |
|---|---|
| `glyco_variants.py` | The analysis. Standard-library offline replay + a live GlyGen-MCP / UniProt / BioMCP mode. Emits and validates the BCO. |
| `variants.csv` | Example input — 7 real variants across `SERPINC1` and `IFNGR2`, with a ground-truth `expected_class` column. |
| `requirements.txt` | **Pinned** environment for the live run + BCO validation (`mcp`, `requests`, `jsonschema`, `referencing`); BioMCP is the `biomcp` CLI, installed out-of-band. |
| `fixtures/glygen/`, `fixtures/uniprot/`, `fixtures/biomcp/` | Recorded tool responses so the offline replay needs no network. |
| `fixtures/ieee2791/` | The IEEE-2791 JSON schema (top-level + 7 domain schemas) for offline BCO validation. |
| `results/` | *Emitted by a run* — `glyco_candidates.csv`, `provenance.json`, and `glyco_run.bco.json`. |

## Run it

Deterministic replay (no network; standard library only — still emits the BCO,
skips validation unless the deps below are present):

```sh
python glyco_variants.py --variants variants.csv --outdir results
```

Full run with BCO validation (and/or `--live` against the real tools):

```sh
pip install -r requirements.txt          # mcp, requests, jsonschema, referencing
uv tool install biomcp-cli               # provides the `biomcp` CLI
python glyco_variants.py --variants variants.csv --outdir results            # validates the BCO
python glyco_variants.py --variants variants.csv --outdir results --live     # live + validates
```

All three outputs are deterministic in offline mode. Live and offline runs
produce the same classifications and a schema-valid BCO (verified); only the raw
annotation values can drift as the upstream databases update — which is why the
provenance and the BCO carry the GlyGen release version and endpoint.

## The result

Ranked output for the 7-variant demo panel (`results/glyco_candidates.csv`):

| rank | variant | class | mechanism | ClinVar | CADD | PolyPhen | AlphaMissense | predictors miss it |
|---|---|---|---|---|---|---|---|---|
| 1 | IFNGR2 T168N | **GOG** | creates N-X-S/T sequon `NST` @168 | Pathogenic | 0.005 | Benign | Benign (0.09) | **yes** |
| 2 | SERPINC1 S114N | **GOG** | creates sequon `NIS` @114 | Pathogenic | 28.0 | Prob. damaging | Pathogenic (0.92) | no |
| 3 | IFNGR2 T70N | **GOG** | creates sequon `NDS` @70 | not provided | 24.5 | Prob. damaging | Benign (0.12) | no |
| 4 | SERPINC1 N167S | **LOG** | destroys sequon @167 (GlyGen-annotated site) | not provided | 13.89 | Benign | Benign (0.12) | no |
| 5 | SERPINC1 R79C | none | no glycosite change | Pathogenic | 33.0 | Prob. damaging | Pathogenic (0.91) | — |
| 6 | SERPINC1 N219D | none | no glycosite change | Pathogenic | 27.3 | Prob. damaging | Pathogenic (0.66) | — |
| 7 | SERPINC1 R220C | *unmapped* | canonical residue 220 is Lys, not Arg | Pathogenic | 35.0 | Tolerated | Ambiguous (0.47) | — |

**The headline finding (rank 1).** `IFNGR2` T168N is ClinVar **Pathogenic** and
causes Mendelian susceptibility to mycobacterial disease — yet CADD, PolyPhen,
SIFT, **and AlphaMissense** all call it harmless. The glycosylation-*gain*
mechanism is the signal the sequence-based predictors miss. The two `none` rows
are *also* pathogenic but
not glycosylation-driven, and the pipeline correctly does not flag them; the
`unmapped` row is the numbering-harmonization guard firing on a real record.

## The BioCompute Object

`results/glyco_run.bco.json` is a full IEEE-2791 object with all eight required
domains, populated from this run:

- `description_domain.pipeline_steps` — GlyGen lookup → sequence fetch →
  harmonize + classify → BioMCP join → rank.
- `execution_domain` — the script, pinned software, and the GlyGen MCP / UniProt
  / MyVariant.info endpoints.
- `parametric_domain` — the sequon rule (`N-X-[S/T]`, X≠Pro), the ±2 window, and
  the ranking.
- `io_domain` — `variants.csv` in, `glyco_candidates.csv` out, and **GlyGen's own
  dataset BCOs (`GLY_001534`, `GLY_001537`) cited as input provenance**.
- `error_domain` — the missense-only scope, the AlphaMissense gap, and the
  `unmapped` guard, recorded as `algorithmic_error`.

The `etag` is a sha256 over the object (deterministic), and the object validates
against the bundled schema (`fixtures/ieee2791/`). This is what makes the run
interoperable with GlyGen's own BCO-based provenance — the reason the recipe
promotes the BCO step to required.

## How it embodies the doctrine

- **Code is the record**, and re-running is one command.
- **Pin what you can** (`requirements.txt`); **record the rest** — `provenance.json`
  and the BCO stamp the GlyGen release (v2.11.1), the endpoints, and sha256s of
  every output, so drift on re-run is visible, not silent.
- **Grounding is mechanical.** Every class is a deterministic sequon computation
  over the real GlyGen glycosites + UniProt sequence; `expected_class` is checked
  in CI.
- **It's testable.** `tests/test_glyco_variants_example.py` runs the offline path
  twice for byte-identical output, checks the provenance hashes and BCO structure
  (all eight domains, etag recomputation), asserts the ground-truth
  classifications, and — when `jsonschema`/`referencing` are installed —
  validates the BCO against the bundled IEEE-2791 schema.

## Field notes (from building this against the live Beta server)

- **Tool-surface drift.** The catalog names the GlyGen glycosite tool
  `get_site_summary`; the live server (release 2.11.1) exposes
  `get_protein_glycosylation_sites`. GlyGen MCP is Beta — pin the release.
- **AlphaMissense needs the `predictions` section.** BioMCP's *default* variant
  view omits AlphaMissense, but it is available via `biomcp get variant <id>
  predictions` (dbNSFP through MyVariant.info) — which is a superset of the
  default view. This example joins it from there. Notably, AlphaMissense *also*
  calls the T168N gain variant benign, so it too misses the mechanism.
- **BioMCP stdio command.** Registering BioMCP as an MCP server is `biomcp mcp`,
  not `biomcp run` (which is not a subcommand). The recipe's install step was
  corrected accordingly.
- **Numbering is the real work.** `SERPINC1` literature "N135" (mature) is
  canonical `N167`; a real ClinVar record (`R220C`) uses a numbering under which
  canonical residue 220 is not Arg. Harmonizing — and refusing to guess when it
  fails — is load-bearing.
