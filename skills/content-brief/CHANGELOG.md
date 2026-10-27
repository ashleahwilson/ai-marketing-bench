# Changelog

## 1.2.1 (2026-10-27)
- Skill and script names stay out of replies and deliverables (a test machine's global instruction to announce skills leaked into client-facing replies in several runs). Text-only change, not re-run.

## 1.2.0 (2026-10-23)
Round 2 (Haiku 58/58): the grader found small unsourced generalizations in angles ("most of the reader's week…"), a brief marked ready with blocking TBDs, a textbook formula held for a source, and a user-supplied `.example` URL questioned.
- No claims about reader behaviour or proportions in the angle or outline unless sourced; textbook definitions need no source.
- `ready` only when nothing blocks the writer; otherwise `draft`.
- User- and brand-supplied URLs count as real, including `.example`.
- Round 3 (Haiku 58/58, Opus 58/58): added the compatibility note; small fact-widening remains on both models (see evals/scorecard.json).

## 1.1.0 (2026-10-23)
Round 1 (Haiku 58/58, Opus 58/58): no failed expectations, but the grader found internals and a stray name in Haiku output.
- Replies and briefs never name this skill, its references or its default ranges ("a typical LinkedIn length").
- "Who can answer" is the user or a person named in brand memory, never a name from outside it.

## 1.0.0 (2026-10-23)
- First release:
  - Modes: Draft, Ask (one round, at most four questions), Guided, Draft with gaps, Hold.
  - Writes `briefs/<slug>.md` in the content-qa-gate brief format, with the writer's section (angle, outline, sources, search, avoid, open items) after the nine fields.
  - Must-includes only from confirmed brand facts or the user; third-party statistics and unconfirmed quotes flagged; keywords unvalidated unless the user supplies data.
  - Pushes back on audiences or offers brand memory rules out, and on topics that depend on held claims.
  - `check_brief.py`: the nine fields as content-qa-gate parses them, duplicate field names, CTA URL, length and date format, keyword line, search figures without data, figures traced to brand memory, keyword data or the request, banned phrases and held claims outside Avoid.
