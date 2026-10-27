# Changelog

## 1.2.2 (2026-10-27)
- Skill and script names stay out of replies and deliverables (a test machine's global instruction to announce skills leaked into client-facing replies in several runs). Text-only change, not re-run.

## 1.2.1 (2026-10-23)
Found by the round 3 grader; not re-run.
- `build_list.py` gives the real basis for each customer exclusion (CRM stage, customer list, or named as a client in brand memory) instead of one generic line that Haiku repeated as fact.
- Declining personal emails names the law for the countries actually in the list (round 3 cited CASL for a list with no Canadian merchants).


## 1.2.0 (2026-10-23)
Round 2 (Haiku 66/70): every reply ran long (259 to 489 words), the no-data reply implied but didn't say who to target instead of CFOs, and the personal-email decline didn't name consent law.
- Word limits per reply type (300, 250, 180 in a hurry), checked with the new `words` command before replying.
- The no-data reply quotes the ICP range and names who to target instead; sources are named generically, never a vendor or connected tool.
- Declining personal emails names consent and privacy law as the reason.
- The list CSV withholds personal addresses from `contact_email` (kept in flags), so a sending tool can't pick them up.
- Shorter score reasons (`+30 Locations (6)`).

## 1.1.0 (2026-10-23)
Round 1 (Haiku 66/70, Opus 70/70): Haiku showed a ranked score table as a guided-mode "preview", called a webinar sign-up implied consent, named no law for Germany, didn't state how many accounts were new when adding to a list, and miscounted in two summaries.
- Guided mode shows no scores, tiers or ranking before sign-off.
- A sign-up or attendee list is never stated as consent; the reply says what to check. Every country gets its law named.
- Adding to an earlier list: the reply states the number of new accounts and names them.
- Self-check: counts copied from the build report; tiers in the reply match the CSV.
- Suppressed people are named in the reply only under "Contacts removed"; `named: unconfirmed` is about naming permission, not client status.
- Plainer flag wording; relative file paths in replies.

## 1.0.0 (2026-10-23)
- First release:
  - Builds a scored account list from the user's own exports (CRM, database, directory, event, webinar) and URL lists; with no data, explains what to bring instead of inventing names.
  - Merges duplicates across company-name and domain variants, never merging two accounts with different domains (listed as possible duplicates instead).
  - Removes suppressed and do-not-contact people, excludes suppressed companies, existing customers (customer file, CRM stage, or brand memory) and rubric disqualifiers.
  - Scores against `icp/scoring.md` (tolerant `criterion | points` reader, documented in `references/rubric-format.md`) or the user's stated criteria, with a reason per point, `max_possible` for blanks, and a "could reach tier" flag. Missing data is flagged, never filled.
  - Flags personal and role addresses; never looks up personal emails or guesses addresses.
  - Lawful-basis notes per country and per list source (CASL, CAN-SPAM, UK GDPR and PECR, EU GDPR).
  - Guided mode (approve the criteria first) and Draft mode.
  - `build_list.py`: build (merge, suppress, score, counts) and verify (every value traces to a source, nothing suppressed).
  - Writes `lists/<name>.csv`, `-excluded.csv`, `-summary.md`, and `-criteria.md` when the rubric was reworded; adds to an earlier list without overwriting it.
