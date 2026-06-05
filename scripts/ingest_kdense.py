#!/usr/bin/env python3
"""One-time batch ingestion of K-Dense skills into the catalog.

Reads scripts/kdense_category_map.yaml (the auditable scope filter), walks a
local clone of K-Dense-AI/scientific-agent-skills, and for every in-scope skill
either CREATES a new catalog/tools/<slug>.md page or REPAIRS the install path of
an existing K-Dense page (the upstream repo migrated scientific-skills/ -> skills/
and dropped the non-existent `claude-scientific-skills` plugin marketplace in
favour of `npx skills add`).

Generated pages are schema-accurate but lean (per the plan); daily curator runs
enrich them over time.

Usage:
    python3 scripts/ingest_kdense.py --repo /tmp/kdense --dry-run
    python3 scripts/ingest_kdense.py --repo /tmp/kdense          # writes
"""
from __future__ import annotations

import argparse
import datetime as _dt
import re
import sys
from pathlib import Path

import yaml

REPO_URL = "https://github.com/K-Dense-AI/scientific-agent-skills"
SUPPLIER_LINK = f"[K-Dense Inc.]({REPO_URL}) (community OSS)"
TODAY = _dt.date.today().isoformat()

# Pretty display names for slugs that don't title-case cleanly.
PRETTY = {
    "adaptyv": "Adaptyv",
    "bgpt-paper-search": "BGPT Paper Search",
    "benchling-integration": "Benchling",
    "biopython": "BioPython",
    "bioservices": "BioServices",
    "bulk-rnaseq": "Bulk RNA-seq",
    "clinical-decision-support": "Clinical Decision Support",
    "clinical-reports": "Clinical Reports",
    "cobrapy": "COBRApy",
    "database-lookup": "Database Lookup",
    "deepchem": "DeepChem",
    "deeptools": "deepTools",
    "diffdock": "DiffDock",
    "dnanexus-integration": "DNAnexus",
    "esm": "ESM",
    "etetoolkit": "ETE Toolkit",
    "geniml": "geniml",
    "ginkgo-cloud-lab": "Ginkgo Cloud Lab",
    "gtars": "gtars",
    "histolab": "histolab",
    "hypothesis-generation": "Hypothesis Generation",
    "imaging-data-commons": "Imaging Data Commons",
    "iso-13485-certification": "ISO 13485 Certification",
    "labarchive-integration": "LabArchives",
    "lamindb": "LaminDB",
    "latchbio-integration": "LatchBio",
    "literature-review": "Literature Review",
    "matchms": "matchms",
    "omero-integration": "OMERO",
    "opentrons-integration": "Opentrons",
    "pacsomatic": "pacsomatic",
    "paper-lookup": "Paper Lookup",
    "pathml": "PathML",
    "pathway-enrichment": "Pathway Enrichment",
    "phylogenetics": "Phylogenetics",
    "polars-bio": "Polars-Bio",
    "primekg": "PrimeKG",
    "protocolsio-integration": "Protocols.io",
    "pydicom": "pydicom",
    "pyhealth": "PyHealth",
    "pylabrobot": "PyLabRobot",
    "pyopenms": "pyOpenMS",
    "pysam": "pysam",
    "pytdc": "PyTDC",
    "rowan": "Rowan",
    "scientific-brainstorming": "Scientific Brainstorming",
    "scientific-critical-thinking": "Scientific Critical Thinking",
    "scikit-survival": "scikit-survival",
    "tiledbvcf": "TileDB-VCF",
    "torchdrug": "TorchDrug",
    "treatment-plans": "Treatment Plans",
    # General-Purpose Utilities
    "aeon": "aeon",
    "astropy": "Astropy",
    "autoskill": "Autoskill",
    "cirq": "Cirq",
    "citation-management": "Citation Management",
    "consciousness-council": "Consciousness Council",
    "dask": "Dask",
    "docx": "DOCX",
    "exa-search": "Exa Search",
    "exploratory-data-analysis": "Exploratory Data Analysis",
    "fluidsim": "FluidSim",
    "generate-image": "Generate Image",
    "geomaster": "GeoMaster",
    "geopandas": "GeoPandas",
    "get-available-resources": "Get Available Resources",
    "hugging-science": "Hugging Science",
    "hypogenic": "HypoGeniC",
    "infographics": "Infographics",
    "latex-posters": "LaTeX Posters",
    "liteparse": "LiteParse",
    "markdown-mermaid-writing": "Markdown & Mermaid Writing",
    "markitdown": "MarkItDown",
    "matlab": "MATLAB / Octave",
    "matplotlib": "Matplotlib",
    "modal": "Modal",
    "networkx": "NetworkX",
    "open-notebook": "Open Notebook",
    "optimize-for-gpu": "Optimize for GPU",
    "parallel-web": "Parallel Web",
    "pdf": "PDF",
    "peer-review": "Peer Review",
    "pennylane": "PennyLane",
    "polars": "Polars",
    "pptx": "PPTX",
    "pptx-posters": "PPTX Posters",
    "pufferlib": "PufferLib",
    "pymatgen": "Pymatgen",
    "pymc": "PyMC",
    "pymoo": "pymoo",
    "pytorch-lightning": "PyTorch Lightning",
    "pyzotero": "pyzotero",
    "qiskit": "Qiskit",
    "qutip": "QuTiP",
    "research-grants": "Research Grants",
    "research-lookup": "Research Lookup",
    "scholar-evaluation": "Scholar Evaluation",
    "scientific-schematics": "Scientific Schematics",
    "scientific-slides": "Scientific Slides",
    "scientific-visualization": "Scientific Visualization",
    "scientific-writing": "Scientific Writing",
    "scikit-learn": "scikit-learn",
    "seaborn": "Seaborn",
    "shap": "SHAP",
    "simpy": "SimPy",
    "stable-baselines3": "Stable-Baselines3",
    "statistical-analysis": "Statistical Analysis",
    "statsmodels": "statsmodels",
    "sympy": "SymPy",
    "timesfm-forecasting": "TimesFM",
    "torch-geometric": "PyTorch Geometric",
    "transformers": "Transformers (Hugging Face)",
    "umap-learn": "UMAP-learn",
    "usfiscaldata": "US Fiscal Data",
    "vaex": "Vaex",
    "venue-templates": "Venue Templates",
    "what-if-oracle": "What-If Oracle",
    "xlsx": "XLSX",
    "zarr-python": "Zarr-Python",
}


def pretty_name(slug: str) -> str:
    if slug in PRETTY:
        return PRETTY[slug]
    return " ".join(w.capitalize() for w in slug.split("-"))


def parse_frontmatter(text: str) -> dict:
    """Return the SKILL.md YAML front-matter as a dict of collapsed strings."""
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    fm = m.group(1) if m else ""
    out = {}
    for key in ("name", "description", "license"):
        mm = re.search(rf"^{key}:\s*(.*?)(?=\n[A-Za-z_][\w-]*:|\Z)", fm, re.S | re.M)
        if mm:
            out[key] = re.sub(r"\s+", " ", mm.group(1)).strip().strip('"').strip("'")
        else:
            out[key] = ""
    return out


def clean_license(raw: str) -> str:
    """Sanitise the messy upstream `license` field into a short label."""
    if not raw:
        return "not stated upstream"
    s = re.split(r"\s*allowed-tools:", raw)[0].strip()
    if not s or s.lower() == "unknown":
        return "not stated upstream"
    if s.startswith("http"):
        return "see upstream LICENSE"
    s = re.sub(r"\s+licen[cs]e\b", "", s, flags=re.I).strip().rstrip(".")
    return s or "not stated upstream"


def first_sentence(desc: str) -> str:
    desc = desc.strip().lstrip(">").strip()
    m = re.match(r"(.+?[.!?])(\s|$)", desc)
    return (m.group(1) if m else desc).strip()


def make_summary(desc: str, limit: int = 25) -> str:
    """<= `limit`-word plain-language card summary."""
    desc = desc.strip().lstrip(">").strip()
    # Drop boilerplate openers so the summary leads with the capability.
    desc = re.sub(r"^(Use this skill (whenever|when|for|any time)|"
                  r"This skill should be used (for|when|whenever)|Use when|Use for)\b[:,]?\s*",
                  "", desc, flags=re.I).strip()
    desc = desc[:1].upper() + desc[1:] if desc else desc
    # Prefer a clean first sentence when it already fits.
    sentence = first_sentence(desc)
    if sentence and len(sentence.split()) <= limit:
        return sentence
    words = desc.split()
    if len(words) <= limit:
        return " ".join(words)
    return " ".join(words[: limit - 1]).rstrip(",.;:") + " …"


def use_cases(desc: str) -> str:
    for marker in ("Use when ", "Use for ", "Best for ", "Use this skill when "):
        i = desc.find(marker)
        if i != -1:
            tail = desc[i + len(marker):]
            tail = re.split(r"(?<=[.!?])\s", tail, maxsplit=1)[0]
            return tail.strip().rstrip(".")
    return first_sentence(desc).rstrip(".")


# --- install-block templates -------------------------------------------------

def install_block(slug: str) -> str:
    return f"""## How to install

- **Claude Code / Claude.ai** — Skills CLI (recommended):
  ```
  npx skills add {REPO_URL.split('https://github.com/')[1]}
  ```
  Installs the K-Dense collection; enable the `{slug}` skill when prompted. Works across Claude Code, Cursor, and Codex via the Agent Skills spec (requires Node ≥ 18).
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone {REPO_URL}
  cp -r scientific-agent-skills/skills/{slug} ~/.claude/skills/
  ```
  Project-scoped alternative: copy into `.claude/skills/` instead of `~/.claude/skills/`. The skill declares its own Python dependencies in its `SKILL.md`; install them (the K-Dense skills generally use `uv` / `pip`) when prompted on first use."""


def footer(slug: str) -> str:
    return (
        "## Installed this tool?\n\n"
        f"[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?"
        f"template=tool-feedback.yml&tool={slug}&details=Filed+from+"
        f"https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2F{slug}.html%0A%0A)"
        " — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page."
    )


def render_page(slug: str, categories, fm: dict) -> str:
    title = f"{pretty_name(slug)} (Claude Skill)"
    desc = fm["description"]
    summary = make_summary(desc)
    lic = clean_license(fm["license"])
    pricing = f"Free / OSS ({lic})" if lic != "not stated upstream" else "Free / OSS — license not stated upstream"
    cat_yaml = "[" + ", ".join(categories) + "]"
    skill_url = f"{REPO_URL}/blob/main/skills/{slug}/SKILL.md"
    return f"""---
title: {title}
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: K-Dense
availability: GA
tool_categories: {cat_yaml}
last_verified: {TODAY}
summary: {summary}
---

# {title}

{first_sentence(desc)}

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | {SUPPLIER_LINK} |
| **Availability** | GA — part of the actively maintained K-Dense `scientific-agent-skills` collection |
| **Pricing** | {pricing} |
| **Capabilities** | Read/Write — Claude runs the skill's Python locally (Bash), not as an MCP tool |

{install_block(slug)}

## What it does

{desc}

**Primary use cases**: {use_cases(desc)}.

## Notes

Distributed as a `SKILL.md` (plus code examples) in the K-Dense collection — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: {lic}. The skill name to enable after install is `{slug}`.

## Sources

- [`{REPO_URL.split('https://github.com/')[1]}`]({REPO_URL})
- [`skills/{slug}/SKILL.md`]({skill_url})

---

{footer(slug)}
"""


# --- repair of existing K-Dense pages ----------------------------------------

MARKETPLACE_RE = re.compile(
    r"- \*\*Claude Code\*\* — plugin marketplace:\n"
    r"\s*```\n"
    r"\s*/plugin marketplace add K-Dense-AI/claude-scientific-skills\n"
    r"\s*/plugin install [^\n]+@claude-scientific-skills\n"
    r"\s*```\n"
)


def repair_text(text: str, slug: str) -> str:
    npx_bullet = (
        "- **Claude Code / Claude.ai** — Skills CLI (recommended):\n"
        f"  ```\n  npx skills add {REPO_URL.split('https://github.com/')[1]}\n  ```\n"
        f"  Installs the K-Dense collection; enable the `{slug}` skill when prompted "
        "(also works in Cursor/Codex via the Agent Skills spec; requires Node ≥ 18).\n"
    )
    if MARKETPLACE_RE.search(text):
        text = MARKETPLACE_RE.sub(npx_bullet, text, count=1)
    elif "npx skills add" not in text:
        # Bare-clone page (e.g. flowio, rdkit-skill, scikit-bio): add a prose
        # line above the fenced clone block.
        text = text.replace(
            "## How to install\n\n```\ngit clone",
            "## How to install\n\n"
            "Install via the Skills CLI (recommended): "
            f"`npx skills add {REPO_URL.split('https://github.com/')[1]}`, then enable the "
            f"`{slug}` skill. Or clone the repo manually:\n\n```\ngit clone",
            1,
        )
    # Path migration: scientific-skills/ -> skills/
    text = text.replace("scientific-agent-skills/scientific-skills/", "scientific-agent-skills/skills/")
    text = text.replace("scientific-skills/", "skills/")
    # Bump last_verified.
    text = re.sub(r"^last_verified:\s*\d{4}-\d{2}-\d{2}\s*$",
                  f"last_verified: {TODAY}", text, count=1, flags=re.M)
    return text


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default="/tmp/kdense", help="local clone of scientific-agent-skills")
    ap.add_argument("--map", default=str(Path(__file__).with_name("kdense_category_map.yaml")))
    ap.add_argument("--catalog", default=str(Path(__file__).resolve().parent.parent / "catalog" / "tools"))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    cfg = yaml.safe_load(Path(args.map).read_text())
    include = cfg["include"]
    aliases = cfg.get("aliases", {})
    skills_dir = Path(args.repo) / "skills"
    catalog = Path(args.catalog)

    created, repaired, missing_src, skipped_dup = [], [], [], []

    for slug in sorted(include):
        categories = include[slug]
        src = skills_dir / slug / "SKILL.md"
        if not src.exists():
            missing_src.append(slug)
            continue
        fm = parse_frontmatter(src.read_text(encoding="utf-8"))
        existing_slug = aliases.get(slug, slug)
        dest = catalog / f"{existing_slug}.md"

        if dest.exists():
            new_text = repair_text(dest.read_text(encoding="utf-8"), slug)
            if not args.dry_run:
                dest.write_text(new_text, encoding="utf-8")
            repaired.append(existing_slug)
        else:
            page = render_page(slug, categories, fm)
            if not args.dry_run:
                dest.write_text(page, encoding="utf-8")
            created.append(slug)

    print(f"{'DRY-RUN ' if args.dry_run else ''}K-Dense batch ingest @ {TODAY}")
    print(f"  in-scope skills in map : {len(include)}")
    print(f"  created (new pages)    : {len(created)}")
    print(f"  repaired (existing)    : {len(repaired)}")
    print(f"  missing in source repo : {len(missing_src)}  {missing_src or ''}")
    if created:
        print("  CREATED:", ", ".join(created))
    if repaired:
        print("  REPAIRED:", ", ".join(repaired))
    return 1 if missing_src else 0


if __name__ == "__main__":
    sys.exit(main())
