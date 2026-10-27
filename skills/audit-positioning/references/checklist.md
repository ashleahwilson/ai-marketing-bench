# The positioning checklist (P1–P5)

These are the same five checks the full marketing audit uses for its positioning dimension, with the same points and tests. The deep dive scores them last, from its deeper findings, so a full audit that reads the result gets the same number. Never change a check, its points or its test here.

## Contents
- The checks
- How to score
- What belongs to other dimensions
- How the deep dive feeds each check
- The checklist file

## The checks

| ID | Check | Full | Partial | 0 |
|---|---|---|---|---|
| P1 | The headline says what it is in plain words | 20: what it does is clear from the headline alone | 10: clear only after the subhead | Buzzwords; it fails the swap test (a competitor's name fits) |
| P2 | Audience is named | 20: a specific audience plus exclusions | 10: a specific audience | "Teams", "businesses", or none |
| P3 | Differentiation from the alternative | 20: one specific true difference, set against what buyers use now | 10: specific but not contrasted | Generic benefits only |
| P4 | Consistency across pages | 20: every page reviewed names the same product, audience and core benefit | 10: one page names a different audience or benefit | Pages describe different products, or the about page is clearer than the home page (contradictions within a page belong to B2; CTA wording to C1) |
| P5 | Claims are supported | 20: bold claims backed by proof, or qualified | 10: some unsupported | The headline claim, or a superlative, is unsupported or contradicted |

## How to score

1. Each check scores exactly 0, 10 or 20. The total is the sum. Nothing else moves it.
2. **One line of evidence per check:** a quote and its page, or a brand-memory line. "Clear" and "generic" are judgments; the quote is what lets someone else check them.
3. **When torn between two levels, award the lower one** and say why in the evidence.
4. **No maturity relief.** None of the positioning checks is relieved for founder-led companies in the full audit, so none is relieved here. Maturity changes the plan and the size of the fixes, never the points.
5. **Score each issue once.** An issue that fits two checks goes in the one whose test names it.
6. **The about page is clearer than the home page** when another page (about, how it works, pricing) says plainly what the product does or who it's for and the home page doesn't. That is P4 at 0, even if every page is otherwise "on topic".
7. **P1 in plain words.** A headline that names the category and the buyer in plain words ("Scheduling software for independent dental clinics") scores 20, even if a rival in the same niche could describe itself the same way. That's a description, not a slogan, and naming the category is the point of the check. The swap test fails a headline made of buzzwords or a slogan with no category ("Payroll that just works", "Actionable insights for modern brands").
8. **P2 counts the whole site.** Audience and exclusions count wherever they appear on the pages reviewed: a specific audience on the home page plus exclusions on the about page is 20. Where they appear is a finding for the report, not a deduction.
9. **P4 needs a real difference.** Pages have different jobs: pricing lists what's included, about tells the founding story, contact has a form. That isn't inconsistency. Deduct only when a page names a different audience, a different product or a different core benefit, or when another page says what the product is more plainly than the home page.
10. **P1 and the swap test.** Without competitor pages, the swap test is the generic one: could any company in this category put its name on the headline unchanged? With supplied competitor pages, it's literal: quote the competitor line that matches.
11. **P5 and brand memory.** A claim brand memory lists under "Needs substantiation" is unsupported. A claim that a brand rule, brand memory fact or another page contradicts ("real-time" against "refreshes every 15 minutes") is contradicted. Both are 0 when it's the headline claim or a superlative. One customer's result supports a claim about that customer; a claim made about every customer ("every month closes by the 3rd") backed by a single account is partial (10) unless it's qualified. A restatement of the same promise ("P&L ready by the 3rd" beside "close in 3 days") is the same claim. Plain descriptions of the company itself (who the team is, where it's based, what's included on a plan) aren't claims that need proof.

## What belongs to other dimensions

Mention these in the deep dive where they help, but never take positioning points for them:
- **CTA wording that varies across pages** belongs to conversion (C1).
- **A contradiction within one page,** such as a banner that says "AI-powered" above "a real person, not a chatbot", is message drift (B2). It can shape the category-frame discussion, and it can be one of the top three findings, but it doesn't touch P4.
- **A breach of the audited company's own brand rules** that isn't a claim (a banned word, a tone rule) belongs to brand (B5). A capability claim the rules or facts contradict is P5.

## How the deep dive feeds each check

| Lens (see lenses.md) | Feeds |
|---|---|
| Who it's for, and who it's not | P2 |
| Category frame | P1 |
| Problem and the alternative | P3 |
| Differentiated value and proof | P3, P5 |
| Consistency across pages | P4 |
| Specificity and the swap test | P1, P3 |

## The checklist file

Save it as `audits/<domain>/dim-positioning.json`, in the full audit's format:

```json
{"dimension": "positioning", "assessable": true, "confidence": "high|medium|low",
 "checks": [{"id": "P1", "points": 10, "max": 20, "evidence": "index.html H1 \"…\": the category is clear only from the subhead"}],
 "score": 60,
 "findings": [{"severity": "high", "check": "P5", "finding": "…", "evidence": "…", "fix": "…"}],
 "strengths": ["…"], "not_observable": ["…"],
 "source": "positioning deep dive, <date>; report: positioning.md"}
```

The checklist file holds positioning findings only: every `check` is P1–P5. An issue that belongs to another dimension (a banner contradiction, CTA wording) can appear in positioning.md, never in this file.

Severity follows the full audit: `high` for 0 on a check (every positioning check is worth 20), `medium` for partial, `low` for the rest.

**If `dim-positioning.json` already exists** (a full audit ran first): read it before scoring, then move the old file to `audits/<domain>/history/dim-positioning-<date>.json` before writing the new one. Never leave a copy named `dim-*.json` in the audit folder itself: the full audit reads every file with that name, and two positioning files would collide. Don't edit `MARKETING-HEALTH.md`, the one-pager or `score.json`: say how the total moves and that the full report changes when it's re-scored.
