# Conversion checks

## Contents
- The checklist (the score)
- How to score
- Page-by-page review (the findings)
- Forms
- Friction and reassurance
- Mobile and speed signals
- What not to flag
- Severity

## The checklist (the score)

These six checks are the conversion dimension of the full marketing audit, unchanged. The deep dive finds more than they measure, but the score comes only from them, so a conversion score from either audit means the same thing.

| ID | Check | Full | Partial | 0 |
|---|---|---|---|---|
| C1 | Primary CTA | 20: one action, consistent wording, present on every key page | 10: present but the wording varies, or it's missing on some pages | Competing or absent |
| C2 | Path to a lead | 20: a form, booking, trial or signup | 10: a form that's hard to find | `mailto:` or phone only |
| C3 | Form friction | 20: 5 fields or fewer, nothing sensitive required | 10: 6–8 fields, or no form at all (C2 already counts that gap) | More than 8, or revenue, budget or phone required up front |
| C4 | Pricing clarity | 15: public prices for the main offer, with an unambiguous currency (a bare "$" counts only if the company sells in one dollar country) | 8: prices shown but the currency is ambiguous, or some items are "quoted" with no range | Nothing, and no reason given |
| C5 | Trust at the decision point | 15: proof (a testimonial, logo or result) on the pricing or contact page itself, plus a privacy link or notice on the page with the form | 8: one of the two | Neither |
| C6 | Mobile ready | 10: viewport meta tag on all pages | 5: on some pages | None |

## How to score

1. **Score every check:** full, partial or 0, with one line of evidence (a quote, a page, or a fact from the markup). The score is the sum.
2. **No maturity relief.** None of the conversion checks carry the founder-led relief (†) used elsewhere in the full audit. A 4-person company that requires phone up front scores 0 on C3, like anyone else. Maturity changes which fixes are realistic, never the points.
3. **Score each issue once.** CTA wording belongs to C1, field count and sensitive fields to C3, currency and "quoted" items to C4, proof and privacy at the form to C5, the viewport tag to C6.
4. **Every-page checks** (C1, C6): met on all pages reviewed is full; on some is partial; on none is 0.
5. **Torn between two levels? Award the lower** and say why in the evidence.
6. **C3 scores the form on the primary path.** If the site has several forms, score the one behind the primary action (a trial signup when the trial is the main CTA, the booking form when a walkthrough is). Name the other forms in the findings.
7. **A check you can't observe** (C6 from markdown, for example) scores 0 with the evidence "not observable from <what you have>", the dimension's confidence is Low, and the report says the total is a floor that the HTML would complete. Never award points for something you couldn't see.
8. **A test is literal.** A viewport tag that blocks zoom still meets C6's test; report the zoom block as a finding. A "We respect your privacy" line counts as a notice for C5 even though a link would be better.

## Page-by-page review (the findings)

For each page, answer these with a quote:

| Area | The question | Evidence to quote |
|---|---|---|
| Primary action | What is the one thing this page wants the visitor to do? | The main CTA text and where it leads |
| Competing actions | How many actions are styled as primary in the first screen? | Each button's text (the inspection lists hero CTAs styled as primary) |
| Wording | Is the same action worded the same way on every page? | Each variant, with its page |
| Placement | Is the action reachable without hunting: in the nav or hero, and again after the main argument? | Where it appears |
| Match | Does the page deliver what the CTA before it promised? | The promise and the destination (a "free trial, no card" link that lands on a card form) |

A page whose job isn't conversion (an about page, a blog post) still gets one line: does it point to the primary action?

## Forms

For the form on the primary path, then briefly for any other:

- **Fields:** count them, and list which are required and which optional. Sensitive fields asked up front (phone, revenue, budget, card details before a free trial) are the first thing to question.
- **Labels:** a field with only a placeholder loses its label once the visitor types. Name those fields.
- **Input types and autofill:** an email field that isn't `type="email"`, a phone field that isn't `type="tel"`, and missing `autocomplete` mean the wrong keyboard and no autofill on a phone.
- **Error handling visible in the HTML:** `aria-live`, `aria-describedby`, `role="alert"` or an error element near fields. A form with `novalidate` and none of these shows no errors at all. Say what you can see; you can't see what happens after a server error.
- **Submit text:** "Submit" or "Send" says nothing about what the visitor gets. Suggest the action from the page's own words ("Book my walkthrough").
- **Privacy notice near the form:** inside it or right beside it, not only in the footer.
- **What happens next:** does the form say what follows a submit (who replies, how soon, what they'll get)? Quote it, or say it's absent.

## Friction and reassurance

- **Pricing clarity:** prices public, currency clear for where they sell, and anything "quoted" given a range or a reason.
- **Promises that the path breaks:** a claim on one page that a later step contradicts ("no credit card required" and a card form) is the most damaging friction there is. Look for it across pages.
- **Proof near the ask:** a named quote, logo or result beside the form or on pricing. Recommending that a quote move beside the form needs naming permission: if the company's `brand/proof.md` records `named: yes`, say so; if it says unconfirmed or doesn't list the quote, say to confirm permission first. Never invent a replacement quote. A named quote that is already live beside the form while brand memory records permission as unconfirmed is a 48-hour action: get the person's OK, or remove the name until you have it.

## Mobile and speed signals

Only what the markup shows. You can't measure load time or see the rendered page.

- **Viewport:** present on each page; whether it blocks zoom (`user-scalable=no`, `maximum-scale=1`).
- **Tap targets:** only sizes set in inline styles (a link or button under 44px high, text under 12px) and links with no text or label. Say that stylesheet sizes can't be seen.
- **Render-blocking scripts:** scripts in the `<head>` without `async` or `defer`. Name each one. Third-party widgets (chat, A/B tools) on the form page matter most.
- **Images:** images without `width` and `height` shift the layout as they load.

## What not to flag

A well-built page gets a short report that says so. Don't apply generic advice against the evidence:
- A form of 3–5 fields with nothing sensitive required is not too long.
- Navigation on a site page is not a defect. Removing it is a landing-page tactic for paid traffic, and only worth raising when the user says the page takes paid traffic.
- A single clear CTA repeated in the nav, hero and form is consistency, not repetition.
- A missing feature you'd personally like (a chat widget, a video, a countdown) is not friction.
- Style preferences are not findings. At most three optional nits, labelled optional, and that limit includes anything in the plan: for a sound page the plan holds only those optional items (and measurement, if they have no analytics), not new work.

## Severity

Same as the full audit: `high` for 0 points on a check worth 20, or a broken promise on the primary path; `medium` for 0 on a smaller check or partial on a 20-point check; `low` for the rest, including deep-dive findings that don't move the score (labels, input types, scripts, image sizes).
