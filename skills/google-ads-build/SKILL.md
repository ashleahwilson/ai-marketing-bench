---
name: google-ads-build
description: Builds a Google Ads search campaign ready to import, or rebuilds one from a Google Ads audit's fixes list. Produces the campaign structure (brand split from non-brand, ad groups by intent theme), keywords with match types, negative keyword lists, responsive search ads within Google's limits, sitelinks, callouts and structured snippets, location, language and bidding settings, a budget split with its reasoning, a conversion-tracking checklist and a landing page per ad group, plus a Google Ads Editor import file. Never invents search volumes, CPCs or forecasts, and uses only claims brand memory or the user supports, so no unproven "#1" or results and no competitor names in ad text. Use when the user wants Google search ads built, set up, written or restructured, for example "set up Google Ads for us", "build a search campaign", "write RSAs for this ad group", "rebuild our account from the audit", "give me keywords for Google Ads". Not for auditing an existing account, or for Meta, LinkedIn or display ads.
license: MIT
compatibility: Recommended for large models. On small models it can occasionally run a segment price or an implied offer detail brand memory doesn't state, so check the ad text. See evals/scorecard.json.
metadata:
  version: "1.2.2"
  author: "Ashleah Wilson"
---

# Google Ads build

Builds a search campaign someone can import, check and turn on. It decides the structure, writes every keyword and ad, and says plainly what it doesn't know yet: search volumes, costs and results come from data, not from the build.

## Ground rules

1. **Every claim in an ad traces to a source.** Prices, numbers, features, customer names and quotes come from brand memory (`brand/`) or the user's own words. A claim brand memory marks "needs substantiation", or a rule bans, stays out. A confirmed fact can run in the form the rule allows (a rule against "real-time" next to a confirmed 15-minute refresh means say "every 15 minutes"). A plausible number is still an invention.
2. **No data, no numbers.** Never state search volumes, CPCs, competition, click forecasts, conversion forecasts or ROAS unless the user supplied the data (a Keyword Planner export or account report). Without it, keywords are **unvalidated** and the budget is a **test**. Not even "typical" ranges.
3. **No superlatives or rankings without proof** ("#1", "best", "leading", "fastest", "most trusted"). A softened version is the same claim. No guarantees the offer doesn't include.
4. **No competitor or third-party trademarks in ad text.** Say why in one sentence: the trademark owner can have the ads restricted or file a complaint. Bidding on a competitor's name is the user's decision: offer it as an optional campaign with its own capped budget and ad text that doesn't name them, labelled "your call", and keep the main build complete without it.
5. **Hold the line, do the work.** When a request can't be met (a claim without proof, a competitor headline, volumes without data), build everything else, leave that part out, and say in one line each why and what would unlock it. Never refuse the whole build. Never lecture.
6. **Talk about the ads, not the machinery.** Never name this skill, its scripts or files like `campaign.json`, or other skills, in the reply or plan, and don't cite internal guidelines ("the skill asks for 4"). Name missing facts ("no landing page for pricing"), not missing brand-memory files.
7. **Nothing goes live.** Everything is written Paused to files. Never touch an ad account, and never overwrite the user's files: write new ones under `ads/google/`.

## Modes

- **Draft** (default): a complete first pass, with every assumption and open question listed.
- **Guided** (when the user wants to decide each part, "step by step", "walk me through"): one stage at a time, in this order: goal and conversion → budget and locations → structure → keywords → ads → assets and settings. Each turn: what you recommend and why (using brand memory), at most three questions each with a recommended default, then stop. No files until the user has made the structure decision. Keep each turn under 250 words: count them before replying, and cut background (brand gaps, later stages) first.

## Workflow

```
- [ ] 1. Load: brand/, any audits/google-ads/<account>/fixes.md, any keyword data, the user's facts
- [ ] 2. Decide what can't be done as asked, and what's missing
- [ ] 3. Design: campaigns, ad groups, keywords, negatives, settings, budget (references/campaign-design.md)
- [ ] 4. Write ads and assets (references/ad-copy-rules.md)
- [ ] 5. Write campaign.json and run scripts/build_ads.py until it has no BLOCKER
- [ ] 6. Self-check, then write plan.md and reply
```

### 1. Load

List the project folder. Read `brand/`: `offer.md` (what's sold, prices, entry offer), `audiences.md` (who, where, who it's not for), `proof.md`, `claims.md`, `results.md`, `rules.md`, `voice.md` (spelling, words never used), `competitors.md`. Look for `audits/google-ads/*/fixes.md` and any keyword export (CSV with "Avg. monthly searches").

**No brand memory?** Build from the user's facts only, mark the plan **provisional**, and offer to set up brand memory. Ad text uses only what the user said. Follow the user's spelling.

### 2. Decide what can't be done, and what's missing

Before designing, list:
- **Held back:** requested items that break a ground rule (competitor in headlines, "#1", an unproven result, a banned claim, volumes or forecasts without data). Each gets one line: what, why, what would unlock it.
- **Open questions:** facts the build needs and doesn't have, such as the primary conversion and whether it's tracked, landing pages for each theme, locations, budget. In Draft mode assume a sensible default, label it "assumed", and keep going.
- **Pushback on the plan itself:** if the budget can't support what was asked, recommend the narrower setup that can work, lead the reply with it, and build that version (offer the wider one as a later step). Under about $20/day total: one non-brand campaign, one or two ad groups, phrase and exact keywords that name the audience or category (never bare "bookkeeping" or "accounting software", even as exact), one country or region (the one the business is based in, unless the user says otherwise), no brand, competitor or third-party-brand campaign. Say the daily figure and why it's too thin for the full request. If a requested keyword is for something the business doesn't sell, or is a generic term without the audience in it, leave it out and say so. If conversion tracking doesn't exist, launching is still possible, but say that the test will only measure clicks until it's fixed.

### 3. Design

Follow [references/campaign-design.md](references/campaign-design.md): brand split from non-brand; ad groups by intent theme, each with a landing page the user or brand memory names (never an invented URL); phrase and exact match; a shared negative list including the "not for" segments; Google Search only; Presence targeting; a bid strategy that fits the account's history; a budget split with reasons, framed as a test unless the user's data says otherwise.

**From an audit:** read the fixes list as described in the reference. Build P1 and P2 fixes, hold anything marked `(confirm first)`, don't build a fix that breaks a brand rule, keep the current budget, and tag every change with its fix number.

**With keyword data:** quote it exactly; anything not in the file stays unvalidated; show the budget arithmetic from its bids.

### 4. Write ads and assets

Follow [references/ad-copy-rules.md](references/ad-copy-rules.md). One RSA per ad group with 10–15 headlines and 3–4 descriptions, each headline able to stand alone, no near-duplicates, pins only when needed. Four or more sitelinks (to real pages only), four or more callouts, one structured snippet. Use the brand's words from `voice.md` and none of its never-use words.

### 5. Check mechanically

Write the build to `ads/google/<campaign-slug>/campaign.json` in the format in [references/spec-format.md](references/spec-format.md), listing the user's own stated facts in `user_facts` and every named competitor in `competitors`. Then run:

```bash
python3 scripts/build_ads.py ads/google/<campaign-slug>/campaign.json --brand brand/ [--planner <keyword export>]
```

It checks character limits, duplicate headlines, pins, policy-risk words, competitor names, never-use words, every number in ad text against brand memory and the user's facts, keyword data against the export, negatives that block keywords, settings and the budget total. It writes `editor-import.csv` only when there's no BLOCKER. A BLOCKER means rewrite the line, never hedge it. Read every CLAIM line: a number can match brand memory and still be wrong for this ad (a group rate shown as a single-location price).

### 6. Self-check, then write

Before replying, confirm: every ad number traced; no held-back item crept into an ad, asset or the CSV; no volume, CPC or forecast without data; every landing page is a named page; the guided-mode limits if guided. Then write `ads/google/<campaign-slug>/plan.md` in this shape:

```
# <Campaign name>: Google Ads build plan
**Recommendation:** <one line: e.g. "Import paused and run a 4-week test at $X/day once the review booking is tracked">
**Status:** Draft | Provisional (no brand memory) | Rebuild from audit (<date>)

## Held back            (what was asked, why not, what would unlock it)
## Before you launch    (open questions and assumptions; conversion tracking first)
## Settings             (table per campaign: networks, locations + Presence, languages, bid strategy, daily budget)
## Structure            (campaign > ad group > theme > landing page)
## Keywords             (per ad group: keyword, match, data: unvalidated or the export's figures)
## Negative keywords    (shared list and campaign negatives, with why)
## Ads                  (per ad group: headlines with character counts and pins, descriptions with counts, paths)
## Assets               (sitelinks, callouts, structured snippets)
## Budget               (split, daily figures, reasoning, what the test measures, review points)
## Conversion tracking  (the checklist, with this brand's primary conversion named)
## Facts used           (each claim in the ads → its source in brand memory or the user's message)
## Audit fixes          (rebuilds only: fix number → done / held / not built, and where)
```

Leave out sections that don't apply (Audit fixes outside a rebuild). Never mention the checker, the spec file's internals or other tools in the plan or the reply.

**The reply** to the user leads with the recommendation (and, without brand memory, says the plan is provisional and offers to set brand memory up), then in under 250 words: what was built (campaigns, ad groups, keyword and headline counts), the held-back items in one line each, the top open questions, and the file paths (`plan.md`, `editor-import.csv`, to import Paused in Google Ads Editor). The detail lives in the plan.

## Keep tools out of the deliverable

Never name this skill, other skills, or their scripts and checks in a reply, report, draft or file the user may pass on: these often go to clients or the public. Describe what was checked, not the tool that checked it. If your environment asks you to say which skill you used, put that in one short line to the user, separate from the deliverable, never inside it.

## What good looks like

The user can import the file, read the plan in ten minutes, and know exactly what to answer before turning it on. Every claim in every ad survives a "where does that come from?" Nothing in the plan depends on a number the build made up.

A worked example (a Pipewise build that holds back a customer's "Best tool" quote and a request for search volumes) is in [assets/examples/pipewise/](assets/examples/pipewise/README.md).
