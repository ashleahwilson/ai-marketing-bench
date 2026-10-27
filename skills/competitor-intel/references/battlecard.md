# The two files

## Contents
- competitors/<name>-battlecard.md
- Writing each section
- brand/competitors.md
- Changelog line

## competitors/<name>-battlecard.md

`<name>` is the competitor's name in lowercase with hyphens (`platewise-books-battlecard.md` or the short name the user uses). The headings below are fixed: keep every one, in this order, even when a section only says `TBD`.

```
# Battlecard: <Competitor> (for <our company>)

Status: draft | provisional (no brand memory) · Built: YYYY-MM-DD
Oldest capture: YYYY-MM-DD · Refresh by: YYYY-MM-DD

## Recommendation
<1–2 lines: where to compete hard, how to position, when to walk away>

## Who they are
- <fact> [source: <where>, <date> · <status>]

## Pricing as shown
| Plan | Price as shown | Includes | Source |
|---|---|---|---|
| <plan> | <exact price and conditions> | <limits, features> | <page, date> |
| <plan> | not shown ("Talk to sales") | | <page, date> |

## Where they're strong
- <real strength> · why it matters to the buyer [source: …]

## Where we win
- <our advantage> · proof: <the brand-memory line, or TBD> [source: brand/<file>, <date>]

## When we lose to them and why
- <counts and pattern from win/loss> [source: <export>, <date>]
- Sample: <n> deals, <date range>

## Landmines
1. "<question a buyer could fairly ask>" · exposes: <the evidenced gap> [source: …]

## Objections
| They say | We say | Proof |
|---|---|---|
| "<objection>" | <response> | <brand-memory line or TBD> |

## Feature comparison
| Capability | <Us> | <Them> | Source |
|---|---|---|---|
| <capability> | Yes (brand/offer.md) | not shown | <page, date> |

## Don't say
- <claim> · <why: unsourced, false on the sources, restricted by a brand rule, their claim not ours>

## Sources
| Source | Captured | Used for |
|---|---|---|

## Open
- TBD: <what's missing> · <who has it>
```

## Writing each section

- **Recommendation:** lead with it. Base it on the win/loss pattern and the evidenced gaps, not on general impressions ("Compete hard for multi-location and Lightspeed restaurants; with single-location owners who want payroll bundled, lead with the named bookkeeper or walk").
- **Where they're strong:** real strengths, at least two when the sources support them. A lower list price, a bundled feature, an annual discount and a feature we don't offer all count. Credibility with reps and buyers comes from naming these.
- **Where we win:** each advantage needs proof from brand memory (`proof.md`, approved `claims.md`, `offer.md`). Proof marked `named: unconfirmed` is described without the customer's name. No proof on record: write the advantage with `proof: TBD` and list it in Open. Never invent a customer, result or percentage.
- **When we lose to them and why:** from win/loss data only. Totals, reason counts, the segment pattern, and the sample size. No data: `TBD: win/loss notes` (don't fill it from general knowledge).
- **Landmines:** two to five, each tied to a sourced gap. A question a smart buyer would ask anyway, not a trap. No sourced gap, no landmine.
- **Objections:** what the buyer is likely to raise, judged from their strengths, reviews and loss reasons. Responses are honest: when they're right (we don't run payroll, we don't connect Amazon), say so and reframe on who we're for. Proof from brand memory or TBD.
- **Feature comparison:** our column from brand memory; theirs from their pages, with `not shown` where a page is silent and "their claim" for performance claims. Include rows where they win.
- **Don't say:** every request, rumour or tempting claim you left out, with the reason, so reps know.
- **Sources:** every file or page used, with its capture date.

Keep the battlecard to what a rep can use on a call: about 600–900 words.

## brand/competitors.md

The brand-memory format. One `## <Competitor>` section each. Facts only, one bullet each, every bullet tagged. Opinions go under `### Our read`, labelled with who said it and when. Old prices go under `### Price history`.

```
# Competitors

Last reviewed: YYYY-MM-DD

## Platewise Books

- Restaurant bookkeeping service, North America [source: platewise.example/ (saved page), 2026-10-15 · confirmed]
- Essentials: $279/month, one location, P&L by the 15th [source: platewise.example/pricing (saved page), 2026-10-15 · confirmed]
- Claims "Trusted by 2,000+ restaurants" [source: platewise.example/pricing (saved page), 2026-10-15 · provisional] | their claim
- Offers a free first month [source: platewise.example/pricing, 2026-05-02 · confirmed] | stale: not on the 2026-10-15 page
- Win/loss 2026-05 to 2026-10: 5 won, 5 lost [source: CRM export winloss.csv, 2026-10-20 · confirmed]

### Price history
- Starter: $259/month [source: platewise.example/pricing, 2026-05-02 · confirmed] | superseded 2026-10-15

### Our read
- Wins on price with single-location owners (Dev Patel, 2026-05-02)
```

Rules:
- Merge into the existing file. Keep other competitors' sections exactly as they are. Update `Last reviewed`.
- Add `### Price history` only when there's an old price to put in it. Every bullet under a competitor carries a source tag; a gap is one `- TBD: <what's missing>` line, not an empty heading.
- Never delete a fact: correct it (old value to history or `superseded`), re-date it if re-seen, or mark it `stale`.
- No rumours, no battlecard tactics (landmines, talk tracks): those live in the battlecard.

## Changelog line

If `brand/changelog.md` exists, add one line at the top of its list:

```
YYYY-MM-DD | competitors | <what changed> | <why>
```
