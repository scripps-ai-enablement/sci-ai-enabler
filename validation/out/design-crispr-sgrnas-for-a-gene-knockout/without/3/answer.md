One thing up front: I don't have programmatic access to a genome browser, BLAST, or CRISPOR's scoring engine from this environment, so I'm **not** going to hand you a specific 20-nt sequence and claim it's genome-verified — for oligos you're actually ordering, a subtly wrong base from my memory is worse than no sequence at all. What I can give you is the exact, reproducible design protocol (tool inputs, thresholds, gene-specific caveats for TP53, and a methods-ready record template) so you get a verified answer in one pass through the right tool.

**Assumption stated:** target is human TP53, reference GRCh38, MANE Select transcript NM_000546.6 / ENST00000269305.9, using SpCas9 (NGG PAM). If your actual gene/build/nuclease differs, swap those inputs into the same pipeline below — the logic doesn't change.

## 1. Gene-specific target-selection logic (the part a generic tool won't tell you)

- **Exon architecture:** TP53 has 11 coding exons (exon 1 is non-coding). Exons 2–4 encode the transactivation domain and are constitutive across essentially all annotated full-length isoforms — good early-knockout territory (frameshift here should trigger NMD or truncate before the DNA-binding domain in exons 5–8).
- **Critical caveat specific to TP53:** there's an internal promoter in intron 4 that drives the Δ40p53 (p47) isoform from an alternate ATG in exon 5. A cut confined to exon 2 alone can leave Δ40p53 intact, producing a partial/confounded knockout. Two ways to handle this:
  - Target **exon 4** (downstream of the Δ40 promoter's exon 1/2 but still upstream of exon 5's internal ATG and well before the DBD) — this is the most common choice in the literature for exactly this reason, or
  - Pick guides in **both exon 3 and exon 5** if you need to guarantee disruption of both full-length p53 and Δ40p53.
- Avoid exon 1 (5′UTR, non-coding) and avoid the very first ~15 codons of exon 2 if you're worried about reinitiation at a downstream ATG rescuing a truncated product.

## 2. Reproducible design protocol (run this once, ~5 minutes)

1. Go to **CRISPOR** (crispor.tefor.net) — it's the standard free tool that does everything you listed in one pass: PAM finding, Doench 2016/Azimuth on-target score, MIT + CFD off-target scores, and flags guides present in prior published libraries.
2. Input: paste the genomic region spanning exons 3–5 of NM_000546 (CRISPOR accepts a gene symbol + "TP53" lookup directly, or paste FASTA from Ensembl for ENST00000269305), genome = **GRCh38/hg38**, PAM = **NGG (SpCas9)**.
3. Restrict candidate guides to those whose **cut site (3 bp upstream of PAM)** falls within the coding sequence of exons 3 or 4, in the sense strand or antisense — either is fine.
4. Filter/rank by:
   - **On-target (Doench '16) score ≥ 60** — higher cutting efficiency.
   - **CRISPOR specificity/MIT off-target score ≥ 70**, and **zero 0–2 mismatch off-targets in any exon** (check the "off-targets" output table, not just the summary score).
   - **No off-target within 10 bp of another gene's TSS or a known essential gene's exon.**
5. For "prior experimental validation," cross-check your top 3–5 candidates against:
   - **GenomeCRISPR** (genomecrispr.dkfz.de) — searchable database of guides used in published functional screens, TP53 included.
   - **Addgene** — search "TP53 sgRNA" or "TP53 CRISPR" for deposited, sequence-confirmed plasmids from published knockout papers; a guide that matches one already in a citable plasmid is your strongest "prior validation" evidence.
   - The original **GeCKOv2** library (Sanjana, Shalem & Zhang, *Nat Methods* 2014; Addgene #1000000048/49) contains 3 pre-scored TP53 guides per half-library — pull the exact sequences from the Addgene-hosted library CSV rather than a secondary source, since that CSV is the authoritative, citable record.

## 3. Selection criteria to apply (put this table in your methods)

| Criterion | Threshold | Tool/source |
|---|---|---|
| Target exon | Exon 3 or 4 (constitutive, pre-DBD, accounts for Δ40p53) | Ensembl/MANE annotation |
| Cut site position | Within first ~30% of CDS, avoid first 15 codons | Manual, from CRISPOR output |
| PAM | NGG, unambiguous, not in a repeat/low-complexity region | CRISPOR |
| On-target score | Doench 2016 Rule Set 2 ≥ 60 | CRISPOR |
| Off-target specificity | MIT score ≥ 70; 0 exonic off-targets at ≤2 mismatches | CRISPOR |
| Prior validation | Present in GeCKOv2 library or a citable Addgene plasmid/publication | GenomeCRISPR, Addgene |

## 4. Order and documentation

- Once CRISPOR gives you 3 ranked candidates meeting the above, add the standard cloning overhangs for your vector (e.g., for lentiCRISPRv2/BsmBI: 5′-CACCG[20nt]-3′ top strand, 5′-AAAC[revcomp 20nt]C-3′ bottom strand; prepend a G if the guide doesn't already start with one, for U6 promoter transcription).
- For your methods section, record per guide: genomic coordinates (GRCh38), transcript/exon, full 20-nt + PAM sequence as output by CRISPOR, on-target and off-target scores with tool version, and the citation for any prior-validation source (paper or Addgene plasmid ID). That's the "clear record of why each candidate was chosen" — CRISPOR's output page itself is exportable and citable (Concordet & Haeussler, *Nucleic Acids Res.* 2018), plus the exon-selection rationale above (Δ40p53 caveat) as your own methodological note.

If you paste your actual CRISPOR output table back to me (even a screenshot or the exported CSV), I can help you rank and pick the final 2–3 guides and write the methods paragraph — I just can't manufacture the raw scored sequences myself without that tool.