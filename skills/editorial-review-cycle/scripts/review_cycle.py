#!/usr/bin/env python3
"""Consolidate reviewer feedback on a draft and check the review packet. Standard library only.

Usage:
    python3 scripts/review_cycle.py consolidate DRAFT --feedback FILE [FILE ...]
        [--brand brand/] [--approvals approvals.md] [--type "blog post"] [--alt OTHER_TEXT] [--qa NAME-qa.md]
    python3 scripts/review_cycle.py check NAME-review.md --draft BASE --version NAME-vN.md
        [--feedback FILE ...] [--brand brand/] [--approvals approvals.md] [--type "blog post"]

consolidate prints: the next version file name, each reviewer and their sign-off, every comment with an ID,
its anchor in the draft, a suggested class, then DUPLICATES, CONFLICTS, FIGURES (each figure a comment
brings in, traced to brand memory or not) and APPROVALS (required sign-offs against what was given).

check prints FAIL / WARN lines for the packet and the new version: missing sections, comments with no
decision, decisions with no decider, an "approved" state the sign-offs don't support, figures in the new
version that trace to nothing, review IDs or internals left in the version. Exit 1 on any FAIL.

Feedback files: optional header lines (Reviewer:, Role:, Reviewed:, Sign-off:) then one comment per bullet
or numbered line. Quoted text ("...") that appears in the draft is the comment's anchor; [Section] tags too.
"""

import argparse
import os
import re
import sys

ROLE_WORDS = ["subject expert", "sme", "editor", "legal", "compliance", "marketing", "approver", "sales",
              "product", "founder", "qa", "medical", "clinical", "advisor", "brand", "seo"]
REMOVE = re.compile(r"\b(remove|cut|delete|drop|take (?:it |this |that |them )?out|lose|soften|tone down|strike|don't use|do not use|get rid of)\b", re.I)
KEEP = re.compile(r"\b(keep|leave it|leave the|retain|don't water|do not water|don't remove|do not remove|don't cut|strengthen|lead with|make it bigger|bolder)\b", re.I)
ADD = re.compile(r"\b(add|include|mention|say that|insert|put in|open with|lead with)\b", re.I)
QUESTION_START = re.compile(r"^(is|are|does|do|can|could|should|would|why|what|how|who|when|where|did)\b", re.I)
PREFERENCE = re.compile(r"(personal preference|your call|\bi'?d\b|\bi would\b|\bmaybe\b|\bperhaps\b|\bconsider\b|\bnit\b|\boptional\b|if you like|up to you)", re.I)
MUST = re.compile(r"\b(wrong|incorrect|misspel\w*|typo|inaccurate|must|required|breaks?|rule|can't|cannot|not allowed|permission|overstates?|substantiat\w*|disclos\w*)\b", re.I)
FIGURE = re.compile(r"[$€£]?\d[\d,]*(?:\.\d+)?(?:\s?(?:%|percent|\+|x\b|k\b|hours?\b|days?\b|weeks?\b|minutes?\b|months?\b|years?\b|locations?\b|/month|/location))?", re.I)
QUOTE = re.compile(r"[\"“]([^\"”]{2,200})[\"”]")
STOP_CAPS = {"Remove", "Keep", "Add", "The", "This", "That", "Brand", "Change", "Make", "Also", "Cut", "Typo", "Should",
             "Don't", "Our", "Your", "Good", "Fix", "Say", "Call", "Open", "Every", "Social", "Otherwise", "Approved"}
FACT_FILES = ["BRAND.md", "offer.md", "proof.md", "positioning.md", "audiences.md", "claims.md", "results.md"]


def norm(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"').replace("–", "-").replace("—", "-")
    return re.sub(r"\s+", " ", s).strip().lower()


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def status_of(raw):
    s = norm(raw or "")
    if not s or s in ("none", "n/a", "na", "-", "not yet", "pending"):
        return "none"
    if re.search(r"(changes requested|not approved|reject|needs changes|request changes)", s):
        return "changes requested"
    if re.search(r"approv\w* (with changes|once|if|pending|subject to|after)|conditional", s):
        return "approved with changes"
    if re.search(r"(approv|signed off|sign off|lgtm)", s):
        return "approved"
    return "none"


def parse_feedback(path, reviewer_hint=None):
    text = read(path)
    meta, comments, cur = {}, [], None
    for line in text.splitlines():
        m = re.match(r"^\s*(reviewer|name|from|role|reviewed|version|sign-?off|status|decision|approval)\s*:\s*(.*)$", line, re.I)
        if m and cur is None:
            key = m.group(1).lower().replace("-", "")
            key = {"name": "reviewer", "from": "reviewer", "version": "reviewed", "status": "signoff",
                   "decision": "signoff", "approval": "signoff"}.get(key, key)
            meta[key] = m.group(2).strip()
            continue
        b = re.match(r"^\s*(?:[-*•]|\d+[.)])\s+(.*)$", line)
        if b:
            cur = b.group(1).strip()
            comments.append(cur)
        elif line.strip() and comments and line.startswith((" ", "\t")):
            comments[-1] += " " + line.strip()
        elif line.strip() and not comments and not line.startswith("#"):
            comments.append(line.strip())
            cur = comments[-1]
    base = os.path.splitext(os.path.basename(path))[0].replace("_", "-").lower()
    role = meta.get("role", "")
    if not role:
        role = next((r for r in ROLE_WORDS if r.replace(" ", "-") in base), "reviewer")
    name = meta.get("reviewer", "") or reviewer_hint
    if not name:
        rest = base
        for r in ROLE_WORDS:
            rest = rest.replace(r.replace(" ", "-"), "")
        name = " ".join(w.capitalize() for w in rest.split("-") if w) or "Unnamed reviewer"
    return {"name": name, "role": role.lower(), "signoff": status_of(meta.get("signoff")),
            "signoff_raw": meta.get("signoff", ""), "reviewed": meta.get("reviewed", ""), "file": path,
            "comments": comments}


def parse_qa(path):
    out, section = [], None
    for line in read(path).splitlines():
        h = re.match(r"^\*\*(Blockers|Fixes)\*\*", line.strip())
        if h:
            section = h.group(1)
            continue
        if line.startswith("**"):
            section = None
        m = re.match(r"^\s*\d+[.)]\s+(.*)$", line)
        if section and m:
            out.append(("must fix" if section == "Blockers" else "should fix", m.group(1).strip()))
    return out


def anchors(comment, draft_n):
    found = [q for q in QUOTE.findall(comment) if norm(q).strip(" .") and norm(q).strip(" .") in draft_n]
    return found


def classify(text, role, forced=None):
    if forced:
        return forced
    t = text.strip()
    if t.endswith("?") or (QUESTION_START.match(t) and "?" in t):
        return "question"
    if PREFERENCE.search(t):
        return "preference"
    if role in ("legal", "compliance") or MUST.search(t):
        return "must fix"
    return "should fix"


def words(s):
    return {w for w in re.findall(r"[a-z0-9$%]+", norm(s)) if len(w) > 3}


def caps(s):
    return {w for w in re.findall(r"\b[A-Z][a-zA-Z]{3,}\b", s) if w not in STOP_CAPS}


def brand_fact_lines(brand):
    lines = []
    if not brand or not os.path.isdir(brand):
        return lines
    for fn in FACT_FILES:
        p = os.path.join(brand, fn)
        if not os.path.isfile(p):
            continue
        section = ""
        for i, line in enumerate(read(p).splitlines(), 1):
            if line.startswith("## "):
                section = line[3:].strip().lower()
                continue
            l = line.lower()
            if fn == "claims.md" and section != "approved claims":
                continue
            if any(x in l for x in ("· provisional", "· assumed", "tbd", "substantiat", "claimed:")):
                continue
            if l.startswith("last reviewed") or not line.strip():
                continue
            lines.append((f"{fn}:{i}", re.sub(r"\[source:[^\]]*\]|\d{4}-\d{2}-\d{2}", "", line).strip()))
    return lines


def figures(text):
    return {norm(f).rstrip(".,") for f in FIGURE.findall(text) if re.search(r"\d", f)}


def bare(fig):
    return re.sub(r"[^\d.]", "", fig.split()[0]) if fig else fig


def trace_figure(fig, facts):
    core = re.escape(norm(fig))
    for ref, line in facts:
        if re.search(rf"(?<![\w.]){core}(?![\w])", norm(line)):
            return ref, line
    num = bare(fig)
    if len(num) >= 2 and re.fullmatch(r"[$€£]?[\d,.]+", fig.strip()):  # bare numbers like 349 or 15; single digits are too common to trust
        for ref, line in facts:
            if re.search(rf"(?<![\d.]){re.escape(num)}(?![\d])", norm(line).replace(",", "")):
                return ref, line
    return None


def parse_approvals(brand, approvals_file):
    src, lines = None, []
    if approvals_file and os.path.isfile(approvals_file):
        src = approvals_file
        lines = [l for l in read(approvals_file).splitlines() if "type:" in l and "sign-off:" in l]
    elif brand and os.path.isfile(os.path.join(brand, "rules.md")):
        text = read(os.path.join(brand, "rules.md"))
        m = re.search(r"^## Approvals\s*$(.*?)(?=^## |\Z)", text, re.S | re.M)
        if m:
            src = os.path.join(brand, "rules.md")
            lines = [l for l in m.group(1).splitlines() if "type:" in l]
    rules = []
    for l in lines:
        l = re.sub(r"\[source:[^\]]*\]", "", l).strip().lstrip("-* ").strip()
        fields = {}
        for part in l.split(" | "):
            if ":" in part:
                k, v = part.split(":", 1)
                fields[k.strip().lower()] = v.strip()
        def pairs(s):
            out = []
            for item in [x.strip() for x in (s or "").split(",") if x.strip()]:
                role, _, name = item.partition("=")
                out.append((role.strip().lower(), name.strip() or "TBD"))
            return out
        rules.append({"type": fields.get("type", "").lower(), "signoff": pairs(fields.get("sign-off")),
                      "backup": pairs(fields.get("backup")), "conflicts": fields.get("conflicts", "")})
    return src, rules


def pick_rule(rules, ctype):
    if not rules:
        return None
    t = (ctype or "").lower().strip()
    for r in rules:
        if t and (r["type"] == t or r["type"].rstrip("s") == t.rstrip("s")):
            return r
    return next((r for r in rules if r["type"] == "default"), None)


def find_reviewer(reviewers, role, name):
    n = norm(name)
    for rv in reviewers:
        if n not in ("tbd", "") and norm(rv["name"]) == n:
            return rv
    for rv in reviewers:
        if rv["role"] == role:
            return rv
    return None


def approval_state(reviewers, rule):
    rows, missing, conditional = [], [], []
    for role, name in rule["signoff"]:
        rv = find_reviewer(reviewers, role, name)
        st = rv["signoff"] if rv else "no feedback"
        via = ""
        if st not in ("approved", "approved with changes"):
            for brole, bname in rule["backup"]:
                if brole == role:
                    b = find_reviewer(reviewers, "__none__", bname)
                    if b and b["signoff"] in ("approved", "approved with changes"):
                        st, via = b["signoff"], f" (by backup {bname})"
        if st == "approved":
            mark = "SIGNED"
        elif st == "approved with changes":
            mark = "SIGNED IF THEIR CHANGES ARE APPLIED"
            conditional.append(f"{role}={name}")
        else:
            mark = "NOT SIGNED"
            missing.append(f"{role}={name} ({st})")
        rows.append(f"- {role}={name}: {st}{via} -> {mark}")
    if missing:
        state = "NOT APPROVED (missing: " + "; ".join(missing) + ")"
    elif conditional:
        state = "APPROVED ONCE CONDITIONS ARE MET (" + ", ".join(conditional) + ")"
    else:
        state = "APPROVED"
    return rows, state, bool(missing)


def next_version(draft):
    d, fn = os.path.split(os.path.abspath(draft))
    stem, ext = os.path.splitext(fn)
    stem = re.sub(r"-(gated|qa-fixed)$", "", stem)
    stem = re.sub(r"-v\d+$", "", stem)
    nums = [1]
    for f in os.listdir(d or "."):
        m = re.match(rf"^{re.escape(stem)}-v(\d+){re.escape(ext)}$", f)
        if m:
            nums.append(int(m.group(1)))
    return os.path.join(os.path.dirname(draft), f"{stem}-v{max(nums) + 1}{ext}"), stem


def build(a):
    draft_n = norm(read(a.draft))
    alt_n = norm(read(a.alt)) if a.alt else ""
    reviewers = [parse_feedback(p) for p in a.feedback]
    items = []
    for rv in reviewers:
        for c in rv["comments"]:
            items.append({"rv": rv, "text": c, "cls": classify(c, rv["role"]), "anchors": anchors(c, draft_n),
                          "alt_only": [q for q in QUOTE.findall(c) if norm(q) not in draft_n and alt_n and norm(q) in alt_n]})
    if a.qa:
        qrv = {"name": "QA check", "role": "qa", "signoff": "n/a", "signoff_raw": "", "reviewed": "", "file": a.qa, "comments": []}
        for cls, c in parse_qa(a.qa):
            problem = c.split(" · ", 1)[-1]  # "where · problem · fix": anchor on the problem, not the heading
            items.append({"rv": qrv, "text": c, "cls": cls, "anchors": anchors(problem, draft_n), "alt_only": []})
    for i, it in enumerate(items, 1):
        it["id"] = f"C{i}"
    return reviewers, items


def consolidate(a):
    reviewers, items = build(a)
    nv, stem = next_version(a.draft)
    print(f"NEXT VERSION: {nv}")
    print("\nREVIEWERS")
    for rv in reviewers:
        print(f"- {rv['name']} ({rv['role']}) · sign-off: {rv['signoff']}" + (f" ('{rv['signoff_raw']}')" if rv['signoff_raw'] else "")
              + (f" · reviewed: {rv['reviewed']}" if rv['reviewed'] else "") + f" · {len(rv['comments'])} comment(s)")
    print("\nCOMMENTS")
    for it in items:
        loc = "; ".join(f'"{q}"' for q in it["anchors"]) or (re.match(r"^\[([^\]]+)\]", it["text"]) or [None, "no anchor"])[1]
        extra = f" · quoted text only in {a.alt}" if it["alt_only"] else ""
        quoted = QUOTE.findall(it["text"])
        if quoted and not it["anchors"] and not it["alt_only"] and not ADD.search(it["text"]):
            extra += " · quoted text NOT FOUND in the draft (older version, or text to add?)"
        print(f"{it['id']} | {it['rv']['name']} ({it['rv']['role']}) | at: {loc} | suggest: {it['cls']}{extra} | {it['text']}")
    print("\nDUPLICATES")
    dup_seen = 0
    for i, x in enumerate(items):
        for y in items[i + 1:]:
            shared = {norm(q) for q in x["anchors"]} & {norm(q) for q in y["anchors"]}
            same_pol = not ((REMOVE.search(x["text"]) and KEEP.search(y["text"])) or (KEEP.search(x["text"]) and REMOVE.search(y["text"])))
            wx, wy = words(x["text"]), words(y["text"])
            jac = len(wx & wy) / max(1, len(wx | wy))
            if same_pol and (shared or jac >= 0.5):
                print(f"- {x['id']} ~ {y['id']}" + (f" (same text: \"{sorted(shared)[0]}\")" if shared else f" (similar wording, {jac:.0%})"))
                dup_seen += 1
    if not dup_seen:
        print("- none found")
    print("\nCONFLICTS")
    src, rules = parse_approvals(a.brand, a.approvals)
    rule = pick_rule(rules, a.type)
    decider = rule["conflicts"] if rule and rule["conflicts"] else "not set (ask the user who decides)"
    conf = 0
    for i, x in enumerate(items):
        for y in items[i + 1:]:
            if x["rv"]["name"] == y["rv"]["name"]:
                continue
            opposite = (REMOVE.search(x["text"]) and KEEP.search(y["text"])) or (KEEP.search(x["text"]) and REMOVE.search(y["text"]))
            if not opposite:
                continue
            shared = {norm(q) for q in x["anchors"]} & {norm(q) for q in y["anchors"]}
            overlap = any(norm(p) in norm(q) or norm(q) in norm(p) for p in x["anchors"] for q in y["anchors"])
            names = caps(x["text"]) & caps(y["text"])
            if shared or overlap or names:
                what = f"\"{sorted(shared)[0]}\"" if shared else ("overlapping text" if overlap else "both mention " + ", ".join(sorted(names)))
                print(f"- {x['id']} ({x['rv']['name']}, {x['rv']['role']}) vs {y['id']} ({y['rv']['name']}, {y['rv']['role']}): {what} -> decided by: {decider}")
                conf += 1
    if not conf:
        print("- none found (still read for conflicts the wording hides)")
    print("\nFIGURES (figures a comment brings in that the draft doesn't have)")
    facts = brand_fact_lines(a.brand)
    draft_figs = figures(read(a.draft))
    nfig = 0
    for it in items:
        for f in sorted(figures(it["text"]) - draft_figs):
            if re.fullmatch(r"\d", f):
                continue  # a lone digit ("November 3") is too common to trace
            hit = trace_figure(f, facts)
            tag = f"in brand memory {hit[0]}: {hit[1][:90]}" if hit else ("UNSUPPORTED: not in brand memory" + (" (comment gives a link)" if "http" in it["text"] else ""))
            print(f"- {it['id']} {f}: {tag}")
            nfig += 1
    if not facts:
        print("- (no brand memory: every new figure is unsupported until someone gives a source)")
    elif not nfig:
        print("- none")
    print("\nAPPROVALS")
    if not rule:
        print(f"- no approval rule found{' in ' + src if src else ' (no ## Approvals in brand/rules.md and no approvals file)'}"
              + (f"; types available: {', '.join(r['type'] for r in rules)}" if rules else ""))
        print("- state: UNKNOWN (ask who must sign off; never call it approved)")
        return 0
    print(f"- rule: type '{rule['type']}' from {src}" + ("" if a.type and rule["type"] != "default" else f" (asked for '{a.type}')" if a.type else ""))
    rows, state, _ = approval_state(reviewers, rule)
    for r in rows:
        print(r)
    if rule["backup"]:
        print("- backup: " + ", ".join(f"{r}={n}" for r, n in rule["backup"]))
    print(f"- conflicts decided by: {decider}")
    print(f"- state: {state}")
    return 0


def section(text, title):
    m = re.search(rf"^#+\s*{title}.*?$(.*?)(?=^#+\s|\Z)", text, re.S | re.M | re.I)
    return m.group(1) if m else None


def check(a):
    fails, warns = [], []
    review = read(a.review)
    for t in ("Approval state", "Comments", "Decision log", "Sign-offs"):
        if section(review, t) is None:
            fails.append(f"packet has no '{t}' section")
    com, log = section(review, "Comments") or "", section(review, "Decision log") or ""
    ids = sorted(set(re.findall(r"\bC\d+\b", com)), key=lambda s: int(s[1:]))
    logged = set(re.findall(r"\bC\d+\b", log))
    for i in ids:
        if i not in logged:
            fails.append(f"{i} is in Comments but has no row in the decision log")
    for row in log.splitlines():
        cells = [c.strip() for c in row.strip().strip("|").split("|")]
        if row.strip().startswith("|") and re.match(r"^C\d+", cells[0] if cells else "") and len(cells) >= 4:
            if not cells[-2] or cells[-2] in ("-", "—", "?"):
                fails.append(f"{cells[0]}: decision log row has no 'decided by'")
    if a.feedback:
        reviewers = [parse_feedback(p) for p in a.feedback]
        src, rules = parse_approvals(a.brand, a.approvals)
        rule = pick_rule(rules, a.type)
        st_text = norm((section(review, "Approval state") or "").strip().splitlines()[0] if (section(review, "Approval state") or "").strip() else "")
        claims_ok = bool(re.search(r"\bapproved\b", st_text)) and not re.search(r"not approved|unknown|waiting|blocked|pending|once", st_text)
        if rule:
            _, state, missing = approval_state(reviewers, rule)
            if claims_ok and missing:
                fails.append(f"packet says approved but the sign-offs say: {state}")
        elif claims_ok:
            fails.append("packet says approved but there is no approval rule to check it against")
    if os.path.abspath(a.version) == os.path.abspath(a.draft):
        fails.append("the new version overwrites the draft")
    if os.path.isfile(a.version):
        ver, base = read(a.version), read(a.draft)
        if norm(ver) == norm(base):
            warns.append("the new version is identical to the draft")
        facts = brand_fact_lines(a.brand)
        fb_text = {p: read(p) for p in (a.feedback or [])}
        for f in sorted(figures(ver) - figures(base)):
            if trace_figure(f, facts):
                continue
            src_fb = [p for p, t in fb_text.items() if f in figures(t)]
            if src_fb and any("http" in t for p, t in fb_text.items() if p in src_fb):
                warns.append(f"{f} in the new version comes from a reviewer who gave a source: record it in the packet")
            else:
                fails.append(f"{f} is in the new version but not in the draft or brand memory" + (" (a reviewer asked for it with no source)" if src_fb else ""))
        for pat, why in ((r"\bC\d+\b", "review IDs"), (r"\bTODO\b|\bTBD\b", "TODO/TBD markers"), (r"review_cycle|\bscript\b|\bskill\b", "internals")):
            if re.search(pat, ver) and not re.search(pat, base):
                fails.append(f"the new version contains {why}")
    else:
        fails.append(f"new version not found: {a.version}")
    if re.search(r"review_cycle|\.py\b|\bthe script\b|\bthis skill\b|\bSKILL\.md\b", review):
        fails.append("the packet mentions internals (script or skill)")
    for f in fails:
        print("FAIL", f)
    for w in warns:
        print("WARN", w)
    print("OK" if not fails else f"{len(fails)} FAIL")
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("consolidate")
    c.add_argument("draft")
    c.add_argument("--feedback", nargs="*", default=[])
    c.add_argument("--brand")
    c.add_argument("--approvals")
    c.add_argument("--type")
    c.add_argument("--alt")
    c.add_argument("--qa")
    k = sub.add_parser("check")
    k.add_argument("review")
    k.add_argument("--draft", required=True)
    k.add_argument("--version", required=True)
    k.add_argument("--feedback", nargs="*", default=[])
    k.add_argument("--brand")
    k.add_argument("--approvals")
    k.add_argument("--type")
    a = ap.parse_args()
    for p in ([a.draft] + list(a.feedback or [])):
        if not os.path.isfile(p):
            print(f"not found: {p}", file=sys.stderr)
            return 2
    return consolidate(a) if a.cmd == "consolidate" else check(a)


if __name__ == "__main__":
    sys.exit(main())
