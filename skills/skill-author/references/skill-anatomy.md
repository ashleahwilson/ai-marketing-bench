# What the new skill must contain

## Contents
- The folder
- Frontmatter
- SKILL.md sections
- Behaviours every skill needs
- Scripts
- The worked example
- Changelog and versions

## The folder

```
skills/<name>/
├── SKILL.md                 under about 200 lines
├── CHANGELOG.md
├── references/              one level deep; "## Contents" on any file over 100 lines
├── scripts/                 standard-library Python for anything mechanical
├── assets/examples/<case>/  one complete input and output, different from every eval
└── evals/
    ├── evals.json           at least 8 evals, at least 2 traps
    ├── files/               the fixtures
    └── rules-ledger.md      why each rule exists
```

Only create a references file when SKILL.md would otherwise grow past about 200 lines, and link every one from SKILL.md with a line on when to read it.

## Frontmatter

```yaml
---
name: <lowercase-with-hyphens, same as the folder>
description: <third person: "Writes…", "Checks…". What it does, then "Use when…" with phrases a user would type. Up to 1,024 characters. Name what it's not for if a neighbouring skill could be confused with it.>
license: <what the user gives; otherwise "Internal use only", and ask>
metadata:
  version: "1.0.0"
  author: "<the user's name if they gave it; otherwise \"TBD\", and ask>"
---
```

Only these keys (plus `compatibility` and `allowed-tools` when needed). No tags, categories or custom fields: other agents ignore or reject them.

## SKILL.md sections

1. **One paragraph:** what it does and what it doesn't.
2. **Ground rules:** the method rules from the ledger, most important first, each with its reason. Keep the user's terms.
3. **Workflow:** a checklist of steps, then a short section per step.
4. **Output:** the fixed shape, in a code block, leading with the recommendation or verdict.
5. **What good looks like:** two or three sentences, then a link to the worked example.

Write it in plain, direct sentences. Explain why a rule matters instead of shouting it.

## Behaviours every skill needs

- **Reads brand memory.** "Read `brand/` if it exists (offer, proof, voice, rules). Without it, do the work and mark the output provisional, and offer to set brand memory up." Facts come from there, never from the skill text.
- **Keeps a fact list.** Every name, number and claim in its output traces to the user, brand memory or a cited source. Unknowns are flagged, never filled.
- **Checks its own output** before replying: the script for anything countable, then a short written checklist for judgment calls. A failed check means rewrite.
- **Knows when not to act.** It pushes back on bad inputs and can recommend doing nothing, without refusing or lecturing.
- **Never overwrites the user's files.** It writes new files beside them.
- **Doesn't talk about itself.** Its replies and deliverables never mention its own name, its scripts or other skills.
- **Two modes where it matters:** Draft (full first pass) and Guided (pause at each material decision). Nothing is sent, posted or published without the user's approval.

## Scripts

Anything a model could miscount goes in a script: word and character limits, required sections, banned words from `brand/voice.md`, figures that must match a source, placeholder text left in. Rules for scripts:
- Python standard library only. No installs.
- Takes file paths as arguments, prints one line per finding (`FAIL`, `WARN`, `OK`) and exits non-zero on a FAIL.
- Reads limits and banned words from brand memory where they live there, with the method's defaults otherwise.
- Run it once yourself on the worked example before saving, and fix it if it errors.

## The worked example

One complete case in `assets/examples/<case>/`: a `README.md` saying what's in it, the input files, and the output the skill should produce. It must differ from every eval (different company, different case), so a test run can't copy the answer. Fictional companies only, and no claimed results.

## Changelog and versions

`CHANGELOG.md` starts with the version and date and lists what the first release does, in user terms. Use `1.0.0` when the material supported at least 8 real evals and every rule has a source; `0.1.0` with "Provisional:" in the changelog and a line in SKILL.md when it didn't.
