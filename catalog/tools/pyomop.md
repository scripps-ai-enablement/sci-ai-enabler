---
title: pyomop
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: Bell Eapen
availability: GA
tool_categories: [Translational Medicine]
last_verified: 2026-08-02
verification: degraded
verified_on: 2026-08-06
reviewed_on: 2026-08-06
verification_note: "documented pyomop-mcp-server entry point boot-errored in this run's smoke test (No such file or directory); fixed the install and registration blocks to the working pyomop --mcp-server subcommand and graded degraded pending a clean reboot next run"
security: cleared
security_on: 2026-08-06
security_note: "GPL-3.0 confirmed by fetching the repository LICENSE directly this run, matching the GitHub license field; resolved the prior license-absent flag"
summary: "Python OMOP CDM toolkit that ships an MCP server, letting Claude inspect and run SQL against an OHDSI CDM database on SQLite, PostgreSQL or MySQL"
---

# pyomop

A Python package for working with OHDSI OMOP Common Data Model databases that ships an MCP server, so Claude can list CDM tables, inspect their columns, and run validated SQL against a local or remote CDM instance.

| | |
|---|---|
| **Type** | MCP server (bundled in a Python package) |
| **Supplier** | [Bell Eapen](https://github.com/dermatologist/pyomop) (open source) |
| **Availability** | GA — PyPI `pyomop` 6.4.0; repo last pushed 2026-07-28 |
| **Pricing** | Free / OSS — **GPL-3.0** per the GitHub license field. Copyleft: redistributing a derived pipeline carries obligations. |
| **Capabilities** | Read/Write — SQL execution plus CDM schema creation, against a database you point it at |
| **Verified** | degraded · 2026-08-06 — pyomop-mcp-server boot-errored in smoke test; fixed to the working pyomop --mcp-server form |
| **Security** | cleared · 2026-08-06 — GPL-3.0 confirmed via direct LICENSE fetch, copyleft only |

## How to install

Requires **Python 3.11+** (`requires_python: >=3.11,<4.0`). Install the package first, then register the server.

- **Install**:
  ```
  pip install pyomop
  ```
  Add `pip install "pyomop[llm]"` for the LangChain-backed plain-text query path, or `pip install "pyomop[http]"` if you want the HTTP transport.
- **Verify it starts** (one-shot check — Ctrl-C once it boots; Claude Code and Claude Desktop launch the process themselves over stdio):
  ```
  pyomop --mcp-server
  ```
- **Claude Code** — stdio:
  ```
  claude mcp add --transport stdio pyomop -- pyomop --mcp-server
  ```
- **Claude Desktop** — add to `claude_desktop_config.json`:
  ```json
  {
    "mcpServers": {
      "pyomop": {
        "command": "pyomop",
        "args": ["--mcp-server"]
      }
    }
  }
  ```
  (A clean-install smoke test this run found the previously-documented `pyomop-mcp-server` console script absent from `PATH` after `pip install pyomop`, even though the package and its `mcp` dependency installed cleanly — so this page now points at the `pyomop --mcp-server` subcommand, which is the form the upstream README itself uses via `uv run pyomop --mcp-server`.)
- **HTTP transport** (optional; a long-lived service you must keep running in another terminal):
  ```
  pyomop-mcp-server-http --host 0.0.0.0 --port 8000
  ```

## What it does

Exposes eight tools over a SQLAlchemy connection to an OMOP CDM v5.4/v6 database:

- **Schema inspection** — `get_usable_table_names`, `get_table_columns`, `get_single_table_info`.
- **Querying** — `run_sql`, `check_sql` (validate a statement before executing it), `example_query`.
- **Setup** — `create_cdm` (build the CDM schema) and `create_eunomia` (load the OHDSI Eunomia demo dataset, useful for trying the server without patient data).

Backends: SQLite, PostgreSQL, MySQL. The package also converts result sets to pandas DataFrames and includes FHIR import utilities and an agent-assisted ETL migration CLI (`pyomop-migrate`) outside the MCP surface.

**Primary use cases**: exploratory querying of an OMOP CDM instance, cohort-count sanity checks, learning the CDM schema against the Eunomia demo database.

## Notes

`create_cdm` and `create_eunomia` are deliberately restricted to **local SQLite** databases upstream, to avoid destructive operations against a production CDM. `run_sql` is not so restricted — point this server at a real clinical database only with a read-only database role and the usual governance review, since the model composes the SQL.

The MCP server covers CDM data access; it does not bundle the OMOP vocabularies. Upstream suggests pairing it with a vocabulary service when Athena vocabularies are not loaded locally — see [OMOPHub MCP Server](omophub-mcp.html).

**GPL-3.0 confirmed** by fetching the repository's `LICENSE` file directly from the `develop` branch (the repo's default) this run — the PyPI metadata still leaves `license_expression` empty, but the rendered file matches the GitHub license field verbatim.

## Sources

- [`dermatologist/pyomop`](https://github.com/dermatologist/pyomop)
- [`pyomop` on PyPI](https://pypi.org/project/pyomop/)
- [OHDSI OMOP Common Data Model](https://ohdsi.github.io/CommonDataModel/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=pyomop&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fpyomop.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
