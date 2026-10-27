---
name: brand-memory
description: Sets up and maintains a brand memory, a brand/ folder of small plain-text files (offer, audiences, positioning, proof, voice, claims, competitors, senders, rules) where every fact carries a source and a status, so every other skill writes from the same truth. Use when the user wants to set up, update, migrate, audit or share their brand context, for example "set up our brand memory from our website", "we changed our pricing", "never call us X again", "move our outreach profile into brand memory", "is our brand memory up to date", "give the new freelancer a brand brief", or when another skill needs brand context that doesn't exist yet. Not for writing campaign copy itself, and never a place to store passwords or API keys.
license: MIT
metadata:
  version: "1.2.1"
  author: "Ashleah Wilson"
---

# Brand memory

One folder, `brand/`, holds what's true about the business. Every other skill reads it instead of asking again. Its value depends on two things: **every fact can be traced to a source**, and **nothing is invented to fill a gap**.

## Ground rules

1. **Every fact carries a source tag**: `[source: <where>, <date> · confirmed | provisional | assumed]`. Unknowns are written as `TBD: <what's missing>`. Never fill a gap with a plausible guess. See [references/schema.md](references/schema.md).
2. **Never invent proof.** No made-up statistics, customers, testimonials, logos or awards, even when the user asks for "something impressive". Offer a fast way to get real proof instead (see "Asked for proof that doesn't exist" below).
3. **Never store credentials.** No API keys, passwords, tokens or login links. Brand memory is plain files that get committed, shared and pasted into agents. If the user offers one, don't write it and don't repeat it back. Point them to a password manager, the tool's own connection settings, or environment variables, and offer to record the non-secret part (for example "Email platform: Mailchimp").
4. **Keep history.** Old prices and superseded proof move to a history section. Every change gets a line in `changelog.md`.
5. **Ask before deleting anything** the user created. For a secret found in an audit, offer to remove it now, and do it on a yes.
6. **No template leftovers.** Replace every `YYYY-MM-DD` and `<placeholder>` with a real value or `TBD: <what's missing>`. Keep the file table in `BRAND.md` matching the files that exist. Don't fill fields such as the opt-out line or the voice from template defaults: they're the user's, so they stay `TBD` until the user gives them.
7. **Do what was asked.** Don't create a whole `brand/` folder the user didn't request (for example, when they asked a question or made a request you're declining). Offer it instead.

## What do you need?

| The user wants to… | Do this |
|---|---|
| Set it up from a website or documents | Follow [references/setup.md](references/setup.md), "From a website or documents" |
| Set it up with no material | Create the skeleton from [assets/template/brand/](assets/template/brand/), then ask the interview questions in [references/setup.md](references/setup.md) |
| Move an `outreach-profile.md` (or other profile) over | Follow [references/setup.md](references/setup.md), "Migrating an existing profile" |
| Record a change, or a rule from feedback | Follow [references/maintenance.md](references/maintenance.md), "Updates" and "Feedback from other skills" |
| Check it before sharing, or because it feels stale | Run the checker, then follow [references/maintenance.md](references/maintenance.md), "Audit" |
| Send something to a freelancer, agency or new hire | Follow [references/maintenance.md](references/maintenance.md), "Sharing" |

If there's no `brand/` folder and the request needs one, set up first. Default to setting up from the website if a URL or pages are available, and from the interview otherwise.

## Workflow

```
- [ ] 1. Read what exists: brand/, any outreach-profile.md, and files the user points to
- [ ] 2. Do the task, using the reference file for it
- [ ] 3. Tag every new or changed fact; write TBD for anything unknown
- [ ] 4. Check for conflicts this change creates elsewhere in brand/
- [ ] 5. Update BRAND.md if the summary changed; add a changelog line
- [ ] 6. Run: python3 scripts/check_brand.py brand/
- [ ] 7. Report back briefly
```

**Step 6.** The checker exits with FAIL if there's a secret or no `BRAND.md`. Fix every FAIL before reporting. WARNs are the audit list: staleness, missing sources, placeholders, unconfirmed permission to name a customer, conflicting numbers.

**Step 7. The report:**
- **Setup:** what's complete, what's provisional, and the three gaps that matter most, each as a question.
- **Update:** one or two lines on what changed, in which files, and any conflicts found (or "no conflicts found").
- **Audit:** problems in priority order: secrets, contradictions, naming permission, staleness, missing sources, gaps. Recommend fixing the first three before the memory is shared.

Keep the report about the business, not the mechanics. Mention file names only where the user needs to act. Never mention the checker, its counts or the source-tag statuses to the user. Translate them ("two facts still need a source", "the Lantern quote needs the customer's OK").

## Asked for proof that doesn't exist

Decline briefly. Invented proof gets repeated by every skill that reads this folder, it breaks advertising rules, and it costs trust the first time a prospect checks. Then help them get real proof fast:
- **Three questions** that surface real results: their best customer, what changed for them, and whether the change was measured.
- **A two-line request** they can send that customer.
- **Honest proof to use in the meantime,** labelled as not a customer result: how the product works, the founder's track record, the number of years doing this work, a public review score. Each is tagged as what it is.

## Keep tools out of the deliverable

Never name this skill, other skills, or their scripts and checks in a reply, report, draft or file the user may pass on: these often go to clients or the public. Describe what was checked, not the tool that checked it. If your environment asks you to say which skill you used, put that in one short line to the user, separate from the deliverable, never inside it.

## What good looks like

A new team member, or another skill, can read `BRAND.md` in two minutes and write something on-brand and true. Every number in any draft traces back to a tagged line in this folder. Gaps are visible as `TBD`s with a question attached, not hidden behind confident filler.
