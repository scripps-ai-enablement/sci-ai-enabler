#!/usr/bin/env python3
"""Generalised batch ingestion of community skill collections into the catalog.

The multi-collection successor to scripts/ingest_kdense.py. Driven by
scripts/collections.yaml (the per-collection registry) + a sibling
scripts/<collection>_category_map.yaml (the auditable scope filter), it walks a
local clone of a collection and, for every in-scope skill, either:

  * CREATE  — renders a new catalog/tools/<slug>.md page (tool not yet
    catalogued from any source), or
  * AUGMENT — appends a sentinel-guarded "Also available in <collection>"
    install bullet to the existing page (tool already catalogued — one entry
    per tool; the augment map says which existing slug it belongs to).

Augmentation is idempotent: re-runs detect the `<!-- alt-install:<key> -->`
sentinel and skip. Skills listed under `skip` are recorded (with a reason) and
never written.

Usage:
    python3 scripts/ingest_collection.py sciagent  --repo /tmp/SciAgent-Skills --dry-run
    python3 scripts/ingest_collection.py neuroclaw --repo /tmp/NeuroClaw
"""
from __future__ import annotations

import argparse
import datetime as _dt
import re
import sys
from pathlib import Path

import yaml

TODAY = _dt.date.today().isoformat()
HERE = Path(__file__).resolve().parent
CATEGORIES = {
    "Chemistry", "Immunology and Microbiology",
    "Integrative Structural and Computational Biology",
    "Molecular and Cellular Biology", "Neuroscience", "Translational Medicine",
    "Drug Repurposing and Discovery", "All", "General-Purpose Utilities",
}


# --- frontmatter + text helpers (shared with the K-Dense ingester) -----------

def parse_frontmatter(text: str) -> dict:
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    fm = m.group(1) if m else ""
    out = {}
    for key in ("name", "description", "license"):
        mm = re.search(rf"^{key}:\s*(.*?)(?=\n[A-Za-z_][\w-]*:|\Z)", fm, re.S | re.M)
        out[key] = re.sub(r"\s+", " ", mm.group(1)).strip().strip('"').strip("'") if mm else ""
    return out


def clean_license(raw: str) -> str:
    if not raw:
        return "not stated upstream"
    s = re.split(r"\s*allowed-tools:", raw)[0].strip()
    if not s or s.lower() == "unknown":
        return "not stated upstream"
    if s.startswith("http"):
        return "see upstream LICENSE"
    # Drop NeuroClaw's parenthetical gloss, keep the SPDX-ish head.
    s = re.sub(r"\s*\(.*?\)\s*$", "", s).strip()
    s = re.sub(r"\s+licen[cs]e\b", "", s, flags=re.I).strip().rstrip(".")
    return s or "not stated upstream"


_OPENER = re.compile(
    r"^(use this (skill|model doc)( whenever| when| for| any time)?|"
    r"this (skill|model doc) should be used( for| when| whenever)?|use when|use for)\b[:,]?\s*",
    re.I)


def clean_opener(desc: str) -> str:
    """Strip trigger-phrase openers (esp. NeuroClaw's 'Use this skill whenever
    the user wants to ...') so the lead reads as a capability, not a trigger."""
    d = desc.strip().lstrip(">").strip()
    prev = None
    while prev != d:
        prev = d
        d = _OPENER.sub("", d).strip()
        d = re.sub(r"^(the user wants?( to| an?)?\s+|any[\w\s/()'-]*?\s+needs to\s+)", "", d, flags=re.I).strip()
    return (d[:1].upper() + d[1:]) if d else d


def first_sentence(desc: str) -> str:
    desc = clean_opener(desc)
    m = re.match(r"(.+?[.!?])(\s|$)", desc)
    return (m.group(1) if m else desc).strip()


def make_summary(desc: str, limit: int = 25) -> str:
    desc = clean_opener(desc)
    # Drop a trailing "Triggers include: ..." clause that bloats NeuroClaw descs.
    desc = re.split(r"\bTriggers include\b", desc, flags=re.I)[0].strip().rstrip(".")
    desc = desc[:1].upper() + desc[1:] if desc else desc
    sentence = first_sentence(desc)
    if sentence and len(sentence.split()) <= limit:
        return sentence
    words = desc.split()
    if len(words) <= limit:
        return " ".join(words)
    return " ".join(words[: limit - 1]).rstrip(",.;:") + " …"


def use_cases(desc: str) -> str:
    for marker in ("Use when ", "Use for ", "Best for ", "Use this skill when ", "Triggers include: "):
        i = desc.find(marker)
        if i != -1:
            tail = desc[i + len(marker):]
            tail = re.split(r"(?<=[.!?])\s", tail, maxsplit=1)[0]
            return tail.strip().rstrip(".")
    return first_sentence(desc).rstrip(".")


# --- per-collection install blocks -------------------------------------------

def install_block(cfg: dict, slug: str, src_relpath: str) -> str:
    repo = cfg["repo"]
    kind = cfg["install"]
    label = cfg["collection_label"]
    if kind == "npx":
        return f"""## How to install

- **Claude Code / Claude.ai** — Skills CLI (recommended):
  ```
  npx skills add {repo}
  ```
  Installs {label}; enable the `{slug}` skill when prompted. Works across Claude Code, Cursor, and Codex via the Agent Skills spec (requires Node ≥ 18).
- **Claude Code / Claude Desktop** — manual clone:
  ```
  git clone https://github.com/{repo}
  cp -r {repo.split('/')[1]}/{src_relpath.rsplit('/', 1)[0]} ~/.claude/skills/
  ```
  Project-scoped alternative: copy into `.claude/skills/` instead of `~/.claude/skills/`. Install the skill's declared Python dependencies on first use."""
    if kind == "plugin":
        plugin = cfg["plugin_name"]
        return f"""## How to install

SciAgent-Skills is **not** an npm package — skills are plain markdown read directly by the agent (no `npx`/`npm`).

- **Claude Code** — clone and load as a plugin:
  ```
  git clone https://github.com/{repo}
  ```
  Then inside Claude Code run `/plugin install {plugin}` (verify it appears under `/plugin` → Installed). Clone into your project directory so Claude Code picks the skills up via `CLAUDE.md`.
- **Manual / other agents** — point the agent at the skill file directly:
  ```
  cp -r {repo.split('/')[1]}/{src_relpath.rsplit('/', 1)[0]} ~/.claude/skills/
  ```
  The skill declares its own Python dependencies in its `SKILL.md`; install them when prompted on first use."""
    # library (NeuroClaw)
    return f"""## How to install

- **Claude Code** — clone and copy the skill into your skills directory:
  ```
  git clone https://github.com/{repo}
  cp -r {repo.split('/')[1]}/{src_relpath.rsplit('/', 1)[0]} ~/.claude/skills/
  ```
  Project-scoped alternative: copy into `.claude/skills/` instead. NeuroClaw skills assume the collection's shared helpers (`claw-shell`, modality tool skills) and the upstream neuroimaging stack (FreeSurfer/FSL/fMRIPrep/etc.) — install those dependencies, or run the bundled installer for the full environment:
  ```
  cd {repo.split('/')[1]} && python installer/setup.py
  ```
  which configures the Python env, CUDA/GPU, and the neuroimaging tools."""


def footer(slug: str) -> str:
    return (
        "## Installed this tool?\n\n"
        f"[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?"
        f"template=tool-feedback.yml&tool={slug}&details=Filed+from+"
        f"https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2F{slug}.html%0A%0A)"
        " — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page."
    )


def render_page(cfg: dict, out_slug: str, categories, fm: dict, src_relpath: str, pretty: dict) -> str:
    repo = cfg["repo"]
    title = f"{pretty.get(out_slug, ' '.join(w.capitalize() for w in out_slug.split('-')))} (Claude Skill)"
    desc = fm["description"]
    lic = clean_license(fm["license"])
    pricing = f"Free / OSS ({lic})" if lic != "not stated upstream" else "Free / OSS — license not stated upstream"
    cat_yaml = "[" + ", ".join(categories) + "]"
    summary = make_summary(desc).replace('"', "'")  # quoted scalar below — colons are common
    skill_url = f"https://github.com/{repo}/blob/main/{src_relpath}"
    return f"""---
title: {title}
parent: All tools
grand_parent: Catalog
tool_type: Claude Skill
supplier: {cfg['supplier']}
availability: GA
tool_categories: {cat_yaml}
last_verified: {TODAY}
summary: "{summary}"
---

# {title}

{first_sentence(desc)}

| | |
|---|---|
| **Type** | Claude Skill |
| **Supplier** | {cfg['supplier_link']} |
| **Availability** | {cfg['availability_note']} |
| **Pricing** | {pricing} |
| **Capabilities** | Read/Write — Claude runs the skill's Python locally (Bash), not as an MCP tool |

{install_block(cfg, out_slug, src_relpath)}

## What it does

{desc}

**Primary use cases**: {use_cases(desc)}.

## Notes

Distributed as a `SKILL.md` (plus code examples) in {cfg['collection_label']} — Claude executes it locally via Bash/Python rather than as an MCP server. Upstream license: {lic}. The skill directory upstream is `{src_relpath.rsplit('/', 1)[0]}`.

## Sources

- [`{repo}`](https://github.com/{repo})
- [`{src_relpath}`]({skill_url})

---

{footer(out_slug)}
"""


# --- idempotent augmentation of an existing page -----------------------------

def augment_text(text: str, cfg: dict, key: str, src_relpath: str) -> str | None:
    """Insert an 'Also available in <collection>' bullet under '## How to
    install'. Returns new text, or None if already present / no anchor."""
    sentinel = f"<!-- alt-install:{key} -->"
    if sentinel in text:
        return None
    anchor = "## How to install\n\n"
    idx = text.find(anchor)
    if idx == -1:
        return None
    repo = cfg["repo"]
    if cfg["install"] == "plugin":
        how = (f"clone [`{repo}`](https://github.com/{repo}) and run `/plugin install "
               f"{cfg['plugin_name']}` in Claude Code (or copy `{src_relpath.rsplit('/', 1)[0]}` "
               f"into `~/.claude/skills/`)")
    else:  # library / npx fallbacks
        how = (f"clone [`{repo}`](https://github.com/{repo}) and copy "
               f"`{src_relpath.rsplit('/', 1)[0]}` into `~/.claude/skills/`")
    bullet = (f"{sentinel}\n- **Also packaged in {cfg['collection_label']}** "
              f"({cfg['supplier_link']}): {how}.\n<!-- /alt-install:{key} -->\n")
    pos = idx + len(anchor)
    return text[:pos] + bullet + text[pos:]


# --- main --------------------------------------------------------------------

def build_index(repo_root: Path, cfg: dict) -> dict:
    """slug -> SKILL.md path, repo-relative."""
    base = repo_root / cfg["skills_subdir"]
    out = {}
    for p in base.rglob("SKILL.md"):
        out[p.parent.name] = p
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("collection", help="key in scripts/collections.yaml (e.g. sciagent, neuroclaw)")
    ap.add_argument("--repo", required=True, help="local clone of the collection repo")
    ap.add_argument("--catalog", default=str(HERE.parent / "catalog" / "tools"))
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    registry = yaml.safe_load((HERE / "collections.yaml").read_text())
    if args.collection not in registry:
        print(f"unknown collection '{args.collection}'", file=sys.stderr)
        return 2
    cfg = registry[args.collection]
    cmap = yaml.safe_load((HERE / f"{args.collection}_category_map.yaml").read_text())
    include = cmap.get("include", {}) or {}
    augment = cmap.get("augment", {}) or {}
    aliases = cmap.get("aliases", {}) or {}
    skip = cmap.get("skip", {}) or {}
    pretty = cmap.get("pretty", {}) or {}

    repo_root = Path(args.repo)
    catalog = Path(args.catalog)
    index = build_index(repo_root, cfg)

    created, augmented, skipped_already, missing_src, bad_cat, no_anchor = [], [], [], [], [], []

    # validate categories
    for slug, cats in include.items():
        for c in cats:
            if c not in CATEGORIES:
                bad_cat.append((slug, c))
    if bad_cat:
        for slug, c in bad_cat:
            print(f"  BAD CATEGORY: {slug} -> {c!r}", file=sys.stderr)
        return 2

    def relpath(src: Path) -> str:
        return str(src.relative_to(repo_root))

    # CREATE
    for slug in sorted(include):
        src = index.get(slug)
        if src is None:
            missing_src.append(slug)
            continue
        out_slug = aliases.get(slug, slug)
        dest = catalog / f"{out_slug}.md"
        if dest.exists():
            # collision the map didn't flag — refuse to overwrite, treat as augment-needed
            no_anchor.append(f"{slug} (would overwrite existing {out_slug}.md — move to `augment`)")
            continue
        page = render_page(cfg, out_slug, include[slug], parse_frontmatter(src.read_text(encoding="utf-8")),
                           relpath(src), pretty)
        if not args.dry_run:
            dest.write_text(page, encoding="utf-8")
        created.append(out_slug)

    # AUGMENT
    for slug, canon in sorted(augment.items()):
        src = index.get(slug)
        if src is None:
            missing_src.append(slug)
            continue
        dest = catalog / f"{canon}.md"
        if not dest.exists():
            no_anchor.append(f"{slug} -> {canon}.md (augment target missing)")
            continue
        new = augment_text(dest.read_text(encoding="utf-8"), cfg, args.collection, relpath(src))
        if new is None:
            skipped_already.append(f"{slug}->{canon}")
            continue
        if not args.dry_run:
            dest.write_text(new, encoding="utf-8")
        augmented.append(f"{slug}->{canon}")

    print(f"{'DRY-RUN ' if args.dry_run else ''}{args.collection} batch ingest @ {TODAY}")
    print(f"  include (create) in map : {len(include)}")
    print(f"  augment (existing) in map: {len(augment)}")
    print(f"  skip (recorded)         : {len(skip)}")
    print(f"  --> CREATED  : {len(created)}")
    print(f"  --> AUGMENTED: {len(augmented)}")
    print(f"  --> already-augmented (idempotent skip): {len(skipped_already)}")
    print(f"  --> missing in source repo: {len(missing_src)}  {missing_src or ''}")
    if no_anchor:
        print(f"  !! NEEDS ATTENTION ({len(no_anchor)}):")
        for x in no_anchor:
            print(f"       {x}")
    if created:
        print("  CREATED:", ", ".join(created))
    if augmented:
        print("  AUGMENTED:", ", ".join(augmented))
    return 1 if (missing_src or no_anchor) else 0


if __name__ == "__main__":
    sys.exit(main())
