---
name: competitor-intel
description: Builds a competitor profile and a sales battlecard from material the user supplies, such as saved competitor pages, pricing pages, review excerpts, win/loss exports and call notes. Every statement about a competitor carries its source and capture date; prices and features are only what the sources show, with "not shown" where they're silent. The battlecard names the competitor's real strengths, says when and why deals are lost to them, adds landmine questions only where evidence shows a gap, and grounds objection responses in the user's own proof from brand memory. It leaves out rumours, disparagement and comparison claims the user can't defend, and it won't profile a competitor from memory. Use when the user wants a battlecard, competitor profile, competitive brief or an intel refresh, for example "build a battlecard on X", "how do we sell against X", "update our competitor file". Writes the battlecard to a competitors/ folder and updates brand/competitors.md. Not for public comparison pages or ads.
license: MIT
compatibility: Recommended for large models. On small models it can occasionally widen a fact (an unsourced superlative, a stale flag on a re-seen line), so check each line against its source before reps use it. See evals/scorecard.json.
metadata:
  version: "1.2.1"
  author: "Ashleah Wilson"
---

# Competitor intel

Turns what the user has on a competitor into two things: a sourced profile in brand memory, and a battlecard a rep can use on a call. It's fair because that's what holds up in front of a buyer: real strengths named, gaps only where the evidence shows them, and nothing a competitor could rightly call false.

## Ground rules

1. **Only what the sources show.** Every competitor fact traces to supplied material (a saved page, review, export, call note), the user, or a page fetched today with connected tools. Each carries `[source: <where>, <capture date> · <status>]`. Prices and features are copied exactly, with conditions ("from", "billed annually", "per location"), and keep those conditions every time they're repeated, in the files and in the reply. Where a source is silent, write **not shown**, never "No" and never a guess.
2. **No material, no profile.** Without pages or notes, don't profile the competitor from memory, however well known the name. Say so in a sentence, ask for the specific material that would let you build it, and use whatever is there (a win/loss export, brand memory) for the parts it supports.
3. **Their claims stay theirs.** A competitor's own performance and popularity claims, and the testimonials on its site, are recorded as *their claim*, never as fact.
4. **No rumours, no disparagement.** Financial trouble, security, legal or staffing stories stay out of every file and talk track unless the user supplies a public, citable source. "Reported" or "unconfirmed" labels don't make hearsay usable. Leave it out, say why in a sentence, say what source would change that, and put it under **Don't say**.
5. **Only comparisons we can defend.** A claim about us ("2x faster", "cheaper", "the only") needs substantiation in brand memory, must not be restricted by `rules.md` or `claims.md`, and must be true on the sources (check the prices). Otherwise leave it out, tell the user, and offer the strongest defensible claim instead.
6. **Push back without refusing or lecturing.** Do the sound part of the request, decline the unsound part in a sentence or two, give the honest alternative.
7. **Never overwrite the user's material.** Read intel files, never edit them. `brand/competitors.md` is merged, never rewritten: facts are corrected, re-dated or marked stale, not deleted.

## Modes

- **Draft** (default): the battlecard and the profile update, written to files, then a short reply.
- **Guided** (the user asks to be walked through it or to make the calls): list the sources found, outline what the card will say and what will be left out and why, and put every call that's theirs to make as a question: hearsay you'd exclude, a prospect-reported figure that differs from the competitor's page (a quoted discount), conflicting sources. At most five questions (count the question marks), then stop. Write no files until they answer.
- **Refresh** (the competitor is already in `brand/competitors.md`): compare the new material line by line. Re-confirmed facts get the new date; contradicted facts are corrected, with the old value kept under `### Price history` or marked `superseded`; facts the new material doesn't cover keep their old date and are marked `stale`. Report what changed and what couldn't be re-verified. Then update the battlecard, or offer to.

## Workflow

```
- [ ] 1. Load: intel material, brand/ (competitors, positioning, offer, proof, claims, rules, voice)
- [ ] 2. Gate: is there material on this competitor? If not, stop at the ask (rule 2)
- [ ] 3. Ledger: every competitor fact with source, date, status; every gap; every excluded item
- [ ] 4. Win/loss: count it
- [ ] 5. Write: brand/competitors.md (merge) and competitors/<name>-battlecard.md
- [ ] 6. Check: script, then judgment checks
- [ ] 7. Reply in the fixed shape
```

### 1. Load

List the project folder. Read every file the user points to, and any `intel/` or `competitors/` folder. Read `brand/`: `competitors.md`, `positioning.md`, `offer.md`, `proof.md`, `claims.md`, `rules.md`, `voice.md` (spelling and words to avoid apply to the battlecard). Use `confirmed` brand facts as fact, flag `provisional` ones, never state `assumed` ones. Proof marked `named: unconfirmed` or `named: no` is used without the customer's name.

**No `brand/`?** Build the competitor side as usual. Mark the battlecard `Status: provisional (no brand memory)`, write our side (advantages, proof, our feature column) as `TBD`, never invent it, and ask for our proof and win/loss history. Keep the user's own spelling conventions. After the reply, offer to set up brand memory.

### 2. Gate

If there's no material about this competitor beyond its name, reply with what's needed and stop. Don't write a battlecard file unless the user asks for a skeleton, and then every section about them is `TBD` except the win/loss summary. Win/loss reasons describe why buyers chose, not what the competitor offers: they go under When we lose, never under Where they're strong.

### 3. Ledger

Work through [references/sources.md](references/sources.md): what each kind of material can support, the status of each fact, shown versus not shown, rumours, comparison claims, staleness. Keep three lists as you go: facts (with tags), gaps (`TBD`), and excluded items with the reason (these feed **Don't say**).

### 4. Win/loss

From exports or notes only: won and lost totals against this competitor, reason counts, the segment pattern visible in the rows (size, location count, POS, region), the date range and the sample size. Qualify any conclusion drawn from fewer than about ten deals. No data: `TBD`.

### 5. Write

Use the formats in [references/battlecard.md](references/battlecard.md). The battlecard has fixed sections, in order: Recommendation, Who they are, Pricing as shown, Where they're strong, Where we win, When we lose to them and why, Landmines, Objections, Feature comparison, Don't say, Sources, Open. Merge the profile into `brand/competitors.md` (create it if missing), update its `Last reviewed` date, and add a line to `brand/changelog.md` if it exists. Touch no other brand file. Revise your own files in place rather than leaving second versions.

### 6. Check

```bash
python3 scripts/check_intel.py competitors/<name>-battlecard.md --brand brand/ --intel <material folder>
python3 scripts/check_intel.py brand/competitors.md
```

Fix every FAIL and rerun until both pass: a FAIL means rewrite, not hedge. Treat each WARN as a question to answer (stale capture: mark it; "No" in the table: is there a source?). Then the judgment checks:
- **Trace:** pick every number, named fact and superlative in the battlecard and the reply ("the lowest price", "we start with a setup review") and find its source line. Anything without one comes out.
- **Like for like:** a price comparison uses the same scope and billing terms on both sides (monthly against monthly, one location against one location), or says they differ.
- **Fairness:** at least two real strengths where the sources support them; no landmine without a sourced gap; no weakness drawn from a single old review.
- **Our side:** every advantage has proof from brand memory or says TBD; nothing a brand rule restricts.
- **Excluded items:** each one is under Don't say and in the reply, once.

### 7. Reply

```
**Recommendation:** <one line: how to sell against them> (or: Hold, and why, in one line)

**Battlecard:** competitors/<name>-battlecard.md · **Profile:** brand/competitors.md (<what changed>)

**Where they're strong:** <the two or three that matter>
**Where we win:** <the two or three with proof>
**When we lose:** <the pattern, with the sample size>

**Left out:** <each rumour, claim or request left out, one line each, with the honest alternative> (only if any)

**Needed from you:** at most 4 items: missing material, proof, dates
```

- Lead with the recommendation. Keep the reply under about 300 words. Talk to the user in the second person.
- For the no-material case, the reply is: what you can't do without material and why (one or two sentences), what you can already say from what's there, and the exact list of material to send.
- In Guided mode, the reply is the sources found, the outline, what you'd leave out, and the questions.
- Never mention the checker, its levels, the ledger, the mode you're in, tag notation such as `captured: TBD`, or which tools or skills are installed. Say what's missing in plain words ("there's no Ledgerline pricing page in the folder", "the export has no date").

## Keep tools out of the deliverable

Never name this skill, other skills, or their scripts and checks in a reply, report, draft or file the user may pass on: these often go to clients or the public. Describe what was checked, not the tool that checked it. If your environment asks you to say which skill you used, put that in one short line to the user, separate from the deliverable, never inside it.

## What good looks like

A rep can use every line on a call and defend it if the buyer pushes back. A competitor reading the card would find their strengths fairly stated and nothing false. Anyone can see where each fact came from and when it goes stale.

A worked example (a Pipewise battlecard against a fictional forecasting tool) is in [assets/examples/pipewise-forecastly/](assets/examples/pipewise-forecastly/README.md).
