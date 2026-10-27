# Measurement: Saltbox Coffee Roasters
2026-10-22 · Sources: 3 HTML pages (home, product, order confirmed); no container export; no analytics export · Confidence: Low

## Verdict
The site can count purchases: the order confirmation page pushes a purchase event, and Google tags wait for consent. Two things need fixing first: the purchase event carries the customer's email, and the Meta Pixel loads before anyone answers the cookie banner.
Measurement score: 95/100 (M1 30/30 · M2 30/30 · M3 15/15 · M4 15/15 · M5 5/10)

## The three things that matter most
1. **The purchase event sends the customer's email.** Evidence: order-confirmed.html, `dataLayer.push({event:"purchase", … customer_email:"{{customer.email}}"})`. Anything in the container that reads the data layer can forward it to analytics or ad tags. Fix: delete `customer_email` from the push this week. Keep transaction_id, value and currency.
2. **The Meta Pixel loads before the cookie banner.** Evidence: on every page, `fbq("init","290018833471652")` and `fbq("track","PageView")` sit in the head above the CookieYes script. Consent mode holds the Google tags, but it doesn't control the pixel. Saltbox sells only in Canada (brand memory), so this is worth reviewing with whoever handles privacy. Fix: move the pixel into the container and fire it only after marketing consent.
3. **Newsletter signups aren't tracked.** Evidence: the footer form (#newsletter, posting to /subscribe) appears on every page, and no event fires for it. Fix: send people to a /subscribed page after signup and track `sign_up` on that page view, with `method: newsletter`.

## What the site can measure today
| Tag | ID | Pages | State | Before consent? |
|---|---|---|---|---|
| Google Tag Manager | GTM-SB31KQ | 3/3 | Loaded after a consent mode default (all denied) | No (held by consent mode) |
| Meta Pixel | 290018833471652 | 3/3 | Configured, PageView on load | Yes |
| CookieYes banner | n/a | 3/3 | Present | n/a |

Conversions: `purchase` is pushed to the data layer when the order confirmation page loads, which is the real outcome. Whether the container forwards it to GA4 and Meta can't be seen without the export.
Forms: the footer newsletter form (one field, email) has no tracking.
UTM handling: no internal links carry UTMs.

## Privacy and consent
Google tags start with consent denied, which is the setup a Canadian audience calls for. The Meta Pixel loads before any choice on every page, and the purchase event includes the customer's email. Both are flags to review with whoever handles privacy, not legal advice.

## Not observable
Order and traffic counts, which tags the container fires (needs the container export), whether GA4 receives the purchase event (needs GA4 DebugView or property access), and ad spend.

## Plan
- Next 48 hours:
  - Remove `customer_email` from the purchase push on the order confirmation page.
  - Export the GTM container (Admin > Export container) so the tags inside it can be checked.
- Next 2 weeks:
  - Move the Meta Pixel into the container, fired only after marketing consent, and remove the hard-coded copy.
  - Add a /subscribed page and a `sign_up` event for the newsletter.
  - Place a test order and confirm one purchase event, with value and currency, in GA4 DebugView.
- Next 3 months:
  - Mark `purchase` and `sign_up` as key events in GA4 and check them against the store's own order count each month.
  - Add `begin_checkout` and `add_to_cart` to see where buyers drop off.

## Measurement checklist
| ID | Check | Points | Evidence |
|---|---|---|---|
| M1 | Analytics configured on every page | 30/30 | GTM-SB31KQ on all 3 pages |
| M2 | Conversions tracked | 30/30 | order-confirmed.html pushes `purchase` on the confirmation page |
| M3 | Ad platform tags | 15/15 | Meta Pixel on every page |
| M4 | Hygiene | 15/15 | No Universal Analytics, no duplicate tags visible |
| M5 | Consent basics | 5/10 | Privacy link sitewide; the banner and consent mode hold Google tags but not the Meta Pixel, so scored as a policy link only |
Score: 95/100. No earlier audit in this folder.
