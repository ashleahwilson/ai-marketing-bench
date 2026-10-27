#!/usr/bin/env python3
"""Work out who has to approve a marketing piece, in what order and by when, and where it stands.

Usage:
    python3 scripts/route.py route <content> --brand brand/ --type "<content type>"
        [--approvals approvals.md] [--requester "Name"] [--requested YYYY-MM-DD] [--go-live YYYY-MM-DD]
        [--spend 18000] [--channel meta] [--audience "..."] [--region "..."] [--brand-change]
        [--reviews reviews/ | --reviews a.md b.md]

    python3 scripts/route.py check <name>-route.md <content> (same options as route)

route prints: the approval rule used, the requester, trigger candidates found in the content (with the line),
brand-rule breaches, customer-consent records, spend thresholds, the route (steps, who, checks, SLA, due date),
each sign-off and whether it counts for this version, blockers, the status line and the go-live check.
Trigger candidates are suggestions: the agent judges each one.

check fails a route file that says Approved when the sign-offs don't support it, that leaves out a required
approver, that counts the requester's own sign-off when the rule forbids it, that is missing a required
section, or that mentions how it was produced.

Standard library only.
"""

import argparse
import datetime as dt
import os
import re
import sys

ROLE_WORDS = ["subject expert", "editor", "legal", "compliance", "marketing", "approver", "finance",
              "brand owner", "brand", "founder", "product", "reviewer"]


def norm(s):
    s = (s or "").replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", s).strip().lower()


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


# ---------- matrix ----------

def pairs(s):
    out = []
    for item in [x.strip() for x in (s or "").split(",") if x.strip()]:
        role, _, name = item.partition("=")
        out.append((role.strip().lower(), name.strip() or "TBD"))
    return out


def parse_fields(line):
    line = re.sub(r"\[source:[^\]]*\]", "", line).strip().lstrip("-* ").strip()
    fields = {}
    for part in line.split(" | "):
        if ":" in part:
            k, v = part.split(":", 1)
            fields[k.strip().lower()] = v.strip()
    return fields


def parse_matrix(brand, approvals_file):
    src, lines = None, []
    if approvals_file and os.path.isfile(approvals_file):
        src = approvals_file
        lines = read(approvals_file).splitlines()
    elif brand and os.path.isfile(os.path.join(brand, "rules.md")):
        text = read(os.path.join(brand, "rules.md"))
        m = re.search(r"^## Approvals\s*$(.*?)(?=^## |\Z)", text, re.S | re.M)
        if m:
            src = os.path.join(brand, "rules.md")
            lines = m.group(1).splitlines()
    types, triggers = [], []
    for l in lines:
        if "type:" in l and "sign-off:" in l:
            f = parse_fields(l)
            sla = {}
            for role, val in pairs(f.get("sla")):
                n = re.search(r"\d+", val)
                if n:
                    sla[role] = int(n.group())
            order = []
            if f.get("order"):
                for step in f["order"].split(">"):
                    order.append([r.strip().lower() for r in step.split(",") if r.strip()])
            types.append({"type": f.get("type", "").lower(), "signoff": pairs(f.get("sign-off")),
                          "backup": pairs(f.get("backup")), "conflicts": f.get("conflicts", ""),
                          "order": order, "sla": sla,
                          "self": norm(f.get("self-approval", "")) or "not set"})
        elif re.match(r"^\s*[-*]?\s*trigger:", l):
            f = parse_fields(l)
            n = re.search(r"\d+", f.get("sla", ""))
            triggers.append({"trigger": norm(f.get("trigger")), "adds": f.get("adds", ""),
                             "checks": f.get("checks", ""), "sla": int(n.group()) if n else None,
                             "before": norm(f.get("before", "approver"))})
    return src, types, triggers


def pick_type(types, ctype):
    t = norm(ctype)
    for r in types:
        if t and (r["type"] == t or r["type"].rstrip("s") == t.rstrip("s")):
            return r, False
    d = next((r for r in types if r["type"] == "default"), None)
    return d, d is not None


# ---------- content ----------

PATTERNS = {
    "performance claim": [
        r"\b\d+(\.\d+)?\s?%(?!\s*off\b)",
        r"\bfrom \d+[\w ]{0,12} to \d+",
        r"\b\d+(\.\d+)?x\b",
        r"\b(cut|cuts|reduce[sd]?|increase[sd]?|double[sd]?|boost[s]?|save[sd]?|grow[s]?|filled|lift[s]?)\b[^.]{0,40}\d",
        r"\b(\d+|one|two|three|four|five)\s+(days?|hours?|weeks?)\b[^.]{0,25}\b(not|instead of)\b",
        r"\bguarantee[sd]?\b",
    ],
    "comparative claim": [
        r"\b(better|faster|cheaper|easier|more accurate|smarter|quicker)\s+than\b",
        r"\b(fastest|best|cheapest|easiest|leading|#1|number one|top-rated)\b",
        r"\bthe only\b", r"\bthe most \w+", r"\bvs\.?\s", r"\bversus\b", r"\bunlike\b",
    ],
    "price or offer": [
        r"\$\s?\d", r"\b\d+\s?% off\b", r"\bfree\b", r"\btrial\b", r"\bdiscount\w*", r"\bpromo\w*",
        r"\bcoupon\w*", r"/month\b", r"\bper (month|location|seat|user|rep)\b", r"\ba month\b",
    ],
    "regulated health": [
        r"\bpatients?\b", r"\bHIPAA\b", r"\bPHIPA\b", r"\bdiagnos\w*", r"\btreat(ment|s)?\b", r"\bcures?\b",
        r"\bsymptoms?\b", r"\bmedical\b", r"\bclinical\w*", r"\bprescri\w*", r"\bhealth (data|information|records?)\b",
    ],
    "regulated financial": [
        r"\btaxable\b", r"\btax deduct\w*", r"\bdeduct(ible|ion)s?\b", r"\breport (them|it|your|their)\b",
        r"\bCRA\b", r"\bIRS\b", r"\bT4\b", r"\bW-2\b", r"\btax advice\b", r"\bwrite[- ]offs?\b",
        r"\binvest\w*", r"\binterest rates?\b", r"\bloans?\b", r"\bcredit scores?\b",
    ],
    "regulated employment": [
        r"\btip[- ]?pool\w*", r"\bminimum wage\b", r"\bovertime\b", r"\bwages?\b", r"\bsalar(y|ies)\b",
        r"\bhiring\b", r"\bjob applicants?\b", r"\btermination\b", r"\bemployment standards\b", r"\blabour law\b",
    ],
    "brand change": [
        r"\bnew logo\b", r"\brebrand\w*", r"\bnew name\b", r"\btagline\b", r"\bbrand colou?rs?\b", r"\bnew look\b",
    ],
}
CASE_SENSITIVE = {r"\bHIPAA\b", r"\bPHIPA\b", r"\bCRA\b", r"\bIRS\b", r"\bT4\b", r"\bW-2\b"}


def content_lines(text):
    out = []
    for i, line in enumerate(text.splitlines(), 1):
        if re.match(r"^\s*(version|author|status|reviewed)\s*:", line, re.I):
            continue
        if line.strip():
            out.append((i, line.strip()))
    return out


def snippet(line, start, end, width=90):
    a = max(0, start - 30)
    b = min(len(line), max(end + 40, a + width))
    s = line[a:b].strip()
    return ("…" if a > 0 else "") + s + ("…" if b < len(line) else "")


def detect(text, competitors):
    found = {}
    pats = dict(PATTERNS)
    if competitors:
        pats["comparative claim"] = pats["comparative claim"] + [r"\b" + re.escape(c) + r"\b" for c in competitors]
    for n, line in content_lines(text):
        for trig, plist in pats.items():
            for p in plist:
                flags = 0 if p in CASE_SENSITIVE else re.I
                m = re.search(p, line, flags)
                if m:
                    found.setdefault(trig, []).append((n, snippet(line, m.start(), m.end())))
                    break
    return found


def brand_rule_phrases(brand):
    path = os.path.join(brand or "", "rules.md")
    if not brand or not os.path.isfile(path):
        return []
    text = read(path)
    m = re.search(r"^## Everywhere\s*$(.*?)(?=^## |\Z)", text, re.S | re.M)
    out = []
    for line in (m.group(1) if m else "").splitlines():
        if not re.match(r"^\s*[-*]\s*(never|don't|do not|no)\b", line, re.I):
            continue
        rule = re.sub(r"\[source:[^\]]*\]", "", line).strip(" -*")
        for q in re.findall(r"[\"“]([^\"”]{2,60})[\"”]", line):
            out.append((q, rule))
    return out


def proof_records(brand):
    path = os.path.join(brand or "", "proof.md")
    recs = []
    if not brand or not os.path.isfile(path):
        return recs
    for line in read(path).splitlines():
        if not line.strip().startswith("-"):
            continue
        body = line.strip()[1:].strip()
        named = re.search(r"named:\s*([\w ]+?)\s*(\||$)", body)
        head = re.split(r"[:\[]", body, 1)[0]
        parts = [p.strip() for p in re.split(r",", re.sub(r"\([^)]*\)", "", head)) if p.strip()]
        names = []
        for p in parts:
            if p[0].islower() or re.search(r"\b(vp|vice president|director|head|owner|ceo|cfo|cto|coo|manager|lead|"
                                           r"president|founders?|controller|cpa|partner)\b", p, re.I):
                continue
            names.append(p)
        recs.append({"names": names, "named": norm(named.group(1)) if named else "not recorded", "line": body[:140]})
    return recs


def quoted_people(text):
    """Attributions next to quotes: lines after a quote, or 'Name, Company' after a closing quote."""
    out = []
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if re.search(r"[\"“][^\"”]{8,}[\"”]", line):
            tail = re.split(r"[\"”]", line)[-1].strip(" .,-—>")
            cand = tail or (lines[i + 1].strip(" >-—") if i + 1 < len(lines) else "")
            m = re.match(r"^((?:Dr\.\s)?[A-Z][a-z]+(?:\s[A-Z][a-z]+)+)", cand)
            if m:
                out.append((i + 1, m.group(1), cand[:90]))
            else:
                says = re.search(r"([A-Z][a-z]+(?:\s[A-Z][a-z]+)?)\s+says", line)
                if says:
                    out.append((i + 1, says.group(1), line.strip()[:90]))
    return out


def current_version(path, text):
    m = re.search(r"^\s*version\s*:\s*(v?\d+)", text, re.I | re.M)
    if m:
        v = m.group(1).lower()
        return v if v.startswith("v") else "v" + v
    m = re.search(r"-v(\d+)\.\w+$", path)
    return f"v{m.group(1)}" if m else None


# ---------- sign-offs ----------

def status_of(raw):
    s = norm(raw)
    if not s or s in ("none", "n/a", "na", "-", "not yet", "pending"):
        return "none"
    if re.search(r"(changes requested|not approved|reject|needs changes|request changes)", s):
        return "changes requested"
    if re.search(r"approv\w* (with changes|once|if|pending|subject to|after)|conditional", s):
        return "approved with changes"
    if re.search(r"(approv|signed off|sign off|lgtm)", s):
        return "approved"
    return "none"


def parse_review(path):
    meta = {}
    for line in read(path).splitlines():
        m = re.match(r"^\s*(reviewer|name|from|role|reviewed|version|sign-?off|status)\s*:\s*(.*)$", line, re.I)
        if m:
            k = m.group(1).lower().replace("-", "")
            k = {"name": "reviewer", "from": "reviewer", "version": "reviewed", "status": "signoff"}.get(k, k)
            meta.setdefault(k, m.group(2).strip())
    base = os.path.splitext(os.path.basename(path))[0].lower()
    role = meta.get("role", "").lower() or next((r for r in ROLE_WORDS if r.replace(" ", "-") in base), "")
    name = meta.get("reviewer", "")
    if not name:
        rest = base
        for r in ROLE_WORDS:
            rest = rest.replace(r.replace(" ", "-"), "")
        name = " ".join(w.capitalize() for w in rest.split("-") if w)
    return {"name": name, "role": role, "reviewed": meta.get("reviewed", ""),
            "signoff": status_of(meta.get("signoff")), "raw": meta.get("signoff", ""), "file": path}


def review_files(items):
    out = []
    for it in items or []:
        if os.path.isdir(it):
            out += [os.path.join(it, f) for f in sorted(os.listdir(it)) if f.endswith(".md")]
        elif os.path.isfile(it):
            out.append(it)
    return out


def for_this_version(rv, content_path, version):
    r = norm(rv["reviewed"])
    if not r:
        return None, "the sign-off doesn't say which file or version it covers"
    base = os.path.basename(content_path).lower()
    files = re.findall(r"[\w.-]+\.(?:md|html|txt|docx|pdf)", r)
    if files and base not in files:
        return False, f"signed {', '.join(files)}, not {base}"
    vs = re.findall(r"\bv\d+\b", r)
    if version and vs and version not in vs:
        return False, f"signed {vs[0]}, this is {version}"
    return True, ""


# ---------- dates ----------

def add_business_days(d, n):
    while n > 0:
        d += dt.timedelta(days=1)
        if d.weekday() < 5:
            n -= 1
    return d


def fmt(d):
    return d.strftime("%a %Y-%m-%d") if d else "not set"


# ---------- build ----------

def build(a):
    text = read(a.content)
    src, types, triggers = parse_matrix(a.brand, a.approvals)
    rule, used_default = pick_type(types, a.type) if types else (None, False)
    version = current_version(a.content, text)
    competitors = []
    cpath = os.path.join(a.brand or "", "competitors.md")
    if a.brand and os.path.isfile(cpath):
        competitors = [m.group(1).strip() for m in re.finditer(r"^##\s+(.+)$", read(cpath), re.M)
                       if norm(m.group(1)) not in ("our read", "contents")]
    found = detect(text, competitors)
    if a.brand_change:
        found.setdefault("brand change", []).append((0, "the request says this changes the brand"))
    spend_hits = []
    spend = a.spend
    if spend is None:
        m = re.search(r"^\s*[-*]?\s*(?:total |media |ad )?(budget|spend)\s*:\s*\$\s?([\d,]+)", text, re.I | re.M)
        if m:
            spend = float(m.group(2).replace(",", ""))
    for t in triggers:
        m = re.match(r"spend over \$?([\d,]+)", t["trigger"])
        if m and spend is not None and spend > float(m.group(1).replace(",", "")):
            spend_hits.append((t, float(m.group(1).replace(",", ""))))
    breaches = [(q, r) for q, r in brand_rule_phrases(a.brand) if norm(q) in norm(text)]
    recs = proof_records(a.brand)
    people = quoted_people(text)
    consent = []
    seen = set()
    for rec in recs:
        hit = [n for n in rec["names"] if n and re.search(r"\b" + re.escape(n) + r"\b", text)]
        if hit and not any(h in seen for h in hit):
            seen.update(hit)
            consent.append({"who": " / ".join(hit), "named": rec["named"], "line": rec["line"]})
    for ln, who, ctx in people:
        if not any(who in c["who"] or c["who"].split(" / ")[0] in who for c in consent):
            consent.append({"who": who, "named": "no record in brand memory", "line": f"line {ln}: {ctx}"})
    if consent:
        found.setdefault("customer named", [])
        for c in consent:
            found["customer named"].append((0, c["who"]))

    requester = a.requester
    if not requester:
        m = re.search(r"^\s*author\s*:\s*(.+)$", text, re.I | re.M)
        requester = m.group(1).strip() if m else None
    self_allowed = bool(rule) and rule["self"] in ("yes", "allowed", "true")

    steps = []  # list of lists of dicts {role, name, checks, sla, why}
    if rule:
        order = rule["order"] or ([[r for r, _ in rule["signoff"] if r != "approver"]] if any(r != "approver" for r, _ in rule["signoff"]) else []) + ([["approver"]] if any(r == "approver" for r, _ in rule["signoff"]) else [])
        names = dict(rule["signoff"])
        placed = set()
        for grp in order:
            step = []
            for role in grp:
                if role in names:
                    step.append({"role": role, "name": names[role], "checks": [f"{rule['type']} sign-off"],
                                 "sla": rule["sla"].get(role), "why": ["required for " + (rule["type"] if not used_default else "default rule")]})
                    placed.add(role)
            if step:
                steps.append(step)
        for role, name in rule["signoff"]:
            if role not in placed:
                steps.insert(max(len(steps) - 1, 0), [{"role": role, "name": name, "checks": [f"{rule['type']} sign-off"],
                                                       "sla": rule["sla"].get(role), "why": ["required"]}])
    consent_needed = False
    unmatched = []
    active = {k: v for k, v in found.items()}
    for t, thr in spend_hits:
        active.setdefault(t["trigger"], []).append((0, f"spend {spend:,.0f} is over {thr:,.0f}"))
    for trig in active:
        rules_for = [t for t in triggers if t["trigger"] == trig or (trig.startswith("regulated") and t["trigger"] == trig)]
        if not rules_for:
            if trig == "customer named":
                consent_needed = True
                continue
            unmatched.append(trig)
            continue
        for t in rules_for:
            if norm(t["adds"]) == "consent":
                consent_needed = True
                continue
            for role, name in pairs(t["adds"]):
                target = None
                for s in steps:
                    for e in s:
                        if norm(e["name"]) == norm(name) or (e["role"] == role and norm(e["name"]) == norm(name)):
                            target = e
                if target:
                    target["checks"].append(t["checks"] or trig)
                    target["why"].append(trig)
                    if role != target["role"] and role not in target["role"].split(" + "):
                        target["role"] += " + " + role
                    if t["sla"] and (target["sla"] or 0) < t["sla"]:
                        target["sla"] = t["sla"]
                    continue
                entry = {"role": role, "name": name, "checks": [t["checks"] or trig], "sla": t["sla"], "why": [trig]}
                before = t["before"] or "approver"
                idx = next((i for i, s in enumerate(steps) if any(before in e["role"].split(" + ") for e in s)), None)
                if idx is None:
                    steps.append([entry])
                elif idx == 0:
                    steps.insert(0, [entry])
                else:
                    steps[idx - 1].append(entry)

    # self-approval
    blockers = []
    if rule:
        for s in steps:
            for e in s:
                if requester and norm(e["name"]) == norm(requester) and not self_allowed:
                    backup = next((n for r, n in rule["backup"] if r in e["role"].split(" + ")), None)
                    note = "the rule doesn't allow self-approval" if rule["self"] == "no" else "the rule doesn't say self-approval is allowed, so it isn't counted"
                    if backup and norm(backup) != norm(requester):
                        e["swap"] = f"{e['name']} is the requester ({note}); backup {backup} signs instead"
                        e["name"] = backup
                    else:
                        e["swap"] = f"{e['name']} is the requester ({note}) and the rule names no backup for {e['role']}"
                        e["name"] = "TBD"
                        blockers.append(f"no eligible {e['role']}: {requester} can't sign their own piece; ask who signs instead")
    for q, r in breaches:
        blockers.append(f'"{q}" breaks a brand rule ({r}); no sign-off clears it, it has to change')
    if consent_needed:
        for c in consent:
            if c["named"] != "yes":
                blockers.append(f"no customer consent on record for {c['who']} (proof.md: named: {c['named']})")

    # sign-offs
    reviews = [parse_review(p) for p in review_files(a.reviews)]
    rows = []
    for s in steps:
        for e in s:
            rv = next((r for r in reviews if e["name"] != "TBD" and norm(r["name"]) == norm(e["name"])), None)
            if not rv:
                e["status"], e["counts"] = "no sign-off", False
                continue
            ok, why = for_this_version(rv, a.content, version)
            e["status"] = rv["signoff"]
            e["counts"] = bool(ok) and rv["signoff"] in ("approved", "approved with changes")
            e["note"] = why if ok is not True else ("counts once their changes are in this version" if rv["signoff"] == "approved with changes" else "")
    for rv in reviews:
        if requester and norm(rv["name"]) == norm(requester) and not self_allowed and rv["signoff"] != "none":
            rows.append(f"{rv['name']} ({rv['role']}) signed '{rv['raw']}' but is the requester: doesn't count")
        elif not any(norm(rv["name"]) == norm(e["name"]) for s in steps for e in s):
            rows.append(f"{rv['name']} ({rv['role'] or 'role unknown'}) signed '{rv['raw']}': not a required step for this route")

    # dates
    start = dt.date.fromisoformat(a.requested) if a.requested else dt.date.today()
    prev = start
    for s in steps:
        dues = []
        for e in s:
            e["due"] = add_business_days(prev, e["sla"]) if e["sla"] is not None else None
            if e["due"]:
                dues.append(e["due"])
        prev = max(dues) if dues else prev
    finish = prev if steps else None
    golive = dt.date.fromisoformat(a.go_live) if a.go_live else None

    # status
    if not rule:
        status = "Unknown: no approval rule"
    elif blockers:
        status = "Not approved: blocked (" + "; ".join(b.split(" (")[0].split(":")[0] for b in blockers) + ")"
    else:
        waiting = []
        for s in steps:
            w = [e for e in s if not e.get("counts") or e.get("status") == "approved with changes"]
            if w:
                waiting = w
                break
        status = ("Not approved: waiting on " + ", ".join(f"{e['role']} ({e['name']})" for e in waiting)) if waiting else "Approved"
    return {"src": src, "rule": rule, "used_default": used_default, "version": version, "found": found,
            "spend": spend, "spend_hits": spend_hits, "breaches": breaches, "consent": consent,
            "consent_needed": consent_needed, "unmatched": unmatched, "steps": steps, "blockers": blockers,
            "rows": rows, "status": status, "start": start, "finish": finish, "golive": golive,
            "requester": requester, "self_allowed": self_allowed, "reviews": reviews}


def report(r, a):
    p = print
    p(f"CONTENT: {a.content} · version: {r['version'] or 'not stated'} · type asked: {a.type or 'not given'}")
    if a.channel or a.audience or a.region:
        p(f"  channel: {a.channel or '-'} · audience: {a.audience or '-'} · region: {a.region or '-'}")
    p(f"MATRIX: {r['src'] or 'none found (no ## Approvals in brand/rules.md and no approvals file)'}")
    if r["rule"]:
        ru = r["rule"]
        p(f"  rule used: type '{ru['type']}'" + (" (DEFAULT: no line for this type; confirm the type)" if r["used_default"] else ""))
        p(f"  sign-off: {', '.join(f'{x}={y}' for x, y in ru['signoff'])}" + (f" · backup: {', '.join(f'{x}={y}' for x, y in ru['backup'])}" if ru["backup"] else ""))
        p(f"  self-approval: {ru['self']}" + (" (treated as not allowed)" if ru["self"] == "not set" else ""))
    p(f"REQUESTER: {r['requester'] or 'not given (ask)'}")
    p("\nTRIGGER CANDIDATES (judge each; a passing feature mention is not a claim)")
    if not r["found"] and not r["spend_hits"]:
        p("- none")
    for trig, hits in r["found"].items():
        for n, s in hits[:6]:
            p(f"- {trig}: " + (f"line {n}: \"{s}\"" if n else s))
    for t, thr in r["spend_hits"]:
        p(f"- spend: {r['spend']:,.0f} is over the {thr:,.0f} threshold")
    if r["spend"] is not None and not r["spend_hits"]:
        p(f"- spend: {r['spend']:,.0f} (no threshold crossed)")
    for u in r["unmatched"]:
        p(f"  ! no matrix rule for '{u}': ask who checks it; don't guess a name")
    p("\nBRAND-RULE BREACHES")
    p("- none" if not r["breaches"] else "\n".join(f'- "{q}": {rule}' for q, rule in r["breaches"]))
    p("\nCUSTOMER CONSENT")
    if not r["consent"]:
        p("- no named customer or attributed quote found")
    for c in r["consent"]:
        ok = "on record" if c["named"] == "yes" else "NOT on record"
        p(f"- {c['who']}: named: {c['named']} -> consent {ok} · {c['line']}")
    p("\nROUTE (due = previous step's due + SLA in business days from " + fmt(r["start"]) + "; public holidays not counted)")
    if not r["steps"]:
        p("- no route: no approval rule")
    for i, s in enumerate(r["steps"], 1):
        for e in s:
            p(f"- step {i}: {e['role']} = {e['name']} · sla {e['sla'] if e['sla'] is not None else 'not set'} · due {fmt(e.get('due'))} · "
              f"sign-off: {e.get('status', 'no sign-off')}{' (COUNTS)' if e.get('counts') else ' (does not count)'}"
              + (f" · {e['note']}" if e.get("note") else ""))
            p(f"    why: {', '.join(dict.fromkeys(e['why']))} · checks: {'; '.join(dict.fromkeys(e['checks']))}")
            if e.get("swap"):
                p(f"    ! {e['swap']}")
    if r["consent_needed"]:
        p("- consent: " + ("; ".join(f"{c['who']} ({'on record' if c['named'] == 'yes' else 'missing'})" for c in r["consent"]) or "none needed"))
    if r["rows"]:
        p("\nOTHER SIGN-OFFS")
        for x in r["rows"]:
            p(f"- {x}")
    p("\nBLOCKERS")
    p("- none" if not r["blockers"] else "\n".join(f"- {b}" for b in r["blockers"]))
    p(f"\nSTATUS: {r['status']}")
    if r["status"] == "Approved":
        p("FINISH: every sign-off is in; due dates and go-live timing no longer apply (don't mention them)")
    elif r["finish"]:
        line = f"FINISH: last step due {fmt(r['finish'])}"
        if r["golive"]:
            if r["finish"] <= r["golive"]:
                slack, d = 0, r["finish"]
                while d < r["golive"]:
                    d += dt.timedelta(days=1)
                    if d.weekday() < 5 and d < r["golive"]:
                        slack += 1
                line += f" · go-live {fmt(r['golive'])} · fits, with {slack} business day(s) spare between the last due date and go-live"
            else:
                line += f" · go-live {fmt(r['golive'])} · DOES NOT FIT at these SLAs"
        p(line)


SECTIONS = ["## Status", "## Triggers found", "## Route", "## Blockers and open questions"]
LEAKS = r"\b(route\.py|script|checker|the skill|approval-routing|editorial-review-cycle|trigger candidates|SKILL\.md|system date|guided mode|draft mode)\b|/Users/|/private/tmp/"


def check(a):
    r = build(a)
    out = read(a.route_file)
    fails, warns = [], []
    for s in SECTIONS:
        if s.lower() not in out.lower():
            fails.append(f"missing section '{s}'")
    m = re.search(r"^## Status\s*$\s*(.+)$", out, re.M | re.I)
    first = norm(m.group(1)) if m else ""
    if first.startswith("approved") and r["status"] != "Approved":
        fails.append(f"says Approved but the sign-offs give: {r['status']}")
    if r["status"] == "Approved" and not first.startswith("approved"):
        warns.append("every required sign-off counts, but the status line doesn't say Approved")
    if not r["rule"] and not first.startswith("unknown"):
        warns.append("no approval rule found: the status should be 'Unknown: no approval rule'")
    for s in r["steps"]:
        for e in s:
            if e["name"] != "TBD" and norm(e["name"]) not in norm(out):
                fails.append(f"required approver missing from the route: {e['role']} ({e['name']})")
            if e.get("due") and e["due"].isoformat() not in out:
                warns.append(f"due date {e['due'].isoformat()} for {e['name']} not in the route")
    if r["requester"] and not r["self_allowed"]:
        for line in out.splitlines():
            if norm(r["requester"]) in norm(line) and re.search(r"\|\s*(approved|signed)\s*(\(v\d+\))?\s*\|?\s*$", norm(line)) and "doesn't count" not in norm(line) and "does not count" not in norm(line):
                fails.append(f"counts the requester's own sign-off: {line.strip()[:100]}")
    for q, _ in r["breaches"]:
        if norm(q) not in norm(out):
            fails.append(f"brand-rule breach not reported: \"{q}\"")
    for c in r["consent"]:
        if c["named"] != "yes" and r["consent_needed"] and norm(c["who"].split(" / ")[0]) not in norm(out):
            fails.append(f"missing customer consent not reported: {c['who']}")
    if re.search(LEAKS, out, re.I):
        fails.append("the route mentions how it was produced (scripts, checks, skill names, system date or absolute paths)")
    if a.reply and os.path.isfile(a.reply) and re.search(LEAKS, read(a.reply), re.I):
        fails.append("the reply mentions how it was produced (scripts, checks, skill names, system date or absolute paths)")
    for f in fails:
        print(f"FAIL: {f}")
    for w in warns:
        print(f"WARN: {w}")
    print("PASS" if not fails else f"{len(fails)} FAIL")
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("route", "check"):
        sp = sub.add_parser(name)
        if name == "check":
            sp.add_argument("route_file")
            sp.add_argument("--reply", help="the reply text file, checked for internals")
        sp.add_argument("content")
        sp.add_argument("--brand")
        sp.add_argument("--approvals")
        sp.add_argument("--type")
        sp.add_argument("--requester")
        sp.add_argument("--requested", help="YYYY-MM-DD, default today")
        sp.add_argument("--go-live", dest="go_live")
        sp.add_argument("--spend", type=float)
        sp.add_argument("--channel")
        sp.add_argument("--audience")
        sp.add_argument("--region")
        sp.add_argument("--brand-change", action="store_true")
        sp.add_argument("--reviews", nargs="*")
    a = ap.parse_args()
    if a.cmd == "route":
        report(build(a), a)
        return 0
    return check(a)


if __name__ == "__main__":
    sys.exit(main())
