# Plan: does the composer plugin help?

**Question being answered:** given the same scientific question, does Claude *with* the
composer plugin recommend better tooling than Claude without it?

**Design:** paired comparison. Every prompt runs twice, identical except for one flag.
One variable, so any difference is attributable to the plugin.

**Model:** pinned to `claude-sonnet-5` everywhere — both arms and the judge. Pin the full
ID rather than the `sonnet` alias, so a future alias change can't silently move the
model under a half-finished sweep.

**Scope:** pilot of 10 recipes first (see "Pilot set" below), then decide whether to
extend to all 70.

---

## Step 0 — Fix the two arms (already verified, nothing to do but record it)

```bash
REPO=/Users/eshav/Documents/sci-ai-enabler
MODEL=claude-sonnet-5
cd /tmp    # run outside the repo, so the 150 skills in .claude/skills stay hidden

# WITH plugin
claude -p --model "$MODEL" --strict-mcp-config --setting-sources project \
  --plugin-dir "$REPO/composer" "$PROMPT"

# WITHOUT plugin
claude -p --model "$MODEL" --strict-mcp-config --setting-sources project "$PROMPT"
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

All **70** recipes are usable. (An earlier draft of this plan excluded
`map-disease-to-genes-and-pathways` because it has no prose prompt block — only install
commands. That exclusion doesn't apply here: the question is generated from the
`## Problem` section, which all 70 recipes have, not from the recipe's own prompt block.)

For the pilot, generate questions for the 10 pilot recipes only. Keep the script capable
of all 70 so extending later is one flag.

**Done when:** `evals/prompts.jsonl` has 10 rows (pilot) or 70 (full), the leak check
passes on all of them, and they read as fair questions.

**Also require self-contained questions.** Learned the hard way: three of the first ten
generated questions referred to an input they never included ("I only have its SMILES
string", "given a paragraph naming the drug"). In a headless session there is nobody to
answer a follow-up, so Claude replies "please paste your SMILES" in one turn and the run
yields no signal at all — in both arms. Two defences, both now in place:

- the generator requires a concrete example inline (a real gene symbol, an actual SMILES
  string, a named indication) rather than "my compound";
- `ab_run.py` appends `SINGLE_SHOT_SUFFIX` — identical text in both arms — telling the
  model to assume a reasonable input, state the assumption, and answer anyway.

Regenerate any prompt that would make a reader ask "what is your X?". Judge that from the
prompt text alone, never from how the arms performed on it — the latter is selecting
prompts on the outcome.

### Pilot set (10 recipes)

Chosen to span the range of `complexity` and `problem_class` rather than to maximize the
expected effect. Stacking the pilot with multi-tool recipes would inflate the effect size
and make the estimate useless for sizing the full run.

| # | Recipe | Complexity | Problem class | Why included |
|---|---|---|---|---|
| 1 | `build-target-dossier` | Multi-tool harness | Knowledge synthesis | 5 tools; largest answer key |
| 2 | `estimate-pk-properties` | Multi-tool harness | Knowledge synthesis | multi-tool, different domain |
| 3 | `scan-drug-repurposing-candidates` | Multi-tool harness | Knowledge synthesis | multi-tool |
| 4 | `map-disease-to-genes-and-pathways` | Multi-tool harness | Knowledge synthesis | multi-tool; the one with no prompt block, so it also tests Step 1's generation path |
| 5 | `extract-structured-data-from-clinical-notes` | **Claude Code alone** | Data analysis | **negative control** — curated answer is "no tool needed", so this detects the plugin *over*-recommending |
| 6 | `benchmark-admet-property-with-pytdc` | One skill or MCP | Data analysis | has a real found benchmark, so it carries into Step 3c |
| 7 | `identify-bacterial-isolate-from-16s-sequence` | One skill or MCP | Data analysis | crisply gradeable later |
| 8 | `design-crispr-sgrnas-for-a-gene-knockout` | One skill or MCP | Experimental design | covers Experimental design |
| 9 | `find-selective-cancer-dependencies-with-depmap` | One skill or MCP | Hypothesis generation | covers Hypothesis generation |
| 10 | `draft-phase23-clinical-trial-protocol` | One skill or MCP | Manuscript prep | open-ended; only 3b applies, no ground truth possible |

That's 4 multi-tool (where the effect is expected to be largest), 1 no-tool negative
control, and 5 single-tool spanning four problem classes. All are `Fully open` and
`Laptop` except where noted, so nothing fails for missing keys or GPUs.

**The pilot's purpose is not to answer the research question.** It is to (a) prove the
pipeline runs end to end, (b) produce a real per-run cost number, and (c) estimate the
effect size and the rep-to-rep variance, which is what tells you whether the full 70 is
worth paying for and how many reps it needs. n=10 cannot support a claim about the plugin
in general — say so in any writeup of pilot results.

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

Budget — **measured**, from 6 real smoke-test runs on `claude-sonnet-5`:

| Scope | Sessions | Cost |
|---|---|---|
| Smoke test (`--limit 2 --reps 1`) | 4 | $2.52 measured |
| **Pilot (10 recipes × 2 arms × 3 reps)** | **60** | **~$45 projected** |
| Full (70 recipes × 2 arms × 3 reps) | 420 | ~$315 projected |

Per-run average is **~$0.75**, with a wide spread: $0.07 for a one-turn clarifying
question up to $1.46 for a full compose run that reads the index and fans out to
WebSearch. An earlier draft of this plan estimated $0.10–0.30/run by extrapolating from
trivial one-line probes; that was **3–7× too low**, because a real compose run does far
more work than a probe. Use the measured figure.

Run the smoke test first regardless — it is the only way to get a real per-run number
before committing to a sweep.

**Done when:** `evals/out/` is populated for all 10 pilot recipes and
`used_compose_skill` is true in essentially every with-plugin run.

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

Feed both answers to a third Claude, also `claude-sonnet-5`, under `--safe-mode` (so the
judge doesn't have the plugin and can't favour its own tooling), labelled only A and B
with the position randomized per prompt, returning a verdict through `--json-schema` so it
tallies automatically. Re-run with A and B swapped; if the verdict flips, discard it for
that prompt as position bias.

The judge is the same model as the arms, which risks self-preference — though note it
cannot favour one *arm* over the other on that basis, since both arms are the same model
too. If the pilot's judge verdicts look suspect, re-judge the 10 pairs with Opus and
compare; that's ~20 extra calls and cheap enough to do as a check.

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

- **Headline:** win / tie / loss counts across the prompts, plus mean invented-tool count
  per arm.
- **Average the 3 reps per prompt first**, so one noisy prompt can't dominate, and
  report the spread across reps. If within-arm spread exceeds the between-arm gap, the
  honest conclusion is "no measurable effect" — and that is a real finding, not a failed
  experiment.
- **Slice by `complexity` and `problem_class`.** This is the actionable part. Hypothesis
  to test, not a finding: the plugin barely matters for the 62 recipes needing one tool
  and matters a lot for the 7 multi-tool harnesses. A single average across heterogeneous
  recipes would hide that.

### For the pilot specifically

With n=10 there is no meaningful statistics — report the raw 10 rows, not an average with
a confidence interval. What to extract instead:

1. **Does the pipeline work?** Both arms produced parseable output for all 10, and the
   plugin arm actually invoked `compose`.
2. **Real per-run cost**, to price the full sweep.
3. **Rep-to-rep spread within an arm**, compared against the with-vs-without gap. If the
   gap is smaller than the noise at n=10, the full run needs more reps, not more recipes.
4. **Did the negative control behave?** On `extract-structured-data-from-clinical-notes`
   the curated answer is "no tool needed" — if the plugin arm recommends a stack anyway,
   that's a finding worth chasing before scaling up.
5. **Anything that makes the scoring look wrong** — name-matching misses, answers in an
   unexpected format. Fix the scorer now, while re-scoring is free.

Then decide: extend to 70, add reps, or fix the design first.

---

## Step 5 — Write it up

Record the exact flags, the commit hash, the model, the date, how many prompts were
excluded and why, and the raw `results.csv`. The claim worth being able to defend is
"re-run this and you'll get the same thing" — which needs the prompt set and the flags
committed, not just the conclusion.

---

## Decided

1. **Model** — `claude-sonnet-5`, pinned by full ID, for both arms and the judge.
2. **Reps** — 3 per arm. (1 only for the smoke test.)
3. **Scope** — 10-recipe pilot first, listed above. Extend to 70 only after Step 4's
   pilot checks pass.

---

## Reference: verified facts about the repo

Collected while planning, so Steps 1–3 don't have to rediscover them:

| Fact | Value |
|---|---|
| Recipes | 70 in `recipes/items/` (plus `index.md`) |
| Recipes with a `## Problem` section (Step 1's input) | 70 of 70 |
| Recipes with an extractable prose prompt block | 69 — not used by this design, but noted: `map-disease-to-genes-and-pathways` has install commands only |
| Recipes linking their catalog tool pages | 70 of 70 — this is the answer key |
| Tools per recipe | 1–6 (19 recipes have 1, 20 have 2, 17 have 3, 9 have 4, 5 have 5–6) |
| Catalog size | 378 tools, in `composer/skills/compose/data/composer-tools.json` |
| Index | 70 recipes + 67 systems, in `composer-index.json` |
| Frontmatter facets for slicing | `problem_class` (40 Data analysis, 19 Knowledge synthesis, …), `complexity` (62 One skill or MCP, 7 Multi-tool harness, 1 Claude Code alone), `evidence_level`, `availability`, `compute_requirements` |
| MCP servers currently configured | none — so this experiment is plugin-vs-no-plugin, not MCP-related |
| Prior manual comparison | `WITH_PLUGIN_SOAT1_*.md` / `WITHOUT_PLUGIN_SOAT1_*.md` at repo root (5 recipes done by hand) |
