---
title: Annotate and verify an engineered plasmid construct
parent: All recipes
grand_parent: Recipes
nav_order: 3
problem_class: Experimental design
subject_areas: [Molecular and Cellular Biology, Immunology and Microbiology]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-07-26
summary: Use the pLannotate skill to auto-annotate an engineered plasmid — promoters, resistance markers, origins, tags — and verify a construct's sequence before you clone or order it.
---

# Annotate and verify an engineered plasmid construct

Hand Claude Code a plasmid sequence (FASTA or GenBank) and get back a fully annotated map — promoters, terminators, selection markers, origins of replication, affinity tags, fluorescent proteins, and the partial feature fragments that genome annotators miss — so you can confirm a construct is what you think it is before transformation or an Addgene deposit.

| | |
|---|---|
| **Problem class** | Experimental design |
| **Subject areas** | Molecular and Cellular Biology, Immunology and Microbiology |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

Engineered plasmids accumulate decades of remixed parts, and their feature annotations are routinely incomplete or wrong. A sequence you inherited, received from a collaborator, or got back from a synthesis vendor often arrives as bare DNA with no feature track — and a missing or misidentified element (a silently truncated origin, the wrong resistance marker, a frameshifted tag) leads to failed transformations and wasted weeks ([McGuffie & Barrick, *Nucleic Acids Res.* 2021](https://doi.org/10.1093/nar/gkab374)). General microbial genome annotators (Prokka, Bakta) don't help here: they don't predict recombinant parts, wholly synthetic sequences, or engineered expression elements, and they won't flag incomplete *fragments* of features.

"Solved" looks like: drop in the construct, get back an annotated GenBank with every recognized feature, its location, its provenance database, and — critically — fragment calls that tell you when a part is present but truncated. You keep that annotated map as the record of what the construct actually is, version-controlled alongside the design.

## Recommended approach

1. **Install the [pLannotate skill](../../catalog/tools/plannotate-plasmid-annotation.html).** It ships in the [SciAgent-Skills](https://github.com/jaechang-hits/SciAgent-Skills) collection — clone once and load as a plugin:

   ```
   git clone https://github.com/jaechang-hits/SciAgent-Skills
   ```

   Then inside Claude Code run `/plugin install sciagent-skills` and confirm pLannotate appears under `/plugin` → Installed. The skill runs BLAST locally against pLannotate's bundled databases (Addgene, fpbase, Swiss-Prot, Rfam), so no upload leaves your machine.

2. **Stage the construct.** One plasmid per file — `construct.fasta` (or `.gb` if you already have partial annotation). Note whether the sequence is **circular** (a complete plasmid) or **linear** (a synthesis fragment or amplicon); pLannotate handles circular topology and will wrap features across the origin only when told the input is circular.

3. **Run the annotation and capture it to a committed artifact.** Have Claude write a small driver script rather than annotating interactively, so the run is re-runnable:

   ```
   Use the pLannotate skill on construct.fasta (CIRCULAR topology).
   Write a script annotate_plasmid.py that:
     - runs pLannotate on the input,
     - emits annotated GenBank (construct.annotated.gb),
       the feature table (features.csv), and the HTML map,
     - includes the pLannotate database version and a sha256 of the
       input FASTA in a provenance.json.
   Then report the feature table: name, type, % identity, % coverage,
   whether each call is FULL-LENGTH or a FRAGMENT, and the source DB.
   ```

   Pin the environment (`requirements.txt` or `environment.yml`) and commit `annotate_plasmid.py`, the pinned env, and `provenance.json`. Because pLannotate's databases move between releases, the recorded database version + input hash are what make the annotation auditable later — see the [reproducibility guide](../../guide/advanced/reproducibility.html).

4. **Verify against your design, reading the fragment column.** Walk the feature table against what the construct is *supposed* to contain: is the selection marker the one you expect (Amp vs Kan)? Is the origin full-length or a fragment (a truncated ori is a silent failure mode)? Is the promoter/RBS/tag intact and in-frame? pLannotate's filtering reports only the most relevant matches and explicitly flags incomplete fragments — that fragment call is the verification signal, not noise.

5. **Hand off downstream.** The annotated GenBank is the record you keep with the construct (and the file Addgene wants on deposit). For a plasmid expressed in a bacterial host you also want to characterize, the [bacterial-genome annotation recipe](annotate-a-bacterial-genome.html) covers the chromosomal side; pLannotate covers the episomal side.

## Why this assembly

Rung 2 of the simplicity ladder — one cataloged skill solves the whole problem. Plasmid annotation is a single well-bounded step with a curated-database dependency and a fragile topology/fragment surface that the [pLannotate skill](../../catalog/tools/plannotate-plasmid-annotation.html) encapsulates. Rung 1 (plain Claude Code) can't do it credibly: the value is in pLannotate's curated genetic-parts databases and its fragment-detection filter, neither of which the model can reproduce from sequence alone. Rung 3+ is unnecessary — there is exactly one tool and one input. Note that the *general* annotators in the catalog (Prokka, Bakta) are the wrong tool here by design: they don't predict engineered or synthetic parts.

## Availability

Fully open. pLannotate is GPL-3.0; the SciAgent-Skills wrapper is CC BY 4.0. All computation runs locally against bundled databases — no account, no API key, no sequence upload. FASTA and GenBank are open formats.

## Compute requirements

Laptop-sufficient. A single plasmid (typically 2–15 kb) annotates in seconds to a minute on a laptop CPU; the local BLAST databases are a one-time download of a few hundred MB. No GPU. Batch-annotating a cloning library of hundreds of constructs is still laptop-scale, just looped.

## Evidence

Reported. pLannotate is the established tool for engineered-plasmid annotation: it annotates recombinant, synthetic, and engineered expression elements that microbial genome pipelines miss, reports incomplete feature fragments, and explains the provenance of each call ([McGuffie & Barrick, *Nucleic Acids Res.* 2021](https://doi.org/10.1093/nar/gkab374)). The web server and its underlying method are widely used for construct verification and Addgene-deposit preparation.

No head-to-head benchmark of the *agent-driven* annotation versus the pLannotate web server is published — the skill buys a local, no-upload run, a pinned database version, and a committed annotated artifact, not a new method. That gap is why this recipe is `Reported`, not `Validated`.

## Alternatives considered

- **pLannotate web server (no skill).** The hosted server at `plannotate.barricklab.org` is the simplest path for a one-off and requires no install — reach for it for a single quick check. The skill is worth it when you want the run local (no upload of unpublished sequence), reproducible (pinned DB version + input hash), and committed alongside the design.
- **Prokka / Bakta (rung 2, wrong tool).** The [bacterial-genome annotators](annotate-a-bacterial-genome.html) are built for chromosomal CDS/rRNA/tRNA calling and do **not** recognize engineered parts; use them for the host genome, not the plasmid.
- **SnapGene / Benchling feature detection.** Commercial construct-management suites annotate plasmids well; reach for them if you already live in that ecosystem. pLannotate is the open, scriptable, version-controllable alternative.

## See also

- [pLannotate (Claude Skill)](../../catalog/tools/plannotate-plasmid-annotation.html) — engineered-plasmid feature annotation.
- [Annotate a single bacterial genome assembly](annotate-a-bacterial-genome.html) — the chromosomal counterpart (Bakta/Prokka).
- [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.html) — the committed-artifact pattern this recipe follows.

## Sources

- [McGuffie & Barrick, "pLannotate: engineered plasmid annotation," *Nucleic Acids Res.* 49(W1):W516–W522](https://doi.org/10.1093/nar/gkab374) — published 2021; verified 2026-06-27 (this run).
- [`jaechang-hits/SciAgent-Skills`](https://github.com/jaechang-hits/SciAgent-Skills) — pLannotate skill source; verified 2026-06-27 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=annotate-and-verify-a-plasmid-construct&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fannotate-and-verify-a-plasmid-construct.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
