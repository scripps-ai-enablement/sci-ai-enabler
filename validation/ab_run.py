#!/usr/bin/env python3
"""Step 2 of the composer A/B evaluation: run every prompt with and without the plugin.

The two arms differ by exactly one flag, ``--plugin-dir``. Everything else is held
constant: same model, same cwd layout, same permission allowlist. Both run from a
throwaway scratch directory so neither can see this repo's .claude/skills (150 skills)
or its CLAUDE.md.

Four flag behaviours were verified by experiment and matter here (see validation/PLAN.md):

  1. ``claude -p`` loads no plugins by default -- without --setting-sources/--plugin-dir
     both arms would secretly be the same bare Claude.
  2. ``--safe-mode`` cancels ``--plugin-dir``, so the treatment arm cannot use safe mode.
  3. ``--setting-sources project`` from a scratch cwd is what suppresses ~/.claude/skills.
  4. Headless tool calls can be silently denied, which looks identical to a missing
     capability in the final text -- so both arms get the same --allowedTools list and
     every denial is counted at score time.

Output is raw and per-run, because scoring is deliberately separate from running: you
will change how you count things several times, and re-scoring must be free.

Usage:
    python3 validation/ab_run.py --limit 2 --reps 1        # smoke test
    python3 validation/ab_run.py                           # the pilot (10 x 2 x 3)
    python3 validation/ab_run.py --jobs 6                   # more parallelism
    python3 validation/ab_run.py --dry-run                  # print the commands only
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
PLUGIN = REPO / "composer"
MODEL = "claude-sonnet-5"

# Identical in both arms. Read-only: the eval measures what gets recommended, not what
# gets installed. Anything outside this list is denied in headless mode, which is fine
# as long as it is denied symmetrically -- ab_score.py reports denials per arm so an
# asymmetry shows up as contamination rather than as a result.
#
# Comma-separated, NOT space-separated: --allowedTools is variadic, so a space-separated
# list swallows whatever follows it on the command line.
#
# The read-only Bash patterns are here because of a measured asymmetry: with only
# Read/Glob/Grep/Web*, the *with* arm hit 4 permission denials per run (the compose skill
# shells out to inspect its bundled index) while the *without* arm hit 0. Denials
# concentrated in one arm handicap that arm, so leaving it would bias the experiment
# against the plugin. These patterns cover file inspection without permitting installs or
# network writes, and apply to both arms identically.
ALLOWED_TOOLS = ",".join([
    "Read", "Glob", "Grep", "WebSearch", "WebFetch",
    "Bash(ls *)", "Bash(cat *)", "Bash(head *)", "Bash(tail *)",
    "Bash(find *)", "Bash(wc *)", "Bash(grep *)", "Bash(file *)", "Bash(echo *)",
])

ARMS = ("with", "without")

# Appended identically to both arms. A headless session has nobody to answer a follow-up
# question, so a prompt that invites one produces a one-turn "please paste your SMILES"
# and no measurable signal -- 4 of the first 4 smoke-test runs on one prompt did exactly
# that. This converts those into answers. It is the same text in both arms, so it cannot
# favour either one; it is recorded here rather than folded into the prompts file so the
# questions stay as generated.
SINGLE_SHOT_SUFFIX = (
    "\n\n(This is a single-shot request — I cannot answer follow-up questions. If you "
    "need a specific input I have not given you, assume a concrete realistic example, "
    "state the assumption you made, and go on to give the full recommendation.)"
)


def build_cmd(arm: str, model: str) -> list[str]:
    """Command for one arm. The prompt is fed on stdin, never as a positional argument.

    Both --allowedTools and --add-dir are variadic, so a trailing positional prompt gets
    consumed as another value and claude exits with "Input must be provided either
    through stdin or as a prompt argument". stdin avoids the ambiguity entirely.
    """
    cmd = [
        "claude", "-p",
        "--model", model,
        "--strict-mcp-config",
        "--setting-sources", "project",
        "--output-format", "stream-json",
        "--verbose",
        "--allowedTools", ALLOWED_TOOLS,
    ]
    if arm == "with":
        cmd += ["--plugin-dir", str(PLUGIN)]
        # The plugin's own bundled index lives under the plugin dir, outside the scratch
        # cwd. Without this the skill cannot read the data files it ships with, which
        # would handicap the arm for a reason unrelated to the plugin's quality.
        cmd += ["--add-dir", str(PLUGIN)]
    return cmd


def parse_stream(path: Path) -> dict:
    """Pull the summary facts out of a saved stream-json file."""
    out = {
        "result_text": "",
        "cost_usd": None,
        "num_turns": None,
        "duration_ms": None,
        "is_error": None,
        "tool_calls": [],
        "skills_invoked": [],
        "subtype": None,
    }
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        t = ev.get("type")
        if t == "assistant":
            for block in ev.get("message", {}).get("content", []):
                if block.get("type") == "tool_use":
                    name = block.get("name", "")
                    out["tool_calls"].append(name)
                    if name == "Skill":
                        skill = (block.get("input") or {}).get("skill")
                        if skill:
                            out["skills_invoked"].append(skill)
        elif t == "result":
            out["result_text"] = ev.get("result") or ""
            out["cost_usd"] = ev.get("total_cost_usd")
            out["num_turns"] = ev.get("num_turns")
            out["duration_ms"] = ev.get("duration_ms")
            out["is_error"] = ev.get("is_error")
            out["subtype"] = ev.get("subtype")
    return out


def run_one(row: dict, arm: str, rep: int, outdir: Path, model: str,
            dry_run: bool) -> dict:
    dest = outdir / row["id"] / arm / str(rep)
    stream = dest / "stream.jsonl"
    meta_path = dest / "meta.json"

    if meta_path.exists():
        return {"id": row["id"], "arm": arm, "rep": rep, "status": "skipped"}

    cmd = build_cmd(arm, model)
    if dry_run:
        print(f"[{row['id']}/{arm}/{rep}] {' '.join(cmd)} <<< <prompt>")
        return {"id": row["id"], "arm": arm, "rep": rep, "status": "dry-run"}

    dest.mkdir(parents=True, exist_ok=True)
    # A fresh cwd per run: outside the repo (so no skill/CLAUDE.md discovery) and
    # unique (so concurrent runs cannot collide on files they write).
    scratch = Path(tempfile.mkdtemp(prefix=f"ab-{row['id']}-{arm}-{rep}-"))
    started = time.time()
    try:
        proc = subprocess.run(cmd, cwd=scratch,
                              input=row["question"] + SINGLE_SHOT_SUFFIX,
                              capture_output=True, text=True, timeout=1800)
        stream.write_text(proc.stdout)
        if proc.stderr.strip():
            (dest / "stderr.txt").write_text(proc.stderr)
        parsed = parse_stream(stream)
        (dest / "answer.md").write_text(parsed["result_text"])
        meta = {
            "id": row["id"],
            "arm": arm,
            "rep": rep,
            "model": model,
            "cmd": cmd,
            "returncode": proc.returncode,
            "wall_s": round(time.time() - started, 1),
            "cost_usd": parsed["cost_usd"],
            "num_turns": parsed["num_turns"],
            "duration_ms": parsed["duration_ms"],
            "is_error": parsed["is_error"],
            "subtype": parsed["subtype"],
            "tool_calls": parsed["tool_calls"],
            "skills_invoked": parsed["skills_invoked"],
            "answer_chars": len(parsed["result_text"]),
        }
        meta_path.write_text(json.dumps(meta, indent=2))
        status = "ok" if proc.returncode == 0 and parsed["result_text"] else "empty"
        return {**{k: meta[k] for k in ("id", "arm", "rep", "cost_usd", "wall_s")},
                "status": status, "skills": parsed["skills_invoked"]}
    except subprocess.TimeoutExpired:
        (dest / "TIMEOUT").write_text("timed out after 1800s\n")
        return {"id": row["id"], "arm": arm, "rep": rep, "status": "timeout"}
    except Exception as e:  # noqa: BLE001 - one bad run must not kill the sweep
        (dest / "ERROR.txt").write_text(repr(e))
        return {"id": row["id"], "arm": arm, "rep": rep, "status": f"error: {e}"}
    finally:
        shutil.rmtree(scratch, ignore_errors=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--prompts", type=Path, default=REPO / "validation" / "prompts.jsonl")
    ap.add_argument("--out", type=Path, default=REPO / "validation" / "out")
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--limit", type=int, help="only the first N prompts")
    ap.add_argument("--only", action="append", help="specific prompt id(s); repeatable")
    ap.add_argument("--jobs", type=int, default=4, help="concurrent sessions")
    ap.add_argument("--model", default=MODEL)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    rows = [json.loads(l) for l in args.prompts.read_text().splitlines() if l.strip()]
    if args.only:
        rows = [r for r in rows if r["id"] in set(args.only)]
    if args.limit:
        rows = rows[: args.limit]
    if not rows:
        print("no prompts selected", file=sys.stderr)
        return 1

    jobs = [(r, arm, rep) for r in rows for arm in ARMS
            for rep in range(1, args.reps + 1)]
    print(f"{len(rows)} prompts x {len(ARMS)} arms x {args.reps} reps "
          f"= {len(jobs)} sessions, {args.jobs} at a time, model={args.model}")

    done = 0
    total_cost = 0.0
    counts: dict[str, int] = {}
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futs = {pool.submit(run_one, r, a, p, args.out, args.model, args.dry_run):
                (r["id"], a, p) for r, a, p in jobs}
        for fut in as_completed(futs):
            res = fut.result()
            done += 1
            counts[res["status"]] = counts.get(res["status"], 0) + 1
            if res.get("cost_usd"):
                total_cost += res["cost_usd"]
            skills = ",".join(res.get("skills") or []) or "-"
            cost = f"${res['cost_usd']:.3f}" if res.get("cost_usd") else "-"
            print(f"[{done}/{len(jobs)}] {res['id']:46s} {res['arm']:8s} rep{res['rep']} "
                  f"{res['status']:8s} {cost:>8s}  skills={skills}", flush=True)

    print(f"\ndone: {counts}")
    print(f"total cost: ${total_cost:.2f}")
    print(f"output: {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
