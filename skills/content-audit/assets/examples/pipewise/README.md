# Worked example: Pipewise blog audit

Pipewise (fictional) sells pipeline forecasting to B2B sales teams of 10 to 100 reps. The user asked:

> Can you audit our blog? Export is in data/blog-export.csv and two of the posts are in posts/. Tell me what to keep and what to cut.

**Inputs**
- `data/blog-export.csv`: 8 pages, with "Demo requests" as the conversion column and no stated period
- `posts/`: two of the eight posts
- `brand/`: offer (with a price history), audiences (with a "Not for" line), proof, voice

**What the audit found**
- The pricing post quotes $39 per rep, a price that ended on 2026-06-30. It's the third-best page for demo requests, so it's action 1.
- Two posts target "sales forecasting": the weaker one merges into the guide.
- The HubSpot integration page has 30 sessions but 4 demo requests, so it stays despite low traffic.
- A post for solo founders serves an audience brand memory excludes, and a 2024 event recap gets 9 sessions: both are removed.

**Outputs**
- [audits/content/AUDIT.md](audits/content/AUDIT.md): the full audit
- [audits/content/inventory.csv](audits/content/inventory.csv): every page with its decision

**The reply the user received**

> **Recommendation:** Fix the old price on your pricing post first: it quotes $39 per rep, which ended in June, and it's your third-best page for demo requests. Then merge one pair, refresh one guide and remove two pages. Three pages stay.
>
> **Top actions**
> 1. Update /blog/pipewise-pricing · "$39 per rep per month" → "$45 USD per rep per month, billed annually; Canadian customers $61 CAD" (640 sessions, 9 demo requests)
> 2. Merge /blog/what-is-sales-forecasting into /blog/sales-forecasting-guide · same keyword; 260 sessions and 0 demo requests against 1900 and 14
> 3. Update /blog/pipeline-coverage-ratio · converts, but untouched since 2024-11-05
> 4. Remove /blog/solo-founder-crm-tips · written for solo founders, an audience you've said you don't serve
> 5. Remove /blog/saastr-2024-recap · 9 sessions, 0 demo requests
>
> **Decisions:** keep 3 · update 2 · merge 1 · remove 2
> **Topic gaps:** explaining a missed forecast to the board; what happens in the forecast walkthrough; forecasting from Salesforce data
> **Not supplied:** a sitemap, and six of the eight posts, so facts inside those six weren't checked.
>
> Files: audits/content/AUDIT.md, audits/content/inventory.csv.
