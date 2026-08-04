# What we can take from ClawBio's verification system

**Reviewed:** 2026-08-04 · **Source:** [github.com/ClawBio/ClawBio](https://github.com/ClawBio/ClawBio),
files read directly (`tests/benchmark/`), not just the README.

## The finding in one sentence

**Their tests can fail when the science is wrong. Ours can only fail when a link is dead or
a metadata field is missing** — so one of our recipes could recommend entirely the wrong tool
and still pass validation.

## Side by side

| | Ours | ClawBio |
|---|---|---|
| Metadata complete | yes (`validate_recipes.py`) | yes |
| Links still resolve | yes (broken vs blocked buckets) | no |
| Code reproduces byte-identically | yes, but 1 of 70 recipes | yes, via checksums |
| **Scientific answers correct** | **no** | yes, against a labelled answer key |
| **Runs offline / repeatably** | **no** (live APIs) | yes, mock API server |
| **Pass/fail bar on quality** | **no** | yes, published thresholds |
| **With/without ablation** | yes | no |
| Automatic repair loop | yes (`repair_agent.py`) | no |

## What's genuinely similar

Both projects are the same kind of thing — a Claude plugin wrapping a catalog of life-science
skills — and independently arrived at four of the same ideas:

1. **A machine-readable catalog with per-entry labels.** We tag recipes with problem class,
   complexity, availability, compute. They tag skills with maturity tiers.
2. **One re-runnable script emitting a machine-readable report.** Ours is
   `validate_recipes.py` → `report.json`; theirs is the benchmark scorer.
3. **Reproducibility via checksums.** They export bundles with SHA-256 hashes. We record
   hashes in `provenance.json` and `tests/test_reproducible_example.py` asserts the artifact
   still matches them.
4. **A grounding rule — don't claim what you can't back.** Ours is enforced textually (the
   test asserts the summary only names terms present in the saved tables); theirs numerically,
   against known-correct genes.

## The four things worth adopting

### 1. Their answer-key file format

`tests/benchmark/ad_ground_truth.json` — 8.4 KB, Alzheimer's disease. Four design choices to
copy:

**Graded positives instead of true/false.** Three tiers with weights: tier-1 causal genes
(APP, with an OMIM ID) weighted 3.0; tier-2 GWAS-replicated (BIN1, with lead SNP and p-value)
2.0; tier-3 novel from a single 2022 paper 1.0. Getting a Mendelian gene right counts triple;
missing a speculative one barely costs anything.

**20 matched negative controls.** Explicitly matched — "same chromosome distribution, similar
expression" — so GAPDH appears as "housekeeping, no AD GWAS signal". Matching means a pipeline
can't score well by being lucky about which genes it happens to name.

**Scoring rules and the pass mark live inside the data file:**

```json
"minimum_acceptable": { "gene_recovery_rate": 0.5, "precision": 0.7, "f1": 0.6 }
```

The answer key carries its own bar. Ours are buried in Python, undocumented, and easy to
change quietly.

**A `source_references` list** recording where every label came from (Bellenguez 2022, OMIM
IDs) — the provenance that a "found, not invented" sourcing rule requires.

### 2. Measuring wrong answers, not just missed ones

This closes the biggest hole in our pilot. We count how many *correct* tools an answer names.
We have no way to notice it naming *unsuitable* ones. It bit us immediately: one pilot recipe's
correct answer is "you don't need a special tool", both arms scored 0.0, and no metric could
express "did it wrongly push a toolkit anyway."

Their fix is structural — a declared negative set, and a false-discovery rate over it.

**The subtlety that makes this real work:** you cannot infer "wrong" from "not on the correct
list." For our bacterial-identification question the expected answer is `blast`, and plain
Claude answered `barrnap`, `RNAmmer`, `megablast` — real, standard, appropriate tools absent
from our catalog. Counting "not on the list = wrong" would have marked a good answer bad.

So each recipe needs **two** lists: should-appear (we have this, from the catalog links) and
should-not-appear (we have nothing). The second must be written by someone who knows the
domain. That is the actual cost of adopting this, and it is not automatable.

### 3. The mock API server

`tests/benchmark/mock_api_server.py` serves deterministic stand-in Ensembl, GWAS Catalog,
ClinVar and ClinPGx endpoints on localhost; skills are redirected with environment variables.

We need this because our 60-run pilot hit live APIs throughout. That is part of why repeats of
the same question disagreed, and it means nobody can reproduce our exact numbers later. We are
closer than it sounds: `recipes/examples/functional-enrichment/` already has a fixtures file
and an `--offline` flag. Theirs generalizes the pattern to a server, so any recipe can be
redirected without touching its code.

**Caveat:** a mock-only CI never notices when a real API changes. The right setup is both —
mocks for repeatability, live checks on a schedule. Our link validator already does the live
half, so we would be combining rather than replacing.

### 4. A verification tier computed from repo evidence

Six tiers, derived automatically rather than assigned by hand: `spec-only` (SKILL.md only) →
`scripted` (runnable code) → `tested` (has tests) → `cli-registered` → `ci-validated` →
`bench-validated` (reserved for skills with *blocking* scientific benchmark validation).

This is a **different axis** from our `evidence_level` field. Ours describes how strong the
*scientific claim* is (Validated / Reported / Proposed). Theirs describes how much proof exists
in the repo that the thing runs. We only have the first.

Adding it would be revealing: by their definitions, 69 of our 70 recipes are `spec-only` prose
and exactly one — `recipes/examples/functional-enrichment/` — reaches `tested`. Uncomfortable,
but a script can compute it, so it is a fact rather than an opinion, and it converts "we should
test more" into a number that can visibly move.

## Where their system is weaker than the README suggests

- **Their ground truth was curated by their own team**, not lifted from an external labelled
  dataset. It cites Bellenguez 2022 and OMIM, so labels trace to literature — better than
  inventing them, weaker than downloading an official frozen benchmark split. **Take their
  format; hold a stricter sourcing bar than they did.**
- **It covers one disease.** Deep and narrow. Our 70 recipes span microbiology,
  cheminformatics, imaging and clinical text, so one answer-key file cannot stretch across
  them — which is why their file *structure* is more valuable to us than its content. We would
  need one per recipe family.
- **"4,280 tests, 92.3% passing" is not validation depth.** That is mostly their Python
  working correctly. The scientific validation is ~74 benchmark tests over one ground-truth
  file.

## What we have that they don't

- **With/without ablation.** Their benchmark measures how good the whole pipeline is; it cannot
  isolate what one component contributes. That is what `validation/ab_run.py` does, and it is
  how we found the composer plugin failing to engage in 7 of 30 runs.
- **An automatic repair loop.** `scripts/repair_agent.py` reads `report.json` and fixes what
  broke. Narrow — links and metadata, not science — but theirs reports only.

The two systems are complementary rather than competing. The trade is: take their answer keys
and offline determinism, keep our ablation and repair loop.

## Next steps, in order

1. **Write the should-not-appear lists** for a handful of recipes. Needs domain knowledge, not
   code. This is the blocking item — everything else is cheap once it exists.
2. **Add precision and false-discovery rate to `ab_score.py`** so over-recommendation becomes
   visible. Small change once step 1 exists.
3. **Adopt their answer-key file format** under `validation/ground_truth/`, filled from
   published, externally-labelled datasets rather than written by us.
4. **Generalize the offline fixture pattern into a mock server** so eval runs stop depending on
   live APIs.
5. **Add a computed `verification_tier`** to recipe frontmatter via `validate_recipes.py`.

Steps 1 and 2 are the pair worth doing first: together they fix the single biggest gap, which
is that nothing we currently run can fail because the science was wrong.
