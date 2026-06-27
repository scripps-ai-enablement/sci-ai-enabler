---
title: Infer the function of an uncharacterized protein from its 3D structure
parent: All recipes
grand_parent: Recipes
nav_order: 16
problem_class: Knowledge synthesis
subject_areas: [Integrative Structural and Computational Biology]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
summary: Submit a protein structure to Foldseek, pull structurally similar annotated hits across AFDB/PDB/SwissProt, and infer likely function where sequence search finds nothing.
last_verified: 2026-06-27
---

# Infer the function of an uncharacterized protein from its 3D structure

Hand Claude a `.pdb`/`.cif` coordinate file; get back a ranked table of structurally similar proteins across the AlphaFold and PDB databases, a confidence-aware function hypothesis read off their annotations, and the saved hit table — useful exactly when BLAST/HMMER return nothing because the homology is too remote for sequence to see.

| | |
|---|---|
| **Problem class** | Knowledge synthesis |
| **Subject areas** | Integrative Structural and Computational Biology |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

You have a structure but no function. The protein is a hypothetical ORF from a freshly assembled genome, a metagenomic bin, or an AlphaFold model whose UniProt entry reads "uncharacterized protein." Sequence search (BLAST, PSI-BLAST, HMMER) comes back empty or hits only other "uncharacterized" entries — the divergence is past the twilight zone where sequence identity carries signal. Structure is conserved far longer than sequence, so a *structural* search against the ~200M-model AlphaFold DB and the PDB often finds an annotated relative that sequence search misses. The bottleneck is that classic structural aligners (DALI, TM-align) are orders of magnitude too slow to scan databases that large, and stitching the hit list into a defensible function call by hand is tedious.

Solved looks like: point at one coordinate file, get a ranked match table (probability, query coverage, E-value, identity) plus a one-paragraph function hypothesis grounded in the top hits' annotations — with the caveat band ("strong" vs "suggestive" vs "no confident hit") stated, and the hit table saved so the call can be audited.

## Recommended approach

Rung 2 — one Claude Skill, the [Foldseek Structural Search skill](../../catalog/tools/foldseek-structural-search.html), which submits your structure to the public Foldseek web API and writes the hits to disk. If you don't yet have a coordinate file, obtain one first with the [AlphaFold MCP server](../../catalog/tools/alphafold.html) (by UniProt accession) or the [PDB MCP server](../../catalog/tools/pdb.html) (by PDB ID) — that fetch is the only reason this might touch a second component.

1. **Install the skill.** Verbatim steps live on the [catalog page](../../catalog/tools/foldseek-structural-search.html) (clone `google-deepmind/science-skills`, copy `foldseek_structural_search` *and* `scienceskillscommon` into `~/.claude/skills/`, install `uv`). The skill needs a real 3D file — it rejects bare sequences and accessions.

2. **Get a coordinate file in hand.** If you only have an accession, fetch the model first:

   ```
   Use the alphafold-server MCP to fetch the predicted structure
   for UniProt <ACCESSION> and save it as structures/<ACCESSION>.cif.
   Report the model's mean pLDDT — I want to know how much of this
   structure I should trust before searching on it.
   ```

   A low-pLDDT model still searches, but treat hits driven by disordered regions skeptically.

3. **Run the structural search and persist a command file.** Capture the invocation as a versioned command so the run is repeatable, not a one-off chat. Ask Claude to write `.claude/commands/foldseek-function.md`:

   ```
   Write a project command file .claude/commands/foldseek-function.md that,
   given a structure path, uses the foldseek_structural_search skill to:
     1. Run scripts/search.py on the structure against databases
        afdb-swissprot,pdb100,afdb50 (annotated DBs first, then the broad one).
     2. Save the full JSON to results/<stem>_foldseek.json and the
        match table to results/<stem>_foldseek.md.
     3. Print the top 10 hits as a table: target, description,
        probability, query coverage, E-value, sequence identity.
   ```

   Then invoke it: `/project:foldseek-function structures/<ACCESSION>.cif`. Prefer the annotated databases (`afdb-swissprot`, `pdb100`) for function transfer; add `afdb50` only to confirm the fold is real and widespread.

4. **Read the function call off the hits — with a confidence band.** Have Claude synthesize, citing only rows in the saved table:

   ```
   From results/<stem>_foldseek.md, propose a function hypothesis.
   Apply these bands and state which one applies:
     - STRONG:      a hit with probability >= 0.9 AND query coverage >= 0.7
                    to a SwissProt/PDB entry with a specific function.
     - SUGGESTIVE:  probability 0.5-0.9 or coverage 0.4-0.7; name the
                    fold/superfamily but flag the function as tentative.
     - NO CONFIDENT HIT: nothing clears SUGGESTIVE; report the closest
                    structural neighbour and say function is unassigned.
   Quote the target IDs and scores you relied on. Note if the best hits
   align only to a single domain of a multi-domain query (partial coverage
   => domain-level, not whole-protein, function transfer).
   ```

5. **Record provenance.** The saved JSON/MD are the audit trail. Have Claude write `results/<stem>_provenance.json` capturing: the Foldseek API access date, the target databases queried *with their version strings as returned by the API*, the input file's sha256, the query length, and the model/agent identity. The Foldseek web DBs are versioned and updated, so a query rerun months later can diverge — the recorded date + DB version makes that visible rather than silent. See the [reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.md) guide for the pattern.

The durable artifact is the committed `.claude/commands/foldseek-function.md`, the `uv`-pinned skill environment, and the saved `results/*_foldseek.{json,md}` + `*_provenance.json` per query.

## Why this assembly

Rung 2, and it stops here. Function-from-structure is a single search-then-interpret step; one skill wraps the whole thing, including the API call and the formatted hit table. Rung 1 (plain Claude Code) can't do it — Claude has no Foldseek binary and the hosted search needs a real structural-alphabet encoding of your coordinates, which the skill's `search.py` performs. A rung-3 toolbelt buys nothing for a one-shot function call; the only legitimate second component is the optional structure-*fetch* step (AlphaFold/PDB MCP), and even that is skipped when you already hold a `.pdb`/`.cif`. No autonomous system is warranted.

## Availability

Fully open. The skill is Apache-2.0 (docs CC-BY-4.0); it calls the public [Foldseek Search](https://search.foldseek.com/) web API with no key and no quota account. The target databases (AlphaFold DB, PDB100, SwissProt-AFDB, BFVD, CATH50, MGnify) are public. Foldseek itself is GPLv3, but this skill uses the hosted service rather than a local install, so there is no GPL obligation on your code. Local `uv` and Python are the only environment dependencies. The hosted API rate-limits large batches — for hundreds of queries, install Foldseek locally (out of this recipe's scope) and point it at downloaded DBs.

## Compute requirements

Laptop. Each query is a single structure upload; the heavy search runs server-side on the Foldseek service and a typical single-domain protein returns ranked hits in well under a minute (queue depending). Output is two small text files (JSON + Markdown) per query. No GPU, no local database download. The only local cost is the optional structure fetch and any visualization you do afterward.

## Evidence

`Reported`. Foldseek is a peer-reviewed, field-defining structural search method — van Kempen et al. (*Nature Biotechnology* 2023) show it runs four-to-five orders of magnitude faster than DALI/TM-align/CE while retaining 86–133% of their sensitivity, making database-scale structural search tractable for exactly the function-inference use case here ([doi:10.1038/s41587-023-01773-0](https://doi.org/10.1038/s41587-023-01773-0)). Structure-based function transfer for proteins that sequence search cannot reach is the documented application of the AlphaFold DB + Foldseek pairing across the literature (Varadi et al., AlphaFold DB, [*Nucleic Acids Res.* 2024](https://doi.org/10.1093/nar/gkad1011)). The skill is a maintained Google DeepMind release that wraps the same hosted API.

What is *not* independently benchmarked is the convenience layer — Claude driving this specific skill to assemble the ranked table and the banded function call. That layer is `Reported` (a vendor-maintained, runnable skill) rather than `Validated` (no head-to-head paper of "Claude + Foldseek skill" vs a hand-built notebook). The numbers above are component-level; the assembly is rational and runnable but not separately measured.

## Alternatives considered

- **Sequence search first (BLAST/HMMER/[InterPro](../../catalog/tools/interpro-database.html)).** Always try this before structural search — it's faster and, when it hits, more directly interpretable. This recipe is the fallback for when sequence search returns nothing or only "uncharacterized" hits. InterPro/Pfam domain scanning is the natural sequence-side companion.
- **[Score point mutations with ESM](score-protein-variants-with-esm.html).** Different question: that scores *variants* of a known protein; this assigns *function* to an unknown one. Use ESM once you know what the protein is.
- **[Triage an AlphaFold model for docking](triage-alphafold-model-for-docking.html).** The structure-*quality* sibling. Run that to decide whether a model is fit for modelling; run this to decide *what the model is*. They share the AlphaFold/PDB fetch step.
- **Local Foldseek + downloaded databases (rung 3).** The right escalation for high-throughput annotation (thousands of ORFs from a genome) or when the hosted service's rate limits or data-residency rules bite. That's a CLI pipeline, not this single-skill recipe.

## See also

- [Foldseek Structural Search (Claude Skill)](../../catalog/tools/foldseek-structural-search.html)
- [AlphaFold MCP Server](../../catalog/tools/alphafold.html) — fetch a model by UniProt accession to feed the search.
- [PDB MCP Server](../../catalog/tools/pdb.html) — fetch experimental coordinates by PDB ID.
- [InterPro Database](../../catalog/tools/interpro-database.html) — sequence-side domain annotation to try first.
- [Triage an AlphaFold model for structure-based drug design](triage-alphafold-model-for-docking.html) — structure-quality counterpart for the same model.
- [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.md)

## Sources

- [van Kempen M. et al., "Fast and accurate protein structure search with Foldseek," *Nature Biotechnology* 2023](https://doi.org/10.1038/s41587-023-01773-0) — published 2023-05; verified 2026-06-27 (this run).
- [Varadi M. et al., "AlphaFold Protein Structure Database in 2024," *Nucleic Acids Res.* 2024](https://doi.org/10.1093/nar/gkad1011) — published 2023-11.
- [`google-deepmind/science-skills` — `foldseek_structural_search/SKILL.md`](https://github.com/google-deepmind/science-skills/blob/main/skills/foldseek_structural_search/SKILL.md) — inputs, `scripts/search.py` invocation, database allowlist, JSON+MD outputs; verified 2026-06-27 (this run).
- [Foldseek Search web service](https://search.foldseek.com/) — verified 2026-06-27 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=infer-protein-function-from-structure&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Finfer-protein-function-from-structure.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
