#!/usr/bin/env python3
"""Mechanical helpers for an AI workload map. Standard library only.

Usage:
    python3 scripts/workload_map.py library [--root PATH]
        Lists the skills in the library (packs.json + each skill's description), marking which exist.
    python3 scripts/workload_map.py weekly FILE.csv
        Converts a time log or survey to hours per week. Finds the hours column and an optional period
        column (day, week, month, quarter, year). Conversions: day x 5 (working days), month x 12/52,
        quarter x 4/52, year x 1/52. Prints one line per row.
    python3 scripts/workload_map.py hours MAP.csv [--rates ai-assisted=0.3,agent-run-review=0.6,stop-doing=1] [--write]
        Computes hours freed per task and in total, ONLY from rows with hours_per_week. keep-human is always 0.
        --write fills saving_rate and hours_freed_per_week in MAP.csv.
    python3 scripts/workload_map.py check MAP.csv [--md MAP.md]
        Checks the map: columns, categories, sign-off on spend, legal, relationship and HR tasks, privacy,
        hours arithmetic, rollout order, and (with --md) required sections and banned content.

Exit code: 0 clean, 1 if any FAIL, 2 on bad input.
"""

import csv
import json
import os
import re
import sys

COLUMNS = ["task_id", "task", "owner", "source", "category", "reason", "human_signoff", "signoff_reason",
           "privacy_flag", "library_skills", "data_access", "guardrails", "hours_per_week", "saving_rate",
           "hours_freed_per_week", "rollout_phase"]
CATEGORIES = ["keep-human", "ai-assisted", "agent-run-review", "stop-doing"]
DEFAULT_RATES = {"keep-human": 0.0, "ai-assisted": 0.3, "agent-run-review": 0.6, "stop-doing": 1.0}
SELF = os.path.basename(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
PHASES = {"30", "60", "90", "later", "none"}
PER_WEEK = {"day": 5.0, "daily": 5.0, "week": 1.0, "weekly": 1.0, "wk": 1.0, "month": 12 / 52, "monthly": 12 / 52,
            "quarter": 4 / 52, "quarterly": 4 / 52, "year": 1 / 52, "yearly": 1 / 52, "annual": 1 / 52,
            "annually": 1 / 52, "biweekly": 0.5, "fortnight": 0.5}

TRIGGERS = {
    "spend": r"\b(budget|budgets|bid|bids|spend|invoice|purchase|sponsorship|media buy|pricing change|refund)\b",
    "legal": r"\b(legal|contract|contracts|claims review|compliance|terms|licen[cs]e agreement|regulat\w*)\b",
    "relationship": r"\b(client|clients|customer|customers|complain\w*|partner|partners|press|journalist|escalat\w*|"
                    r"reference request|reviews? repl\w*|reply to|replies to|negotiat\w*)\b",
    "hr": r"\b(performance|appraisal|check-ins?|hiring|interview candidates|salary|salaries|compensation|"
          r"disciplin\w*|promotion|termination|one-on-one|1:1)\b",
    "personal": r"\b(patient|patients|health|personal data|slack messages|employee data|medical|ssn|sin number)\b",
    "approval": r"\b(approve|approves|approval|approvals|sign off|sign-off|signoff|negotiat\w*)\b",
}
BANNED_MD = [
    (r"\bFTEs?\b", "FTE conversion: report hours, never full-time equivalents"),
    (r"full[- ]time equivalent", "FTE conversion: report hours, never full-time equivalents"),
    (r"headcount (reduction|cut|savings?)", "headcount reduction language"),
    (r"(reduce|cut|lower|trim) (the )?headcount", "headcount reduction language"),
    (r"\b(roles?|positions?|people|jobs?|seats?) (you |we )?(can|could) (be )?(cut|eliminat\w*|remov\w*|let go)", "names roles to cut"),
    (r"\b(eliminate|cut|remove) (\w+ )?(roles?|positions?|jobs?)\b", "names roles to cut"),
    (r"equivalent (of|to) (\d+(\.\d+)?|one|two|three|four|five|half an?) (people|person|employees?|hires?|heads?)", "headcount equivalent"),
    (r"workload_map\.py|SKILL\.md|\bthe script\b|\bthe checker\b", "skill internals in a deliverable"),
    (r"\bTODO\b|<placeholder>|\bXX+\b|lorem ipsum", "placeholder left in"),
]
MD_SECTIONS = ["Recommendation", "The map", "Human sign-off", "Data and access", "Risks and guardrails",
               "30/60/90", "Capacity", "Open questions"]


def num(v):
    try:
        return float(str(v).strip())
    except (TypeError, ValueError):
        return None


def read_csv(path):
    with open(path, newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
        return rows, (rows[0].keys() if rows else [])


def find_root(start):
    d = os.path.abspath(start)
    for _ in range(4):
        if os.path.exists(os.path.join(d, "packs.json")):
            return d
        d = os.path.dirname(d)
    return None


def first_sentence(text):
    m = re.match(r"(.+?\.)(\s|$)", text.strip())
    return (m.group(1) if m else text.strip())[:300]


def description(skill_md):
    text = open(skill_md, encoding="utf-8").read()
    m = re.search(r"^description:\s*(.+)$", text, re.M)
    return m.group(1).strip().strip('"\'') if m else ""


def cmd_library(args):
    root = None
    if "--root" in args:
        root = args[args.index("--root") + 1]
    root = root or find_root(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
    if not root:
        print("LIBRARY INDEX NOT FOUND: use references/library.md")
        return 0
    packs = json.load(open(os.path.join(root, "packs.json"), encoding="utf-8")).get("packs", [])
    seen = set()
    for p in packs:
        print(f"## {p.get('title', p.get('name'))}")
        for s in p.get("skills", []):
            seen.add(s)
            if s == SELF:
                continue
            md = os.path.join(root, "skills", s, "SKILL.md")
            if os.path.exists(md):
                print(f"- {s}: {first_sentence(description(md))}")
            else:
                print(f"- {s}: NOT BUILT YET (listed in packs.json only; don't recommend it)")
    extra = sorted(d for d in os.listdir(os.path.join(root, "skills"))
                   if d not in seen and d != SELF and os.path.exists(os.path.join(root, "skills", d, "SKILL.md")))
    if extra:
        print("## Not in a pack")
        for s in extra:
            print(f"- {s}: {first_sentence(description(os.path.join(root, 'skills', s, 'SKILL.md')))}")
    return 0


def cmd_weekly(args):
    rows, cols = read_csv(args[0])
    cols = list(cols)
    hcol = next((c for c in cols if re.search(r"hour|hrs|time", c, re.I)), None)
    pcol = next((c for c in cols if re.search(r"period|per|frequency|unit", c, re.I) and c != hcol), None)
    if not hcol:
        print("NO HOURS COLUMN FOUND: no time data, so no hours figure")
        return 0
    print(f"hours column: {hcol}; period column: {pcol or '(none: read as per week)'}")
    total, missing = 0.0, 0
    for i, r in enumerate(rows, 1):
        h = num(r.get(hcol))
        label = " | ".join(str(r[c]) for c in cols[:3] if c not in (hcol, pcol))
        if h is None:
            missing += 1
            print(f"row {i}: {label}: NO HOURS")
            continue
        period = (r.get(pcol) or "week").strip().lower() if pcol else "week"
        factor = PER_WEEK.get(period)
        if factor is None:
            print(f"row {i}: {label}: UNKNOWN PERIOD '{period}': ask the user")
            continue
        wk = h * factor
        total += wk
        note = "" if factor == 1 else f" (from {h:g} per {period})"
        print(f"row {i}: {label}: {wk:.2f} h/week{note}")
    print(f"total logged: {total:.2f} h/week; rows without hours: {missing}")
    return 0


def parse_rates(spec):
    rates = dict(DEFAULT_RATES)
    if spec:
        for part in spec.split(","):
            k, v = part.split("=")
            k = k.strip()
            if k not in CATEGORIES:
                raise SystemExit(f"unknown category in --rates: {k}")
            rates[k] = float(v.rstrip("%")) / (100 if v.strip().endswith("%") or float(v.rstrip("%")) > 1 else 1)
    rates["keep-human"] = 0.0
    return rates


def cmd_hours(args):
    path = args[0]
    spec = args[args.index("--rates") + 1] if "--rates" in args else None
    rates = parse_rates(spec)
    rows, cols = read_csv(path)
    with_h = [r for r in rows if num(r.get("hours_per_week")) is not None]
    if not with_h:
        print("NO TIME DATA: state no hours figure anywhere. Say what to collect instead.")
        return 0
    by_cat, by_owner, logged, freed = {}, {}, 0.0, 0.0
    for r in rows:
        h = num(r.get("hours_per_week"))
        cat = (r.get("category") or "").strip()
        if h is None:
            print(f"{r.get('task_id')}: {r.get('task')}: no hours (excluded)")
            if "--write" in args:
                r["saving_rate"], r["hours_freed_per_week"] = "", ""
            continue
        rate = rates.get(cat)
        if rate is None:
            print(f"{r.get('task_id')}: unknown category '{cat}'")
            continue
        f = round(h * rate, 2)
        logged += h
        freed += f
        by_cat[cat] = by_cat.get(cat, 0) + f
        by_owner[r.get("owner", "")] = by_owner.get(r.get("owner", ""), 0) + f
        print(f"{r.get('task_id')}: {r.get('task')}: {h:g} h/week x {rate:g} = {f:g} freed")
        if "--write" in args:
            r["saving_rate"], r["hours_freed_per_week"] = f"{rate:g}", f"{f:g}"
    print(f"rates used: " + ", ".join(f"{k} {v:g}" for k, v in rates.items()))
    print(f"coverage: {len(with_h)} of {len(rows)} tasks have hours; {logged:.2f} h/week logged")
    for k in CATEGORIES:
        if k in by_cat:
            print(f"freed by category: {k}: {by_cat[k]:.2f}")
    for k, v in by_owner.items():
        print(f"freed by owner: {k}: {v:.2f}")
    print(f"TOTAL FREED: {freed:.2f} h/week (an estimate from assumed rates, not a measurement)")
    if "--write" in args:
        with open(path, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=list(cols))
            w.writeheader()
            w.writerows(rows)
        print(f"wrote saving_rate and hours_freed_per_week to {path}")
    return 0


def cmd_check(args):
    path = args[0]
    md = args[args.index("--md") + 1] if "--md" in args else None
    rows, cols = read_csv(path)
    res = []
    add = lambda lvl, msg: res.append((lvl, msg))
    missing = [c for c in COLUMNS if c not in cols]
    if missing:
        add("FAIL", f"missing columns: {', '.join(missing)}")
    any_hours = False
    for r in rows:
        tid = r.get("task_id") or "?"
        task = (r.get("task") or "").lower()
        text = task + " " + (r.get("reason") or "").lower()
        cat = (r.get("category") or "").strip()
        sign = (r.get("human_signoff") or "").strip().lower()
        priv = (r.get("privacy_flag") or "").strip().lower()
        phase = (r.get("rollout_phase") or "").strip().lower()
        hit = {k for k, pat in TRIGGERS.items() if re.search(pat, task)}
        if cat not in CATEGORIES:
            add("FAIL", f"{tid}: category '{cat}' is not one of {', '.join(CATEGORIES)}")
        if sign not in ("yes", "no"):
            add("FAIL", f"{tid}: human_signoff must be yes or no")
        if priv not in ("yes", "no"):
            add("FAIL", f"{tid}: privacy_flag must be yes or no")
        if phase not in PHASES:
            add("FAIL", f"{tid}: rollout_phase must be one of 30, 60, 90, later, none")
        if hit & {"spend", "legal", "relationship", "hr", "personal", "approval"} and sign != "yes" and cat != "stop-doing":
            add("FAIL", f"{tid}: looks like {', '.join(sorted(hit))}: needs human_signoff yes (or say why not)")
        if hit & {"hr", "personal"}:
            if cat != "keep-human":
                add("FAIL", f"{tid}: HR or personal data task must be keep-human")
            if priv != "yes":
                add("FAIL", f"{tid}: HR or personal data task needs privacy_flag yes")
        if "approval" in hit and cat == "agent-run-review":
            add("FAIL", f"{tid}: an approval or negotiation can't be agent-run; the agent can prepare it, a person decides")
        if cat == "agent-run-review" and hit & {"spend", "legal"}:
            add("WARN", f"{tid}: agent-run on a spend or legal task: confirm the agent only prepares and a named person approves")
        if cat == "keep-human" and phase in {"30", "60", "90"}:
            add("WARN", f"{tid}: keep-human task has a rollout phase; use none")
        if phase == "30" and (priv == "yes" or hit & {"hr", "personal", "legal", "approval"}):
            add("FAIL", f"{tid}: first 30 days should be low-risk work, not legal, approval or personal-data tasks")
        if phase == "30" and cat in ("ai-assisted", "agent-run-review") and hit & {"relationship", "spend"}:
            add("WARN", f"{tid}: client-facing or spend task in the first 30 days: start with internal work")
        if cat == "stop-doing" and not (r.get("reason") or "").strip():
            add("FAIL", f"{tid}: stop-doing needs the evidence in reason")
        h, f, rate = num(r.get("hours_per_week")), num(r.get("hours_freed_per_week")), num(r.get("saving_rate"))
        if h is not None:
            any_hours = True
        if f is not None and h is None:
            add("FAIL", f"{tid}: hours freed with no logged hours: remove it")
        if f is not None and h is not None and rate is not None and abs(h * rate - f) > 0.06:
            add("FAIL", f"{tid}: hours freed {f:g} doesn't equal {h:g} x {rate:g}")
        if cat == "keep-human" and f:
            add("FAIL", f"{tid}: keep-human frees no hours")
        if cat in ("ai-assisted", "agent-run-review") and not (r.get("data_access") or "").strip():
            add("WARN", f"{tid}: AI task with no data and access noted")
    if md:
        text = open(md, encoding="utf-8").read()
        for s in MD_SECTIONS:
            if not re.search(rf"^#+ .*{re.escape(s)}", text, re.M | re.I):
                add("FAIL", f"{os.path.basename(md)}: missing section '{s}'")
        for pat, why in BANNED_MD:
            m = re.search(pat, text, re.I)
            if m:
                add("FAIL", f"{os.path.basename(md)}: {why}: '{m.group(0)}'")
        if not any_hours:
            m = re.search(r"\b\d+(\.\d+)?\s*(hours?|hrs?|h)(/|\s)(a |per )?(week|wk|month)", text, re.I)
            if m:
                add("FAIL", f"{os.path.basename(md)}: an hours figure with no time data: '{m.group(0)}'")
    for lvl, msg in res:
        print(f"{lvl}: {msg}")
    fails = sum(1 for lvl, _ in res if lvl == "FAIL")
    print(f"{'FAIL' if fails else 'PASS'}: {len(rows)} tasks, {fails} fail, {sum(1 for l, _ in res if l == 'WARN')} warn")
    return 1 if fails else 0


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("library", "weekly", "hours", "check"):
        print(__doc__)
        return 2
    cmd, args = sys.argv[1], sys.argv[2:]
    if cmd != "library" and (not args or not os.path.exists(args[0])):
        print(f"file not found: {args[0] if args else '(none)'}")
        return 2
    return {"library": cmd_library, "weekly": cmd_weekly, "hours": cmd_hours, "check": cmd_check}[cmd](args)


if __name__ == "__main__":
    sys.exit(main())
