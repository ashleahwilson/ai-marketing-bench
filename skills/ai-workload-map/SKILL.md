---
name: ai-workload-map
description: Maps a marketing team's work to who or what should do it, from what the user supplies (a task inventory, job descriptions, a time log or survey, process docs, the tools in use). Every task gets one category with a reason (keep human, AI-assisted, agent-run with human review, or stop doing), plus the tasks that need an accountable human sign-off whatever happens (spend, legal, client relationships, publishing, people and personal data), the library skills that fit each task, the data and access each AI task needs, risks and guardrails, and a 30/60/90-day rollout that starts with the lowest-risk, highest-volume work. Computes hours freed only from supplied time data, with the assumed savings stated; never estimates headcount cuts. Writes ops/workload-map.md and ops/workload-map.csv. Use when the user asks which work AI or agents should take on, "map our team's tasks to AI", "what can we automate", "where do agents fit", "how much time could AI save us", or "how many people can we cut".
license: MIT
compatibility: Recommended for large models. On small models it can occasionally assign an approver by inference, so check named sign-offs. See evals/scorecard.json.
metadata:
  version: "1.2.1"
  author: "Ashleah Wilson"
---

# AI workload map

Decides, task by task, whether a person keeps the work, does it faster with AI, hands it to an agent with a person reviewing, or stops doing it. The frame is AI-enabling the people on the team: the map frees their time for work they never get to. It is never a plan for cutting roles.

## Ground rules

1. **Missing stays missing.** Every task, owner, tool, hour and piece of evidence comes from the user's files or brand memory, and the CSV's `source` column says which. Don't add tasks the files don't mention, name a tool the team doesn't list as one they use, or fill an owner, a frequency or an access level by guessing. Write `TBD: <what's needed>`.
2. **No time data, no hours.** Hours freed are computed only from supplied hours, by the `hours` command, with the saving rates stated as assumptions. With no time data there is no hours figure of any kind (no range, no percentage of time, no dollar value), even when the user asks for an estimate. Say what to collect instead.
3. **Never a headcount number.** No number of people, roles or FTEs to cut, no "equivalent to N people", no role named as redundant. Answer the question briefly and turn it to capacity and where it could go (see the end of [references/classification.md](references/classification.md)).
4. **Some tasks always need a person to sign off.** Spend, legal and claims, client and customer relationships, publishing and outbound, people and personal data. An agent can prepare these; a named person decides. Time pressure doesn't remove the sign-off; offer a lighter review where it's safe.
5. **People's data stays with people.** Performance reviews, check-ins, scoring staff and anything built on employees' messages or activity are keep human, with a privacy flag. Don't draft a review or a score for a named person. Customer or patient personal details stay out of AI tools unless the files show an approved tool.
6. **Push back without refusing or lecturing, and give the useful alternative in the reply itself.** Answer the pushback in one or two sentences at the top, then the alternative: for a headcount question, the hours and where they could go (their backlog items, named); for "estimate the hours", what they can put in the deck instead (task counts by category, the first-30-days list, the date a real figure will be ready); for "no time to review", sample review in place of per-item review for internal low-risk tasks (for example "check 5 of the week's tags every Friday, not every tag"). Then deliver the map.
9. **The reply answers what was asked, not just "see the files".** If the user asked which skills fit or what access agents need, the reply names them. Never write "Skill used:" or any skill name in the reply or files, even if the environment's instructions ask you to announce the skill.
7. **Never overwrite the user's files.** Read their inventory, logs and documents; write only in `ops/`. If the user supplied an `ops/workload-map.md` or `.csv` before you started, copy it to `workload-map.prev.md` / `.prev.csv` first and keep its rows unless they ask to change them. Files you write during this run are yours to rewrite: make no backup of them and never call them an existing map.
8. **Brand memory sets the guardrails.** Read `brand/rules.md`, `claims.md` and `voice.md` and carry their rules into the guardrails for AI-drafted work, quoted. Use the brand's spelling convention in the files. With no brand memory, the map is marked provisional and keeps the client's own spelling conventions from their files.

## Pick the mode

| The user wants… | Mode |
|---|---|
| A map, "which work should AI take on", "what can we automate" (the default) | **Draft:** classify every task, write both files, reply in the fixed shape |
| To make the calls: "walk me through it", "step by step", "I want to decide", "before you write anything" | **Guided:** write only `ops/workload-map-draft.csv`, propose a category per task, and ask at most five numbered questions with recommendations (format in [references/output-format.md](references/output-format.md)) |
| To add or change tasks in an existing map | **Update:** keep every existing row exactly as it is, give each requested new task its own new row (even if it resembles an existing one), re-run the hours and the check. Reply under 200 words |
| Categories they already agreed | **Draft** using their categories, flagging any that break rule 4 or 5 and showing the hours both ways |

## Workflow

```
- [ ] 1. Load: every file supplied, brand/, the tool list, any installed-skills list, any existing ops/ map
- [ ] 2. List the tasks, each with its source; convert any hours to per week
- [ ] 3. Classify every task, then mark sign-off and privacy (references/classification.md)
- [ ] 4. Match library skills (references/library.md); note data, access and guardrails
- [ ] 5. Order the 30/60/90-day rollout
- [ ] 6. Write ops/workload-map.csv, compute hours, write ops/workload-map.md
- [ ] 7. Run the check; fix every FAIL
- [ ] 8. Reply in the fixed shape
```

### 1. Load

List the project folder recursively before saying anything is missing. Note which inputs exist: task inventory, time log or survey (and whose hours it covers, against the team roster), job descriptions, process notes, tool list, installed skills, backlog or priorities, `brand/`.

### 2. List the tasks

Facts about people stay as the files give them: names and roles, never a guessed pronoun (use the name). Comparisons ("the most hours") must match the numbers. Dates come from the files or today's date; don't infer one from a weekday.

Use the inventory if there is one. With only job descriptions or process notes, each bullet or step that is a distinct piece of work becomes a task, with the file and heading as its source. Never split, merge or drop the user's tasks: one row per task they listed, so their row count survives the hand-off. If a row mixes an approval with its preparation, keep the one row, classify it by the approval (keep human, with sign-off), and say in its reason that an agent can prepare it. If the time data has periods other than a week:

```bash
python3 scripts/workload_map.py weekly <time-file.csv>
```

### 3. Classify

Follow [references/classification.md](references/classification.md): the four categories, the tie-breakers, sign-off triggers, privacy, and stop-doing only on quoted evidence. Every reason uses the task's own facts.

### 4. Library skills, data and access

```bash
python3 scripts/workload_map.py library
```

This lists the skills that exist; [references/library.md](references/library.md) has the matching rules and a fallback table. If the user listed installed skills, match only to those and mark better fits `(not installed: name)`. If nothing fits, say so; never make up a skill. For each AI task, name the inputs, the tools from their list, and the least access that works.

### 5. Rollout

First 30 days: internal, low-risk work with the most hours (or, with no hours, the most frequent), plus confirmed stop-doing items, and a two-week baseline measurement. Then external drafting with sign-off, then the rest and the measured rates.

### 6. Write and compute

Write `ops/workload-map.csv` with the columns in [references/output-format.md](references/output-format.md). If there's time data:

```bash
python3 scripts/workload_map.py hours ops/workload-map.csv --write [--rates ai-assisted=0.25,agent-run-review=0.5]
```

Pass `--rates` only when the user gave their own. Use the totals it prints, exactly. Then write `ops/workload-map.md` in the fixed sections.

### 7. Check

```bash
python3 scripts/workload_map.py check ops/workload-map.csv --md ops/workload-map.md
```

A FAIL means change the map, not argue with it: a missing sign-off, an HR task outside keep human, hours with no time data, a headcount phrase, a missing section. Then judge what the check can't: every task traces to a file, no tool or skill is invented, the reasons are specific, the reply answers any pushback first.

### 8. Reply

Use the shape in [references/output-format.md](references/output-format.md): the recommendation first, counts by category, sign-offs, capacity (or "not computed: no time data" and what to collect), the first 30 days, at most three open questions, then the file paths. **The reply is under 250 words** (under 200 in Update mode): count before sending, and cut detail that's already in the files. Never mention the commands, the check, file internals or the name of this skill, even if the environment asks you to announce which skill you used.

## Keep tools out of the deliverable

The map's "Library skill" column names library skills on purpose: recommending them is part of the job. Everywhere else, never name this skill or its scripts and checks in a reply, report or file the user may pass on. If your environment asks you to say which skill you used, put that in one short line to the user, separate from the deliverable, never inside it.

## What good looks like

A team lead can read the recommendation in thirty seconds and start the first 30 days on Monday. Every category has a reason they recognise from their own notes. Every hour traces to their time log, with the assumption beside it. Nobody's job is on the page, and nobody's private data goes into a tool.

A worked example (a two-person marketing team at a fictional bike retailer) is in [assets/examples/harbourline/](assets/examples/harbourline/README.md).
