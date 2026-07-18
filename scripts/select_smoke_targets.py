#!/usr/bin/env python3
"""Select the SAFE subset of catalog tools to smoke-test, deterministically.

This is the code-enforced safety gate for the verifier's quarantined smoke-test
job (see .github/workflows/verify.yml). It is intentionally NOT the model's job:
only targets this script emits are ever installed/booted, so the decision of
"what untrusted code may run" is auditable Python, not an LLM judgment.

A tool qualifies only if ALL hold:
  * tool_type is a Claude Skill or an MCP server (installable/bootable);
  * we can extract a public, no-auth install command (pip / uv / npx / npm);
  * NOTHING on the page trips the gate denylist (api key, token, subscription,
    institutional, credentialed, login/account, credits, wet-lab, paid, DUA,
    dbGaP, enterprise, waitlist, request access, ...).
Anything excluded here is NOT skipped by the verifier — it still gets the static
liveness/provenance/security checks; it just never has its code executed.

Ordering: unstamped entries first, then oldest `verified_on`, so bootstrap and
30-day maintenance both drain naturally. Emits a JSON batch (default: stdout).

Run: python3 scripts/select_smoke_targets.py --max 12 [--out batch.json]
Stdlib only.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TOOLS = REPO / "catalog" / "tools"

# tool_type values whose install is a runnable install+boot we can smoke-test.
SMOKE_TYPES = {"Claude Skill", "MCP server"}

# If any of these appears anywhere on the page (case-insensitive), the tool is
# gate-excluded from execution — it may need auth, cost money, or touch a lab.
# Conservative by design: over-exclusion is the safe direction.
GATE_DENY = [
    "api key", "api-key", "apikey", "access token", "auth token", "bearer",
    "subscription", "paid", "per experiment", "per-experiment", "credit",
    "institutional", "credentialed", "controlled-access", "controlled access",
    "dbgap", "data use agreement", "dua", "enterprise", "waitlist",
    "request access", "request-gated", "sign up", "sign-up", "signup",
    "log in", "login", "create an account", "account required", "register",
    "wet lab", "wet-lab", "oauth", "client secret", "license key",
]

# Extract a public install command we can hand to the smoke runner.
INSTALL_PATTERNS = [
    (re.compile(r"`(pip install [A-Za-z0-9_.\-\[\]=<>! ]+)`"), "pip"),
    (re.compile(r"`(uv tool install [A-Za-z0-9_.\-]+)`"), "uv"),
    (re.compile(r"`(uvx [A-Za-z0-9_.\-]+)`"), "uvx"),
    (re.compile(r"`(npx skills add [A-Za-z0-9_./\-]+)`"), "npx-skills"),
    (re.compile(r"`(npx -y [A-Za-z0-9_.@/\-]+)`"), "npx"),
]

# Optional boot check for MCP servers: a `claude mcp add ... -- <cmd>` line tells
# us the launch command; we only capture it, the runner decides how to probe.
MCP_BOOT = re.compile(r"claude mcp add[^`\n]*?--\s+([A-Za-z0-9_.\-]+(?:\s+[A-Za-z0-9_.\-]+)*)")


def parse_frontmatter(text: str) -> dict:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    fm = {}
    for line in text[3:end].splitlines():
        if ":" in line and not line.lstrip().startswith("#"):
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip()
    return fm


def select(max_n: int) -> list[dict]:
    candidates = []
    for path in sorted(TOOLS.glob("*.md")):
        if path.name == "index.md":
            continue
        text = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        if fm.get("tool_type") not in SMOKE_TYPES:
            continue
        low = text.lower()
        if any(term in low for term in GATE_DENY):
            continue
        install_cmd = boot_cmd = None
        for rx, kind in INSTALL_PATTERNS:
            m = rx.search(text)
            if m:
                install_cmd, install_kind = m.group(1), kind
                break
        if not install_cmd:
            continue
        mb = MCP_BOOT.search(text)
        if mb:
            boot_cmd = mb.group(1).strip()
        candidates.append({
            "slug": path.stem,
            "tool_type": fm.get("tool_type", ""),
            "install_kind": install_kind,
            "install_cmd": install_cmd,
            "boot_cmd": boot_cmd,
            "verified_on": fm.get("verified_on", ""),  # "" sorts first -> unstamped first
        })
    # Unstamped ("") first, then oldest verified_on.
    candidates.sort(key=lambda c: (c["verified_on"] != "", c["verified_on"], c["slug"]))
    return candidates[:max_n]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max", type=int, default=12, help="max targets to emit")
    ap.add_argument("--out", type=Path, default=None, help="write JSON batch here")
    args = ap.parse_args()
    batch = {"selected": select(args.max), "gate": "safe-subset-v1"}
    text = json.dumps(batch, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.write_text(text, encoding="utf-8")
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
