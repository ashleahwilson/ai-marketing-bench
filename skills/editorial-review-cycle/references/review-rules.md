# Review rules

How to classify, merge, route and apply comments, and how to state the approval. Work through them in this order.

## Contents

- Classify
- Merge duplicates
- Surface conflicts
- Claims and figures from reviewers
- What gets applied
- Writing the new version
- The approval state
- Your own editor pass

## Classify

Every comment gets exactly one class.

| Class | When | Examples |
|---|---|---|
| **must fix** | Wrong facts, prices or names; typos; anything legal or compliance requires; a brand-rule breach; a QA blocker | "$329 is wrong, it's $349"; "disclosure must be in the first paragraph" |
| **should fix** | A clear improvement to accuracy, structure or clarity that nobody contests | "cut this paragraph, it repeats the intro"; "add Lightspeed to the POS list" (when brand memory confirms it) |
| **preference** | Taste, signalled by the reviewer ("I'd", "your call", "nit") or with no reason beyond style | "I'd say month-end instead of end of the month" |
| **question** | The reviewer asks rather than asks for a change | "Is this meant for groups too?" |

A preference from the approver is still a preference, but the approver's preferences are applied unless they conflict with another comment. A question is never turned into an edit: answer it from the draft or brand memory if you can (quote the line), otherwise route it to the author.

## Merge duplicates

Two or more comments asking for the same change at the same place become one item. Keep every reviewer's name on it ("Dev Patel, Priya Shah") and the strongest class among them. Comments at the same place asking for *different* things are not duplicates: they're a conflict or two separate items.

## Surface conflicts

A conflict is two reviewers asking for incompatible things: remove versus keep, soften versus strengthen, name versus anonymize. Some conflicts hide in different wording ("keep Maria's name everywhere" against "remove both names"). Read for them, don't rely on matching words.

For each conflict:
1. State both positions in the reviewers' own words, with names and roles.
2. Add the facts that bear on it, from brand memory only ("brand memory has no evidence for 'fastest'"; "permission to name her is unconfirmed"). Don't add an opinion about who's right.
3. Find the decider in the approvals list (`conflicts:`). If it's split by topic, say which topic this is and why.
4. **If the decider has already decided** (their comment takes a side), apply their side, and log it as decided by them, citing the rule. The other reviewer's view stays in the log.
5. **If the decider hasn't weighed in**, the conflict is open. Don't pick a side, don't split the difference, don't write a compromise wording neither reviewer asked for. The new version keeps the draft's wording at that spot, and the packet says so: "v2 keeps the draft headline until Rafael Costa decides." Escalate to the decider by name.
6. **No decider in the rules:** the approver decides. No approver either: ask the user who decides.

A brand rule is not a reviewer. When a reviewer asks for something a rule in `brand/rules.md` → Everywhere forbids, it isn't a conflict to escalate: the rule stands, the request is not applied, and the log names the rule and who set it.

## Claims and figures from reviewers

A reviewer's request to add or keep a claim gets the same scrutiny as the draft. Reviewers are a common source of unsupported claims ("everyone knows 60% of restaurants fail").

| The reviewer asks to add… | Do |
|---|---|
| A figure, result, price or feature that matches a confirmed line in `brand/` | Apply it, and cite the line |
| A figure or claim not in brand memory | Don't apply it. Log it as "not applied: no source in brand memory" and ask the reviewer for the source (the study link, the client data). Never write a softer version of it ("many clients save hours") |
| A third-party statistic | Not applied unless the reviewer gives the source. With a source (a link), it can go in, linked, and the log records who supplied it |
| A claim a brand rule bans or holds | Not applied. Quote the rule |
| A product fact that contradicts the draft and can't be checked (no brand memory) | Flag it for the product owner to confirm. Apply it only if the user confirms |

A reviewer who supplies a source for an existing claim resolves a "needs a source" item. Record the source and who gave it, and suggest adding it to brand memory.

## What gets applied

Applied to the new version:
- must fix and should fix items, unless they're in an open conflict or need a fact nobody has supplied;
- the approver's preferences, and any preference the brand's voice rules already require;
- QA blockers whose fix needs no new fact (deleting an expired date, linking a source a reviewer gave).

Not applied, and listed for the owner:
- other preferences ("owner's call");
- questions;
- open conflicts;
- requests for unsupported claims;
- anything that needs a fact, link, date or permission nobody has given.

When one change makes another moot (the editor rewords a sentence that legal's change removes), apply the controlling change and log the other as "moot after C3".

## Writing the new version

- Start from the text the reviewers read. If they quote `<name>-gated.md`, that's the base, not the original.
- Name it `<name>-v<n>.md`, the next number after any existing versions (the original counts as v1). Never write over the draft, the gated file or an earlier version.
- The new version is clean, publishable text in the draft's own format: no review IDs, no "[pending]" markers, no notes. Open items live in the packet.
- Keep the draft's spelling convention, or the brand's if `voice.md` sets one. Don't convert spelling to your own house style.
- Change only what a decision covers. Every difference between base and new version must trace to a row in the decision log.

## The approval state

The packet and the reply lead with one of:

| State | When |
|---|---|
| **Approved** | Every required sign-off for this content type is given for this version: `approved`, or `approved with changes` whose changes are all applied in it, and no conflict is open |
| **Not approved: waiting on <role (name)>** | Any required sign-off is missing, `changes requested`, or conditional on something not met |
| **Not approved: open conflict** | Sign-offs may be in, but a conflict is waiting on its decider |
| **Unknown: no approval rule** | There's no approvals list for this content type. Say who has signed what, and ask who must sign off |

- A reviewer who asked for changes has to see the new version before their sign-off counts.
- `approved with changes` counts only when all of that reviewer's changes are applied. If any were decided against or left open, they need to confirm their sign-off on the new version.
- A sign-off counts only from the named person, or from the named backup when they've actually signed. Never record a sign-off nobody gave, even when the user asks you to ("just mark it approved"). Say who's missing, name the backup if the rules have one, and make the hand-off fast: the new version is ready to send them.
- A reviewer who isn't on the required list (a marketing lead on a blog post) doesn't block approval, but their comments are still logged.

## Your own editor pass

Only when the user asks, or offers it when there's no editor feedback at all. It's labelled in the packet and the reply as **Editor pass (mine, not a reviewer's)**, with its own IDs (`E1`, `E2`…).
- It checks the same things an editor would: typos, never-use words and channel rules in `voice.md`, repetition, unclear sentences, length.
- It adds no facts and changes no claims.
- Its fixes go in the new version only if they're mechanical (typos, banned words, punctuation rules). The rest are suggestions.
- It is never a sign-off. If the approvals list requires an editor, the state stays "waiting on editor (<name>)".
