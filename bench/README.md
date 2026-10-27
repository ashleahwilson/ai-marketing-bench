# The bench: how skills are tested

Two tools live here:
- **Evals** prove that a skill improves output.
- **The library scan** grades how skills are built.

## Evals (the Bench Standard, items C13–C17)

```
plan  ->  run  ->  grade  ->  aggregate
```

**1. Plan.** Create a folder per eval and config. Each prompt file has no expectations in it, so runners can't see them.

```bash
python3 bench/plan.py skills/reach-out ../ai-marketing-bench-runs/reach-out --iteration 6 --configs with-skill:opus,with-skill:haiku,no-skill:haiku
```

Add `comparison-skill:haiku --comparison <path>` to compare against the closest public skill.

**2. Run.** Each entry in `runs.json` is a self-contained prompt for a fresh agent. Either hand the entries to subagents, or run them headless with your own Claude login:

```bash
python3 bench/run_headless.py ../ai-marketing-bench-runs/reach-out/iteration-6 --parallel 4
```

Each run is isolated from your machine: it loads no user or project CLAUDE.md, no installed skills or plugins and no MCP servers, so only the skill under test shapes the output. Run the grader with the same flags (`--setting-sources "" --strict-mcp-config --disable-slash-commands`). Runs that already have a `response.md` are skipped, so re-running resumes an interrupted iteration. Add `--dry-run` to see the commands without making model calls.

**3. Grade.** Give a separate agent `bench/prompts/grader.md`, with `{evals_path}` and `{workspace}` filled in. It writes a `grading.json` per run. The grader must never be the agent that wrote the skill.

**4. Aggregate**, and write the published scorecard:

```bash
python3 bench/aggregate.py ../ai-marketing-bench-runs/reach-out/iteration-6 --scorecard skills/reach-out --version 3.1.0
```

Keep run folders outside the repo. They're large, and only the scorecard is published.

## Library scan

```bash
python3 bench/scan_library.py scan/2026-10 <cloned-library> [<cloned-library> ...]
```

This scores every SKILL.md on routing, structure, portability, evidence and safety, then writes `results.json`, `results.csv` and `summary.md`. It reads files and never executes them. See `scan/2026-10/report.md` for the October 2026 results and method.
