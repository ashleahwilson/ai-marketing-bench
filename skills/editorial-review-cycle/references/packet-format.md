# The review packet

`<name>-review.md` is written beside the draft for whoever owns the piece and whoever signs it off. Fixed sections, in this order. Section headings must stay exactly as shown.

```markdown
# Review: <title of the piece>

- Draft reviewed: <file the reviewers read>
- New version: <name>-v<n>.md
- Content type: <type> (approval rule from <brand/rules.md | approvals.md | none>)
- Reviewers: <name (role)>, …

## Approval state

<Approved | Not approved: waiting on <role (name)> | Not approved: open conflict | Unknown: no approval rule>
<one line: what has to happen next, and who does it>

## Needs a decision

1. <conflict or escalation> · <reviewer A (role)>: "<their words>" · <reviewer B (role)>: "<their words>" · <facts from brand memory> · Decides: <name, per rule> · v<n> carries: <which wording, until decided>

## Comments

| ID | Reviewer (role) | Where | Comment | Class |
|---|---|---|---|---|
| C1 | Dev Patel (subject expert), Hannah Ruiz (approver) | "$329/month" | Price is wrong; single location is $349 (merged C1, C5) | must fix |

## Decision log

| ID | Decision | Decided by | Why |
|---|---|---|---|
| C1 | Applied: "$349/month" | Hannah Ruiz (approver), uncontested | Matches brand/offer.md |

## Sign-offs

| Role | Required | Name | Status | Counts for v<n>? |
|---|---|---|---|---|
| editor | yes | Priya Shah | changes requested | no: needs to see v2 |

## Questions back to reviewers

- <name>: <the question, and what you need from them>
```

## Rules for each section

- **Approval state** is always the first section, and its first line is one of the four states. Never "approved" while any required sign-off is missing.
- **Needs a decision** lists open conflicts and anything only a named person can settle. Write "Nothing" if empty. A conflict the decider already settled goes in the decision log, not here.
- **Comments:** one row per comment, using the reviewer's words (shortened, never reworded into something they didn't say). Merged duplicates share a row and list every reviewer and the merged IDs. QA findings appear with reviewer "QA check". Your own editor pass, if any, goes in a separate table headed `### Editor pass (mine, not a reviewer's)`, IDs E1, E2….
- **Decision log:** one row for every comment ID, including merged ones (point them at the row they merged into). Decision is one of: Applied, Applied in part, Not applied, Open, Answered, Moot. **Decided by** is a person from the feedback or the approvals list and their role, "brand rule (<who set it>)", or "you" when the user decided in the conversation. Never blank, never "me", never a name that isn't in the feedback, the approvals list or brand memory. A QA blocker fixed by deleting a line is "QA check (blocker); owner to confirm". For an uncontested change, it's the reviewer who asked, marked "uncontested". Why is one line, citing the brand-memory file where it matters.
- **Sign-offs:** every required role from the approvals list, plus anyone else who gave a status. "Counts for v<n>?" says yes, no, or "yes, once <condition>".
- **Questions back to reviewers:** source requests for unsupported claims, permissions, product facts to confirm. Name who you need each answer from.

## The reply

The reply to the user is shorter than the packet and uses this shape:

```
**Approval state:** <the state line>
**Next step:** <who does what, in one line>

**Applied in v<n>:** <count>: <a short list, grouped>
**Needs a decision:** <each open item, who decides> (or "Nothing")
**Not applied:** <each, with the reason in a few words>
**Questions back:** <who needs to answer what> (only if any)

Files: <name>-v<n>.md (new version), <name>-review.md (packet and decision log).
```

- Under 250 words for a normal review. When the user is in a hurry, under 150, leading with the fastest path.
- Second person. No narration, no mention of how you checked anything.
