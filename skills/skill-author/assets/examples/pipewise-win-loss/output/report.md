**Skill:** skills/win-loss-summary/ · Ready to test

**Rules derived** (8)
1. Lead with the reason the buyer gave most often, and how many times · from "Lead with the reason the buyer gave most often, and say how many times they gave it."
2. Quotes are word for word from the transcript · from "That's a paraphrase in quote marks."
3. Deal size at the top, from the CRM export or the user, or "not given" · from "put the deal size at the top, we always want it"
4. Report, don't recommend; optional "Questions this raises", as questions · from "Don't recommend. The summary reports what the buyer said."
5. Under 300 words, one page · from "One page. Under 300 words."
6. Say "buyer", not "customer" · from "a loss was never a customer"
7. Don't predict; write what the buyer said · from "Did he say that? … Don't predict."
8. Never name individual people at other companies · from "just the company"

**Not made into rules:** the $48,000 deal size (a CRM fact, read at run time). No one-offs or conflicts found.
**Tests:** 9 evals, 3 traps · every rule tested at least once; traps cover a missing deal size, a buyer who gave no clear reason, and a request to add recommendations.
**Removed from the source:** nothing confidential found (the notes already used fictional stand-ins).
**Transfer test** (desk check): a win where the buyer gave two reasons equally often · held on quotes, length and wording; guessed at the lead. Rule 1 now says: if two reasons tie, lead with both and say so.
**Not tested yet:** blind tests haven't run. To run them, plan fresh runs with and without the skill, then have someone who didn't write it grade them (commands below).

    python3 bench/plan.py skills/win-loss-summary ../ai-marketing-bench-runs/win-loss-summary --iteration 1 --configs with-skill:haiku,no-skill:haiku,with-skill:opus,no-skill:opus
    python3 bench/run_headless.py ../ai-marketing-bench-runs/win-loss-summary/iteration-1 --parallel 3

**Need from you:**
1. Is the deal size always in the CRM export, or sometimes only in the rep's notes?
2. Should summaries of wins and losses share one format (they do now)?
