#!/usr/bin/env python3
"""Tests for install/env prep in scripts/run_smoke_tests.py.

The smoke runner installs each tool under an isolated temp HOME, then boots MCP
servers. Installs must land somewhere the boot probe can reach:
  * pip  -> a --target dir exposed on PYTHONPATH,
  * uv tool install -> ~/.local/bin (HOME is the temp dir) pinned and put on PATH
    so a boot command like `biomcp serve` can find the installed binary.

The second case is the BioMCP regression: uv installed the `biomcp` executable
into <work>/.local/bin, which was NOT on PATH, so `biomcp serve` failed with
"command not found". These tests pin the env prep without executing anything.

Pure standard library. Run: python3 -m unittest discover -s tests
"""
from __future__ import annotations

import importlib.util
import os
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "run_smoke_tests.py"

_spec = importlib.util.spec_from_file_location("run_smoke_tests", SCRIPT)
runner = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(runner)


class PrepareInstall(unittest.TestCase):
    def setUp(self):
        self.work = Path("/tmp/smoke_work_xyz")

    def test_uv_tool_install_puts_bin_on_path(self):
        env = {"PATH": "/usr/bin"}
        cmd = runner._prepare_install("uv tool install biomcp-cli", self.work, env)
        bin_dir = str(self.work / ".local" / "bin")
        # Command is unchanged; env is adjusted so the boot probe finds the binary.
        self.assertEqual(cmd, "uv tool install biomcp-cli")
        self.assertEqual(env["UV_TOOL_BIN_DIR"], bin_dir)
        self.assertTrue(env["PATH"].startswith(bin_dir + os.pathsep))
        self.assertIn("/usr/bin", env["PATH"])

    def test_pip_install_targets_pythonpath(self):
        env = {}
        cmd = runner._prepare_install("pip install anndata", self.work, env)
        target = str(self.work / "site")
        self.assertIn(f"--target {target}", cmd)
        self.assertEqual(env["PYTHONPATH"], target)

    def test_other_installs_untouched(self):
        env = {"PATH": "/usr/bin"}
        cmd = runner._prepare_install("npx skills add org/repo", self.work, env)
        self.assertEqual(cmd, "npx skills add org/repo")
        self.assertEqual(env, {"PATH": "/usr/bin"})  # no PATH/PYTHONPATH mutation


class ProbeBoot(unittest.TestCase):
    """The MCP stdio handshake probe, exercised against fake local servers."""

    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="probe_")
        self.env = dict(os.environ)

    def _server(self, body: str) -> str:
        path = Path(self.dir) / f"srv_{len(list(Path(self.dir).iterdir()))}.py"
        path.write_text(textwrap.dedent(body), encoding="utf-8")
        return f"{sys.executable} {path}"

    def test_compliant_server_completes_handshake(self):
        # Reads the initialize request, replies with a JSON-RPC result, stays up.
        cmd = self._server("""
            import sys, json, time
            msg = json.loads(sys.stdin.readline())
            print(json.dumps({"jsonrpc": "2.0", "id": msg["id"],
                              "result": {"protocolVersion": "2025-06-18",
                                         "serverInfo": {"name": "fake"},
                                         "capabilities": {}}}), flush=True)
            time.sleep(10)
        """)
        status, log = runner._probe_boot(cmd, self.dir, self.env, 5)
        self.assertEqual(status, "pass")
        self.assertIn('"result"', log)

    def test_startup_logs_before_response_are_ignored(self):
        # Non-JSON startup chatter on stderr must not break handshake detection.
        cmd = self._server("""
            import sys, json, time
            sys.stderr.write("booting fake server...\\n"); sys.stderr.flush()
            json.loads(sys.stdin.readline())
            print(json.dumps({"jsonrpc": "2.0", "id": 1, "result": {}}), flush=True)
            time.sleep(10)
        """)
        status, _ = runner._probe_boot(cmd, self.dir, self.env, 5)
        self.assertEqual(status, "pass")

    def test_dead_command_is_boot_error(self):
        # Exits non-zero immediately without speaking MCP (like a bad subcommand).
        cmd = self._server("""
            import sys
            sys.stderr.write("Error: unknown command 'serve'\\n")
            sys.exit(2)
        """)
        status, _ = runner._probe_boot(cmd, self.dir, self.env, 5)
        self.assertEqual(status, "boot_error")

    def test_server_that_stays_up_passes_without_response(self):
        # Legacy fallback: a server still alive at the timeout counts as booted.
        cmd = self._server("import time; time.sleep(30)")
        status, _ = runner._probe_boot(cmd, self.dir, self.env, 2)
        self.assertEqual(status, "pass")

    def test_clean_exit_without_mcp_passes(self):
        cmd = self._server("print('ok')")
        status, _ = runner._probe_boot(cmd, self.dir, self.env, 5)
        self.assertEqual(status, "pass")


class ToolchainDetection(unittest.TestCase):
    """`needs_toolchain` fires only when the compiler binary is missing."""

    def test_compiler_absent_is_needs_toolchain(self):
        for log in [
            "distutils...CompileError: command 'gcc' failed: No such file or directory",
            "error: command 'cc' failed: command not found",
            "gcc: not found",
            "gcc: No such file or directory",
            "unable to execute 'cc': No such file or directory",
        ]:
            with self.subTest(log=log):
                self.assertTrue(runner._needs_toolchain(log))

    def test_real_failures_are_not_needs_toolchain(self):
        # A compile error WITH a compiler present, or an unrelated failure, must
        # stay a real install_error — not be excused as a missing toolchain.
        for log in [
            "CompileError: command 'gcc' failed with exit status 1",
            "error: metadata-generation-failed",
            "ERROR: Could not find a version that satisfies the requirement foo",
            "ModuleNotFoundError: No module named 'setuptools'",
        ]:
            with self.subTest(log=log):
                self.assertFalse(runner._needs_toolchain(log))


class MergeResults(unittest.TestCase):
    def test_retried_outcomes_overlay_in_order(self):
        prior = [
            {"slug": "a", "status": "pass"},
            {"slug": "b", "status": "needs_toolchain"},
            {"slug": "c", "status": "install_error"},
        ]
        retried = [{"slug": "b", "status": "pass"}]
        merged = runner._merge_results(prior, retried)
        self.assertEqual([r["slug"] for r in merged], ["a", "b", "c"])
        self.assertEqual([r["status"] for r in merged], ["pass", "pass", "install_error"])


if __name__ == "__main__":
    unittest.main()
