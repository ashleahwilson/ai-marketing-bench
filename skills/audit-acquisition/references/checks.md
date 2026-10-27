# What to judge, area by area

The page checker measures; this file covers what needs reading. Every finding quotes the page or the measured fact behind it, names the page, and ends with a fix someone could start this week.

## Contents
- Indexability (first, always)
- On-page basics, per page
- Buyer questions and content
- AI search and answer engines
- Local listings (local businesses only)
- Channels visible from the site
- Paid presence
- Search Console and analytics exports
- What is never observable from outside

## Indexability (first, always)

Check before anything else, because nothing else matters for a page search engines are told to skip.
- Robots meta on every page: `noindex`, `none`, `nofollow`. A leftover from a staging site or a redesign is the usual cause.
- Canonical tags: missing, self, or pointing elsewhere. A canonical to a staging or old domain tells search engines to index that URL instead.
- robots.txt, if supplied: `Disallow` rules covering key pages, and a `Sitemap:` line. A page blocked in robots.txt can't have its noindex read, so fix both: remove the noindex and the Disallow together, or keep the page out on purpose and say so.
- Sitemap, if supplied: key pages missing; URLs that are noindexed, blocked or canonicalised elsewhere (conflicting signals); URLs on another domain.
- **robots.txt or a sitemap not supplied:** say "not supplied, not checked". Never say the site has none.
- Response codes, redirects, page speed and JavaScript rendering can't be seen from saved HTML: list them under "Not observable" with how to check them (Search Console's page indexing and Core Web Vitals reports, or the user's own crawl).

## On-page basics, per page

Build the per-page table from the checker: title (characters), meta description, H1 count, canonical, robots meta, in sitemap, links in from other reviewed pages. Then judge:
- **Titles.** Does each name what the page is about in the buyer's words? "Home" or the company name alone tells a searcher nothing. Over 60 characters may be cut off.
- **Meta descriptions.** Present, unique, under about 160 characters, and saying what the page offers. A meta description repeats the page's claims, so an unsupported claim in it is still unsupported.
- **H1.** One per page, saying what the page is.
- **Internal links.** Key pages and content linked from other pages. A page nothing links to (among those reviewed) is hard for search engines and people to find.
- **Images.** Missing alt text: ask for alt text describing what the image shows. Never write a guessed description of an image you can't see. A menu, price list or schedule published only as an image is invisible to search: publish it as text.

**Suggested titles and meta descriptions** use only facts already on the page or in confirmed brand memory, never a claim marked unsubstantiated or a phrase a brand rule forbids. Keep titles to 60 characters and descriptions to 160, and count them before you hand them over.

## Buyer questions and content

Content earns search visits when it answers a question a buyer actually types. Judge:
- **What exists, and how fresh.** The newest dated item and its date, as precise as the page gives it: "January 2025" is about 21 months before October 2026, never "2025-01-01, 661 days". Undated listings are a finding.
- **Whether it targets buyer questions.** Topics drawn from the offer and the audience: how much it costs, how it works with what they already use, how to do the job it replaces, how to choose. "Why every team should be data-driven" answers no one's question.
- **Proposed topics.** Phrase each as a buyer question, and tie each to something the site or brand memory says the business does (a service, a price, an integration, an audience, a stated exclusion). If brand memory lists the audience's own words or pains, use them. Never attach a search volume, difficulty or ranking forecast to a topic unless the user supplied that data.
- If a Search Console export is supplied, prefer topics it shows: queries with impressions and few clicks, and queries where a page sits just off the first page.

## AI search and answer engines

AI assistants and answer boxes quote pages that state facts plainly. Judge:
- **Entity facts.** Can a reader find, in plain sentences: what the business is, who it's for, where it operates, who runs it, what it costs, what it works with? Quote the sentence that does this, or name the page where the clear version is buried (often a product or about page) and recommend moving it up.
- **FAQ structure.** Real questions with direct answers, on the page and, where the answers are visible, marked up as FAQ structured data.
- **Structured data.** Which types exist, and whether they match what's visible. Organization (name, address, logo, sameAs social profiles), SoftwareApplication or Product, LocalBusiness for locations. A rating or review count in structured data with no reviews visible on the page is a policy risk and a credibility problem: remove it until real reviews are shown.
- **What AI assistants currently say is not observable here.** Don't claim to know which tools ChatGPT, Perplexity or Google's AI answers recommend. Offer a way to find out: a fixed list of 10 to 20 buyer questions, asked in each assistant once a month, with the answers logged.

## Local listings (local businesses only)

Apply when the business serves customers at a location or in an area (restaurants, clinics, trades, retail). Otherwise write "Not a local business: not assessed."
- **Name, address and phone (NAP)** the same everywhere they appear. Compare every page: a location page and the home page listing different numbers is a finding, quoting both.
- **One page per location** with address, phone, opening hours and a map. Missing hours are a finding; never fill them in.
- **LocalBusiness (or a subtype such as Restaurant or Dentist) structured data** per location, built only from the address, phone and hours on that page.
- **Ordering, booking and directions per location.** A delivery or booking link shared by every location, or a map embed on only one, sends people to the wrong place: each location page gets its own.
- **Google Business Profile, review counts and star ratings are not observable from the site.** Say so, and ask for the profile links or an export. Never state a rating or a review count you haven't been given.

## Channels visible from the site

List what the pages show, by kind: social profiles, newsletter signup, partner or integration listings, marketplaces and delivery apps, press, third-party review profiles, ad tags. Only the five kinds in check A5 count towards the score. Say what's missing for this business type and maturity, using one standard: founder-led, one channel working; first hire, one repeatable channel plus the profiles buyers check (a review or partner listing); small team and up, several channels, each measured. Suggest a specific listing or profile only as a question unless the pages show it exists.

## Paid presence

Report paid activity only from what's supplied (an ads export, spend figures) or visible in the source (ad tags such as Google Ads or Meta Pixel). An ad tag shows a tag is installed, not that ads are running or what they cost.

## Search Console and analytics exports

When supplied, run the search-data script and use its numbers exactly. Report:
- Branded vs non-branded clicks, when the brand terms are known (ask, or use the company name).
- CTR by position band, from the export. Name the band boundaries as used (positions under 3.5 count as 1 to 3). Compare queries with the site's own band, not with an outside benchmark. If you mention an industry benchmark, label it as one and name its source.
- Pages and queries losing clicks, with the position change. A position drop explains a click drop; it doesn't explain the cause. Name causes to check (the page changed, a competitor page, a search feature, a technical change), never one as fact.
- Pages and queries with impressions and no clicks: usually a title and meta description problem when the position is good, or a page sitting on page two when it isn't.
- State the export's period on every figure ("last 3 months vs previous 3 months").

## What is never observable from outside

Traffic and visits, search volume, rankings and positions, keyword difficulty, backlinks, ad spend, conversion rates, Google Business Profile reviews, and what AI assistants answer. Without a supplied export, none of these appears as a number anywhere in the report or the reply: not as a range, an estimate, or "roughly". Say what would provide each one (the company's Search Console, analytics, rank-tracking export or ad account), and ask for it.
