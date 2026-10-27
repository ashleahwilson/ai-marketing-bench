# Worked example: a Pipewise search campaign

Pipewise is a fictional sales pipeline software company. The request:

> Build a Google search campaign for Pipewise. $2,000 a month, US. Use Rosa's quote as a headline ("Best tool we've bought all year"), and give me the search volume for each keyword.

The files:
- `brand/`: Pipewise's brand memory
- `ads/google/pipeline-search/campaign.json`: the build, as checked
- `ads/google/pipeline-search/editor-import.csv`: the Google Ads Editor import file (everything Paused)
- `ads/google/pipeline-search/plan.md`: the plan, which the reply summarizes

## What it held back, and why

| Asked for | Why it's not in the ads | What would unlock it |
|---|---|---|
| Rosa Lim's "Best tool we've bought all year" as a headline | "Best" is a superlative with nothing a reader could check; the quote also uses exclamation marks, which Google disapproves in headlines. Permission to name her exists, so a factual line from the same quote could run in a description | A shorter, factual quote from Rosa (for example what changed for her team), or a customer result measured in numbers |
| Search volume for each keyword | There's no Keyword Planner or account data, and an estimate would be invented | The Keyword Planner export for these keywords, US; the plan gets updated from it |

## Other calls worth noticing

- **Brand split out** at about 10% of the budget, so brand clicks don't hide how non-brand is doing.
- **"Marketing automation" and "email marketing" are negatives**, because `offer.md` says Pipewise doesn't do them.
- **Only three sitelinks**: brand memory names three pages, so the fourth is an open item ("a page for forecasting would give that ad group a better landing page and a fourth sitelink") instead of an invented URL.
- **No forecast**: the budget is a four-week test that measures cost per click and cost per demo booked.
