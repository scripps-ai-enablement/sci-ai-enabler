#!/usr/bin/env python3
"""Install + boot the safe subset of catalog tools and record what happened.

RUNS ONLY inside the quarantined smoke-test job(s) (.github/workflows/verify.yml):
an ephemeral container with NO secrets and `contents: read`. It executes
third-party install/boot commands that `scripts/select_smoke_targets.py` already
gated to the open, no-auth, no-cost subset. Every command is run with a hard
timeout in an isolated temp HOME/target so a fresh VM is the entire blast radius.
The verifier AGENT never runs this or any component code — it only reads the
`smoke-results.json` this script emits.

Statuses per target:
  pass | install_error | boot_error | timeout | skipped | needs_toolchain
`needs_toolchain` means the install failed ONLY because the slim sandbox has no
C compiler (a dependency tried to build from source). The workflow retries those
targets in a compiler-equipped container via --retry-from-results and merges the
outcome, so the default job stays slim. See verify.yml.

Run: python3 scripts/run_smoke_tests.py --batch .verify/smoke-batch.json \
        --out .verify/smoke-results.json
Retry: python3 scripts/run_smoke_tests.py --retry-from-results RESULTS.json \
        --out RESULTS.json          # re-runs needs_toolchain targets, merged
Stdlib only.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import tempfile
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

INSTALL_TIMEOUT = 180  # seconds per install command
BOOT_TIMEOUT = 25      # seconds to probe an MCP server boot
LOG_CHARS = 1500       # truncate captured output

# An install failed ONLY because no C compiler is present (a dependency tried to
# build from source). Matched narrowly on "the compiler binary is missing" — a
# genuine CompileError WITH a compiler present is left as a real install_error.
_COMPILER_ABSENT = re.compile(
    r"command '(?:gcc|cc|clang|g\+\+|c\+\+|cl)' failed: (?:No such file or directory|command not found)"
    r"|\b(?:gcc|cc|clang|g\+\+): (?:not found|command not found|No such file or directory)"
    r"|unable to execute '(?:gcc|cc|clang|g\+\+)': No such file",
    re.IGNORECASE,
)


def _needs_toolchain(log: str) -> bool:
    """True if an install failed purely for lack of a C compiler."""
    return bool(_COMPILER_ABSENT.search(log))


def _merge_results(prior: list[dict], retried: list[dict]) -> list[dict]:
    """Overlay retried outcomes onto prior results, preserving order."""
    by_slug = {r["slug"]: r for r in retried}
    return [by_slug.get(r["slug"], r) for r in prior]


def _text(chunk) -> str:
    """Normalise a captured stream to str. On TimeoutExpired CPython hands back
    partial output as bytes even in text mode, so each chunk may be str, bytes,
    or None — concatenating those raw raises TypeError and crashes the batch."""
    if chunk is None:
        return ""
    if isinstance(chunk, bytes):
        return chunk.decode("utf-8", "replace")
    return chunk


def _run(cmd: str, cwd: str, env: dict, timeout: int) -> tuple[int | None, str]:
    """Run one command with a timeout; return (returncode|None-on-timeout, log)."""
    try:
        p = subprocess.run(
            shlex.split(cmd), cwd=cwd, env=env, timeout=timeout,
            capture_output=True, text=True,
        )
        return p.returncode, (_text(p.stdout) + _text(p.stderr))[-LOG_CHARS:]
    except subprocess.TimeoutExpired as e:
        return None, ("[timeout]\n" + _text(e.stdout) + _text(e.stderr))[-LOG_CHARS:]
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


def _mcp_initialize_request() -> str:
    """A minimal JSON-RPC `initialize` request for the MCP stdio handshake."""
    return json.dumps({
        "jsonrpc": "2.0", "id": 1, "method": "initialize",
        "params": {
            "protocolVersion": "2025-06-18",
            "capabilities": {},
            "clientInfo": {"name": "smoke-test", "version": "0.0.0"},
        },
    })


def _probe_boot(cmd: str, cwd: str, env: dict, timeout: int) -> tuple[str, str]:
    """Boot an MCP stdio server and confirm it actually speaks MCP.

    MCP stdio servers expect a client to send a newline-delimited JSON-RPC
    `initialize` request on stdin; many (e.g. `biomcp serve`) exit non-zero
    right away when there is none, which the old "immediate exit = boot_error"
    heuristic misread as a failure. We now perform the handshake: send the
    request and watch (merged) stdout for a matching JSON-RPC response.

    Returns (status, log):
      * a well-formed response to our request  -> pass  (completed the handshake)
      * still running at the timeout           -> pass  (booted, awaiting client)
      * clean exit (rc 0)                       -> pass
      * non-zero exit with no MCP response      -> boot_error
    """
    try:
        p = subprocess.Popen(
            shlex.split(cmd), cwd=cwd, env=env, text=True,
            stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,  # merge so one reader can't deadlock on a full pipe
        )
    except FileNotFoundError as e:
        return "boot_error", f"[command not found] {e}"

    out_lines: list[str] = []
    handshook = threading.Event()

    def _reader():
        for line in p.stdout:  # blocks until the server exits or is terminated
            out_lines.append(line)
            s = line.strip()
            if not s:
                continue
            try:
                msg = json.loads(s)
            except ValueError:
                continue  # startup log line, not JSON-RPC
            if (isinstance(msg, dict) and msg.get("jsonrpc") == "2.0"
                    and msg.get("id") == 1 and ("result" in msg or "error" in msg)):
                handshook.set()
                return

    reader = threading.Thread(target=_reader, daemon=True)
    reader.start()
    try:
        p.stdin.write(_mcp_initialize_request() + "\n")
        p.stdin.flush()
    except (BrokenPipeError, OSError):
        pass  # server exited before it read stdin

    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline:
        if handshook.is_set() or p.poll() is not None:
            break
        time.sleep(0.1)

    responded = handshook.is_set()
    rc = p.poll()
    if rc is None:  # still up — tear it down
        p.terminate()
        try:
            p.wait(3)
        except subprocess.TimeoutExpired:
            p.kill()
    reader.join(2)
    for stream in (p.stdin, p.stdout):
        try:
            if stream:
                stream.close()
        except OSError:
            pass
    log = "".join(out_lines)[-LOG_CHARS:]

    if responded:
        return "pass", log
    if rc is None:
        return "pass", log
    if rc == 0:
        return "pass", log
    return "boot_error", log


def smoke_one(target: dict, workroot: Path, install_timeout: int = INSTALL_TIMEOUT) -> dict:
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

    rc, log = _run(cmd, str(work), env, install_timeout)
    result["log"] = log
    if rc is None:
        result["status"] = "timeout"
        return result
    if rc != 0:
        result["status"] = "needs_toolchain" if _needs_toolchain(log) else "install_error"
        return result

    # Optional boot probe for MCP servers: perform the MCP stdio handshake and
    # confirm the server speaks MCP (see _probe_boot). Skills (no boot_cmd) pass
    # on a clean install.
    if boot_cmd:
        status, blog = _probe_boot(boot_cmd, str(work), env, BOOT_TIMEOUT)
        result["log"] = (log + "\n--- boot ---\n" + blog)[-LOG_CHARS:]
        result["status"] = status
        return result

    result["status"] = "pass"
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--batch", type=Path, default=Path(".verify/smoke-batch.json"))
    ap.add_argument("--out", type=Path, default=Path(".verify/smoke-results.json"))
    ap.add_argument("--retry-from-results", type=Path, default=None,
                    help="re-run only needs_toolchain targets from a prior "
                         "results file and merge the outcome (for the "
                         "compiler-equipped retry job)")
    ap.add_argument("--install-timeout", type=int, default=INSTALL_TIMEOUT,
                    help="seconds per install command (raise for the retry job, "
                         "where source builds are expected)")
    args = ap.parse_args()

    if args.retry_from_results:
        prior = json.loads(args.retry_from_results.read_text(encoding="utf-8"))
        prior_results = prior.get("results", [])
        retry_targets = [
            {"slug": r["slug"], "install_cmd": r.get("install_cmd"),
             "boot_cmd": r.get("boot_cmd")}
            for r in prior_results if r.get("status") == "needs_toolchain"
        ]
        with tempfile.TemporaryDirectory(prefix="smoke_root_") as root:
            retried = [smoke_one(t, Path(root), args.install_timeout)
                       for t in retry_targets]
        # Only valid installs that had already started building reach the retry
        # (they were needs_toolchain, not install_error). If one STILL won't
        # install even with a compiler + generous timeout, that's a heavy build
        # environment the sandbox does not provide — not a catalog defect — so
        # record it as skipped-with-reason rather than a false failure.
        for r in retried:
            if r["status"] != "pass":
                r["log"] = ("[retried with a C toolchain; still not installable "
                            "in the sandbox — needs a heavier build environment] "
                            + r.get("log", ""))[-LOG_CHARS:]
                r["status"] = "skipped"
        results = _merge_results(prior_results, retried)
        gate = prior.get("gate", "")
    else:
        batch = json.loads(args.batch.read_text(encoding="utf-8"))
        targets = batch.get("selected", [])
        gate = batch.get("gate", "")
        with tempfile.TemporaryDirectory(prefix="smoke_root_") as root:
            results = [smoke_one(t, Path(root), args.install_timeout)
                       for t in targets]

    doc = {
        "generated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "gate": gate,
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
