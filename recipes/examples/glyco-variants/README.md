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
It exists to demonstrate the principle the cookbook asks every recipe to follow:

> **The durable record of an AI-assisted analysis is committed code plus a
> pinned environment and a provenance record — not a chat transcript.**

An assistant (Claude) may author or edit `glyco_variants.py` for you. What you
keep, cite in a paper, and re-run six months later is this directory. See the
guide page
[Reproducible, provenance-tracked AI analysis](../../../guide/advanced/reproducibility.html)
for the general pattern.

## What's here

| File | Role |
|---|---|
| `glyco_variants.py` | The analysis. Standard-library offline replay + a live GlyGen-MCP / UniProt / BioMCP mode. |
| `variants.csv` | Example input — 7 real variants across `SERPINC1` and `IFNGR2`, with a ground-truth `expected_class` column. |
| `requirements.txt` | **Pinned** environment for the live run (`mcp`, `requests`); BioMCP is the `biomcp` CLI, installed out-of-band. |
| `fixtures/glygen/` | Recorded GlyGen MCP glycosite responses + the data release stamp (v2.11.1). |
| `fixtures/uniprot/` | Canonical UniProt FASTA sequences, for the sequon check. |
| `fixtures/biomcp/` | Recorded BioMCP variant annotations (ClinVar / CADD / PolyPhen / SIFT). |
| `results/` | *Emitted by a run* — `glyco_candidates.csv` (ranked) + `provenance.json`. |

## Run it

Deterministic replay (no network, standard library only):

```sh
python glyco_variants.py --variants variants.csv --outdir results
```

Live run against the real tools the recipe prescribes:

```sh
pip install -r requirements.txt          # mcp, requests
uv tool install biomcp-cli               # provides the `biomcp` CLI
python glyco_variants.py --variants variants.csv --outdir results --live
```

Both write `glyco_candidates.csv` (ranked, glycosylation-altering hits first) and
a `provenance.json`. The live and offline runs produce the **same
classifications** (verified); only the raw annotation values can drift as the
upstream databases update — which is exactly why the fixtures and `provenance.json`
carry the GlyGen release version and endpoint.

## The result

Ranked output for the 7-variant demo panel (`results/glyco_candidates.csv`):

| rank | variant | class | mechanism | ClinVar | CADD | PolyPhen | predictors miss it |
|---|---|---|---|---|---|---|---|
| 1 | IFNGR2 T168N | **GOG** | creates N-X-S/T sequon `NST` @168 | Pathogenic | 0.005 | Benign | **yes** |
| 2 | SERPINC1 S114N | **GOG** | creates sequon `NIS` @114 | Pathogenic | 28.0 | Prob. damaging | no |
| 3 | IFNGR2 T70N | **GOG** | creates sequon `NDS` @70 | not provided | 24.5 | Prob. damaging | no |
| 4 | SERPINC1 N167S | **LOG** | destroys sequon @167 (GlyGen-annotated site) | not provided | 13.89 | Benign | no |
| 5 | SERPINC1 R79C | none | no glycosite change | Pathogenic | 33.0 | Prob. damaging | — |
| 6 | SERPINC1 N219D | none | no glycosite change | Pathogenic | 27.3 | Prob. damaging | — |
| 7 | SERPINC1 R220C | *unmapped* | canonical residue 220 is Lys, not Arg — numbering could not be reconciled | Pathogenic | 35.0 | Tolerated | — |

**The headline finding (rank 1).** `IFNGR2` T168N is ClinVar **Pathogenic** and
causes Mendelian susceptibility to mycobacterial disease — yet CADD (0.005),
PolyPhen (benign), and SIFT (tolerated) all call it harmless. The
glycosylation-*gain* mechanism (a new N-X-S/T sequon that sterically disrupts
receptor assembly) is the signal the sequence-based predictors miss. That is the
entire reason this recipe exists, reproduced from live data.

**It also shows specificity, not just sensitivity.** The two `none` rows
(`R79C`, `N219D`) are *also* pathogenic with high CADD — but glycosylation is not
their mechanism, and the pipeline correctly does **not** flag them. And the
`unmapped` row is the recipe's central trap firing on a real record: the guard
refuses to classify a variant whose stated residue does not match the canonical
sequence, rather than silently comparing against the wrong position.

## How it embodies the doctrine

- **Code is the record.** The workflow is a version-controlled script, not an
  interactive session. Re-running it is one command.
- **Pin what you can.** `requirements.txt` pins the live-mode deps; the offline
  replay is standard-library only.
- **Record the rest.** `provenance.json` stamps the GlyGen data release
  (v2.11.1), the MCP endpoint, the BioMCP source, the input sha256, and a sha256
  of every output, so any divergence on re-run is visible rather than silent.
- **Grounding is mechanical.** Every classification is a deterministic sequon
  computation over the real GlyGen glycosites + UniProt sequence — the model
  cannot narrate a gain/loss that the sequence does not support. The
  `expected_class` column is checked in CI.
- **It's testable.** `tests/test_glyco_variants_example.py` runs the offline path
  twice for byte-identical output, verifies the provenance hash, and asserts the
  ground-truth classifications — including the T168N headline finding.

## Field notes (from building this against the live Beta server)

These are real observations worth feeding back to the recipe and the GlyGen MCP
catalog page:

- **Tool-surface drift.** The recipe/catalog name the GlyGen glycosite tool
  `get_site_summary`; the live server (data release 2.11.1) exposes
  `get_protein_glycosylation_sites` instead. The GlyGen MCP is Beta and its tool
  surface is moving — pin the release you queried, as this artifact does.
- **AlphaMissense.** BioMCP's default variant payload returns ClinVar / CADD /
  PolyPhen / SIFT but **not** AlphaMissense. The recipe's "join AlphaMissense"
  step is therefore best-effort via BioMCP today; this demo ranks on ClinVar +
  CADD + a predictor-discordance flag instead.
- **Numbering is the real work.** `SERPINC1` literature "N135" (mature) is
  canonical `N167`; and a real ClinVar record (`R220C`, rs121909554) uses a
  numbering under which canonical residue 220 is not Arg at all. Harmonization —
  and refusing to guess when it fails — is load-bearing, not decorative.
