---
title: BLAST (Bio-MCP)
parent: All tools
grand_parent: Catalog
tool_type: MCP server
supplier: Bio-MCP
availability: GA
tool_categories: [All]
last_verified: 2026-06-20
verification: works
verified_on: 2026-07-20
security: caution
security_on: 2026-07-20
security_note: "provenance matches Bio-MCP org, repo resolves but no LICENSE file upstream despite MIT claim and no push since 2025-06, no OSV advisories"
summary: "MCP server wrapping NCBI BLAST+ for nucleotide/protein similarity search and custom database creation, run locally over stdio."
---

# BLAST (Bio-MCP)

MCP server that lets Claude run NCBI BLAST+ sequence-similarity searches against local or custom databases.

| | |
|---|---|
| **Type** | MCP server (stdio; optional HTTP job queue) |
| **Supplier** | [Bio-MCP](https://github.com/bio-mcp/bio-mcp-blast) (community OSS) |
| **Availability** | GA — public GitHub repo, MIT-licensed |
| **Pricing** | Free / OSS (MIT) |
| **Capabilities** | Read/Write — runs BLAST+ binaries locally; can build databases (`makeblastdb`) |
| **Verified** | works · 2026-07-20 |
| **Security** | caution · 2026-07-20 — no LICENSE file upstream despite MIT claim, unmaintained since 2025-06, no OSV advisories |

## How to install

BLAST+ binaries must be on your `PATH` first, then clone and install the server.

1. **Install the BLAST+ binaries** (prerequisite — the server shells out to them):
   ```
   conda install -c bioconda blast
   ```
   (macOS alternative: `brew install blast`; Ubuntu: `sudo apt install ncbi-blast+`.)
2. **Clone and install the server**:
   ```
   git clone https://github.com/bio-mcp/bio-mcp-blast.git
   cd bio-mcp-blast
   pip install -e .
   ```
3. **(Optional) verify it starts**, then Ctrl-C — Claude launches the process itself via stdio, so you do **not** keep this running:
   ```
   python -m src.server
   ```
4. **Register it.**
   - **Claude Code** (stdio) — run from inside the cloned `bio-mcp-blast` directory so `$(pwd)` resolves, or substitute the absolute clone path:
     ```
     claude mcp add --transport stdio bio-blast -- python -m src.server
     ```
     (run this with the working directory set to your clone, e.g. `cd /path/to/bio-mcp-blast` first — replace `/path/to/bio-mcp-blast` with the absolute path of your clone, or `$(pwd)` if you are still inside it from the previous step)
   - **Claude Desktop** — add to `claude_desktop_config.json` (`cwd` must be the absolute path of your clone):
     ```json
     {
       "mcpServers": {
         "bio-blast": {
           "command": "python",
           "args": ["-m", "src.server"],
           "cwd": "/path/to/bio-mcp-blast"
         }
       }
     }
     ```
     (replace `/path/to/bio-mcp-blast` with the absolute path of your clone — e.g. `/Users/you/repos/bio-mcp-blast`)

## What it does

Exposes BLAST+ as MCP tools:

- `blastn` — nucleotide-vs-nucleotide search
- `blastp` — protein-vs-protein search
- `makeblastdb` — build a custom BLAST database from a FASTA file
- `blastn_async` / `blastp_async` — queue-based async variants for long searches
- `get_job_status` / `get_job_result` — monitor and retrieve async-job output

**Primary use cases**: Sequence-similarity search for gene/protein identification, screening contigs and amplicons against custom databases, microbial/metagenomic homology lookups.

## Notes

Primary transport is stdio (`python -m src.server`); Claude Code/Desktop launch the process. The async tools optionally use a separate HTTP job queue (`bio-mcp-queue`, `--queue-url http://localhost:8000`) for long-running searches — that queue is a long-lived service you must start separately and is not required for the synchronous `blastn`/`blastp` tools. Part of the broader Bio-MCP collection (samtools, bcftools, seqkit, bwa, bedtools, fastqc, interpro, evo2), each a discrete per-tool MCP server sharing this clone-and-`pip install -e .` pattern. Tagged `All` because sequence-similarity search is a cross-cutting primitive across every life-science domain.

## Sources

- [`bio-mcp/bio-mcp-blast`](https://github.com/bio-mcp/bio-mcp-blast)
- [Bio-MCP organization](https://github.com/bio-mcp)
- [NCBI BLAST+](https://blast.ncbi.nlm.nih.gov/)

---

## Installed this tool?

[Share feedback](https://github.com/scripps-ai-enablement/sci-ai-enabler/issues/new?template=tool-feedback.yml&tool=blast&details=Filed+from+https%3A%2F%2Fscripps-ai-enablement.github.io%2Fsci-ai-enabler%2Fcatalog%2Ftools%2Fblast.html%0A%0A) — install path, OS, errors, workarounds. The form opens with this tool pre-selected and a link back to this page.
