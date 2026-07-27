#!/usr/bin/env python3
"""Tests for the inbound-request state machine (scripts/request_state.py).

The behaviour that matters most is the one that was wrong in production: a
request the curator understood but could not answer — a recipe whose components
are not catalogued — must NOT land in `(closed this run)`, because the loop-closer
closes those issues as `completed`. Issue #74 was closed 2m24s after it was filed
with nothing shipped. `(blocked)` is the state that fixes that, and
`classify()` is what the workflows branch on, so both are pinned hard here.

Mutations are also asserted idempotent: the workflows re-apply them after a lost
push race, resetting to origin/main first, without tracking what already landed.

Pure standard library. Run: python3 -m unittest discover -s tests
"""
from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "scripts" / "request_state.py"

_spec = importlib.util.spec_from_file_location("request_state", SCRIPT)
rs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rs)

Q74 = ('- [#74 @goodb 2026-07-27] queue: recipes | question="Localize an implant tip" '
       "| author=@goodb | issue=74")


def state(open_=("_None._",), blocked=("_None._",), closed=("_None._",),
          with_blocked=True) -> str:
    """A minimal curator-state.md with the three lifecycle sections."""
    parts = ["---\ntitle: Curator state\n---\n\n# Curator state\n",
             "## User requests (open)\n\n" + "\n".join(open_) + "\n"]
    if with_blocked:
        parts.append("## User requests (blocked)\n\n" + "\n".join(blocked) + "\n")
    parts.append("## User requests (closed this run)\n\n" + "\n".join(closed) + "\n")
    parts.append("## Missing components\n\n- **x** — y\n")
    return "\n".join(parts)


class TestParsing(unittest.TestCase):
    def test_issue_from_prefix_and_field(self):
        self.assertEqual(rs.issue_of(Q74), "74")
        self.assertEqual(rs.issue_of("- no prefix | issue=91 → done"), "91")
        self.assertIsNone(rs.issue_of("- nothing here"))

    def test_prefix_wins_over_field(self):
        # A result note may cite another issue; the bullet's own prefix decides.
        line = "- [#74 @a 2026-07-27] queue: recipes | issue=74 → see issue=12 for context"
        self.assertEqual(rs.issue_of(line), "74")

    def test_blocked_on_slugs(self):
        line = Q74 + " | blocked-on=catalog:brainglobe-atlasapi,deepslice → deferred"
        self.assertEqual(rs.blocked_on(line), ["brainglobe-atlasapi", "deepslice"])
        self.assertEqual(rs.blocked_on(Q74), [])

    def test_chain_defaults_to_zero_and_clamps(self):
        self.assertEqual(rs.chain_of(Q74), 0)
        self.assertEqual(rs.chain_of(Q74 + " | chain=2"), 2)
        self.assertEqual(rs.chain_of(Q74 + " | chain=oops"), 0)

    def test_outcome_strips_trailing_punctuation(self):
        self.assertEqual(rs.outcome_of(Q74 + " → outcome=shipped."), "shipped")
        self.assertEqual(rs.outcome_of(Q74 + " → outcome=already-covered"),
                         "already-covered")
        self.assertIsNone(rs.outcome_of(Q74))

    def test_result_prose_strips_the_machine_token(self):
        """The token is state, not prose — a comment must not end in
        "outcome=blocked", which reads as a leaked variable to the user."""
        self.assertEqual(rs.result_prose(Q74 + " → components missing. outcome=blocked"),
                         "components missing.")
        self.assertEqual(rs.result_prose(Q74 + " → outcome=shipped; wrote recipes/items/a.md"),
                         "wrote recipes/items/a.md")
        self.assertEqual(rs.result_prose(Q74 + " → no LICENSE upstream outcome=declined."),
                         "no LICENSE upstream")
        self.assertEqual(rs.result_prose(Q74 + " → plain note"), "plain note")

    def test_classify_always_carries_result_prose(self):
        for section, kw in (("open", "open_"), ("blocked", "blocked"), ("closed this run", "closed")):
            got = rs.classify(state(**{kw: [Q74 + " → done. outcome=shipped"]}), "74")
            with self.subTest(section):
                self.assertEqual(got["result_prose"], "done.")
        self.assertEqual(rs.classify(state(), "74")["result_prose"], "")

    def test_result_note(self):
        self.assertEqual(rs.result_of(Q74 + " → wrote recipes/items/foo.md"),
                         "wrote recipes/items/foo.md")
        self.assertTrue(rs.result_of(Q74).startswith("[#74"))


class TestClassify(unittest.TestCase):
    def test_open_blocked_closed_absent(self):
        self.assertEqual(rs.classify(state(open_=[Q74]), "74")["status"], "open")
        self.assertEqual(rs.classify(state(blocked=[Q74]), "74")["status"], "blocked")
        self.assertEqual(rs.classify(state(closed=[Q74]), "74")["status"],
                         "closed this run")
        self.assertEqual(rs.classify(state(), "74")["status"], "absent")

    def test_outcome_blocked_in_closed_section_is_still_blocked(self):
        """Defence in depth: a mislabelled entry must not close the user's issue."""
        line = Q74 + " → outcome=blocked; needs brainglobe-atlasapi catalogued"
        self.assertEqual(rs.classify(state(closed=[line]), "74")["status"], "blocked")

    def test_carries_the_fields_the_chain_branches_on(self):
        line = (Q74 + " | blocked-on=catalog:deepslice | chain=1 | via=recipes-block"
                     " → outcome=blocked; deferred")
        got = rs.classify(state(blocked=[line]), "74")
        self.assertEqual(got["blocked_on"], ["deepslice"])
        self.assertEqual(got["chain"], 1)
        self.assertEqual(got["via"], "recipes-block")
        self.assertEqual(got["outcome"], "blocked")
        self.assertEqual(got["result"], "outcome=blocked; deferred")

    def test_classifies_against_a_file_missing_the_blocked_section(self):
        """Pre-migration files must classify without raising."""
        text = rs.ensure_sections(state(open_=[Q74], with_blocked=False))
        self.assertEqual(rs.classify(text, "74")["status"], "open")


class TestEnsureSections(unittest.TestCase):
    def test_inserts_blocked_between_open_and_closed(self):
        out = rs.ensure_sections(state(with_blocked=False))
        self.assertIn("## User requests (blocked)", out)
        self.assertLess(out.index("## User requests (open)"),
                        out.index("## User requests (blocked)"))
        self.assertLess(out.index("## User requests (blocked)"),
                        out.index("## User requests (closed this run)"))

    def test_preserves_surrounding_content(self):
        out = rs.ensure_sections(state(open_=[Q74], with_blocked=False))
        self.assertIn(Q74, out)
        self.assertIn("## Missing components", out)
        self.assertIn("- **x** — y", out)

    def test_idempotent(self):
        once = rs.ensure_sections(state(with_blocked=False))
        self.assertEqual(rs.ensure_sections(once), once)


class TestMove(unittest.TestCase):
    def test_open_to_blocked_restores_placeholder(self):
        out, changed = rs.move(state(open_=[Q74]), "74", rs.BLOCKED)
        self.assertTrue(changed)
        self.assertEqual(rs.bullets(out, rs.OPEN), [])
        self.assertIn("_None._", out.split("## User requests (blocked)")[0])
        self.assertEqual(rs.bullets(out, rs.BLOCKED), [Q74])

    def test_blocked_back_to_open_bumping_chain(self):
        line = Q74 + " | blocked-on=catalog:deepslice → outcome=blocked"
        out, changed = rs.move(state(blocked=[line]), "74", rs.OPEN, chain=1)
        self.assertTrue(changed)
        self.assertIn("chain=1", rs.bullets(out, rs.OPEN)[0])
        self.assertEqual(rs.bullets(out, rs.BLOCKED), [])

    def test_chain_is_rewritten_not_duplicated(self):
        out, _ = rs.move(state(open_=[Q74 + " | chain=1"]), "74", rs.BLOCKED, chain=2)
        line = rs.bullets(out, rs.BLOCKED)[0]
        self.assertIn("chain=2", line)
        self.assertNotIn("chain=1", line)

    def test_chain_inserted_before_the_result_arrow(self):
        out, _ = rs.move(state(open_=[Q74 + " → partial"]), "74", rs.BLOCKED, chain=1)
        line = rs.bullets(out, rs.BLOCKED)[0]
        self.assertLess(line.index("chain=1"), line.index("→"))

    def test_note_replaces_an_existing_result(self):
        out, _ = rs.move(state(open_=[Q74 + " → old note"]), "74", rs.CLOSED,
                         note="outcome=shipped; wrote recipes/items/foo.md")
        line = rs.bullets(out, rs.CLOSED)[0]
        self.assertNotIn("old note", line)
        self.assertEqual(line.count("→"), 1)
        self.assertTrue(line.endswith("outcome=shipped; wrote recipes/items/foo.md"))

    def test_note_clears_a_stale_outcome_from_the_field_head(self):
        """The bug this guards: a hand-back that keeps `outcome=blocked` in the
        head classifies as blocked forever, so the request never runs again."""
        line = Q74 + " | outcome=blocked | blocked-on=catalog:deepslice → deferred"
        out, _ = rs.move(state(blocked=[line]), "74", rs.OPEN, chain=1,
                         note="components catalogued; write the recipe now")
        moved = rs.bullets(out, rs.OPEN)[0]
        self.assertNotIn("outcome=blocked", moved)
        self.assertIn("blocked-on=catalog:deepslice", moved)  # provenance kept
        self.assertNotIn("| |", moved)
        self.assertEqual(rs.classify(out, "74")["status"], "open")

    def test_note_clears_a_stale_outcome_written_after_the_arrow(self):
        line = Q74 + " → outcome=blocked; needs deepslice"
        out, _ = rs.move(state(blocked=[line]), "74", rs.OPEN, note="unblocked")
        self.assertEqual(rs.classify(out, "74")["status"], "open")

    def test_leaves_other_entries_alone(self):
        other = "- [#70 @b 2026-07-01] queue: recipes | issue=70 → shipped"
        out, _ = rs.move(state(open_=[other, Q74]), "74", rs.BLOCKED)
        self.assertEqual(rs.bullets(out, rs.OPEN), [other])

    def test_absent_issue_is_a_no_op(self):
        before = state(open_=[Q74])
        out, changed = rs.move(before, "999", rs.CLOSED)
        self.assertFalse(changed)
        self.assertEqual(out, before)

    def test_idempotent(self):
        once, first = rs.move(state(open_=[Q74]), "74", rs.BLOCKED)
        twice, second = rs.move(once, "74", rs.BLOCKED)
        self.assertTrue(first)
        self.assertFalse(second)
        self.assertEqual(once, twice)


class TestAppend(unittest.TestCase):
    def test_replaces_the_placeholder(self):
        out, changed = rs.append(state(), Q74)
        self.assertTrue(changed)
        self.assertEqual(rs.bullets(out, rs.OPEN), [Q74])
        self.assertNotIn("_None._", out.split("## User requests (blocked)")[0])

    def test_adds_a_missing_bullet_prefix(self):
        out, _ = rs.append(state(), Q74[2:])
        self.assertEqual(rs.bullets(out, rs.OPEN), [Q74])

    def test_one_entry_per_issue_per_section(self):
        """The chain re-appends after a lost race; it must not double-queue."""
        once, _ = rs.append(state(), Q74)
        twice, changed = rs.append(once, Q74 + " | chain=1")
        self.assertFalse(changed)
        self.assertEqual(len(rs.bullets(twice, rs.OPEN)), 1)

    def test_appends_to_a_chosen_section(self):
        out, _ = rs.append(state(), Q74, rs.BLOCKED)
        self.assertEqual(rs.bullets(out, rs.BLOCKED), [Q74])
        self.assertEqual(rs.bullets(out, rs.OPEN), [])

    def test_idempotent(self):
        once, _ = rs.append(state(), Q74)
        twice, changed = rs.append(once, Q74)
        self.assertFalse(changed)
        self.assertEqual(once, twice)


class TestPrune(unittest.TestCase):
    def test_removes_only_the_named_issue(self):
        other = "- [#70 @b 2026-07-01] queue: recipes | issue=70 → shipped"
        out, changed = rs.prune(state(closed=[other, Q74]), "74")
        self.assertTrue(changed)
        self.assertEqual(rs.bullets(out, rs.CLOSED), [other])

    def test_restores_the_placeholder_when_emptied(self):
        out, _ = rs.prune(state(closed=[Q74]), "74")
        self.assertEqual(rs.bullets(out, rs.CLOSED), [])
        self.assertIn("_None._", out.split("## Missing components")[0]
                      .split("## User requests (closed this run)")[1])

    def test_idempotent(self):
        once, first = rs.prune(state(closed=[Q74]), "74")
        twice, second = rs.prune(once, "74")
        self.assertTrue(first)
        self.assertFalse(second)
        self.assertEqual(once, twice)


class TestRealStateFiles(unittest.TestCase):
    """The shipped state files must parse and expose all three sections."""

    def test_both_curator_states(self):
        for rel in ("recipes/curator-state.md", "catalog/curator-state.md"):
            path = REPO / rel
            with self.subTest(rel):
                self.assertTrue(path.exists(), f"{rel} missing")
                text = path.read_text()
                for section in rs.SECTIONS:
                    self.assertIsNotNone(
                        rs._span(text, section),
                        f"{rel} lacks '## User requests ({section})' — run "
                        f"request_state.py ensure-sections",
                    )
                # No entry may sit in two sections at once.
                seen: dict[str, str] = {}
                for section in rs.SECTIONS:
                    for line in rs.bullets(text, section):
                        issue = rs.issue_of(line)
                        if issue is None:
                            continue
                        self.assertNotIn(issue, seen,
                                         f"{rel}: #{issue} in both "
                                         f"{seen.get(issue)} and {section}")
                        seen[issue] = section


if __name__ == "__main__":
    unittest.main()
