# Builder brief: one skill for AI Marketing Bench

You are building ONE skill for the AI Marketing Bench library, a library of marketing and GTM skills for AI agents that must be measurably better than public versions, and must prove it with published, blind-graded test results. The skill name and its scope are in your task message.

Repo: this repository (by Ashleah Wilson, MIT licence). Below, `<repo>` is its absolute path and `<runs>` is a folder outside it for eval runs, such as `../ai-marketing-bench-runs`. Run commands from the repo root.

## Read first (in this order)

1. `STANDARD.md`: the 17-item Bench Standard. Your skill must meet all of it.
2. `bench/README.md`: how evals are planned, run, graded and aggregated.
3. One finished exemplar, end to end: `skills/content-qa-gate/` (SKILL.md, references/, scripts/, evals/evals.json, evals/files/, assets/examples/, CHANGELOG.md, evals/scorecard.json). Also skim `skills/brand-voice-gate/SKILL.md` and `skills/brand-memory/SKILL.md` (the brand memory format every skill reads: `brand/` folder, source tags `[source: …, date · confirmed|provisional|assumed]`, `TBD:` gaps).
4. The comparison skill(s) named in your task, if any. Read them fully: your job is to beat them on the tests.

## Hard rules

- **Only write inside `skills/<your-skill>/`** and your run folder `<runs>/<your-skill>/`. Never edit `packs.json`, `README.md`, `.claude-plugin/`, `scripts/`, `bench/`, or any other skill. Never commit or push. Another agent integrates your work.
- Never send, post, schedule or create anything outside those folders (no tasks, chips, sessions, emails). No web research needed; if you do any, never put user data into it.
- Every company in fixtures and examples is fictional. Reuse the existing fictional brands where they fit: Tallyhouse (restaurant bookkeeping; brand memory at `skills/brand-voice-gate/evals/files/tallyhouse-brand/brand/`), Quillmetrics (Shopify revenue analytics; `skills/brand-voice-gate/evals/files/quillmetrics-brand/brand/`), Ferncliff (dental clinic scheduling, no brand memory), Pipewise (B2B sales software, see `skills/reach-out`). Copy fixtures into your own `evals/files/`; don't reference other skills' folders at runtime.
- Writing rules for everything you write (skill text, examples, replies the skill produces): Canadian spelling (behaviour, colour, centre, organization, program); em dashes very sparingly; direct, plain, anti-hype; never the words "mid-market"; no openers like "Most companies/teams/leaders…"; no reassurance by denial. Write the skill's prose the way `skills/content-qa-gate/SKILL.md` reads.

## Method (follow in order)

1. **Scope.** Decide exactly what the skill does and doesn't do, its modes, its fixed output shape, and its hand-off files (what it reads from other library skills, what it writes for the next one). Keep it to one job.
2. **Evals first.** Write `evals/evals.json` (format: see the exemplar; `files`, `files_dest` or `files_dest_map`, `expectations`, `"trap": true`) with **at least 8 evals, at least 2 traps** (the right answer is to push back, hold, ask, or not invent). Plant specific, checkable problems in the fixtures. Expectations must be literal and gradeable from the output alone, written before any run. Include at least one eval with no brand memory, one where the skill must not invent facts, and one that tests a hand-off file or a mode. Make some expectations hard enough that a strong model without the skill can fail them (skills that hit 100% every round can't be told apart from their next version).
3. **Build the skill** to the Standard: `SKILL.md` (under ~200 lines, third-person description ≤1,024 chars saying what and when, `license: MIT`, `metadata.version: "1.0.0"`, `metadata.author: "Ashleah Wilson"`), `references/` one level deep (a `## Contents` section on any file over 100 lines), a **stdlib-only Python script** for anything mechanical (counting, format checks, consistency, tracing claims to sources), a worked example in `assets/examples/` that is **different from every eval** (so runners can't copy an answer), and `CHANGELOG.md`. The skill must: read `brand/` and work without it (marked provisional), trace every fact to a source and never invent ("missing stays missing"), self-check before replying, use a fixed output shape that leads with the recommendation, push back without refusing or lecturing, never mention its scripts, file internals, its own name or other skills' names to the user or in any deliverable (reports go to clients: the test machine's global instructions may ask agents to announce which skill they use, and that must not leak into a client-facing file or reply), and never overwrite the user's original files. If the environment applies its own writing rules (for example Canadian spelling), a client deliverable with no brand memory keeps the client's own conventions.
4. **Lint:** `python3 scripts/lint_skill.py skills/<your-skill> --strict` must PASS.
5. **Run round 1** (from the repo root):
   ```
   python3 bench/plan.py skills/<s> <runs>/<s> --iteration 1 --configs with-skill:haiku,no-skill:haiku,comparison-skill:haiku,with-skill:opus,no-skill:opus --comparison <path to comparison skill>
   python3 bench/run_headless.py <runs>/<s>/iteration-1 --parallel 3
   ```
   Drop `comparison-skill:haiku` and `--comparison` if there's no comparison skill. Each run is isolated from the test machine (no CLAUDE.md, installed skills or MCP servers), so only the skill under test shapes the output. Re-run the same command to resume runs that crashed (it skips finished ones). Check every run has `outputs/response.md`.
6. **Grade blind, with a separate agent.** You must not grade your own runs. Fill `bench/prompts/grader.md` with `{evals_path}` and `{workspace}` (add eval-specific grading clarifications at the end, and tell the grader to read nothing in your skill folder except `evals/evals.json` and `evals/files/`), save it to the run folder as `grader-prompt-<n>.md`, then run a fresh headless grader:
   ```
   cd <runs>/<s>/iteration-1 && claude -p "$(cat ../grader-prompt-1.md)" --model opus --permission-mode acceptEdits --allowedTools Read Write Glob Grep "Bash(python3:*)" --setting-sources "" --strict-mcp-config --disable-slash-commands --add-dir <runs>/<s> --add-dir <repo>/skills/<s>/evals > grader-report.md
   ```
   Then `python3 bench/aggregate.py <runs>/<s>/iteration-1` for the table. **Its columns are alphabetical (comparison-skill, no-skill, with-skill), not plan order: read the header row.**
7. **Fix and re-run, at most two more rounds**, on `with-skill:haiku` (add `with-skill:opus` once at the end if you changed anything significant). Fix real failures in the skill, not by weakening expectations. Only clarify an expectation if the grader shows it is genuinely ambiguous, and then re-grade every config on it. Bump the version and add a CHANGELOG entry each round.
8. **Scorecard.** Write `evals/scorecard.json` in the exemplar's format: method, every config's result, Haiku by round, and `losses_and_open_issues` listing every lost test and every invented fact found, honestly. Set `status`: "Meets the Bench Standard bar" only if it beats no skill and the comparison skill on total, is never worse on traps, and has no invented facts in any with-skill output in the final round; otherwise say exactly which part fails. If the bar is met only on large models, add to SKILL.md frontmatter: `compatibility: Recommended for large models. <one-sentence caveat>. See evals/scorecard.json.`
9. Final lint `--strict` PASS.

## Report back (your final message)

Keep it under 300 words:
- What the skill does (2 sentences) and its hand-offs (reads / writes).
- A score table: every config, every round.
- Bar status, and the open issues in one line each.
- Anything another skill or the integrator must know (for example a file format other skills should read).
