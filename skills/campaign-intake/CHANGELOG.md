# Changelog

## 1.2.1 (2026-10-27)
- Skill and script names stay out of replies and deliverables. Integration change, not re-run.

## 1.2.0 (2026-10-27)
Round 2 (Haiku 75/76): on the BFCM trap Haiku said nothing could ship by the deadline, and on the webinar it re-dated the whole series over a one-day gap against the rough floor, colliding two sessions.
- The scoped-down version names what goes live by the original date whenever existing assets allow.
- A floor within about three days of the time available is tight, not "doesn't fit".
- Never move a requester's event date to fit the floor; cut scope for that date, and never create a date clash.
- "Likely" answers only when brand memory suggests one.

## 1.1.0 (2026-10-27)
Round 1 (Haiku 72/76, Opus 74/76): replies ran long on clean and Update requests, Haiku asked three non-blocking questions on a complete request, picked one of two candidate success metrics, used a name from its environment, and wrote method words ("lead-time table") into intakes.
- Reply length limits by status (ready under 150 words, Update under 200), at most five flags.
- A complete request gets no questions; definitions, exports and baselines are assumptions.
- Two candidate success metrics with no choice: ask which one counts.
- Names only from the request, the user's message or brand memory.
- One intake file per request; no method words in the file (the validator now catches them).

## 1.0.0 (2026-10-24)
- First release:
  - Three modes: Draft (full intake, open items marked), Guided (questions first, no file), Update (apply answers to an existing intake and log them).
  - A fixed intake format (`references/intake-format.md`): 19 fields, value conventions (`unknown:`, `assumed:`, `open:`, `none`), four statuses, a plain-language route vocabulary, and how brief and build steps read it.
  - Judgment rules for which questions to ask (at most four, each changing the plan), feasibility with lead-time floors and a scoped-down version, conflicting asks kept apart, claims, quotes and audiences checked against brand memory, and risks.
  - `check_intake.py`: required fields, placeholders, dates against a supplied today, numeric budgets, statuses, route terms, question count, open fields against status, held or banned brand phrases in the fields, internal names, working days and a rough lead-time floor, and claims in the request to judge.
