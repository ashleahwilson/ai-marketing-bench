# Discovery: build the shared briefing

Discovery runs once, before any dimension is scored. Every dimension reads this one briefing, so no analysis fetches the same page twice.

## Contents
- Pages to collect
- What to extract
- Classify the business
- Classify the marketing maturity
- The briefing file

## Pages to collect

Collect up to 8 pages. Get raw HTML where you can, because tracking tags only show up in the source.

| Page | Where to look | Why |
|---|---|---|
| Home | `/` | Positioning, primary CTA, proof |
| Pricing | `/pricing`, `/plans`, a pricing link in the nav | Offer clarity, friction |
| Product or services | `/product`, `/services`, `/how-it-works`, `/features` | Whether the offer is concrete |
| About | `/about`, `/company`, `/team` | Who they are, team size, stated audience |
| Proof | `/customers`, `/case-studies`, `/reviews` | Evidence quality |
| Content | `/blog`, `/resources`, `/insights` | Acquisition engine, freshness |
| Conversion | `/contact`, `/demo`, `/signup`, `/book` | Form friction, the path to a lead |
| Careers | `/careers`, `/jobs` | Team size and shape, marketing hires |

Also useful when you can reach them: public ad libraries (Meta Ad Library, Google Ads Transparency Center, LinkedIn page ads), the company's LinkedIn page, and review sites. For the user's own company, use connected analytics or Search Console data, with read-only access.

**If you can't fetch pages** (no browsing, the site blocks it), ask the user to paste or save the pages. Never reconstruct a site from memory or general knowledge.

## What to extract

Run `python3 scripts/inspect_page.py <saved pages>` on every HTML page you have, and add what it finds to the briefing. Then read each page for what a script can't judge: what the company says it does, who it says it's for, the proof it shows, and the voice.

Facts the briefing must hold, each with the page it came from:
- **Stated offer:** a quote of the headline, plus one sentence on what they actually sell.
- **Stated audience and exclusions**, quoted.
- **Primary CTA** on each page, and where it leads.
- **Prices**, if public.
- **Proof items:** each quote, logo, number or award, with who it's attributed to.
- **Content:** what exists, and the date of the newest item.
- **Tracking:** tags found on which pages, and whether conversion events are in the source.
- **Forms:** fields, and how many are required.
- **Team signals:** size, roles, marketing roles, open marketing jobs.

## Classify the business

Pick the one type that best fits. If two fit, name the primary type and note the secondary.

| Type | Signals | What matters most |
|---|---|---|
| B2B SaaS / software | Pricing tiers, "demo", integrations, trial | Positioning against alternatives, demo/trial path, product-led proof |
| B2B services / agency / professional | "Book a call", case studies, team bios | Specialisation, proof of outcomes, a low-risk first step |
| E-commerce / D2C | Cart, product pages, shipping and returns | Product pages, checkout friction, reviews, retention |
| Local or multi-location business | Locations, hours, maps, "near me" | Local search, reviews, booking or call path |
| Marketplace / platform (two-sided) | Separate messaging for buyers and sellers | Clarity for each side, liquidity proof |
| B2C app / subscription | App store links, free tier, onboarding | Activation, store presence, retention messaging |

## Classify the marketing maturity

This calibrates every score. Judge it from evidence, and say what the evidence was.

| Maturity | Typical signals | What "good" looks like at this stage |
|---|---|---|
| **Founder-led** | Under ~10 people, the founder is the voice, no marketing roles, sporadic content | A sharp message, one channel working, a clean path to a conversation |
| **First hire** | ~10–50 people, one marketer or hiring the first | The basics are instrumented, consistent positioning, one repeatable acquisition motion |
| **Small team** | 2–5 marketers, regular content, some paid | Multiple channels measured, a defined funnel, proof at each stage |
| **Full function** | Marketing leadership, specialists, many channels | Attribution, experimentation, brand system, operating cadence |

Never score a founder-led company against full-function expectations. A founder-led company with a sharp message and one working channel can score in the 70s.

## The briefing file

Write `audits/<domain>/briefing.md`:
- The two classifications, each with its evidence.
- The pages collected, and the ones missing.
- The extraction above.
- What wasn't observable.

Every dimension analysis reads this file, and no other web fetching is needed.
