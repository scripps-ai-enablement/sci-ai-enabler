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


if __name__ == "__main__":
    unittest.main()
