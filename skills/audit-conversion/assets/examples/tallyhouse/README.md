# Worked example: Tallyhouse, four pages, score 38/100

Tallyhouse is a fictional restaurant bookkeeping firm. The files:
- `site/`: the saved HTML of its home, pricing, about and contact pages (the input)
- `brand/`: the parts of its brand memory the audit reads (offer, proof, rules, voice)
- `audits/tallyhouse.example/conversion.md`: the report
- `audits/tallyhouse.example/dim-conversion.json`: the checklist result the full marketing audit reads

## Why 38, and why it matches the full audit

The six checks are the full audit's conversion dimension, so the deep dive lands on the same 38 the full audit gave these pages: C1 10 (one action, three wordings), C2 20, C3 0 (revenue and phone required), C4 8 (bare "$" for a Canada and US business, catch-up "quoted"), C5 0, C6 0. What the deep dive adds is below the score: placeholder-only labels, no autofill, no error messages, "Submit", an about page with no way forward, and a plan that respects what brand memory says.

## What brand memory changed

- **The quote beside the form.** The obvious fix for C5 is to move Maria Okafor's quote next to the form. Brand memory records her naming permission as unconfirmed, so the plan asks for her OK first and doesn't treat the quote as ready to use.
- **Spelling.** The voice file says Canadian spelling, so the report uses it.

## What it didn't do

- **No conversion rates.** There's no analytics export, so the funnel section says what to send instead of estimating.
- **No predicted lift.** The test backlog names the metric each change should move, not how far.
- **No invented friction.** The analytics tag loads `async`, so speed gets a line under "What's working", not a finding.
