#!/usr/bin/env python3
"""Repair recipes in a validate -> fix -> re-validate feedback loop.

Pipeline per recipe:

    1. validate_recipes.py finds the problems  (the objective signal)
    2. claude -p edits the recipe .md to fix them  (the repair)
    3. validate_recipes.py --only <slug> re-checks  (the feedback)
    4. still failing? loop with the new findings, up to --max-attempts

Nothing is committed. Fixed files are left in the working tree for you to review
with `git diff` before committing.

Examples:
    python3 scripts/repair_agent.py --dry-run                 # just show what's broken
    python3 scripts/repair_agent.py --slug estimate-pk-properties
    python3 scripts/repair_agent.py --max-recipes 10 --max-attempts 3
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ITEMS_DIR = REPO_ROOT / "recipes" / "items"
VALIDATOR = REPO_ROOT / "scripts" / "validate_recipes.py"
PROMPT_FILE = REPO_ROOT / "scripts" / "repair_prompt.md"
REPORT_PATH = REPO_ROOT / "report.json"

ALLOWED_TOOLS = "Read Edit Grep Glob WebSearch WebFetch"


# --------------------------------------------------------------------------- #
# Validation
# --------------------------------------------------------------------------- #
def validate_all() -> dict:
    """Run the validator over all recipes, writing report.json, and return it."""
    subprocess.run(
        [sys.executable, str(VALIDATOR), "--out", str(REPORT_PATH)],
        cwd=REPO_ROOT, check=False,
    )
    return json.loads(REPORT_PATH.read_text(encoding="utf-8"))


def validate_one(slug: str) -> dict:
    """Validate a single recipe, returning its result dict."""
    proc = subprocess.run(
        [sys.executable, str(VALIDATOR), "--only", slug],
        cwd=REPO_ROOT, capture_output=True, text=True, check=False,
    )
    report = json.loads(proc.stdout)
    return report["recipes"][0]


def is_clean(result: dict) -> bool:
    return result["passed"]


# --------------------------------------------------------------------------- #
# Prompt construction
# --------------------------------------------------------------------------- #
def render_findings(result: dict) -> str:
    """A human-readable findings block appended to the repair prompt."""
    lines = [f"- Recipe file: `recipes/items/{result['slug']}.md`"]
    if result["missing_fields"]:
        lines.append(f"- Missing frontmatter fields: {result['missing_fields']}")
    if result["broken_links"]:
        lines.append("- Broken links (dead — must fix):")
        for b in result["broken_links"]:
            lines.append(f"    - {b['url']}  ({b['detail']})")
    if result["blocked_links"]:
        lines.append("- Blocked links (verify before touching — usually valid):")
        for b in result["blocked_links"]:
            lines.append(f"    - {b['url']}  ({b['detail']})")
    if not result["fetch_ok"]:
        lines.append(f"- Source did not parse: {result['fetch_detail']}")
    return "\n".join(lines)


def build_prompt(result: dict, include_blocked: bool) -> str:
    base = PROMPT_FILE.read_text(encoding="utf-8")
    today = date.today().isoformat()
    findings = render_findings(result)
    blocked_note = (
        "" if include_blocked else
        "\nOnly the broken links and missing fields above are required fixes this "
        "run; leave verified-valid blocked links as they are.\n"
    )
    return (
        f"{base}\n\n---\n\n## This repair\n\n"
        f"Today's date is {today} (use it for `last_verified`).\n\n"
        f"Findings for this recipe:\n\n{findings}\n{blocked_note}"
    )


# --------------------------------------------------------------------------- #
# Agent invocation
# --------------------------------------------------------------------------- #
def run_agent(prompt: str, model: str, max_turns: int, timeout: int) -> dict:
    """Invoke `claude -p` headless. Returns a small status dict."""
    cmd = [
        "claude", "-p", prompt,
        "--allowedTools", ALLOWED_TOOLS,
        "--permission-mode", "acceptEdits",
        "--output-format", "json",
        "--max-turns", str(max_turns),
        "--model", model,
    ]
    try:
        proc = subprocess.run(
            cmd, cwd=REPO_ROOT, capture_output=True, text=True, timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return {"ok": False, "summary": "agent timed out", "cost": None, "turns": None}

    if proc.returncode != 0:
        detail = (proc.stderr or proc.stdout or "").strip().splitlines()
        return {"ok": False, "summary": f"agent exited {proc.returncode}: "
                f"{detail[-1] if detail else 'no output'}", "cost": None, "turns": None}

    try:
        payload = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return {"ok": True, "summary": proc.stdout.strip()[-200:], "cost": None, "turns": None}

    result_text = payload.get("result", "") or ""
    summary_line = next(
        (ln for ln in reversed(result_text.splitlines()) if ln.startswith("SUMMARY:")),
        result_text.strip().splitlines()[-1] if result_text.strip() else "(no summary)",
    )
    return {
        "ok": not payload.get("is_error", False),
        "summary": summary_line,
        "cost": payload.get("total_cost_usd"),
        "turns": payload.get("num_turns"),
    }


# --------------------------------------------------------------------------- #
# Per-recipe repair loop
# --------------------------------------------------------------------------- #
def file_signature(path: Path) -> int:
    return hash(path.read_text(encoding="utf-8")) if path.exists() else 0


def repair_recipe(result: dict, args) -> dict:
    """Run the fix/re-validate loop for one recipe. Returns an outcome record."""
    slug = result["slug"]
    path = ITEMS_DIR / f"{slug}.md"
    print(f"\n=== {slug} ===")
    print(render_findings(result))

    attempts = 0
    for attempt in range(1, args.max_attempts + 1):
        attempts = attempt
        before = file_signature(path)
        prompt = build_prompt(result, args.include_blocked)

        print(f"  attempt {attempt}/{args.max_attempts}: invoking agent…")
        status = run_agent(prompt, args.model, args.max_turns, args.timeout)
        meta = []
        if status["turns"] is not None:
            meta.append(f"{status['turns']} turns")
        if status["cost"] is not None:
            meta.append(f"${status['cost']:.3f}")
        print(f"    agent: {status['summary']}" + (f"  [{', '.join(meta)}]" if meta else ""))

        if not status["ok"]:
            return {"slug": slug, "fixed": False, "attempts": attempt,
                    "note": status["summary"]}

        result = validate_one(slug)
        if is_clean(result):
            print(f"    ✓ re-validated clean")
            return {"slug": slug, "fixed": True, "attempts": attempt, "note": "clean"}

        print(f"    still failing: "
              f"{[b['detail'] for b in result['broken_links']]} "
              f"missing={result['missing_fields']}")

        if file_signature(path) == before:
            return {"slug": slug, "fixed": False, "attempts": attempt,
                    "note": "no change made — stopping"}

    return {"slug": slug, "fixed": False, "attempts": attempts,
            "note": "exhausted attempts"}


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def select_targets(report: dict, args) -> list[dict]:
    targets = []
    for r in report["recipes"]:
        if args.slug:
            if r["slug"] == args.slug:
                targets.append(r)
            continue
        if not r["passed"]:
            targets.append(r)
        elif args.include_blocked and r["blocked_links"]:
            targets.append(r)
    if args.slug and not targets:
        sys.exit(f"Recipe '{args.slug}' not found in report.")
    if args.max_recipes:
        targets = targets[: args.max_recipes]
    return targets


def main() -> int:
    ap = argparse.ArgumentParser(description="Repair recipes in a feedback loop")
    ap.add_argument("--slug", help="Repair only this recipe")
    ap.add_argument("--max-recipes", type=int, default=None,
                    help="Cap how many failing recipes to attempt this run")
    ap.add_argument("--max-attempts", type=int, default=3,
                    help="Fix/re-validate rounds per recipe (default 3)")
    ap.add_argument("--include-blocked", action="store_true",
                    help="Also target recipes whose only issue is blocked (403/429) links")
    ap.add_argument("--dry-run", action="store_true",
                    help="Validate and list problems; do not call the agent")
    ap.add_argument("--model", default="opus", help="Model for the agent (default: opus)")
    ap.add_argument("--max-turns", type=int, default=30, help="Agent turn cap per attempt")
    ap.add_argument("--timeout", type=int, default=900, help="Per-attempt timeout (s)")
    args = ap.parse_args()

    started = time.monotonic()
    print("Validating all recipes…")
    report = validate_all()
    s = report["summary"]
    print(f"  {s['passed']}/{s['total']} passed, {s['failed']} failed")

    targets = select_targets(report, args)
    if not targets:
        print("Nothing to repair. 🎉")
        return 0

    print(f"\nRepair targets ({len(targets)}): "
          f"{', '.join(t['slug'] for t in targets)}")

    if args.dry_run:
        for t in targets:
            print(f"\n=== {t['slug']} ===")
            print(render_findings(t))
        print("\n(dry run — no changes made)")
        return 0

    outcomes = [repair_recipe(t, args) for t in targets]

    print("\nRe-validating all recipes…")
    final = validate_all()
    fs = final["summary"]

    print("\n" + "=" * 60)
    print("REPAIR SUMMARY")
    print("=" * 60)
    for o in outcomes:
        mark = "✓ fixed" if o["fixed"] else "✗ still failing"
        print(f"  {mark:16} {o['slug']}  ({o['attempts']} attempt(s); {o['note']})")
    fixed = sum(1 for o in outcomes if o["fixed"])
    print("-" * 60)
    print(f"  fixed {fixed}/{len(outcomes)} targeted this run")
    print(f"  report.json now: {fs['passed']}/{fs['total']} passed, {fs['failed']} failed")
    print(f"  elapsed {time.monotonic() - started:.0f}s")
    print("\nReview changes with:  git diff recipes/items/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
