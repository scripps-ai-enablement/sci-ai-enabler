# Plan: does the composer plugin help?

**Question being answered:** given the same scientific question, does Claude *with* the
composer plugin recommend better tooling than Claude without it?

**Design:** paired comparison. Every prompt runs twice, identical except for one flag.
One variable, so any difference is attributable to the plugin.

---

## Step 0 — Fix the two arms (already verified, nothing to do but record it)

```bash
REPO=/Users/eshav/Documents/sci-ai-enabler
cd /tmp    # run outside the repo, so the 150 skills in .claude/skills stay hidden

# WITH plugin
claude -p --strict-mcp-config --setting-sources project --plugin-dir "$REPO/composer" "$PROMPT"

# WITHOUT plugin
claude -p --strict-mcp-config --setting-sources project "$PROMPT"
```

Both were tested directly (2026-07-27): the first sees `composer:compose` plus Claude's
11 built-in skills, the second sees only the 11 built-ins. Nothing else leaks into
either arm.

Four things verified by experiment that would silently break this if changed:

1. `claude -p` **loads no plugins by default** — without these flags both arms are
   secretly identical and the plugin looks useless.
2. `--safe-mode` **cancels** `--plugin-dir` — safe mode cannot be used on the
   with-plugin arm. (Tested: `--safe-mode --plugin-dir composer` reports no `compose`
   skill.)
3. Dropping `--setting-sources project` lets `~/.claude/skills` (the `devtu-*` and
   `tooluniverse-*` skills) load into **both** arms, confounding the measurement.
4. Headless runs can have tool calls **denied** for lack of approval, which in the final
   text is indistinguishable from a missing capability. Both arms need the same
   `--allowedTools` allowlist, and denials must be logged per arm.

Both arms keep WebSearch and WebFetch. A scientist without the plugin still has a
browser; removing it would rig the result.

**Done when:** one prompt has been pasted into both commands by hand and returned two
different-looking answers.

---

## Step 1 — Build the prompt set

**Goal:** one plain-language question per recipe, phrased the way a scientist would ask
it, naming no tools.

This matters more than anything else in the plan. The prompts inside the recipes read
like *"Build a dossier for STK11. Use open-targets, uniprot, alphafold, depmap…"* —
that hands over the answer. Both arms would score identically and the whole experiment
would return "no difference."

**How:**

1. For each file in `recipes/items/*.md`, pull the `## Problem` section and the title.
2. Call Claude once per recipe to rewrite it as a single question a researcher would
   type, with an explicit instruction: never name a database, skill, plugin, or MCP
   server.
3. Extract that recipe's **tool list** from the `catalog/tools/*.html` links on its page
   — every recipe has them, 1 to 6 each.
4. **Automatic leak check:** if the rewritten question contains any tool name from its
   own list (slug or title form), reject and regenerate. Three lines of code; protects
   the entire experiment.
5. Skim all 70 by hand. This is the one manual pass worth doing.

Write to `evals/prompts.jsonl`, one row per recipe: `id`, `question`, `tools` (from
step 3), plus `problem_class`, `complexity`, `evidence_level` copied from the
frontmatter — results get sliced by those in Step 4.

Note: `map-disease-to-genes-and-pathways.md` has no prose prompt block, only install
commands. Exclude it and record why. 69 usable.

**Done when:** `evals/prompts.jsonl` has 69 rows, the leak check passes on all of them,
and they read as fair questions.

---

## Step 2 — Run both arms

**Goal:** two answers per prompt per repetition, saved raw to disk.

**How:** a script that loops over `prompts.jsonl` and, for each row, runs the two Step 0
commands. Three properties it must have:

- **Resumable** — skip any output file that already exists, so a crash at prompt 40
  doesn't cost the first 39.
- **`--output-format stream-json`** — saves the full event stream, not just the prose.
  That yields cost, turn count, and every tool call, including whether the plugin arm
  actually invoked `compose`. If that count is zero, the plugin never fired and the run
  is void.
- **3 repetitions per arm** — Claude varies between runs. Without reps a real gap can't
  be distinguished from noise.

Layout:

```
evals/out/<prompt-id>/<with|without>/<rep>/stream.jsonl
evals/out/<prompt-id>/<with|without>/<rep>/answer.md
```

Budget: 69 prompts × 2 arms × 3 reps = 414 sessions. Test calls ran ~$0.10 each on
Sonnet on trivial prompts; real compose runs do more work, so plan for **a few hundred
dollars on Opus**, less on Sonnet. Run `--limit 3 --reps 1` first to sanity-check the
pipeline before committing to the full sweep.

**Done when:** `evals/out/` is fully populated and `used_compose_skill` is true in
essentially every with-plugin run.

---

## Step 3 — Evaluate

Three layers, in this order. Each is independently useful, so work can stop after any
one of them.

### 3a. Counts (free, objective, do this first)

All 378 real components are listed in
`composer/skills/compose/data/composer-tools.json`. Per answer, count:

- how many of *that recipe's* tools it named → **recall against the curated answer**
- how many component-shaped names it gave that aren't in the catalog at all →
  **invented tools**. The compose skill explicitly forbids inventing tools, so this
  measures the plugin against its own promise.
- did it cite a curated recipe by name, and does it carry the three required caveats
  (evidence label, availability, compute tier)?
- cost, turns, word count.

### 3b. Blinded judge (cheap, explains why)

Feed both answers to a third Claude under `--safe-mode` (so the judge doesn't have the
plugin and can't favour its own tooling), labelled only A and B with the position
randomized per prompt, returning a verdict through `--json-schema` so it tallies
automatically. Re-run with A and B swapped; if the verdict flips, discard it for that
prompt as position bias.

### 3c. Ground truth (later phase, strongest evidence)

Score answers against datasets where the labels were assigned by someone else, before
this experiment existed. Deferred — but design 3a's output so items can be bolted on
without redoing anything.

#### The hard rule: ground truth is FOUND, not written

Labels must come from an external, already-published, already-labelled dataset. Claude's
role is mechanical only:

| Claude may | Claude may not |
|---|---|
| search for candidate datasets | decide what the correct answer is |
| download them | write the questions from its own knowledge |
| parse the label column | invent plausible-sounding false items |
| reshape rows into items | pick which facts are worth testing |

Why this is not a stylistic preference: if the same model authors the test and takes it,
the errors correlate. Claude asks the questions Claude finds natural, labels "true" what
Claude already believes, and writes false items that are plausible-to-Claude rather than
genuinely hard. The eval then flatters the system under test, and there is no way to tell
from the scores. A dataset built by people who had never heard of this plugin cannot do
that.

An authored item with a real citation attached is still authored. "Is WRN a selective
dependency in MSI-high colorectal lines? → true (DepMap 24Q2, PMID 30971823)" fails this
rule: Claude chose the question and chose what counts as correct, and the citation only
makes it *look* external.

#### Step 3c.1 — Inventory candidate datasets

Per recipe, search for an existing labelled dataset and record: name, version, release
date, URL, licence, the label column, class balance, and row count. If nothing is found,
that recipe is **out of scope for 3c** — it stays with 3a/3b rather than getting a
fabricated key.

Candidates to check, by recipe shape:

| Recipe shape | Candidate found datasets |
|---|---|
| ADMET prediction | TDC `ADMET_Group` official splits (already wired into `benchmark-admet-property-with-pytdc`, and it ships a leaderboard baseline) |
| Variant classification | ClinVar 3-star expert-panel classifications (pathogenic *and* benign) |
| Somatic CNV/SNV calling | SEQC2 HCC1395 tumour/normal truth sets |
| HRV / ECG | PhysioNet records with published beat annotations |
| Cell-type annotation | author-assigned labels in public cellxgene datasets |
| Cancer dependency | DepMap Chronos scores (selective *and* non-dependencies) |
| Bacterial ID from 16S | type-strain reference sequences |
| Docking pose | PDBBind holo structures, scored as RMSD < 2 Å |
| Term harmonization | UMLS/SNOMED mapping tables |

#### Step 3c.2 — Guard against contamination

Found datasets have the mirror-image problem of authored ones: a well-known benchmark is
likely in training data, so a model can score well from memory and the tooling gets undue
credit. Mitigations, in order of strength:

1. Prefer dataset **versions released after May 2026** (DepMap quarterly releases,
   ClinVar monthly drops) — the post-cutoff logic applied to the dataset rather than to
   individual items.
2. Report performance on pre- and post-cutoff subsets as separate columns.
3. Note in the writeup which datasets are likely memorized, rather than quietly averaging
   them in.

#### Step 3c.3 — Take negatives from the same source

Do not have Claude write false statements. Use datasets that already contain the negative
class — ClinVar benign variants, DepMap non-dependencies, terminated trials — so both
labels come from one external source with one labelling procedure. Roughly half the items
should be negatives: that half measures whether the tooling stops the model agreeing with
a plausible false premise, which is the failure mode the SOAT1 × familial
hypercholesterolemia case exemplifies.

#### Step 3c.4 — Score three numbers separately, never blended

- accuracy on positive items
- accuracy on negative items (a yes-machine scores 100% on positives alone)
- abstention rate — a correct "I can't determine this" should rank above a confident
  wrong answer

#### Coverage will not be uniform, and the writeup must say so

Crisply gradeable: anything ending in an identification, classification, or number (16S
ID, MS/MS compound ID, ACMG call, CNV detection, DepMap dependency, ADMET prediction, code
harmonization, docking pose). Partially gradeable: dossiers and PK estimates, where
individual facts are checkable even if the document isn't. Not gradeable this way: "draft a
Phase 2/3 protocol", "manuscript prep" — those stay with 3b. How many recipes land in each
bucket is an output of Step 3c.1, not something to estimate in advance.

**Keep the answer file where the run can't read it.** Both arms run from `/tmp` with no
repo access, so committing ground truth under `evals/` is safe as designed — but adding
`--add-dir` to a run would let it read its own answer key.

**Done when:** `evals/results.csv` has one row per prompt with the counts and the judge
verdict.

---

## Step 4 — Quantify

- **Headline:** win / tie / loss counts across the 69 prompts, plus mean invented-tool
  count per arm.
- **Average the 3 reps per prompt first**, so one noisy prompt can't dominate, and
  report the spread across reps. If within-arm spread exceeds the between-arm gap, the
  honest conclusion is "no measurable effect" — and that is a real finding, not a failed
  experiment.
- **Slice by `complexity` and `problem_class`.** This is the actionable part. Likely
  shape: the plugin barely matters for the 62 recipes needing one tool, and matters a
  lot for the 7 multi-tool harnesses. A single average across 70 heterogeneous recipes
  hides that.

---

## Step 5 — Write it up

Record the exact flags, the commit hash, the model, the date, how many prompts were
excluded and why, and the raw `results.csv`. The claim worth being able to defend is
"re-run this and you'll get the same thing" — which needs the prompt set and the flags
committed, not just the conclusion.

---

## Decide before starting

1. **Model** — Sonnet for the sweep is ~5× cheaper and probably sufficient; Opus if the
   result should reflect real usage.
2. **Reps** — 3 is right; 1 is only for pipeline testing.
3. **Scope** — all 69, or a 15-prompt pilot first. Pilot recommended.

---

## Reference: verified facts about the repo

Collected while planning, so Steps 1–3 don't have to rediscover them:

| Fact | Value |
|---|---|
| Recipes | 70 in `recipes/items/` (plus `index.md`) |
| Recipes with an extractable prose prompt | 69 (`map-disease-to-genes-and-pathways` has install commands only) |
| Recipes linking their catalog tool pages | 70 of 70 — this is the answer key |
| Tools per recipe | 1–6 (19 recipes have 1, 20 have 2, 17 have 3, 9 have 4, 5 have 5–6) |
| Catalog size | 378 tools, in `composer/skills/compose/data/composer-tools.json` |
| Index | 70 recipes + 67 systems, in `composer-index.json` |
| Frontmatter facets for slicing | `problem_class` (40 Data analysis, 19 Knowledge synthesis, …), `complexity` (62 One skill or MCP, 7 Multi-tool harness, 1 Claude Code alone), `evidence_level`, `availability`, `compute_requirements` |
| MCP servers currently configured | none — so this experiment is plugin-vs-no-plugin, not MCP-related |
| Prior manual comparison | `WITH_PLUGIN_SOAT1_*.md` / `WITHOUT_PLUGIN_SOAT1_*.md` at repo root (5 recipes done by hand) |
