---
title: RDKit Cheminformatics Skill
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: [Chemistry]
last_verified: 2026-05-20
summary: Claude skill providing RDKit recipes for SMILES parsing, descriptors, fingerprints, substructure search, reactions, and 2D/3D molecular generation.
---

# RDKit Cheminformatics Skill

Claude skill providing Python recipes for the full RDKit cheminformatics stack — molecular I/O, descriptor calculation, fingerprinting, substructure matching, reaction handling, and 3D coordinate generation.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [K-Dense Inc.](https://github.com/K-Dense-AI/scientific-agent-skills) (community OSS) |
| **Availability** | GA — actively maintained 2025–2026 |
| **Pricing** | Free / OSS (BSD-3-Clause skill; MIT repo) |
| **Capabilities** | Read/Write — Claude executes RDKit via the Bash/Python tool |

## How to install

```
git clone https://github.com/K-Dense-AI/scientific-agent-skills
cp -r scientific-agent-skills/scientific-skills/rdkit ~/.claude/skills/
pip install rdkit
```

Project-scoped alternative: copy into `.claude/skills/` instead of `~/.claude/skills/`.

## What it does

`SKILL.md` with recipes for:

- SMILES / SDF / MOL parsing and standardization
- Descriptors (MW, LogP, TPSA) and Lipinski rules
- Morgan / RDKit / MACCS fingerprints and similarity
- Substructure matching and SMARTS queries
- 2D depiction and 3D embedding (ETKDG)
- Reaction templates and enumeration

**Primary use cases**: SMILES parsing and standardization for ML pipelines, descriptor calculation, substructure / similarity search, reaction enumeration.

## Notes

Skill is documentation plus Python recipes — Claude executes RDKit locally via Bash/Python. Sibling skills in the same repo (`datamol`, `molfeat`, `medchem`, `deepchem`) cover higher-level workflows.

## Sources

- [`K-Dense-AI/scientific-agent-skills`](https://github.com/K-Dense-AI/scientific-agent-skills)
- [`scientific-skills/rdkit/SKILL.md`](https://github.com/K-Dense-AI/scientific-agent-skills/blob/main/scientific-skills/rdkit/SKILL.md)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=rdkit-skill&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Frdkit-skill.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
