# Effectiveness pilot: do well-built public skills beat no skill?

*AI Marketing Bench · October 2026 · pilot, not a verdict*

The library scan grades how skills are built. This pilot asks the question the scan can't answer: **does the skill make the deliverable better?**

We took three skills from the best-built public library ([coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills), commit `1efedbc`) and ran **the author's own tests**, evals 1–3 for each skill, with the skill and without it. A separate grader scored every assertion and labelled each one:
- **Process:** did a skill-specific step happen? A run without the skill can't know these steps.
- **Outcome:** is what the user receives good?

The outcome-only comparison is the fair one.

## Results (Claude Haiku, 18 runs, blind grading)

| Skill | With skill (all) | No skill (all) | **With skill (outcome)** | **No skill (outcome)** |
|---|---|---|---|---|
| marketing-plan | 17/25 | 8/25 | **11/12 (92%)** | **7/12 (58%)** |
| copywriting | 20/25 | 15/25 | **16/20 (80%)** | **13/20 (65%)** |
| competitors | 15/24 | 15/24 | **11/19 (58%)** | **14/19 (74%)** |
| **All** | 52/74 (70%) | 38/74 (51%) | **38/51 (75%)** | **34/51 (67%)** |

Most of the headline gap comes from process assertions. On outcomes, the skills add 8 points overall, and one skill made outcomes worse.

## What it looked like

- **marketing-plan** helps where it counts: honest budget maths, a ranked list of open decisions, and a clear diagnosis of the binding constraint. But it's built for a long interactive engagement. In a single pass it produced a 40KB plan with a 139-row idea bank that was mostly filler, against a 9KB plan without the skill that a team could use as written.
- **copywriting** gives a modest, real edge: alternatives with rationale, annotations, and SEO meta. It's also more placeholder-heavy, and on the pricing-page test it produced less finished copy than no skill.
- **competitors** made two of three pages worse in this setup. Its evidence discipline turned well-known public facts into `[VERIFY]` cells, so a HubSpot vs Salesforce page came back almost entirely placeholders. The no-skill pages were usable drafts, though one invented product features.

## Limits

- **Small sample:** 3 evals per skill, one model (Haiku), one run per configuration. Treat the direction as a signal, not a measurement.
- **No web research.** Runners were barred from it so the comparison stayed controlled. That handicaps **competitors**, whose design assumes research. A rerun with web access is needed before drawing conclusions about that skill.
- **Some assertions couldn't be passed by either run.** One test refers to an audit that wasn't attached, others need live competitor data, and two check whether the skill triggers, which a forced load can't test. All of these were flagged during grading.

The broader lesson matches SkillsBench (arXiv 2602.12670): **even well-built skills don't reliably beat no skill, and the only way to know is to test.**
