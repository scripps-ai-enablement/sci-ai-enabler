---
title: Find a selective tool compound for a target
parent: All recipes
grand_parent: Recipes
nav_order: 13
problem_class: Knowledge synthesis
subject_areas: [Chemistry, Drug Repurposing and Discovery]
evidence_level: Proposed
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-08-16
summary: Rank candidate tool compounds for one target by curated affinity and measured selectivity using the GtoPdb skill, with an explicit "not profiled enough to call" verdict.
---

# Find a selective tool compound for a target

Give Claude Code a gene symbol; get back a committed table of candidate ligands for that target, each with its curated affinity, the measured selectivity window against every other target the same ligand was tested on, and a verdict that distinguishes *selective* from *never counter-screened*.

| | |
|---|---|
| **Problem class** | Knowledge synthesis |
| **Subject areas** | Chemistry, Drug Repurposing and Discovery |
| **Evidence level** | Proposed |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

You have a target and you need a small molecule to interrogate it — to knock its function down in a cell assay, to confirm a genetic hit pharmacologically, to run a counter-screen. The literature offers a dozen compounds described as "selective", and the description is frequently wrong or, more often, untested: the compound was profiled against three related receptors and nothing else, and "selective" means "we did not look".

This is where target-validation experiments go quietly wrong. A promiscuous compound produces a phenotype, the phenotype is attributed to the intended target, and the paper is not recoverable. The reference data for the question exists — IUPHAR/BPS curates ligand–target affinities out of primary literature with species, action type and affinity parameter attached — but it lives behind a REST API whose useful fields sit in sub-resources, and whose most dangerous property is that a compound with sparse data and a genuinely clean compound look identical in the output.

Solved looks like: a ranked table of candidate ligands with affinity at your target, the best affinity at any *other* target, the selectivity window in log units, how many targets the ligand was actually tested against, and a three-way verdict that refuses to call a thinly-profiled compound selective.

## Recommended approach

1. **Install the [Guide to PHARMACOLOGY skill](../../catalog/tools/gtopdb-database.html).** It supplies the endpoint map, the sub-resource routing (target and ligand metadata live in `/databaseLinks`, `/structure` and `/synonyms`, not in the base record), and two API traps you will otherwise hit: `name=` lookups are fuzzy across all fields and can return the wrong record, and the `approved=true` query parameter is *silently ignored* — use `type=Approved` instead. No account, no API key.

2. **Declare the query before running it.** Write `config.yaml` and commit it:

   ```yaml
   target_accession: P28223        # UniProt; resolved to targetId once, then pinned
   target_id: 6                    # from step 3, recorded as a literal
   species: Human                  # required, never left blank
   affinity_parameters: [pKi, pIC50]
   selectivity_threshold_log: 1.5  # ~30-fold; declared before any table is read
   min_targets_profiled: 5         # below this, no compound may be called selective
   ```

   The `species` and `selectivity_threshold_log` fields are the two that must be chosen before you see results.

3. **Resolve the target by accession, and abort if the answer is not unique.** `GET /services/targets?accession=<UniProt>` (or `geneSymbol=`); both are documented as exact-match. Write the returned `targetId`, `name`, `type` and `familyNames` into `config.yaml` and `provenance.json`. If zero or more than one target comes back, stop — do **not** fall back to `name=`, which is the fuzzy path the skill warns about.

4. **Pull the target's interactions, filtered by species.** `GET /services/targets/{id}/interactions?species=Human`. Keep every field; the ones that carry the answer are `ligandId`, `ligandName`, `affinity`, `affinityParameter`, `action`, `primaryTarget`, `selectivity` (a curator free-text note, e.g. `"Not Determined"`), `targetSpecies` and `refs[].pmid`. Two rules in `fetch_gtopdb.py`:

   - **`affinity` is a string and can be empty.** An empty affinity is not a weak affinity — it is a recorded interaction with no number attached. Route those rows to `no_affinity.csv` and never let them reach the ranking.
   - **Never pool `affinityParameter` values.** A pKi from a binding assay and a pIC50 from a functional assay are different measurements; carry the parameter as a column and compare like with like.

5. **For every candidate ligand, pull its own interaction list — this is the selectivity denominator.** `GET /services/ligands/{ligandId}/interactions` for each ligand from step 4, cached to `raw/ligand_<id>.json` so re-runs cost nothing. Then in `rank_selectivity.py`, per ligand and *within the declared species*:

   - `affinity_on_target` — best affinity at your `target_id`.
   - `best_offtarget_affinity` and `best_offtarget_name` — best affinity at any other target.
   - `selectivity_log = affinity_on_target - best_offtarget_affinity`. **Subtract; do not divide.** These are already log-scale values, so a 30-fold window is Δ 1.5; dividing 8.6 by 7.1 gives 1.2 and means nothing.
   - `n_targets_profiled` — how many distinct targets this ligand has an affinity value for at all.
   - `primary_target_flag` and `curator_selectivity_note` — carried as their own columns, as evidence, not folded into the verdict.

6. **Emit a three-way verdict that defaults to the honest one.** Write `candidates.csv` with a `verdict` column:

   - `promiscuous` — `selectivity_log` below the declared threshold.
   - `selective_by_evidence` — threshold met **and** `n_targets_profiled >= min_targets_profiled`.
   - `insufficiently_profiled` — the default, and where a compound with one or two recorded interactions lands no matter how good the number looks. State it in words next to the ratio: *"12 000-fold over 1 other target tested"* is not a selectivity claim.

7. **Record provenance and keep the raw JSON.** GtoPdb API responses carry no release version, so `provenance.json` records the **query date**, the target and ligand counts returned, the resolved `targetId`, the species filter, the threshold literals, the skill commit, and the per-row `pmid` list. Commit `config.yaml`, both scripts, `raw/`, `candidates.csv`, `no_affinity.csv` and `provenance.json`. GtoPdb releases several times a year, so the query date is what makes a later divergence visible. See the [reproducibility guide](../../guide/advanced/reproducibility.html) for the pattern.

8. **Before ordering anything, check the top candidate's affinity against a second source.** Curated selection means non-overlapping coverage, not error — see **Evidence**. Pull the same compound through the [ChEMBL polypharmacology recipe](profile-compound-polypharmacology.html) and treat a disagreement larger than your selectivity window as a reason to read the primary papers behind both numbers, which the `pmid` column gives you.

## Why this assembly

Rung 2. The whole recipe is one skill plus a script, and it stays there: every column of the output comes from GtoPdb, so a toolbelt adds surface without adding evidence.

Rung 1 fails for the usual reason and one specific one. Asked for selective ligands at a target, Claude Code alone will produce a fluent, plausibly-formatted table of compound names and pKi values from training memory, and nothing in the output reveals which numbers are real. The specific reason is that the two failure modes here are *API-shaped*: a fuzzy `name=` lookup silently returns a different target, and `approved=true` is silently ignored — both produce a clean-looking table of the wrong data. The skill documents both.

The honest boundary: a chemist who already knows the GtoPdb endpoint map is effectively at rung 1, since the deliverable is a stdlib script hitting a public unauthenticated API. The skill earns its place by supplying that map and the traps, not by doing arithmetic.

## Availability

Fully open. No account, no API key, no institutional licence. The skill code is CC BY 4.0 (SciAgent-Skills); the GtoPdb database is ODbL-1.0 with contents under CC BY-SA 4.0 — the share-alike obligation applies if you redistribute a derived database, which `candidates.csv` in a public repository is, so attribute IUPHAR/BPS.

Two things to know. **Queries leave your machine**: the target gene symbol or UniProt accession goes to `guidetopharmacology.org`, which discloses your target of interest. There is no local mirror in this recipe, so for a confidential target either accept the disclosure or use the ODbL database download instead. And the skill executes Python locally via Bash rather than as an MCP tool, so it needs a Claude Code session with Bash, not Claude.ai chat.

## Compute requirements

Laptop. Step 4 is a single HTTP call. Step 5 is one call per candidate ligand, which is the only cost that scales: a well-studied aminergic GPCR returns a few dozen ligands and finishes in under a minute; a heavily-curated family target with 200+ ligands is a few minutes of polite sequential requests. Cache every response to `raw/` — re-running the ranking after changing a threshold should make zero network calls. Total output is well under 10 MB.

## Evidence

**Proposed.** No documented attempt at this assembly — Claude driving the GtoPdb skill to rank tool compounds by selectivity — is known. The component-level and method-level evidence is unusually direct, though, and every gate above traces to one of these.

- **The resource.** GtoPdb holds 3,103 protein targets and 13,260 ligands with expert-curated affinities and key references, and the 2026 release report includes an explicit comparison of its data coverage against ChEMBL and BindingDB ([Harding et al., *Nucleic Acids Res.* 2026](https://doi.org/10.1093/nar/gkaf1067)). Curated depth, not exhaustive breadth — which is exactly why step 6 counts targets profiled.
- **The species gate.** A 2026 systematic comparison of GtoPdb against the PDSP Ki database across histamine receptors H1R–H4R found affinity deviations of **up to 3.2 log units across species** and up to **4.2 log units** between recombinant human receptors and native human brain tissue ([Bindel & Seifert, *Mol. Pharmacol.* 2026](https://doi.org/10.1016/j.molpha.2026.100139)). A 3.2-log species discrepancy is roughly 1 600-fold — fifty times wider than the 30-fold selectivity window most projects set, so an unfiltered species column does not degrade the answer, it destroys it. Verified against the API this run: zotepine's 16 GtoPdb interactions interleave `targetSpecies: "Human"` and `"Rat"` rows with no other distinguishing mark.
- **The "absence is not selectivity" gate.** The same study reports **limited ligand overlap** between the two databases, differing primary literature, and **missing or incomplete functional characterization for 69 of 302** histamine-receptor ligands — concluding that selective data inclusion "may give the impression of missing data despite substantial experimental data". That is the failure this recipe's default verdict exists to prevent, and the reason step 8 exists.
- **The component.** The [GtoPdb skill](../../catalog/tools/gtopdb-database.html) is `verification: works` (2026-07-20) and `security: cleared`, from the BixBench-evaluated SciAgent-Skills collection.

Not established: that the three-way verdict is calibrated. Nobody has measured how often `selective_by_evidence` compounds behave selectively in a cell assay. Treat the table as a triage that ranks candidates and rejects the obviously unprofiled — not as a substitute for your own counter-screen.

## Alternatives considered

**[Profile a compound's polypharmacology from ChEMBL](profile-compound-polypharmacology.html)** runs the other direction — compound in, target profile out — over a far larger and noisier corpus. Reach for it when you already have a compound and want everything ever measured on it; reach for this recipe when you have a target and no compound. The two are complements, and step 8 uses one to check the other. ChEMBL's advantage is breadth; GtoPdb's is that a human pharmacologist chose the representative measurement and attached the species and action type, which is what a selectivity comparison needs.

**The PDSP Ki database** is the natural second source for aminergic GPCRs, and Bindel & Seifert show its overlap with GtoPdb is limited enough that checking both is the defensible move. No Claude-installable component covers it, so this recipe cannot give a followable path — filed for the catalog curator.

**A [ToolUniverse](../../catalog/tools/tooluniverse.html) harness** reaches GtoPdb alongside hundreds of other tools. That is rung 3 for a question whose every column comes from one resource; take it only if selectivity triage is one step inside a wider target-validation run, in which case [validate a drug target with a go/no-go score](validate-a-drug-target-with-a-go-no-go-score.html) is the better entry point.

## See also

- [Guide to PHARMACOLOGY (GtoPdb) skill](../../catalog/tools/gtopdb-database.html)
- [Profile a compound's polypharmacology from ChEMBL bioactivity data](profile-compound-polypharmacology.html) — the compound-first mirror, and this recipe's step-8 cross-check.
- [Build a target dossier from gene name to structure to cancer dependency](build-target-dossier.html) — the wider target context this table slots into.
- [Validate a drug target with a go/no-go score](validate-a-drug-target-with-a-go-no-go-score.html) — where a tool-compound verdict feeds a decision.
- [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html)

## Sources

- [Harding S.D. et al., "The IUPHAR/BPS Guide to PHARMACOLOGY in 2026," *Nucleic Acids Res.* 2026](https://doi.org/10.1093/nar/gkaf1067) — published 2026-01; verified 2026-08-16 (this run).
- [Bindel L.J. & Seifert R., "Binding affinities for histamine receptors 1 to 4: Systematic comparison of ligands from the PDSP Ki database and IUPHAR/BPS Guide to Pharmacology," *Mol. Pharmacol.* 2026](https://doi.org/10.1016/j.molpha.2026.100139) — published 2026; verified 2026-08-16 (this run).
- [GtoPdb web services documentation](https://www.guidetopharmacology.org/webServices.jsp) — endpoints, parameters and ODbL / CC BY-SA 4.0 licence terms verified 2026-08-16 (this run).
- [`SciAgent-Skills` — `gtopdb-database/SKILL.md`](https://github.com/jaechang-hits/SciAgent-Skills/blob/main/skills/structural-biology-drug-discovery/gtopdb-database/SKILL.md) — endpoint map, exact-match rule and the silently-ignored `approved=true` caveat verified 2026-08-16 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=find-a-selective-tool-compound-for-a-target&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Ffind-a-selective-tool-compound-for-a-target.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
