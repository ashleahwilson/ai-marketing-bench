# Brief format

A brief has two parts. The top part is the nine fields content-qa-gate reads, written exactly as `- Field: value` lines. The bottom part, under `## For the writer`, is what a writer needs beyond that. Save it as `briefs/<slug>.md`.

```markdown
# Brief: How to run a weekly pipeline review

Status: ready
Brand memory: brand/ (read 2026-10-23)

- Goal: get sales managers to start a free 14-day trial
- Audience: sales managers running teams of 5–20 reps at B2B software companies
- Channel: blog
- Key message: a pipeline review only helps if it ends with a next step on every deal
- Must include: the four questions to ask about each deal; that Pipewise flags deals with no next step; the free 14-day trial
- CTA: "Start your free trial" → https://pipewise.example/trial
- Primary keyword: pipeline review
- Length: 800–1,200 words
- Publish date: 2026-12-02

## For the writer

### Angle
...

### Outline
1. ...

### Sources to use
- "flags deals with no next step": brand/offer.md (confirmed)

### Search
Keyword status: unvalidated. No search data was supplied. Candidates to check: pipeline review; sales pipeline review meeting.

### Avoid
- ...

### Open before writing
- TBD: ...
```

## The nine fields

| Field | Write it as | Where it comes from |
|---|---|---|
| Goal | What the reader should do or believe after reading, in one line | The user. Never assumed |
| Audience | One specific reader: role, business type, size | The user, or brand memory's segment when the request clearly fits it |
| Channel | One word first: `blog`, `landing`, `web`, `email`, `newsletter`, `linkedin`, `social` | The user |
| Key message | One sentence the reader should repeat | Built from confirmed facts and the angle |
| Must include | Items separated by semicolons | Confirmed brand facts or the user only |
| CTA | `"<button or link text>" → <URL>` | The user or brand memory. Unknown URL: `→ TBD: URL` |
| Primary keyword | The keyword phrase only: no volume, no note, no brackets | The user's data, or the topic (then marked unvalidated under Search) |
| Length | `<low>–<high> words` | The channel rule in `brand/voice.md` if there is one, otherwise the channel |
| Publish date | `YYYY-MM-DD`, or `TBD` | The user |

Why these rules matter to the next skill:
- content-qa-gate reads every `- <words>: <value>` line in the whole file, and a later line with the same name replaces an earlier one. So the writer section never starts a bullet with one of the nine field names followed by a colon.
- It checks that the CTA URL is linked in the piece, so the URL must be real or `TBD`.
- It looks for the primary keyword word for word in the title, H1 and first 100 words, so anything else on that line breaks the check. Keyword status goes under `### Search`.
- It reads `Length` with the pattern `<number>–<number> words`.
- It flags dates in the piece earlier than `Publish date`.

## Status line

| Status | When |
|---|---|
| `ready` | All nine fields filled from the user or confirmed brand memory, and nothing under Open before writing blocks the writer |
| `provisional (no brand memory)` | No `brand/` folder; facts come from the request only |
| `draft (gaps marked TBD)` | Any field is `TBD`, or an open item blocks the writer (for example a source or permission the piece depends on) |

## Writer section

Keep each part short. A writer should read the whole section in two minutes.

- **Angle:** the one idea that makes this piece worth reading, and why it suits this audience. One or two sentences.
- **Outline:** 3 to 7 numbered sections, each a heading and one line on what it covers. Every factual point in the outline is one of the must-includes or a sourced line.
- **Sources to use:** each must-include, with the file and line it comes from and its status. User-supplied facts say "from the request".
- **Search:** keyword status (validated from the user's data, with the figures exactly as supplied, or unvalidated) and up to five candidates to check. Search channels only.
- **Avoid:** claims held in brand memory, never-use words, banned phrases from `rules.md`, and channel rules (for example "no hashtags"). Quoting a banned phrase here is how the writer learns it.
- **Open before writing:** every `TBD`, each with who can answer it. Facts that need a source before they can run go here, not in Must include.

Any field can be `TBD`. content-qa-gate skips the checks that depend on a missing field and says so.
