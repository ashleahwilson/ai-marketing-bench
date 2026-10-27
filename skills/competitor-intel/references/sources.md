# Sources: what counts, and how to tag it

## Contents
- What can be used
- The source tag on a competitor fact
- Reading each kind of material
- Shown, not shown, and "No"
- Rumours and hearsay
- Comparison claims about us
- Staleness

## What can be used

Only material in front of you: pages the user saved or pasted (HTML, text, PDF), pricing pages, review excerpts, win/loss exports, call notes, the user's own statements, and brand memory. If browsing tools are connected and the user asks you to fetch a page, a page you fetched counts too, with today's date as the capture date. Nothing from memory: what a competitor charged or offered "as far as you know" is not a source, however familiar the name.

## The source tag on a competitor fact

```
- Essentials: $279/month, one location [source: platewise.example/pricing (saved page), 2026-10-15 · confirmed]
```

- **Where:** the page or file (URL path or file name), plus what kind it is if that isn't obvious (saved page, review site, win/loss export, call notes).
- **When:** the capture date: when the page was saved, the review was copied, or the export was run. Not today's date, unless you captured it today. Use the date in the file (its header, a "saved on" or "exported" line, or the date in the file name). If the material carries no date, write `captured: TBD` and ask for it; an undated source isn't stale, it's undated.
- **Status**, as in brand memory, applied to competitors:

| Status | For |
|---|---|
| `confirmed` | What a competitor's own current page says about **its own prices, plans, features, integrations and terms**; facts in the user's CRM or win/loss export; what the user tells you directly |
| `provisional` | The competitor's claims about **its own performance or popularity** ("2,000+ restaurants", "cut no-shows by 40%", "2x faster", a testimonial on its site): record them as *their claim*. Review excerpts. Prospect-reported facts from call notes (a quoted price shown in an email) |
| `assumed` | Never used for a competitor fact. If you'd have to assume it, it's `TBD` |

## Reading each kind of material

- **Pricing pages:** copy each price exactly, with its conditions, and repeat the conditions every time the price appears ("from $99/month, billed annually", never "$99/month" in a later section or the reply): "from", per what (location, provider, seat), billing period ("billed annually"), plan limits. Where the page says "Talk to sales" or shows nothing, the price is **not shown**. Discounts on the page (annual billing) are facts too.
- **Their home or feature pages:** features and integrations listed are confirmed as offered. Performance numbers and testimonials are their claims.
- **Reviews:** cite each one with its date and rating. Say how many there are and how old ("two reviews, both from 2024"). One review is one customer's experience, not a pattern: write "one reviewer, 2026-08, said…", never "customers say". Reviews older than 18 months are context only; don't build a landmine on them alone.
- **Win/loss exports:** count. Give won and lost totals against this competitor, the reason counts, and any pattern in deal size, segment or region you can see in the rows (for example "all five losses were single-location"). Say when the sample is small (under about ten deals) and qualify the conclusion. Never extend a pattern beyond the rows.
- **Call notes:** what the prospect showed or said is prospect-reported (`provisional`, with the call date). What a colleague "heard" is hearsay: see below.

## Shown, not shown, and "No"

If a page doesn't mention a feature, write **not shown**, never "No". A missing line on a marketing page isn't proof of a missing feature. A gap is only a gap when a source says so: a review ("we export sales by hand every week, wish they connected to it"), a lost or won deal reason ("couldn't connect to Lightspeed"), or the page itself limiting it ("Toast and Square integrations", "payroll on the Plus plan"). Then state it with its evidence ("two won deals and one review say they don't connect to Lightspeed") and build a landmine on it. What stays out is the flat, unattributed version said to a buyer ("they can't do X"): frame it as a question the buyer can check.

## Rumours and hearsay

Claims that a competitor is in financial trouble, has security or legal problems, is being sold, or is losing staff stay out of every file and every talk track unless the user supplies a public, citable source (a filing, a breach disclosure, a court record, a news report). "Someone at a trade show said" and "a rep heard" are not sources, and labelling them "unconfirmed" or "reported" doesn't make them usable: a rep repeating it to a buyer is disparagement either way, and it's easy to disprove.

When asked to include one: build everything else, leave it out, say why in a sentence, say what source would change that, and give the rep something true to lead with. Where it fits, offer a neutral question that lets the buyer check the topic themselves ("How did you vet their data security?") without asserting a problem. Put the rumour itself under **Don't say**.

## Comparison claims about us

"We're 2x faster", "cheaper", "better support", "the only one that…" go in a battlecard only when brand memory substantiates them (`claims.md` approved claims, `proof.md` results) **and** the competitor side is sourced. Check the arithmetic against the sources: if our listed price is higher than theirs, "cheaper" is false, whatever the request says. A claim `rules.md` restricts or `claims.md` lists as needing substantiation stays out. Tell the user what was left out and offer the strongest claim that is defensible.

## Staleness

A capture older than 90 days is stale. In a refresh:
- A fact the new material re-confirms gets the new date.
- A fact the new material contradicts is corrected; the old value moves to a `### Price history` line (prices) or is marked `superseded <date>`, never silently deleted.
- A fact the new material doesn't cover keeps its old date and gets marked `stale`. Never re-date a fact you didn't see again.

Every battlecard carries a **Refresh by** date: the oldest capture it relies on plus 90 days.
