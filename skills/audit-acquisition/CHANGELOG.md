# Changelog

## 1.2.2 (2026-10-27)
- Skill and script names stay out of replies and deliverables (a test machine's global instruction to announce skills leaked into client-facing replies in several runs). Text-only change, not re-run.

## 1.2.1 (2026-10-24)
- Fix: the page table in check_pages.py replaced | in titles with /, so audits misquoted titles (round 3, Opus). Titles now keep the | (escaped for the table). Not re-graded.

## 1.2.0 (2026-10-24)
Round 2 (Haiku 68/68) still had small inventions: "14 bookkeepers" for "a team of 14", prices said to be on a menu image no one saw, a recommendation to link marketplace listings the site never shows, and a warning that a .example domain isn't live.
- Facts restated at the page's own scope; images never described; unseen listings asked about, not recommended.
- The page's domains are the real site, including reserved test names.
- One channel standard by maturity; band boundaries named in search data.
- No internal term for the facts file in replies.

## 1.1.0 (2026-10-24)
Round 1 (Haiku 57/68, Opus 68/68): Haiku twice told the user the site files were missing when they were in site/, and runners asked for clearer maturity and check definitions.
- Paths the user names are relative to the project folder; list it recursively and never report files missing until a recursive search is empty.
- Maturity labels defined in the scoring reference, with an assumption rule when the pages show no team size.
- A2 zero level and the A3 sentence test made unambiguous.
- Replies use plain words, not check codes or rule names; quick reads counted to under 200 words.
- Dates as precise as the page gives them; per-location ordering and map links checked for local businesses.
- --domain accepts a URL; paste-ready titles go in the on-page section; out-of-scope issues get one line.

## 1.0.0 (2026-10-24)
- First release:
  - Quick read, Draft and Guided modes; writes `audits/<domain>/acquisition.md` in a fixed shape (verdict, top three findings, indexability and on-page basics, buyer questions, AI search, local listings, channels, search data, checklist score, 48-hour / 2-week / 3-month plan, not observable, how it was done).
  - Indexability blockers (noindex, robots.txt Disallow, canonical to another URL on a key page) lead the verdict and the plan, outside the score.
  - Ends with the six acquisition checks (A1-A6) of the full marketing health audit, recomputed from the deeper findings; writes `acquisition-checks.json` in the same dimension-file format, and shows how an earlier audit's overall score would change, without editing it.
  - `check_pages.py`: titles, descriptions, H1s, heading skips, canonical, robots meta, robots.txt and sitemap conflicts, structured data and rating claims, FAQ signals, internal links in, navigation, channel kinds, newsletter, phones, postcodes, hours, map embeds, newest dated content.
  - `search_data.py`: Search Console exports (including compare exports) and analytics exports: branded split, CTR by position band, top-3 queries with low CTR, impressions without clicks, pages and queries losing clicks.
  - `score_acquisition.py` (rubric levels, founder-led relief, earlier-audit comparison) and `check_report.py` (sections, three findings, plan horizons, score match, no traffic figures without data, no guarantees, no internal names).
