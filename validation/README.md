# Validation

How we check that this repo's contents actually work. Internal engineering docs — not
published to the site.

Two separate things live here, and they answer different questions:

| | Question | Status |
|---|---|---|
| **A/B harness** | Does the composer plugin help, and by how much? | Built, one pilot run done |
| **Recipe validator** (`../scripts/validate_recipes.py`) | Are recipe pages well-formed and are their links alive? | Long-standing, runs in CI |

Neither currently checks whether a recipe's *science* is correct. That gap, and a concrete
plan for closing it, is in [CLAWBIO-COMPARISON.md](CLAWBIO-COMPARISON.md).

## Start here

| Document | What it is |
|---|---|
| [RESULTS.md](RESULTS.md) | **Read this first.** Plain-language findings from the pilot: what the plugin does well, where it falls short, what to do next. |
| [PLAN.md](PLAN.md) | The method in full, plus every pitfall we hit and why the flags are what they are. |
| [CLAWBIO-COMPARISON.md](CLAWBIO-COMPARISON.md) | What ClawBio's verification system has that ours doesn't, and what to adopt. |

## The A/B harness

Asks Claude the same science question twice — once with the composer plugin available, once
without — and scores both automatically. The two commands differ by exactly one flag.

```bash
# 1. generate the questions (only needed when recipes change)
python3 validation/make_prompts.py            # 10-recipe pilot set
python3 validation/make_prompts.py --all      # all 70
python3 validation/make_prompts.py --check    # verify no question names a tool

# 2. run both arms (resumable; safe to interrupt and re-run)
python3 validation/ab_run.py --limit 2 --reps 1    # smoke test first, ~$3
python3 validation/ab_run.py --reps 3             # full pilot, ~$50

# 3. score (free, re-run as often as you like)
python3 validation/ab_score.py

# 4. blinded side-by-side comparison
python3 validation/ab_judge.py
```

### Files

| File | Role |
|---|---|
| `make_prompts.py` | Turns each recipe into a scientist-voice question with all tool names stripped, and extracts the expected tools from the recipe's catalog links. Rejects any question that leaks a tool name from its own answer key. |
| `ab_run.py` | Runs each question with and without the plugin. Resumable, parallel, pinned to `claude-sonnet-5`. |
| `ab_score.py` | Counts results against the catalog → `results.csv`, `by_prompt.csv`, `summary.md`. |
| `ab_judge.py` | Shows both answers to a third Claude, blinded and position-swapped → `judge.csv`. |
| `prompts.jsonl` | The test set. Committed, so results are reproducible. |
| `out/` | Raw per-run transcripts. Gitignored — bulky and machine-specific. |

### Why running and scoring are separate

`ab_run.py` costs real money and takes ~20 minutes. `ab_score.py` costs nothing. You will
change how things are counted several times — we already did, twice — and each change must
not mean paying for 60 more sessions. So runs are saved raw to `out/` and scoring reads from
disk.

### The two arms

```bash
# with plugin
claude -p --model claude-sonnet-5 --strict-mcp-config --setting-sources project \
  --plugin-dir <repo>/composer --add-dir <repo>/composer

# without plugin
claude -p --model claude-sonnet-5 --strict-mcp-config --setting-sources project
```

Both run from a scratch directory outside the repo, so neither can see `.claude/skills`
(150 skills) or `CLAUDE.md`. Both get the same read-only tool allowlist. Both keep web
access — a scientist without the plugin still has a browser, and removing it would rig the
comparison.

Four flag behaviours were established by experiment and each would silently corrupt the
result if changed. They are documented in [PLAN.md](PLAN.md#step-0); the short version:
`claude -p` loads no plugins by default, `--safe-mode` cancels `--plugin-dir`,
`--setting-sources project` is what hides user-level skills, and denied tool calls are
indistinguishable from missing capabilities in the final text.

## Known limitations

- **The pilot is 10 recipes.** It cannot support a claim about the plugin in general.
- **Answer-key recall is partly circular.** The expected tools come from the same catalog
  the plugin ships, so "the plugin names more catalog tools" is somewhat true by
  construction. It measures steering toward our curated answers, not correctness.
- **Nothing here can fail for being scientifically wrong.** We measure whether an answer
  *missed* the right tool. We do not measure whether it named an unsuitable one. See
  CLAWBIO-COMPARISON.md.
- **Runs hit live APIs**, so repeats differ and exact numbers can't be reproduced later.
- **The judge is the same model as the arms**, which risks self-preference.
