# Approvals and feedback formats

Two plain-text formats: the approvals list (who must sign off on what) and the reviewer feedback file. Both can be written by hand in a minute, and any skill can read them.

## The approvals list

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

## Reviewer feedback files

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
