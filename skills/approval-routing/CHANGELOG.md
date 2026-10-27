# Changelog

## 1.2.1 (2026-10-27)
- Skill and script names stay out of replies and deliverables. Integration change, not re-run.

## 1.2.0 (2026-10-27)
Round 2 (Haiku 64/65): the one loss was a 219-word reply to an approved piece.
- An approved piece gets a reply under 100 words: status, who signed which version, the file. No timing line, no unflagged judgment calls, no type question unless it changes who signs.
- No rewriting the piece unasked; the reply names the words that must change.
- Reply lines must agree with the status.

## 1.1.0 (2026-10-27)
Round 1 (Haiku 64/65, Opus 64/65; no skill 41 and 53): fixes from the grader's notes.
- Never names the method, its mode or helpers, the system date, or absolute paths in a reply or file (two runs opened with the method's name; one cited the system date).
- A missing request date is written as "not given", never filled with today's date.
- Never suggests softening a claim, including regulated ones such as "HIPAA-compliant".
- Says plainly when the approval list has no line for the content type.
- The router reports the business days spare before go-live, so the reply can't overstate slack.

## 1.0.0 (2026-10-24)
- First release:
  - Three modes: Draft (route and file), Guided (questions first, no file), Status (where it stands, re-routed for the current version).
  - Nine triggers found in the content itself: performance claim, comparative claim, price or offer, customer named, regulated health, financial and employment topics, spend over a threshold, brand change; with guidance on what isn't a trigger.
  - Reads and writes the shared approvals format (copied from the editorial review cycle, unchanged), plus backward-compatible routing extensions: `order:`, `sla:` and `self-approval:` fields on type lines, and `trigger:` lines that readers of the shared format ignore.
  - Self-approval with backups, sign-offs checked against the version they cover, customer consent from `brand/proof.md`, brand-rule breaches as blockers no sign-off clears.
  - `route.py route`: trigger candidates, route, due dates in business days, go-live fit, sign-off status. `route.py check`: fails an unsupported "Approved", a missing approver, a counted self-approval, an unreported breach or missing consent, missing sections and leaked internals.
  - Writes `<name>-route.md`; never overwrites earlier route files.
