# Marketing Health: Tallyhouse
2026-10-10 · B2B services / professional (secondary: B2B SaaS) · First hire · Confidence: Medium

## Score
45/100 · Grade D · Rebuild the foundations, starting with acquisition and conversion.

| Dimension | Weight | Score | Headline |
|---|---|---|---|
| Positioning | 25% | 60 | Specific audience and a consistent story; the 3-day headline has no proof on any page |
| Acquisition | 20% | 34 | One blog post from March 2024; most pages have no nav, meta description or canonical |
| Conversion | 20% | 38 | The contact form asks for 10 fields, 7 of them required, including revenue |
| Brand | 15% | 47 | The home page says "AI-powered" and "not a chatbot" side by side |
| Measurement | 20% | 45 | Analytics is configured on the home page only; form submissions are not tracked |

## The three things that matter most
1. **The headline's 3-day claim is unsupported.** Evidence, index.html: "Close your books in 3 days, not 3 weeks." The only proof is Maria Okafor's quote, which does not mention timing. Fix: quote one client's measured close time with name and business, or change the H1 to a claim you can show.
2. **The contact form is too long to convert.** Evidence, contact.html: 10 fields, 7 required, including "Annual revenue" and "phone". Fix: cut it to first name, email, restaurant and number of locations. Ask revenue and phone on the call.
3. **Form submissions are not tracked.** Evidence: GA4 loads on the home, pricing and contact pages, but no conversion event appears in the source of any page. Fix: fire a lead event on successful submit, mark it as a key event in GA4, and confirm it with a test submission.

## By dimension
### Positioning (60)
Strengths: Audience is specific, with exclusions on about.html ("We don't serve retail, e-commerce or franchises with more than 15 locations"). All four pages tell the same story.
- High, P5: headline claim unsupported. Fix: see finding 1 above.
- Medium, P1: the H1 says the benefit, not the category. Fix: "Restaurant bookkeeping that closes your books in 3 days."
- Medium, P3: no alternative is named or contrasted. Fix: one comparison line under the H1.
Not observable: how buyers compare Tallyhouse with others.

### Acquisition (34)
Strengths: The home subhead is a quotable what-and-for-whom sentence.
- Medium, A4: newest content is "How to calculate prime cost (March 2024)". Fix: publish one restaurant-finance article in 30 days and link it from the home page.
- Medium, A5: no social, press, review or partner-directory links. Fix: footer links to LinkedIn, a review profile and any Toast, Square or Lightspeed listings.
- Medium, A1: meta descriptions missing on pricing, about and contact. Fix: write one for each.
Not observable: search rankings and referral traffic.

### Conversion (38)
Strengths: The form is one click from the nav and the hero (contact.html).
- High, C3: 10 fields, 7 required. Fix: see finding 2 above.
- Medium, C4: "$349/month" with no currency, in a company that sells in Canada and the US; catch-up pricing has no range. Fix: add CAD or USD, and a range for catch-up.
- Medium, C1: the primary CTA is worded three ways. Fix: use "Book a free month-end review" everywhere.
- Medium, C5: the form page has no proof and no privacy link. Fix: place the Okafor quote beside the form and a privacy link under Submit.
- Low, C6: no viewport meta tag on any page. Fix: add it to every page's head.
Not observable: form completion rate and whether submissions reach a person.

### Brand (47)
Strengths: The one testimonial is named, with business and location count (index.html).
- High, B2: the banner "New: AI-powered bookkeeping for restaurant groups" sits directly above "A real bookkeeper who knows restaurants, not a chatbot". Fix: remove the banner this week.
- Medium, B1: the inner pages are stubs without nav or footer, and title formats differ. Fix: one header, footer and title format on every page.
- Medium, B4: the dashboard image has no alt text. Fix: add alt text describing the screen.
- Low, B5: no Tallyhouse brand memory supplied, so the fallback applies. No site fix.
Not observable: brand perception and recall.

### Measurement (45)
Strengths: GA4 is in place on the home page, with no retired Universal Analytics tags and no duplicates. No ad tags are missing, as no paid activity is visible.
- High, M2: no conversion events. Fix: see finding 3 above.
- Medium, M1: gtag('config') only on the home page; pricing and contact load the library without it; about has no tag. Fix: add the config call to pricing and contact, and the full snippet to about.
- Medium, M5: no privacy policy link on any page. Fix: publish a privacy policy and link it from every footer and the contact form; add a consent mechanism if EU or UK visitors are served.
Not observable: tag-manager tracking not visible in the saved HTML, traffic, conversion rates and ad spend.

## Plan
- Next 48 hours:
  - Remove the "AI-powered" banner from index.html (B2).
  - Cut the contact form to four fields: first name, email, restaurant, locations (C3).
  - Add gtag('config','G-TH12345') to pricing.html and contact.html, and fire a lead event on successful submit (M1, M2).
- Next 2 weeks:
  - Add the viewport meta tag and the site nav to pricing, about and contact (C6, A6).
  - Publish a privacy policy, link it in every footer and beside the form, and place the Okafor quote beside the form (M5, C5).
  - Write meta descriptions for pricing, about and contact, and use one CTA phrase everywhere (A1, C1).
  - Add currency to every price and a range for catch-up pricing (C4).
- Next 1–3 months:
  - Source the 3-day claim with two or three named client close times, or change the headline (P5).
  - Publish one restaurant-finance article a month, linked from the home page (A4).
  - Add channel evidence: LinkedIn, a review profile, partner-directory listings (A5).

## How this was scored
- Pages reviewed: 4 of up to 8 (index, pricing, about, contact), saved HTML in `site/`.
- Pages missing: product or services, proof or case studies, blog listing and `/blog/prime-cost`, careers page.
- Classification: B2B services from the booking path and named bookkeepers, with SaaS features from POS integrations. First hire from "team of 14" and "We're hiring a Marketing Coordinator" (about.html).
- Confidence: Medium. Five dimensions assessed, all high-enough evidence, capped at Medium because only four pages were reviewed (score.py).
- No brand memory was supplied, so B5 uses the fallback rule.
- Scored with `scripts/score.py --pages 4`; the dimension files are in this folder.
