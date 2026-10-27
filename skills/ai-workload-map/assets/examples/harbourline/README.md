# Worked example: Harbourline Cycles

Harbourline Cycles is a fictional two-store bike retailer with a two-person marketing team (Amelia Grant and Luis Ortega). No results are claimed.

Input:
- `team/tasks.csv`: eight tasks with hours, some per month
- `team/tools.md`: the tools they use
- `brand/rules.md`: two brand rules

Output:
- `reply.md`: the reply
- `ops/workload-map.csv`: the hand-off file, one row per task
- `ops/workload-map.md`: the readable map

## Decisions worth noticing

| Task | Category | Why |
|---|---|---|
| Product descriptions (5 h/week, the most hours) | AI-assisted, month two | It's the biggest task, but it's published, so it waits until the internal pilots have shown the review routine works |
| Weekly sales summary | Agent-run, human review, month one | Same figures every week, read only by the owners. No library skill does recurring reports, so the map says so rather than stretching one |
| Flyer print approval | Keep human | Spend. An agent could prepare the quote comparison; Amelia still decides |
| Faxing price lists | Stop doing | The notes say both partners asked for email in 2025: evidence, not a hunch |

## Hours

Monthly hours were converted to weekly (× 12 ÷ 52) before anything was added: the newsletter's 6 hours a month is 1.38 a week. The 4.54 hours a week freed come only from the logged hours and the stated default rates, and the map says to replace the rates with measured ones after the pilot. The map never turns hours into people.
