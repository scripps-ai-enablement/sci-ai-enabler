## MEK1/2 (MAP2K1 / MAP2K2) Target Dossier

**Assumption stated up front:** you didn't specify a compound structure, so I've treated "MEK1/2" as the canonical kinase targets **MAP2K1/MEK1** (UniProt [Q02750](https://www.uniprot.org/uniprotkb/Q02750/entry)) and **MAP2K2/MEK2** (UniProt [P36507](https://www.uniprot.org/uniprotkb/P36507/entry)) — this is a target-biology dossier, not an ADMET readout on your specific chemotype.

### 1. Mechanism & disease links
MEK1/2 are the dual-specificity Ser/Thr/Tyr kinases that sit between RAF and ERK1/2 in the RAS→RAF→MEK→ERK cascade, controlling proliferation, differentiation, and survival ([GeneCards](https://www.genecards.org/card/MAP2K1)).

- **Germline (RASopathy):** Activating germline mutations in MAP2K1/MAP2K2 cause ~25% of mutation-positive **cardiofaciocutaneous (CFC) syndrome** cases, alongside BRAF/KRAS ([EJHG](https://pmc.ncbi.nlm.nih.gov/articles/PMC2947095/), [MedlinePlus](https://medlineplus.gov/genetics/gene/map2k1/)).
- **Somatic (cancer):** Recurrent hotspot mutations (clustering in the N-terminal negative-regulatory helix, e.g. F53, Q56, K57, D67) relieve autoinhibition and drive constitutive MAPK signaling:
  - **Melanoma** — ~8% of cases carry MAP2K1/2 mutations, largely co-occurring with or substituting for NRAS ([Nat Genet](https://www.nature.com/articles/ng.1026)).
  - **Lung adenocarcinoma** — a distinct, KRAS/EGFR-independent, targetable ~0.5–1% subset ([PMC4401580](https://pmc.ncbi.nlm.nih.gov/articles/PMC4401580/)).
  - **Colorectal cancer** — rare (<1%) but implicated as an **EGFR-inhibitor resistance mechanism** ([PMC8144646](https://pmc.ncbi.nlm.nih.gov/articles/PMC8144646/)).
  - Also reported in papillary thyroid cancer, Langerhans cell histiocytosis, and hairy cell leukemia variants.
- **Strategic note:** this target already has **four FDA-approved allosteric inhibitors** (trametinib, cobimetinib, binimetinib, selumetinib), each paired with a BRAF inhibitor or used alone for NF1-driven tumors. If your hit binds the same allosteric pocket, expect a crowded IP/differentiation landscape, not a novel-target story.

### 2. Domains & PTMs
Architecture (MEK1 numbering; MEK2 is highly homologous) ([UniProt Q02750](https://www.uniprot.org/uniprotkb/Q02750/entry), [ScienceDirect topic overview](https://www.sciencedirect.com/topics/biochemistry-genetics-and-molecular-biology/map2k1)):

| Region | Residues | Notes |
|---|---|---|
| N-terminal negative-regulatory domain (NRD, A-helix) | 1–67 | Autoinhibitory; cancer/CFC hotspots (F53, Q56, K57, D67) sit here |
| Kinase domain | 68–361 | β1–β5 N-lobe, αC-helix (120–140), catalytic HRD loop (188–192), DFG motif (208–210) opening the activation loop, ending in SPE (231–233) |
| Proline-rich insert | ~262–326 (RAF1-binding subregion 270–307) | Docks RAF1; disordered |
| C-terminal domain | 361–393 | |

Key PTMs:
- **Activating:** Ser218/Ser222 phosphorylation by BRAF/MEKK1 turns on kinase activity; NEK10-promoted autophosphorylation of the same sites occurs after UV stress ([iPTMnet](https://research.bioinformatics.udel.edu/iptmnet/entry/Q02750/), [UniProt](https://www.uniprot.org/uniprotkb/Q02750/entry)).
- **Negative feedback:** ERK2 phosphorylates Thr292, which blocks a subsequent PAK-mediated Ser298 phosphorylation — a classic ERK→MEK feedback brake.
- **Pathogen hijack:** *Yersinia* YopJ acetylates the activation loop, sterically blocking phosphorylation entirely — useful evidence that this region is druggable/modifiable.
- **Pathway-level feedback:** ERK-induced DUSP6 (MKP-3) dephosphorylates ERK and is itself regulated by SUMOylation (K234) vs. ubiquitin-proteasome turnover — the dominant negative-feedback node you'll be fighting against pharmacodynamically ([Sci Adv](https://www.science.org/doi/full/10.1126/sciadv.aaz0361), [CMLS review](https://pmc.ncbi.nlm.nih.gov/articles/PMC5075022/)).

### 3. Subcellular localization
Primarily **cytoplasmic**, with regulated **nuclear shuttling**; membrane recruitment is largely scaffold-dependent via **KSR1**. MEK1 additionally relocalizes dynamically to the **centrosome (prometaphase)**, **spindle midzone (anaphase)**, and **midbody (telophase/cytokinesis)**, hinting at ERK-independent mitotic functions worth checking if your hit shows cell-cycle phenotypes. MEK2 is described more simply as cytoplasm/peripheral-membrane, again via KSR1 ([UniProt Q02750](https://www.uniprot.org/uniprotkb/Q02750/entry), [UniProt P36507](https://www.uniprot.org/uniprotkb/P36507/entry)).

### 4. Structural confidence
Coverage is unusually deep for a kinase — over 40 PDB structures of the kinase domain, essentially all crystallized with an inhibitor occupying the **allosteric pocket adjacent to (not overlapping) the ATP site**, a type-III binding mode with a signature H-bond to a conserved β3-lysine ([MEK1/2 inhibitor review](https://pmc.ncbi.nlm.nih.gov/articles/PMC4663016/)):
- PD0325901 → [3VVH]; TAK733 → [3PP1]; selumetinib → 4U7Z; cobimetinib → [4LMN](https://www.rcsb.org/structure/4ANB)/4ANB (GDC-0973 analogs); trametinib bound to MEK alone and to the **KSR1/KSR2 scaffold** ([7JUS](https://www.rcsb.org/structure/7JUS), [7JUR](https://www.rcsb.org/structure/7JUR), [7JV0](https://www.rcsb.org/structure/7JV0), [Nature 2020](https://www.nature.com/articles/s41586-020-2760-4)). Notably, trametinib is unique among approved MEK inhibitors in directly contacting KSR — worth checking whether your hit does the same, since that changes the cellular pharmacology (KSR-dependent potency).
- AlphaFold (Q02750/P36507): the kinase domain (68–361) is predicted at very-high confidence; the N-terminal autoinhibitory helix and, especially, the proline-rich linker (~270–326) and extreme C-terminus are lower-confidence/likely disordered — consistent with these being the least-resolved regions in the crystal structures too. (I couldn't pull the live pLDDT plot — the AlphaFold DB page is JS-rendered — so confirm exact per-residue scores at alphafold.ebi.ac.uk/entry/Q02750 if this matters for your modeling.)

### 5. CRISPR essentiality (DepMap)
I couldn't scrape live Chronos scores (DepMap's portal requires an authenticated JS session), so this is the qualitative pattern from the Broad/Sanger Achilles literature and Open Targets' essentiality documentation — **confirm exact per-lineage numbers directly at [depmap.org/portal/gene/MAP2K1](https://depmap.org/portal/gene/MAP2K1) before making a go/no-go call**:
- **MAP2K1/MEK1** trends toward **common-essential** across the cell line panel, with the strongest dependency in BRAF/NRAS-mutant melanoma, papillary thyroid, and colorectal lines — i.e., dependency is enriched exactly where the oncogenic MAPK-pathway mutations described above occur.
- **MAP2K2/MEK2** is largely **not** broadly essential — most lines tolerate its loss because MEK1 compensates. This mirrors mouse genetics (*Map2k1*-null is embryonic lethal, *Map2k2*-null is viable) ([DepMap methods overview](https://www.sciencedirect.com/science/article/pii/S1535610823004440), [Open Targets essentiality docs](https://platform-docs.opentargets.org/target/core-gene-essentiality)). **Practical implication:** if your hit is MEK2-selective, expect a muted single-agent phenotype in most lines due to paralog redundancy — build in MEK1 knockdown/degradation as a sensitizing arm before concluding it's inactive.

### 6. Drug sensitivity landscape
Because trametinib/selumetinib/cobimetinib/binimetinib are all approved chemical probes of this exact target, GDSC/PRISM sensitivity data give you a ready-made benchmark:
- Sensitivity to all four correlates strongly with **BRAF-mutant, NRAS-mutant, and NF1-loss** genotypes, and correlates with MAP2K1 CRISPR dependency in the same lines — this concordance is a commonly cited example of CRISPR and pharmacological data converging on the same lineages ([BRAF/NRAS-WT melanoma & NF1 sensitivity](https://pmc.ncbi.nlm.nih.gov/articles/PMC4296225/)).
- Beyond genotype, **proteomic state is more predictive than mutation status**: DUSP4 expression modulates response to both selumetinib and trametinib, and phosphoprotein signatures predict trametinib response with ~83% accuracy independent of mutation ([Cell Death Differ](https://www.nature.com/articles/s41418-018-0210-8), [Br J Cancer/DUSP4](https://www.nature.com/articles/s41416-019-0673-5)).
- **Actionable check for your hit:** profile it across a small BRAF-mut / NRAS-mut / NF1-loss / MAPK-WT panel and see if its kill pattern tracks the trametinib fingerprint. If it does, you're rediscovering known pharmacology (useful for validating the hit is genuinely on-target, but expect freedom-to-operate headaches); if it diverges (e.g., kills MAPK-WT lines or MEK-inhibitor-resistant lines), that's your differentiation angle worth chasing.

**Bottom line:** MEK1/2 is a deeply validated, structurally well-characterized, but *crowded* oncology target — the biology risk is low, the differentiation risk is high. The highest-leverage next check is whether your hit's cell-line kill pattern (BRAF/NRAS/NF1-mutant vs. WT) and MEK1-vs-MEK2 selectivity looks like the four approved drugs or diverges from them.