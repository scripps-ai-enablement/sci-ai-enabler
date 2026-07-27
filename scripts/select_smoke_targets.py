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
RECIPES = REPO / "recipes" / "items"

# At most 1-in-N of a batch may be recipe dependencies. Candidate ordering is
# unstamped-first, and recipe targets carry no `verified_on`, so without a cap a
# fresh crop of dependency blocks would monopolize every batch and silently
# starve tool-page re-verification.
RECIPE_SHARE = 3

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
# `[ \t]` rather than `\s` between argv tokens: `\s` matches newlines, so the
# capture ran past the end of the line and swallowed whatever followed on the
# next line (a page with an install line plus an import line yielded
# "foo-server run\npython3 -c"). Launch commands are single-line by definition.
MCP_BOOT = re.compile(
    r"claude mcp add[^`\n]*?--[ \t]+([A-Za-z0-9_.\-]+(?:[ \t]+[A-Za-z0-9_.\-]+)*)"
)

# Optional boot check for anything that documents an import: a
# `python3 -c "import <module>"` line. We capture ONLY a dotted identifier and
# SYNTHESIZE the command in `import_boot()` — we never pass the page's literal
# string through. That is the whole point: these pages are LLM-authored, and
# scraping the literal text would turn any page into an arbitrary-code channel
# into the smoke container, destroying the property this module exists to hold
# (what untrusted code runs is decided by auditable Python, not by a page).
# The `python3 -c "..."` payload, confined to one line (`.` excludes newlines).
IMPORT_CMD = re.compile(r"""python3? +-c +(["'])(.+?)\1""")
# A dotted module name following the `import` keyword, and nothing else.
IMPORT_NAME = re.compile(r"\bimport +([A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z0-9_]+)*)")


def import_boot(text: str) -> str | None:
    """A safe `python3 -c "import a, b"` boot command, or None.

    Every module a block documents is checked, not just the first: a recipe with
    two dependencies writes one import line for both, and verifying half of it
    would report a pass while leaving a dependency untested.

    The returned command is REBUILT from validated dotted identifiers, so
    whatever else the page's literal string contained cannot survive into it.
    """
    modules: list[str] = []
    for cmd in IMPORT_CMD.finditer(text):
        for name in IMPORT_NAME.findall(cmd.group(2)):
            if name not in modules:
                modules.append(name)
    if not modules:
        return None
    return 'python3 -c "import ' + ", ".join(modules) + '"'


def boot_for(text: str) -> str | None:
    """MCP launch command if the page has one, else a documented import check."""
    m = MCP_BOOT.search(text)
    if m:
        return m.group(1).strip()
    return import_boot(text)


def section_block(text: str, heading: str) -> str:
    """The whole body of a `## <heading>` section, or "" when absent."""
    lines = text.splitlines()
    out, capture = [], False
    for line in lines:
        if line.startswith("## "):
            if capture:
                break
            capture = line[3:].strip().lower() == heading.lower()
            continue
        if capture:
            out.append(line)
    return "\n".join(out)


def recipe_dependency_targets() -> list[dict]:
    """Smoke targets from every recipe's `## Dependencies` block.

    A recipe dependency is a pinned pip install plus a documented import, so it
    is exactly the shape the runner already handles. Only `pip` is eligible: the
    runner's install rewriting (`_prepare_install`) understands pip and uv, and
    the sandbox image has no conda, R, or compiler — a conda target would fail
    with rc 127 and read as a real `install_error`.
    """
    targets = []
    if not RECIPES.is_dir():
        return targets
    for path in sorted(RECIPES.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        block = section_block(text, "Dependencies")
        if not block.strip():
            continue
        # Gate the DEPENDENCIES BLOCK, not the whole page. Scanning the whole
        # recipe measured 87/97 pages blocked, because HARD_DENY terms
        # ("institutional", "subscription") occur in a recipe's `## Availability`
        # section describing its *components'* access bars — which says nothing
        # about whether a pinned public PyPI package is safe to install. The gate
        # asks "does executing this need credentials or paid access?", and for a
        # public pip package the answer is structurally no: the `==` pin and the
        # pip-only restriction below already confine these to registry-resolvable
        # public packages. A block that does mention a key or a license gate is
        # still excluded.
        if gate_blocked(block):
            continue
        for rx, kind in INSTALL_PATTERNS:
            if kind != "pip":
                continue
            for m in rx.finditer(block):
                cmd = m.group(1).strip()
                if "==" not in cmd:
                    continue  # unpinned: RECIPE_AGENT.md forbids it, don't execute it
                targets.append({
                    "slug": path.stem,
                    "source": "recipe",
                    "tool_type": "",
                    "install_kind": kind,
                    "install_cmd": cmd,
                    "boot_cmd": import_boot(block),
                    "verified_on": "",
                })
    return targets


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
        # An MCP launch command if the page documents one, otherwise a documented
        # import check. The import branch is deliberately NOT conditional on
        # tool_type: a wrapper Skill page that documents `python3 -c "import x"`
        # gains a real functional check instead of passing on install alone.
        boot_cmd = boot_for(text)
        candidates.append({
            "slug": path.stem,
            "source": "tool",
            "tool_type": fm.get("tool_type", ""),
            "install_kind": install_kind,
            "install_cmd": install_cmd,
            "boot_cmd": boot_cmd,
            "verified_on": fm.get("verified_on", ""),  # "" sorts first -> unstamped first
        })

    # Canonical order: unstamped ("") first, then oldest verified_on.
    order = lambda c: (c["verified_on"] != "", c["verified_on"], c["slug"])
    recipes = sorted(recipe_dependency_targets(), key=order)
    candidates.sort(key=order)

    # Cap the recipe share so dependency targets — all unstamped, so all sorting
    # to the front — cannot crowd tool pages out of the batch entirely.
    if recipes:
        cap = max(1, max_n // RECIPE_SHARE)
        batch = recipes[:cap] + candidates
        batch.sort(key=order)
        return batch[:max_n]
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
