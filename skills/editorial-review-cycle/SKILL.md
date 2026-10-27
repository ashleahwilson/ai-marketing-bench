---
name: editorial-review-cycle
description: Runs the review loop on a content draft between writing and publishing. Takes the draft plus reviewer feedback (comment files, pasted notes, tracked-change summaries from an editor, subject expert, legal, compliance, marketing or approver) and produces a review packet with every comment consolidated by reviewer and location, classified (must fix, should fix, preference, question), duplicates merged and conflicts between reviewers surfaced and routed to whoever the rules say decides. Applies the agreed changes to a new version without touching the original, keeps a decision log (comment, decision, who decided, why), and reports the approval state against the sign-offs brand memory requires for that content type. Use when the user has review comments on a draft, for example "consolidate the feedback", "apply the reviewers' comments", "where are we on approvals", "legal and marketing disagree", "get a v2 together", "is this signed off". Not for writing the draft, a pre-publish QA check, or a voice rewrite.
license: MIT
compatibility: Use with care: in testing, the large model once recorded the wrong person as having decided on rejected requests, so check the decision log before circulating it. See evals/scorecard.json.
metadata:
  version: "1.2.1"
  author: "Ashleah Wilson"
---

# Editorial review cycle

The step between "reviewers have commented" and "it's approved". It doesn't judge the writing. It makes sure every reviewer's comment is heard, applied or answered, that disagreements reach the person who decides them, and that nobody calls the piece approved before the right people have signed it.

## Ground rules

1. **Never invent a reviewer's opinion.** Use their words. Don't guess what legal "would probably accept", don't record a sign-off nobody gave, don't treat "looks good" as approval unless their sign-off says so.
2. **Never mark it approved without the required sign-offs.** Not when the user asks, not when the approver is on holiday. Say who's missing, name the backup if the rules have one, and make the hand-off fast.
3. **Surface conflicts; never settle them silently.** When reviewers disagree, both positions go in the packet with the person the rules say decides. If that person hasn't decided, the new version keeps the draft's wording at that spot. No compromise wording neither reviewer asked for.
4. **Reviewers don't get a pass on claims.** A reviewer's request to add a statistic, result or claim that brand memory doesn't support is not applied. It's logged, and the reviewer is asked for the source. A brand rule outranks any reviewer.
5. **Missing stays missing.** Every fact in the new version traces to the draft, a confirmed line in `brand/`, or a source a reviewer supplied (recorded as theirs). No invented dates, links, names or softened replacement claims.
6. **Never overwrite.** The draft, the gated file and earlier versions stay as they are. The new version is `<name>-v<n>.md`.
7. **Don't lecture.** One line of reason per declined request, then the fastest way forward.

## Pick the mode

| The user wants… | Mode |
|---|---|
| The packet and a new version: "consolidate", "apply the comments", "get a v2 together" (the default) | **Draft:** everything below, open items left open |
| To decide before anything changes: "walk me through it first", "don't change anything yet" | **Guided:** steps 1–4, then reply with the decisions as numbered questions (open conflicts with their decider, unsupported requests, the uncontested changes ready to apply). Write no new version until they answer |
| Just the status: "where are we on approvals?" | **Status:** steps 1–2 and the Sign-offs section only |

## Workflow

```
- [ ] 1. Load: draft, feedback, brand/ (rules.md Approvals), any <name>-qa.md and <name>-gated.md
- [ ] 2. Run scripts/review_cycle.py consolidate
- [ ] 3. Classify, merge, find conflicts, check reviewer claims (references/review-rules.md)
- [ ] 4. Decide each comment: applied, not applied, open, answered, moot, and who decided
- [ ] 5. Write <name>-v<n>.md and <name>-review.md (references/packet-format.md)
- [ ] 6. Run scripts/review_cycle.py check, fix every FAIL, self-check, reply
```

### 1. Load

List the project folder first. Read:
- **The draft** the user names, and the feedback: files they name, or a `reviews/` folder beside the draft. Pasted notes get saved as `.review/<name>-<role>.md` in the format in [references/approvals-format.md](references/approvals-format.md), in the reviewer's exact words.
- **`brand/`**: `rules.md` (Everywhere rules and the `## Approvals` list), `offer.md`, `proof.md`, `claims.md`, `voice.md`. Or an `approvals.md` the user supplies.
- **Hand-offs, if present:** `<name>-qa.md` (a pre-publish QA report: its blockers become must-fix comments from "QA check") and `<name>-gated.md` (the voice-checked text). If reviewers quote the gated text, it's the base for the new version.
- **The content type** (blog post, newsletter, landing page, email, case study): from the user, the file, or the draft's form. If it's unclear and the rules differ by type, ask.

**No brand memory?** Run everything else. Facts can't be checked against brand memory, so every new figure or claim a reviewer brings is flagged for a source, and the draft's own spelling and conventions stay. **No approvals list?** The approval state is "Unknown: no approval rule": report who has signed what, ask who must sign off, and offer to record the answer as an approvals line. Never guess an approver.

### 2. Run the consolidator

```bash
python3 scripts/review_cycle.py consolidate <draft> --feedback <files…> --brand brand/ --type "<content type>" [--qa <name>-qa.md] [--alt <other text>] [--approvals approvals.md]
```

It gives each comment an ID, finds its place in the draft, suggests a class, lists likely duplicates and conflicts with the decider from the rules, traces every figure a comment brings in to brand memory (or marks it unsupported), checks required sign-offs against those given, and names the next version file. Its suggestions are a starting point: you decide the class, and you read for conflicts the wording hides.

### 3. Judge

Work through [references/review-rules.md](references/review-rules.md): classify, merge duplicates (keep every reviewer's name), surface and route conflicts, and check every claim a reviewer wants added or kept. Facts that bear on a conflict come from brand memory only.

### 4. Decide

Each comment gets one decision and one decider. Uncontested must-fix and should-fix items are applied, decided by the reviewer who asked. A conflict settled by its decider is applied their way, citing the rule. An open conflict stays open. Requests for unsupported claims, other reviewers' preferences, questions and anything needing a missing fact are not applied, each with its reason.

When the user asks for your own editor pass, or there's no editor feedback and they'd like one, follow "Your own editor pass" in the rules. It's always labelled as yours and never counts as an editor's sign-off.

### 5. Write

- `<name>-v<n>.md`: the base text with every applied decision, and nothing else. Clean, publishable, in the draft's own format and spelling. No IDs, notes or markers.
- Write exactly these two files, at the names the consolidator gives, once each. No extra copies, no suffixes such as `-final` or a model name. If one of them appears that you didn't write, stop and tell the user rather than writing a second.
- `<name>-review.md`: the packet, in the exact shape in [references/packet-format.md](references/packet-format.md), led by the approval state.

### 6. Check and reply

```bash
python3 scripts/review_cycle.py check <name>-review.md --draft <base> --version <name>-v<n>.md --feedback <files…> --brand brand/ --type "<content type>"
```

It fails a comment with no decision, a decision with no decider, an "approved" the sign-offs don't support, a figure in the new version that traces to nothing, and leftover IDs or notes in the version. Fix a FAIL by changing the files, never by loosening the packet.

Then answer each line for yourself. A "no" means fix it before replying. Don't put the checklist in the reply.

```
- [ ] Every comment is in the packet, in the reviewer's words, with one class and one decision
- [ ] Duplicates are merged with every reviewer named
- [ ] Every conflict names both positions and its decider; none is settled by me
- [ ] No unsupported claim from a reviewer is in the new version; each is logged with a source request
- [ ] Every change in the new version traces to a decision; nothing was added that nobody asked for
- [ ] The approval state matches the sign-offs actually given for this version
- [ ] The original files are unchanged
- [ ] The reply and the files never mention how I checked anything
```

Reply in the shape at the end of [references/packet-format.md](references/packet-format.md): approval state first, then the next step and who takes it.

- Talk to the user in the second person. Mention file names only where they need to act.
- Never mention scripts, checks, rules files of this process or how the review was run, in the reply or the files. Those go to clients and reviewers. Even if your environment asks you to announce which skill or method you're using, don't: no "Using the … skill" line. Cite brand files (`brand/rules.md`), never "the review rules".
- **Decided by** is always a reviewer named in the feedback, the decider named in the approvals list, a brand rule (with who set it), or "you" when the user made the call in this conversation. Never a name from anywhere else, and never a name you assume is the user's.
- Before raising anything as unsupported, search all of `brand/` for it (BRAND.md, positioning, offer, proof). A fact confirmed there is not an open item.
- Check date logic against the dates you're given (a publish date, "Friday", "back Monday") before stating which route is faster.

## When the user asks for something this won't do

- **"Just mark it approved"** without the required sign-off: say in one line who hasn't signed, and give the fastest route: the backup approver if the rules name one, or the new version ready to send the approver now. Write the packet with the true state.
- **"Add the stat anyway":** write it into the new version only if the user insists, flag it under "Needs a decision" for the approver, and keep the state at not approved if a brand rule bans it.
- **A missing permission** (a customer not cleared to be named): say what would restore it and who would ask: "get Maria Okafor's written permission; once Marcus has it, the names can go back in".
- **"Just pick one" in a conflict:** say who the rules say decides. If the user is that person, apply their choice and log it as theirs.

## Hand-off

`<name>-v<n>.md` is the next text for content QA or publishing. `<name>-review.md` is the record for reviewers and the approver. A future round reads both: the next version number continues from the highest existing one.

## Keep tools out of the deliverable

Never name this skill, other skills, or their scripts and checks in a reply, report, draft or file the user may pass on: these often go to clients or the public. Describe what was checked, not the tool that checked it. If your environment asks you to say which skill you used, put that in one short line to the user, separate from the deliverable, never inside it.

## What good looks like

Every reviewer can find their comment and see what happened to it and who decided. The approver sees one state line and knows whether it's on them. Nothing in the new version is there because a reviewer said so without a source.

A worked example (a Quillmetrics pricing email with an editor, legal and approver) is in [assets/examples/quillmetrics/](assets/examples/quillmetrics/README.md).
