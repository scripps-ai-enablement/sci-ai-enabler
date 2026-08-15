---
title: Look up the curated composition and stoichiometry of a protein complex
parent: All recipes
grand_parent: Recipes
nav_order: 16
problem_class: Knowledge synthesis
subject_areas: [Integrative Structural and Computational Biology, Molecular and Cellular Biology]
evidence_level: Proposed
complexity: Claude Code alone
availability: Fully open
compute_requirements: Laptop
last_verified: 2026-08-15
summary: Have Claude Code script the Complex Portal release files so a gene or UniProt accession returns curated subunits, stoichiometry, and an evidence class.
---

# Look up the curated composition and stoichiometry of a protein complex

Turn a gene name or UniProt accession into a table of the curated complexes it belongs to, with per-subunit stoichiometry and an explicit label for whether the entry was determined experimentally or inferred.

| | |
|---|---|
| **Problem class** | Knowledge synthesis |
| **Subject areas** | Integrative Structural and Computational Biology, Molecular and Cellular Biology |
| **Evidence level** | Proposed |
| **Complexity** | Claude Code alone |
| **Availability** | Fully open |
| **Compute** | Laptop |

## Problem

You are deciding which subunits to co-express before a pulldown, choosing what to put in a co-folding job, or trying to work out whether a protein pair you found in a crystal lattice is a real assembly. In every case the question is the same: *is this a known complex, which subunits does it contain, and in what ratio?* Getting it wrong is expensive — a co-expression construct missing an obligate partner produces aggregate, and a co-folding job given the wrong stoichiometry produces a confident model of something that does not exist.

The usual sources answer a different question. A PPI network gives you binary edges inferred from pulldowns and two-hybrid screens; it will happily connect twelve proteins that never occupy the same particle. A PDB entry gives you the assembly that crystallized, which is a construct, not the physiological complex. The Complex Portal is the resource that answers this question directly — manually curated stable complexes with composition, stoichiometry, topology, and complex-specific GO terms, with stable versioned identifiers. But two of its properties trip up casual use: a large fraction of entries are **not** backed by direct experimental evidence for that species, and the human download ships a *predicted* file alongside the curated one that is the same size. Solved looks like a committed script that resolves an accession to complexes, carries the evidence class into every output row, and never silently mixes the two files.

## Recommended approach

Complex Portal and IntAct are catalogued as [Claude Science connectors](../../catalog/tools/complex-portal.html) for interactive lookup, and that is the right route for one question you will not re-run. For anything that feeds a construct design or a co-folding run, have Claude Code build the artifact against the CC0 release files instead.

1. **Pull one release into `data/` and record it.** The ComplexTAB files are per-species, named by NCBI taxon ID, under [`ftp.ebi.ac.uk/pub/databases/intact/complex/current/complextab/`](https://ftp.ebi.ac.uk/pub/databases/intact/complex/current/complextab/) — `9606.tsv` (human), `10090.tsv` (mouse), `559292.tsv` (*S. cerevisiae*), `83333.tsv` (*E. coli* K-12), `7227.tsv`, `6239.tsv`, `3702.tsv`, `2697049.tsv` (SARS-CoV-2), and about twenty more. Download only the species you need, then write each file's sha256 and its FTP Last-Modified date into `provenance.json`. There is no version number on the directory, so **the date is the release identifier** — the current set is dated 2026-01-14.

   ```
   Download 9606.tsv from
   https://ftp.ebi.ac.uk/pub/databases/intact/complex/current/complextab/
   into data/. Do NOT download 9606_predicted.tsv. Record the sha256 and the
   Last-Modified header of every file in provenance.json.
   ```

2. **Refuse the predicted file unless it is asked for explicitly.** `9606_predicted.tsv` sits next to `9606.tsv` and is comparable in size (both ~5.0 MB), so a glob over `*.tsv` doubles your human hit count with entries that are not manually curated. Have the script take an explicit `--include-predicted` flag, default it off, and stamp a `curation_set` column of `curated` or `predicted` on every row so the two can never be merged by accident downstream.

3. **Parse composition and stoichiometry out of one column.** The `Identifiers (and stoichiometry) of molecules in complex` field is pipe-separated accessions with a parenthesised count — for `CPX-4111` (sheep collagen type I trimer) it reads `Q9MZW3(2)|W5NTT7(1)`. Explode it to one row per subunit with an integer copy number. Participants are not all UniProt accessions: the field also carries ChEBI IDs for small molecules, RNA Central IDs, and nested `CPX-` identifiers where a complex is a subunit of a larger one. Route each prefix explicitly and **fail on an unrecognised one** rather than dropping it — a silently discarded ChEBI cofactor turns an obligate holoenzyme into an apoprotein in your output.

4. **Carry the evidence code, and treat it as the headline field.** The `Evidence Code` column is an ECO term with its label inline. `CPX-4111` above is `ECO:0005547` — *biological system reconstruction evidence based on inference from background scientific knowledge used in manual assertion* — and its `Experimental evidence` column is `-`. That is a curator's reasoned assertion, not a measurement, and it is a perfectly good basis for a hypothesis and a bad basis for a claim in a figure legend. Emit the raw ECO ID, its label, and a derived two-value `evidence_class` of `experimental` or `inferred`, and make the script require the ECO ID to be present. Complex Portal has used the Evidence Code Ontology to separate direct experimental support from homology- and orthology-based inference since its first release ([Meldal et al. 2015](https://doi.org/10.1093/nar/gku975)).

5. **Cross-check stoichiometry against the assembly statement.** The `Complex assembly` column is an independent, human-readable claim about the topology — `Heterotrimer` for `CPX-4111`. Have the script compare it against the copy numbers it parsed in step 3 and write a `stoichiometry_agrees` boolean. Disagreement is not necessarily an error, but it is the signal that the entry's stoichiometry is partial and you should read the entry rather than trust the table.

6. **Resolve the structural and functional links you will actually use.** The `Cross references` column carries typed references — wwPDB, EMDB, Reactome, MatrixDB, and `pubmed:...(see-also)` — and `Go Annotations` carries complex-specific GO terms. Split them on type into `xrefs.csv` so a downstream co-folding or docking step can pick up a PDB entry without re-parsing. Keep the `Complex ac` version suffix if present: Complex Portal identifiers are stable **and versioned** ([Meldal et al. 2019](https://doi.org/10.1093/nar/gky1001)), so an unversioned `CPX-` string in a methods section is under-specified.

7. **Emit, and handle the negative result honestly.** Commit `complex_lookup.py`, `data/` (or its checksums), `complexes.csv`, `subunits.csv`, `xrefs.csv`, and `provenance.json`. Absence from the Complex Portal is **not** evidence that no complex exists — curation is deliberately incomplete outside the finished yeast and *E. coli* complexomes — so have the script emit an explicit `no curated complex found` row rather than an empty file, and go to IntAct (below) for the pairwise-evidence question when it does.

The script is stdlib-only — `urllib` and `csv` are enough — so there is no environment to pin beyond the Python version, which belongs in `provenance.json` alongside the release date and the model identity that authored the script. The Complex Portal grows continuously, so a re-run months later will differ; the recorded date and checksums are what make that visible instead of silent.

## Why this assembly

Rung 1. The work is "download one tab-separated file per species and apply four documented conventions", which is what Claude Code does natively — no Skill, no MCP server, no dependency. Rung 2 would mean the Claude Science *Structures & Interactions* connector, which is genuinely the better tool for a single conversational question but has no separately addressable MCP URL and cannot leave a re-runnable script behind; it also puts the predicted-file and evidence-code gates back inside a conversation where they are easy to skip. Escalating further buys nothing: there is no search, no model, and no optimization here. The hard part is refusing three defaults — glob the directory, trust the row, treat absence as absence — and a script is a better place to encode a refusal than a prompt.

## Availability

Fully open. Complex Portal data has been CC0 since the 2022 release ([Meldal et al. 2022](https://doi.org/10.1093/nar/gkab991)), downloadable from the EMBL-EBI FTP with no account, no key, and no rate limit worth planning around. IntAct is CC BY 4.0. Nothing about your query leaves your machine once the files are downloaded, so an unpublished target list is safe here — in deliberate contrast to the connector route, which sends the gene name to a hosted service. If you take the interactive route instead, that needs a Claude.ai plan with Claude Science access and the *Structures & Interactions* connector enabled.

## Compute requirements

Laptop. The largest curated species file is human at 5.0 MB; mouse is 1.4 MB and yeast 872 KB, and most of the other twenty-odd species are under 100 KB. The whole complextab set is well under 20 MB, the download is the slow step, and every operation in this recipe is a dictionary lookup or a string split. Runtime is a couple of seconds and RAM stays under 500 MB. No GPU, no network access after step 1.

## Evidence

Proposed. No documented attempt at an LLM-scripted Complex Portal lookup is known. The grounding is resource-level and strong: the Complex Portal is manually curated by the IntAct team at EMBL-EBI, provides stable versioned identifiers and standards-compliant downloads across ~20 species ([Meldal et al. 2019](https://doi.org/10.1093/nar/gky1001)), and by the 2022 release held over 1100 human complexes plus a first-draft *E. coli* complexome ([Meldal et al. 2022](https://doi.org/10.1093/nar/gkab991)).

Each gate above traces to a stated property verified this run, not to a heuristic. The evidence-code gate is the resource's own design — the Evidence Code Ontology has been used since 2015 specifically to mark whether an entry has direct experimental support or was inferred from homology or orthology ([Meldal et al. 2015](https://doi.org/10.1093/nar/gku975)) — and the worked `CPX-4111` example above is a real curated entry whose evidence is an inference with a blank experimental-evidence column. The predicted-file gate comes from the directory listing itself. The value of the curated-composition question over inferred edges has a quantitative demonstration in the yeast complexome analysis: curating it produced a **50% increase in curated complexes over the previous CYC2008 reference set**, and only about **40% of expanded co-complex pairs also have genetic interactions** ([Meldal et al. 2021](https://doi.org/10.1093/nar/gkab077)) — i.e. co-membership and interaction evidence are substantially non-overlapping, which is exactly why a PPI network is the wrong place to ask this.

The closest documented analogous workflow is the Complex Portal's own use as the reference set against which large-scale complexome experiments are scored (ibid.) — the same joins, driven by hand rather than by an agent.

## Alternatives considered

- **The Claude Science connector, interactively.** Reach for [Complex Portal](../../catalog/tools/complex-portal.html) and [IntAct](../../catalog/tools/intact.html) as connectors when you have one question and will not re-run it. You lose the artifact and must apply the evidence-code and predicted-set gates yourself in the prompt.
- **IntAct, when Complex Portal comes back empty.** [IntAct](../../catalog/tools/intact.html) holds curated *pairwise* molecular-interaction records with experimental evidence, reachable at [`ebi.ac.uk/intact/ws`](https://www.ebi.ac.uk/intact/ws). It answers a weaker question — "has anyone observed these two molecules interacting" — with no stoichiometry and no assertion that the pair sits in one particle. Use it to avoid concluding "no complex" from a curation gap, not as a substitute for composition.
- **Infer the complex from a PPI network instead.** [build-ppi-network-and-rank-hub-genes](build-ppi-network-and-rank-hub-genes.html) gets you edges and hub ranks across the whole interactome, which is the right tool when your question is topological. It cannot tell you copy number, and its densely connected neighbourhoods are not complexes.
- **Read the stoichiometry off a structure.** If a PDB entry for the assembly exists, [vet-a-pdb-structure-before-reusing-it](vet-a-pdb-structure-before-reusing-it.html) will tell you whether its biological assembly is trustworthy. That is the stronger evidence when it exists — but it is a construct in a crystal, so check it against the curated entry rather than instead of it.

## See also

- [Complex Portal (Claude Science Connector)](../../catalog/tools/complex-portal.html)
- [IntAct (Claude Science Connector)](../../catalog/tools/intact.html)
- [Characterize a protein–protein interface](characterize-a-protein-protein-interface.html) — the downstream consumer; its biological-vs-packing verdict cites curated complex membership as orthogonal evidence.
- [Predict a protein–protein complex interface](predict-protein-protein-complex-interface.html) — co-folding, which needs the subunit list and stoichiometry this recipe produces.
- [Build a PPI network and rank hub genes](build-ppi-network-and-rank-hub-genes.html) — inferred edges, as opposed to curated membership.
- [Reproducible, provenance-tracked AI analysis](../../guide/advanced/reproducibility.md) — the artifact pattern this recipe follows.

## Sources

- [Complex Portal ComplexTAB release directory, `ftp.ebi.ac.uk/pub/databases/intact/complex/current/complextab/`](https://ftp.ebi.ac.uk/pub/databases/intact/complex/current/complextab/) — files dated 2026-01-14; fetched 2026-08-15 (this run). Species file inventory, sizes, and the `9606_predicted.tsv` companion file.
- [ComplexTAB `9606`-format example, `9940.tsv`](https://ftp.ebi.ac.uk/pub/databases/intact/complex/current/complextab/9940.tsv) — fetched 2026-08-15 (this run). Exact 19-column header and the `CPX-4111` worked row quoted above.
- [Meldal et al., "Complex Portal 2022: new curation frontiers," *NAR* 50:D578](https://doi.org/10.1093/nar/gkab991) — published 2022-01-01; CC0 licence change, >1100 human complexes, draft *E. coli* complexome.
- [Meldal et al., "Complex Portal 2018," *NAR* 47:D550](https://doi.org/10.1093/nar/gky1001) — published 2019-01-01; stable versioned identifiers, ~20 species, ComplexTAB and REST API.
- [Meldal et al., "Analysing the yeast complexome," *NAR* 49:3156](https://doi.org/10.1093/nar/gkab077) — published 2021-01-01; 50% increase over CYC2008, 40% co-complex/genetic-interaction overlap.
- [Meldal et al., "The Complex Portal — an encyclopaedia of macromolecular complexes," *NAR* 43:D479](https://doi.org/10.1093/nar/gku975) — published 2015-01-01; Evidence Code Ontology use, stoichiometry and topology capture, small-molecule and nucleic-acid participants.
- [Complex Portal (Claude Science Connector) catalog entry](../../catalog/tools/complex-portal.html) — catalog `last_verified` 2026-07-17.
- [IntAct (Claude Science Connector) catalog entry](../../catalog/tools/intact.html) — catalog `last_verified` 2026-07-17.

---

## Tried this recipe?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=recipe-feedback.yml&recipe=look-up-curated-complex-composition&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Frecipes%2Fitems%2Flook-up-curated-complex-composition.html%0A%0A) — what worked, what didn't, what you'd change. The form opens with this recipe pre-selected and a link back to this page.
