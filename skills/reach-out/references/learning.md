# Learning: the profile, feedback and results

This skill learns into **brand memory** (`brand/`) when the project has one: the senders go in `senders.md`, the voice in `voice.md`, standing rules in `rules.md` (under `## By skill` → `### reach-out`, or `## Everywhere` for org-wide rules), and results in `results.md`, with a source tag on every line. Use the brand-memory skill if it's installed.

Without `brand/`, it learns into `outreach-profile.md`, a single plain file the user can read and edit. Read whichever exists before every draft, and write to it whenever the user teaches you something.

## Contents
- First-run setup
- Turning feedback into rules
- Learning from results
- Building a voice from past emails

## First-run setup

If there's no profile, draft first, then offer to set one up. Ask three questions, all in one message:

1. Who sends these? (name, role, company, and the mailing address for the signature)
2. What do you sell, and to whom? (one line)
3. What's one result you can name? (customer, number, and whether they've agreed to be named)

Create the profile from [../assets/outreach-profile-template.md](../assets/outreach-profile-template.md) with the answers. Mark the voice `provisional` until it has been tuned. Never invent the sender's name, title or experience. Until the profile exists, use `[Your name]` and `[your role]`.

## Turning feedback into rules

When the user reacts to a draft, whether by commenting or by quietly editing it:

1. **Apply it now** to the draft in front of you.
2. **Generalise it.** Write a rule that would still hold for a different prospect next month. "Too salesy" might become `No "we help X do Y" lines. Let the proof make the claim.` Keep any condition the user gave ("for startups under 50 people").
3. **File it** where it applies. If there's no memory yet, create `outreach-profile.md` from the template now (or `brand/` if the brand-memory skill is available), fill in what you already know, leave the rest blank, and file the rule. Don't wait for setup.
   - **Everywhere:** `brand/rules.md` → `## Everywhere`, or the profile's `## Voice rules`
   - **One signal type:** `brand/rules.md` → `### reach-out`, or the profile's `## Signal rules`
   - **One sender:** that sender's entry in `brand/senders.md`, or the profile's `## Senders`
   - If it's unclear, ask: "Save that for all outreach, or just for [signal]?"
4. **Confirm in one line** what you saved, naming the file path and section (for example "Saved to `outreach-profile.md` under Voice rules").

For quiet edits, compare their version with yours and propose the differences that look like standing preferences. Don't save one-off wording.

If files can't be written in this environment, give the user the exact line to paste and where it goes.

## Learning from results

When the user shares outcomes (replies, meetings, unsubscribes), record them under `## Results` as one line per test:

```
2026-10-14 | cold, controllers after NetSuite move | subject "close after go-live" vs "month-end at 2x" | 4/40 vs 1/40 replies | keep A
```

Compare by persona, signal and subject line, not by single emails. Propose one change at a time, and only once there's enough volume to mean something. As a rough guide, under about 30 sends per variant is noise, so say so.

## Building a voice from past emails

When the user wants drafts to sound like them, use the best source available:
1. Sent emails that got replies, ideally 5 or more.
2. Emails they paste in.
3. Their website and LinkedIn posts, made more conversational.

Pull out the patterns: typical length, how they open, how they ask, how they sign off, words they use, and words they never use. Write these as voice rules, not as example emails to copy. Keep at most 3 approved examples per signal type, replacing the oldest. Note the source and date, and remove `provisional` once the user approves a draft written in the new voice.
