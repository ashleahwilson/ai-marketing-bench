# Judgment: deciding each piece

## Contents
- The five decisions
- The four questions, in order
- Competing pieces
- Outdated facts
- Pieces that serve no audience
- Metrics: what they can and can't decide
- When data is missing
- Blanket rules and other pushback
- Re-audits
- Evidence lines

## The five decisions

| Decision | Use when | Always include |
|---|---|---|
| **keep** | True, current enough, serves an audience, and the numbers (or its age, or its sales use) justify it | Why it stays, in numbers |
| **update** | Worth keeping, but something in it is wrong, retired, held, stale or thin | Exactly what to change: quote the line and give the replacement from brand memory, or say "remove this line" |
| **merge** | Competes with a stronger piece on the same topic or keyword. Its useful parts move into the target, then it redirects there | `target`: the stronger piece. What to carry over |
| **redirect** | No unique value, or about something retired, but a current page covers the same need. Send visitors and links there | `target`: the page that answers the same need |
| **remove** | No conversions, no sales use, no audience or no remaining purpose, nothing close to redirect to, and older than six months | Why nothing should replace it. "Return 410 or unpublish" is fine; the owner does it |

`needs data` is for a piece the inputs can't decide. Say which number would decide it ("conversions for this page", "traffic for both pieces to pick the one to keep").

## The four questions, in order

Ask them of every piece. The first "no" usually sets the decision.

1. **Is it true?** Every price, offer, claim, statistic and customer quote against `brand/`. Wrong or retired → `update`, or `redirect` when the whole piece is about the retired thing (an announcement of a discontinued product).
2. **Is it alone?** Another piece targeting the same keyword or answering the same question → `merge` the weaker into the stronger.
3. **Is it for someone the business serves?** Its reader against `audiences.md` and "We don't do" in `offer.md`. Written for an excluded audience → `remove` (or `redirect` if a served-audience page covers the same need). It doesn't matter how much traffic it gets: visitors the business can't serve aren't an asset.
4. **Do the numbers justify it?** Traffic, conversions, impressions, age, last update and notes. See "Metrics" below.

## Competing pieces

- **Same primary keyword, or near-identical titles:** competing. Merge the weaker into the stronger.
- **Stronger** means more conversions first, then more traffic, then more recently updated. Name both pieces and both sets of numbers in the evidence.
- **Both convert?** Still merge two blog posts that compete for the same keyword: the merge keeps the stronger post, carries over what converts in the weaker one, and the redirect keeps its visitors. Conversions protect a piece from removal, not from a merge.
- **Text overlap only** (two pieces share a lot of words but target different keywords): open both and judge. A comparison page and a how-to post can share vocabulary and do different jobs. Never fold a comparison, pricing or sales-use page into a blog post; keep both, or merge the post into the sales page.
- **No metrics:** you can still say two pieces compete and should become one. Say which to keep needs traffic data, or pick on content (the fuller, more current piece) and say that's what the pick rests on.
- A merge's target must survive the audit. Never merge into a piece that is itself being merged, redirected or removed.

## Outdated facts

Check every fact the script lists and read the posts for the ones it can't (claims without numbers, product names, quotes).

- **Prices:** compare the sentence, not just the number. A figure that matches only a `Price history` line is outdated. The same number can still be current for a different plan: say which line it matches and leave correct lines alone.
- **Discontinued offers:** a piece that sells or explains something under `Discontinued` in `offer.md`. If it's the whole piece → redirect to the nearest current page (pricing, the replacement, or the hub) or remove; if it's a mention → update.
- **Held or banned claims:** anything under "Needs substantiation" or "Restricted" in `claims.md`, or forbidden in `rules.md`. Update to remove the claim; don't soften it into a vaguer version.
- **Withdrawn proof:** a quote, customer or figure under `Withdrawn` in `proof.md`. Remove it; suggest a current item from `proof.md` only if one is recorded as usable.
- **Dated references:** "New for 2022", "coming in 2023", an event recap, last year's checklist. An announcement whose "coming soon" has passed is outdated even without brand memory.
- **Facts that contradict each other** across pieces (two different prices for the same plan) with no brand memory to settle it: flag both, ask which is current. Never pick one.

A fact brand memory doesn't mention isn't wrong because it's missing. List it as "not in brand memory: confirm" only if it's a price, statistic or customer claim.

## Pieces that serve no audience

Read the piece's reader from its title and body: who would search for this? Compare with every segment and persona in `audiences.md`, and with "Not for" / "We don't do". Flag it when its reader is excluded (an e-commerce guide for a restaurant bookkeeper, a 100-location franchise piece when the ceiling is 15) or matches no one listed (an Instagram guide for a scheduling product: "confirm who this is for"). Without brand memory, say what the piece's audience appears to be and ask; don't remove on that alone.

## Metrics: what they can and can't decide

- **Conversions protect.** Any conversion means the piece earns its place; the question becomes keep or update, not remove. Low-traffic pages that convert are often the most valuable on the site (integration pages, comparisons, pricing explainers).
- **Notes protect.** "Linked in sales emails", "used in onboarding", "sent to every lead" → keep, whatever the traffic.
- **Age protects.** Under six months since publishing (the default; the user can change it) is too new to judge on traffic.
- **Impressions without clicks** suggest a title or intent problem: update, don't remove.
- **Low traffic with zero conversions, older than six months, no notes:** a removal or redirect candidate. Then ask question 2: if a stronger piece covers the topic, merge or redirect instead of removing.
- **Conversions not supplied:** never remove on traffic alone. Mark low-traffic pieces `needs data` ("check conversions before removing"). Say this once in the reply.
- A sitemap `lastmod` is when the page last changed, not when it was published: never call a page "new" or "too new" from it.
- Any ranking you state ("your second-best page") must be computed from the export: sort it, don't eyeball it.
- Periods: compare pieces within the export's own period. Never annualize, extrapolate or compare with an industry benchmark.

## When data is missing

| Missing | Do | Don't |
|---|---|---|
| All metrics (posts only) | Decide from content: wrong facts, duplicates, dated announcements, excluded audiences. Everything else `needs data` | Remove or keep "because it probably gets traffic" |
| Conversions | Decide on traffic, but no removals on traffic alone | Treat clicks as conversions |
| Sitemap | Skip sitemap checks; say so | Guess which pages are live |
| Posts (export only) | Decide from titles and numbers; say facts inside the pieces weren't checked | Claim a page contains an outdated price you haven't read |
| Brand memory | Mark the audit provisional; check facts only against each other; gaps limited to the posts' own open questions; offer to set it up | Assume prices, audiences or claims |

A URL in the sitemap but not the export has no data: `needs data`, never removed. A URL in the export but not the sitemap may be orphaned: say so and ask whether it should be linked or redirected.

## Blanket rules and other pushback

- **"Delete everything under X":** run the rule, then show what it catches wrongly: pieces with conversions, with sales use in the notes, too new to judge, or with a stronger piece to merge into. Give the safe removal list as well, so the user can act today. One line on why, no lecture.
- **"Just delete them for me":** you don't delete or edit site files. Hand over the list and the exact action per URL (remove and return 410, or 301 to the target).
- **"Keep it as is" when it carries a wrong fact:** say no in the first line, quote the wrong line and the brand line, give the exact replacement, and confirm the piece itself stays (with its numbers).
- **"Add traffic estimates" or "how much traffic will we gain":** say you only use the numbers they supplied and won't estimate. Offer what would answer it (a before-and-after comparison in their analytics after the change).

## Re-audits

When `audits/content/inventory.prev.csv` exists after the copy in step 1:
- For each earlier `update`, `merge`, `redirect` or `remove`, check whether it happened: the URL still in the export or sitemap, or `last_updated` unchanged, means it's still open. List those first under "Since the last audit".
- Name new pieces since the last audit, and decisions that change because brand memory changed (a price change, a discontinued offer).
- Compare metrics only for the same URL across the two files, and say both periods.

## Evidence lines

Quote, don't paraphrase. Good:
- `1800 sessions; 22 conversions; "A single location is $299/month" vs offer.md: "Single location: $349/month, effective 2026-10-01"`
- `45 sessions but 7 conversions; published 2026-05-04`
- `same primary keyword "prime cost" as /blog/prime-cost-guide (2400 sessions, 18 conversions vs 310 and 0)`

Bad: "low engagement", "underperforming", "probably outdated", "high potential".
