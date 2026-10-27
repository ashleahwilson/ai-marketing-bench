# Worked example: a Tallyhouse blog post that comes back Hold

Tallyhouse is a fictional restaurant bookkeeping firm. The files:
- `labour-post.md`: the post
- `brief-labour.md`: its brief
- `brand/`: the parts of brand memory the QA gate reads
- `labour-post-qa.md`: the report the QA gate wrote, which is also its reply

## Why Hold and not Fix first

The post is well built. It meets the brief, links the right CTA, and has a sensible title, description, headings and alt text. Two lines stop it:

| Line | Why it blocks | Fix |
|---|---|---|
| "The industry standard is that labour should be 25–30% of sales" | A third-party statistic with no source in the piece or in brand memory. It might be roughly right, but the QA gate doesn't confirm figures from memory | A source link from the author, or delete the line |
| "Join our free labour-planning webinar on October 28" | The post publishes on November 3, so the invitation will already have expired | Delete, or replace with the next date |

## What it didn't flag

- **The $18,000 / $60,000 example.** It's a worked hypothetical ("If you paid…"), not a claim about anyone, so it only gets a nit to make that clearer.
- **Voice.** The post follows the brand's voice rules (Canadian spelling, no never-use words), so there's nothing to report.
- **The bookkeeper's hospitality-finance background, the dashboard and the POS systems.** Each is confirmed in `brand/`.

Every line in the report points to a place in the post and gives a fix the author can apply without asking a follow-up question.
