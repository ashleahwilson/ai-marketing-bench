---
name: win-loss-summary
description: Writes a one-page summary of a win-loss interview with a buyer who chose or rejected the product, leading with the reason the buyer gave most often, using word-for-word quotes and reporting rather than recommending. Use when the user has a win-loss or lost-deal interview transcript or notes and wants a summary, for example "summarize this win-loss call", "write up the Halden interview", "why did we lose this deal, from the transcript". Not for deal reviews built from CRM data alone, or for competitive battlecards.
license: MIT
metadata:
  version: "1.0.0"
  author: "Rosa Lindqvist"
---

# Win-loss summary

Turns one buyer interview into a page sales and product can read on a phone. It reports what the buyer said. It doesn't recommend, predict or paraphrase.

## Ground rules

1. **Lead with the reason the buyer gave most often, and say how many times.** The loudest reason isn't always the real one. If two reasons tie, lead with both and say they tied.
2. **Quotes are word for word from the transcript.** A paraphrase never goes in quote marks.
3. **Deal size at the top,** taken from the CRM export or the user. If neither has it: "Deal size: not given". Never estimate it.
4. **Report, don't recommend.** Product decides what to do. An optional last section, "Questions this raises", holds questions only.
5. **Don't predict.** Write what the buyer said ("maybe next year"), not what they'll do.
6. **Under 300 words.** Sales reads these on a phone.
7. **"Buyer", not "customer".** A loss was never a customer.
8. **Never name individual people at other companies.** Name the company only.
9. **Facts come from the transcript, the CRM export, brand memory or the user.** Read `brand/` for product names and words to avoid. Without it, write the summary and mark it provisional.

## Workflow

```
- [ ] 1. Load: the transcript, the CRM export if given, brand/
- [ ] 2. Count the reasons the buyer gave, with line references
- [ ] 3. Write the summary in the shape below
- [ ] 4. Check: python3 scripts/check_summary.py <summary> --transcript <transcript>
- [ ] 5. Reply
```

The check confirms the word count, that every quoted passage appears in the transcript, that the deal size line exists, and that no "should", "recommend" or "will likely" slipped in. A FAIL means rewrite.

## Output

```
**<Won | Lost>: <company>, <role>** · Deal size: <amount | not given>
**Main reason** (given <n> times): <reason>
**Other reasons:** <reason (n)>
**In their words:** "<exact quote>" (<line>)
**Questions this raises:** (optional, questions only)
```

Never mention the check, its script or this skill's name in the summary or the reply.

## What good looks like

Product can act on it without reading the transcript, and every quote survives a search of the transcript. A worked example is in `assets/examples/`.
