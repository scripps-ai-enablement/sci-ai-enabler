## Recipe match

This maps directly onto a curated recipe in the knowledge base: **[Design CRISPR sgRNAs for a gene knockout](recipes/items/design-crispr-sgrnas-for-a-gene-knockout.md)** — a Claude Skill ("sgRNA Design," from the open-source SciAgent‑Skills collection) that does exactly what you're asking: tiered guide selection (validated library → CRISPick → de novo Rule Set 2/Azimuth on‑target + CFD off‑target), landed exons, PAM checks, and a committed, citable output file.

- **Evidence:** Reported — the de novo scoring (Rule Set 2/Azimuth, CFD) is the field-standard model underlying CRISPOR/CRISPick, validated on >4,000 sgRNAs; the tiered assembly itself isn't separately benchmarked.
- **Availability:** Fully open — no paid API, no key.
- **Compute:** Laptop-sufficient, seconds–minutes per gene.
- **Explicit caveat from the recipe itself:** *"Do not run rung 1 (plain Claude Code) for guide design; it will hallucinate sequences and scores."* — i.e., don't trust an LLM eyeballing candidates from memory, which is exactly the failure mode you're trying to avoid.

### To get the full, properly-scored pipeline (do this)
```
git clone https://github.com/jaechang-hits/SciAgent-Skills
/plugin install sciagent-skills
```
Then in Claude Code:
> "Design CRISPR-Cas9 knockout sgRNAs for human TP53, MANE Select transcript NM_000546.6/ENST00000269305.9, GRCh38, SpCas9 NGG PAM. Target early constitutive coding exons. Use tiered selection (validated library → CRISPick → Rule Set 2 + CFD de novo). Output `guides.csv` (sequence, PAM, exon, strand, on_target_score, off_target_assessment, source_tier) and `provenance.json` (genome build, skill version, source DB versions)."

That's the only path to real Rule Set 2/Azimuth on-target scores and a genuine genome-wide CFD off-target search — I did not fabricate those numbers below, because I can't compute them correctly without that tool.

## What I *did* verify live, this session, against real GRCh38 data

I pulled TP53's actual exon structure and sequence from the Ensembl REST API (MANE Select ENST00000269305.9, chr17, minus strand) and cross-validated the CDS start against Ensembl's own annotation (both gave genomic position 7,676,594 for the "A" of ATG — confirms the fetch is correct, not hallucinated). From that real sequence I hand-verified two independent, PAM-valid, position-vetted candidates targeting **exon 2 — the first coding exon, containing the annotated start codon**, shared by the canonical/full-length transcript:

| | Guide 1 (top pick) | Guide 2 (independent backup) |
|---|---|---|
| Protospacer (5'→3') | `CTTCCGGGTCACTGCCATGG` | `CGTCGAGCCCCCTCTGAGTC` |
| PAM | `AGG` | `AGG` |
| Strand | − | − |
| Genomic coords (GRCh38, chr17) | 7,676,591–7,676,610 | 7,676,549–7,676,568 |
| Cut site | between 7,676,593/7,676,594 — **inside the ATG start codon** | between 7,676,551/7,676,552 — codon ~15 |
| GC% | 65% | 70% |
| Poly-T (U6 terminator) check | pass | pass |
| Rationale | Cuts between the 1st/2nd base of the annotated translation start codon; any NHEJ indel disrupts initiation. | Non-overlapping site ~40 nt downstream; PTC would land >50 nt upstream of the last exon junction, satisfying the classic NMD rule — frameshift alleles should also be transcript-depleted, not just truncated. |

**What I have not verified — do not order until this is done:** Rule Set 2/Azimuth on-target score, genome-wide CFD off-target score, and whether either sequence already exists in Addgene/Broad GPP/Sanger WGE as a validated entry (their portals require live JS interaction I can't script headlessly here — check `portals.broadinstitute.org/gpp/public/gene/search`, `wge.stemcell.sanger.ac.uk`, or DepMap manually, or just run the skill above, which automates that tier check).

## Important TP53-specific design caveat

TP53 isn't produced from one transcript — an internal promoter in intron 4 drives N-terminally truncated isoforms (Δ133p53, Δ160p53) that **lack exons 1–4 entirely**. Both guides above knock out full-length p53 (p53α/TAp53) reliably, but will **not** touch those short isoforms. If your assay needs pan-isoform ablation, add a second guide in exons 5–8 (DNA-binding domain, shared by essentially all isoforms) — generate it the same grounded way, or via the skill.

## Ready-to-order oligos (lentiCRISPRv2, Addgene #52961; BsmBI/Esp3I cloning, Zhang lab convention)

Neither guide starts with G, so a G was appended per standard U6 Pol III transcription-start convention (21-nt spacer, standard and tolerated by Cas9):

**Guide 1**
```
Top:    5'-CACCGCTTCCGGGTCACTGCCATGG-3'
Bottom: 5'-AAACCCATGGCAGTGACCCGGAAGC-3'
```
**Guide 2**
```
Top:    5'-CACCGCGTCGAGCCCCCTCTGAGTC-3'
Bottom: 5'-AAACGACTCAGAGGGGGCTCGACGC-3'
```

## Methods-section template (fill in after running the scoring step)

> "CRISPR-Cas9 knockout guides targeting the TP53 translation start codon (exon 2, NM_000546.6/ENST00000269305.9, GRCh38) were designed against the reference genome; candidate sites were required to carry a valid SpCas9 NGG PAM within the first constitutive coding exon, ranked by Rule Set 2 on-target score (Doench et al. 2016, *Nat Biotechnol*) and CFD off-target score (Hsu et al. 2013, *Nat Biotechnol*; Doench et al. 2016) [via <skill/CRISPOR/CRISPick, version, run date>], and cross-checked against [validated-library source]. Guides were cloned into lentiCRISPRv2 (Addgene #52961; Sanjana, Shalem & Zhang 2014, *Nat Methods*) via BsmBI digestion."

This is a single-shot answer, so I couldn't confirm scope with you first — I assumed human GRCh38, MANE Select TP53, and SpCas9 NGG, and stopped short of inventing on/off-target numbers I can't actually compute reliably from here. Run the skill install above for the fully-scored, provenance-tracked shortlist before you commit to an oligo order.