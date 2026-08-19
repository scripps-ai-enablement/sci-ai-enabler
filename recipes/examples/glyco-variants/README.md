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

This artifact **follows the recipe faithfully**: it emits the recipe's exact
output columns and uses the recipe's ranking rule (see below). Every run also
emits an IEEE-2791 BioCompute Object (`glyco_run.bco.json`), validated against
the bundled 2791 schema. See the guide page
[Reproducible, provenance-tracked AI analysis](../../../guide/advanced/reproducibility.html).

## What's here

| File | Role |
|---|---|
| `glyco_variants.py` | The analysis. Standard-library offline replay + a live GlyGen-MCP / UniProt / ProtVar / BioMCP mode. Emits + validates the BCO. |
| `variants.csv` | Example input — 7 real variants across `SERPINC1` and `IFNGR2`, with a ground-truth `expected_class` column. |
| `requirements.txt` | **Pinned** environment for the live run + BCO validation. |
| `fixtures/{glygen,uniprot,protvar,biomcp}/` | Recorded tool responses so the offline replay needs no network. |
| `fixtures/ieee2791/` | The IEEE-2791 JSON schema (top-level + 7 domains) for offline BCO validation. |
| `results/` | *Emitted by a run* — `glyco_candidates.csv`, `provenance.json`, `glyco_run.bco.json`. |

## Run it

```sh
python glyco_variants.py --variants variants.csv --outdir results            # offline, deterministic
pip install -r requirements.txt && python glyco_variants.py ... --live       # live + BCO validation
```

## The result

Ranked per the recipe — GOG/LOG hits above `none` (unmapped last), then within
that group by **AlphaMissense pathogenicity, then ClinVar significance**
(`results/glyco_candidates.csv`, the recipe's 7 columns):

| rank | site | class | ClinVar | AlphaMissense |
|---|---|---|---|---|
| 1 | SERPINC1 S114N | **GOG** (new sequon N114-I115-S116) | Pathogenic | Pathogenic (0.873) |
| 2 | IFNGR2 T70N | **GOG** (new sequon N70-D71-S72) | not in ClinVar | Benign (0.184) |
| 3 | IFNGR2 T168N | **GOG** (new sequon N168-S169-T170) | Pathogenic | Benign (0.086) |
| 4 | SERPINC1 N167S | **LOG** (destroys GlyGen site Asn167) | not in ClinVar | Benign (0.084) |
| 5 | SERPINC1 R79C | none | Pathogenic | Pathogenic (0.809) |
| 6 | SERPINC1 N219D | none | Pathogenic | Pathogenic (0.656) |
| 7 | SERPINC1 R220C | *unmapped* (ProtVar: reference Arg ≠ UniProt Lys at 220) | not evaluated | — |

Every AlphaMissense value here was checked against an independent hand review by
GlyGen's glycan data manager and agrees to the digit; so does this ordering.

**What the ranking surfaces.** The four glycosylation-altering variants sort
above the two `none` controls, and the unmapped variant is held out at the
bottom — so the report leads with the mechanistically plausible candidates. Note
`IFNGR2` T168N (rank 4): it is ClinVar **Pathogenic** yet AlphaMissense (like
CADD/PolyPhen/SIFT) calls it **Benign** — a case where the glycosylation-gain
mechanism, not the sequence-based pathogenicity score, is the signal. The
recipe's ranking key is AlphaMissense pathogenicity, so this predictor-benign
variant sits mid-pack rather than at the top; a triage that specifically wanted
"variants predictors miss" would re-sort on that discordance.

## The BioCompute Object

`results/glyco_run.bco.json` is a full IEEE-2791 object (eight required domains):
`description_domain.pipeline_steps` (GlyGen lookup → sequence → harmonize +
classify → ProtVar/BioMCP join → rank); `execution_domain` (script, pinned software,
endpoints); `parametric_domain` (sequon rule, the ranking, and that the
expression check was not applied — no tissue context); `io_domain` citing
**GlyGen's own dataset BCOs (`GLY_001534`, `GLY_001537`) as input provenance**, each
naming the dataset file it distributes (`human_protein_mutation_germline_all.csv`,
`human_protein_mutation_cancer_all.csv`);
and `error_domain` (missense-only scope, ranking heuristic, unmapped guard). The
`etag` is a deterministic sha256, and the object validates against the bundled
schema.

## How it embodies the doctrine

- **Code is the record**; re-running is one command.
- **Pin what you can, record the rest** — `provenance.json` and the BCO stamp the
  GlyGen release (v2.11.1), the endpoints, and sha256s of every output.
- **Grounding is mechanical** — each class is a deterministic sequon computation
  over the real GlyGen glycosites + UniProt sequence; `expected_class` is checked
  in CI.
- **It's testable** — `tests/test_glyco_variants_example.py` checks determinism
  (incl. the BCO), the recipe column schema and ranking, the ground-truth
  classifications, the AlphaMissense join, and (with `jsonschema`) full BCO
  schema validation.

## Field notes (from building against the live Beta server)

- **GlyGen tool drift.** The catalog names `get_site_summary`; the live server
  (release 2.11.1) exposes `get_protein_glycosylation_sites`. GlyGen MCP is Beta
  — pin the release.
- **AlphaMissense must be keyed by UniProt accession.** Sourcing it through a
  genomic variant lookup returns another transcript's or another accession's
  score: `IFNGR2 p.T70N` matches two records, one canonically **Thr149Asn**
  (0.1203 vs the correct 0.1845), and for `SERPINC1` the first entry of dbNSFP's
  isoform array is the TrEMBL fragment `Q8TCE1`, not `P01008` (S114N 0.9209 vs
  0.8726). Indexing the array yourself does not generalise either — in a randomized
  sample of 362 genes, 18% list fewer AlphaMissense scores than isoforms (29% of
  those listing more than one), with no indication which were dropped. Hence
  ProtVar, which is accession-keyed and batched.
- **BioMCP stdio command** is `biomcp mcp`, not `biomcp run`.
- **Numbering is the real work.** `SERPINC1` literature "N135" (mature) is
  canonical `N167`. And `R220C` does not exist for `P01008` — canonical residue
  220 is Lys (252, the mature-frame equivalent, is Tyr) — so refusing it is the
  only correct answer. What the genomic lookup did instead was match a record
  where `R220C` is a valid label for a *different* UniProt entry and import its
  annotations onto a row already declined, producing the earlier run's spurious
  "Pathogenic / Ambiguous (0.473)". Asking per accession, ProtVar reports the
  reference mismatch and the row carries no annotation at all.
- **ProtVar's `clinicalSignificances` is not all ClinVar.** Keep only calls whose
  `sources` include ClinVar: `N167S` reports Pathogenic from **Ensembl alone**,
  and MyVariant has no ClinVar record there — `rs121909570` marks position 167,
  where `N167T` is the ClinVar allele, not `N167S`.
