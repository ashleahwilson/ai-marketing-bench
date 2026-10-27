# Changelog

## 1.2.2 (2026-10-27)
- Skill and script names stay out of replies and deliverables (a test machine's global instruction to announce skills leaked into client-facing replies in several runs). Text-only change, not re-run.

## 1.2.1 (2026-10-24)
- Don't guess pronouns from first names; use the person's name or "they" unless a source states their pronouns. Both models guessed in round 3. Not re-run.

## 1.2.0 (2026-10-23)
Round 2 (Haiku 65/66): the no-brand-memory reply didn't offer to set one up; runs volunteered email patterns nobody asked for, stretched a page's save date into a posting date, miscounted CRM rows, wrote a Guided-mode file before the user answered, and ran 400-500 words.
- The no-brand-memory line always carries the offer to set one up.
- No email patterns or guesses unless asked.
- Facts cite the file that says them; save dates aren't posting or start dates; rows are counted.
- Guided mode writes the contacts file only after the user answers.
- Shorter reply table; the user's brand is "your"; saved paths are relative.

## 1.1.0 (2026-10-23)
Round 1 (Haiku 64/66, Opus 66/66): Haiku declined personal data without naming the consent risk of texting, and a no-sources reply didn't say personas would be provisional. Runners also found three gaps in the instructions.
- The personal-data decline must name the consent risk, in the same one or two sentences.
- With no brand memory, the reply always says personas are provisional, including the no-sources reply.
- Guided mode: unsettled roles are written as the likely value plus "(proposed)"; "Start with" names only someone already in motion, otherwise "pending your answers".
- Undated sources are written as `undated` (the checker warns instead of failing) and flagged.

## 1.0.0 (2026-10-23)
- First release:
  - Maps one account's buying committee from supplied sources (team pages, org charts, CRM and LinkedIn exports, call notes, job postings), with seven roles, evidence, dates, confidence and brand-memory personas.
  - Recommends who to contact first and in what order, plans around blockers, and names gaps, including roles being hired.
  - Flags people who left, titles older than a newer source, sources over 12 months old, wrong-company rows, and accounts outside the brand's audience.
  - Never names people without a source, never sources personal emails or mobile numbers, and labels guessed work emails unverified (only on request).
  - Draft and Guided modes.
  - Writes `accounts/<company>/contacts.md` for outreach drafting; `check_contacts.py` validates it (fields, allowed roles and statuses, dated sources, unlabelled or personal emails, phone numbers, left contacts in the order, names not found in any source).
