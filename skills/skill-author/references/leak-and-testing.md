# Leak scan and testing

## Contents
- What counts as a leak
- Replacing it
- Reporting it
- The transfer test
- Blind tests and honest wording

## What counts as a leak

Anything from the source material that shouldn't travel with a skill that may be shared with a team, an agency or the public:

| Category | Examples | Action |
|---|---|---|
| Secrets | API keys, tokens, passwords, private keys, login links | Remove. Never copy, never repeat, even masked. Tell the user to revoke and replace it |
| Client and customer names | The real company or person the work was for | Replace with a fictional stand-in |
| Personal data | Emails, phone numbers, addresses, health details | Remove or replace with reserved addresses (`name@company.example`) |
| Business figures | Revenue, growth rates, margins, deal sizes, salaries | Remove, or replace with clearly fictional figures in fixtures only |
| Internal prices and terms | Day rates, discounts, contract terms not on the public site | Remove |
| Anything marked confidential | "Internal only", "don't share", NDA material | Remove |

The scan script finds the mechanical ones (keys, emails, phone numbers, figures, web addresses, names you pass with `--name`). It can't know which names are real: you decide that from the source, and pass each real name to the scan so it proves they're gone.

The user's own brand (their company name, their public prices) isn't a leak, but it still doesn't belong in the skill text: it lives in brand memory (see [corrections.md](corrections.md)).

## Replacing it

- Use fictional stand-ins that are obviously made up, with reserved domains (`.example`).
- Keep the shape that made the case useful: a three-location restaurant stays a three-location restaurant, a vague result stays vague.
- Don't swap a real figure for an invented one in anything the skill will treat as a fact. In fixtures, fictional figures are fine and labelled fictional.

## Reporting it

In the reply, list what was removed by category and count: "an API key (rotate it: it was in plain text in the notes), the client's name in 6 places, 3 revenue figures, 2 email addresses". Never the values. Say that the stand-ins are fictional. If the scan found nothing, say "nothing confidential found".

## The transfer test

A skill built from a few cases can quietly encode those cases instead of the method. Before reporting:
1. Write one realistic case that isn't in the source or the evals: a different customer, a different kind of input, one rule under pressure.
2. Follow the new SKILL.md on it, literally, as a newcomer would.
3. Note where it held and where you had to guess or fall back on the original case. Each guess is either a missing rule (ask for it) or a rule that's too narrow (rewrite it more generally, without adding anything the material doesn't support).

Report it as a **desk check**, done by the author, not as a test result.

## Blind tests and honest wording

Real results need fresh runs with and without the skill, graded by someone who didn't write it. Print the commands (`check_skill.py --eval-commands` prints them) and stop there.

| Don't say | Say instead |
|---|---|
| "Passes all tests" / "beat the public version" | "Built from 7 real corrections, with 9 tests written. Blind tests haven't run yet" |
| "Tested and ready" | "Ready to test" |
| A pass rate or score you didn't measure | Nothing, until the graded runs exist |

If the user asks you to state results ahead of the tests (for a pitch, say), decline that line in a sentence and give them the honest one they can use today.
