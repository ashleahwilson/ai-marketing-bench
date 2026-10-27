# Conversion audit: Tallyhouse
2026-10-24 · B2B services (secondary: B2B SaaS) · First hire · Pages reviewed: 4 · Confidence: High

## Verdict
Conversion checklist score 38/100. Cut the contact form to four fields this week: it is the only path to a lead, and it asks for annual revenue and a phone number before anyone has spoken to you.

## The three findings that matter most
1. **The contact form asks for too much, too early.** Evidence, contact.html: 10 fields, 7 required, including "Annual revenue" and "phone". Fix: keep first name, email, restaurant name and number of locations; ask revenue and phone on the review call; drop or make optional the rest.
2. **Nothing at the form reassures the owner.** Evidence, contact.html: no privacy link or notice, no line about what happens after "Submit", and no proof on the page. Fix: add "We use your details only to book your review" with a privacy policy link under the button, and one line on what follows (who replies and when, once you've decided it). Move the Maria Okafor quote beside the form only after she confirms you may name her: brand memory records her permission as unconfirmed.
3. **No page is set up for phones.** Evidence: none of the four pages has a `<meta name="viewport">` tag, so phones render the desktop layout, form included. Fix: add `<meta name="viewport" content="width=device-width, initial-scale=1">` to every page's head, then fill in the form on a phone.

## Page by page
### index.html · primary action: "Start with a free month-end review" → /contact
- Primary action: one action, repeated in the nav as "Book a free review". Fine, apart from the wording (see contact.html).
- Proof: "We finally know our prime cost before the month is over." — Maria Okafor, owner, Lantern Noodle Bar (3 locations). Specific and attributed. Naming permission is unconfirmed in brand memory.
- Images: the dashboard image has no `alt`, `width` or `height`. Fix: add all three.
- Mobile: no viewport tag (finding 3).

### pricing.html · primary action: "Book a free review" → /contact
- Prices: "$349/month" and "From $299/location/month", with no currency. About.html says you serve "restaurants across Canada and the US", so a bare "$" is ambiguous. Fix: "$349 CAD/month" (or USD, or both).
- "Catch-up bookkeeping: Quoted per month of backlog" gives no range or reason. Fix: a "from" price per month of backlog, or say what drives the quote.
- No proof on the page where owners compare price. Fix: the Okafor quote here works too, once permission is confirmed.

### contact.html · primary action: "Submit" (form) 
- The H1 "Book your free month-end review" is the third wording of the same action ("Book a free review" in the nav and on pricing, "Start with a free month-end review" on the home page). Fix: use "Book a free month-end review" everywhere, including the button.
- Form: see Forms.

### about.html · no call to action
- The page ends at "We're hiring a Marketing Coordinator" with no link to the review. Fix: one "Book a free month-end review" link after the team paragraph.

## Forms
**contact.html, the only form.** 10 fields: first_name, last_name, email, phone, restaurant, locations, pos, revenue, current_bookkeeper, message. Required: first_name, last_name, email, phone, restaurant, locations, revenue. Optional: pos, current_bookkeeper, message.
- Labels: every field relies on a placeholder or has no prompt at all (email, phone, the POS menu and message), so the prompt disappears once someone types. Fix: a visible label above each field you keep.
- Input types: phone is a plain text field, so phones show the letter keyboard. If you keep it (optional, after the cut), make it `type="tel"`. No field has `autocomplete`, so browsers can't fill name and email.
- Error handling: browser validation only; there's no error message element in the HTML. Fix: an inline message under each required field.
- Submit text: "Submit". Fix: "Book my free review".
- Privacy near the form: none. What happens next: none. (Finding 2.)

## Funnel
Not observable: no analytics export supplied. Send page views of /contact, form starts and form submits for one month (from GA4, which already loads on the contact page) to see where owners drop off.

## What's working
- One click from the nav or the home hero reaches the form (index.html, "Book a free review" → /contact).
- Prices for the two main plans are public (pricing.html).
- The one testimonial is specific and attributed, with business name and location count (index.html).
- No render-blocking scripts: the analytics tag loads `async` on every page that has it.

## Plan
- Next 48 hours:
  - Cut the contact form to first name, email, restaurant and locations; rename the button "Book my free review" (contact.html).
  - Add the viewport tag to all four pages.
  - Ask Maria Okafor for written permission to use her name and quote beside the form.
- Next 2 weeks:
  - Add a privacy line with a policy link and a what-happens-next line under the form (contact.html).
  - Use "Book a free month-end review" as the only CTA wording (nav, home hero, pricing, contact H1).
  - Add currency to every price and a "from" price for catch-up work (pricing.html).
  - Add visible labels, `autocomplete`, and inline error messages to the form.
- Next 3 months:
  - Track form submits as a conversion event, so the next audit can read the funnel instead of guessing it.
  - Collect one or two more named quotes with permission, so pricing and contact each carry proof.

## Test backlog
| # | Hypothesis | Change | Metric |
|---|---|---|---|
| 1 | Owners comparing prices on pricing.html leave to think it over before clicking through to a separate contact page | Put the four-field form at the foot of pricing.html as well as on contact.html | Form submits per pricing-page visit |
| 2 | Owners don't know what the free review involves, so the ask feels like a sales call | Add three lines above the form saying what the review covers and how long it takes, using the wording you already use for the review | Form starts per contact-page visit |
| 3 | A named peer beside the form makes the ask feel safer (once permission is confirmed) | Show the Okafor quote beside the form for half the period, without it for the other half | Form submits per form start |

Run these one at a time after the fixes above, comparing equal periods, and only once form submits are tracked.

## Not observable and how this was done
- Not observable: conversion rates, form starts and submits, lead volume, how fast submissions are answered, how the pages render, load times.
- Pages reviewed: index, pricing, about and contact, as saved HTML. Missing: any services, case-study or campaign landing pages.
- Business type: B2B services (named bookkeepers, a booking path) with software features (POS integrations). Maturity: first hire, from "a team of 14" and "We're hiring a Marketing Coordinator" (about.html).
- Brand memory read: offer, proof (Okafor naming unconfirmed), rules and voice (Canadian spelling).
- Confidence: High: four HTML pages including the form page.

## Conversion checklist score

| Check | Points | Max | Evidence |
|---|---|---|---|
| C1 Primary CTA | 10 | 20 | One action, worded three ways: "Book a free review" (nav, pricing), "Start with a free month-end review" (home), "Book your free month-end review" (contact H1) |
| C2 Path to a lead | 20 | 20 | Form at /contact, linked from the nav and the home hero |
| C3 Form friction | 0 | 20 | 10 fields, 7 required, including revenue and phone |
| C4 Pricing clarity | 8 | 15 | Prices public but bare "$" for a Canada and US business; catch-up "quoted" with no range |
| C5 Trust at the decision point | 0 | 15 | No proof on pricing or contact; no privacy link or notice on the form page |
| C6 Mobile ready | 0 | 10 | No viewport tag on any of the four pages |

**Total: 38/100**
