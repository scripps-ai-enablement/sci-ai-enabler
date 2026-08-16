---
title: Aging and Senescence Research (ToolUniverse Claude Skill)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: Zitnik Lab (Harvard Medical School)
availability: GA
tool_categories: [Drug Repurposing and Discovery, Molecular and Cellular Biology, Translational Medicine]
last_verified: 2026-08-16
summary: ToolUniverse agent skill for geroscience — senescence markers, aging hallmarks, longevity GWAS, and senolytic target discovery with graded evidence.
---

# Aging and Senescence Research (ToolUniverse Claude Skill)

A ToolUniverse agent skill for geroscience questions: it places a gene or pathway within the aging-hallmarks framework, assembles genetic and pathway evidence, and looks for senolytic or geroprotector opportunities.

| | |
|---|---|
| **Type** | Claude Skill (one of ToolUniverse's pre-built agent skills) |
| **Supplier** | [Zitnik Lab, Harvard Medical School](https://github.com/mims-harvard/ToolUniverse) |
| **Availability** | GA — part of the ToolUniverse skills collection (`skills/tooluniverse-aging-senescence/`) |
| **Pricing** | Free / OSS (Apache-2.0); OpenGenes, GWAS Catalog, Open Targets, KEGG, STRING and PubMed are free public resources |
| **Capabilities** | Read-only — drives ToolUniverse tool calls; no data writes |

## How to install

This skill calls ToolUniverse tools, so the **ToolUniverse MCP server must be installed first** (see the [ToolUniverse](tooluniverse.html) page). Simplest registration:

```
claude mcp add --transport stdio tooluniverse -- uvx tooluniverse
```

Then add the skills:

- **Claude Code** — install the whole skill collection (the skill resolves as `tooluniverse-aging-senescence`):
  ```
  npx skills add mims-harvard/ToolUniverse
  ```
- **Manual / other agents** — copy just this skill directory into your skills folder:
  ```
  git clone https://github.com/mims-harvard/ToolUniverse
  cp -r ToolUniverse/skills/tooluniverse-aging-senescence ~/.claude/skills/
  ```
  (replace `~/.claude/skills/` with your agent's skills directory if you are not using Claude Code/Desktop.)

The skill sets `disable-model-invocation: true` upstream, so invoke it explicitly (e.g. ask Claude to "use the aging and senescence skill") rather than relying on automatic dispatch.

## What it does

Runs a seven-phase geroscience workflow:

0. **Query parsing** — classifies the question as being about an aging gene, a senescence marker, an age-related disease, or a drug, and routes accordingly.
1. **Hallmarks classification** — maps the subject onto the twelve hallmarks-of-aging framework.
2. **Genetic evidence** — `OpenGenes_get_gene` / `OpenGenes_search_genes` for curated aging-gene records with mechanism and study counts, plus `gwas_get_snps_for_gene` and `gwas_search_associations` for longevity and age-related-disease loci, and model-organism lifespan data.
3. **Pathway analysis** — `KEGG_get_pathway_genes` and `kegg_search_pathway` for senescence, autophagy, telomere and epigenetic pathways, with STRING interaction context.
4. **Senolytic / geroprotector discovery** — the drug layer, covering the established senolytics (dasatinib + quercetin, fisetin, navitoclax) and `OpenTargets_get_associated_targets_by_disease_efoId` for aggregated disease-target evidence.
5. **Literature and clinical context** — `PubMed_search_articles`.
6. **Interpretation** — an evidence-graded report that explicitly separates correlative findings from causal ones established by knockout or intervention.

Covered subject matter includes senescence markers (p16/CDKN2A, SASP, SA-β-gal), epigenetic clocks, telomere biology, longevity GWAS and centenarian genetics.

**Primary use cases**: senescence-pathway analysis, age-related disease genetics, senolytic target discovery, centenarian-genetics queries.

## Notes

It is a reasoning layer over ToolUniverse; without the MCP server registered, the tool calls fail. The correlative-versus-causal distinction is the point of the skill — a gene that merely changes expression with age is reported as such and not promoted to a target.

For the safety read on any target this surfaces, follow with [Gene Liability Evaluation](tooluniverse-gene-liability.html); for the underlying resources see [GWAS Catalog](gwas-database.html), [KEGG](kegg-database.html), [Open Targets](open-targets.html), [STRING](string-database-ppi.html) and [PubMed](pubmed.html). ToolUniverse ships ~68 such skills; other workflows are catalogued separately.

## Sources

- [`mims-harvard/ToolUniverse`](https://github.com/mims-harvard/ToolUniverse)
- [`skills/tooluniverse-aging-senescence/SKILL.md`](https://github.com/mims-harvard/ToolUniverse/blob/main/skills/tooluniverse-aging-senescence/SKILL.md)
- [OpenGenes](https://open-genes.com/)
- [ToolUniverse documentation](https://zitniklab.hms.harvard.edu/ToolUniverse/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=tooluniverse-aging-senescence&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Ftooluniverse-aging-senescence.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
