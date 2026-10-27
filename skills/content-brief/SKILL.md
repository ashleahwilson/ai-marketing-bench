---
name: content-brief
description: Turns a content request (a topic, a goal, a rough idea or a campaign need) plus brand memory into a brief a writer or another skill can work from, saved in briefs/ in the format content-qa-gate later checks the finished piece against (goal, audience, channel, key message, must-includes, CTA with URL, primary keyword, length, publish date), followed by an angle, outline, sources and what to avoid. Must-includes come only from confirmed brand facts or the user; keywords are marked unvalidated unless the user supplies search data, and no volumes, rankings or statistics are invented. Asks one short round of questions when the goal, audience or CTA is missing, and pushes back when a request targets an audience the brand doesn't serve or depends on an unsubstantiated claim. Use when the user wants a content brief, a writer's brief, a blog or email brief, or "a brief for a post on X". Not for planning a whole content calendar, writing the piece, or checking a finished draft (use content-qa-gate).
license: MIT
compatibility: Recommended for large models, and check any description of what an offer includes. In testing both Haiku and Opus occasionally widened a fact (what a free review covers, a planned launch date treated as past). See evals/scorecard.json.
metadata:
  version: "1.2.1"
  author: "Ashleah Wilson"
---

# Content brief

Turns a request into a brief that a writer can follow without asking a question, and that content-qa-gate can check the finished piece against. The brief decides what the piece must say and must not say. It doesn't write the piece.

## Ground rules

1. **Must-includes come from two places only:** a line tagged `confirmed` in `brand/`, or a fact the user stated. Provisional, assumed or held facts never become must-includes. A third-party statistic the user supplies needs a cited source before it can run: it goes under "Open before writing", not into Must include.
2. **Never invent search data.** No volumes, difficulty scores, rankings, traffic estimates or "high-volume" labels unless the user supplied the data. Without data, the keyword is marked unvalidated and the brief says what would validate it. If the user asked for numbers, say once that you don't have their data and won't estimate, then deliver the brief anyway.
3. **Missing stays missing.** An unknown URL, date or fact is written `TBD: <what's missing>` and listed with who can answer it. A plausible guess is still an invention.
4. **Ask, don't guess, when the essentials are missing.** If the goal or the CTA action is missing, or the audience can't be read from the request or a single clear segment in brand memory, ask one round of at most four short questions and don't write the file yet. If the user said "don't ask" or "just draft it", write it with `TBD`s instead.
5. **Push back on a brief that can't work.** If the requested audience or offer is one brand memory says the brand doesn't serve, or the topic only works with a claim brand memory holds as unsubstantiated, don't write that brief. Say why in one line, name what would change the answer, and offer the nearest brief that does work. Never refuse outright, and never lecture.
6. **No invented generalizations either.** The angle and outline make no claim about how readers behave or how many do something ("most owners…", "the average clinic…") unless brand memory or the user says it. Plain definitions and formulas a reader could find in any textbook (what food cost % is, how it's calculated) are explanation, not claims: they need no source. URLs the user or brand memory gives are real, even reserved test domains such as `.example`.
7. **Never overwrite the user's files.** A brief with the same name gets a new slug (`-v2`). Brand memory is read, never edited.

## Pick the mode

| The request… | Mode |
|---|---|
| Has the goal, audience and CTA (or brand memory supplies the audience) | **Draft** (default): write the full brief |
| Is missing the goal or the CTA action, or the audience is unclear | **Ask:** one round, at most four questions, no file |
| Says "walk me through it", "let's decide together", or is a campaign with several pieces | **Guided:** propose 2–3 angles (and the list of pieces for a campaign), ask the user to pick, then draft one brief per piece |
| Says "don't ask", "just draft it", "I'll fill the gaps" | **Draft with gaps:** write it, `Status: draft (gaps marked TBD)`, gaps listed first |
| Targets an audience or offer brand memory rules out, or rests on a held claim | **Hold:** no file; reason, what would change it, and the nearest workable brief |

## Workflow

```
- [ ] 1. Load: the request, brand/, any data or notes the user points to
- [ ] 2. Decide the mode (table above, judgment in references/judgment.md)
- [ ] 3. Build the fact list: every fact the brief will use, with its source
- [ ] 4. Write briefs/<slug>.md in the format in references/brief-format.md
- [ ] 5. Self-check: run scripts/check_brief.py, then the questions in references/judgment.md
- [ ] 6. Reply in the fixed shape
```

### 1. Load

List the project folder first and look for `brand/`, even if the user didn't mention it. Read `BRAND.md`, `audiences.md`, `offer.md`, `proof.md`, `claims.md`, `rules.md` and `voice.md` where they exist. Read any keyword export, research or notes the user names.

**No `brand/` folder?** Work from the request only. Mark the brief `Status: provisional (no brand memory)`, use only facts the user stated, and end the reply by offering to set up brand memory (the brand-memory skill) or to record the facts from this request.

### 2. Decide the mode

Work through [references/judgment.md](references/judgment.md): is there enough to write it, does the request fit the brand's audience and offer, and can the topic stand on confirmed facts. Ask or hold before writing anything.

### 3. The fact list

Before writing, list each fact the brief will rely on and its source: `brand/<file>` with its status, or "from the request". Anything else is either cut or moved to "Open before writing". Check each must-include against the rules in judgment.md: quotes word for word from `proof.md` with their naming permission, the right price for this audience, third-party statistics flagged for a source, no incentive or deadline the user didn't give.

### 4. Write the brief

Follow [references/brief-format.md](references/brief-format.md) exactly. The nine fields come first as `- Field: value` lines, then `## For the writer` with Angle, Outline, Sources to use, Search, Avoid and Open before writing. Three details the next skill depends on:
- The `Primary keyword` line holds the keyword phrase only. Its status (unvalidated, or the figures from the user's data) goes under `### Search`.
- `Length` reads `<low>–<high> words`, from the channel rule in `brand/voice.md` where there is one.
- No bullet in the writer section starts with one of the nine field names and a colon.

Put held claims, banned phrases, never-use words and channel rules (for example "no hashtags") under Avoid, so the writer knows them.

Slug: lowercase, hyphenated, three to six words from the topic (`briefs/food-cost-percentage.md`).

### 5. Self-check

```bash
python3 scripts/check_brief.py briefs/<slug>.md --brand brand/ [--keywords <data file>] --request "<the user's request>"
```

Fix every FAIL and rerun. For every CHECK line: trace the figure or phrase to a source, move it under Avoid or Open before writing, or delete it. Then answer the six self-check questions at the end of judgment.md. A "no" means rewrite the brief, not add a caveat to the reply.

### 6. Reply

```
**Brief:** written to briefs/<slug>.md (ready | provisional | draft with gaps) | not written: <one-line reason>

**Recommendation:** <the angle in one line, or for Ask/Hold, what's needed or the nearest brief that works>

**Before it goes to a writer:** numbered gaps, flags and decisions for the user (TBDs, sources needed, naming permission, keyword status). "Nothing blocking" if none.

**Kept out:** one line naming what was deliberately left out and why (held claims, unrecorded figures). Omit if nothing.
```

- **Ask:** the "Brief" line says not written yet, then the numbered questions, each with the likely answer from brand memory where there is one. Nothing else.
- **Hold:** the reason quoted from brand memory with its file, what would change the answer, and the nearest workable brief offered in one line. Under 200 words.
- Keep replies under 250 words. The brief is in the file; don't paste the whole thing.
- Never mention the checker, this skill, its references or its default ranges by name ("a typical LinkedIn length", not "the skill's default"). Talk to the user in the second person.
- "Who can answer" is "you" or a person named in `brand/` (for example a founder in `proof.md`). Never name anyone else, even someone you know from other context.

## Keep tools out of the deliverable

Never name this skill, other skills, or their scripts and checks in a reply, report, draft or file the user may pass on: these often go to clients or the public. Describe what was checked, not the tool that checked it. If your environment asks you to say which skill you used, put that in one short line to the user, separate from the deliverable, never inside it.

## What good looks like

A writer who has never met the brand reads the brief in three minutes and writes something content-qa-gate passes first time. Every must-include points to a line in `brand/` or the request. Every gap is a visible `TBD` with an owner. Nothing in the brief depends on a number the skill made up.

A worked example (a Tallyhouse brief for catch-up bookkeeping) is in [assets/examples/tallyhouse/](assets/examples/tallyhouse/README.md).
