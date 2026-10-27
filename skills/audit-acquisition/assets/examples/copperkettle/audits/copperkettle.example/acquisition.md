# Acquisition audit: Copperkettle Catering
2026-10-20 · Local business (catering) · Founder-led · Pages reviewed: 4 · Data: Search Console export (queries and pages, one period) · Confidence: Medium

## Verdict
Fix the weddings page's canonical tag this week: search engines are being sent to an old URL, so the page that should win wedding searches can't.
Acquisition checklist score: 66/100 · Blocker: /weddings canonicalises to /weddings-2023

## Top three findings
1. **The weddings page tells search engines to index an old URL.** Evidence: /weddings has `rel="canonical" href="https://copperkettle.example/weddings-2023"`, and the export shows /weddings-2023 with 900 impressions, 0 clicks, at position 19.0; "wedding catering halifax" has 1,200 impressions and no clicks at position 18.5. Fix: point the canonical on /weddings at https://copperkettle.example/weddings and redirect /weddings-2023 to /weddings.
2. **The office lunch page is titled "Untitled", with no description.** Evidence: /office-lunch; in the export "office lunch catering halifax" earns 4 clicks from 1,600 impressions (0.25%) at position 4.1, while the site's own non-branded queries at positions 4 to 10 average 1.0%. Fix: title "Office lunch catering in Halifax | Copperkettle" (47 characters); description "Boxed lunches or a hot buffet delivered anywhere in Halifax and Dartmouth by 11:45. From $18 per person, minimum 15." (116 characters).
3. **The address, phone and service area aren't machine-readable.** Evidence: no structured data on any page; "2140 Gottingen St, Halifax, NS B3K 3B3" and "(902) 555-0161" appear as text on / and /contact. Fix: add LocalBusiness structured data to the home page with that address and phone, areaServed Halifax and Dartmouth, and sameAs the Instagram profile.

## Indexability and on-page basics
| Page | Title (chars) | Meta description | H1 | Canonical | Robots | Links in |
|---|---|---|---|---|---|---|
| / | Copperkettle Catering / Office and wedding catering in Halifax (62) | yes | 1 | self | none | 3 |
| /office-lunch | Untitled (8) | missing | 1 | self | none | 3 |
| /weddings | Wedding catering / Copperkettle Catering (40) | yes | 1 | /weddings-2023 | none | 3 |
| /contact | Get a quote / Copperkettle Catering (35) | yes | 1 | self | none | 3 |

robots.txt and the sitemap weren't supplied, so they weren't checked.
- The home title is 62 characters and may be cut off: "Office and wedding catering in Halifax | Copperkettle" (53) keeps the meaning.
- The buffet photo on / has no alt text: add a description of what it shows.

## Buyer questions and content
There's no blog or dated content. For a six-person kitchen that's fine, if the service pages answer what buyers ask. Topics, each tied to the site:
- How much does office catering cost in Halifax? (/office-lunch already says "From $18 per person, minimum 15 people"; the export shows "catering halifax prices" with 350 impressions and no clicks at position 12.0.)
- What's the latest we can order an office lunch? ("Order by 2 pm the day before", /office-lunch.)
- Do you cater vegan and gluten-free office lunches? (/office-lunch.)
- How many guests can you cater for a wedding? ("40 to 200 guests", /weddings.)

## AI search and answer engines
The home page has the sentence an answer engine can quote: "Copperkettle Catering cooks weekday office lunches and wedding dinners for 20 to 200 guests across Halifax and Dartmouth." The weddings page answers two real questions as headings. Add FAQ structured data to those two answers, and a short question-and-answer section to /office-lunch using the facts above.

## Local listings
One location. Address and phone match on / and /contact. No opening or delivery hours are stated, and there's no map. The Google Business Profile, its reviews and its rating aren't visible from the site: send the profile link to check that its name, address and phone match these pages.

## Channels
Instagram (footer) and a newsletter signup for seasonal menus (/). No review profiles, venue partner pages or ad tags. For a founder-led caterer, one more kind is enough: a "preferred caterer" listing on venue websites would be the natural one, if any venue lists them.

## Search data
From the Search Console export (one period, queries and pages):
- Branded ("copperkettle"): 120 of 160 clicks (75%), CTR 40.0%. Non-branded: 40 clicks from 5,650 impressions, CTR 0.7%.
- CTR by position band, non-branded: positions 4 to 10, 1.0% (40 clicks / 4,100 impressions); positions 11 to 20, 0.0% (0 / 1,550).
- Impressions without clicks: "wedding catering halifax" (1,200, position 18.5), "catering halifax prices" (350, position 12.0); page /weddings-2023 (900, position 19.0).
- A one-period export can't show which pages are losing clicks. A "compare" export (last 3 months vs previous 3 months) would.

## Checklist score
| Check | Points | Evidence |
|---|---|---|
| A1 Titles and meta descriptions | 10/20 | Titles on all 4 pages; /office-lunch is "Untitled" with no description |
| A2 On-page structure | 8/15 | One H1 everywhere; /weddings canonical points elsewhere; no structured data |
| A3 Answer-engine readiness | 15/15 | Quotable sentence on /; question headings on /weddings |
| A4 Content engine | 10/20 | No dated content: 0, raised to 10 for a founder-led company |
| A5 Channel evidence | 8/15 | One kind: Instagram |
| A6 Navigation and linking | 15/15 | Same nav on every page, linking every service page |
| **Total** | **66/100** | Founder-led relief on A4 |

## Plan
- Next 48 hours:
  - Point the /weddings canonical at itself and redirect /weddings-2023 to /weddings.
  - Replace the "Untitled" title and add the description on /office-lunch.
- Next 2 weeks:
  - Add LocalBusiness structured data to / and FAQ structured data to the two wedding answers.
  - Add a short question-and-answer section to /office-lunch (price, order cut-off, dietary options).
  - Add alt text to the buffet photo and shorten the home title.
- Next 3 months:
  - Send a compare export (last 3 months vs previous 3 months) to check the weddings fix is picked up: /weddings should replace /weddings-2023 in the pages report.
  - Ask the venues you cater for most whether they list preferred caterers, and get listed.

## Not observable
- Google Business Profile, reviews and rating: send the profile link.
- Whether /weddings-2023 still returns a page or already redirects: check it in a browser or Search Console's URL inspection.
- Backlinks and local citations: needs the Search Console links report.
- Page speed: Search Console's Core Web Vitals report.

## How this was done
Read the saved HTML of four pages (home, office lunch, weddings, contact) and a one-period Search Console export of queries and pages. robots.txt and the sitemap weren't supplied. Founder-led from "Owner-chef Rosa Delgado and a team of six" (/). Confidence is Medium: four pages, with the key service pages present.
