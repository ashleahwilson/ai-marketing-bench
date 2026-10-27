# Worked example: a Tallyhouse newsletter channel

Tallyhouse is a fictional restaurant bookkeeping company. Its `brand/voice.md` already exists and was reviewed with the team. No results are claimed.

## Input

The user said: "We never wrote rules for the client newsletter. Here are the last three issues and one of Dev's edits, in evidence/. Add the newsletter to our voice guide."

- `evidence/issue-august.md`, `issue-september.md` (approved by Hannah Ruiz), `issue-october.md` (approved by Dev Patel)
- `evidence/dev-edit.md`: one before-and-after edit by Dev
- `brand/`: the existing voice.md and changelog.md (before: see the brand-voice-gate fixtures; after: the files in this folder)

## What the skill noticed

- All three issues open with which month is closed and where the P&L is, run 39 to 47 words, and are signed with a first name. Three pieces, no counterexample: confirmed.
- Dev's edit removes "We're thrilled to share some exciting updates with our valued clients!". One piece: provisional.
- The October issue opens "September is closed!". The existing confirmed rule says no exclamation marks in email, and the other two issues have none. That's a ruling, not a change.
- "labour" in the August issue fits the Canadian spelling already on file. No new spelling rule needed.

## Output: the reply

**Recommendation:** Newsletter rules added to voice.md: two settled, three provisional. One ruling needed on exclamation marks before the newsletter section is final.

**Rulings needed:**
1. Exclamation marks in the newsletter. The October issue opens "September is closed!" (approved by Dev). Your email rule says no exclamation marks, and the August and September issues have none. Keep the email rule for the newsletter, allow one per issue, or treat October as a one-off?

**What's in voice.md:** a Newsletter section (under 60 words; signed with the sender's first name), a Do (open with which month is closed and where the P&L is), a Don't ("we're thrilled", "exciting updates"), "valued clients" on the never-use list, and one newsletter example from the September issue. Everything already in the file is unchanged.

**Thin or missing evidence:** the Don't, the never-use entry and the example rest on one piece each. Two more of Dev's or Hannah's edits to newsletter drafts would settle them.

## Output: the files

- `brand/voice.md`: the updated guide
- `brand/changelog.md`: one new line, newest first
