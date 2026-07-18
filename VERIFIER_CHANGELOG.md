# Verifier changelog

Rolling, reverse-chronological log of catalog verification + security passes. Each scheduled or
on-demand run that produces changes prepends a dated block; the top block is mirrored to the pinned
"Verification updates" issue.

## 2026-07-18

### Added
- Bootstrapped the Verifier agent: `VERIFIER_AGENT.md`, the two-job `verify.yml` workflow
  (quarantined smoke-test job + sandboxed agent job), `scripts/select_smoke_targets.py` +
  `scripts/run_smoke_tests.py`, `catalog/verifier-state.md`, and the `verification` / `security`
  stamp schema (front-matter fields + metadata-table rows + area-card badges). No catalog entries
  stamped yet — the first bootstrap pass populates them.
