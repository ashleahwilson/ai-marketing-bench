# The acquisition checklist score

The deep dive ends with the same six checks the full marketing health audit uses for its acquisition dimension, so the two always agree. The deeper findings decide each check; the checks decide the score. Never adjust the total by hand.

## Contents
- The six checks
- How to decide each check
- Maturity relief
- Blockers sit outside the score
- The checks file
- When an earlier audit exists

## The six checks

| ID | Check | Full | Partial | 0 |
|---|---|---|---|---|
| A1 | Titles and meta descriptions | 20: unique title and meta description on every page | 10: titles everywhere, some meta descriptions missing | Titles missing or duplicated |
| A2 | On-page structure | 15: one H1 per page, logical H2s, a canonical tag, structured data | 8: two or three of these | One or none |
| A3 | Answer-engine readiness | 15: a plain, quotable "what we do, for whom" sentence, plus FAQ-style content | 8: one of the two | Neither |
| A4 † | Content engine | 20: new content in the last 90 days, on topic for the audience | 10: within 12 months | Older, or none |
| A5 † | Channel evidence | 15: two or more kinds visible (ad tags, social profiles, press, third-party reviews, partner or integration listings) | 8: one kind | None visible |
| A6 | Navigation and linking | 15: navigation on every page; key pages linked | 8: navigation missing on some pages | No usable navigation |

## How to decide each check

Use the measured page facts, one line of evidence per check (a quote, a page, or a measured fact). When torn between two levels, award the lower one and say why. Score each issue once: it belongs to exactly one check.

- **A1.** Full only if every reviewed page has a title and a meta description and no two pages share either. Titles on every page and unique, but a meta description missing or duplicated on some: 10. Any page without a title, or two pages with the same title: 0. Length problems (a title over 60 characters) are findings, not point losses.
- **A2.** Count four elements on each page: exactly one H1; H2s with no skipped levels; a canonical tag pointing to the page itself (a canonical pointing to another page or domain doesn't count); structured data. All four on every page: 15. Every page meets at most one of the four: 0. Anything between: 8.
- **A3.** The sentence must say what the business does and for whom, in plain words, on the home page or the main product or service page, quotable as it stands. Two adjacent sentences that do it together count. For a local consumer business, the place served ("three locations in Toronto") is the "for whom". A sentence that also carries an unsupported claim still counts here; flag the claim separately. Only a sentence that says neither what nor for whom (a slogan) fails. FAQ-style content means questions as headings, an FAQ section, expandable questions or FAQ structured data. One "Questions?" heading over a contact line isn't FAQ content.
- **A4 †.** Use the newest dated item on topic for the buyer (a post, guide, case study, update). Count days back from the audit date. Undated content can't earn points: say so. A blog listing with no dates scores 0 and is a finding.
- **A5 †.** Count kinds, not links: two social profiles are one kind. A map embed is not a review listing. A newsletter signup and a delivery-app listing are channel signals to report, but only the five kinds in the table count here (delivery apps and marketplaces count as partner or marketplace listings).
- **A6.** Navigation on every reviewed page and every key page linked from at least one other page: 15. Navigation missing on some pages, or a key page with no link to it from any reviewed page: 8. No usable navigation: 0.

## Maturity relief

Classify from evidence on the pages or in an earlier briefing, and quote it:

| Maturity | Signals |
|---|---|
| **Founder-led** | Under about 10 people, the founder is the face and voice, no marketing roles. "A small team" with a named founder and no headcount counts here |
| **First hire** | About 10–50 people, one marketer or hiring the first (a 14-person firm hiring its first marketing coordinator is first hire) |
| **Small team** | 2–5 marketers, regular content, some paid activity |
| **Full function** | Marketing leadership, specialists, many channels |

If the pages give no evidence of team size (a restaurant with three locations and no about page), say so, classify it as founder-led as a stated assumption, and say the score falls by the relief amount if they're larger.

For a **founder-led** company only, A4 or A5 that would score 0 gets its partial credit instead (10 and 8). First-hire and later companies get no relief. Use the maturity from an earlier audit's briefing if one exists; otherwise classify it from evidence (team size, roles, open jobs), quoting it. Never relax the unmarked checks.

## Blockers sit outside the score

The six checks don't measure whether pages can be indexed at all. A **blocker** is a key page (home, pricing, product or services, contact, booking, demo, location pages) that:
- carries a robots meta `noindex` (or `none`),
- is blocked by a robots.txt `Disallow` rule (which also hides any noindex tag from crawlers), or
- has a canonical tag pointing to another page or domain (for example a staging host).

A blocker doesn't change the checklist score, but it overrides everything else: it is finding 1, it leads the verdict line, it's in the 48-hour plan, and any content or channel plan waits until it's fixed. A noindexed or canonicalised page that the sitemap lists is a conflicting signal: name it with the blocker.

## The checks file

Save `audits/<domain>/acquisition-checks.json` in the same format as the full audit's dimension files, so either can be compared with the other:

```json
{"dimension": "acquisition", "maturity": "first hire", "assessable": true, "confidence": "high|medium|low",
 "audit_date": "2026-10-24", "pages_reviewed": ["/", "/pricing"],
 "checks": [{"id": "A1", "points": 10, "max": 20, "evidence": "Titles on all 5 pages; meta description only on /"}],
 "score": 0,
 "blockers": ["/pricing: robots meta 'noindex, nofollow'"],
 "findings": [{"severity": "blocker|high|medium|low", "check": "A1|indexability|local|channels|search data",
   "finding": "...", "evidence": "...", "fix": "..."}],
 "strengths": ["..."], "not_observable": ["..."]}
```

Then run `python3 scripts/score_acquisition.py audits/<domain>/`. It recomputes `score` from the checks, rejects points the rubric doesn't allow, and applies the relief rule. Fix any FAIL and run it again.

Severity: `blocker` for indexability on a key page; `high` for 0 points on a 20-point check, or a search-data loss on the page that earns the most non-branded clicks; `medium` for 0 on a smaller check or partial on a large one; `low` for the rest.

## When an earlier audit exists

If `audits/<domain>/dim-acquisition.json` and `score.json` exist from a full marketing health audit, read them first. Re-score from the evidence, not from the earlier numbers. The script prints the earlier score, each check that changed, and what the overall score and grade would become. Report the change and the reason for each changed check. Leave the earlier files exactly as they are: the user decides whether to adopt the new score.
