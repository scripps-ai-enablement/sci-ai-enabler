---
title: 'Reproducible example: functional enrichment'
parent: All recipes
grand_parent: Recipes
nav_exclude: true
permalink: /recipes/examples/functional-enrichment/
---

# Reproducible example — functional enrichment on a gene list

This is the reference *artifact* for the recipe
[Run functional enrichment on a gene list](../../items/run-functional-enrichment-on-a-gene-list.html).
It exists to demonstrate the principle the cookbook asks every recipe to follow:

> **The durable record of an AI-assisted analysis is committed code plus a
> pinned environment and a provenance record — not a chat transcript.**

An assistant (Claude) may author or edit `enrichment.py` for you. What you keep,
cite in a paper, and re-run six months later is this directory — not the
conversation that produced it. See the guide page
[Reproducible, provenance-tracked AI analysis](../../../guide/advanced/reproducibility.html)
for the general pattern.

## What's here

| File | Role |
|---|---|
| `enrichment.py` | The analysis. Standard-library offline replay + a live `gget`/Enrichr mode. |
| `genes.txt` | Example input — one gene symbol per line. |
| `requirements.txt` | **Pinned** environment for the live run. |
| `fixtures/enrichr_response.json` | A recorded Enrichr response (with its snapshot date) for the deterministic replay. |
| `provenance.json` | *Emitted by a run* — records code version, source + snapshot date, input hash, and a sha256 of every output. |

## Run it

Deterministic replay (no network, standard library only):

```sh
python enrichment.py --offline fixtures/enrichr_response.json \
    --genes genes.txt --outdir results/enrichment
```

Live run against the real Enrichr API, as the recipe describes:

```sh
pip install -r requirements.txt
python enrichment.py --genes genes.txt --outdir results/enrichment \
    --run-date 2026-06-22
```

Both write per-library CSVs, a `SUMMARY.md` that cites only terms present in the
saved tables, and a `provenance.json`.

## How it embodies the doctrine

- **Code is the record.** The workflow is a script under version control, not an
  interactive session. Re-running it is one command.
- **Pin what you can.** `requirements.txt` pins `gget`/`pandas`; `provenance.json`
  stamps the code version and parameters.
- **Record the rest.** The Enrichr libraries evolve, so a live run can differ
  from the snapshot — that is expected. The fixture and `provenance.json` carry
  the **snapshot date** and a content hash so any divergence is visible rather
  than silent.
- **Grounding is mechanical.** `SUMMARY.md` only names terms that appear in the
  CSVs above the significance threshold — the model cannot narrate a pathway
  that isn't in the data.
- **It's testable.** `tests/test_reproducible_example.py` runs the offline path
  twice and asserts byte-identical, provenance-stamped output. Reproducibility
  is a CI check, not a promise.
