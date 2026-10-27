# Campaign spec and Editor CSV

## Contents
- The spec file: campaign.json
- Field notes
- The Editor import file
- The audit fixes list (input)

## The spec file: campaign.json

Write one spec per build at `ads/google/<campaign-slug>/campaign.json`. The checker reads it, checks it, and writes `editor-import.csv` beside it.

```json
{
  "brand_name": "Tallyhouse",
  "domain": "tallyhouse.example",
  "currency": "CAD",
  "monthly_budget": 3000,
  "spelling": "Canadian",
  "keyword_data": null,
  "competitors": ["Platewise"],
  "user_facts": ["$3,000 a month", "Canada only"],
  "conversion_actions": [{"name": "Review booked", "primary": true}],
  "shared_negatives": [
    {"name": "Non-brand negatives", "campaigns": ["non-brand"],
     "keywords": [{"text": "jobs", "match": "phrase"}]}
  ],
  "campaigns": [
    {
      "name": "Search | Brand",
      "type": "brand",
      "daily_budget": 10,
      "networks": ["Google search"],
      "locations": ["Canada"],
      "location_option": "presence",
      "languages": ["English"],
      "bid_strategy": "Maximize clicks",
      "negatives": [],
      "ad_groups": [
        {
          "name": "Brand",
          "landing_page": "https://tallyhouse.example/",
          "keywords": [{"text": "tallyhouse", "match": "exact", "volume": null, "cpc_low": null, "cpc_high": null}],
          "ads": [
            {
              "headlines": [{"text": "Tallyhouse Bookkeeping", "pin": null}],
              "descriptions": [{"text": "Bookkeeping for restaurants, with a P&L every month.", "pin": null}],
              "path1": "review",
              "path2": ""
            }
          ]
        }
      ]
    }
  ],
  "assets": {
    "sitelinks": [{"text": "Pricing", "desc1": "", "desc2": "", "url": "https://tallyhouse.example/pricing"}],
    "callouts": ["Named bookkeeper"],
    "snippets": [{"header": "Service catalog", "values": ["Monthly P&L", "Sales tax filings", "Catch-up books"]}]
  }
}
```

## Field notes

- `type`: `brand`, `non-brand` or `competitor`. Competitor keywords outside a `competitor` campaign are flagged.
- `user_facts`: the user's own words for any fact they gave in the conversation that ad text uses (a price, a trial length). Numbers in ad text must match brand memory or one of these. Quote the user; don't paraphrase a number.
- `competitors`: every competitor the user or brand memory names. Their names are blocked in ad text.
- `keyword_data`: the path to a Keyword Planner export, or `null`. Leave `volume`, `cpc_low` and `cpc_high` as `null` unless the file gives them; they must match the file exactly.
- `shared_negatives[].campaigns`: campaign names, or `["non-brand"]` for every non-brand campaign, or `["all"]`.
- `spelling`: `US`, `Canadian` or `UK`. Defaults to what `voice.md` says. Without brand memory, use the market's convention (US for a US-only campaign) or the user's own spelling.
- `pin`: `null`, or 1–3 for headlines, 1–2 for descriptions.

## The Editor import file

`editor-import.csv` has one row per item, and Google Ads Editor (Account > Import > From file) maps the columns:

| Row | Columns |
|---|---|
| Campaign | Campaign, Campaign Type, Networks, Budget, Budget type, Bid Strategy Type, Languages, Campaign Status |
| Location | Campaign, Location, Targeting method |
| Campaign negative | Campaign, Keyword, Criterion Type (Campaign Negative Phrase / Exact / Broad) |
| Ad group | Campaign, Ad Group, Ad Group Status |
| Keyword | Campaign, Ad Group, Keyword, Criterion Type (Exact / Phrase / Broad), Final URL |
| RSA | Campaign, Ad Group, Ad type, Headline 1–15, Headline n position, Description 1–4, Description n position, Path 1, Path 2, Final URL, Status |
| Shared negative list | Shared set, Keyword, Criterion Type (Negative Phrase / Exact / Broad) |
| Sitelink | Campaign, Link Text, Description Line 1, Description Line 2, Final URL |
| Callout | Callout text |
| Structured snippet | Header, Snippet Values (separated by semicolons) |

Everything is Paused. Tell the user to check Editor's import preview before posting changes, since column names can differ slightly between Editor versions, and to link the shared negative list to the listed campaigns if the import doesn't.

## The audit fixes list (input)

Written by a Google Ads audit at `audits/google-ads/<account>/fixes.md`:

```
# Fixes: <account>
Source: AUDIT.md (<YYYY-MM-DD>) · Date range: <start> to <end> · Confidence: High|Medium|Low

1. [P1] settings · <problem with evidence> · <fix with exact value>
...

## Account facts
- <budget per campaign, geo and presence setting, networks, bid strategy, conversion actions, brand terms>
```

Areas: structure, keywords, negatives, ads, assets, settings, budget, tracking, landing. P1 = within 48 hours, P2 = 2 weeks, P3 = 3 months. A fix ending `(confirm first)` waits for the user. Unknowns are written `TBD: <what's missing>`.
