#!/usr/bin/env python3
"""Fold recipe-dependency smoke verdicts into `index/recipe-dependencies.json`.

The smoke job executes two kinds of target: catalog tool pages (which the
Verifier agent stamps with `verification:` / `verified_on:` badges) and recipe
dependencies — libraries a recipe's own script pip-installs, which have no
catalog page and therefore nothing to stamp.

This script keeps those two lanes separate. It extracts only the `source:
"recipe"` results and accumulates them into a committed JSON keyed by package, so
that:

  - `scripts/build_index.py` can render the executed verdict on the library index;
  - the recipes curator can fix a yanked pin or a wrong import module
    (`RECIPE_AGENT.md`, "Rules for the `## Dependencies` block");
  - the Verifier agent stays in its lane — it owns catalog badges, not recipes.

Accumulates rather than replaces: a run only smoke-tests a slice of the batch, so
a package absent from this run keeps its previous verdict instead of reverting to
unknown. Pure standard library.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# Every pinned spec in the command, not just the first. A recipe installing
# `pip install A==1 B==2 C==3` executes and imports all three in one target, so
# one verdict covers all three — recording only A left B and C looking unchecked
# on the library index while they had in fact been tested.
SPEC = re.compile(r"([A-Za-z0-9._\-]+)(?:\[[A-Za-z0-9,._\-]+\])?==[A-Za-z0-9._!*+\-]+")


def packages_of(install_cmd: str) -> list[str]:
    """Base names of every `==`-pinned package in a pip command, in order."""
    if not install_cmd or "pip install" not in install_cmd:
        return []
    tail = install_cmd.split("pip install", 1)[1]
    seen: list[str] = []
    for name in SPEC.findall(tail):
        if name not in seen:
            seen.append(name)
    return seen


def fold(results: list[dict], previous: dict, today: str) -> dict:
    """Merge this run's recipe-dependency results over the previous record set."""
    by_package = {r["package"]: dict(r) for r in previous.get("results", [])}
    for r in results:
        if r.get("source") != "recipe":
            continue  # catalog tool pages are the Verifier agent's lane
        for pkg in packages_of(r.get("install_cmd", "")):
            by_package[pkg] = {
                "package": pkg,
                "recipe": r.get("slug", ""),
                "install_cmd": r.get("install_cmd", ""),
                "boot_cmd": r.get("boot_cmd") or "",
                "status": r.get("status", ""),
                "checked_on": today,
            }
    return {
        "version": 1,
        "generated": today,
        "results": [by_package[k] for k in sorted(by_package)],
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--results", required=True, type=Path,
                    help="smoke-results.json from the smoke job")
    ap.add_argument("--out", required=True, type=Path)
    args = ap.parse_args(argv)

    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    results: list[dict] = []
    if args.results.exists():
        try:
            results = json.loads(args.results.read_text(encoding="utf-8")).get("results", [])
        except json.JSONDecodeError as exc:
            print(f"record_dependency_verdicts: unreadable {args.results}: {exc}",
                  file=sys.stderr)

    previous: dict = {}
    if args.out.exists():
        try:
            previous = json.loads(args.out.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            previous = {}

    folded = fold(results, previous, today)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(folded, indent=2, ensure_ascii=False) + "\n",
                        encoding="utf-8")
    fresh = sum(1 for r in results if r.get("source") == "recipe")
    print(f"record_dependency_verdicts: {fresh} recipe verdict(s) this run, "
          f"{len(folded['results'])} tracked total -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
