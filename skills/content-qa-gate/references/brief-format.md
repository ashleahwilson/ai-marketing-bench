# Brief format

content-qa-gate reads a brief written as a Markdown list of `- Field: value` lines. The content-brief skill writes this format, and a person can write it by hand in two minutes. Save it as `briefs/<slug>.md` or beside the piece as `brief-<slug>.md`.

```markdown
# Brief: How to read your prime cost

- Goal: get single-location owners to book a free month-end review
- Audience: owner-operators of single-location independent restaurants
- Channel: blog
- Key message: prime cost tells you whether last month worked, and you should see it before the month is over
- Must include: what prime cost is; the Lantern Noodle Bar quote; that your bookkeeper sends a monthly P&L
- CTA: "Book a free month-end review" → https://example.com/review
- Primary keyword: prime cost
- Length: 600–900 words
- Publish date: 2026-10-20
```

| Field | Used for |
|---|---|
| Goal, Audience, Key message | Brief fit (judgment) |
| Must include | Each item checked present and accurate (judgment) |
| CTA | The checker requires the URL to be linked; the wording is judged |
| Channel | Which checks run: search checks for blog, landing, web |
| Primary keyword | Title, H1 and first 100 words |
| Length | `<low>–<high> words` |
| Publish date | `YYYY-MM-DD`; dates in the piece before it are flagged |

Any field can be missing. The QA gate skips the checks that depend on it and says so.
