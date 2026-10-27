# Approvals and feedback formats (shared)

> This format is shared with the editorial review cycle in this library. The first two parts below are copied unchanged from that skill's `references/approvals-format.md` so both read and write the same files. Approval routing adds optional fields and `trigger:` lines, described under "Routing extensions". They are backward-compatible: a reader that only knows the shared format ignores them and still gets the same sign-off list.

## Contents
- The approvals list (shared)
- Reviewer feedback files (shared)
- Routing extensions (optional fields, trigger lines, how a route is built)
- Customer consent records
- Checklist when adding lines for a user

Two plain-text formats: the approvals list (who must sign off on what) and the reviewer feedback file. Both can be written by hand in a minute, and any skill can read them.

## The approvals list (shared)

It lives in `brand/rules.md` under its own `## Approvals` heading, or in a standalone `approvals.md` the user supplies (same lines, heading optional). One line per content type:

```markdown
## Approvals

- type: blog post | sign-off: editor=Priya Shah, approver=Hannah Ruiz | conflicts: Hannah Ruiz [source: Hannah Ruiz, 2026-10-12 · confirmed]
- type: newsletter | sign-off: editor=Priya Shah, approver=Hannah Ruiz | backup: approver=Dev Patel | conflicts: Hannah Ruiz [source: Hannah Ruiz, 2026-10-12 · confirmed]
- type: case study | sign-off: editor=Priya Shah, legal=Marcus Lee, approver=Hannah Ruiz | conflicts: legal=Marcus Lee on claims, customer permissions and compliance; Hannah Ruiz on everything else [source: Hannah Ruiz, 2026-10-12 · confirmed]
- type: default | sign-off: approver=Hannah Ruiz | conflicts: Hannah Ruiz [source: Hannah Ruiz, 2026-10-12 · confirmed]
```

| Field | Required | Meaning |
|---|---|---|
| `type:` | yes | The content type, lower case (`blog post`, `landing page`, `email`, `case study`). `default` applies when no type matches |
| `sign-off:` | yes | Comma-separated `role=Name`. Every one must sign off before the piece is approved. A name can be `TBD` |
| `backup:` | no | `role=Name`: who may sign for that role when the named person is away. A backup's sign-off counts only when it's given |
| `conflicts:` | no | Who decides when reviewers disagree. Can be split by topic, as in the case-study line. If missing, the approver decides; if there's no approver, ask the user |

Fields are separated by ` | `. The source tag at the end follows the brand-memory format. Lines without `type:` are ignored.

**No list at all?** The approval state is unknown. Say so, ask who must sign off for this content type, and offer to add the line to `brand/rules.md` once they answer. Never fill the list with a guessed name or role.

## Reviewer feedback files (shared)

One file per reviewer, anywhere the user keeps them (often `reviews/` beside the draft). Header lines first, then one comment per bullet or numbered line:

```markdown
Reviewer: Priya Shah
Role: editor
Reviewed: prime-cost-guide.md (v1)
Sign-off: changes requested

- "recieve" is misspelled. Should be "receive".
- [Intro, second paragraph] Cut this paragraph. It repeats the opening.
- Is this meant for groups too?
```

| Header | Values |
|---|---|
| `Reviewer:` | Full name |
| `Role:` | editor, subject expert, legal, compliance, marketing, approver, or the team's own word |
| `Reviewed:` | The file and version they read |
| `Sign-off:` | `approved`, `approved with changes`, `changes requested`, or `none` |

- Quoted text that appears in the draft is the comment's location. A `[Section]` tag works too.
- `approved with changes` (or "approved once…") is a sign-off that counts only when its conditions are met in the new version. A condition that depends on someone else ("once legal is happy") is met only when that person signs.
- A comment that says "looks good" is not a sign-off unless the `Sign-off:` line says so.
- Missing headers are read from the file name (`priya-shah-editor.md`). If the role still can't be told, ask.

**Pasted notes, tracked-change summaries, emails:** save each reviewer's notes in this format as `.review/<name>-<role>.md` in the project folder, copying their words exactly. Don't tidy, merge or soften them on the way in. If a sign-off isn't stated, write `Sign-off: none`.

## Routing extensions

All optional. They sit on the same `## Approvals` lines (or in the same `approvals.md`), so there is still one list.

### Extra fields on a `type:` line

```markdown
- type: case study | sign-off: editor=Priya Shah, legal=Marcus Lee, approver=Hannah Ruiz | conflicts: Hannah Ruiz | order: editor > legal > approver | sla: editor=1, legal=3, approver=2 | self-approval: no [source: Hannah Ruiz, 2026-10-20 · confirmed]
```

| Field | Meaning | If missing |
|---|---|---|
| `order:` | Steps separated by ` > `. Roles in one step, separated by commas, review at the same time | Everyone except the approver reviews at once; the approver signs last |
| `sla:` | `role=N`: business days that role has to respond, counted from when the step before it is due | "Not set": no due date for that step; say so, don't guess one |
| `self-approval:` | `no` or `yes`. With `no`, a person's sign-off never counts on a piece they requested or wrote | Treated as `no`. Say the rule is silent and ask whether that's right |

### Trigger lines

A `trigger:` line adds a reviewer (or a consent record) when the content contains something specific. Trigger lines never contain `type:` or `sign-off:`, so readers of the shared format skip them.

```markdown
- trigger: performance claim | adds: legal=Marcus Lee | checks: every result, speed or savings claim has substantiation on file | sla: 3 | before: approver [source: …]
- trigger: price or offer | adds: finance=Dev Patel | checks: every price matches offer.md; terms and end date stated | sla: 1 | before: approver [source: …]
- trigger: customer named | adds: consent | checks: written OK to be named recorded in proof.md (named: yes) | before: approver [source: …]
- trigger: spend over 2500 | adds: finance=Dev Patel | checks: the spend is in the approved budget | sla: 1 | before: approver [source: …]
```

| Field | Meaning |
|---|---|
| `trigger:` | One of: `performance claim`, `comparative claim`, `price or offer`, `customer named`, `regulated health`, `regulated financial`, `regulated employment`, `spend over <amount>`, `brand change` |
| `adds:` | `role=Name` (one or more, comma-separated), or the word `consent` for a customer-consent record instead of a person |
| `checks:` | What that reviewer looks at for this trigger. Copy it into the route as written |
| `sla:` | Business days for this reviewer. If the person is already on the route for the same piece, the longer of the two applies |
| `before:` | The role this reviewer must finish before (default `approver`). The reviewer joins the step just before that role and works at the same time as it. If that role is the first step, they get a new step ahead of it |

### How a route is built

1. Pick the `type:` line for the content type (exact or plural match, else `default`, and say the default was used).
2. Lay out its steps from `order:`.
3. For each trigger found in the content, add the reviewer from its `trigger:` line. If that person is already on the route, don't add them twice: add the trigger's checks to their row and keep the longer response time. Two triggers that name the same person become one row.
4. A trigger found in the content with no `trigger:` line still goes on the route, with the reviewer as `TBD: who checks <trigger>?`. Never fill in a name.
5. Apply `self-approval:`. If the requester holds a role and self-approval isn't `yes`, the `backup:` for that role signs instead. With no backup, the role is `TBD` and the route is blocked until the user names someone.
6. Due dates: the first step is due its SLA in business days after the request date. Each later step is due its SLA after the previous step's due date (the latest one, when a step has several reviewers). Weekends don't count. Public holidays aren't counted either, so say so when a date falls near one.

### Sign-offs and versions

A sign-off comes from a reviewer feedback file (above). It counts for this route only when:
- it's from the person the route names for that role (or that role's named backup),
- its `Reviewed:` line names this file and this version (a sign-off on `v1` doesn't cover `v2`; a missing `Reviewed:` line means ask),
- its `Sign-off:` is `approved`, or `approved with changes` with those changes in this version,
- it isn't the requester's own sign-off when self-approval is `no`.

A message saying someone approved ("Hannah said it's fine") goes in a feedback file as `.review/<name>-<role>.md` with their exact words and the version they saw. If the version isn't known, it doesn't count yet: ask.

## Customer consent records

Consent lives in `brand/proof.md`, on the customer's line, as `named: yes | no | unconfirmed` with a source tag (the brand-memory format). For a route:
- `named: yes` with a source: consent on record. Cite the line.
- `unconfirmed`, `no`, or the customer isn't in `proof.md`: no consent on record. That's a blocker, and no staff sign-off stands in for it.
- The fix is the customer's written OK, recorded on their line in `proof.md` (`named: yes`, with the date and where it's kept), or removing the name and quote.

## Checklist when adding lines for a user

Only on a yes from the user, and only with names and numbers they gave:
- One `type:` line per content type they named, with the `sign-off:` roles and names they gave, and `TBD` for any name they didn't.
- `trigger:` lines only for the triggers they confirmed, with the person they named.
- A source tag with their name and today's date, `confirmed`.
- A line in `brand/changelog.md`.
