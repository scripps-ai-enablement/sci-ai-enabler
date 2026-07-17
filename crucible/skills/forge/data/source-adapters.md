# Source adapters — the pluggable fragment-mining tier

Crucible mines fragments from three tiers of source. The first two are fixed; the third is an
**open, pluggable tier** so new raw / unstructured sources can be added without touching the core
pipeline. Every adapter obeys the same contract and emits `fragment.schema.json` objects.

## Adapter contract
```
extract(query, cutoff_date) -> Fragment[]
```
- `query`: the framed goal + anchors from Stage 0 (disease id, gene/target seeds, drug space).
- `cutoff_date`: only return evidence with `snapshot_date <= cutoff_date`. This is what makes
  retrospective time-sliced evaluation (eval T1) possible — an adapter that ignores the cutoff
  breaks the benchmark.
- returns typed fragments with normalized ontology ids and a resolvable `source_id`.

An adapter **self-registers** by adding a row to the registry below; the Stage-1 source-discovery
step reads this registry, proposes which adapters are relevant to the goal, and invokes them.

## Registry

### Tier 1 — literature (fixed)
| corpus | tool | fragment shape |
|---|---|---|
| `literature/pubmed` | `pubmed` (`search_articles`, `get_full_text_article`) | relation extracted from abstract/full text |
| `literature/biorxiv` | `biorxiv` (`search_preprints`, `get_preprint`) | same, preprint |
| `literature/consensus` | `consensus.search` | claim + citation |

### Tier 2 — preprocessed structured databases (fixed)
| corpus | tool | fragment shape |
|---|---|---|
| `structured/opentargets` | `ot` (GraphQL associations, known drugs) | target–disease / drug–disease association |
| `structured/chembl` | `chembl` (mechanism, bioactivity, ADMET) | drug–target mechanism; ADMET property |
| `structured/ctrials` | `c-trials` (`search_trials`, `analyze_endpoints`) | trial outcome / status (feeds G3) |

### Tier 3 — raw / unstructured (pluggable; add rows here)
| corpus | tool | fragment shape | status |
|---|---|---|---|
| `raw/geo` | `gget` skill / `tooluniverse` / NCBI E-utilities | "gene ↑/↓ in condition [GSE…]" differential-expression signal | **reference adapter (shipped)** |
| `raw/pride` | `tooluniverse` / PRIDE API | protein abundance change | proposed |
| `raw/metabolomics-workbench` | `tooluniverse` / MW REST | metabolite level change | proposed |
| `raw/cellxgene` | `gget cellxgene` | cell-type-resolved expression | proposed |
| `raw/gwas-catalog` | `tooluniverse` / GWAS Catalog | variant–trait association | proposed |

**GEO is the reference adapter, not the whole tier.** To add a source: implement `extract` against
its API (prefer one reachable via `tooluniverse` or `biomcp` so it works inside the agent loop),
normalize entities to the shared ontology ids, stamp `snapshot_date`, add a registry row. The rest
of the pipeline (bridge discovery, gauntlet, tournament) is source-agnostic.

## Normalization (required for cross-corpus bridging)
- genes/proteins → Ensembl / HGNC (resolve via `biomcp`)
- diseases/phenotypes → EFO / MONDO (resolve via `ot search_entities`)
- drugs/compounds → ChEMBL / ChEBI (resolve via `chembl compound_search`)

Two fragments from different corpora are only bridgeable once their subjects/objects share an
ontology id. Corpus diversity across a bridge's fragments is a scored novelty signal in Stage 2.
