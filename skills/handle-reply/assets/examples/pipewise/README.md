# Worked example: Pipewise, three replies

Pipewise is a fictional pipeline-forecasting company. Its founder, Maya Chen, sent a cold email (`outreach/drafts-forecast.txt`) to sales leaders at software companies. Three replies came back on 2026-11-12 (`outreach/inbox-2026-11-12.txt`):

1. **Luis Ortega, Corbel Software:** interested, with three questions. Brand memory answers one (the Team plan price). It doesn't cover Pipedrive or Canadian data storage, so the reply holds those and they go to Maya under Needs you.
2. **Ruth Amsel, Halden Analytics:** a referral to Victor Lindqvist. Ruth gets a short thanks; Victor gets a first email that says only what Ruth said, with the full cold footer, and a flag that his address came from a reply rather than a published source.
3. **Greg Pollard, Talvo:** an opt-out. One-line confirmation, added to the suppression list.

The prompt was: "Three replies came in today to my forecast emails. They're in outreach/inbox-2026-11-12.txt. Handle them."

Files produced:
- `response.md`: the reply to the user
- `outreach/replies-2026-11-12.txt`: every block, drafts and holds
- `outreach/suppression.csv`: Greg added
- `outreach/reply-log.csv`: one row per person, plus Victor

Every company and person here is fictional, and no results are claimed for any real business.
