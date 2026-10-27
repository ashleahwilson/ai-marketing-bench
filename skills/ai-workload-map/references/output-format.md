# Output format

## Contents
- ops/workload-map.csv (the hand-off file)
- ops/workload-map.md (the readable map)
- The reply
- Guided mode questions

## ops/workload-map.csv (the hand-off file)

One row per task, these columns in this order. Other tools and skills load this file, so keep the column names and the values exactly as listed.

| Column | Values |
|---|---|
| task_id | The user's ID if they have one (T1), otherwise T1, T2… in the order supplied |
| task | The task in the user's words |
| owner | Person or role from the files; `TBD` if none |
| source | The file the task came from (`task-inventory.csv`, `job-descriptions.md: Marketing Coordinator`) |
| category | `keep-human`, `ai-assisted`, `agent-run-review` or `stop-doing` |
| reason | One line from the task's own facts |
| human_signoff | `yes` or `no` |
| signoff_reason | Spend, legal, relationship, publishing, HR or personal data, and who if the files say; blank if no |
| privacy_flag | `yes` or `no` |
| library_skills | Skill names separated by `;`, or blank. Skills not installed are written `(not installed: name)` |
| data_access | Inputs, tools and the least access, or `TBD: <what's needed>` |
| guardrails | The rule that applies to this task, or blank |
| hours_per_week | Logged hours converted to per week; blank with no time data. Never estimated |
| saving_rate | Filled by the hours step (0 to 1); blank with no hours |
| hours_freed_per_week | Filled by the hours step; blank with no hours |
| rollout_phase | `30`, `60`, `90`, `later` or `none` (keep-human) |

Quote any cell with a comma in it.

## ops/workload-map.md (the readable map)

These sections, in this order, with these headings:

```
# AI workload map: <team or company>
<Status line: date · built from <files> · Draft | Provisional: no brand memory | Provisional: no time data>

## Recommendation
Three to five lines: what to start first and why, what stops, what stays human, and capacity freed
(the hours with the assumption, or "Not computed: no time data").

## The map
| ID | Task | Owner | Who does it | Why | Human sign-off | Library skill |
(one row per task; Who does it reads "Keep human", "AI-assisted", "Agent-run, human review" or "Stop doing")

## Human sign-off required
One line per task: task · trigger · who signs off.

## Data and access each AI task needs
One line per ai-assisted or agent-run task: inputs · tools · least access. TBD where unknown.

## Risks and guardrails
Three to six risks for this team, each with its guardrail. Quote brand rules that apply.

## 30/60/90-day rollout
First 30 days / Days 31–60 / Days 61–90, each a short list of task IDs with one line on why that order,
and what to measure.

## Capacity freed
With time data: total hours a week, by category, coverage, and the assumption sentence. Where the capacity
could go (the user's backlog or priorities; otherwise an open question).
With no time data: "Not computed: no time data." Then what to collect, from whom, for how long.

## Open questions
Gaps and decisions, each as a question with who can answer it.
```

Hours freed appear only as hours a week. Never FTEs, people, roles or salary.

## The reply

Under 250 words, counted (under 200 in Update mode), even with pushback. The detail lives in the files. Lead with the recommendation.

```
**Recommendation:** <what to start first, what stops, what stays human: one or two sentences>

**At a glance:** <n> keep human · <n> AI-assisted · <n> agent-run with review · <n> stop doing
**Needs a person to sign off:** <task: trigger>, …
**Capacity:** <hours a week freed, with the assumption> | Not computed: no time data. <what to collect>
**First 30 days:** <tasks>
**Open questions:** <at most three>

Files: ops/workload-map.md, ops/workload-map.csv
```

If the user asked something to push back on (a headcount number, skipping review, an agent judging staff, an hours estimate with no data), answer it first in one or two sentences, then give the alternative in the reply (capacity and where it goes; what goes in the deck instead; sample review replacing per-item review), then the shape above. If they asked a direct question (which skills, what access), add one line per task answering it. Never add a "Skill used:" line. Talk to the user in the second person.

## Guided mode questions

Write `ops/workload-map-draft.csv` only. The reply lists the proposed category for every task with its reason (one line each), then at most five numbered questions, the material calls only: a borderline category, a sign-off that changes a current habit, a stop-doing, a rate assumption. Each question carries your recommendation and the evidence:

```
1. Approve weekly bid changes: keep with Amara (spend), or let an agent prepare the changes for her
   to approve in one weekly sitting? Recommendation: the second.
```

End with: "Answer these and I'll write the final map."
