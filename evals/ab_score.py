#!/usr/bin/env python3
"""Step 3a of the composer A/B evaluation: count things. No judge, no opinions.

Everything here is matched against files already in the repo, so the numbers are
checkable by anyone: 378 real components in composer-tools.json, 70 recipes and 67
systems in composer-index.json, and each prompt's own answer key (the catalog tools its
recipe links to).

Reads evals/out/<id>/<arm>/<rep>/ and writes:
    evals/results.csv      one row per run
    evals/by_prompt.csv    one row per prompt, reps averaged, both arms side by side
    evals/summary.md       the readable comparison

Scoring is separate from running on purpose: expect to change how things are counted and
re-run this several times. It costs nothing.

Usage:
    python3 evals/ab_score.py
    python3 evals/ab_score.py --show-unknown     # list the invented-looking names
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import statistics
import sys
from collections import defaultdict
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
DATA = REPO / "composer" / "skills" / "compose" / "data"

# Phrases Claude Code emits when a tool call is refused for lack of approval. A denial is
# indistinguishable from a missing capability in the final prose, so it is counted
# explicitly -- if the two arms differ here, the comparison is contaminated.
DENIAL_PATTERNS = [
    "requested permissions",
    "permission to use",
    "user doesn't want to proceed",
    "tool use was rejected",
    "haven't granted it yet",
]

# Names that look like components but are not catalog entries and are not inventions.
NOT_A_COMPONENT = {
    "claude", "claude code", "claude desktop", "anthropic", "python", "bash", "r",
    "conda", "pip", "uv", "uvx", "npx", "docker", "git", "github", "jupyter",
    "websearch", "webfetch", "read", "write", "grep", "glob", "mcp", "json", "csv",
    "api", "cli", "sdk", "llm", "ai", "excel", "rest", "http", "url", "pdf", "sql",
}

DETERMINERS = {
    "this", "that", "these", "those", "the", "a", "an", "our", "your", "their", "its",
    "each", "both", "one", "another", "any", "no", "such", "same", "other", "first",
    "second", "third", "next", "custom", "single", "new", "existing",
}

GENERIC_SUFFIX = re.compile(
    r"\s*[\(\-]?\s*(Claude Skill|MCP server|MCP|Plugin|Connector|Skill)\s*\)?\s*$", re.I
)


def surface_forms(entry: dict) -> set[str]:
    """Ways a catalog entry's name could legitimately appear in prose."""
    forms = {entry["slug"], entry["slug"].replace("-", " ")}
    title = GENERIC_SUFFIX.sub("", entry["title"]).strip()
    if title:
        forms.add(title)
        # "Open Targets Platform" -> also match "Open Targets"
        words = title.split()
        if len(words) > 2:
            forms.add(" ".join(words[:2]))
    return {f.lower() for f in forms if len(f) >= 4}


def load_catalog() -> tuple[dict[str, set[str]], dict[str, set[str]], dict[str, set[str]]]:
    tools = json.loads((DATA / "composer-tools.json").read_text())["tools"]
    idx = json.loads((DATA / "composer-index.json").read_text())
    tool_forms = {t["slug"]: surface_forms(t) for t in tools}
    recipe_forms = {r["slug"]: surface_forms(r) for r in idx["recipes"]}
    system_forms = {s["slug"]: surface_forms(s) for s in idx.get("systems", [])}
    return tool_forms, recipe_forms, system_forms


def mentions(text: str, forms: dict[str, set[str]]) -> list[str]:
    low = text.lower()
    hit = []
    for slug, fs in forms.items():
        for f in fs:
            if re.search(r"(?<![a-z0-9])" + re.escape(f) + r"(?![a-z0-9])", low):
                hit.append(slug)
                break
    return sorted(hit)


def candidate_components(text: str) -> set[str]:
    """Names the answer explicitly presents as a Skill / MCP server / plugin / connector.

    Only this pattern. An earlier version also harvested every backticked identifier,
    which made the metric meaningless: it counted JSON field names (`acute_symptoms`),
    filenames (`records.jsonl`), env vars (`ANTHROPIC_API_KEY`) and ordinary
    bioinformatics binaries that are simply absent from a 378-entry catalog (`blastn`,
    `barrnap`) as "invented components". Requiring the component noun is what makes a hit
    mean "this was offered to the scientist as an installable thing that does not exist".
    """
    cands: set[str] = set()
    for m in re.finditer(
        r"\b([A-Z][A-Za-z0-9_.+-]*(?:[ -][A-Z0-9][A-Za-z0-9_.+-]*){0,2})\s+"
        r"(?:MCP(?:\s+server)?|[Ss]kill|[Pp]lugin|[Cc]onnector)\b", text
    ):
        cands.add(m.group(1).strip())
    return cands


def unknown_components(text: str, tool_forms: dict[str, set[str]],
                       recipe_forms: dict[str, set[str]],
                       system_forms: dict[str, set[str]]) -> list[str]:
    """Component-shaped names that are in no catalog -- candidate inventions.

    Heuristic, and deliberately reported as a list rather than only a count, because the
    list is the only way to tell a real invention from a matcher miss. Read it before
    trusting the number.
    """
    known: set[str] = set()
    for forms in (tool_forms, recipe_forms, system_forms):
        for fs in forms.values():
            known |= fs
    out = []
    for c in candidate_components(text):
        norm = c.lower().replace("_", " ").replace("-", " ").strip()
        flat = c.lower()
        # "This plugin", "The Skill" -- the regex caught a determiner, not a name.
        if norm.split()[0] in DETERMINERS or norm in DETERMINERS:
            continue
        if norm in NOT_A_COMPONENT or flat in NOT_A_COMPONENT:
            continue
        if flat in known or norm in known:
            continue
        # Substring in EITHER direction. "Open Targets MCP plugin" segments to the
        # candidate "Open Targets MCP", which contains the real catalog name; without the
        # reverse check a correctly-named tool is scored as an invention.
        if any(flat in k or norm in k or k in norm for k in known):
            continue
        out.append(c)
    return sorted(set(out))


def score_run(rundir: Path, row: dict, catalog) -> dict | None:
    meta_path = rundir / "meta.json"
    if not meta_path.exists():
        return None
    meta = json.loads(meta_path.read_text())
    answer = (rundir / "answer.md").read_text() if (rundir / "answer.md").exists() else ""
    stream_raw = ""
    if (rundir / "stream.jsonl").exists():
        stream_raw = (rundir / "stream.jsonl").read_text()

    tool_forms, recipe_forms, system_forms = catalog
    named_tools = mentions(answer, tool_forms)
    key = row.get("tools") or []
    key_hits = sorted(set(named_tools) & set(key))
    unknown = unknown_components(answer, tool_forms, recipe_forms, system_forms)

    low = stream_raw.lower()
    denials = sum(low.count(p) for p in DENIAL_PATTERNS)

    return {
        "id": row["id"],
        "arm": meta["arm"],
        "rep": meta["rep"],
        "status": "ok" if meta.get("returncode") == 0 and answer else "bad",
        "complexity": row.get("complexity"),
        "problem_class": row.get("problem_class"),
        "key_size": len(key),
        "key_hits": len(key_hits),
        "key_recall": round(len(key_hits) / len(key), 3) if key else None,
        "catalog_hits": len(named_tools),
        "unknown_components": len(unknown),
        "recipes_cited": len(mentions(answer, recipe_forms)),
        "systems_cited": len(mentions(answer, system_forms)),
        "has_evidence_label": int(bool(re.search(r"\b(Validated|Reported|Proposed)\b", answer))),
        "has_availability": int(bool(re.search(
            r"\b(Fully open|Subscription required|Institutional access|availability)\b",
            answer, re.I))),
        "has_compute": int(bool(re.search(
            r"\b(laptop|workstation|GPU|cluster|compute (?:tier|requirement))\b",
            answer, re.I))),
        "used_compose_skill": int(any("compose" in s for s in meta.get("skills_invoked", []))),
        "tool_calls": len(meta.get("tool_calls", [])),
        "permission_denials": denials,
        "cost_usd": meta.get("cost_usd"),
        "num_turns": meta.get("num_turns"),
        "wall_s": meta.get("wall_s"),
        "words": len(answer.split()),
        "_key_hit_slugs": ";".join(key_hits),
        "_unknown": ";".join(unknown),
    }


def mean(xs):
    xs = [x for x in xs if x is not None]
    return round(statistics.fmean(xs), 3) if xs else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--prompts", type=Path, default=REPO / "evals" / "prompts.jsonl")
    ap.add_argument("--out", type=Path, default=REPO / "evals" / "out")
    ap.add_argument("--evals", type=Path, default=REPO / "evals")
    ap.add_argument("--show-unknown", action="store_true")
    args = ap.parse_args()

    rows = {json.loads(l)["id"]: json.loads(l)
            for l in args.prompts.read_text().splitlines() if l.strip()}
    catalog = load_catalog()

    runs = []
    for pid, row in rows.items():
        for arm in ("with", "without"):
            for rep_dir in sorted((args.out / pid / arm).glob("*")) \
                    if (args.out / pid / arm).exists() else []:
                r = score_run(rep_dir, row, catalog)
                if r:
                    runs.append(r)
    if not runs:
        print("no scored runs found -- has ab_run.py been run?", file=sys.stderr)
        return 1

    fields = [k for k in runs[0] if not k.startswith("_")] + ["_key_hit_slugs", "_unknown"]
    with (args.evals / "results.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(runs)

    # Average reps within each (prompt, arm) before comparing, so one noisy prompt with
    # extra reps cannot dominate.
    by: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for r in runs:
        by[(r["id"], r["arm"])].append(r)

    METRICS = ["key_recall", "key_hits", "catalog_hits", "unknown_components",
               "recipes_cited", "has_evidence_label", "has_availability", "has_compute",
               "tool_calls", "permission_denials", "cost_usd", "num_turns", "words"]

    prompt_rows = []
    for pid, row in rows.items():
        rec = {"id": pid, "complexity": row.get("complexity"),
               "problem_class": row.get("problem_class"), "key_size": len(row.get("tools") or [])}
        for arm in ("with", "without"):
            rs = by.get((pid, arm), [])
            rec[f"n_{arm}"] = len(rs)
            for m in METRICS:
                rec[f"{m}_{arm}"] = mean([x[m] for x in rs])
            # spread across reps: is a gap bigger than the noise?
            vals = [x["key_recall"] for x in rs if x["key_recall"] is not None]
            rec[f"key_recall_spread_{arm}"] = (
                round(max(vals) - min(vals), 3) if len(vals) > 1 else 0.0)
        rec["compose_fired"] = mean([x["used_compose_skill"] for x in by.get((pid, "with"), [])])
        if rec.get("key_recall_with") is not None and rec.get("key_recall_without") is not None:
            rec["recall_delta"] = round(rec["key_recall_with"] - rec["key_recall_without"], 3)
        prompt_rows.append(rec)

    pfields = list(prompt_rows[0].keys())
    with (args.evals / "by_prompt.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=pfields)
        w.writeheader()
        w.writerows(prompt_rows)

    # ---- summary.md ----
    L = []
    L.append("# Composer plugin A/B — results\n")
    L.append(f"- runs scored: **{len(runs)}** "
             f"({sum(1 for r in runs if r['arm']=='with')} with / "
             f"{sum(1 for r in runs if r['arm']=='without')} without)")
    L.append(f"- prompts: **{len(prompt_rows)}**")
    models = {json.loads((args.out / r['id'] / r['arm'] / str(r['rep']) / 'meta.json').read_text()).get('model') for r in runs[:5]}
    L.append(f"- model: {', '.join(sorted(m for m in models if m))}")
    bad = [r for r in runs if r["status"] != "ok"]
    if bad:
        L.append(f"- **{len(bad)} runs did not complete cleanly** — excluded nowhere, "
                 f"inspect them: {', '.join(sorted({r['id'] for r in bad}))}")

    fired = mean([r["used_compose_skill"] for r in runs if r["arm"] == "with"])
    L.append(f"- compose skill actually invoked in the *with* arm: **{fired}** "
             f"(must be ~1.0, else the plugin never fired and results are void)")
    dw = sum(r["permission_denials"] for r in runs if r["arm"] == "with")
    dwo = sum(r["permission_denials"] for r in runs if r["arm"] == "without")
    note = "(symmetric)"
    if abs(dw - dwo) > max(3, 0.3 * max(dw, dwo, 1)):
        handicapped = "with" if dw > dwo else "without"
        other = "without" if handicapped == "with" else "with"
        note = (f"— **asymmetric**: the `{handicapped}` arm was denied more tool calls, so it "
                f"is handicapped. Read any `{handicapped}` win as a lower bound, and treat a "
                f"`{other}` win as possibly an artefact of the denials rather than a result.")
    L.append(f"- permission denials: with={dw}, without={dwo} {note}")

    L.append("\n## Per-arm means\n")
    L.append("| metric | with plugin | without plugin |")
    L.append("|---|---|---|")
    for m in METRICS:
        a = mean([r[m] for r in runs if r["arm"] == "with"])
        b = mean([r[m] for r in runs if r["arm"] == "without"])
        L.append(f"| {m} | {a} | {b} |")

    L.append("\n## Win / tie / loss on answer-key recall\n")
    # Only prompts with at least one run in BOTH arms are comparable. Counting an unrun
    # prompt as a tie would silently inflate the tie count and understate the effect.
    scored = [r for r in prompt_rows if r["n_with"] and r["n_without"]]
    unrun = [r for r in prompt_rows if not (r["n_with"] and r["n_without"])]
    wins = sum(1 for r in scored if (r.get("recall_delta") or 0) > 0)
    losses = sum(1 for r in scored if (r.get("recall_delta") or 0) < 0)
    ties = len(scored) - wins - losses
    L.append(f"**with plugin won {wins}, tied {ties}, lost {losses}** "
             f"of {len(scored)} comparable prompts.\n")
    if unrun:
        L.append(f"*{len(unrun)} prompt(s) not counted — missing runs in one or both arms: "
                 f"{', '.join('`'+r['id']+'`' for r in unrun)}*\n")
    L.append("Recall = fraction of the tools that prompt's curated recipe links to that "
             "the answer actually named.\n")

    L.append("| prompt | key | recall with | recall without | delta | spread with/without | unknown with/without |")
    L.append("|---|---|---|---|---|---|---|")
    for r in sorted(scored, key=lambda x: -(x.get("recall_delta") or 0)):
        L.append(f"| `{r['id']}` | {r['key_size']} | {r.get('key_recall_with')} | "
                 f"{r.get('key_recall_without')} | {r.get('recall_delta')} | "
                 f"{r.get('key_recall_spread_with')}/{r.get('key_recall_spread_without')} | "
                 f"{r.get('unknown_components_with')}/{r.get('unknown_components_without')} |")

    L.append("\n### Read the spread column before believing a delta\n")
    L.append("`spread` is max-minus-min recall across reps within one arm. Where spread "
             "is as large as the delta, that prompt shows run-to-run noise, not an effect.\n")

    L.append("\n## Sliced by complexity\n")
    L.append("| complexity | n | recall with | recall without |")
    L.append("|---|---|---|---|")
    for cx in sorted({r["complexity"] for r in prompt_rows if r["complexity"]}):
        sub = [r for r in prompt_rows if r["complexity"] == cx]
        L.append(f"| {cx} | {len(sub)} | {mean([r.get('key_recall_with') for r in sub])} | "
                 f"{mean([r.get('key_recall_without') for r in sub])} |")

    L.append("\n## Sliced by problem class\n")
    L.append("| problem class | n | recall with | recall without |")
    L.append("|---|---|---|---|")
    for pc in sorted({r["problem_class"] for r in prompt_rows if r["problem_class"]}):
        sub = [r for r in prompt_rows if r["problem_class"] == pc]
        L.append(f"| {pc} | {len(sub)} | {mean([r.get('key_recall_with') for r in sub])} | "
                 f"{mean([r.get('key_recall_without') for r in sub])} |")

    tc = sum(r["cost_usd"] or 0 for r in runs)
    L.append(f"\n## Cost\n\ntotal **${tc:.2f}** across {len(runs)} runs "
             f"(with=${sum(r['cost_usd'] or 0 for r in runs if r['arm']=='with'):.2f}, "
             f"without=${sum(r['cost_usd'] or 0 for r in runs if r['arm']=='without'):.2f})\n")

    L.append("\n## Caveats baked into these numbers\n")
    L.append("- `unknown_components` is a heuristic (component-shaped names absent from all "
             "three catalogs). Read the `_unknown` column of results.csv before quoting it; "
             "a matcher miss looks identical to an invention.")
    L.append("- Recall credits naming a tool, not using it correctly. A wrong recommendation "
             "that happens to name the right tool still scores.")
    L.append(f"- n={len(prompt_rows)} prompts. Report the rows, not a confidence interval.")

    (args.evals / "summary.md").write_text("\n".join(L) + "\n")

    print("\n".join(L[:40]))
    print(f"\nwrote results.csv, by_prompt.csv, summary.md to {args.evals}")

    if args.show_unknown:
        print("\n--- unknown (possibly invented) components ---")
        for r in runs:
            if r["_unknown"]:
                print(f"{r['id']:44s} {r['arm']:8s} rep{r['rep']}  {r['_unknown']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
