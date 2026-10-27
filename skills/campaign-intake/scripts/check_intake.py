#!/usr/bin/env python3
"""Validate a campaign intake file (references/intake-format.md). Standard library only.

Usage:
    python3 scripts/check_intake.py intake/<slug>.md --today 2026-11-02 [--brand brand/] [--request requests/email.md ...]

Checks:
    FAIL   a required field missing or blank; a placeholder (<...>, YYYY, bare TBD); an unparseable date; a deadline or
           key date not after --today (unless the key date is labelled "(past)"); a budget that isn't digits, a digit
           range, none, unknown, assumed or open; an unknown status; a route item outside the vocabulary; more than four
           questions; an open field while Status is ready; a phrase brand memory holds or bans written into the fields;
           an internal tool name in the file
    WARN   the route's rough lead-time floor exceeds the working days available while Status isn't scoped down or hold;
           conflicts listed while Status is ready; a key date in the past (labelled)
    INFO   working days available and the rough floor
    CLAIM  phrases in the request that brand memory holds, bans or can't support, quotes whose naming is unconfirmed,
           superlatives, percentages and certification claims: judge each one

Exit code: 0 if no FAIL, 1 if any FAIL, 2 on bad input.
"""

import argparse
import datetime
import os
import re
import sys

REQUIRED = ["Campaign", "Requested by", "Objective", "Business result", "Audience", "Brand audience match", "Offer",
            "CTA", "Channels", "Deadline", "Key dates", "Budget", "Assets existing", "Assets needed", "Approvals",
            "Decision owner", "Success metric", "Measured by", "Route"]
STATUSES = ["ready", "needs answers", "scoped down: needs approval", "hold"]
ROUTE_TERMS = ["content brief", "email sequence", "linkedin posts", "google ads campaign", "meta ads campaign", "outreach",
               "claims review", "disclosure check", "accessibility review", "voice check", "qa before publish",
               "brand memory update", "agency brief", "approval routing", "prospect list", "icp", "competitor profile",
               "other:"]
# Planning floors in working days (references/judgment.md). Checks and briefs run before or after builds; builds overlap.
LEAD = {"content brief": 1, "email sequence": 3, "linkedin posts": 2, "google ads campaign": 3, "meta ads campaign": 3,
        "outreach": 2, "agency brief": 1, "prospect list": 2}
OTHER_LEAD = [(r"video", 10), (r"webinar", 10), (r"landing page", 5), (r"print", 10), (r"linkedin ads", 3)]
INTERNAL = ["campaign-intake", "content-brief", "email-sequence", "linkedin-content", "google-ads-build",
            "meta-ads-build", "claims-review", "disclosure-check", "brand-memory", "brand-voice-gate", "content-qa-gate",
            "reach-out", "check_intake", "approval-routing", "agency-brief", "accessibility-review", "build-list",
            "competitor-intel", "SKILL.md", "packs.json", "the checker", "lead-time table", "lead time table",
            "judgment.md", "intake-format.md"]
MARKERS = ("unknown", "assumed", "open", "none")
ISO = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")
SUPERLATIVE = re.compile(r"#\s?1\b|\bnumber one\b|\b(cheapest|best|leading|fastest|the only|most trusted|largest|lowest)\b", re.I)
PERCENT = re.compile(r"\b\d+(\.\d+)?\s?%")
CERT = re.compile(r"\b(HIPAA|GDPR|SOC ?2|PCI|ISO ?27001)\b[^.\n]{0,30}\b(certified|compliant|approved|accredited)\b|"
                  r"\b(certified|compliant|approved|accredited)\b[^.\n]{0,30}\b(HIPAA|GDPR|SOC ?2|PCI|ISO ?27001)\b", re.I)
QUOTED = re.compile(r"[\"“]([^\"”]{4,120})[\"”]")


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def sections(text):
    out, name = {"_head": []}, "_head"
    for line in text.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            name = m.group(1).strip().lower()
            out[name] = []
        else:
            out[name].append(line)
    return out


def parse_fields(lines):
    fields = {}
    for line in lines:
        m = re.match(r"^\s*[-*]\s+([A-Za-z ]+?):\s*(.*)$", line)
        if m:
            fields[m.group(1).strip()] = m.group(2).strip()
    return fields


def parse_date(y, mo, d):
    try:
        return datetime.date(int(y), int(mo), int(d))
    except ValueError:
        return None


def working_days(start, end):
    days, d = 0, start
    while d < end:
        d += datetime.timedelta(days=1)
        if d.weekday() < 5:
            days += 1
    return days


def marked(value):
    return value.lower().startswith(MARKERS)


def brand_phrases(brand):
    """Phrases brand memory holds or bans, with the line they come from."""
    held = []
    for fname in ("rules.md", "claims.md"):
        p = os.path.join(brand, fname)
        if not os.path.exists(p):
            continue
        section = ""
        for line in read(p).splitlines():
            if line.startswith("## "):
                section = line[3:].strip().lower()
                continue
            if fname == "claims.md" and "approved" in section:
                continue
            for q in QUOTED.findall(line):
                held.append((q.strip(), f"brand/{fname}: {line.strip()[:140]}"))
    return held


def unnamed_proof(brand):
    out = []
    p = os.path.join(brand, "proof.md")
    if not os.path.exists(p):
        return out
    for line in read(p).splitlines():
        if re.search(r"named:\s*(unconfirmed|no)\b", line, re.I):
            names = re.findall(r"\b([A-Z][a-z]+(?:\s[A-Z][a-z]+)+)\b", line.split("[source")[0])
            out.append((names, line.strip()[:160]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("intake")
    ap.add_argument("--today", help="YYYY-MM-DD (default: the system date)")
    ap.add_argument("--brand", help="brand/ folder")
    ap.add_argument("--request", nargs="*", default=[], help="the original request files")
    a = ap.parse_args()
    if not os.path.exists(a.intake):
        print(f"FAIL  file not found: {a.intake}")
        sys.exit(2)
    try:
        today = datetime.date.fromisoformat(a.today) if a.today else datetime.date.today()
    except ValueError:
        print("FAIL  --today must be YYYY-MM-DD")
        sys.exit(2)

    text = read(a.intake)
    secs = sections(text)
    head = "\n".join(secs["_head"])
    fails, warns, infos, claims = [], [], [], []

    m = re.search(r"^Status:\s*(.+)$", head, re.M)
    status = m.group(1).strip().lower() if m else ""
    if status not in STATUSES:
        fails.append(f"Status '{status or 'missing'}' is not one of: {', '.join(STATUSES)}")
    if not re.search(r"^Today:\s*\d{4}-\d{2}-\d{2}", head, re.M):
        fails.append("header needs 'Today: YYYY-MM-DD'")

    fields = parse_fields(secs.get("fields", []))
    if "fields" not in secs:
        fails.append("no '## Fields' section")
    for f in REQUIRED:
        if f not in fields:
            fails.append(f"field missing: {f} (write 'unknown: <what> (ask: <who>)' if it isn't known)")
        elif not fields[f]:
            fails.append(f"field blank: {f}")

    for f, v in fields.items():
        if re.search(r"<[^>]{1,40}>|YYYY|\bTBD\b(?!:)", v):
            fails.append(f"{f}: placeholder left in '{v[:60]}'")
        if v.lower().startswith("open") and status == "ready":
            fails.append(f"{f} is open but Status is ready")

    # Dates
    dl = fields.get("Deadline", "")
    deadline = None
    if dl and not marked(dl):
        mm = ISO.search(dl)
        deadline = parse_date(*mm.groups()) if mm else None
        if not deadline:
            fails.append(f"Deadline '{dl}' is not a YYYY-MM-DD date (or unknown/assumed)")
        elif deadline <= today:
            fails.append(f"Deadline {deadline} is not after today ({today})")
    elif dl.lower().startswith("assumed"):
        mm = ISO.search(dl)
        deadline = parse_date(*mm.groups()) if mm else None
    kd = fields.get("Key dates", "")
    if kd and not marked(kd):
        for part in [p.strip() for p in kd.split(";") if p.strip()]:
            mm = ISO.search(part)
            if not mm:
                fails.append(f"Key dates: '{part}' has no YYYY-MM-DD date")
                continue
            d = parse_date(*mm.groups())
            if not d:
                fails.append(f"Key dates: '{part}' is not a real date")
            elif d <= today and "(past" not in part.lower():
                fails.append(f"Key dates: {d} is not after today ({today}); label it '(past)' and say what it means")
            elif d <= today:
                warns.append(f"Key dates: {d} is in the past; make sure Risks or Questions say what that means")
    for f in ("Success metric", "Business result"):
        for mm in ISO.finditer(fields.get(f, "")):
            d = parse_date(*mm.groups())
            if d is None:
                fails.append(f"{f}: '{mm.group(0)}' is not a real date")
            elif d <= today:
                fails.append(f"{f}: {d} is not after today ({today})")

    # Budget
    b = fields.get("Budget", "")
    if b and not marked(b):
        if not re.match(r"^\d+(\.\d+)?(\s*-\s*\d+(\.\d+)?)?(\s|$)", b):
            fails.append(f"Budget '{b[:50]}' must start with digits or a digit range (no $, k or commas), or be none/unknown/assumed/open")
    elif b.lower().startswith("assumed") and not re.search(r"\d", b):
        fails.append("Budget is assumed but has no number")

    # Route
    route = fields.get("Route", "")
    items = [r.strip() for r in route.split(";") if r.strip()] if route and not marked(route) else []
    for it in items:
        if not any(it.lower().startswith(t) for t in ROUTE_TERMS):
            fails.append(f"Route item '{it[:50]}' doesn't start with a route term (use 'other: <work>' for anything else)")

    # Feasibility floor
    if deadline and deadline > today and items:
        avail = working_days(today, deadline)
        builds, pre, notes = [], 0, []
        for it in items:
            low = it.lower()
            if low.startswith("content brief"):
                pre = max(pre, 1)
            elif low.startswith("claims review") or low.startswith("disclosure check"):
                pre = max(pre, 2)
            elif low.startswith("other:"):
                days = next((d for pat, d in OTHER_LEAD if re.search(pat, low)), None)
                if days is None:
                    notes.append(f"no default for '{it[:40]}'")
                else:
                    builds.append(days)
            else:
                term = next((t for t in LEAD if low.startswith(t)), None)
                if term:
                    days = LEAD[term]
                    if term == "email sequence" and re.search(r"\b([4-9]|1\d)\b", low):
                        days = 5
                    if term == "meta ads campaign" and "video" in low:
                        days = 10
                    builds.append(days)
        appr = fields.get("Approvals", "")
        approval = 2 if appr and not marked(appr) else 0
        floor = pre + (max(builds) if builds else 0) + approval
        infos.append(f"{avail} working days from {today} to {deadline} (public holidays not subtracted); "
                     f"rough floor for this route: {floor} (brief/claims {pre} + longest build {max(builds) if builds else 0} + approval {approval})"
                     + (f"; {', '.join(notes)}" if notes else ""))
        if floor > avail and not status.startswith(("scoped down", "hold")):
            warns.append(f"the route needs about {floor} working days but {avail} are available: say so, and scope down")

    # Questions and conflicts
    q = [l for l in secs.get("questions", []) if re.match(r"^\s*\d+[.)]\s", l)]
    if len(q) > 4:
        fails.append(f"{len(q)} questions; ask at most four, and record the rest as assumptions")
    conf = [l for l in secs.get("conflicts", []) if re.match(r"^\s*\d+[.)]\s", l)]
    if conf and status == "ready" and not re.search(r"resolved", "\n".join(secs.get("conflicts", [])), re.I):
        warns.append("conflicts are listed but Status is ready: is each one resolved?")

    # Internal names
    for name in INTERNAL:
        if name.lower() in text.lower():
            fails.append(f"internal name '{name}' appears in the intake; describe the work in plain words")

    # Brand memory phrases
    if a.brand and os.path.isdir(a.brand):
        field_text = "\n".join(f"{k}: {v}" for k, v in fields.items() if not v.lower().startswith("open"))
        held = brand_phrases(a.brand)
        for phrase, src in held:
            if phrase.lower() in field_text.lower():
                fails.append(f"'{phrase}' is in the fields, but brand memory holds or bans it ({src})")
        reqtext = "\n".join(read(r) for r in a.request if os.path.exists(r))
        for phrase, src in held:
            if reqtext and phrase.lower() in reqtext.lower():
                claims.append(f"request uses '{phrase}': {src}")
        for names, line in unnamed_proof(a.brand):
            for n in names:
                if reqtext and re.search(r"\b" + re.escape(n.split()[0]) + r"\b", reqtext, re.I):
                    claims.append(f"request mentions {n}: naming not cleared ({line})")
                    break
    elif a.brand:
        infos.append(f"no brand folder at {a.brand}: mark the intake provisional")
    reqtext = "\n".join(read(r) for r in a.request if os.path.exists(r))
    for line in reqtext.splitlines():
        if SUPERLATIVE.search(line):
            claims.append(f"superlative or comparison: '{line.strip()[:100]}'")
        if PERCENT.search(line):
            claims.append(f"percentage: '{line.strip()[:100]}' (a claim needs a source; a discount or target is the requester's)")
        if CERT.search(line) or re.search(r"\b(HIPAA|GDPR|SOC ?2)\b", line):
            claims.append(f"compliance or certification wording: '{line.strip()[:100]}' (legal review)")

    for level, rows in (("FAIL", fails), ("WARN", warns), ("INFO", infos), ("CLAIM", claims)):
        for r in rows:
            print(f"{level:<6}{r}")
    print(f"\n{len(fails)} FAIL, {len(warns)} WARN, {len(claims)} CLAIM")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
