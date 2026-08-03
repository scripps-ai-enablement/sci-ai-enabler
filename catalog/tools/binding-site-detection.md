---
title: Binding Site Detection (bioSkills)
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: GPTomics bioSkills
availability: GA
tool_categories: [Drug Repurposing and Discovery, Integrative Structural and Computational Biology]
last_verified: 2026-08-01
summary: "Find and rank druggable pockets on an apo protein with fpocket, P2Rank, CASTp and DoGSiteScorer — including cryptic pockets over an MD ensemble"
verification: works
verified_on: 2026-08-03
reviewed_on: 2026-08-03
security: cleared
security_on: 2026-08-03
security_note: "GPTomics/bioSkills root LICENSE confirmed MIT this run, not archived, 1.1k stars, skill dir current"
---

# Binding Site Detection (bioSkills)

A Claude Code skill that detects putative ligand-binding pockets de novo on a structure with no bound ligand, and ranks them by druggability or ligandability score.

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | [GPTomics bioSkills](https://github.com/GPTomics/bioSkills) (community OSS, MIT) |
| **Availability** | GA — part of the bioSkills collection |
| **Pricing** | Free / OSS (MIT) — fpocket, P2Rank and mdpocket are separately installed OSS; CASTp and DoGSiteScorer are free academic web services |
| **Capabilities** | Read/Write — Claude runs the skill's workflow locally (Bash/Python) and can call the two web servers, not as an MCP tool |
| **Verified** | works · 2026-08-03 |
| **Security** | cleared · 2026-08-03 — GPTomics/bioSkills MIT confirmed, provenance matches, no advisories |

## How to install

bioSkills is **not** an npm package — skills are plain markdown/code read directly by the agent. Clone the repo, then either run the installer for the whole category or copy the single skill directory.

- **Claude Code** — clone and install via the bundled script:
  ```
  git clone https://github.com/GPTomics/bioSkills
  cd bioSkills
  ./install-claude.sh --categories "structural-biology"
  ```
  The installer copies matching skills into `~/.claude/skills/` (default target). Use `./install-claude.sh --list` to preview the skills first.
- **Claude Code / other agents** — copy just this one skill:
  ```
  cp -r bioSkills/structural-biology/binding-site-detection ~/.claude/skills/
  ```
  (run from inside your clone — the previous step left you in `bioSkills/`; otherwise replace `bioSkills/` with the absolute path of your clone). Install fpocket and, if you want ML ranking, P2Rank when prompted on first use.

## What it does

Enumerates surface concavities, then scores them — and is explicit that the two steps answer different questions:

- **Enumeration** — geometric cavity detection with fpocket (Voronoi alpha-spheres) or CASTp (analytic surface topology, area and volume).
- **Ranking** — machine-learned ligandability with P2Rank (surface-point clustering) or DoGSiteScorer (difference-of-Gaussians features plus an SVM druggability model, via the ProteinsPlus server).
- **Interpretation discipline** — a geometric cavity is a hypothesis, not automatically a functional or druggable site: it may be a crystal-additive cleft or a non-functional groove. Druggability scores were trained on *holo* sets, so they systematically under-detect apo, shallow and cryptic pockets.
- **Cryptic and transient pockets** — `mdpocket` tracks pocket occurrence and persistence across an MD trajectory or conformational ensemble, which is the route to sites that are closed in the deposited structure.
- **Predicted models** — warns that pocket-lining side-chain rotamers are among the least reliable atoms in an AlphaFold/ESMFold model, so detection on a predicted structure needs extra scepticism.
- **Components** — fpocket 4.1+ (primary), P2Rank 2.4+, CASTp and DoGSiteScorer (web), mdpocket, Biopython 1.83+, NumPy 1.26+.

**Primary use cases**: apo-structure pocket discovery for a new target, choosing a docking box, cryptic-pocket hunting over an MD ensemble.

## Notes

Distributed as a `SKILL.md` (plus reference material) in the bioSkills collection — Claude executes the workflow locally rather than as an MCP server. The upstream skill front-matter name is `bio-structural-biology-binding-site-detection`; if invoked as a namespaced plugin command it resolves under the bioSkills plugin, not as a bare `/binding-site-detection`. `tool_type` upstream is `mixed`: fpocket, P2Rank and mdpocket run locally, while CASTp and DoGSiteScorer are submitted to external academic web servers — check your data-sharing policy before sending an unpublished structure to either. Sits upstream of the catalogued docking entries [AutoDock Vina](autodock-vina-docking.html), [smina](smina-molecular-docking.html) and [DiffDock](diffdock.html), and downstream of [Structure Preparation](structure-preparation.html); the mdpocket route needs a trajectory from [GROMACS MCP Server](gromacs-mcp.html) or [OpenMM MCP Server](openmm-mcp.html). Upstream directory: `structural-biology/binding-site-detection`.

## Sources

- [`GPTomics/bioSkills`](https://github.com/GPTomics/bioSkills)
- [`structural-biology/binding-site-detection/SKILL.md`](https://github.com/GPTomics/bioSkills/blob/main/structural-biology/binding-site-detection/SKILL.md)
- [fpocket](https://github.com/Discngine/fpocket)
- [P2Rank](https://github.com/rdk/p2rank)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=binding-site-detection&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fbinding-site-detection.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
