#!/usr/bin/env python3
"""Step 3b of the composer A/B evaluation: blinded pairwise judge.

Counting (ab_score.py) tells you *that* there is a gap. It cannot tell you that an answer
confidently recommended something retired, or that it was well organised but useless. That
needs a reader.

Three protections, all of which matter:

  - the judge runs under --safe-mode, so it does not have the composer plugin itself and
    cannot reward output that looks like its own tooling;
  - answers are labelled only A and B, and which arm is A is decided by a hash of the
    prompt id, so it is blinded but reproducible;
  - each pair is judged twice, in both orders. If the verdict flips, position bias
    dominated and the pair is reported as UNSTABLE rather than counted.

Verdicts come back through --json-schema, so they tally without parsing prose.

Usage:
    python3 evals/ab_judge.py                 # judge rep 1 of every prompt
    python3 evals/ab_judge.py --rep 2
    python3 evals/ab_judge.py --model claude-opus-5     # re-check with a stronger judge
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
MODEL = "claude-sonnet-5"

SCHEMA = {
    "type": "object",
    "properties": {
        "more_useful": {"enum": ["A", "B", "tie"]},
        "better_grounded": {"enum": ["A", "B", "tie"]},
        "more_specific_tooling": {"enum": ["A", "B", "tie"]},
        "unsupported_claims": {"enum": ["A", "B", "neither", "both"]},
        "why": {"type": "string"},
    },
    "required": ["more_useful", "better_grounded", "more_specific_tooling",
                 "unsupported_claims", "why"],
    "additionalProperties": False,
}

TEMPLATE = """\
A life scientist asked this question:

<question>
{question}
</question>

Two assistants answered. Judge them.

<answer_A>
{a}
</answer_A>

<answer_B>
{b}
</answer_B>

Judge on these axes, independently:

- more_useful: which answer would get this scientist further, faster?
- better_grounded: which makes fewer claims it cannot support? Naming a specific real
  resource is grounded; vague gestures at "various databases" are not; a confidently
  named resource that does not exist is the worst case.
- more_specific_tooling: which names concrete, checkable tooling rather than generic advice?
- unsupported_claims: which answer contains more assertions presented as fact without a
  source? "neither" if both are clean, "both" if both are bad.

A longer or better-formatted answer is not automatically better. Prefer the one a working
scientist could actually act on. Use "tie" when they are genuinely comparable — do not
manufacture a difference.

Answer only through the structured output.
"""


def read_answer(out: Path, pid: str, arm: str, rep: int) -> str | None:
    p = out / pid / arm / str(rep) / "answer.md"
    if not p.exists():
        return None
    t = p.read_text().strip()
    return t or None


def a_is_with(pid: str) -> bool:
    """Deterministic blinding: stable across re-runs, unguessable per prompt."""
    return hashlib.sha256(pid.encode()).digest()[0] % 2 == 0


def judge_once(question: str, a: str, b: str, model: str, cwd: Path) -> dict:
    cmd = [
        "claude", "-p",
        "--model", model,
        "--safe-mode",
        "--strict-mcp-config",
        "--output-format", "json",
        "--json-schema", json.dumps(SCHEMA),
        TEMPLATE.format(question=question, a=a, b=b),
    ]
    r = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=900)
    if r.returncode != 0:
        raise RuntimeError(f"judge exited {r.returncode}: {r.stderr[:300]}")
    payload = json.loads(r.stdout)
    res = payload.get("result")
    return json.loads(res) if isinstance(res, str) else res


def resolve(label: str, a_with: bool) -> str:
    """Map a judge's A/B answer back to with/without."""
    if label == "A":
        return "with" if a_with else "without"
    if label == "B":
        return "without" if a_with else "with"
    return label


def judge_pair(row: dict, out: Path, rep: int, model: str, scratch: Path) -> dict | None:
    pid = row["id"]
    w = read_answer(out, pid, "with", rep)
    wo = read_answer(out, pid, "without", rep)
    if not w or not wo:
        return {"id": pid, "status": "missing-answer"}

    a_with = a_is_with(pid)
    first_a, first_b = (w, wo) if a_with else (wo, w)

    try:
        v1 = judge_once(row["question"], first_a, first_b, model, scratch)
        # Same pair, positions swapped. A is now the other arm.
        v2 = judge_once(row["question"], first_b, first_a, model, scratch)
    except Exception as e:  # noqa: BLE001
        return {"id": pid, "status": f"error: {e}"}

    rec = {"id": pid, "status": "ok", "a_was": "with" if a_with else "without"}
    for axis in ("more_useful", "better_grounded", "more_specific_tooling"):
        r1 = resolve(v1[axis], a_with)
        r2 = resolve(v2[axis], not a_with)   # swapped order flips the mapping
        rec[axis] = r1 if r1 == r2 else "UNSTABLE"
        rec[f"{axis}_order1"] = r1
        rec[f"{axis}_order2"] = r2
    u1, u2 = v1["unsupported_claims"], v2["unsupported_claims"]
    rec["unsupported_claims"] = (
        resolve(u1, a_with) if u1 in ("A", "B") else u1
    )
    rec["why_order1"] = v1["why"]
    rec["why_order2"] = v2["why"]
    return rec


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--prompts", type=Path, default=REPO / "evals" / "prompts.jsonl")
    ap.add_argument("--out", type=Path, default=REPO / "evals" / "out")
    ap.add_argument("--rep", type=int, default=1, help="which repetition to judge")
    ap.add_argument("--model", default=MODEL)
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--csv", type=Path, default=REPO / "evals" / "judge.csv")
    args = ap.parse_args()

    rows = [json.loads(l) for l in args.prompts.read_text().splitlines() if l.strip()]
    scratch = Path("/tmp/composer-ab-judge")
    scratch.mkdir(parents=True, exist_ok=True)

    print(f"judging {len(rows)} pairs (rep {args.rep}) with {args.model}, both orders")
    recs = []
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futs = {pool.submit(judge_pair, r, args.out, args.rep, args.model, scratch): r["id"]
                for r in rows}
        for fut in as_completed(futs):
            rec = fut.result()
            if rec:
                recs.append(rec)
                print(f"  {rec['id']:46s} {rec['status']:16s} "
                      f"useful={rec.get('more_useful','-')} "
                      f"grounded={rec.get('better_grounded','-')}", flush=True)

    if not recs:
        print("nothing judged", file=sys.stderr)
        return 1

    fields = sorted({k for r in recs for k in r})
    fields = [f for f in ("id", "status", "a_was", "more_useful", "better_grounded",
                          "more_specific_tooling", "unsupported_claims") if f in fields] + \
             [f for f in fields if f not in ("id", "status", "a_was", "more_useful",
                                             "better_grounded", "more_specific_tooling",
                                             "unsupported_claims")]
    with args.csv.open("w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=fields)
        wr.writeheader()
        wr.writerows(recs)

    ok = [r for r in recs if r["status"] == "ok"]
    print(f"\n--- tally over {len(ok)} judged pairs ---")
    for axis in ("more_useful", "better_grounded", "more_specific_tooling"):
        c = {k: sum(1 for r in ok if r.get(axis) == k)
             for k in ("with", "without", "tie", "UNSTABLE")}
        print(f"{axis:24s} with={c['with']}  without={c['without']}  "
              f"tie={c['tie']}  unstable={c['UNSTABLE']}")
    print("\nUNSTABLE = verdict flipped when A and B were swapped, i.e. position bias "
          "rather than a real preference. Do not count those as either arm winning.")
    print(f"wrote {args.csv}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
