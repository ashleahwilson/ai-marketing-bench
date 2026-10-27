# Dimension rubrics

Five dimensions, each scored 0–100 as the **sum of fixed checks**. Each check awards full, partial or zero points against a stated test. Fixed checks keep two audits of the same site within a few points of each other. Each section below is the complete brief for one dimension's analysis. In a full audit, give each section, plus the briefing, to a separate parallel analysis.

## Contents
- How to score
- Positioning (25%)
- Acquisition (20%)
- Conversion (20%)
- Brand (15%)
- Measurement (20%)
- Output format

## How to score

1. **Score every check in the table:** full, partial or 0 points, using its test. Write one line of evidence per check (a quote, a page, or an `inspect_page.py` fact). The dimension score is the sum, and `score.py` recomputes it from the checks.
2. **Calibrate for maturity.** For a **founder-led** company only, a check marked † that would score 0 gets its partial credit instead (for example, no content programme at 4 people). First-hire and later companies get no relief. Never relax the unmarked checks.
3. **Score each issue once.** Every issue belongs to exactly one check: message contradictions to B2, CTA wording to C1, missing privacy notices to C5 and M5 only as their tests say, unconfigured analytics to M1. Don't take points off a second check for the same issue.
4. **Checks that apply to every page** (A1, A2, A6, C1, C6, M1, M5): met on all pages reviewed is full; met on some is partial; met on none is 0.
5. **When torn between two levels, award the lower one** and say why in the evidence. A consistent tie-break keeps repeat audits within a few points.
6. **What isn't observable** (traffic, conversion rates, spend) is listed, not scored. Never estimate it.
7. **Findings come from the checks that lost points:** 3–5 per dimension, worst first. Each has a severity (`high` for 0 points on a check worth 20 or more, `medium` for 0 on a smaller check or partial on a large one, `low` for the rest), its evidence, and a fix concrete enough to start this week.
8. **Strengths come from the checks that scored full points.**

## Positioning (25%)

| ID | Check | Full | Partial | 0 |
|---|---|---|---|---|
| P1 | The headline says what it is in plain words | 20: what it does is clear from the headline alone | 10: clear only after the subhead | Buzzwords; it fails the swap test (a competitor's name fits) |
| P2 | Audience is named | 20: a specific audience plus exclusions | 10: a specific audience | "Teams", "businesses", or none |
| P3 | Differentiation from the alternative | 20: one specific true difference, set against what buyers use now | 10: specific but not contrasted | Generic benefits only |
| P4 | Consistency across pages | 20: every page reviewed names the same product, audience and core benefit | 10: one page names a different audience or benefit | Pages describe different products, or the about page is clearer than the home page (contradictions within a page belong to B2; CTA wording to C1) |
| P5 | Claims are supported | 20: bold claims backed by proof, or qualified | 10: some unsupported | The headline claim, or a superlative, is unsupported or contradicted |

## Acquisition (20%)

| ID | Check | Full | Partial | 0 |
|---|---|---|---|---|
| A1 | Titles and meta descriptions | 20: unique title and meta description on every page | 10: titles everywhere, some meta descriptions missing | Titles missing or duplicated |
| A2 | On-page structure | 15: one H1 per page, logical H2s, a canonical tag, structured data | 8: two or three of these | One or none |
| A3 | Answer-engine readiness | 15: a plain, quotable "what we do, for whom" sentence, plus FAQ-style content | 8: one of the two | Neither |
| A4 † | Content engine | 20: new content in the last 90 days, on topic for the audience | 10: within 12 months | Older, or none |
| A5 † | Channel evidence | 15: two or more kinds visible (ad tags, social profiles, press, third-party reviews, partner or integration listings) | 8: one kind | None visible |
| A6 | Navigation and linking | 15: navigation on every page; key pages linked | 8: navigation missing on some pages | No usable navigation |

## Conversion (20%)

| ID | Check | Full | Partial | 0 |
|---|---|---|---|---|
| C1 | Primary CTA | 20: one action, consistent wording, present on every key page | 10: present but the wording varies, or it's missing on some pages | Competing or absent |
| C2 | Path to a lead | 20: a form, booking, trial or signup | 10: a form that's hard to find | `mailto:` or phone only |
| C3 | Form friction | 20: 5 fields or fewer, nothing sensitive required | 10: 6–8 fields, or no form at all (C2 already counts that gap) | More than 8, or revenue, budget or phone required up front |
| C4 | Pricing clarity | 15: public prices for the main offer, with an unambiguous currency (a bare "$" counts only if the company sells in one dollar country) | 8: prices shown but the currency is ambiguous, or some items are "quoted" with no range | Nothing, and no reason given |
| C5 | Trust at the decision point | 15: proof (a testimonial, logo or result) on the pricing or contact page itself, plus a privacy link or notice on the page with the form | 8: one of the two | Neither |
| C6 | Mobile ready | 10: viewport meta tag on all pages | 5: on some pages | None |

## Brand (15%)

| ID | Check | Full | Partial | 0 |
|---|---|---|---|---|
| B1 | Voice consistency | 25: one recognisable voice across pages | 12: mostly consistent | Clashing registers |
| B2 | No message drift | 25: nothing contradicts the core story | 12: minor drift | A visible contradiction, such as an "AI-powered" banner on a brand that sells "a real person, not a chatbot" |
| B3 | Proof credibility | 20: attributed, specific proof | 10: some vague proof ("trusted by companies worldwide") | Only vague or unverifiable proof |
| B4 | Asset care | 20: alt text, consistent page titles, no placeholder assets | 10: a few gaps | Many gaps |
| B5 | Matches brand memory | 10: no breaches of the audited company's `brand/` rules or claims | 5: a minor breach | A rule or claim breach |

**B5 without the company's brand memory** (none exists, or the `brand/` folder belongs to the auditor): award 10 if B1 and B2 both scored full, otherwise 5. Never judge a site against someone else's brand memory.

## Measurement (20%)

| ID | Check | Full | Partial | 0 |
|---|---|---|---|---|
| M1 | Analytics configured on every page | 30: present and configured on every page (for GA4, the library and a `config` call, or a Tag Manager container) | 15: on some pages, or loaded without configuration | None |
| M2 | Conversions tracked | 30: conversion events in the source for the primary action | 15: tracking via Tag Manager that can't be seen in the source (say so) | None |
| M3 † | Ad platform tags | 15: tags present where there's paid activity, or no paid activity observed | 8: some missing | Paid activity with no tags |
| M4 | Hygiene | 15: no retired (Universal Analytics) or duplicated tags | 8: one of these | Both, or several duplicates (an unconfigured tag belongs to M1) |
| M5 | Consent basics | 10: a privacy policy link sitewide, and a consent mechanism where required | 5: a policy link only | Neither |

**If only rendered text or markdown is available, with no HTML source,** set measurement as not assessable.

## Output format

Save each dimension's result to `audits/<domain>/dim-<name>.json`:

```json
{"dimension": "conversion", "assessable": true, "confidence": "high|medium|low",
 "checks": [{"id": "C3", "points": 0, "max": 20, "evidence": "contact.html: 10 fields, 7 required incl. revenue"}],
 "score": 55,
 "findings": [{"severity": "high", "check": "C3", "finding": "…", "evidence": "…", "fix": "…"}],
 "strengths": ["…"], "not_observable": ["…"]}
```

`score.py` recomputes `score` as the sum of the check points. If the dimension can't be assessed, set `"assessable": false`, `"score": null`, leave `checks` empty, and give the reason.
