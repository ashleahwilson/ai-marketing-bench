# Google Ads audit: Brightwater Physio

**Score: 35/100 (F) · Confidence: High (60 days, 70 real conversions) · August 1 to September 29, 2026 · Spend $3,526.65**
Make "Contact page view" a secondary action first: bidding is learning from page views, and every other number in the account is distorted until it stops.

## Top three findings
1. **A page view counts as a booking.** Evidence: "Contact page view" (category Page view, counted Every) is a primary action alongside "Booking confirmed", adding 12 of the 82 conversions. Reported cost per conversion is $43.01; cost per real booking is $50.38. Fix: set "Contact page view" to secondary. At stake: the signal Maximize conversions bids on in Search | Physiotherapy.
2. **Irrelevant searches with no bookings.** Evidence: "physio jobs halifax" $212.40, "massage chair for back pain" $176.20, "physiotherapy course online" $148.75, "physio exercises for knee pdf" $94.85, all 0 conversions. The campaign's only negative, [jobs], is exact match, so it doesn't block "physio jobs halifax". Fix: phrase negatives "jobs", "course", "pdf", "massage chair", "exercises". At stake: $632.20 in 60 days.
3. **Search Partners spend with no bookings.** Evidence: Search | Physiotherapy spent $203.10 on Search Partners, 0 conversions. Fix: turn off Search Partners. At stake: $203.10 in 60 days.

## Scorecard
| Check | Status | Key number |
|---|---|---|
| Conversion tracking | FAIL | 12 of 82 conversions are page views |
| Wasted spend and negatives | FAIL | $632.20 on irrelevant terms (17.9% of search-term spend) |
| Match-type mix | PASS | 29.2% of keyword spend on broad |
| Budget limits | WARN | Search | Physiotherapy loses 12.5% of impression share to budget |
| Bid strategy vs volume | PASS | 30 conversions per 30 days on Maximize conversions |
| Quality Score | WARN | Spend-weighted 6.5; "sports injury physio" below average on Exp. CTR and landing page |
| Responsive search ad coverage | WARN | Sports injury: 6 headlines, 2 descriptions, Poor |
| Location targeting | WARN | Search | Physiotherapy uses Presence or interest |
| Network settings | FAIL | $203.10 on Search Partners, 0 conversions |
| Brand / non-brand split | PASS | Brand runs in its own campaign |
| Landing page match | FAIL | Sports injury ad group sends traffic to the homepage |

## Findings by check
### 1. Conversion tracking
Primary actions: "Booking confirmed" (70) and "Contact page view" (12, counted Every). A page view isn't a booking. Demote it to secondary; keep it for reporting. Until then, the 82 conversions overstate bookings by 12.

### 2. Wasted spend and negatives
Four terms, $632.20, 0 conversions (listed above). "massage chair for back pain" is a product search; brand memory says the clinic doesn't sell equipment. Negatives go on Search | Physiotherapy as phrase match. Replace [jobs] (exact) with "jobs" (phrase).

### 3. Match-type mix
Exact $96.40, phrase $2,399.15, broad $1,031.10. Broad runs on Maximize conversions. No change, once conversion tracking is fixed.

### 4. Budget limits
Search | Physiotherapy loses 12.5% of search impression share to budget ($60/day, averaging $57.17). The $632.20 of waste and $203.10 of partner spend in the same campaign is money to move before any budget increase.

### 5. Bid strategy against conversion volume
Search | Physiotherapy: 60 conversions in 60 days on Maximize conversions. Search | Brand: Maximize clicks. Both fine for the volume, though the 60 includes page views.

### 6. Quality Score
Spend-weighted 6.5. "sports injury physio" (Quality Score 5, $1,031.10) is Below average on Exp. CTR and Landing page exp.

### 7. Responsive search ad coverage
Sports injury has one ad with 6 headlines and 2 descriptions, ad strength Poor. Add headlines from facts already in the other ads (direct billing, evening appointments, registered physiotherapists). No brand-rule breaches in live ads.

### 8. Location targeting
Search | Physiotherapy targets Halifax with "Presence or interest", which shows ads to people outside Halifax who show interest in it. Switch to Presence. No user-locations export, so spend outside Halifax isn't measured.

### 9. Network settings
Search Partners: $203.10, 0 conversions. Turn off. No Display Network on either campaign.

### 10. Brand and non-brand split
Brand terms ("brightwater") run only in Search | Brand. Fine.

### 11. Landing page match
Sports injury ($1,031.10) points to the homepage, and its keyword's landing page rating is Below average. Point it at the booking page the Physiotherapy ad group uses (brightwaterphysio.example/book), or a sports injury page if one exists.

## Plan
**Next 48 hours:** demote "Contact page view"; add the five phrase negatives and remove [jobs]; turn off Search Partners; switch Search | Physiotherapy to Presence.
**Next 2 weeks:** rewrite the Sports injury ad to 8+ headlines and 3+ descriptions; change its final URL.
**Next 3 months:** re-run this audit on 60+ days of clean booking data; decide on budget once waste is gone.

## Not checked
- Spend outside Halifax: needs the user-locations report.

## Sources and assumptions
- Exports: campaigns, campaigns-by-network, campaign-settings, keywords, search-terms, negative-keywords, ads, conversion-actions (August 1 to September 29, 2026)
- Brand memory: BRAND.md, offer.md, rules.md
- Assumptions: none beyond the relevance calls above, each with its reason
- Rules of thumb used: 8+ headlines and 3+ descriptions; 15+ conversions per 30 days for target-based bidding; confidence thresholds. These are this audit's, not Google's.
- Read-only: no changes were made to the account.
