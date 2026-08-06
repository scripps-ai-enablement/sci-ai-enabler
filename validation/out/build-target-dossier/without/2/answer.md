## MEK1/2 (MAP2K1/MAP2K2) — Target Dossier

*Assumption: "MEK1/2" = MAP2K1 (UniProt Q02750) as primary, with paralog MAP2K2/MEK2 (P36507, ~80% identity, same domains/mechanism) noted where it diverges — since both are the physiological RAF-MEK-ERK kinases and are essentially always co-targeted.*

### Disease links & mechanism
MEK1 sits in the RAS→RAF→MEK→ERK cascade: RAF (BRAF/RAF1) phosphorylates the activation loop at **Ser218/Ser222** (MEK2: Ser222/Ser226), switching on the kinase, which then dual-phosphorylates ERK1/2's TEY motif — its only known physiological substrates [UniProt](https://www.uniprot.org/uniprotkb/Q02750/entry) [PMC4663016](https://pmc.ncbi.nlm.nih.gov/articles/PMC4663016/).

- **Somatic cancer mutations**: melanoma, lung adenocarcinoma, colorectal cancer (K57E/N/T, Q56P; ~1-2%, mutually exclusive with RAS/RAF, linked to anti-EGFR resistance) [Clin Colorectal Cancer 2020](https://www.clinical-colorectal-cancer.com/article/S1533-0028(20)30171-7/fulltext); Langerhans cell histiocytosis (~33% of BRAF-WT cases) [Blood 2014](https://ashpublications.org/blood/article/124/19/3007/33329); Erdheim-Chester disease (~20%) [case report](https://www.cancernetwork.com/view/erdheim-chester-disease-a-case-report-of-braf-v600e-negative-map2k1-positive-ecd-diagnosed-by-blood-next-generation-sequencing-assay-and-a-brief-literature-review); melorheostosis (bone disorder) [UniProt](https://www.uniprot.org/uniprotkb/Q02750/entry).
- **Germline RASopathy**: Cardiofaciocutaneous syndrome-3 (MAP2K1) / CFC4 (MAP2K2) [OMIM 615279](https://omim.org/entry/615279), [OMIM 615280](https://omim.org/entry/615280).
- **Resistance biology**: hotspots cluster in the N-terminal negative-regulatory region (F53del, Q56P, K57E/N) and catalytic core (C121S, E203K), producing constitutively active, partially RAF-independent "class II/III" mutants. **C121S** resists both BRAF and MEK inhibitors (incl. trametinib); **E203K** resists cobimetinib and anti-PD-1 but stays trametinib-sensitive [PMC9890140](https://pmc.ncbi.nlm.nih.gov/articles/PMC9890140/).

### Domains & PTMs (UniProt Q02750)
- Kinase domain: residues **68–361** (STE family, ATP-binding ~74–97, catalytic Asp190) [InterPro IPR000719](https://www.ebi.ac.uk/interpro/entry/InterPro/IPR000719/).
- Proline-rich RAF1-binding insert: **270–307**, unique to MEK1/2 among kinases.
- N-terminal negative-regulatory/MAPK-docking region with a leucine-rich **NES (~32–44)** enforcing cytoplasmic retention [Fukuda et al. 1996, JBC](https://www.jbc.org/article/S0021-9258(18)98294-3/fulltext).
- Key PTMs: activating **pSer218/pSer222** (by BRAF/RAF1); inhibitory feedback **pThr292** (by ERK2); **pSer298** (PAK); pathogen effector YopJ (*Yersinia*) acetylates/blocks Ser218/222 phosphorylation to shut the pathway down [UniProt PTM](https://www.uniprot.org/uniprotkb/Q02750/entry).

### Subcellular localization
Primarily **cytoplasmic** at steady state (NES-enforced), with regulated nuclear shuttling; also annotated at cytoskeleton/centrosome/spindle pole/midbody during mitosis [UniProt](https://www.uniprot.org/uniprotkb/Q02750/entry).

### Structural confidence
- **AlphaFold (AF-Q02750-F1)**: global pLDDT 83 — kinase domain (~68–361) is high-to-very-high confidence (catalytic core ~130–300 often >95); N-terminal regulatory region (~1–67) and C-terminal tail (~362–393) drop to low confidence (pLDDT ~25–46), i.e., disordered [alphafold.ebi.ac.uk/entry/Q02750](https://alphafold.ebi.ac.uk/entry/Q02750).
- **PDB** (~88 structures): kinase-domain-only crystal forms typically start at residue ~35–62 (e.g., 1S9J, 3EQC, 3EQH), confirming the N-terminus is disordered/truncated experimentally too. Rich allosteric-inhibitor-bound set: PD0325901 (3VVH), selumetinib (4U7Z), cobimetinib (4LMN), plus KSR1/2–MEK1 and BRAF–MEK1 co-complexes with trametinib, binimetinib, pimasertib etc. (e.g., PDB 7JV0, 7M0T–7M0Y) [RCSB](https://www.rcsb.org/structure/7JV0), [Nature 2020](https://www.nature.com/articles/s41586-020-2760-4). The allosteric pocket (adjacent to, not overlapping, ATP site) is well resolved and is the site nearly all clinical MEK inhibitors occupy.

### CRISPR essentiality & drug sensitivity (DepMap/GDSC)
- **Not pan-essential** — MAP2K1 doesn't clear DepMap's common-essential Chronos threshold (~-0.5 to -1) genome-wide. It's a **selective, genotype-defined dependency**, strongest in **BRAF-mutant** lines (cutaneous melanoma especially), per SuperDendrix analysis of DepMap CERES/Chronos data [PMC8979493](https://pmc.ncbi.nlm.nih.gov/articles/PMC8979493/) and Sanger Project Score [score.depmap.sanger.ac.uk/gene/MAP2K1](https://score.depmap.sanger.ac.uk/gene/MAP2K1).
- One preprint reports MAP2K1/MAP2K2 as a **synthetic-lethal paralog pair** in combinatorial CRISPR screens — flagging this as **unverified** (the DOI format looked non-standard for bioRxiv when checked, so treat as a lead to confirm, not an established finding).
- **Drug sensitivity** (GDSC/CTRP/PRISM, trametinib/selumetinib/PD0325901/binimetinib/cobimetinib across >1000 lines): sensitivity ranks **BRAF-mutant > NRAS-mutant > KRAS-mutant** [PMC3531057](https://pmc.ncbi.nlm.nih.gov/articles/PMC3531057/). Clinically, "RAF-regulated" (class II) MEK1 mutants stay drug-responsive; RAF-independent (class III, e.g., C121S) mutants are resistant [PMC9890140](https://pmc.ncbi.nlm.nih.gov/articles/PMC9890140/).

### Bottom line
This is a **validated, druggable, clinically precedented node** (5 approved allosteric MEK inhibitors already exist) — so differentiation, not target validation, is the open question. Its value is genotype-gated (BRAF/NRAS-mutant tumors), essentiality is selective rather than universal, structural biology is mature (well-defined allosteric pocket, N-terminal regulatory region is intrinsically disordered in both predicted and experimental structures), and known resistance mutations (C121S, E203K) are worth screening any new chemotype against early.

*Caveat: this is a single-pass literature/database pull, not exhaustive — verify hotspot frequencies and the paralog synthetic-lethality claim against current COSMIC/DepMap data before committing resources.*