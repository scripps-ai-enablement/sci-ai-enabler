## Assumptions I'm making (state these in your methods, since you didn't specify)

- **Target**: human *TP53*, GRCh38/hg38, canonical transcript **NM_000546.6** (protein p53α, 393 aa), gene on **chr17 minus strand**.
- **Nuclease**: SpCas9, NGG PAM, standard NHEJ knockout (frameshift indels), not HDR.
- **Delivery/cloning**: plasmid transfection into a standard line (e.g., HEK293T/U2OS-type), using the **pSpCas9(BB)-2A-Puro (PX459) V2.0** BbsI-based cloning scheme (Addgene #62988) — the same backbone the literature guides below were actually validated in. If you're using lentiCRISPRv2 or a synthetic RNP instead, the spacer sequences are identical; only the oligo overhangs below change.
- **Goal**: a functional protein-null allele suitable for making an isogenic knockout line, not a specific point mutation.

## The one design decision that matters most for TP53 specifically

Generic advice says "target early constitutive exons." For *TP53* that's a trap if applied naively. *TP53* doesn't just encode p53α — it produces ~12 isoforms (p53β/γ, Δ40p53, Δ133p53, Δ160p53 variants) from an **internal promoter inside intron 4** plus alternative splicing/translation start sites ([Δ133p53 review, PMC7698932](https://pmc.ncbi.nlm.nih.gov/articles/PMC7698932/); [p53 isoforms review, PMC4968168](https://pmc.ncbi.nlm.nih.gov/articles/PMC4968168/)). A cut in exon 2–4 disrupts full-length p53α/β/γ but **does not touch Δ133p53/Δ160p53**, which start translation downstream of that promoter. Exon 7 (and the exon 5–8 DNA-binding-domain block generally) is present in *all* known isoforms — it's the region siRNA studies use (siE7) precisely because knocking it down eliminates every isoform band.

So the design has two legitimate targets depending on your actual goal:

| Goal | Where to cut | Consequence |
|---|---|---|
| Ablate canonical p53 (the standard "p53-null cell line" use case — DNA damage response, Nutlin/MDM2 studies, most cancer biology papers) | Exon 4 | Kills p53α/β/γ; Δ133/Δ160 isoforms survive |
| Ablate p53 signaling completely, all isoforms | Exon 5, 6, or 7 (shared block) | Kills everything, but cut is later in the CDS so a small in-frame indel is slightly more likely to survive than in exon 4 |

I'm recommending the exon-4 strategy as primary (it's what's actually used in the published, validated reagents below, and it's the standard interpretation of "TP53 knockout" in the literature) and giving you an exon-5 guide as a second, pan-isoform-leaning option so you can decide which fits your experiment.

## Candidate guides (prioritizing prior experimental validation over predicted scores alone)

| # | Spacer (5'→3', 20 nt) | Exon | PAM context | Validation source | Empirical evidence |
|---|---|---|---|---|---|
| **G1 (primary)** | `CCATTGTTCAATATCGTCCG` | 4 | NGG downstream in genome (confirm in CRISPOR, see below) | Addgene plasmid [#217455](https://www.addgene.org/217455/) (Diffley lab); used in Zeng et al., *Cell* 2023, PMID 36681079 | Used to generate confirmed p53-null U2OS/RPE1 lines in a peer-reviewed paper; independently used as "TP53_Up_sgRNA" paired with G2 in a separate published protocol |
| **G2 (paired/backup)** | `GGGCAGCTACGGTTTCCGTC` | 4 | confirm in CRISPOR | Independent published protocol (paired "Down" guide with G1); also used alone in HCT116 targeting (sgTP53-E4) | Reported ~40–45% homozygous mutant clones by genotyping in HCT116 |
| **G3 (pan-isoform option)** | `TATCTGAGCAGCGCTCATGG` | 5 | confirm in CRISPOR | Addgene plasmid [#217456](https://www.addgene.org/217456/) (Diffley lab); same Zeng et al. *Cell* 2023 paper | Used alongside G1 in the same validated knockout study |
| G4 (alt. exon-4, less validated) | `GACGGAAACCGTAGCTGCCC` | 4 | confirm | Cited in secondary literature alongside G1/G2 as a third exon-4 option | Lower independent confirmation than G1/G2 |
| G5 (alt. exon-4, less validated) | `TGGTTATAGGATTCAACCGG` | 4 | confirm | Same source as G4 | Lower independent confirmation than G1/G2 |

**Recommended ordering set: G1 + G2** (co-transfect for higher knockout probability and a genotyping-friendly small deletion between the two cut sites, since they were used as a matched flanking pair), with **G3 kept as a validated backup/alternative** if you decide you need pan-isoform ablation instead.

**Important limitation — read before ordering**: I do not have a live genome-alignment tool in this session, so I have not personally recomputed Doench 2016/Azimuth on-target scores or CFD off-target scores against GRCh38 for these five sequences, and the PAM/strand annotations above are marked "confirm" rather than asserted, because gene-model/build versions can shift exact coordinates. Before ordering oligos, run this 60-second check, which is standard practice regardless of who designed the guides:

1. Go to **CRISPOR** (crispor.tefor.net) — free, peer-reviewed (Haeussler et al. 2016, *Genome Biology*), the de facto standard for this exact task.
2. Input genome **hg38**, paste in RefSeq **NM_000546.6** or the genomic region chr17:7,668,402–7,687,550, PAM = 20bp-NGG-SpCas9.
3. Locate G1–G3 in the output list (search for the 20-mers above). Confirm: (a) exact exon/PAM match, (b) Doench '16 on-target score, (c) CFD specificity score and nearest off-target mismatch count.
4. Reject/replace any guide with CFD specificity score below ~50 or an off-target with ≤2 mismatches in another exon — TP53 has no processed pseudogene, so cross-reactivity risk here is normally low, but always verify per-guide.

This gives you a defensible, numeric on-/off-target record to keep alongside the validation trail above — you'll have both "predicted score" and "used in a peer-reviewed knockout" for your citation.

## Ordering-ready oligos (PX459/lentiCRISPRv2 BbsI cloning, standard U6 CACC/AAAC overhangs)

If a spacer doesn't start with G, a G is added for U6 transcription (doesn't change targeting).

| Guide | Top oligo (order this) | Bottom oligo (order this) |
|---|---|---|
| G1 | 5'-CACCG**CCATTGTTCAATATCGTCCG**-3' | 5'-AAAC**CGGACGATATTGAACAATGG**C-3' |
| G2 | 5'-CACCG**GGGCAGCTACGGTTTCCGTC**-3' | 5'-AAAC**GACGGAAACCGTAGCTGCCC**C-3' |
| G3 | 5'-CACC**GTATCTGAGCAGCGCTCATGG**-3' | 5'-AAAC**CCATGAGCGCTGCTCAGATA**C-3' |

(G1/G2 already start with a pyrimidine so an extra G is prepended per convention; G3 already starts with a purine-adjacent G so it's used natively — double-check this against whichever cloning protocol your specific vector's documentation specifies, since some kits want the G only when absent.)

## Validation/genotyping plan (for your methods section)

1. **Indel confirmation**: PCR-amplify a ~400–600 bp amplicon flanking the cut site(s), Sanger sequence, quantify with **TIDE** or **ICE** (Synthego).
2. **Clonal isolation**: single-cell dilution or FACS sort, expand, re-genotype by Sanger + TIDE/ICE per clone; if using G1+G2 together, a clean PCR size-shift on a gel flags the flanking deletion directly.
3. **Protein-level confirmation**: Western blot for p53 loss (mRNA can persist via NMD escape, so protein loss is the operative readout for "knockout").
4. **Functional confirmation**: Nutlin-3a stabilization assay or DNA-damage (etoposide/doxorubicin) induction — absence of p53 target gene induction (e.g., *CDKN1A*/p21) confirms functional null.

## Methods section draft (edit species/line/vector as needed)

> Guide RNAs targeting exon 4 of human *TP53* (NM_000546.6; GRCh38) were selected based on prior experimental validation in the literature (Zeng et al., *Cell* 2023, PMID 36681079; Addgene plasmids #217455/#217456) and confirmed for on-target activity (Doench et al. 2016, Rule Set 2) and off-target specificity (CFD score; Doench et al. 2016) using CRISPOR (Haeussler et al. 2016, *Genome Biology*) against the GRCh38 reference genome. Oligonucleotides encoding spacer sequences [G1: CCATTGTTCAATATCGTCCG; G2: GGGCAGCTACGGTTTCCGTC] were cloned into pSpCas9(BB)-2A-Puro (PX459) V2.0 (Addgene #62988) via BbsI digestion and ligation. Exon 4 was targeted to disrupt canonical p53α/β/γ; because *TP53* also encodes N-terminally truncated isoforms (Δ133p53, Δ160p53) transcribed from an internal intron-4 promoter (Khoury & Bourdon, and related isoform literature), knockout of these isoforms was not assumed and was excluded from experimental claims / was independently addressed with an exon-5 guide (Addgene #217456), as applicable. Knockout was confirmed by Sanger sequencing/TIDE indel quantification and Western blot for p53 protein loss.

## Sources
- [PX459-TP53-exon4, Addgene #217455](https://www.addgene.org/217455/)
- [PX459-TP53-exon5, Addgene #217456](https://www.addgene.org/217456/)
- [Zeng et al., Cell 2023 (ScienceDirect)](https://www.sciencedirect.com/science/article/pii/S0092867422015793)
- [The Δ133p53 Isoforms, Tuners of the p53 Pathway (PMC7698932)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7698932/)
- [p53 Isoforms: Key Regulators of the Cell Fate Decision (PMC4968168)](https://pmc.ncbi.nlm.nih.gov/articles/PMC4968168/)
- [The TP53 Database — hg38 gene sequence/exon map](https://tp53.cancer.gov/hg38seq)
- [GenScript gRNA database description](https://www.genscript.com/gRNA-database.html)

If you tell me your actual cell line, delivery method (RNP vs. plasmid vs. lentivirus), and whether you need pan-isoform ablation, I can narrow this to a single confirmed guide set and adjust the oligo design accordingly.