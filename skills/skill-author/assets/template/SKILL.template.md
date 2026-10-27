---
name: <lowercase-with-hyphens, same as the folder>
description: <Third person. What it does, in one or two sentences. Use when <phrases a user would type>. Not for <the nearest thing it shouldn't be used for>.>
license: <what the user gives; otherwise "Internal use only">
metadata:
  version: "1.0.0"
  author: "<the user's name, or TBD>"
---

# <Title>

<One paragraph: what it does, what it doesn't.>

## Ground rules

1. **<Rule from the ledger, imperative.>** <Why, in a few words, from the correction.>
2. **Facts come from brand memory or the user.** Read `brand/` if it exists. Never take a price, name, claim or result from memory. Anything unknown is flagged, not filled.
3. **Without brand memory,** do the work, mark the output provisional, and offer to set brand memory up.
4. **Never overwrite the user's files.** Write new files beside them.

## Workflow

```
- [ ] 1. Load: the request, the inputs, brand/
- [ ] 2. <Do the work>
- [ ] 3. Check: python3 scripts/<check>.py <output>; then the judgment checklist
- [ ] 4. Reply in the fixed shape
```

### 3. Check

<What the script checks. What needs judgment.> A FAIL means rewrite, not hedge.

### 4. Reply

```
**<Recommendation / verdict line first>**
<the named sections>
**Needs from you:** <only what's missing>
```

Never mention scripts, file internals or skill names in the reply or the deliverable.

## What good looks like

<Two or three sentences.> A worked example is in [assets/examples/<case>/](assets/examples/<case>/README.md).
