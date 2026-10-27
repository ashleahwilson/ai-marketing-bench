# The route file and the reply

`<name>-route.md` is written beside the piece, where `<name>` is the piece's file name without its extension (`bfcm-landing-v2.md` gives `bfcm-landing-v2-route.md`). It's for whoever owns the piece and every approver on it, so it uses names, dates and the content's own words. Fixed sections, in this order, with these exact headings.

```markdown
# Approval route: <title of the piece>

- Content: <file> (<version or "version not stated">) · <type> · <channel> · <audience or region, if given>
- Requested by: <name>, <request date, or "date not given">
- Go-live: <date, or "not given">
- Approval rule: <brand/rules.md (<type> line) | approvals.md | none> <add "provisional: no brand memory" when there's none>

## Status

<Approved | Not approved: waiting on <role (name)>, … | Not approved: blocked by <reason> | Unknown: no approval rule>
<one line: what happens next and who does it>
<one line on timing: last step due <date>; fits / doesn't fit go-live on <date>. Leave this line out when the status is Approved>

## Triggers found

| Trigger | Where (quote) | Adds | Why |
|---|---|---|---|
| Performance claim | "spend 40% less time on month-end" | legal (Marcus Lee) | No substantiation on file in claims.md |

<or "None beyond the content type's own sign-offs." Judgment calls are marked "(judgment call)".>

## Route

| Step | Who (role) | Checks | Due | Sign-off |
|---|---|---|---|---|
| 1 | Priya Shah (editor) | Blog post sign-off | 2026-10-27 | approved (v1), counts |
| 2 | Marcus Lee (legal) | Substantiation for "40% less time" | 2026-10-29 | none yet |
| — | Customer consent: Maria Okafor (Lantern Noodle Bar) | Written OK to be named | before approver | not on record |

## Blockers and open questions

1. <blocker or question> · <who can resolve it> · <fastest fix>

<or "None.">
```

## Rules for each section

- **Status** is the first section and its first line is exactly one of the four states. "Approved" only when every step's sign-off counts for this version, consent is on record wherever it's needed, and there are no blockers. "Blocked" wins over "waiting" when both apply. With "waiting", name the people in the earliest step still open.
- **Triggers found:** one row per trigger, with the content's exact words (shortened is fine). "Adds" names the person from the matrix, or `TBD: who checks this?` when the matrix has no line for it. "Why" is one line.
- **Route:** one row per person per step, in order. People who review at the same time share a step number. Checks come from the matrix (the type line and any trigger lines), merged when one person covers several. Due dates are calendar dates (`YYYY-MM-DD`), or "not set" when the matrix has no response time. Sign-off says what was given, for which version, and whether it counts: "approved (v1), doesn't count for v2", "approved, doesn't count: requester's own work". Consent rows use "—" as the step.
- **Blockers and open questions:** numbered. Each names who can resolve it and the fastest fix. Questions come here too: the content type when it's unclear, who signs when a role is `TBD`, who checks a trigger the matrix doesn't cover.
- Never write who ran a check or how. No tool names, scripts, file internals, or the names of any helper. This file goes to approvers.

## The reply

Shorter than the file. This shape:

```
**Status:** <the state line>
**Next step:** <who does what, by when>

<Up to 5 lines: the blockers and triggers that matter, each with its fix.>

<Questions, numbered, only if there are any.>

The full route is in <name>-route.md.
```

- Under 100 words when the piece is Approved; under 200 when the user is in a hurry; under 300 otherwise.
- Every line agrees with the status: don't write "no blockers" and then list something that stops the piece.
- Second person. No checklist, no internals, no lecture. A declined request gets one line of reason and the fastest path.
- **Guided mode:** no file. Reply with the triggers found, the draft route as you'd build it, and the decisions as numbered questions. Write the file when they answer.
