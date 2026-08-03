# Composer plugin: does it help? — pilot results

**Date:** 2026-08-03 · **Model:** Sonnet 5 · **Scope:** 10 recipes, 60 conversations, $51.73

---

## What we did

We set up a test that asks Claude the same science question twice — once with the composer
plugin turned on, once with it off — and then compares the two answers.

The questions come from the recipes themselves, rewritten to sound like a scientist asking
for help, with every tool name stripped out. (If the question said "use Open Targets and
UniProt," both sides would score the same and the test would be meaningless.) An automatic
check rejects any question that still names a tool the recipe recommends.

We ran 10 recipes, three times per side, so the results aren't just luck. 60 conversations
in total, $51.73.

Everything is reusable: re-testing the next version of the plugin is one command.

---

## The good news

**The plugin makes Claude include the practical caveats.** Whether a tool is free or paid,
whether you need a powerful computer, how trustworthy the recommendation is. Plain Claude
mentioned the free-or-paid question **zero times out of 30 answers**. The plugin mentioned
it in most. Same pattern for the other two. This is the plugin doing exactly what it is
designed to do, and it is not a small difference.

**It picks the right tools about twice as often.** Measured against the tools each recipe
actually recommends: the plugin got 60% of them, plain Claude 34%. The plugin did better on
5 of the 10 questions and worse on none.

**It doesn't invent fake tools.** Neither side did, so this is a tie — but it is worth
knowing that nothing is being made up.

**The gap is biggest where it should be.** On the harder questions needing four or five
tools stitched together, the plugin got 67% versus 26%. On simple one-tool questions plain
Claude was nearly as good.

**It didn't over-recommend.** One recipe's correct answer is "you don't need any special
tool for this." The plugin correctly did not push a toolkit at it.

---

## The bad news

### 1. The plugin doesn't switch on about a quarter of the time

It engaged in 23 of 30 runs. On the clinical trial protocol question it never engaged —
three tries, zero. Claude had the plugin available and simply didn't reach for it. Whatever
the plugin is worth, users are currently getting about three-quarters of it, and nothing at
all on some kinds of question.

**Why, most likely:** the plugin's description says it is for people asking things like
"what tools should I use for…". But scientists don't ask that. They ask "can you help me
draft this trial plan?" The pattern in our data:

| switched on | how the question started |
|---|---|
| 3 out of 3 | "**How do I** go from a disease name…" |
| 3 out of 3 | "**How can I** get this done…" |
| 3 out of 3 | "**How should I approach** this?" |
| 2 out of 3 | "I need to know… **can you pull together**…" |
| 1 out of 3 | "I'm running a screen… **can you pull together**…" |
| 0 out of 3 | "I'm developing a drug… **can you help me turn that into**…" |

Every "how do I" question switched it on. The pure "please do this for me" question never
did. That looks like a wording fix in the plugin's description — add examples of how people
actually phrase requests. It isn't a perfect rule (one "can you help me" question did
switch it on), so treat it as a strong lead rather than a proven cause.

### 2. It costs twice as much, and it is not clear the answer is better

$1.15 per question versus $0.57.

We also had a separate Claude read both answers side by side, without being told which was
which, and pick the better one. It usually preferred the answer from **plain** Claude — 5
to 2 on usefulness. Its reasoning was consistent: plain Claude produced more actual
findings, while the plugin produced more of a shopping list of tools to go install. In one
case plain Claude surfaced a specific relevant trial and drug combination that the plugin's
answer left out entirely.

The plugin's own instructions say the deliverable is a working setup **plus a first real
result**. That second half appears to be under-delivered.

### 3. The extra cost is not going into better research

Both sides did the same amount of web searching — about 140 searches each. The difference
is that the plugin adds roughly 320 extra file and shell operations on top, reading its own
catalog files. That is where the doubled cost goes, and it isn't turning into better
answers.

### 4. It reads its own files the slow, fragile way

Its most-used tool was the command line — 184 uses. That triggered 104 blocked-permission
events, versus 52 for plain Claude. It is shelling out to read files that it could simply
read directly. This also means the plugin breaks down harder than plain Claude in any
setting where commands need approval.

### 5. Never inventing a tool is also capping quality

The plugin is required to only recommend tools in our catalog. Good for avoiding
made-up answers — and it worked. But on the bacterial-identification question, plain Claude
recommended `barrnap`, `RNAmmer`, and `megablast`: real, standard, appropriate tools that
are **not in our catalog**, so our plugin isn't allowed to mention them. Right now, gaps in
the catalog are a hard ceiling on how good the plugin's answers can be.

### 6. The required caveats are still missing about a third of the time

Even when the plugin does engage, it leaves out one of its three required caveats roughly
30% of the time, despite that being a hard rule.

---

## The honest part

**Our two measurements disagree.** One says the plugin is better (it picks the right
tools). The other says plain Claude is better (its answers were more useful). Both are
indirect guesses at quality.

There's also a catch in the first one: the list of "right tools" comes from the same catalog
the plugin carries. So "the plugin names more of our catalog's tools" is partly true by
definition. It shows the plugin reliably steers people to our curated answers. It cannot
show those answers are better than what Claude comes up with on its own.

**Other limits worth stating plainly:**

- 10 recipes is a pilot. It cannot support a claim about the plugin in general.
- The side-by-side comparison rests on 6–7 usable comparisons. Three or four flipped their
  verdict when we swapped the order of the two answers, so we threw those out — the reader
  was going by position, not quality.
- We used the same model as judge and as test subject. Worth re-checking with a stronger one.

---

## What to do next

1. **Fix the wording so the plugin switches on more often.** Cheap, and right now roughly a
   quarter of the plugin's value never reaches anyone.
2. **Have it read files directly instead of shelling out.** Cuts cost and the blocked-
   permission problem at once.
3. **Re-run the side-by-side comparison with a stronger model (~$5)** before redesigning
   anything around "plain Claude was better." It is the finding that would most change the
   plugin's direction and it currently rests on the thinnest evidence.
4. **Then build tests with real known answers** — pulled from published, already-labelled
   datasets, not written by us. That is what settles a disagreement between two indirect
   measurements.
5. **Hold off on all 70 recipes** (~$360). Better spent after the fixes, measuring the
   improved plugin.

---

## Two corrections we made along the way

Worth stating up front so the numbers above hold up:

- **Our first cost estimate was 3–7× too low.** It was extrapolated from trivial one-line
  test questions. The real figure is about $0.75 per conversation.
- **Our first "invented tools" measurement was wrong.** It reported around 4 fabrications
  per answer. On inspection it was counting spreadsheet column names, filenames, and real
  software simply missing from our catalog. After the fix: neither side invents anything.

---

## Files

| File | What it is |
|---|---|
| `evals/PLAN.md` | the method, and every pitfall we hit |
| `evals/prompts.jsonl` | the 10 questions we tested, with the expected tools |
| `evals/make_prompts.py` | writes the questions, checks none leak a tool name |
| `evals/ab_run.py` | runs each question with and without the plugin |
| `evals/ab_score.py` | counts the results |
| `evals/ab_judge.py` | the blind side-by-side comparison |
| `evals/summary.md` | the full scored numbers |
| `evals/results.csv` | one row per conversation |
| `evals/judge.csv` | the side-by-side verdicts |

To re-run the whole thing against a new version of the plugin:

```bash
python3 evals/make_prompts.py       # only needed if the recipes changed
python3 evals/ab_run.py --reps 3
python3 evals/ab_score.py
python3 evals/ab_judge.py
```
