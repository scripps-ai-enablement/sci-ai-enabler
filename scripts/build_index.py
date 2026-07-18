#!/usr/bin/env python3
"""Build the Composer semantic index from the knowledge-base pages.

A deterministic projection of every catalog tool, recipe, and autonomous-science
system into one compact JSON file the Composer plugin loads in full. Each entry
carries its filterable frontmatter *facets* plus the curated `summary` and a mined
`keywords` list — the fields the model matches a scientist's problem against. The
long prose isn't stored (it would bloat the load); the model reads a shortlisted
candidate's full page on demand.

Design notes:
- stdlib only (no PyYAML); the frontmatter here is simple `key: value` / inline
  `[a, b, c]` lists, so a small hand parser is enough.
- The seven subject-area categories are non-mutually-exclusive Scripps departments,
  so they are stored as facets for ranking — never used as a retrieval gate. The
  matchable meaning lives in `semantic_digest`/`keywords`.
- Fails loudly (exit 1) on any closed-vocab facet value out of range, or on a page
  missing its mandated one-sentence lead description (it backs the summary/keywords
  an entry is matched on). A silent data bug becomes a visible CI failure.

Run: python3 scripts/build_index.py   (writes index/composer-index.json)
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
# Two artifacts, mirroring the repo's "answers vs ingredients" split:
#   composer-index.json  — curated recipes (the answers; always loaded)
#   composer-tools.json  — the catalog (the ingredient library; loaded only when
#                          the composer reaches the ladder-walk step)
# Autonomous-science systems are still parsed and validated (page-quality CI) but
# are NOT written to the composer index: they are external systems the composer
# cannot install or run, so they are informational site content only. A system
# that is genuinely hookable earns a catalog entry (e.g. Biomni as a Claude Skill).
OUT_INDEX = REPO / "index" / "composer-index.json"
OUT_TOOLS = REPO / "index" / "composer-tools.json"
# The plugin bundles a mirror of the index so it works on a fresh marketplace
# install with no repo checkout. build_index writes both locations so they can't
# drift; the workflow commits both.
PLUGIN_DATA = REPO / "composer" / "skills" / "compose" / "data"

# ---- closed vocabularies (facets we validate; see AGENT.md / RECIPE_AGENT.md) ----

SUBJECT_AREAS = {
    "Chemistry",
    "Immunology and Microbiology",
    "Integrative Structural and Computational Biology",
    "Molecular and Cellular Biology",
    "Neuroscience",
    "Translational Medicine",
    "Drug Repurposing and Discovery",
    "All",
}
TOOL_CATEGORIES = SUBJECT_AREAS | {"General-Purpose Utilities"}
PROBLEM_CLASSES = {
    "Literature triage",
    "Hypothesis generation",
    "Experimental design",
    "Data analysis",
    "Knowledge synthesis",
    "Manuscript prep",
    "Workflow automation",
}
EVIDENCE_LEVELS = {"Validated", "Reported", "Proposed"}
COMPLEXITY = {
    "Claude Code alone",
    "One skill or MCP",
    "Multi-tool harness",
    "Autonomous system",
}
RECIPE_AVAILABILITY = {
    "Fully open",
    "Subscription required",
    "Institutional access",
    "Internal only",
}
COMPUTE = {
    "Laptop",
    "Workstation with GPU",
    "Multi-GPU server",
    "HPC or cloud cluster",
}

# Acronym / technical-term shape for keyword extraction: a token containing a run
# of >=2 uppercase letters (RNA, ADMET, EEG, PDB, CRISPR, scRNA-seq, AlphaFold…).
KEYWORD_RE = re.compile(r"\b[A-Za-z][A-Za-z0-9]*[A-Z]{2,}[A-Za-z0-9-]*\b")
ALSO_KEYWORD_RE = re.compile(r"\b[A-Z][a-zA-Z]+(?:-[A-Za-z0-9]+)+\b")  # hyphenated, e.g. RNA-seq

# High-frequency, low-signal tokens that appear across most pages and don't help
# discriminate one component from another — drop them from the keyword list.
KEYWORD_STOPLIST = {
    "MCP", "API", "APIs", "LLM", "LLMs", "GA", "OSS", "JSON", "HTTP", "HTTPS",
    "URL", "URLs", "AI", "PDF", "CSV", "TSV", "UI", "CLI", "SDK", "ID", "IDs",
    "OS", "VM", "GPU", "CPU", "RAM", "README", "GitHub", "PyPI",
}


class PageError(Exception):
    pass


def parse_frontmatter(text: str, path: Path) -> tuple[dict, str]:
    """Return (frontmatter dict, body). Raises PageError if no frontmatter."""
    if not text.startswith("---"):
        raise PageError(f"{path}: no YAML frontmatter")
    end = text.find("\n---", 3)
    if end == -1:
        raise PageError(f"{path}: unterminated frontmatter")
    fm_block = text[3:end].strip("\n")
    body = text[end + 4 :]

    fm: dict = {}
    for line in fm_block.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, raw = line.partition(":")
        key = key.strip()
        raw = raw.strip()
        if raw.startswith("[") and raw.endswith("]"):
            inner = raw[1:-1].strip()
            fm[key] = [v.strip() for v in inner.split(",")] if inner else []
        else:
            fm[key] = raw
    return fm, body


def lead_description(body: str, path: Path) -> str:
    """The one-sentence paragraph between the first `# ` heading and the metadata
    table (or first `## ` section). Mandated by every page schema."""
    lines = body.splitlines()
    started = False
    para: list[str] = []
    for line in lines:
        if not started:
            if line.startswith("# "):
                started = True
            continue
        stripped = line.strip()
        if not stripped:
            if para:
                break
            continue
        if stripped.startswith(("|", "##", "<!--")):
            break
        para.append(stripped)
    text = " ".join(para).strip()
    if not text:
        raise PageError(f"{path}: missing lead description (one-sentence summary under the # title)")
    return text


def section_body(body: str, header: str) -> str:
    """First paragraph under a `## <header>` section, if present."""
    pattern = re.compile(rf"^## {re.escape(header)}\s*$", re.MULTILINE)
    m = pattern.search(body)
    if not m:
        return ""
    rest = body[m.end() :].splitlines()
    para: list[str] = []
    for line in rest:
        stripped = line.strip()
        if not stripped:
            if para:
                break
            continue
        if stripped.startswith(("##", "|", "<!--", "```")):
            if para:
                break
            continue
        # strip leading list markers / numbering for a cleaner digest
        para.append(re.sub(r"^(\d+\.|[-*])\s+", "", stripped))
    return " ".join(para).strip()


def extract_keywords(*texts: str) -> list[str]:
    found: dict[str, None] = {}
    for t in texts:
        for rx in (KEYWORD_RE, ALSO_KEYWORD_RE):
            for tok in rx.findall(t):
                tok = tok.strip(".,;:()")
                if 2 <= len(tok) <= 30 and tok not in KEYWORD_STOPLIST:
                    found.setdefault(tok, None)
    return sorted(found, key=str.lower)[:12]


def require(fm: dict, key: str, path: Path) -> str:
    val = fm.get(key)
    if not val:
        raise PageError(f"{path}: missing required frontmatter `{key}`")
    return val


def check_vocab(values, allowed: set, field: str, path: Path, errors: list):
    vals = values if isinstance(values, list) else [values]
    for v in vals:
        if v not in allowed:
            errors.append(f"{path}: `{field}` value {v!r} not in closed vocabulary")


def _is_truthy(val) -> bool:
    return str(val).strip().lower() in {"true", "yes", "1"}


def build_tool(path: Path, errors: list) -> dict | None:
    fm, body = parse_frontmatter(path.read_text(encoding="utf-8"), path)
    title = require(fm, "title", path)
    summary = fm.get("summary", "")
    categories = fm.get("tool_categories", [])
    check_vocab(categories, TOOL_CATEGORIES, "tool_categories", path, errors)
    lead = lead_description(body, path)
    what = section_body(body, "What it does")
    # The matchable representation is summary + keywords + facets; keywords are
    # mined from the lead/section text so salient methods/entities survive even
    # though the long prose isn't stored. Finalists get a full-page read on demand.
    keywords = extract_keywords(title, summary, lead, what)
    # `claude_science: true` marks a component that is offered inside Anthropic's
    # Claude Science. The keyword miner can't recover the phrase from prose (no
    # 2+-uppercase run), so inject it as a first-class keyword — this is how the
    # marker becomes discoverable via the composer's summary+keyword match.
    claude_science = _is_truthy(fm.get("claude_science", ""))
    if claude_science and "Claude Science" not in keywords:
        keywords = (["Claude Science"] + keywords)[:12]
    return {
        "slug": path.stem,
        "title": title,
        "tool_type": fm.get("tool_type", ""),
        "availability": fm.get("availability", ""),
        "tool_categories": categories,
        "last_verified": fm.get("last_verified", ""),
        "claude_science": claude_science,
        "summary": summary,
        "keywords": keywords,
        "path": f"catalog/tools/{path.name}",
    }


def build_recipe(path: Path, errors: list) -> dict | None:
    fm, body = parse_frontmatter(path.read_text(encoding="utf-8"), path)
    title = require(fm, "title", path)
    summary = fm.get("summary", "")
    pc = fm.get("problem_class", "")
    sa = fm.get("subject_areas", [])
    ev = fm.get("evidence_level", "")
    cx = fm.get("complexity", "")
    av = fm.get("availability", "")
    cr = fm.get("compute_requirements", "")
    check_vocab(pc, PROBLEM_CLASSES, "problem_class", path, errors)
    check_vocab(sa, SUBJECT_AREAS, "subject_areas", path, errors)
    check_vocab(ev, EVIDENCE_LEVELS, "evidence_level", path, errors)
    check_vocab(cx, COMPLEXITY, "complexity", path, errors)
    check_vocab(av, RECIPE_AVAILABILITY, "availability", path, errors)
    check_vocab(cr, COMPUTE, "compute_requirements", path, errors)
    lead = lead_description(body, path)
    problem = section_body(body, "Problem")
    return {
        "slug": path.stem,
        "title": title,
        "problem_class": pc,
        "subject_areas": sa,
        "evidence_level": ev,
        "complexity": cx,
        "availability": av,
        "compute_requirements": cr,
        "last_verified": fm.get("last_verified", ""),
        "summary": summary,
        "keywords": extract_keywords(title, summary, lead, problem),
        "path": f"recipes/items/{path.name}",
    }


def build_system(path: Path, errors: list) -> dict | None:
    fm, body = parse_frontmatter(path.read_text(encoding="utf-8"), path)
    title = require(fm, "title", path)
    tagline = fm.get("tagline", "")
    lead = lead_description(body, path)
    summary = tagline or lead
    return {
        "slug": path.stem,
        "title": title,
        "domain": fm.get("domain", ""),
        "lifecycle_stages": fm.get("lifecycle_stages", []),
        "validation_type": fm.get("validation_type", ""),
        "autonomy": fm.get("autonomy", ""),
        "availability": fm.get("availability", ""),
        "access": fm.get("access", ""),
        "last_verified": fm.get("last_verified", ""),
        "summary": summary,
        "keywords": extract_keywords(title, tagline, lead),
        "path": f"autonomous-science/systems/{path.name}",
    }


def collect(repo: Path, glob: str, builder, errors: list) -> list[dict]:
    out = []
    for path in sorted(repo.glob(glob)):
        if path.name == "index.md":
            continue
        try:
            entry = builder(path, errors)
            if entry is not None:
                out.append(entry)
        except PageError as e:
            errors.append(str(e))
    return out


def build_all(repo: Path) -> tuple[list[dict], list[dict], list[dict], list[str]]:
    """Parse every page under `repo` into (tools, recipes, systems, errors).
    Pure: reads the corpus, writes nothing. Tests call this against the real repo
    and against synthetic temp corpora; main() wraps it with file output."""
    errors: list[str] = []
    tools = collect(repo, "catalog/tools/*.md", build_tool, errors)
    recipes = collect(repo, "recipes/items/*.md", build_recipe, errors)
    systems = collect(repo, "autonomous-science/systems/*.md", build_system, errors)
    return tools, recipes, systems, errors


def main() -> int:
    tools, recipes, systems, errors = build_all(REPO)

    if errors:
        print(f"build_index: {len(errors)} page error(s):", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    from datetime import datetime, timezone

    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    index = {
        "version": 1,
        "generated": generated,
        "counts": {"tools": len(tools), "recipes": len(recipes)},
        "tools_file": "composer-tools.json",
        "recipes": recipes,
    }
    tools_doc = {
        "version": 1,
        "generated": generated,
        "count": len(tools),
        "tools": tools,
    }
    index_json = json.dumps(index, indent=2, ensure_ascii=False) + "\n"
    tools_json = json.dumps(tools_doc, indent=2, ensure_ascii=False) + "\n"
    for base in (OUT_INDEX.parent, PLUGIN_DATA):
        base.mkdir(parents=True, exist_ok=True)
        (base / "composer-index.json").write_text(index_json, encoding="utf-8")
        (base / "composer-tools.json").write_text(tools_json, encoding="utf-8")
    print(
        f"build_index: wrote index/ and {PLUGIN_DATA.relative_to(REPO)}/ — "
        f"{len(recipes)} recipes, {len(tools)} tools "
        f"({len(systems)} autonomous-science pages validated, not indexed)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
