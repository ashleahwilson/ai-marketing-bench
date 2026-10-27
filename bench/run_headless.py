#!/usr/bin/env python3
"""Run every planned eval in a fresh headless Claude Code session. Standard library only.

Usage:
    python3 bench/run_headless.py WORKSPACE/iteration-N [--parallel 4] [--only with-skill-haiku] [--dry-run]

Reads runs.json (from bench/plan.py). For each run, invokes:
    claude -p "<runner prompt>" --model <model> --permission-mode acceptEdits
           --allowedTools Read Write Edit Glob Grep "Bash(python3:*)" --add-dir <skill and run folders>
           --setting-sources "" --strict-mcp-config --disable-slash-commands
The last three flags isolate each run from the machine it runs on: no user or project CLAUDE.md, no installed
skills or plugins, no MCP servers. Only the skill under test (read by path from its prompt) shapes the output.
Each run's transcript goes to <run>/transcript.txt; runs that already have outputs/response.md are skipped,
so an interrupted iteration can be resumed by running the command again.

Needs the `claude` CLI on PATH and an account that can run headless sessions. Runs use real model calls.
"""

import argparse
import concurrent.futures as cf
import json
import os
import subprocess
import sys

# Keep the tester's own setup out of the runs (see the module docstring)
ISOLATION = ["--setting-sources", "", "--strict-mcp-config", "--disable-slash-commands"]
TIMEOUT_S = 900  # 15 minutes; long list runs (9+ contacts) took up to ~4 minutes in testing


def run_one(r, dry):
    run_dir = os.path.dirname(r["out_dir"])
    if os.path.isfile(os.path.join(r["out_dir"], "response.md")):
        return r, "skipped (already has response.md)"
    dirs = sorted({run_dir, os.path.dirname(run_dir)} | ({r["skill_dir"]} if r.get("skill_dir") else set()))
    cmd = ["claude", "-p", r["prompt"], "--model", r["model"], "--permission-mode", "acceptEdits",
           "--allowedTools", "Read", "Write", "Edit", "Glob", "Grep", "Bash(python3:*)"] + ISOLATION
    for d in dirs:
        cmd += ["--add-dir", d]
    if dry:
        return r, "dry run: " + " ".join(cmd[:6]) + " …"
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT_S, cwd=r["out_dir"], stdin=subprocess.DEVNULL)
        open(os.path.join(run_dir, "transcript.txt"), "w").write(p.stdout + "\n--- stderr ---\n" + p.stderr)
        ok = os.path.isfile(os.path.join(r["out_dir"], "response.md"))
        return r, "done" if ok else f"finished without response.md (exit {p.returncode})"
    except subprocess.TimeoutExpired:
        return r, f"timed out after {TIMEOUT_S}s"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("iteration_dir")
    ap.add_argument("--parallel", type=int, default=4)
    ap.add_argument("--only", help="run only this config, e.g. with-skill-haiku")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    runs = json.load(open(os.path.join(a.iteration_dir, "runs.json"), encoding="utf-8"))
    if a.only:
        runs = [r for r in runs if r["config"] == a.only]
    print(f"{len(runs)} run(s), {a.parallel} at a time")
    failed = 0
    with cf.ThreadPoolExecutor(max_workers=a.parallel) as ex:
        for r, status in ex.map(lambda r: run_one(r, a.dry_run), runs):
            print(f"eval {r['eval']:>3}  {r['config']:<22} {status}")
            failed += not (status.startswith(("done", "skipped", "dry run")))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
