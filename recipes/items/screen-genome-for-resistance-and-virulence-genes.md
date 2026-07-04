---
title: Screen a bacterial genome for resistance and virulence genes
parent: All recipes
grand_parent: Recipes
nav_order: 46
problem_class: Data analysis
subject_areas: [Immunology and Microbiology]
evidence_level: Reported
complexity: One skill or MCP
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-07-04
summary: Use the BLAST MCP server to search a bacterial assembly's proteins against CARD and VFDB, emitting a curated resistance- and virulence-gene profile with a committed script and pinned databases.
---

# Screen a bacterial genome for resistance and virulence genes

Hand Claude Code an assembled bacterial genome and get back a curated table of the antimicrobial-resistance (AMR) and virulence genes it carries — each hit anchored to a CARD or VFDB reference with percent identity, coverage, and the database release it was called against.

| | |
|---|---|
| **Problem class** | Data analysis |
| **Subject areas** | Immunology and Microbiology |
| **Evidence level** | Reported |
| **Complexity** | One skill or MCP |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

You have annotated one clinical or environmental isolate (the [bacterial-genome-annotation recipe](annotate-a-bacterial-genome.html) gives you a protein FASTA) and now need the biological punchline: what resistance and virulence genes does it carry? This is the step every genome-characterization paper does after annotation — screen the predicted proteins against a curated AMR reference (CARD) and a virulence reference (VFDB), then report the hits with identity and coverage so a reviewer can judge each call ([Santhosh et al., *BMC Genomics* 2025](https://doi.org/10.1186/s12864-025-12363-6)).

The mechanics are a homology search, but the footguns are real: reporting spurious partial hits because you forgot a coverage cutoff; conflating "gene present" with "gene expressed/functional"; and — the one that quietly breaks reproducibility — not recording which CARD/VFDB release the call came from, so the profile can't be reproduced when the databases move. "Solved" looks like: point the agent at the protein FASTA and two pinned reference databases, get back a `resistance_hits.csv` and `virulence_hits.csv` filtered at explicit identity/coverage thresholds, plus a provenance record naming the exact database releases.

## Recommended approach

1. **Install the [BLAST (Bio-MCP) server](../../catalog/tools/blast.html).** It wraps NCBI BLAST+ and exposes `makeblastdb`, `blastp`, and `blastn` as MCP tools. Follow the catalog page's clone-and-`pip install -e .` steps and register it with `claude mcp add`. The BLAST+ binaries must be on `PATH` first.

2. **Download and pin the reference databases.** Fetch the CARD protein homolog model FASTA ([card.mcmaster.ca](https://card.mcmaster.ca/)) and the VFDB core-dataset protein FASTA ([mgc.ac.cn/VFs](http://www.mgc.ac.cn/VFs/)). **Record the release version/date of each** — CARD is versioned (e.g., `card-data v3.2.x`); VFDB is dated by download. Compute a `sha256` of each FASTA. These are your pinned inputs.

3. **Have the agent build the databases and run the search into a committed script.** A prompt:

   ```
   Using the bio-blast MCP server, write me a script screen_resistome.py that:
     1. Builds two protein BLAST databases with makeblastdb from
        card_proteins.faa and vfdb_core_proteins.faa.
     2. Runs blastp of my proteins (annot/proteins.faa) against each,
        with -evalue 1e-10 and outfmt 6 (qseqid sseqid pident length
        qlen slen evalue bitscore), max_target_seqs 5.
     3. Keeps hits with pident >= 90 AND coverage (length/slen) >= 0.80;
        for each query keeps the single best hit per database.
     4. Writes resistance_hits.csv and virulence_hits.csv with the
        reference id, gene name, pident, coverage, evalue, and the
        source database + release string.
     5. Writes provenance.json: BLAST+ version, CARD release, VFDB
        download date, each FASTA sha256, the pident/coverage cutoffs,
        the input proteins.faa sha256, run date, and model id.
   Commit screen_resistome.py; do not paste results back as prose I
   can't audit.
   ```

   Pin the environment with a `requirements.txt` (BLAST+ via conda, plus `pandas`). Keep `screen_resistome.py`, the pinned env, and `provenance.json` under version control alongside the two database FASTAs (or their download URLs + hashes if too large to commit).

4. **Sanity-check the thresholds and hits.** The 90% identity / 80% coverage cutoffs are a conservative default for "present"; loosen to ~80%/60% only if you are deliberately looking for divergent homologs and will say so. Watch for: many partial hits (coverage just under cutoff — likely fragments across contig breaks), and a single reference matched by many queries (paralog family). Presence of a gene is not proof of a functional resistance phenotype — flag borderline calls for follow-up.

5. **Re-run and hand off.** Because the databases and cutoffs are pinned in `provenance.json`, re-running `screen_resistome.py` reproduces the profile byte-for-byte until you deliberately bump a database release (which the provenance record makes visible). The two CSVs feed a surveillance report, an outbreak comparison, or the multi-isolate [pan-genome recipe](compute-bacterial-pangenome-from-assemblies.html).

## Why this assembly

Rung 2 of the simplicity ladder — one cataloged MCP server does the whole job. The [bacterial-genome-annotation recipe](annotate-a-bacterial-genome.html) explicitly stops before AMR/virulence calling ("run the protein FASTA against a curated database as a separate step … run it from the CLI"); this recipe *is* that step, done with a cataloged tool instead of raw CLI. Rung 1 (plain Claude Code) could shell out to `blastp`, but the BLAST MCP gives the agent first-class `makeblastdb`/`blastp` tools and keeps the invocation auditable. Rung 3+ is unnecessary: a homology search against two curated databases is one well-bounded step. A dedicated resistome caller (RGI, AMRFinderPlus) with SNP models would be more sensitive to point-mutation resistance, but neither is catalogued as a Claude tool today — see **Alternatives considered**.

## Availability

Fully open. The BLAST MCP server is MIT-licensed and BLAST+ is public-domain NCBI software. CARD is freely downloadable under its own license (free for academic/non-commercial use; check terms for commercial). VFDB is freely available for academic use. All computation runs locally on your assembly — no account, no API key, no upload.

## Compute requirements

Laptop-sufficient. Building the two protein databases and running `blastp` of ~5,000 predicted proteins against CARD (~5k sequences) and VFDB core (~4k sequences) completes in well under a minute on a modern multi-core laptop with 8–16 GB RAM. The database FASTAs are tens of MB. No GPU. Scaling to hundreds of isolates is embarrassingly parallel — loop the same script per genome.

## Evidence

Reported. A peer-reviewed WGS-characterization workflow for Shiga-toxin *E. coli* validated `blast+`-based detection of AMR and virulence genes against a 131-isolate reference collection extensively characterized by conventional methods, reporting repeatability, reproducibility, accuracy, precision, sensitivity, and specificity **above 95%** for the majority of assays ([Bogaerts et al., *Microbial Genomics* 2021](https://doi.org/10.1099/mgen.0.000531)). The CARD+VFDB-after-annotation pattern this recipe wraps is the field-standard characterization move ([Santhosh et al., *BMC Genomics* 2025](https://doi.org/10.1186/s12864-025-12363-6)).

No head-to-head benchmark of the *agent-driven* BLAST-MCP assembly versus a hand-typed `blastp` command is published — the MCP loop buys first-class BLAST tools, pinned database releases, and a recorded provenance file, not a new method. The underlying BLAST+ homology search is the validated component.

## Alternatives considered

- **Plain Claude Code, no MCP (rung 1).** Fine if BLAST+ is already installed; the MCP gives the agent structured `makeblastdb`/`blastp` tools and a cleaner audit trail. Reach for rung 1 for a one-off search you will not repeat.
- **RGI / AMRFinderPlus (dedicated resistome callers).** These add SNP/protein-variant models that catch *point-mutation* resistance a straight homology search misses, and curated coverage rules. Reach for them when point-mutation resistance matters (e.g., fluoroquinolone `gyrA` mutations). Neither is catalogued as a Claude tool today — surfaced as a missing component to the catalog curator.
- **Bakta's built-in feature annotation.** Bakta calls structure (CDS, ncRNA, CRISPR) but is not a dedicated resistance caller; the [annotation recipe](annotate-a-bacterial-genome.html) produces the protein FASTA this recipe consumes.

## See also

- [BLAST (Bio-MCP)](../../catalog/tools/blast.html) — the MCP server this recipe drives.
- [Annotate a single bacterial genome assembly](annotate-a-bacterial-genome.html) — produces the protein FASTA input.
- [Compute a bacterial pan-genome from a set of genome assemblies](compute-bacterial-pangenome-from-assemblies.html) — the multi-isolate comparative recipe this feeds.

## Sources

- [Bogaerts et al., "Validation strategy of a bioinformatics whole genome sequencing workflow for Shiga toxin-producing *Escherichia coli*...," *Microb. Genom.* 2021](https://doi.org/10.1099/mgen.0.000531) — validates `blast+` AMR/virulence gene detection at >95% sensitivity/specificity; published 2021; verified 2026-07-04 (this run).
- [Alcock et al., "CARD 2023...," *Nucleic Acids Research* 51:D690–D699](https://doi.org/10.1093/nar/gkac920) — canonical CARD reference; published 2023; verified 2026-07-04 (this run).
- [Liu et al., "VFDB 2022: a general classification scheme for bacterial virulence factors," *Nucleic Acids Research* 50:D912–D917](https://doi.org/10.1093/nar/gkab1107) — canonical VFDB reference; published 2022; verified 2026-07-04 (this run).
- [Santhosh et al., "Genomic characterization of an environmental *Burkholderia thailandensis* strain...," *BMC Genomics* 2025](https://doi.org/10.1186/s12864-025-12363-6) — Bakta + CARD/VFDB characterization pattern; published 2025; verified 2026-07-04 (this run).

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=screen-genome-for-resistance-and-virulence-genes&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Fscreen-genome-for-resistance-and-virulence-genes.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
