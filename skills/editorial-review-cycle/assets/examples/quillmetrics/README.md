# Worked example: a Quillmetrics email with three reviewers

Quillmetrics is a fictional Shopify revenue analytics company. The files:
- `bfcm-email.md`: the draft
- `reviews/`: feedback from the editor (Mei Tanaka), legal (Lena Fischer) and the approver (Rafael Costa)
- `brand/`: brand memory, including the `## Approvals` list in `rules.md`
- `bfcm-email-v2.md`: the new version, with the agreed changes only
- `bfcm-email-review.md`: the packet and decision log

The reply to the user:

> **Approval state:** Not approved: waiting on Lena Fischer (legal) and Mei Tanaka (editor), then Rafael Costa (approver)
> **Next step:** send v2 to Lena for sign-off, and ask Mei to confirm hers.
>
> **Applied in v2:** 3: the real-time line now says "refreshed every 15 minutes", the "best Black Friday ever" line is out, and the "dashbaord" typo is fixed.
> **Needs a decision:** Nothing. Mei wanted to keep the "best Black Friday ever" line and Lena wanted it out; Rafael decides conflicts on email and chose removal.
> **Not applied:** "catch problems 3x faster": there's no result like that in brand memory.
> **Questions back:** Mei: what's the source for the 3x figure? Lena: your sign-off on v2.
>
> Files: bfcm-email-v2.md (new version), bfcm-email-review.md (packet and decision log).

## What to notice

| Moment | What happened | Why |
|---|---|---|
| Mei vs Lena on the "best Black Friday ever" line | Both positions logged; applied Rafael's call | The rules say Rafael decides conflicts on email, and he'd already decided. Had he not, v2 would have kept the line and listed it under "Needs a decision" |
| "real time" | Applied without escalation | A brand rule forbids promising real-time data, and the 15-minute refresh is confirmed in `offer.md` |
| "3x faster" | Not applied, source requested | An editor's suggestion is still a claim. No softer version ("much faster") was written in its place |
| Rafael's "fine once legal is happy" | Recorded as conditional | His sign-off counts only once Lena signs v2 |
| Mei's "approved with changes" | Not counted yet | Two of her changes weren't applied, so her condition isn't met |
