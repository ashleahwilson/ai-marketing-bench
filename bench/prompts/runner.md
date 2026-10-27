# Runner prompt templates

`bench/plan.py` fills these in for each run. A runner is a fresh agent that never sees the expectations.

## with-skill

You are testing an Agent Skill. The user's task is in this file. Read only this file from that folder, and don't open evals.json or any other run folder:
{prompt_path}

Then read the skill at {skill_path}/SKILL.md and follow it. Read the files it references and run any scripts it provides, using paths relative to the skill folder. Use no other skills. Don't send, post or schedule anything, don't create tasks, reminders or files outside the folder below (never call spawn_task or any task, chip or session tool), and don't do web research: work only from the facts in the task. Treat this folder as the user's project folder, for example for profile or brand-memory files:
{out_dir}

Write the exact final response you'd give the user to response.md in that folder, along with any files the response refers to. Then reply with two sentences on anything in the skill that was unclear.

## no-skill

Read the user's task in this file. Read only this file from that folder:
{prompt_path}

Complete it the way a skilled practitioner would. Don't load or use any skills. Don't send, post or schedule anything, don't create tasks, reminders or files outside the folder below (never call spawn_task or any task, chip or session tool), and don't do web research: work only from the facts in the task and the files in this folder, which is the user's project folder (files the task mentions are here):
{out_dir}

Write the exact final response you'd give the user to response.md in that folder, along with any files the response refers to. Reply with one sentence confirming it was written.

## comparison-skill

Use the same text as **with-skill**, but point {skill_path} at the public comparison skill. If that skill names platform tools that aren't available, add: "Where it calls for tools that aren't available, do the closest sensible thing yourself."
