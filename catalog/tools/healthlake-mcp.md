---
title: AWS HealthLake MCP Server
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: AWS Labs
availability: GA
tool_categories: [Translational Medicine]
last_verified: 2026-07-19
summary: Apache-2.0 MCP server for AWS HealthLake FHIR datastores — CRUD, advanced search, patient-everything, and import/export jobs, with a read-only safety mode.
---

# AWS HealthLake MCP Server

Open-source MCP server that connects Claude to AWS HealthLake FHIR datastores for reading, searching, and (optionally) writing clinical resources, with automatic datastore discovery.

| | |
|---|---|
| **Type** | MCP server |
| **Supplier** | [AWS Labs](https://github.com/awslabs/mcp/tree/main/src/healthlake-mcp-server) |
| **Availability** | GA — distributed on PyPI as `awslabs.healthlake-mcp-server` (Apache-2.0) |
| **Pricing** | Free / OSS (Apache-2.0). Requires an AWS account; AWS HealthLake usage is billed by AWS, and FHIR data is HIPAA-eligible on AWS. |
| **Capabilities** | Read/Write — full FHIR R4 CRUD, search, and bulk import/export; `--readonly` flag blocks all mutating operations |

## How to install

- **Claude Code** — direct stdio add via `uvx` (requires [uv](https://docs.astral.sh/uv/) installed):

  ```
  claude mcp add --transport stdio healthlake --env AWS_REGION=us-east-1 --env AWS_PROFILE=your-profile-name -- uvx awslabs.healthlake-mcp-server@latest
  ```

  (replace `your-profile-name` with a configured AWS CLI profile, and `us-east-1` with the region hosting your HealthLake datastore. Add `--readonly` after `@latest` — i.e. `-- uvx awslabs.healthlake-mcp-server@latest --readonly` — to disable writes.)

- **Claude Desktop** — add to `claude_desktop_config.json`:

  ```json
  {
    "mcpServers": {
      "healthlake": {
        "command": "uvx",
        "args": ["awslabs.healthlake-mcp-server@latest"],
        "env": {
          "AWS_REGION": "us-east-1",
          "AWS_PROFILE": "your-profile-name",
          "MCP_LOG_LEVEL": "INFO"
        }
      }
    }
  }
  ```

  This is a stdio server — Claude Desktop/Code launches the `uvx` process itself, so there is no long-running service to keep open in a separate terminal. (To verify the server boots before wiring it up, run `uvx awslabs.healthlake-mcp-server@latest` once in a terminal and Ctrl-C after it initializes.)

- **Docker** — pre-built image, credentials passed as environment variables:

  ```
  docker run -e AWS_ACCESS_KEY_ID=<key> -e AWS_SECRET_ACCESS_KEY=<secret> -e AWS_REGION=us-east-1 awslabs/healthlake-mcp-server
  ```

## What it does

- **list_datastores**, **get_datastore_details** — automatic discovery of available HealthLake datastores, exposed as MCP resources (no manual datastore-ID configuration).
- **read_fhir_resource**, **create_fhir_resource**, **update_fhir_resource**, **delete_fhir_resource** — FHIR R4 CRUD by resource type and ID.
- **search_fhir_resources** — advanced search: chained parameters, `_include`/`_revinclude`, modifiers, date/number prefixes, and pagination.
- **patient_everything** — the FHIR `$everything` operation to pull a full patient record graph.
- **start_fhir_import_job**, **start_fhir_export_job**, **list_fhir_jobs** — bulk import/export job management.

**Primary use cases**: EHR-backed cohort review, agentic clinical-data workflows over HealthLake, patient-record summarization, and bulk FHIR ETL orchestration.

## Notes

Authentication uses AWS Signature V4 with standard credential resolution (IAM roles, `AWS_PROFILE`, or `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY` env vars); the invoking principal needs HealthLake IAM permissions (`healthlake:ListFHIRDatastores`, `healthlake:DescribeFHIRDatastore`, and the FHIR resource actions). Use `--readonly` for production, audit, or compliance scenarios where writes must be blocked. AWS HealthLake is a HIPAA-eligible service, but a Claude configuration is only appropriate for PHI when covered under the applicable BAA and required settings — see Anthropic's healthcare BAA guidance. Distinct from the vendor-agnostic FHIR MCP servers ([WSO2](fhir-wso2.html), [Momentum](fhir-momentum.html)): this one is AWS HealthLake-specific and adds datastore discovery plus bulk import/export.

## Sources

- [`awslabs/mcp` — `src/healthlake-mcp-server`](https://github.com/awslabs/mcp/tree/main/src/healthlake-mcp-server)
- [HealthLake MCP Server docs](https://awslabs.github.io/mcp/servers/healthlake-mcp-server)
- [Building healthcare AI agents with the AWS HealthLake MCP server (AWS blog, 2026-01-07)](https://aws.amazon.com/blogs/industries/building-healthcare-ai-agents-with-open-source-aws-healthlake-mcp-server/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=healthlake-mcp&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fhealthlake-mcp.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
