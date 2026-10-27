# Changelog

## 1.2.1 (2026-10-27)
- Skill and script names stay out of replies and deliverables. Integration change, not re-run.

## 1.2.0 (2026-10-27)
Round 2 (Haiku 65/67):
- Pushback comes with the alternative in the reply itself: capacity and named backlog items for a headcount question, what can go in the deck instead of an hours estimate, sample review that replaces per-item review when there's no time to review.
- The reply answers direct questions (which skills, what access) instead of pointing to the files; guided replies give a reason per task.
- No "Skill used:" line in the reply or files, even when the environment asks for one.

## 1.1.0 (2026-10-27)
Round 1 (Haiku 63/67, Opus 66/67; no skill 38/67 on both):
- Replies are under 250 words, counted (under 200 in Update mode). Both models ran to 264–277 words on an update with pushback.
- Never split, merge or drop the user's rows: a mixed approval-and-preparation row stays one row, classified by the approval. Update mode gives each new task its own row.
- Backups only for maps the user supplied; never call the run's own draft an existing map.
- Every task that touches a tool lists its access, including approvals (agent read-only, person decides). Prospect and customer contact records get a privacy flag.
- No guessed pronouns, comparisons must match the numbers, no dates inferred from weekdays, and no skill name in the reply even if the environment asks for one.

## 1.0.0 (2026-10-24)
- First release:
  - Four categories per task (keep human, AI-assisted, agent-run with human review, stop doing), each with a reason from the task's own facts; stop doing only on quoted evidence.
  - Human sign-off on spend, legal and claims, client relationships, publishing and outbound, people and personal data, whatever the category. Performance and HR tasks stay human with a privacy flag.
  - Library skills matched from the live library index or the user's installed list; a fallback table in `references/library.md`.
  - Data and access per AI task (least access, only listed tools), risks and guardrails from brand memory, and a 30/60/90-day rollout ordered by risk, then volume.
  - `workload_map.py`: library index, weekly conversion of time logs, hours freed from supplied hours only (stated rates, coverage), and a check of the map (columns, sign-offs, privacy, arithmetic, rollout order, headcount language, required sections).
  - Draft, Guided and Update modes. Writes `ops/workload-map.md` and `ops/workload-map.csv`; never gives a headcount figure.
