# Worked example: a win-loss summary skill for Pipewise

Pipewise (fictional B2B sales forecasting software) wants its product marketing team's win-loss interview summaries written the same way every time. Rosa corrected an assistant across three sessions; this turns those corrections into a skill.

- **Input:** [input/session-notes.md](input/session-notes.md), three sessions with nine corrections. Buyer companies and people are fictional stand-ins.
- **Output:**
  - [output/report.md](output/report.md): the reply the user receives.
  - [output/win-loss-summary/](output/win-loss-summary/): the skill folder. Its skill file is saved here as `SKILL.example.md` so agents don't load it as a live skill; in a real run it's `SKILL.md`. Its evals and fixtures are shortened to the first three in full plus one-line summaries of the rest, to keep this example readable.
  - [output/win-loss-summary/evals/rules-ledger.md](output/win-loss-summary/evals/rules-ledger.md): why each rule exists.

What to notice:
- The deal size ($48,000) is a fact from the CRM: it stays out of the skill. The skill gets the method half: "put the deal size at the top, taken from the CRM export or the user; if it's missing, write 'Deal size: not given'".
- "Use 'buyer', not 'customer'" is kept in the user's own words.
- No test results are claimed. The transfer test is labelled a desk check.
