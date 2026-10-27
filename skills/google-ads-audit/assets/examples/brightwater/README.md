# Worked example: Brightwater Physio

A fictional single-clinic physiotherapy practice in Halifax. Sixty days of exports, brand memory present, draft mode.

**The request:** "Audit our Google Ads, exports are in exports/."

**Files**
- `exports/`: the CSV downloads (campaigns, network segment, settings, keywords, search terms, negatives, ads, conversion actions)
- `brand/`: the clinic's brand memory
- `audits/google-ads/brightwater-physio/AUDIT.md`: the report
- `audits/google-ads/brightwater-physio/fixes.md`: the fixes list for whoever applies the changes
- `audits/google-ads/brightwater-physio/working/irrelevant.txt`: the search terms judged irrelevant, with reasons
- `audits/google-ads/brightwater-physio/working/metrics.json`: every computed figure

**The reply**

> **35/100 (F), confidence High.** Fix what bidding learns from first: a contact page view counts as a booking, so the account is optimizing toward the wrong thing.
>
> **Top three**
> 1. "Contact page view" is a primary conversion · 12 of 82 conversions · make it secondary. Cost per real booking is $50.38, not the $43.01 shown.
> 2. Irrelevant searches · $632.20 on job seekers, courses, PDFs and massage chairs, 0 bookings · add phrase negatives; the existing [jobs] negative is exact match and misses "physio jobs halifax".
> 3. Search Partners · $203.10, 0 bookings · turn it off in Search | Physiotherapy.
>
> **Do in the next 48 hours:** demote the page view, add the four negatives, turn off Search Partners, switch Search | Physiotherapy to Presence targeting.
>
> Full audit and a fixes list are in audits/google-ads/brightwater-physio/.

No result is claimed: the example shows the method, not an outcome.
