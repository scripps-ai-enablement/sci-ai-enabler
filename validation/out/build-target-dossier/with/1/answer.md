## MEK1/MEK2 (MAP2K1 / MAP2K2) Target Dossier

*Assumption: "MEK1/2 hit" = a compound engaging the canonical kinase targets MAP2K1 (MEK1, UniProt [Q02750](https://www.uniprot.org/uniprotkb/Q02750)) and/or MAP2K2 (MEK2, [P36507](https://www.uniprot.org/uniprotkb/P36507)). Flag if your hit is actually paralog-selective — that changes the read below substantially.*

### Mechanism & disease links
MEK1/2 are dual-specificity Ser/Thr-Tyr kinases sitting between RAF and ERK1/2 in the RAS→RAF→MEK→ERK cascade. RAF (BRAF/RAF1) phosphorylates the activation-loop serines (MEK1 Ser218/Ser222; MEK2 Ser222/Ser226), and active MEK then phosphorylates ERK1/2 to drive proliferation and survival signaling. MEK also allosterically controls BRAF activation via KSR scaffolds — the pathway is a feedback loop, not a one-way relay ([UniProt Q02750](https://rest.uniprot.org/uniprotkb/Q02750.txt), [P36507](https://rest.uniprot.org/uniprotkb/P36507.txt)).

- **Germline (RASopathies):** MAP2K1 variants → Cardiofaciocutaneous syndrome 3; MAP2K2 variants → CFC4. Developmental disorders, not oncology indications.
- **Somatic cancer drivers:** MAP2K1/2 mutations in ~8% of melanomas (often BRAF/NRAS-independent, and some confer MEK-inhibitor resistance), ~50% of BRAF-WT Langerhans cell histiocytosis, papillary thyroid cancer, colorectal cancer, lung adenocarcinoma, and low-grade serous ovarian cancer ([Nature Genetics melanoma exome study](https://www.nature.com/articles/ng.1026); [PTC/CRC study](https://pmc.ncbi.nlm.nih.gov/articles/PMC8144646/); [LCH study](https://ashpublications.org/blood/article/124/10/1655/32977/High-prevalence-of-somatic-MAP2K1-mutations-in)).
- **Validated clinical target:** four approved MEK inhibitors already exist (trametinib, cobimetinib, binimetinib — combined with BRAF inhibitors in BRAF V600 melanoma/NSCLC; selumetinib in NF1 plexiform neurofibroma), so mechanism-of-action risk is low but the space is competitive/crowded.

### Domains & PTMs
| | MEK1 (Q02750) | MEK2 (P36507) |
|---|---|---|
| Kinase domain | 68–361 | 72–369 |
| ATP-binding / active site | — | 78–86, 101 (ATP); 194 (catalytic base) |
| Key activating phospho-sites | Ser218, Ser222 (RAF) | Ser222, Ser226 (RAF) |
| Feedback/other phospho-sites | Thr292 (ERK2, dephosphorylates activators), Ser298 (PAK), Thr286 | Ser23, Ser293/295/306, Thr394/396 |
| Notable non-canonical PTM | Acetylation by *Yersinia* YopJ (blocks activation — infection biology, not typically drug-relevant) | Same YopJ acetylation on Ser222/226 |

Source: UniProt feature tables ([Q02750](https://rest.uniprot.org/uniprotkb/Q02750.txt), [P36507](https://rest.uniprot.org/uniprotkb/P36507.txt)).

### Subcellular localization
Predominantly **cytoplasmic**, with a peripheral-membrane pool (MEK2's membrane association is reportedly KSR1-dependent). MEK1 additionally shows dynamic mitotic localization — centrosome/spindle pole at prometaphase, midzone at anaphase, midbody at telophase — consistent with a described non-canonical role in cell division, not just MAPK signaling. Relevant if your assay reads out nuclear ERK translocation rather than total pathway activity.

### Structural confidence (AlphaFold)
- **MEK1** AF-Q02750-F1: global pLDDT **83.3** (61% very-high, 20% confident, 19% low/very-low).
- **MEK2** AF-P36507-F1: global pLDDT **81.6** (63% very-high, 15% confident, 22% low/very-low).
Both models are high-confidence overall — good enough for docking/SBDD on the kinase domain core. The low-confidence fraction (~15-22%) is consistent with flexible termini/loops rather than the ATP pocket itself, but I did not pull per-residue pLDDT to confirm exactly which residues fall below 70; verify that directly in the AlphaFold PAE viewer before trusting any pocket-adjacent loop conformation ([AF-Q02750](https://alphafold.ebi.ac.uk/entry/Q02750), [AF-P36507](https://alphafold.ebi.ac.uk/entry/P36507)). Numerous experimental PDB structures also exist for MEK1 (e.g., with trametinib/selumetinib bound) — worth using those over the AF model for any pocket-level SBDD work.

### CRISPR essentiality (DepMap) — the important nuance
This is the finding most likely to matter for your prioritization call: **in standard genome-wide single-gene CRISPR KO screens, neither MEK1 nor MEK2 scores as essential individually** in most DepMap cell lines. That looks like a red flag against the target, but it's a paralog-redundancy artifact, not a biology-doesn't-matter result — a paired-guide (pgPEN) paralog screen showed a strong **MEK1/MEK2 synthetic-lethal interaction**: only the double knockout kills cells, explaining why single-gene DepMap Chronos scores understate a target that's clearly druggable (four approved drugs) ([paralog synthetic lethality study, PMC8534300](https://pmc.ncbi.nlm.nih.gov/articles/PMC8534300/)). 

Practical implication: if you're scoring your hit against public single-gene DepMap dependency data, expect it to look weak/non-essential — that's expected for this target class and doesn't argue against the mechanism. (I could not query live DepMap portal Chronos scores directly — it sits behind an interactive login wall — so treat the "not essential individually" claim as literature-derived rather than a fresh portal pull.)

### Drug sensitivity (GDSC/PRISM)
- Existing MEK inhibitors (CI-1040, PD0325901, selumetinib, refametinib, trametinib) show genotype-stratified sensitivity in GDSC: **BRAF-mutant > NRAS-mutant > KRAS-mutant** lines by mean IC50, i.e., sensitivity tracks how directly RAF drives MEK in that genetic background ([GDSC MEK-inhibitor genotype study](https://www.sciencedirect.com/science/article/pii/S1535610814001202)).
- Cross-inhibitor expression biomarkers: **SPRY2** was the most recurrently selected predictive feature across six different MEK1/2 inhibitors in GDSC; **DUSP4** suppression also tracks response in melanoma. Both are ERK-pathway negative-feedback genes, so they're mechanistically sensible response markers to check in your own cell panel ([SPRY2/DUSP4 biomarker papers](https://www.nature.com/articles/s41416-019-0673-5)).
- PRISM (fixed 2.5 µM screen) corroborates immune/cell-cycle-linked response signatures but is coarser than GDSC dose-response for this class.

### Bottom line for the go/no-go call
Mechanism and disease rationale are solid and clinically de-risked (approved drugs exist), structural confidence is good enough for structure-based work, and genotype-driven sensitivity patterns (BRAF/RAS mutation status, SPRY2/DUSP4) give you a real hypothesis to test against your hit's selectivity data. The one thing to actively check before investing further: **whether your hit engages both MEK1 and MEK2** — given the redundancy, a paralog-selective compound may underperform in cells relative to its biochemical potency, and that's the single biggest reason on-target biology could disappoint despite a clean enzymatic IC50.