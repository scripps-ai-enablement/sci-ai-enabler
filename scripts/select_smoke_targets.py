#!/usr/bin/env python3
"""Select the SAFE subset of catalog tools to smoke-test, deterministically.

This is the code-enforced safety gate for the verifier's quarantined smoke-test
job (see .github/workflows/verify.yml). It is intentionally NOT the model's job:
only targets this script emits are ever installed/booted, so the decision of
"what untrusted code may run" is auditable Python, not an LLM judgment.

A tool qualifies only if ALL hold:
  * tool_type is a Claude Skill or an MCP server (installable/bootable);
  * we can extract a public, no-auth install command (pip / uv / npx / npm);
  * NOTHING on the page trips the safety gate (`gate_blocked`).
The gate over-excludes on purpose — over-exclusion is the safe direction, so
paid, credentialed, and controlled-access tools stay blocked no matter what.
It has exactly two deliberate relaxations so that no-auth servers that merely
*mention* optional credentials are still eligible:
  * API-key / token mentions only trip the gate when they are NOT marked
    OPTIONAL. "optional API keys (NCBI, ...) raise rate limits" (BioMCP) does
    not gate-exclude; "requires an API key" still does.
  * "register" only trips the gate for account registration, not for
    "register the server"-style MCP client setup steps.
Everything else — subscription, paid, oauth, dbGaP, wet-lab, sign up, login,
account required, enterprise, waitlist, request access, ... — is a hard denial.
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

# Hard denials: if any appears anywhere on the page (case-insensitive), the tool
# is gate-excluded from execution outright — paid, credentialed, or controlled-
# access requirements that no surrounding context can make safe to run.
# Conservative by design: over-exclusion is the safe direction.
HARD_DENY = [
    "subscription", "paid", "per experiment", "per-experiment", "credit",
    "institutional", "credentialed", "controlled-access", "controlled access",
    "dbgap", "data use agreement", "dua", "enterprise", "waitlist",
    "request access", "request-gated", "sign up", "sign-up", "signup",
    "log in", "login", "create an account", "account required",
    "wet lab", "wet-lab", "oauth", "client secret", "license key",
]

# API-key / token mentions. These trip the gate BY DEFAULT — a page that needs a
# credential must not be smoke-executed — EXCEPT for occurrences the page clearly
# marks OPTIONAL. This is the BioMCP case: "optional API keys (NCBI, OpenFDA,
# ...) raise rate limits" describes a server that runs fully with no auth, so it
# should be eligible; "requires an API key" must still be excluded.
CREDENTIAL_TERMS = [
    "api key", "api-key", "apikey", "access token", "auth token", "bearer",
]
# A credential occurrence counts as OPTIONAL only when it falls inside one of
# these anchored phrasings (the qualifier must sit next to the credential, so a
# stray "optional" or "no ..." elsewhere in the sentence can't relax a required
# key). High precision on purpose: an unmatched mention stays excluded.
_OPTIONAL_CREDENTIAL = re.compile(
    # "optional API keys", "optional per-source api key"
    r"optional\s+(?:[\w./-]+\s+){0,3}?"
    r"(?:api[- ]?keys?|apikeys?|access tokens?|auth tokens?|bearer(?:\s+tokens?)?|credentials?|authentication)"
    # "API keys are optional"
    r"|(?:api[- ]?keys?|apikeys?|access tokens?|auth tokens?|bearer(?:\s+tokens?)?|credentials?)"
    r"\s+(?:are|is)\s+(?:entirely |completely |fully |totally |purely )?optional\b"
    # "no API key required", "no authentication needed"
    r"|\bno\s+(?:api[- ]?keys?|apikeys?|access tokens?|auth tokens?|tokens?|credentials?|authentication|auth)"
    r"\s+(?:is\s+|are\s+)?(?:required|needed|necessary)\b",
    re.IGNORECASE,
)

# "register" is an account-registration signal EXCEPT when it means registering
# the MCP server/tool with the client ("register the server") — a setup step,
# not a credential gate, so it must not exclude no-auth servers like BioMCP.
_REGISTER = re.compile(r"\bregist(?:er|ration)\b", re.IGNORECASE)
_REGISTER_BENIGN = re.compile(
    r"regist(?:er|ration)\s+(?:the\s+|a\s+|an\s+|your\s+|this\s+|it\s+)?"
    r"(?:mcp\s+)?(?:server|tool|service|client|plugin|extension|command|connector|integration|endpoint)\b",
    re.IGNORECASE,
)


def _credential_required(low: str) -> bool:
    """True if any API-key/token mention is NOT clearly marked optional."""
    optional = [m.span() for m in _OPTIONAL_CREDENTIAL.finditer(low)]
    for term in CREDENTIAL_TERMS:
        for m in re.finditer(re.escape(term), low):
            s, e = m.span()
            if not any(lo <= s and e <= hi for lo, hi in optional):
                return True
    return False


def _registration_required(low: str) -> bool:
    """True if the page mentions account registration (not MCP server setup)."""
    for m in _REGISTER.finditer(low):
        if not _REGISTER_BENIGN.match(low, m.start()):
            return True
    return False


def gate_blocked(text: str) -> bool:
    """Return True if the page trips the safety gate (never smoke-execute it).

    Over-exclusion is the safe direction, so anything that needs paid,
    credentialed, or controlled-access resources stays blocked. The only
    deliberate relaxations are (1) API-key/token mentions the page marks
    OPTIONAL and (2) "register the server"-style MCP setup steps.
    """
    low = text.lower()
    if any(term in low for term in HARD_DENY):
        return True
    if _credential_required(low):
        return True
    if _registration_required(low):
        return True
    return False

# Extract a public install command we can hand to the smoke runner. The command
# may be written inline in backticks (`pip install foo`) OR on its own line
# inside a fenced ``` code block (indented, no surrounding backticks) — BioMCP
# uses the latter. Each body is therefore delimited by EITHER a backtick or a
# line boundary, matched in MULTILINE mode. Bodies are tried in priority order.
_INSTALL_BODIES = [
    ("pip", r"pip install [A-Za-z0-9_.\-\[\]=<>! ]+"),
    ("uv", r"uv tool install [A-Za-z0-9_.\-]+"),
    ("uvx", r"uvx [A-Za-z0-9_.\-]+"),
    ("npx-skills", r"npx skills add [A-Za-z0-9_./\-]+"),
    ("npx", r"npx -y [A-Za-z0-9_.@/\-]+"),
]
INSTALL_PATTERNS = [
    (re.compile(r"(?:`|^[ \t]*)(" + body + r")(?:`|[ \t]*$)", re.MULTILINE), kind)
    for kind, body in _INSTALL_BODIES
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
        if gate_blocked(text):
            continue
        install_cmd = boot_cmd = None
        for rx, kind in INSTALL_PATTERNS:
            m = rx.search(text)
            if m:
                install_cmd, install_kind = m.group(1).strip(), kind
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
