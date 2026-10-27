# Changelog

## 1.2.1 (2026-10-27)
- Its own name and scripts stay out of replies and reports. Integration change, not re-run.

## 1.2.0 (2026-10-27)
Round 2 (Haiku 59/65): the decline gave three sentences of reasons; check mode paraphrased a FAIL ("if it stays long") instead of naming it; no offer to set up missing brand memory; Guided mode ended on side questions and turned a brand fact into a rule; test steps were vague; a reply reported the structure check's counts.
- Declines give one sentence of reason.
- Check mode gives every FAIL its own line, in its own terms.
- Missing brand memory is named, with an offer to set it up, in every mode.
- Guided mode ends with a direct approval question and keeps brand facts out of the rules.
- Test steps name the evals file and the commands; self-check names and counts stay out of replies.

## 1.1.0 (2026-10-27)
Round 1 (Haiku 46/65, Opus 58/65): approved job wording (an SMS reply line, subject lines, a send condition) was moved to brand memory that didn't exist, leaving placeholders; check mode on Haiku audited the wrong folder; self-checks were reported as "passes" and "held"; a licence and author were invented; replies ran long.
- Job wording the user approved stays in the skill word for word; nothing moves to brand memory unless brand memory already holds it.
- Check mode audits the folder in the user's project only, and lists every problem found.
- The new-case read-through and structure check are described as self-checks, never as passing.
- Author and licence come from the user, or are left as TBD / internal use and asked about; fixture details never reach the reply.
- Replies under 300 words (150 when declining), with plain-language terms and a line when there's no brand memory.

## 1.0.0 (2026-10-24)
- First release:
  - Turns a session transcript, notes, approved examples and the user's corrections into a skill folder that meets the Bench Standard.
  - Corrections first: each is classified (method, brand fact, one-off, superseded, conflict) and written to a rules ledger (`evals/rules-ledger.md`) with the quote that triggered it.
  - Evals before the skill: at least 8, at least 2 traps, built from the real cases.
  - Three modes: Draft (default), Guided (stops after the ledger and test plan for approval), Check (reviews an existing skill folder before it's shared).
  - `check_skill.py`: name format and folder match, description length, person and "use when", frontmatter keys, version, line counts, links, reference depth and contents, stdlib-only scripts, eval count, traps, expectations and fixture files, worked example, changelog; prints blind-eval commands without running them.
  - `leak_scan.py`: secrets (masked), emails, phone numbers, named real clients, money figures, percentages, web addresses, titled names and company names.
  - Thin material gives a provisional `0.1.0` draft and a request for specific cases; deceptive purposes are declined with an honest alternative offered.
