## MEK1/2 (MAP2K1/MAP2K2) Target Dossier

**Scope assumption:** treating human **MAP2K1** (UniProt [Q02750](https://www.uniprot.org/uniprotkb/Q02750), Ensembl ENSG00000169032) as the primary paralog, with **MAP2K2/MEK2** (P36507, ~80% kinase-domain identity) noted where it diverges — this matches how the field and most databases (DepMap, GDSC) treat the pair, since essentially all clinical MEK inhibitors hit both.

*Method note: this maps onto a curated recipe in my tool index ("build a target dossier from gene → structure → cancer dependency": Open Targets + UniProt + AlphaFold + DepMap). Its hosted Open Targets MCP connector currently fails its handshake, so I pulled the underlying public databases directly (UniProt REST, AlphaFold DB, literature/DepMap search) rather than routing through that connector.*

---

### 1. Disease links & mechanism
MEK1/2 sit immediately downstream of RAF and upstream of ERK1/2 in the RAS→RAF→MEK→ERK (MAPK) cascade — RAF phosphorylates the MEK1 activation loop at **Ser218/Ser222**, activating it as the sole known physiological ERK1/2 kinase.
- **Somatic cancer driver:** MAP2K1/2 activating mutations occur in ~8% of melanomas (often co-occurring with or independent of BRAF/NRAS), ~0.6% of lung adenocarcinoma, and ~1–2% of colorectal cancers; hotspots cluster in the negative-regulatory helix A, αC-β4 loop, and β7–β8 loop. ([AACR MCT](https://aacrjournals.org/mct/article/22/2/227/716261/High-Throughput-Functional-Evaluation-of-MAP2K1); [Clin Cancer Res](https://aacrjournals.org/clincancerres/article/21/8/1935/79015/MAP2K1-MEK1-Mutations-Define-a-Distinct-Subset-of); [PMC8144646](https://pmc.ncbi.nlm.nih.gov/articles/PMC8144646/))
- MAP2K1-mutant colorectal tumors specifically predict **poor response to anti-EGFR therapy** and to vertical MAPK-pathway blockade. ([PubMed 33436306](https://pubmed.ncbi.nlm.nih.gov/33436306/))
- **Germline RASopathy:** heterozygous gain-of-function MAP2K1/MAP2K2 mutations cause ~25% of cardiofacio­cutaneous syndrome (BRAF accounts for ~75%, KRAS <2%) — craniofacial dysmorphism, congenital heart defects, short stature. ([Frontiers Pediatrics](https://www.frontiersin.org/journals/pediatrics/articles/10.3389/fped.2022.990111/full); [PMC9614356](https://pmc.ncbi.nlm.nih.gov/articles/PMC9614356/))

### 2. Domains & PTMs (UniProt Q02750)
- 393 aa; **protein kinase domain spans residues 68–361** (PROSITE rule).
- N-terminal region contains the negative-regulatory/docking region controlling RAF and ERK binding.
- Key regulatory phosphosites:
  - **Ser218 / Ser222** — activation-loop sites phosphorylated by BRAF/RAF1; this is *the* activating event.
  - **Thr292** — phosphorylated by MAPK1 (ERK), a negative-feedback site.
  - **Ser298** — phosphorylated by PAK.
  - Thr286 — phosphothreonine identified by MS (regulatory role less defined).
- Notable non-canonical PTM: the *Yersinia* effector **YopJ acetylates MEK1**, blocking phosphorylation/activation — a well-studied bacterial immune-evasion mechanism, useful context if off-target immunomodulatory effects matter. (UniProt Q02750)

### 3. Subcellular localization
Predominantly **cytoplasmic** at steady state, with nuclear, membrane, and centrosome/spindle-pole (mitotic) pools (UniProt). Cytoplasmic retention is driven by a **leucine-rich nuclear export signal at residues ~32–44** in the N-terminal domain — deleting it redirects MEK1 to the nucleus. MEK1 also actively **escorts phosphorylated ERK out of the nucleus**, making its NES mechanistically important for shutting off nuclear MAPK signaling, not just for MEK's own localization. ([Fukuda et al., JBC](https://www.jbc.org/article/S0021-9258(18)98294-3/fulltext); [PNAS](https://www.pnas.org/doi/10.1073/pnas.94.8.3742))

### 4. Structural confidence & inhibitor-bound structures
- **AlphaFold model AF-Q02750-F1:** global pLDDT 83.25 — 61.3% of residues "Very High" confidence, 19.6% "Confident," ~19% Low/Very Low. The kinase domain (68–361) sits well within the high-confidence core; the low-confidence tails correspond to the flexible N-terminal NES/docking region and disordered C-terminus — treat those regions as poorly modeled for any docking/design work. (AlphaFold DB API)
- Multiple experimental structures exist with clinical MEK inhibitors bound, several via the **KSR scaffold** rather than MEK alone:
  - **7JUR / 7JUX** — KSR2:MEK1 and KSR1:MEK1 with trametinib (reveals trametinib partly acts through the KSR-MEK interface, not classical MEK-alone allostery).
  - **7JUS** — KSR2:MEK1 with cobimetinib; **7JV0** — KSR1:MEK1 with PD0325901.
  - **4ANB** — MEK1 with the cobimetinib-related carboxamide series (GDC-0973/XL518 analogs).
  - Foundational binary/ternary MEK1–nucleotide–inhibitor structures (Ohren et al.) established the classic **allosteric, non-ATP-competitive pocket** adjacent to the ATP site that essentially all approved MEK inhibitors exploit. ([RCSB 7JUR](https://www.rcsb.org/structure/7JUR); [RCSB 4ANB](https://www.rcsb.org/structure/4ANB); [PMC7746607](https://pmc.ncbi.nlm.nih.gov/articles/PMC7746607/))

### 5. CRISPR essentiality (DepMap)
- MAP2K1 is a **context-selective, not pan-essential**, dependency: strongest in **BRAF-V600E melanoma lines** (a repeatedly reported conditional dependency alongside MAPK1/MITF) and more broadly across **RAS/RAF-pathway-activated lineages**, where MAPK-pathway genes (EGFR, ERBB2, BRAF, MAP2K1, ERBB4) show among the most predictive dependency signal of any pathway module. ([DepMap pan-cancer map, ScienceDirect](https://www.sciencedirect.com/science/article/pii/S1535610823004440); [bioRxiv 2020.07.13.184697](https://www.biorxiv.org/content/10.1101/2020.07.13.184697v1.full))
- **Gap flagged:** I did not pull live per-line Chronos gene-effect numbers or a lineage-ranked dependency chart — the DepMap portal (`depmap.org/portal/gene/MAP2K1`) gives exact current scores and is worth a direct pull before finalizing; I'm not fabricating specific score values here.

### 6. Drug sensitivity & resistance
Approved/clinical MEK1/2 inhibitors: **trametinib, cobimetinib, binimetinib, selumetinib** — all allosteric, ATP-noncompetitive. Sensitivity patterns from GDSC/CTD2-type screens and clinical data:
- Best activity in **BRAF-V600E-mutant** contexts (trametinib, cobimetinib); **binimetinib** shows relatively more activity in **NRAS-mutant** melanoma.
- MEK-inhibitor **monotherapy has minimal activity in BRAF-mutant tumors** generally (used clinically in combination with BRAF inhibitors instead).
- **Resistance mechanisms:** BRAF or KRAS gene amplification is a recurrent acquired-resistance route in colorectal and melanoma models; BRAF-amplification-driven resistance is reversible on drug withdrawal, whereas KRAS-amplification-driven resistance instead drives an EMT/chemoresistant state that does *not* revert. ([Nat Commun 2019](https://www.nature.com/articles/s41467-019-09438-w); [PMC6684215](https://pmc.ncbi.nlm.nih.gov/articles/PMC6684215/))
- **Gap flagged:** I did not pull quantitative GDSC/CTRP IC50 tables — worth pulling directly from the GDSC portal or ChEMBL if you need exact potency/AUC numbers for a specific cell-line panel.

---

### Bottom line for go/no-go
MEK1/2 is a **mechanistically well-validated, clinically precedented node** (four approved inhibitors, strong genetic and structural rationale, well-defined allosteric pocket) — the biology risk is low. The real decision variables are: (a) whether your hit offers **differentiation** from four existing approved drugs (selectivity, resistance-mechanism coverage, e.g. targeting the BRAF/KRAS-amplification escape routes, or a KSR-interface mechanism like trametiglue), and (b) confirming your compound's cell-line sensitivity profile against the RAS/RAF-mutant-selective dependency pattern above rather than assuming pan-cancer activity. I'd pull the live DepMap Chronos scores and a GDSC/CTRP potency table for your specific lines next — those are the two gaps flagged above.