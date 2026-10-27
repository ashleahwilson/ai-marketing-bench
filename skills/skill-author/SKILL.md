---
name: skill-author
description: Turns work that went well into a reusable Agent Skill that meets the Bench Standard, and checks an existing skill folder before it's shared. Reads a session transcript or notes, approved examples and, above all, the user's corrections ("no, not like that, like this"). Writes each correction as a rule with the example that triggered it, separates brand facts from method, writes at least 8 tests (2 or more traps) from the real cases before writing the skill, then builds the folder (SKILL.md, references, a standard-library script for anything mechanical, a worked example, changelog), runs a transfer test and a leak scan, and reports the rules, tests, what was removed and what to test next. Use when the user wants to make, capture or package a skill from their own work, for example "turn this into a skill", "make a skill from my notes", "save how we did this so the team can repeat it", or "check this skill before I share it". Not for running the blind tests, and not for skills built to deceive people.
license: MIT
metadata:
  version: "1.2.1"
  author: "Ashleah Wilson"
---

# Skill author

Good work happens once, in a session, after a few rounds of "no, like this". This turns that session into a skill that gets it right the first time, and proves it can be tested. The corrections are the most valuable input: each one is a rule someone had to learn the hard way.

## Ground rules

1. **Corrections first.** Every correction becomes a rule, written with the words that triggered it. Classify each one before writing anything: method (goes in the skill), brand fact (goes in brand memory, not the skill), one-off (not a rule), superseded (the later correction wins, and the ledger says so), or conflict (ask who decides). See [references/corrections.md](references/corrections.md).
2. **Missing stays missing.** Never invent a rule, a test case, a fact or a result the material doesn't support. A plausible rule is still an invention. With one example or no corrections, build a thin draft marked provisional (version `0.1.0`) and ask for the specific cases that would turn it into a real skill.
3. **Business facts live in brand memory; the job's own wording lives in the skill.** Prices, customer names, naming permission, product facts and claims are read from `brand/` (or the user) at run time, never written into the skill. But wording the user approved for this job (an exact reply line, a date format, approved subject lines, a send condition) is method: keep it in the skill word for word. Never move anything out of the skill unless `brand/` already holds it; if it doesn't, keep it in the skill and suggest adding it to `brand/`. A skill that writes `[placeholder]` where the user gave the exact words is broken.
4. **Tests before the skill.** Write the evals from the real cases and corrections first, so the skill is written to pass them and not the other way round.
5. **Nothing confidential leaves the source.** Before saving, remove secrets, client and customer names, personal details, revenue, internal prices and anything marked confidential. Replace what's needed with fictional stand-ins and say so. Never repeat a secret back, even partly; tell the user to revoke and replace it, since it sat in plain text.
6. **Never claim a result you didn't get.** A transfer test you ran yourself is a desk check, and is labelled that way. Blind test results exist only after someone else grades fresh runs. If asked to say it passed tests that haven't run, decline that line and offer an honest one.
7. **Keep the user's conventions, and invent nothing about them.** Spelling, tone and terms come from the source material and `brand/`, not from your own defaults or the environment's writing rules: a US company's skill keeps US spelling. Use the author name and licence the user gives; if they gave none, write `author: "TBD"` and `license: Internal use only` and ask. Fictional details you made up for test fixtures stay in the fixtures, labelled fictional, and never appear in the reply or the skill's rules.
8. **Check the purpose.** If the skill exists to deceive people (fake reviews or testimonials, posing as customers, hiding that something is an ad), decline that purpose with one sentence of reason, offer the honest version that meets the same goal, and build it only on a yes. No lecture, no list of consequences.
9. **Never edit the user's files.** Source notes stay as they are. In check mode, report; change an existing skill only when asked, and keep a copy of the original.
10. **No internals in what the user receives.** The skill you write never tells its user its own name, its scripts or other skills' names. Your reply doesn't name this method or its scripts either: say what was found.

## Modes

- **Draft** (default): build the full folder, then report.
- **Guided**: when the user wants to approve first ("walk me through it", "I want to see the rules first"), stop after step 3. Show the ledger and the planned tests, and end with one direct question asking the user to approve or change the rules. Write no skill files yet. Brand facts are listed for brand memory only: don't also turn them into a rule such as "mention X when relevant".
- **Check**: when the user points at an existing skill folder ("check this before I share it"), check that folder in the user's project folder (never this skill's own files or test fixtures): run the spec check and the leak scan from step 6 on it, judge every CHECK line, and reply in the check shape below with one line per problem found: every FAIL the spec check prints gets its own line, in its own terms (for example "over 100 lines with no contents section"). Change nothing unless asked.

## Workflow

```
- [ ] 1. Load: the source material, brand/, and the purpose check
- [ ] 2. Ledger: every correction, classified, with its quote and source
- [ ] 3. Tests: plan at least 8 evals (2+ traps) from the real cases   <- Guided mode stops here
- [ ] 4. Write evals/evals.json and its fixtures
- [ ] 5. Build the skill to the standard
- [ ] 6. Check: spec checker, leak scan, transfer test; fix every FAIL
- [ ] 7. Reply in the fixed shape
```

### 1. Load

Read everything the user points to: transcripts, notes, approved outputs, earlier drafts (the gap between a draft and the approved version is a correction too). Read `brand/` if it exists. Note which names, figures and details are real (clients, customers, people, revenue, keys): they're what the leak scan must catch. Then the purpose check (rule 8).

**Too little to work from?** One example and no corrections, or corrections with no example of the good result: build only the provisional draft (rule 2), and ask for the next cases by name ("two more posts you approved and one you rejected, with what was wrong").

### 2. Ledger

Write `skills/<name>/evals/rules-ledger.md` from [assets/template/rules-ledger.md](assets/template/rules-ledger.md): one row per correction with the quote, source and date, its class, the rule as it will read in the skill, and the eval ids that test it. Name the skill in lowercase with hyphens (`Event Recap Posts!` becomes `event-recap-posts`).

### 3 and 4. Tests

Follow [references/evals.md](references/evals.md). Every method rule gets at least one eval. Traps come from corrections where the right move is to hold, ask or leave a gap. Fixtures are small, fictional and stripped of the real details. Expectations are literal, written now, and gradeable from the output alone.

### 5. Build

Follow [references/skill-anatomy.md](references/skill-anatomy.md) and copy the templates in [assets/template/](assets/template/SKILL.template.md) (save the skill file as `SKILL.md`). The new skill must read `brand/` and work without it, keep a fact list, check its own output (a stdlib script for anything countable: length, characters, required fields, banned words), lead its output with the recommendation, and ship one worked example in `assets/examples/` that is different from every eval. Version `1.0.0` when the material was enough, `0.1.0` and marked provisional when it wasn't.

### 6. Check

```bash
python3 scripts/check_skill.py skills/<name> --eval-commands
python3 scripts/leak_scan.py skills/<name> --name "<each real name from the source>"
```

Fix every FAIL in the spec check and every LEAK in the scan, then run both again. Decide every CHECK line: keep it only if it's a fictional stand-in or a public fact the user approved. Then the transfer test: pick one realistic case the skill wasn't built from, follow the new skill on it, and note where it held and where it guessed. See [references/leak-and-testing.md](references/leak-and-testing.md).

### 7. Reply

```
**Skill:** skills/<name>/ · Ready to test | Provisional draft | Not built: <one-line reason>

**Rules derived** (<n>)
1. <rule> · from "<the correction, quoted>"

**Not made into rules:** brand facts (and where they belong), one-offs, superseded corrections
**Tests:** <n> evals, <n> traps · <one line on what they cover>
**Removed from the source:** <categories and counts, never the values> | nothing confidential found
**Tried on a new case** (my own read-through, not a test): <the new case> · <handled | had to guess at: …>
**Not tested yet:** no blind tests have run, so there are no results. To run them: <the steps or commands the spec check prints, naming skills/<name>/evals/evals.json>
**Need from you:** <at most 3 questions>
```

For **check mode**:

```
**Verdict:** Ready to share | Fix first | Hold: <one-line reason>   (Hold for any secret or confidential detail)
**Fix** 1. <file and line> · <problem> · <fix>
**Fine:** one line on what passed
```

Under 300 words (under 150 when declining). Plain language for someone who isn't a developer: say "tests where the right answer is to hold back" rather than "traps" the first time. If there's no `brand/` folder, say so in one line and offer to set one up ("I can set up brand memory for X if you'd like"), in every mode. Never print a secret, never claim a pass rate, and never describe your own checks as passing or holding: they're self-checks, not tests. Never mention the checker, the scan or a "structure check" by name, or report their counts: say what was found.

## Keep tools out of the deliverable

The skill you write names itself and may refer to other library skills: that's the job. In your replies and reports, never name this skill or its scripts and checks; describe what was checked instead. If your environment asks you to say which skill you used, put that in one short line to the user, separate from the deliverable.

## What good looks like

Someone who never saw the session can read the ledger and see why every rule exists. Every rule is tested at least once. Nothing in the folder could embarrass the user if it were shared with the client it came from. The report says exactly what has and hasn't been proven.

A worked example (a win-loss summary skill built from one sales team's corrections) is in [assets/examples/pipewise-win-loss/](assets/examples/pipewise-win-loss/README.md).
