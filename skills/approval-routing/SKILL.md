---
name: approval-routing
description: Works out who has to approve a piece of marketing before it goes out, in what order and by when, and tracks where it stands. Reads the content and its details (type, channel, audience, region, spend, requester, go-live) and finds what needs extra review, such as performance or comparative claims, prices and offers, a named customer or testimonial, health, financial or employment topics, spend over a threshold, or a brand change. Applies the approval list in brand memory and returns the route (approvers, what each checks, order, due dates) and the status from the sign-offs on record. Never calls a piece approved while a sign-off, customer consent or brand-rule fix is missing, and never counts the requester's sign-off on their own work when the rules forbid it. Use when the user asks who needs to sign off, whether something can go out, or where approvals stand, for example "route this for approval", "can this go live Thursday", "just ship it". Not for consolidating reviewer comments or editing the piece.
license: MIT
compatibility: Recommended for large models. On small models it can occasionally mislabel a line as a confirmed feature or route on the default rule, so check the trigger table. See evals/scorecard.json.
metadata:
  version: "1.2.1"
  author: "Ashleah Wilson"
---

# Approval routing

The step between "it's written" and "it's live". It doesn't judge the writing. It decides who has to see the piece, what each person is checking for, the order they see it in and when each is due, and whether the piece can go out today.

## Ground rules

1. **Never call it approved without every required sign-off.** Not when the user is in a hurry, not with "I'll get approval later", not when the approver is the one asking. Say who's missing and give the fastest honest route.
2. **The requester doesn't approve their own work** when the approval list says so, or says nothing. Their sign-off doesn't count. Use the role's backup if there is one; if not, ask who signs instead.
3. **Staff sign-offs never stand in for a customer's consent.** A named customer or quote needs `named: yes` in `brand/proof.md`. No record, no consent.
4. **A brand rule outranks any approver.** A phrase the rules ban has to change; no sign-off clears it.
5. **Missing stays missing.** Every name on the route comes from the approval list or the user. Every date comes from the list's response times. No invented approvers, backups, consent records, budgets or due dates. If something's unknown, it's `TBD` with a question.
6. **Don't over-route.** A confirmed product feature, general advice or the audience description isn't a trigger. Extra reviewers cost a week.
7. **Never overwrite.** The piece, the reviews, `brand/` and earlier route files stay as they are. A new version gets its own route file.
8. **Don't lecture.** One line of reason for anything you won't do, then the fastest way forward.
9. **Never soften a claim as the fix.** Not a performance figure, not "HIPAA-compliant", not a superlative. The fix is: cut it, or get it substantiated and checked by the person the list names.
10. **Speak only about the piece.** Never name this method, its mode, its files or any helper, even if your environment asks you to announce what you use. Never mention the system date or absolute file paths: give file names relative to the project folder.

## Pick the mode

| The user wants… | Mode |
|---|---|
| A route for a piece: "who needs to approve this", "route this" (the default) | **Draft:** everything below; write `<name>-route.md` |
| To decide first: "walk me through it", "before you write anything", "don't create it yet" | **Guided:** steps 1–4, then reply with the triggers, the draft route and numbered questions. No file until they answer |
| Where it stands: "is it signed off", "can it go out Thursday", "everyone approved it, right?" | **Status:** the full route (a change since sign-off can add reviewers), led by the status; write `<name>-route.md` |

## Workflow

```
- [ ] 1. Load: the piece, its details, brand/ (rules.md Approvals, proof.md, offer.md, claims.md), reviews, earlier route files
- [ ] 2. Run scripts/route.py route
- [ ] 3. Judge every trigger candidate and read for ones it missed (references/triggers.md)
- [ ] 4. Build the route and the status (references/approvals-format.md)
- [ ] 5. Write <name>-route.md (references/route-format.md)
- [ ] 6. Run scripts/route.py check, fix every FAIL, self-check, reply
```

### 1. Load

List the project folder first. Read:
- **The piece** and its details: content type, channel, audience, region, spend, requester, request date (if it isn't given, write "not given" in the file, and count due dates from today, saying so; never present today as the request date), go-live. Take them from the user, the file (`Version:`, `Author:`, `Budget:` lines) or the piece's form. If the list has no line for the type, say so in those words ("there's no `guide` line in your approval list") and ask which line applies (in Draft mode, route on `default` and put the question first).
- **`brand/rules.md`**: the `## Approvals` list and the `## Everywhere` rules. Or an `approvals.md` the user supplies. The format, including the routing fields (`order:`, `sla:`, `self-approval:`, `trigger:` lines), is in [references/approvals-format.md](references/approvals-format.md). It's shared with the editorial review loop: read and write it exactly.
- **`brand/proof.md`** (consent), **`offer.md`** (prices and offers on record), **`claims.md`** (substantiated claims).
- **Sign-offs:** reviewer files the user names, or `reviews/` or `.review/` beside the piece. Sign-offs reported in chat ("Hannah's fine with it") get saved as `.review/<name>-<role>.md` in their words, with the version they saw.
- **Earlier route files** (`*-route.md`) and any review packet (`<name>-review.md`): they show what was routed and signed before.

**No brand memory or no approval list?** Run everything else. The status is "Unknown: no approval rule", the file is marked provisional, and the useful output is the trigger list plus numbered questions: who signs off on this type, and who checks each trigger. Keep the piece's own spelling and conventions in anything you quote. Offer to record the answers as approval lines.

### 2. Run the router

```bash
python3 scripts/route.py route <piece> --brand brand/ --type "<type>" --requester "<name>" --requested <YYYY-MM-DD> [--go-live <YYYY-MM-DD>] [--spend <amount>] [--reviews reviews/] [--approvals approvals.md] [--brand-change]
```

It picks the approval line, lists trigger candidates with the line they're on, finds banned phrases and named customers, checks consent records, applies triggers, self-approval and backups, works out due dates in business days, checks which sign-offs count for this version, and gives the status and whether the route fits go-live. Its candidates are a starting point: it can't tell a feature from a claim, and it misses claims without numbers.

### 3. Judge

Work through [references/triggers.md](references/triggers.md) for every candidate: keep it, drop it (a feature, the audience line), or mark it a judgment call. Then read the piece again for triggers the patterns miss: a claim without a number, an implied comparison, a customer's logo, a guarantee.

### 4. Build the route

Follow "How a route is built" in the format file. If you kept a trigger the router dropped, or dropped one it kept, recompute the affected steps and dates by hand with the same rule. Then the status:

| Status | When |
|---|---|
| **Approved** | Every required sign-off counts for this version, consent is on record wherever needed, no blockers |
| **Not approved: waiting on …** | Sign-offs still due; name the earliest open step |
| **Not approved: blocked by …** | A brand-rule breach, missing consent, no eligible signer, or a claim the user wants to run unsubstantiated |
| **Unknown: no approval rule** | No approval list for this business |

### 5. Write

`<name>-route.md` beside the piece, in the exact shape in [references/route-format.md](references/route-format.md). Status first.

### 6. Check and reply

```bash
python3 scripts/route.py check <name>-route.md <piece> --reply <your reply file> (same options as step 2)
```

It fails an "Approved" the sign-offs don't support, a required approver missing from the route, the requester's own sign-off counted, an unreported banned phrase or missing consent, a missing section, and any mention of how the route was made. Fix a FAIL by changing the file.

Then answer each line for yourself. A "no" means fix it before replying. Don't put the checklist in the reply.

```
- [ ] Every name on the route is from the approval list or the user; every TBD has a question
- [ ] Every trigger quotes the piece; nothing was added for a feature or the audience line
- [ ] No sign-off counted that is for another version, from the requester, or from someone not on the route
- [ ] Consent is on record for every named customer, or it's a blocker
- [ ] Due dates follow the response times; the go-live fit and the spare days are exactly as the router gives them
- [ ] The status matches all of the above
- [ ] The original files and earlier route files are unchanged
- [ ] The reply and the file never mention how anything was checked
```

Reply in the shape at the end of the route-format file: status first, then the next step and who takes it.

## When the user asks for something this won't do

- **"Just ship it, I'll get approval later" / "mark it approved":** one line on what's missing, then the fastest path. Usually: cut the claim or phrase that adds a reviewer or breaks a rule, and send it to the remaining approvers now, with the due dates. Write the file with the true status. Under 200 words.
- **"I'm the approver, I'll sign it myself":** say their sign-off can't count on their own piece, name the backup if the line has one, otherwise ask who signs instead.
- **"They all signed off, so it's good to go":** check the version and the consent before agreeing. If it's genuinely approved, the reply is the status, who signed which version, and the file name: under 100 words. No judgment calls you decided not to flag, no due dates, no type question unless the type genuinely changes who signs.
- **Rewriting the piece:** don't. Say which words have to change and why; offer new copy only if asked.

## Hand-off

`<name>-route.md` is the tracking record for the owner and every approver. The editorial review loop reads the same approval list and reviewer files, and its `<name>-review.md` packet holds the comments; a later status check reads both. Approval lines you add for the user go in `brand/rules.md`, in the shared format.

## Keep tools out of the deliverable

Never name this skill, other skills, or their scripts and checks in a reply, report, draft or file the user may pass on: these often go to clients or the public. Describe what was checked, not the tool that checked it. If your environment asks you to say which skill you used, put that in one short line to the user, separate from the deliverable, never inside it.

## What good looks like

Each approver can see why they're on the route, what to look for and when it's due. The owner sees one status line and knows whether it's on them. Nothing on the route is there because it was guessed, and nothing was called approved that wasn't.

A worked example (a Pipewise webinar email with a named customer and a requester who is also the approver) is in [assets/examples/pipewise/](assets/examples/pipewise/README.md).
