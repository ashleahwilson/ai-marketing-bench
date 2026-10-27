# Turning corrections into rules

## Contents
- Where corrections hide
- The five classes
- Writing the rule
- Conflicts and supersession
- Generalizing without inventing
- The ledger

## Where corrections hide

- **Direct pushback:** "no, not like that", "don't…", "stop…", "too long", "that's wrong".
- **The draft-to-final gap.** When both a draft and the approved version exist, every change between them is a correction, even if nobody said it out loud. Name the change, and quote both versions.
- **Repeated fixes.** A correction made twice is a strong rule. Note the count.
- **Praise with a reason.** "Yes, this, because it opens with the owner's problem" confirms a rule. Praise with no reason confirms nothing.
- **Approved examples** show what good looks like, but a single example can't tell you which of its features matter. Treat features seen once as observations, not rules.

## The five classes

| Class | What it is | Where it goes |
|---|---|---|
| **Method** | How the work is done, true for any customer or brand ("open with the problem in the customer's words") | A rule in SKILL.md, tested by at least one eval |
| **Brand fact** | Something true about this business: a price, a product name, a claim, who may be named, a banned word ("single location is $349") | Not in the skill. The ledger says which brand memory file it belongs in. The skill gets the method half instead ("take prices from `brand/offer.md`, never from memory") |
| **One-off** | A preference for this piece only ("make this one warmer, it's her birthday week") | Not a rule. Listed so the user sees it was considered |
| **Superseded** | An earlier correction a later one replaced ("under 400 words", later "cap it at 350") | Only the later one becomes a rule. The ledger records both, with dates |
| **Conflict** | Two corrections that can't both hold, with no clear order or owner ("questions in subject lines" vs "never questions in subject lines" from two people) | Not a rule yet. Ask who decides. In Draft mode, leave it out of the skill and list it under "Need from you" |

A correction can split in two. "Single location is $349, not $299, get it from the pricing page" is a brand fact ($349) plus a method rule (prices come from the source of truth, never memory). Record both halves.

**Job wording is method, not brand fact.** An exact reply line, a date format, approved subject lines or a send condition ("day 3 only goes to people who haven't connected") belong to this job: keep them in the skill word for word, with the approved examples. Only move a fact out of the skill when `brand/` already holds it. If it doesn't, keep it in the skill and list it as "suggest adding to brand memory".

Brand rules the user states during the session ("never say AI-powered") are brand facts: they belong in `brand/rules.md` or `brand/voice.md`, and the skill tells the agent to apply whatever brand memory's rules say. Hard-coding them would make the skill wrong for every other brand.

## Writing the rule

- **Imperative and specific:** "Open with the customer's problem, in their words from the interview." Not "Make openings engaging."
- **Give the reason in a few words,** taken from the correction where possible. A model follows a rule it understands far better than a rule in capitals.
- **Keep the trigger example.** In the ledger, quote the correction and, where short, the line it corrected. In SKILL.md, a short before-and-after helps when the rule is easy to misread.
- **Measurable where possible.** "Under 350 words" beats "concise". Anything countable goes to the skill's script as well.
- **Keep the user's own words** for their terms. If they say "customers", don't write "clients".

## Conflicts and supersession

- **Dated and from the same person:** the later one wins. Record the earlier one as superseded.
- **Undated, or from different people with no stated owner:** ask. Don't pick the one you prefer.
- **A correction that contradicts brand memory:** the brand memory may be out of date. Flag it; don't silently follow either.

## Generalizing without inventing

A rule should cover the pattern, not just the one case ("only use numbers the customer said" covers every case study, not just Lantern's). But generalizing is not adding: a rule the user never implied ("post on Tuesdays", "use three hashtags") is an invention even if it's common advice. If a rule seems necessary and nothing in the material supports it, put it under "Need from you" as a question.

## The ledger

`skills/<name>/evals/rules-ledger.md` is the hand-off file. It lives in `evals/` because it explains the tests and isn't loaded when the skill runs. Columns: number, rule as written in the skill, the correction quoted, source and date, class, eval ids. Then three short lists: brand facts (with the brand memory file each belongs in), one-offs, open conflicts. Anyone revising the skill later reads this first, so a rule is never deleted without knowing why it was added.
