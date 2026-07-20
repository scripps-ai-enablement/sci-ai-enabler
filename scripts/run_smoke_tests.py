#!/usr/bin/env python3
"""Install + boot the safe subset of catalog tools and record what happened.

RUNS ONLY inside the quarantined smoke-test job (.github/workflows/verify.yml):
an ephemeral container with NO secrets and `contents: read`. It executes
third-party install/boot commands that `scripts/select_smoke_targets.py` already
gated to the open, no-auth, no-cost subset. Every command is run with a hard
timeout in an isolated temp HOME/target so a fresh VM is the entire blast radius.
The verifier AGENT never runs this or any component code — it only reads the
`smoke-results.json` this script emits.

Statuses per target: pass | install_error | boot_error | timeout | skipped.

Run: python3 scripts/run_smoke_tests.py --batch .verify/smoke-batch.json \
        --out .verify/smoke-results.json
Stdlib only.
"""
from __future__ import annotations

import argparse
import json
import os
import shlex
import subprocess
import tempfile
from datetime import datetime, timezone
from pathlib import Path

INSTALL_TIMEOUT = 180  # seconds per install command
BOOT_TIMEOUT = 25      # seconds to probe an MCP server boot
LOG_CHARS = 1500       # truncate captured output


def _run(cmd: str, cwd: str, env: dict, timeout: int) -> tuple[int | None, str]:
    """Run one command with a timeout; return (returncode|None-on-timeout, log)."""
    try:
        p = subprocess.run(
            shlex.split(cmd), cwd=cwd, env=env, timeout=timeout,
            capture_output=True, text=True,
        )
        return p.returncode, (p.stdout + p.stderr)[-LOG_CHARS:]
    except subprocess.TimeoutExpired as e:
        out = ((e.stdout or "") + (e.stderr or ""))
        if isinstance(out, bytes):
            out = out.decode("utf-8", "replace")
        return None, ("[timeout]\n" + out)[-LOG_CHARS:]
    except FileNotFoundError as e:
        return 127, f"[command not found] {e}"


def _prepare_install(cmd: str, work: Path, env: dict) -> str:
    """Adjust cmd + env so the install lands where the boot probe can reach it.

    Returns the (possibly rewritten) install command and mutates `env` in place:
      * pip  -> install into a temp --target and expose it on PYTHONPATH so a
                `python -m ...` boot probe can import it.
      * uv tool install -> uv drops executables in ~/.local/bin (HOME is our temp
                dir). Pin that bin dir and prepend it to PATH so the boot command
                (e.g. `biomcp serve`) can actually find the installed binary.
    """
    if cmd.startswith("pip install "):
        target_dir = work / "site"
        env["PYTHONPATH"] = str(target_dir)
        return cmd.replace("pip install ", f"pip install --target {target_dir} ", 1)
    if cmd.startswith("uv tool install "):
        bin_dir = work / ".local" / "bin"
        env["UV_TOOL_BIN_DIR"] = str(bin_dir)
        env["PATH"] = str(bin_dir) + os.pathsep + env.get("PATH", "")
    return cmd


def smoke_one(target: dict, workroot: Path) -> dict:
    slug = target["slug"]
    install_cmd = target.get("install_cmd")
    boot_cmd = target.get("boot_cmd")
    result = {"slug": slug, "install_cmd": install_cmd, "boot_cmd": boot_cmd,
              "status": "skipped", "log": ""}
    if not install_cmd:
        result["log"] = "no install command"
        return result

    # Isolate: fresh HOME (npx skills writes ~/.claude), fresh pip --target dir.
    work = Path(tempfile.mkdtemp(prefix=f"smoke_{slug}_", dir=workroot))
    env = dict(os.environ)
    env["HOME"] = str(work)
    env["PIP_DISABLE_PIP_VERSION_CHECK"] = "1"
    env.pop("ANTHROPIC_API_KEY", None)  # belt-and-suspenders: never expose secrets
    env.pop("GITHUB_TOKEN", None)

    cmd = _prepare_install(install_cmd, work, env)

    rc, log = _run(cmd, str(work), env, INSTALL_TIMEOUT)
    result["log"] = log
    if rc is None:
        result["status"] = "timeout"
        return result
    if rc != 0:
        result["status"] = "install_error"
        return result

    # Optional boot probe for MCP servers: a server that stays up until the short
    # timeout is treated as a successful boot; an immediate nonzero exit is a
    # boot_error. Skills (no boot_cmd) pass on a clean install.
    if boot_cmd:
        brc, blog = _run(boot_cmd, str(work), env, BOOT_TIMEOUT)
        result["log"] = (log + "\n--- boot ---\n" + blog)[-LOG_CHARS:]
        if brc is None:
            result["status"] = "pass"        # still running at timeout = booted
        elif brc == 0:
            result["status"] = "pass"
        else:
            result["status"] = "boot_error"
        return result

    result["status"] = "pass"
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", type=Path, default=Path(".verify/smoke-batch.json"))
    ap.add_argument("--out", type=Path, default=Path(".verify/smoke-results.json"))
    args = ap.parse_args()

    batch = json.loads(args.batch.read_text(encoding="utf-8"))
    targets = batch.get("selected", [])
    with tempfile.TemporaryDirectory(prefix="smoke_root_") as root:
        results = [smoke_one(t, Path(root)) for t in targets]

    doc = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "gate": batch.get("gate", ""),
        "count": len(results),
        "results": results,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(doc, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    # Console summary (the artifact is the source of truth).
    for r in results:
        print(f"{r['status']:14s} {r['slug']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
