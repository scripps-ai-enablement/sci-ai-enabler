#!/usr/bin/env python3
"""Step 1 of the composer A/B evaluation: build the prompt set.

For each recipe, produce one plain-language question a scientist would actually type,
naming no tools. The recipe's own prompt block cannot be used for this: it reads
"Build a dossier for STK11. Use open-targets, uniprot, alphafold..." and hands over the
answer, which would make both arms score identically.

So the question is generated from the recipe's ``## Problem`` section (all 70 recipes
have one), and the *answer key* is extracted mechanically from the ``catalog/tools/*``
links on the page (all 70 recipes have at least one).

A generated question that still names a tool from its own answer key is rejected and
regenerated, up to --max-attempts times. That check is what protects the whole
experiment, so it is not optional.

Usage:
    python3 validation/make_prompts.py                      # the 10 pilot recipes
    python3 validation/make_prompts.py --all                # all 70
    python3 validation/make_prompts.py --only build-target-dossier
    python3 validation/make_prompts.py --check              # re-run leak check on existing file

See validation/PLAN.md for the full design.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
ITEMS = REPO / "recipes" / "items"
INDEX = REPO / "composer" / "skills" / "compose" / "data" / "composer-index.json"
TOOLS = REPO / "composer" / "skills" / "compose" / "data" / "composer-tools.json"
MODEL = "claude-sonnet-5"

# The 10-recipe pilot, per validation/PLAN.md. Spans complexity and problem_class rather
# than maximizing the expected effect -- a pilot stacked with multi-tool recipes would
# inflate the effect size and be useless for sizing the full run.
PILOT = [
    "build-target-dossier",
    "estimate-pk-properties",
    "scan-drug-repurposing-candidates",
    "map-disease-to-genes-and-pathways",
    "extract-structured-data-from-clinical-notes",  # negative control: no tool needed
    "benchmark-admet-property-with-pytdc",
    "identify-bacterial-isolate-from-16s-sequence",
    "design-crispr-sgrnas-for-a-gene-knockout",
    "find-selective-cancer-dependencies-with-depmap",
    "draft-phase23-clinical-trial-protocol",
]

REWRITE_PROMPT = """\
Below is the "Problem" section of a scientific how-to page.

Rewrite it as ONE question that a working life scientist would type into Claude when
they have this problem and do not yet know what tooling exists.

Hard rules:
- Name NO database, tool, skill, plugin, MCP server, software package, algorithm, or
  website. Not even in passing. Describe the goal and the data they have, never the means.
- Keep any concrete scientific specifics (gene names, organisms, file formats, sample
  types, endpoints) -- those make the question realistic and answerable.
- The question must be SELF-CONTAINED and answerable as written. Never refer to data,
  a file, a sequence, or a paragraph that you do not actually include in the text. If the
  task needs a specific input, put a concrete realistic example inline (a real gene
  symbol, an actual SMILES string, a named disease) rather than saying "my compound" or
  "the attached notes". A question that would make the reader ask "what is your X?" is wrong.
- 1 to 4 sentences. First person. No preamble, no markdown, no quotes around it.
- Output ONLY the question text.

--- Problem section ---
{problem}
"""


def load_facets() -> dict[str, dict]:
    idx = json.loads(INDEX.read_text())
    return {r["slug"]: r for r in idx["recipes"]}


def load_tool_names() -> dict[str, dict]:
    return {t["slug"]: t for t in json.loads(TOOLS.read_text())["tools"]}


def problem_section(md: str) -> str:
    """Extract the ## Problem section body."""
    m = re.search(r"^## Problem\s*\n(.*?)(?=^## )", md, re.S | re.M)
    return m.group(1).strip() if m else ""


def answer_key(md: str) -> list[str]:
    """Tool slugs the recipe links to -- the curated correct answer."""
    return sorted(set(re.findall(r"catalog/tools/([a-z0-9][a-z0-9-]*)", md)))


def leak_terms(key: list[str], tool_meta: dict[str, dict]) -> list[str]:
    """Surface forms of each answer-key tool that must not appear in the question.

    Both the slug ("open-targets" -> "open targets") and the catalog title, minus
    generic suffixes that would cause false positives ("MCP", "Claude Skill").
    Single-word terms shorter than 4 chars are dropped: they match inside other words
    and would reject every candidate.
    """
    terms: set[str] = set()
    for slug in key:
        terms.add(slug.replace("-", " "))
        terms.add(slug)
        meta = tool_meta.get(slug)
        if not meta:
            continue
        title = meta["title"]
        title = re.sub(
            r"\s*\((Claude Skill|MCP|MCP server|Plugin|Connector)\)\s*$", "", title
        )
        title = re.sub(r"\s+(MCP server|MCP|Claude Skill|Skill|Plugin)$", "", title)
        terms.add(title)
    return sorted(t.lower() for t in terms if len(t) >= 4)


def find_leaks(question: str, terms: list[str]) -> list[str]:
    q = question.lower()
    return [t for t in terms if re.search(r"(?<![a-z0-9])" + re.escape(t) + r"(?![a-z0-9])", q)]


def claude(prompt: str, cwd: Path) -> str:
    """One headless Claude call with no customizations loaded at all.

    --safe-mode: the question writer must not have the composer plugin, or it may
    phrase questions in the plugin's own vocabulary and tilt the experiment.
    """
    cmd = [
        "claude", "-p",
        "--model", MODEL,
        "--safe-mode",
        "--strict-mcp-config",
        "--output-format", "json",
        prompt,
    ]
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=600)
    if r.returncode != 0:
        raise RuntimeError(f"claude exited {r.returncode}: {r.stderr[:400]}")
    return json.loads(r.stdout)["result"].strip()


def generate(slug: str, tool_meta: dict, facets: dict, scratch: Path,
             max_attempts: int) -> dict:
    md = (ITEMS / f"{slug}.md").read_text()
    problem = problem_section(md)
    if not problem:
        raise RuntimeError(f"{slug}: no ## Problem section")
    key = answer_key(md)
    terms = leak_terms(key, tool_meta)

    prompt = REWRITE_PROMPT.format(problem=problem)
    attempts = []
    for i in range(1, max_attempts + 1):
        extra = ""
        if attempts:
            extra = (
                "\n\nYour previous attempt leaked these forbidden names: "
                + ", ".join(sorted({l for _, ls in attempts for l in ls}))
                + ". Rewrite without them."
            )
        q = claude(prompt + extra, scratch)
        q = q.strip().strip('"')
        leaks = find_leaks(q, terms)
        attempts.append((q, leaks))
        if not leaks:
            f = facets.get(slug, {})
            return {
                "id": slug,
                "question": q,
                "tools": key,
                "problem_class": f.get("problem_class"),
                "complexity": f.get("complexity"),
                "evidence_level": f.get("evidence_level"),
                "availability": f.get("availability"),
                "compute_requirements": f.get("compute_requirements"),
                "attempts": i,
            }
    raise RuntimeError(
        f"{slug}: {max_attempts} attempts all leaked tool names. Last: {attempts[-1][1]}"
    )


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", type=Path, default=REPO / "validation" / "prompts.jsonl")
    ap.add_argument("--all", action="store_true", help="all 70 recipes, not just the pilot")
    ap.add_argument("--only", action="append", help="specific slug(s); repeatable")
    ap.add_argument("--max-attempts", type=int, default=4)
    ap.add_argument("--check", action="store_true",
                    help="re-run the leak check on an existing prompts file and exit")
    ap.add_argument("--force", action="store_true", help="regenerate rows already present")
    args = ap.parse_args()

    tool_meta = load_tool_names()
    facets = load_facets()

    if args.check:
        rows = [json.loads(l) for l in args.out.read_text().splitlines() if l.strip()]
        bad = 0
        for row in rows:
            leaks = find_leaks(row["question"], leak_terms(row["tools"], tool_meta))
            status = "LEAK " + ",".join(leaks) if leaks else "ok"
            if leaks:
                bad += 1
            print(f"{row['id']:48s} {status}")
        print(f"\n{len(rows)} prompts, {bad} leaking")
        return 1 if bad else 0

    if args.only:
        slugs = args.only
    elif args.all:
        slugs = sorted(p.stem for p in ITEMS.glob("*.md") if p.stem != "index")
    else:
        slugs = PILOT

    existing = {}
    if args.out.exists() and not args.force:
        for line in args.out.read_text().splitlines():
            if line.strip():
                row = json.loads(line)
                existing[row["id"]] = row

    scratch = Path("/tmp/composer-ab-prompts")
    scratch.mkdir(parents=True, exist_ok=True)

    rows: dict[str, dict] = dict(existing)
    for slug in slugs:
        if slug in rows:
            print(f"[skip]  {slug}")
            continue
        try:
            row = generate(slug, tool_meta, facets, scratch, args.max_attempts)
        except Exception as e:  # noqa: BLE001 - one bad recipe must not kill the batch
            print(f"[FAIL]  {slug}: {e}", file=sys.stderr)
            continue
        rows[slug] = row
        print(f"[ok]    {slug}  (key={len(row['tools'])}, attempts={row['attempts']})")
        print(f"        {row['question']}")
        # Write after every success so a crash never loses completed work.
        order = [s for s in slugs if s in rows] + [s for s in rows if s not in slugs]
        args.out.write_text(
            "".join(json.dumps(rows[s], ensure_ascii=False) + "\n"
                    for s in dict.fromkeys(order))
        )

    print(f"\n{len(rows)} prompts -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
