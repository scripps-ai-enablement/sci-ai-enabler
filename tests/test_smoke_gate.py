#!/usr/bin/env python3
"""Tests for the smoke-test target selector in scripts/select_smoke_targets.py.

The gate is the code-enforced answer to "what untrusted code may run" in the
verifier's quarantined smoke job, so its exclusion behaviour is safety-critical
and must be pinned. The guiding principle is that over-exclusion is the SAFE
direction: paid, credentialed, and controlled-access tools must stay blocked.

These tests pin the two deliberate gate relaxations that let no-auth servers
through without weakening any of that:
  * API-key / token mentions only trip the gate when NOT marked OPTIONAL, so a
    server like BioMCP ("optional API keys ... raise rate limits") stays
    eligible while "requires an API key" stays blocked.
  * "register" only trips for account registration, not "register the server"
    MCP client setup.

They also pin install-command extraction, which must read a command from a
fenced ``` code block (BioMCP's `uv tool install biomcp-cli`), not only from
inline backticks.

Pure standard library. Run: python3 -m unittest discover -s tests
"""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "select_smoke_targets.py"
TOOLS = REPO / "catalog" / "tools"

_spec = importlib.util.spec_from_file_location("select_smoke_targets", SCRIPT)
gate = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(gate)


class OptionalCredentialsPass(unittest.TestCase):
    """No-auth servers that merely mention optional credentials are eligible."""

    ALLOWED = [
        # The motivating BioMCP phrasing, verbatim in spirit.
        "optional API keys (NCBI, OpenFDA, NCI CTS) raise rate limits",
        "optional per-source api key unlocks private sources",
        "API keys are optional",
        "the access token is entirely optional",
        "no API key required to use this server",
        "no authentication needed; runs anonymously",
        "runs fully offline, no auth, no api key needed",
    ]

    def test_optional_credentials_not_blocked(self):
        for text in self.ALLOWED:
            with self.subTest(text=text):
                self.assertFalse(gate.gate_blocked(text))


class RequiredCredentialsBlocked(unittest.TestCase):
    """Anything that actually needs a credential stays excluded."""

    BLOCKED = [
        "Requires an API key from your dashboard",
        "You must provide a bearer token",
        "Set your access token in the environment before running",
        "Sign in and copy your api-key into the config",
        "Provide an auth token issued by the vendor",
    ]

    def test_required_credentials_blocked(self):
        for text in self.BLOCKED:
            with self.subTest(text=text):
                self.assertTrue(gate.gate_blocked(text))

    def test_mixed_optional_and_required_is_blocked(self):
        # One optional key and one that is plainly required -> stay excluded.
        text = ("The NCBI api key is optional and raises rate limits, but a "
                "vendor api key is required for the private endpoint.")
        self.assertTrue(gate.gate_blocked(text))

    def test_optional_key_does_not_rescue_a_hard_denial(self):
        # "optional API key" must not smuggle a paid / credentialed tool through.
        self.assertTrue(gate.gate_blocked("optional API key; paid subscription required"))
        self.assertTrue(gate.gate_blocked("API key optional but institutional login needed"))
        self.assertTrue(gate.gate_blocked("optional api key; controlled-access dbGaP data"))


class RegisterCarveOut(unittest.TestCase):
    """'register the server' is MCP setup; 'register an account' is auth."""

    def test_mcp_registration_allowed(self):
        for text in [
            "install the CLI, then register the server: claude mcp add ...",
            "register the MCP server for programmatic tool access",
            "registering AnnData via setup_anndata",
            "register your tool with the client",
        ]:
            with self.subTest(text=text):
                self.assertFalse(gate.gate_blocked(text))

    def test_account_registration_blocked(self):
        for text in [
            "you must register for a free account",
            "registration required to obtain access",
            "register an account to get your API key",
            "please register at example.com before use",
        ]:
            with self.subTest(text=text):
                self.assertTrue(gate.gate_blocked(text))

    def test_mixed_registration_is_blocked(self):
        # A benign server-registration line does not excuse account registration.
        text = "register the server with claude mcp add; you must register an account first"
        self.assertTrue(gate.gate_blocked(text))


class HardDenialsUnchanged(unittest.TestCase):
    """The non-credential hard terms still block, exactly as before."""

    def test_hard_terms_block(self):
        for term in gate.HARD_DENY:
            with self.subTest(term=term):
                self.assertTrue(gate.gate_blocked(f"This tool needs {term} to run."))

    def test_representative_hard_denials(self):
        for text in [
            "Requires an enterprise subscription",
            "Uses OAuth to sign in",
            "Access is controlled-access via dbGaP",
            "Runs in a wet lab",
            "Join the waitlist to request access",
            "You need a license key and client secret",
        ]:
            with self.subTest(text=text):
                self.assertTrue(gate.gate_blocked(text))


class CatalogInvariants(unittest.TestCase):
    """Exercise the gate against the real catalog, not just synthetic strings."""

    def _tools(self):
        return [p for p in sorted(TOOLS.glob("*.md")) if p.name != "index.md"]

    def test_biomcp_is_gate_allowed(self):
        # The concrete regression: BioMCP runs with no auth but mentions optional
        # API keys and "register the server". It must not be gate-excluded.
        text = (TOOLS / "biomcp.md").read_text(encoding="utf-8")
        self.assertFalse(gate.gate_blocked(text))

    def test_hard_denial_terms_always_block(self):
        # Invariant: presence of any HARD_DENY substring => gate blocks the page.
        # Over-exclusion stays guaranteed for the hard terms.
        for path in self._tools():
            low = path.read_text(encoding="utf-8").lower()
            if any(term in low for term in gate.HARD_DENY):
                with self.subTest(tool=path.name):
                    self.assertTrue(gate.gate_blocked(path.read_text(encoding="utf-8")))

    def test_allowed_pages_have_no_unqualified_credential(self):
        # Anything the gate allows must not carry an unqualified credential
        # mention (the whole point of the credential carve-out).
        for path in self._tools():
            text = path.read_text(encoding="utf-8")
            if not gate.gate_blocked(text):
                with self.subTest(tool=path.name):
                    self.assertFalse(gate._credential_required(text.lower()))

    def test_select_runs_end_to_end(self):
        # select() still runs end to end and returns a list after the gate change.
        selected = gate.select(300)
        self.assertIsInstance(selected, list)


class InstallExtraction(unittest.TestCase):
    """Install commands are read from fenced code blocks AND inline backticks."""

    def _extract(self, text):
        for rx, kind in gate.INSTALL_PATTERNS:
            m = rx.search(text)
            if m:
                return kind, m.group(1).strip()
        return None, None

    def test_fenced_code_block_command(self):
        # BioMCP's shape: command on its own indented line inside a ``` fence.
        text = (
            "- **Claude Code** — install the CLI, then register the server:\n"
            "  ```\n"
            "  uv tool install biomcp-cli\n"
            "  claude mcp add --transport stdio biomcp -- biomcp serve\n"
            "  ```\n"
        )
        self.assertEqual(self._extract(text), ("uv", "uv tool install biomcp-cli"))

    def test_inline_backtick_command_still_works(self):
        self.assertEqual(
            self._extract("Install with `pip install foo` then import it."),
            ("pip", "pip install foo"),
        )
        self.assertEqual(
            self._extract("Run `npx skills add org/repo` to add the skill."),
            ("npx-skills", "npx skills add org/repo"),
        )

    def test_command_mid_prose_is_not_matched(self):
        # Only a line-start (fenced/bare) or a backtick delimits a command; a
        # bare command in the middle of a sentence must not be extracted.
        self.assertEqual(
            self._extract("Do not run pip install evil in production."),
            (None, None),
        )

    def test_biomcp_is_selected_with_install_command(self):
        # The end-to-end regression: BioMCP now clears the gate AND yields an
        # extractable install command, so it is eligible for smoke-boot testing.
        selected = {c["slug"]: c for c in gate.select(500)}
        self.assertIn("biomcp", selected)
        self.assertEqual(selected["biomcp"]["install_kind"], "uv")
        self.assertEqual(selected["biomcp"]["install_cmd"], "uv tool install biomcp-cli")


if __name__ == "__main__":
    unittest.main()
