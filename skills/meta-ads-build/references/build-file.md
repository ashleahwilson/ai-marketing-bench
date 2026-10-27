# The build file

## Contents
- Where it goes
- Format
- Field rules
- The upload file

## Where it goes

`ads/meta/<campaign-slug>/build.md` is the source of truth. The checker exports `ads/meta/<campaign-slug>/ads.csv` from it (one row per ad). If you revise, overwrite your own build file; never write into the user's drafts, briefs or audit files. A check-and-fix of the user's drafts goes to `<their-file>-fixed.md` beside the original, in this same format.

## Format

```
# Meta build: <campaign name>
Status: draft | provisional (no brand memory) 
Mode: draft | rebuild | check and fix
Campaign: <campaign name>
Special ad category: none | employment | housing | financial products and services | social issues
Countries: <ISO codes or names>
Objective: <Leads | Sales | Traffic | Engagement | Awareness | App promotion>
Optimization event: <event and where it fires, e.g. Lead on /review/booked (pixel, tested 2026-10-18)>
Daily budget: <amount and source, or [TBD: budget]>
Budget level: campaign (Advantage+ campaign budget) | ad set
Offer: <the short offer phrase that must appear early in every primary text, e.g. free month-end review>
Landing page: <URL or [link: landing page needed]>

FACTS
- <fact the ads may use> | <source: brand/offer.md · confirmed, brief, user, audit F2>
OPEN
- <gap only the user can fill>

## Ad set: <name>
Audience: <broad / Advantage+ audience, with any suggestions>
Age: 18-65+
Gender: all
Location: <country, region, or city + radius>
Detailed targeting: none
Custom audiences: <name (size) | consent: <basis> | use: exclusion / seed / retargeting>  or none
Lookalikes: <seed and %>  or none
Exclusions: <current customers, recent leads>
Placements: Advantage+ placements | <manual list and why>
Budget: <only if budget level is ad set>

## Ad: A1
Ad set: <exact ad set name>
Concept: <one line: the angle and the format>
Hook: <the first line: the words a scroller sees first, or the first 3 seconds of a video>
Primary text: <body; the hook and the offer inside the first 125 characters>
Headline: <40 characters or fewer>
Description: <30 characters or fewer>
CTA button: <a Meta button: Learn more, Sign up, Book now, Apply now, Get quote, Contact us, Download, Subscribe, Shop now>
URL: <landing page with UTM, or placeholder>
Format: single image | video | carousel
Aspect ratios: 1:1 or 4:5 for feed; 9:16 for Stories and Reels
On screen: <what the image or video shows, text overlay, and for video a beat list with seconds>
Proof used: <brand/proof.md line, or none>
```

## Field rules

- One field per line, `Field: value`. A long primary text can continue on the following lines until the next field.
- **Hook**: if the ad is a video whose hook is visual, start the hook with `[visual]` and still front-load the primary text.
- **Primary text**: about 125 characters show before "See more" in feed. The hook and the offer go there. Total under 2,200; most good ones are 1 to 4 short sentences.
- **Headline**: 27 characters shows almost everywhere; 40 is the most that shows reliably in feed. Never over 40.
- **Description**: shows only on some placements; 30 characters or fewer, never essential to the message.
- **On screen**: text overlay kept short (a few words), never a claim the copy can't make. For video: captions on, the point in the first 3 seconds, a 9:16 cut for Reels and Stories with the key content clear of the top and bottom 14% (interface overlays).
- **FACTS**: every figure, price, name, quote and offer detail in any ad appears here with its source. Missing stays missing: `[TBD: …]` in OPEN, never a plausible value.

## The upload file

`ads.csv` columns: Campaign Name, Special Ad Categories, Campaign Objective, Optimization Goal, Countries, Daily Budget, Ad Set Name, Location, Age, Gender, Audience, Custom Audiences, Lookalikes, Exclusions, Placements, Ad Name, Body, Title, Link Description, Call to Action, Link, Creative Format, Aspect Ratios, Creative Brief. The names follow Ads Manager's bulk-import labels where one exists (Body, Title, Link Description, Call to Action, Link). Tell the user to map them to their account's current import template and add the image or video file names before importing.
