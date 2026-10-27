---
name: linkedin-content
description: Writes LinkedIn posts for a named person or a company page from the user's own material (a point of view, a story they tell, a result, notes from a call or talk) as a single post, a short series or a carousel outline. Each post comes with two alternative openings and, when there's a link, a suggested first comment. Reads brand memory for voice, proof, permissions and LinkedIn channel rules, writes a person's post in their first person from known details only, and never invents an anecdote, client, number or quote. Keeps out broetry, engagement bait, hashtag piles, performed candour, manufactured stories and population openers. Use when the user wants something to post on LinkedIn, for example "write a LinkedIn post from my notes", "turn this talk into posts", "a 3-post series for our founder", "outline a carousel", "polish my LinkedIn draft". Saves posts to files that brand-voice-gate can check. Not for posting or scheduling, content calendars, or other platforms.
license: MIT
compatibility: Recommended for large models. On any model it can occasionally add a small connective claim (a reason or process detail) that the material doesn't state, so check the post before posting. See evals/scorecard.json.
metadata:
  version: "1.2.1"
  author: "Ashleah Wilson"
---

# LinkedIn content

Turns what someone actually knows, did or saw into a post that reads as written by them. The material is the post. The skill's job is to find the one point in it, open on its most specific detail, and keep out everything that makes LinkedIn posts read as generated.

## Ground rules

1. **Missing stays missing.** Every name, number, story, quote and claim in a post comes from the user's material or a `confirmed` line in `brand/`. A plausible detail that makes the post feel real is an invention: no made-up client, dialogue, struggle, turning point, feeling or figure. If the user wants a story they haven't supplied, ask for the real one.
2. **Don't widen a fact.** One pilot clinic's result is not what "clinics" see. One customer's quote is not what "clients" say. A figure the user hedged ("I think", "not sure", "?") stays out of the post and goes under "Check before posting".
3. **Brand rules win over the material.** A claim that `rules.md` bans or `claims.md` lists as needing substantiation stays out, even when it's in the person's own notes. Say what was left out and why, in one line each.
4. **Naming needs permission.** If `proof.md` marks a person or company `named: no` or `named: unconfirmed`, no post presented as ready names or tags them. Write the version that can go out now (describe them from recorded facts only, quote their recorded words exactly) and offer a short permission request. A named version, if given, is labelled for use only after they agree. A client named in the material but not recorded in `proof.md` is treated the same way.
5. **A person's post is theirs.** Write in their first person ("I"), using only details about them from `brand/` or the user. Never give them a past, a family or a moment they didn't supply.
6. **No AI tells.** No broetry, engagement bait, hashtag piles, performed candour, manufactured friction or population openers ([references/tells.md](references/tells.md)). If the user asks for one, deliver the clean version and say why in one or two sentences. Push back, never refuse, never lecture.
7. **Never overwrite the user's files.** Posts go in new files under `linkedin/`. Nothing is posted, scheduled or sent.

## Pick the format and mode

| The user wants… | Format |
|---|---|
| A post (the default) | **Single post** |
| "a series", "a week of posts", "one a week from these notes" | **Series:** 2–5 posts, one idea each |
| "a carousel", "slides", "a document post" | **Carousel outline:** numbered slides plus a caption post |

| The user says… | Mode |
|---|---|
| Nothing about process (the default) | **Draft:** the finished post(s), ready to review |
| "guided", "help me pick the angle", "walk me through it", "before you write anything" | **Guided:** offer 2–4 angles, each resting on a fact, ask which one, and stop. Write after they choose |

## Workflow

```
- [ ] 1. Load: the material, brand/, who is posting (a person or the page), the format
- [ ] 2. Fact list: every usable fact, and every one held back
- [ ] 3. Decide: is there a post here? (if not, ask for what's missing)
- [ ] 4. Write: craft.md for structure, tells.md for what to keep out
- [ ] 5. Save to linkedin/ and run scripts/check_post.py
- [ ] 6. Self-check, then reply in the fixed shape
```

### 1. Load

List the project folder first and look for `brand/`, even if the user didn't mention it. Read `BRAND.md`, `voice.md` (the `### LinkedIn` rule under `## By channel`: word limit, person, hashtags, exclamation marks), `rules.md`, `claims.md`, `proof.md`, `offer.md`, and `senders.md` or `positioning.md` if present. Read every file of material the user points to.

**No `brand/` folder?** Write from the material alone, keep the writer's own spelling, use the defaults in [references/craft.md](references/craft.md), and say right after the recommendation that there's no brand memory, so the voice is provisional and brand rules weren't checked. End by offering to set one up (the brand-memory skill).

### 2. Fact list

Before writing, list what the post may rest on (for yourself, not the reply). Mark each fact:
- **usable:** in the material, or `confirmed` in `brand/`
- **held:** banned by a rule, or listed under "Needs substantiation" (for example "3 days, not 3 weeks")
- **needs permission:** a person or company `proof.md` doesn't clear to name
- **unsure:** the user hedged it, or it's a third-party figure with no source
- **missing:** something the post would need that nobody supplied (the client, the result, the person's story)

### 3. Decide

- **Enough to write:** go to step 4.
- **The request depends on something missing** (a client story, a result, a person's background, "make up a story"): don't write it. Reply with "Needs your input first", the three to five questions that would get the real version, and what you can write now from usable facts (a short post, or a structure with `[blanks]` clearly labelled as a template, never saved as a post).
- **Guided mode:** reply with the angles and stop.

### 4. Write

Follow [references/craft.md](references/craft.md): one point per post, open on the most specific usable detail, paragraphs of two to four sentences, end on the practice, the person's own line, a real next step, or a question they'd want answered. Then the two alternative openings (different facts already in the post, nothing new). Check every line against [references/tells.md](references/tells.md).

**Links.** In the body or the first comment is the user's choice. If they don't say, use a suggested first comment and say in one line that it can go in the post instead. Never invent a URL. A link the user or brand memory gives is real, even on a test domain such as `.example`: don't flag it as a placeholder.

### 5. Save and check

Save each post as only its text (no headings, notes or openings) to `linkedin/<slug>.md`, a series as `linkedin/<slug>-1.md`, `-2.md`…, a carousel as `linkedin/<slug>-carousel.md` (`## Slide 1`… then `## Caption`). Then run:

```bash
python3 scripts/check_post.py linkedin/<file>.md [more files] --brand brand/ --sources <each material file> --kind personal|company [--format carousel]
```

For material pasted into the chat, pass it with `--sources-text "<the facts>"`. The check fails over-length posts, too many hashtags or exclamation marks, engagement bait, three one-sentence lines in a row, population openers, never-use words and banned phrases, numbers not in the material or `brand/`, names `proof.md` doesn't clear, and leftover placeholders. **Fix a FAIL by rewriting the post, never by adding a source.** Look at every WARN (performed candour, stock phrasing, links in the body, untraced names or quotes) and fix it unless it's deliberate.

### 6. Self-check, then reply

Answer each line for yourself. Each "no" means fix the post or add a line to "Check before posting". Don't put the checklist in the reply.

```
- [ ] I listed the folder and read brand/ (or said there's none)
- [ ] Every number, name, quote and story detail is in the material or confirmed in brand/; none is widened
- [ ] Held claims and unsure figures are out of the post, and the reply says what was left out and why
- [ ] Nobody brand memory doesn't clear to name is named or tagged in a ready version
- [ ] A person's post is in their first person and gives them nothing they didn't supply
- [ ] Within the LinkedIn rule: word count (as measured), hashtags, exclamation marks, spelling
- [ ] No bait, no broetry, no population opener, no performed candour
- [ ] Two alternative openings per post; a first comment wherever a link isn't in the body
- [ ] Would this person say it out loud to one colleague without performing?
```

## Reply

Lead with the recommendation. Use this shape every time:

```
**Recommendation:** Ready to post | Ready once you <one action> | Needs your input first: <what>
<only if there's no brand/: one line saying the voice is provisional and brand rules weren't checked, and offering to set up brand memory>

### Post   (a series: "### Post 1 of 3: <topic>"; a carousel: "### Slides", then "### Caption")
<the post exactly as saved>

**Other openings**
1. <opening line>
2. <opening line>

**First comment:** <one or two sentences and the link> (only when a link isn't in the body)

**Check before posting:** what to confirm, permissions, links to add. "Nothing" if nothing.
**Left out:** each held, unsure or unconfirmed item, and why, in one line. Omit if nothing.
**Saved to:** `linkedin/<file>.md`
```

- **Ready to post** only when "Check before posting" is "Nothing". If anything must be confirmed or added first, it's **Ready once you <that action>**.
- Name brand-voice-gate only when the user asks to get the post ready for a check or review.

- **Needs your input first** replaces the post sections with **What I need** (three to five questions) and **What I can write now**. Say plainly what brand memory has on the subject (for example "brand memory has nothing about Sam"). Ask about what really happened, never about the made-up premise (not "what did she do in the diner?" but "how did she come to restaurants?").
- **Guided** replaces them with **Angles** (2–4, each with the fact it rests on and where it's recorded, one or two lines each) and one question. No post yet.
- Both stay under 200 words. Save the reply and measure it: `python3 scripts/check_post.py --reply <reply file>`. Over 200 means cut, then measure again.
- Explain a declined request (bait, a held claim, a name) once, in **Left out**, in one line each. Don't repeat it above the post.
- Dates from brand memory stay in: if the date has passed, use the past tense ("launched October 14"), don't drop it.
- Describe brand memory only as it's written (its status, who reviewed it). Don't guess at it.
- Talk to the user in the second person. Never mention the checker, its results, the fact list or source tags. Mention file names only where the user needs to act.

## When the user asks for something the skill won't do

- **"Make it viral", "a client who 10x'd", "make up a story":** say in one sentence that you'd need the real one, ask for it, and offer what you can write now. No lecture about honesty.
- **"Add engagement bait", "more hashtags", "break it into one-liners":** deliver the clean post. One or two sentences on why (it reads as a formula, and a real link or question does the job). Offer the honest equivalent: a link, "message me", a specific question.
- **"Name and tag the customer" without recorded permission:** the ready version leaves the name out; offer a two-line message asking their OK, and the named version for after they say yes.
- **"Use this claim anyway":** if a brand rule bans it, keep it out and say the rule. If it only needs a source, write it only if the user supplies one now.

## Hand-off

Each `linkedin/*.md` file holds only post text (or slides and caption), ready to paste or to check with brand-voice-gate, which reads it as a LinkedIn draft. The alternative openings, first comment and checks stay in the reply.

## Keep tools out of the deliverable

Never name this skill, other skills, or their scripts and checks in a reply, report, draft or file the user may pass on: these often go to clients or the public. Describe what was checked, not the tool that checked it. If your environment asks you to say which skill you used, put that in one short line to the user, separate from the deliverable, never inside it.

## What good looks like

The person reads the post and recognises their own story, said the way they'd say it, with nothing they'd have to explain if a colleague asked "did that happen?". Every number traces to their notes or to `brand/`.

A worked example (a Tallyhouse founder's post from interview notes) is in [assets/examples/tallyhouse/](assets/examples/tallyhouse/README.md).
