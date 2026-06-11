#!/usr/bin/env python3
"""CI tests for the Composer plugin.

The Composer's reasoning is model-driven and not unit-testable, but its
foundations are: the index generator, the plugin/marketplace structure, the
grounding invariant (every indexed path resolves to a real page), the
capture-loop wiring, and — most valuably — a freshness check that fails if a
content page changed without the committed index being rebuilt.

Pure stdlib + (optionally) PyYAML. Run: python3 -m unittest discover -s tests
"""

from __future__ import annotations

import importlib.util
import json
import re
import unittest
from pathlib import Path

try:
    import yaml  # noqa: F401
    HAVE_YAML = True
except ImportError:
    HAVE_YAML = False

REPO = Path(__file__).resolve().parent.parent
PLUGIN = REPO / "composer"
PLUGIN_DATA = PLUGIN / "skills" / "compose" / "data"

# Import scripts/build_index.py as a module without needing a package.
_spec = importlib.util.spec_from_file_location("build_index", REPO / "scripts" / "build_index.py")
build_index = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(build_index)


def write_page(path: Path, frontmatter: dict, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["---"]
    for k, v in frontmatter.items():
        if isinstance(v, list):
            lines.append(f"{k}: [{', '.join(v)}]")
        else:
            lines.append(f"{k}: {v}")
    lines.append("---")
    path.write_text("\n".join(lines) + "\n\n" + body, encoding="utf-8")


def valid_recipe_fm(**over):
    fm = {
        "title": "Test recipe",
        "problem_class": "Data analysis",
        "subject_areas": ["All"],
        "evidence_level": "Proposed",
        "complexity": "One skill or MCP",
        "availability": "Fully open",
        "compute_requirements": "Laptop",
        "last_verified": "2026-06-11",
        "summary": "A test recipe summary.",
    }
    fm.update(over)
    return fm


# ---------------------------------------------------------------------------
# 1. The index generator against the real corpus
# ---------------------------------------------------------------------------

class TestRealCorpus(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tools, cls.recipes, cls.systems, cls.errors = build_index.build_all(REPO)

    def test_no_errors_on_real_corpus(self):
        self.assertEqual(self.errors, [], f"build_index reported page errors: {self.errors}")

    def test_nonempty(self):
        self.assertGreater(len(self.tools), 0)
        self.assertGreater(len(self.recipes), 0)
        self.assertGreater(len(self.systems), 0)

    def test_counts_match_files_on_disk(self):
        def md_count(glob):
            return len([p for p in REPO.glob(glob) if p.name != "index.md"])
        self.assertEqual(len(self.tools), md_count("catalog/tools/*.md"))
        self.assertEqual(len(self.recipes), md_count("recipes/items/*.md"))
        self.assertEqual(len(self.systems), md_count("autonomous-science/systems/*.md"))

    def test_every_entry_has_matchable_fields(self):
        for arr, name in ((self.tools, "tool"), (self.recipes, "recipe"), (self.systems, "system")):
            for e in arr:
                self.assertTrue(e["slug"], f"{name} missing slug")
                self.assertTrue(e["title"], f"{name} {e['slug']} missing title")
                self.assertTrue(e["summary"].strip(), f"{name} {e['slug']} has empty summary")
                self.assertIsInstance(e["keywords"], list)

    def test_grounding_invariant_every_path_resolves(self):
        # The composer reads a finalist's full page by `path`; a dangling path
        # would let it cite a page that doesn't exist. Every path must resolve.
        for arr in (self.tools, self.recipes, self.systems):
            for e in arr:
                self.assertTrue((REPO / e["path"]).is_file(), f"dangling path: {e['path']}")

    def test_recipe_facets_in_closed_vocab(self):
        for r in self.recipes:
            self.assertIn(r["problem_class"], build_index.PROBLEM_CLASSES)
            self.assertIn(r["evidence_level"], build_index.EVIDENCE_LEVELS)
            self.assertIn(r["complexity"], build_index.COMPLEXITY)
            self.assertIn(r["availability"], build_index.RECIPE_AVAILABILITY)
            self.assertIn(r["compute_requirements"], build_index.COMPUTE)
            for sa in r["subject_areas"]:
                self.assertIn(sa, build_index.SUBJECT_AREAS)

    def test_tool_categories_in_closed_vocab(self):
        for t in self.tools:
            for c in t["tool_categories"]:
                self.assertIn(c, build_index.TOOL_CATEGORIES)

    def test_composer_dogfoods_itself(self):
        # The Composer ships its own catalog page, so it appears in the index it consumes.
        slugs = {t["slug"] for t in self.tools}
        self.assertIn("composer", slugs)


# ---------------------------------------------------------------------------
# 2. Validation fails loudly on bad input (synthetic corpora)
# ---------------------------------------------------------------------------

class TestValidationFailsLoudly(unittest.TestCase):
    def _build(self, make):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            make(root)
            return build_index.build_all(root)

    def test_bad_problem_class_errors(self):
        def make(root):
            write_page(root / "recipes/items/bad.md",
                       valid_recipe_fm(problem_class="Bogus class"), "# Bad\n\nLead.\n")
        _, _, _, errors = self._build(make)
        self.assertTrue(any("not in closed vocabulary" in e for e in errors), errors)

    def test_bad_tool_category_errors(self):
        def make(root):
            write_page(root / "catalog/tools/bad.md",
                       {"title": "Bad tool", "tool_categories": ["Nonexistent Dept"],
                        "summary": "x"}, "# Bad tool\n\nLead.\n")
        _, _, _, errors = self._build(make)
        self.assertTrue(any("not in closed vocabulary" in e for e in errors), errors)

    def test_missing_lead_description_errors(self):
        def make(root):
            # Frontmatter valid, but the body jumps straight to a section with no lead paragraph.
            write_page(root / "recipes/items/nolead.md",
                       valid_recipe_fm(), "# No lead\n\n## Problem\n\nbody\n")
        _, _, _, errors = self._build(make)
        self.assertTrue(any("missing lead description" in e for e in errors), errors)

    def test_missing_required_title_errors(self):
        def make(root):
            fm = valid_recipe_fm()
            del fm["title"]
            write_page(root / "recipes/items/notitle.md", fm, "# x\n\nLead.\n")
        _, _, _, errors = self._build(make)
        self.assertTrue(any("missing required" in e for e in errors), errors)

    def test_valid_synthetic_corpus_has_no_errors(self):
        def make(root):
            write_page(root / "recipes/items/ok.md", valid_recipe_fm(), "# OK\n\nA clean lead.\n")
            write_page(root / "catalog/tools/ok.md",
                       {"title": "OK tool", "tool_categories": ["All"], "summary": "x"},
                       "# OK tool\n\nA clean lead.\n")
            write_page(root / "autonomous-science/systems/ok.md",
                       {"title": "OK sys", "tagline": "a tagline"}, "# OK sys\n\nA clean lead.\n")
        tools, recipes, systems, errors = self._build(make)
        self.assertEqual(errors, [])
        self.assertEqual((len(tools), len(recipes), len(systems)), (1, 1, 1))


# ---------------------------------------------------------------------------
# 3. Committed index is fresh and internally consistent
# ---------------------------------------------------------------------------

class TestIndexArtifacts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = json.loads((REPO / "index" / "composer-index.json").read_text())
        cls.tools_doc = json.loads((REPO / "index" / "composer-tools.json").read_text())

    def test_index_structure(self):
        self.assertEqual(self.index["tools_file"], "composer-tools.json")
        for key in ("version", "generated", "counts", "recipes", "systems"):
            self.assertIn(key, self.index)

    def test_counts_field_matches_arrays(self):
        c = self.index["counts"]
        self.assertEqual(c["recipes"], len(self.index["recipes"]))
        self.assertEqual(c["systems"], len(self.index["systems"]))
        self.assertEqual(c["tools"], len(self.tools_doc["tools"]))

    def test_committed_index_is_fresh(self):
        # The strongest guard: rebuild from the live corpus and compare to the
        # committed arrays. Fails if a page changed without `build_index.py`
        # being re-run. The `generated` date is ignored so this isn't flaky.
        # Reports only the drifted slugs, never a full-index diff.
        tools, recipes, systems, errors = build_index.build_all(REPO)
        self.assertEqual(errors, [])

        def drifted(fresh, committed):
            fresh_by = {e["slug"]: e for e in fresh}
            comm_by = {e["slug"]: e for e in committed}
            added = sorted(fresh_by.keys() - comm_by.keys())
            removed = sorted(comm_by.keys() - fresh_by.keys())
            changed = sorted(s for s in fresh_by.keys() & comm_by.keys() if fresh_by[s] != comm_by[s])
            return added, removed, changed

        problems = []
        for label, fresh, committed in (
            ("recipes", recipes, self.index["recipes"]),
            ("systems", systems, self.index["systems"]),
            ("tools", tools, self.tools_doc["tools"]),
        ):
            added, removed, changed = drifted(fresh, committed)
            if added or removed or changed:
                problems.append(f"{label}: +{added} -{removed} ~{changed}")
        self.assertEqual(problems, [],
                         "committed index is stale — run `python3 scripts/build_index.py`. Drift: "
                         + "; ".join(problems))

    def test_bundled_copy_matches_root(self):
        # The plugin ships a mirror; drift would make installs stale silently.
        for name in ("composer-index.json", "composer-tools.json"):
            self.assertEqual((REPO / "index" / name).read_bytes(),
                             (PLUGIN_DATA / name).read_bytes(),
                             f"{name}: bundled plugin copy differs from index/ — run scripts/build_index.py")


# ---------------------------------------------------------------------------
# 4. Plugin + marketplace structure
# ---------------------------------------------------------------------------

class TestPluginStructure(unittest.TestCase):
    def test_marketplace_json_valid(self):
        mk = json.loads((REPO / ".claude-plugin" / "marketplace.json").read_text())
        self.assertTrue(mk.get("name"))
        entry = next((p for p in mk["plugins"] if p["name"] == "composer"), None)
        self.assertIsNotNone(entry, "composer not listed in marketplace.json")
        # Plugin `source` is relative to the marketplace root (the repo root that
        # holds .claude-plugin/), and must resolve to a real plugin directory
        # containing its own .claude-plugin/plugin.json.
        src = (REPO / entry["source"]).resolve()
        self.assertTrue(src.is_dir(), f"marketplace source does not resolve: {entry['source']}")
        self.assertTrue((src / ".claude-plugin" / "plugin.json").is_file(),
                        f"marketplace source {entry['source']} has no plugin.json")

    def test_plugin_json_valid(self):
        pj = json.loads((PLUGIN / ".claude-plugin" / "plugin.json").read_text())
        self.assertEqual(pj["name"], "composer")
        self.assertTrue(pj.get("version"))

    def test_command_present(self):
        self.assertTrue((PLUGIN / "commands" / "compose.md").is_file())

    def test_skill_has_frontmatter(self):
        text = (PLUGIN / "skills" / "compose" / "SKILL.md").read_text()
        self.assertTrue(text.startswith("---"), "SKILL.md missing YAML frontmatter")
        fm_block = text.split("---", 2)[1]
        self.assertRegex(fm_block, r"\bname:\s*compose\b")
        self.assertIn("description:", fm_block)

    def test_bundled_data_present_and_parses(self):
        for name in ("composer-index.json", "composer-tools.json"):
            json.loads((PLUGIN_DATA / name).read_text())


# ---------------------------------------------------------------------------
# 5. Capture-loop wiring (guards against half-removing one side)
# ---------------------------------------------------------------------------

class TestCaptureWiring(unittest.TestCase):
    def test_responder_form_check_includes_label(self):
        wf = (REPO / ".github" / "workflows" / "responder.yml").read_text()
        self.assertIn("composition-report", wf,
                      "responder.yml form-check no longer recognizes composition-report")

    def test_responder_agent_documents_label_and_trailer(self):
        ra = (REPO / "RESPONDER_AGENT.md").read_text()
        self.assertIn("claude:composition-report", ra)
        self.assertIn("report=composition", ra)

    def test_recipe_agent_handles_report(self):
        self.assertIn("report=composition", (REPO / "RECIPE_AGENT.md").read_text())

    def test_curator_state_has_composition_section(self):
        self.assertIn("## Composition reports", (REPO / "recipes" / "curator-state.md").read_text())

    @unittest.skipUnless(HAVE_YAML, "PyYAML not installed")
    def test_composition_report_form_valid(self):
        form = yaml.safe_load((REPO / ".github" / "ISSUE_TEMPLATE" / "composition-report.yml").read_text())
        self.assertIn("claude:composition-report", form["labels"])
        ids = {f.get("id") for f in form["body"]}
        for required in ("problem", "outcome"):
            self.assertIn(required, ids, f"composition-report form missing field id={required}")


# ---------------------------------------------------------------------------
# 6. All issue forms + workflows are well-formed YAML
# ---------------------------------------------------------------------------

@unittest.skipUnless(HAVE_YAML, "PyYAML not installed")
class TestYamlWellFormed(unittest.TestCase):
    def test_issue_templates_parse(self):
        for f in (REPO / ".github" / "ISSUE_TEMPLATE").glob("*.yml"):
            with self.subTest(file=f.name):
                yaml.safe_load(f.read_text())

    def test_workflows_parse(self):
        for f in (REPO / ".github" / "workflows").glob("*.yml"):
            with self.subTest(file=f.name):
                yaml.safe_load(f.read_text())


if __name__ == "__main__":
    unittest.main(verbosity=2)
