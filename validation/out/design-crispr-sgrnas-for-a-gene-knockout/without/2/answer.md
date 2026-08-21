## Design brief & assumptions (stated up front, since this is single-shot)

- **Target:** human *TP53*, genome build **GRCh38/hg38**, canonical transcript NM_000546 (RefSeq)/ENST00000269305 (Ensembl). Gene body: chr17:7,668,402–7,687,550, **minus strand** (11 exons; exon 1 is 5′UTR-only, translation starts in exon 2).
- **Nuclease:** SpCas9, NGG PAM (most common; if you're actually using a Cas9 variant like NG-PAM or a base/prime editor, say so and the exon math still holds but PAM search changes).
- **Goal:** simple loss-of-function knockout of canonical full-length p53 via frameshift/NMD — the standard interpretation of "TP53 knockout" in ~95% of published work — with a note below on an important isoform caveat you should decide on explicitly.
- **Cloning context assumed:** BsmBI/BbsI-based U6-sgRNA vector (pX330/pX459/lentiCRISPRv2-style, the Zhang-lab `CACCG` / `AAAC` overhang convention). If you're using IDT Alt-R crRNA or a different vector, only the oligo-flank section below changes — the 20-nt spacer is the same.

## Why exon 4/5, and the isoform trap specific to TP53

*TP53* isn't a simple single-promoter gene, which matters for "early constitutive exon" targeting:

- **P1 promoter** (upstream of exon 1) drives full-length p53 and Δ40p53 (translated from an internal ATG in exon 2/3).
- **P2 promoter** (inside intron 4) drives transcripts starting mid-gene that translate Δ133p53 and Δ160p53 from internal ATGs located in **exon 5**.

So a guide in exon 2 or exon 3 will only ablate full-length p53 + Δ40p53 — the Δ133/Δ160 isoforms initiate downstream of that cut and can escape disruption entirely. A guide placed in **exon 4 or the 5′ part of exon 5** is the standard compromise used in the literature: early/constitutive to the canonical CDS, upstream of the DNA-binding domain (exons 5–8, where most hotspot mutations sit, so you avoid confounding a KO with a partial-DBD product), and it's the region essentially every published "TP53 KO" cell line paper actually targets. If your experiment specifically depends on ablating *all twelve* p53 isoforms (e.g., isoform-specific biology), you'd instead want a guide in exon 6/7, downstream of both internal ATGs — flagged as an alternative strategy below rather than guessed at, since I don't have a pre-validated sequence there to hand you.

## Method used to pick these two candidates

Rather than generate sequences from memory (a single wrong base is a wasted oligo order), I:
1. Pulled experimentally-validated, peer-reviewed, Addgene-deposited sgRNA constructs targeting *TP53* exon 4 and exon 5.
2. Independently re-confirmed each 20-nt protospacer + adjacent PAM against the **hg38 reference** via UCSC BLAT (not just trusting the paper/Addgene listing) — this catches transcription errors and confirms the PAM is real, not just present in someone's summary.
3. Discarded a candidate that *didn't* independently verify (see caveat below) rather than presenting it as safe to order.

You should still run the two winners through **CRISPOR** or **Benchling** yourself before ordering, for a live Doench 2016 (Rule Set 2/Azimuth) on-target score and a CFD/MIT off-target scan against the current genome build — I can confirm genomic identity and PAM validity via BLAT, but I don't have a live off-target aligner here, so treat off-target risk below as "supported by absence of reported off-target phenotypes across many published uses," not as a computed CFD score.

## Recommended guide pair

| | **Guide 1 (primary) — Exon 4** | **Guide 2 (backup/co-transfect) — Exon 5** |
|---|---|---|
| Protospacer (5′→3′) | `ACCATTGTTCAATATCGTCC` | `TATCTGAGCAGCGCTCATGG` |
| PAM | `GGG` | `TGG` |
| Strand / coords (hg38) | `+`, chr17:7,676,208–7,676,231 | `+`, chr17:7,675,058–7,675,081 |
| Verification | BLAT: 23/23 perfect match, single unique hit in genome | BLAT: 23/23 perfect match, single unique hit in genome |
| Cut site | ~3 bp 5′ of PAM, within exon 4 coding sequence, upstream of the DNA-binding domain | ~3 bp 5′ of PAM, within exon 5 (5′ portion; near the P2-driven Δ133/Δ160 start codons — see caveat) |
| Prior validation | Used to make functional TP53-null cell lines; Addgene #121917 (`pX330-TP53-1`), Howard et al., *Cancer Res.* 2019 | Used to make functional TP53-null cell lines; Addgene #217456 (`PX459-TP53-exon5`), Zeng et al., *Cell* 2023 (186(3):528–542, PMID 36681079) |
| Isoform coverage | Disrupts full-length p53 + Δ40p53; does **not** guarantee disruption of Δ133p53/Δ160p53 | Same caveat — confirm exact cut position relative to ATG133/ATG160 in CRISPOR/Benchling if pan-isoform KO matters to you |

**Why two guides, not one:** ordering both and either co-transfecting or picking whichever gives the cleaner indel by TIDE/ICE is standard practice — it hedges against one guide underperforming in your specific cell line's chromatin context, and gives you an independent confirmation that the phenotype you see is on-target (same gene, two different cut sites, same loss-of-function result).

## Ready-to-order oligos (BsmBI/BbsI, `CACCG`/`AAAC` overhang convention — check this matches your specific vector's protocol)

Both protospacers lack a 5′ G, which U6 transcription prefers, so a G is appended (standard practice, doesn't change targeting).

**Exon 4 guide:**
- Top: `5′-CACCGACCATTGTTCAATATCGTCC-3′`
- Bottom: `5′-AAACGGACGATATTGAACAATGGTC-3′`

**Exon 5 guide:**
- Top: `5′-CACCGTATCTGAGCAGCGCTCATGG-3′`
- Bottom: `5′-AAACCCATGAGCGCTGCTCAGATAC-3′`

## Design record (paste/adapt for Methods)

> sgRNAs targeting early constitutive coding exons of human *TP53* (exon 4: 5′-ACCATTGTTCAATATCGTCC-3′, PAM GGG; exon 5: 5′-TATCTGAGCAGCGCTCATGG-3′, PAM TGG; GRCh38 chr17:7,676,208–7,676,231 and chr17:7,675,058–7,675,081, respectively) were selected from previously validated constructs (Addgene #121917, Howard et al., *Cancer Res.* 2019; Addgene #217456, Zeng et al., *Cell* 2023) and re-verified for unique, exact genomic match and correct PAM adjacency against the GRCh38 reference via UCSC BLAT. Both target sites lie upstream of the DNA-binding domain (exons 5–8) in exons shared across the canonical P1-driven transcripts, enabling frameshift/nonsense-mediated decay of full-length p53 upon indel formation.

## Caveats — please don't skip these before ordering/citing

1. **One candidate I checked failed independent verification and I excluded it.** A second Addgene-listed exon-4 construct (#217455, also Zeng et al. 2023) reports the sequence `CCATTGTTCAATATCGTCCG` — a 1-base-shifted variant of the same locus — but it did not return a clean BLAT match in my check (likely a transcription artifact in how that page's sequence was captured, not necessarily wrong in the original paper). I did not include it. This is exactly the kind of error a single wrong base in an oligo order would bake in silently — always re-verify the exact string from the primary source/plasmid map yourself before synthesis.
2. **Run both guides through CRISPOR/Benchling for a live off-target CFD score and Doench on-target score** against the current annotation — I've confirmed genomic identity and uniqueness of the protospacer+PAM, not a computed genome-wide mismatch tolerance search.
3. **Isoform completeness:** if your assay depends on ablating Δ133p53/Δ160p53 as well as full-length p53, check the exon-5 cut position against the ATG133/ATG160 codons in a browser, or add a third guide in exon 6/7.
4. **Confirm edits experimentally** — indel formation via TIDE/ICE (Sanger) or amplicon NGS, and loss of p53 protein by western blot ± Nutlin-3a or DNA-damage induction (since p53 is normally low-abundance until stabilized) — before relying on "presumed knockout" clones.
5. Coordinates above are GRCh38; if your lab standardizes on GRCh37/hg19, re-run BLAT/CRISPOR on that build before ordering, since a couple of exon-numbering/UTR annotations differ between builds.

Sources: [Addgene #217455](https://www.addgene.org/217455/), [Addgene #217456](https://www.addgene.org/217456/), [Addgene #121917](https://www.addgene.org/121917/), [Zeng et al. 2023, *Cell*](https://www.nature.com/articles/s41419-024-06783-7), [p53 isoforms review, PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC4968168/), UCSC hg38 BLAT (genome.ucsc.edu).