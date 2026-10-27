# 586 public marketing skills, graded

*AI Marketing Bench · library scan · October 2026*

We graded every skill in the four largest public marketing and go-to-market skill libraries on how it's built: can an agent find it, load it, run it anywhere, and trust it? The short version: **most are well built, and almost none are tested.**

## Headline numbers

| | |
|---|---|
| Public skills scanned | **586** across 4 libraries |
| Skills that define any tests | **50 (8.5%)**, all in one library |
| Skills that publish test results | **0** |
| Skills that say when *not* to use them | **11 (2%)** |
| Average build score, excluding evidence | **87.5%** of available points |

## By library

| Library | Skills | Avg score | Grades A / B / C / D | Tests defined | Results published |
|---|---|---|---|---|---|
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | 50 | **81** | 10 / 39 / 1 / 0 | 100% | 0% |
| [OpenClaudia/openclaudia-skills](https://github.com/OpenClaudia/openclaudia-skills) | 78 | 73 | 0 / 67 / 11 / 0 | 0% | 0% |
| [swan-gtm/gtm-skills](https://github.com/swan-gtm/gtm-skills) (gtmskills.com) | 402 | 70 | 0 / 305 / 87 / 10 | 0% | 0% |
| [thatrebeccarae/claude-marketing](https://github.com/thatrebeccarae/claude-marketing) | 56 | 66 | 0 / 30 / 25 / 1 | 0% | 0% |

Corey Haines' library is the best built and the only one that defines tests (a median of 8 per skill). None of the libraries publishes the results of running them.

## What we found

**1. Testing is the gap that matters.** Every library loses most of its points on evidence. A skill can be perfectly formatted and still make an agent's output worse. Without published test results, there's no way to know which skills help. This matches the largest independent benchmark so far (SkillsBench, arXiv 2602.12670). It found curated skills raise task success by about 16 points on average, but 16 of 84 tasks got *worse* with a skill, and self-generated skills gave no benefit.

**2. Routing is mostly good, with one blind spot.** 91% of descriptions say when to use the skill. Only 2% say when *not* to. Research on skill routing finds that agents choosing from names and descriptions alone are far less accurate than agents reading the full skill, so the close-but-wrong cases are where routing fails.

**3. Libraries differ in style:**
- **Swan's** skills are short (median 95 lines) and many-authored. 38 don't say when to use them, and 27 call platform-specific tools by name, which ties them to one product.
- **Rebecca Rae's** are the most capable on paid media, but 14 need package installs, and 15 don't state their triggers.
- **Corey Haines'** are long and thorough (median 307 lines). Half have long reference files with no table of contents.
- **OpenClaudia's** are the most consistent on structure, with no tests.

**4. Safety is clean.** None of the 586 contains the risky patterns we scanned for: piping downloads into a shell, broad deletes, hard-coded secrets, or disabled safety checks.

## Method

Each skill is scored 0–100 by a static scanner (`bench/scan_library.py`, open source in this repo) across five categories:

| Category | Points | Checks |
|---|---|---|
| Routing | 30 | Description present and sized well, says when to use it, written in the third person, names close cases where it shouldn't fire |
| Structure | 20 | Valid name matching its folder, body under 500 lines, internal links resolve, references one level deep with tables of contents |
| Portability | 20 | Portable frontmatter, no hard-wired vendor tools or machine paths, no package installs |
| Evidence | 20 | Tests defined (8+), test results published, worked examples, versioned |
| Safety | 10 | No pipe-to-shell, broad deletes, eval/exec, hard-coded secrets or disabled safety checks |

Grades: A 85+, B 70–84, C 55–69, D 40–54, F under 40.

**What this doesn't measure:** whether a skill improves an agent's output. Only running tests can show that, which is the point of finding 1. The rubric also reflects the [Bench Standard](../../STANDARD.md) this library is built to, so treat the grades as a measure of how a skill is built, not a verdict on its author's expertise. Several of the lower-scoring skills contain excellent domain knowledge.

**Sources:**
- Repositories cloned at these commits: coreyhaines31/marketingskills `1efedbc` (2026-10-08), thatrebeccarae/claude-marketing `a8a63ec` (2026-05-14), OpenClaudia/openclaudia-skills `28bf209` (2026-09-18), swan-gtm/gtm-skills `67abd04` (2026-10-07). One Swan template folder was excluded.
- Full per-skill results are in `results.csv` and `results.json`.
- Skill counts differ from the libraries' own marketing figures because we count SKILL.md files in each repository on the date above.
