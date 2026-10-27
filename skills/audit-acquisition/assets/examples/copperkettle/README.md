# Worked example: Copperkettle Catering

Copperkettle Catering is a fictional six-person caterer in Halifax that cooks office lunches and wedding dinners. The owner asked: "How do people find us online, and what should we fix first? Pages are in site/, and I exported Search Console into gsc/. Today is 2026-10-20."

Inputs:
- `site/`: saved HTML of the home, office lunch, weddings and contact pages.
- `gsc/`: a one-period Search Console export (`Queries.csv`, `Pages.csv`).
- No brand memory, robots.txt or sitemap.

Outputs:
- [audits/copperkettle.example/acquisition.md](audits/copperkettle.example/acquisition.md): the acquisition file.
- [audits/copperkettle.example/acquisition-checks.json](audits/copperkettle.example/acquisition-checks.json): the six checks, in the full audit's dimension-file format.

The reply to the owner:

> **Fix the weddings page's canonical tag this week.** It tells search engines to index an old URL (/weddings-2023), and your export shows that old URL with 900 impressions and no clicks at position 19. Acquisition checklist score: 66/100.
>
> 1. /weddings canonicalises to /weddings-2023: point it at itself and redirect the old URL.
> 2. /office-lunch is titled "Untitled" with no description, and "office lunch catering halifax" gets 4 clicks from 1,600 impressions at position 4.1.
> 3. No structured data, so your address, phone and service area aren't machine-readable.
>
> Next 48 hours: fix the canonical and the redirect; give /office-lunch a real title and description (both are written out in the file).
>
> The full audit is in audits/copperkettle.example/acquisition.md. I couldn't see your Google Business Profile or reviews: send the profile link and I'll check its name, address and phone match the site. A "compare" Search Console export (last 3 months vs previous 3 months) would show which pages are gaining or losing clicks.

What it shows: the blocker leads even though the score is respectable; every figure comes from the pages or the export; founder-led relief is applied to the content check only; and the suggested title and description use only facts already on the page.
