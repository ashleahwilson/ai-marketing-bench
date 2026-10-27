# Output formats

## Contents
- inventory.csv
- AUDIT.md
- Guided mode questions
- Check mode reply

## inventory.csv

One row per piece: every URL in the export, the posts folder and the sitemap. Columns, in this order (metric columns only for metrics the export supplied):

| Column | Content |
|---|---|
| url | The path, e.g. `/blog/prime-cost-guide` |
| title | From the export or the post. Blank if neither has one: never made up |
| published, last_updated | As supplied (export, post front matter, or sitemap lastmod) |
| sessions / clicks / pageviews / users, conversions, impressions | Copied exactly from the export. Blank if not supplied |
| word_count, primary_keyword | As supplied, or counted from the post |
| flags | Short signals: stale, thin, low traffic, converts, old figure, retired, held, pair, no data |
| audience | The segment or persona it serves (`Owner-operator`), `none: <excluded or unlisted audience>`, or `unknown` without brand memory |
| decision | keep, update, merge, redirect, remove, needs data |
| target | For merge and redirect: the URL that survives |
| reason | One line, plain language |
| evidence | The numbers and quoted lines the decision rests on |
| priority | 1–10 for the top actions, blank otherwise |

This file is what the person running the site works from. Content-brief work can read the gaps from AUDIT.md.

## AUDIT.md

```markdown
# Content audit: <site or brand>

Date: <YYYY-MM-DD> · Data: <export name and period, metrics supplied> · Posts read: <N or "not supplied"> · Sitemap: <N URLs or "not supplied"> · Brand memory: <as of date, or "none: provisional">

**Recommendation:** <one or two sentences: the first thing to do and the shape of the rest>

## Top actions
1. **<Decision>** <URL> · <the problem, with numbers or the quoted line> · <the exact action>
(at most 10, in priority order)

## Decisions
| Decision | Count | Pieces |
|---|---|---|
| Keep | N | /a, /b |
| Update | N | … |
| Merge | N | /x → /y |
| Redirect | N | /x → /y |
| Remove | N | … |
| Needs data | N | … |

## Wrong or outdated facts
- <URL> · "<quoted line from the piece>" · brand memory: "<quoted line>" (<file>) · <replacement or "remove the line">

## Competing pieces
- <stronger URL> (<numbers>) and <weaker URL> (<numbers>) · <same keyword / same question> · merge the weaker into the stronger; carry over <what>

## Pieces that serve no audience
- <URL> · written for <reader> · brand memory: "<Not for line>" · <decision>

## Low traffic, kept on purpose
- <URL> · <numbers> · <conversions, sales use, or too new>
(only when the user asked about pruning, or a page under the traffic threshold stays)

## Topic gaps
- <topic> · serves: "<persona, pain, trigger or offer line>" (<file>) · nearest existing piece: <URL or none>
(for the next briefs; no search volumes)

## Since the last audit
(re-audits only: earlier actions still open, new pieces, decisions changed by brand-memory changes)

## Needs data
- <URL> · <what would decide it>

## How this was done
- Inputs used and what was missing, in one or two lines each
- Thresholds: low traffic under <N> <metric> in the export period; stale after <N> months; too new under <N> months; thin under <N> words
- What wasn't checked (facts inside pieces when no posts were supplied; anything without brand memory)
```

Leave out a section with nothing in it, except Recommendation, Top actions, Decisions, Topic gaps and How this was done. In a client file, no internal vocabulary: no script names, flag codes in capitals, "the checker", or skill names.

## Guided mode questions

Before any final file, reply with:

```
**Recommendation (so far):** <one line>

**Fixing regardless** (wrong or retired facts; not optional)
- <URL> · <quoted line> → <brand line>

**Your calls** (my recommendation in brackets)
1. Merge <weaker> into <stronger>? <sessions and conversions for both> [merge]
2. Remove <URL>? <sessions, conversions, audience> [remove] or redirect to <URL>?
(every question, redirects included, carries sessions or clicks and conversions for each piece it names)
3. <needs data item>: <what would decide it>

Reply with the numbers you agree with, or changes. I'll then write the full audit and inventory.
```

Save only `audits/content/inventory-draft.csv`. Write `inventory.csv` and `AUDIT.md` after the answers.

## Check mode reply

```
**<Keep | Update | Merge | Redirect | Remove>:** <one-line reason with the numbers>

<The exact change: "Change 'A single location is $299/month' to 'A single location is $349/month'." Lines that are already correct stay.>

<One line on anything else in the piece that needs a decision, or nothing.>
```

Under 200 words.
