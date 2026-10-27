#!/usr/bin/env python3
"""Positioning deep dive helper. Standard library only.

Usage:
    python3 scripts/positioning_scan.py scan <pages or folder> [--competitors <pages or folder>]
    python3 scripts/positioning_scan.py score <audits/<domain>/dim-positioning.json> [--previous <old.json>]
    python3 scripts/positioning_scan.py trace <audits/<domain>/positioning.md> --sources <pages or folder> [--brand brand/]

scan   Per page: title, meta description, H1, subhead, CTA labels, audience lines, claims and generic phrases.
       Across pages: CTA wording that varies, audience wording that varies, phrases repeated on 2+ pages,
       and pages whose wording is more specific than the home page. With --competitors: phrases the site
       shares with each competitor page (swap-test candidates) and the site's lines no competitor shares.
score  Checks the P1-P5 checklist (each check 0, 10 or 20; every check present once), recomputes the total,
       compares with a previous checklist, and, if score.json from a full audit sits beside the file,
       prints the full audit's total and grade recomputed with the new positioning score (it never edits it).
trace  Reads the "## Headline options" section and lists every number, proper noun and quoted phrase that
       doesn't appear in the sources or brand memory, brand-memory never-use words and rule phrases used,
       and spelling that doesn't match the site's convention. Exit 1 if anything needs attention.
"""

import glob
import html
import json
import os
import re
import sys

GENERIC = ["unlock", "leverage", "seamless", "actionable insights", "modern teams", "modern brands",
           "modern sales teams", "drive results", "at scale", "streamline", "data-driven", "next-generation",
           "world-class", "cutting-edge", "innovative", "ai-powered", "all-in-one", "revolutionary",
           "game-changer", "solution", "empower", "smarter decisions", "close more deals", "with confidence",
           "grow faster", "best-in-class", "trusted by", "loved by", "platform", "just works",
           "takes the stress out", "focus on what matters", "easy", "effortless", "hassle-free", "peace of mind",
           "for modern", "your whole team"]
CLAIM = re.compile(r"(\d[\d,.%$]*|#1|\bonly\b|\bbest\b|\bfastest\b|\bleading\b|\breal-time\b|\btrusted by\b|"
                   r"\bloved by\b|\bguarantee|\bnot a chatbot\b|\bai-powered\b)", re.I)
AUDIENCE = re.compile(r"(built for|made for|designed for|\bfor (?:independent|small|growing|b2b|agencies|"
                      r"shopify|clinics|teams|restaurants|merchants|sales)|we don't serve|we do not serve|"
                      r"not for|not the right fit|who it's not for|teams of \d|\d+\s*(?:to|-|–)\s*\d+\s+"
                      r"(?:locations|reps|employees|stores))", re.I)
CTA_WORDS = re.compile(r"^(book|start|get|try|request|schedule|sign|join|talk|contact|see|buy|claim|download)\b", re.I)
SPELL = [("analyse", "analyze"), ("optimise", "optimize"), ("colour", "color"), ("centre", "center"),
         ("behaviour", "behavior"), ("organisation", "organization"), ("favourite", "favorite"),
         ("labour", "labor"), ("prioritise", "prioritize"), ("cheque", "check")]
STOP = set("the a an and or of to for in on with your you our we by at is are it this that from as be".split())


def read(path):
    return open(path, encoding="utf-8", errors="replace").read()


def files(args):
    out = []
    for a in args:
        if os.path.isdir(a):
            out += sorted(glob.glob(os.path.join(a, "*.htm*")) + glob.glob(os.path.join(a, "*.md")))
        elif os.path.isfile(a):
            out.append(a)
    return out


def strip(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()


def parse(path):
    raw = read(path)
    page = {"file": os.path.basename(path), "title": "", "meta": "", "h1": [], "subhead": "",
            "ctas": [], "text": "", "lines": []}
    if path.endswith(".md"):
        body = raw
        page["h1"] = [l[2:].strip() for l in body.splitlines() if l.startswith("# ")]
        clean = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", body)
        lines = [l.strip("#*-> ").strip() for l in clean.splitlines() if l.strip()]
        page["ctas"] = [m for m in re.findall(r"\[([^\]]+)\]\([^)]+\)", body) if CTA_WORDS.match(m)]
    else:
        raw_nc = re.sub(r"<!--.*?-->", " ", raw, flags=re.S)
        m = re.search(r"<title[^>]*>(.*?)</title>", raw_nc, re.S | re.I)
        page["title"] = strip(m.group(1)) if m else ""
        m = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)', raw_nc, re.I)
        page["meta"] = html.unescape(m.group(1)) if m else ""
        page["h1"] = [strip(x) for x in re.findall(r"<h1[^>]*>(.*?)</h1>", raw_nc, re.S | re.I)]
        h1_end = re.search(r"</h1>", raw_nc, re.I)
        if h1_end:
            m = re.search(r"<(p|h2)[^>]*>(.*?)</\1>", raw_nc[h1_end.end():], re.S | re.I)
            page["subhead"] = strip(m.group(2)) if m else ""
        for tag, attrs, inner in re.findall(r"<(a|button)([^>]*)>(.*?)</\1>", raw_nc, re.S | re.I):
            label = strip(inner)
            if label and (CTA_WORDS.match(label) or "btn" in attrs or "mailto:" in attrs):
                page["ctas"].append(label + (" (mailto)" if "mailto:" in attrs else ""))
        body = re.sub(r"<(script|style|nav|footer)[^>]*>.*?</\1>", " ", raw_nc, flags=re.S | re.I)
        blocks = re.split(r"</?(?:p|h\d|li|blockquote|div|footer|nav|title)[^>]*>", body, flags=re.I)
        lines = [strip(b) for b in blocks if strip(b)]
    page["lines"] = lines
    page["text"] = " ".join(lines)
    if not page["subhead"] and len(lines) > 1 and path.endswith(".md"):
        page["subhead"] = next((l for l in lines if l not in page["h1"]), "")
    return page


def ngrams(text, n=4):
    if isinstance(text, list):
        out = set()
        for line in text:
            out |= ngrams(line, n)
        return out
    words = [w for w in re.findall(r"[a-z0-9'%$-]+", text.lower())]
    out = set()
    for i in range(len(words) - n + 1):
        g = words[i:i + n]
        if sum(w not in STOP for w in g) >= 2:
            out.add(" ".join(g))
    return out


def scan(args):
    comp_args = []
    if "--competitors" in args:
        i = args.index("--competitors")
        comp_args = args[i + 1:]
        args = args[:i]
    pages = [parse(p) for p in files(args)]
    if not pages:
        print("FAIL: no pages found. Ask for saved HTML or pasted copy; never review a site you haven't read.")
        return 1
    print(f"# Positioning scan: {len(pages)} page(s)\n")
    for p in pages:
        low = p["text"].lower()
        print(f"## {p['file']}")
        print(f"- title: {p['title'] or '(none)'}")
        if p["meta"]:
            print(f"- meta description: {p['meta']}")
        print(f"- H1: {' | '.join(p['h1']) or '(none)'}")
        print(f"- subhead: {p['subhead'] or '(none)'}")
        print(f"- CTA labels: {', '.join(dict.fromkeys(p['ctas'])) or '(none)'}")
        aud = [l for l in p["lines"] if AUDIENCE.search(l)]
        print(f"- audience lines: {' || '.join(aud) or '(none found)'}")
        claims = [l for l in p["lines"] if CLAIM.search(l) and len(l) < 300]
        print(f"- claims to source: {' || '.join(claims) or '(none found)'}")
        gen = [g for g in GENERIC if re.search(r"\b" + re.escape(g) + r"\b", low)]
        print(f"- generic phrases: {', '.join(gen) or '(none)'}")
        print()
    print("## Across pages")
    labels = {}
    for p in pages:
        for c in dict.fromkeys(p["ctas"]):
            if c.lower() not in {x.lower() for x in p["h1"]}:
                labels.setdefault(c, []).append(p["file"])
    if len(labels) > 1:
        print("- CTA wording varies (belongs to conversion in the full audit, not to P4): " +
              "; ".join(f'"{k}" on {", ".join(v)}' for k, v in labels.items()))
    elif labels:
        print(f"- one CTA label everywhere: \"{next(iter(labels))}\"")
    auds = {p["file"]: [l for l in p["lines"] if AUDIENCE.search(l)] for p in pages}
    if sum(1 for v in auds.values() if v) > 1:
        print("- audience wording by page (check they name the same audience):")
        for f, v in auds.items():
            if v:
                print(f"    {f}: {' || '.join(v)}")
    grams = {}
    for p in pages:
        for g in ngrams(p["lines"]):
            grams.setdefault(g, set()).add(p["file"])
    rep = sorted((g for g, s in grams.items() if len(s) > 1), key=lambda g: -len(grams[g]))
    if rep:
        print("- phrases repeated on 2+ pages: " + "; ".join(f'"{g}" ({len(grams[g])})' for g in rep[:12]))
    home = next((p for p in pages if re.match(r"(index|home)", p["file"], re.I)), None)
    if home:
        hg = sum(1 for g in GENERIC if re.search(r"\b" + re.escape(g) + r"\b", home["text"].lower()))
        ha = len(auds.get(home["file"], []))
        for p in pages:
            if p is home:
                continue
            pg = sum(1 for g in GENERIC if re.search(r"\b" + re.escape(g) + r"\b", p["text"].lower()))
            if len(auds.get(p["file"], [])) > ha and pg <= hg:
                print(f"- {p['file']} names its audience more specifically than the home page, with fewer generic "
                      f"phrases (home {hg}, {p['file']} {pg}): check P4 ('about page clearer than the home page')")
    if comp_args:
        comps = [parse(p) for p in files(comp_args)]
        site_grams = {}
        for p in pages:
            for g in ngrams(p["lines"], 3):
                site_grams.setdefault(g, set()).add(p["file"])
        print("\n## Swap test (supplied competitor pages only)")
        shared_all = set()
        for c in comps:
            cg = ngrams(c["lines"], 3)
            shared = sorted(set(site_grams) & cg)
            shared_all |= set(shared)
            print(f"- {c['file']} H1: {' | '.join(c['h1']) or '(none)'}")
            print(f"  shares with the site: " + ("; ".join(f'"{g}" (site: {", ".join(sorted(site_grams[g]))})'
                                                       for g in shared[:15]) or "(no 3-word phrases)"))
        uniq = []
        for p in pages:
            for l in p["lines"]:
                lg = ngrams(l, 3)
                if len(l) > 40 and lg and not (lg & shared_all) and (AUDIENCE.search(l) or CLAIM.search(l) or len(l) > 80):
                    uniq.append(f"{p['file']}: {l}")
        print("- site lines that share no phrase with any competitor page (candidates for what's specific):")
        for u in uniq[:12]:
            print(f"    {u}")
    return 0


ALLOWED = {f"P{i}": {0, 10, 20} for i in range(1, 6)}
BANDS = [(85, "A"), (70, "B"), (55, "C"), (40, "D"), (0, "F")]
WEIGHTS = {"positioning": 25, "acquisition": 20, "conversion": 20, "brand": 15, "measurement": 20}


def checklist(path):
    d = json.load(open(path, encoding="utf-8"))
    return d, {c["id"]: c.get("points") for c in d.get("checks", [])}


def score(args):
    prev = None
    if "--previous" in args:
        i = args.index("--previous")
        prev = args[i + 1]
        del args[i:i + 2]
    if not args or not os.path.isfile(args[0]):
        print(__doc__)
        return 2
    d, pts = checklist(args[0])
    bad = 0
    if d.get("dimension") != "positioning":
        print('FAIL: "dimension" must be "positioning"')
        bad += 1
    for cid, allowed in ALLOWED.items():
        if cid not in pts:
            print(f"FAIL: {cid} missing")
            bad += 1
        elif pts[cid] not in allowed:
            print(f"FAIL: {cid} has {pts[cid]} points; allowed: 0, 10 or 20")
            bad += 1
    extra = [c for c in pts if c not in ALLOWED]
    if extra:
        print(f"FAIL: unknown checks {extra}; the positioning checklist is P1-P5 only")
        bad += 1
    for c in d.get("checks", []):
        if not str(c.get("evidence", "")).strip():
            print(f"FAIL: {c['id']} has no evidence line")
            bad += 1
    total = sum(v for v in pts.values() if isinstance(v, int))
    if d.get("score") != total:
        print(f"NOTE: score {d.get('score')} replaced by the sum of the checks ({total}); fix the file")
        bad += 1
    print("| Check | Points |\n|---|---|")
    for cid in ALLOWED:
        print(f"| {cid} | {pts.get(cid, '-')} / 20 |")
    print(f"| Total | {total} / 100 |")
    if prev and os.path.isfile(prev):
        _, old = checklist(prev)
        ot = sum(v for v in old.values() if isinstance(v, int))
        moved = [f"{c} {old.get(c)}→{pts.get(c)}" for c in ALLOWED if old.get(c) != pts.get(c)]
        print(f"\nPrevious checklist: {ot} → now {total} ({'; '.join(moved) or 'no check moved'})")
    sj = os.path.join(os.path.dirname(os.path.abspath(args[0])), "score.json")
    if os.path.isfile(sj):
        s = json.load(open(sj, encoding="utf-8"))
        dims = {k: v.get("score", 50) for k, v in s.get("dimensions", {}).items()}
        dims["positioning"] = total
        new_total = round(sum(dims.get(k, 50) * w / 100 for k, w in WEIGHTS.items()))
        grade = next(g for cut, g in BANDS if new_total >= cut)
        print(f"Full audit total: {s.get('total')} (grade {s.get('grade')}) → {new_total} (grade {grade}) "
              f"with this positioning score. The full report is unchanged until it's re-scored.")
    print("\nPASS" if not bad else f"\n{bad} problem(s): fix the checklist file and rerun")
    return 1 if bad else 0


def section(text, name):
    m = re.search(rf"^##\s+{name}.*?$(.*?)(?=^##\s|\Z)", text, re.M | re.S | re.I)
    return m.group(1) if m else ""


def trace(args):
    def opt(flag):
        if flag in args:
            i = args.index(flag)
            v = args[i + 1]
            del args[i:i + 2]
            return v
        return None
    src, brand = opt("--sources"), opt("--brand")
    if not args or not os.path.isfile(args[0]) or not src:
        print(__doc__)
        return 2
    opts = section(read(args[0]), "Headline options")
    if not opts.strip():
        print("FAIL: no '## Headline options' section found")
        return 1
    # Only the option lines themselves (headline / subhead), not the "built from" source notes.
    cand = "\n".join(l for l in opts.splitlines()
                     if re.search(r"(headline|subhead|^\s*[-*]?\s*\*\*?[A-C1-3][.):])", l, re.I)
                     and not re.search(r"built from|source|why|trace", l, re.I)) or opts
    corpus = " ".join(parse(p)["text"] for p in files([src]))
    never, rules = [], []
    if brand and os.path.isdir(brand):
        for f in glob.glob(os.path.join(brand, "*.md")):
            t = read(f)
            corpus += " " + t
        v = os.path.join(brand, "voice.md")
        if os.path.isfile(v):
            nv = re.sub(r"\[source:[^\]]*\]", "", section(read(v), "Words we never use"))
            for line in nv.splitlines():
                if line.strip().startswith("-"):
                    never += [w.strip(" -\"'").lower() for w in line.split(",") if w.strip(" -\"'")]
        r = os.path.join(brand, "rules.md")
        if os.path.isfile(r):
            rules = re.findall(r'"([^"]{3,})"', section(read(r), "Everywhere"))
    low_corpus = corpus.lower()
    issues = 0
    for n in sorted(set(re.findall(r"\$?\d[\d,.]*\s*(?:%|m|k|x)?", cand, re.I))):
        core = n.strip().rstrip(".,")
        if core and core.lower() not in low_corpus:
            print(f"UNTRACED number: {core}")
            issues += 1
    names = set()
    for m in re.finditer(r"\b([A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)*)", cand):
        before = cand[max(0, m.start() - 2):m.start()]
        if re.search(r"[\"“:.!?]\s?$|^\s*$", before) and " " not in m.group(1):
            continue  # a capital that only starts a sentence or a quoted option
        names.add(m.group(1))
    for nm in sorted(names):
        if nm.lower() in {"headline", "subhead", "option", "built", "a", "b", "c", "i", "we", "you", "your", "our"}:
            continue
        if nm.lower() not in low_corpus:
            print(f"UNTRACED name or term: {nm}")
            issues += 1
    lc = cand.lower()
    for w in never:
        if w and re.search(r"\b" + re.escape(w) + r"\b", lc):
            print(f"NEVER-USE word in an option: {w}")
            issues += 1
    for ph in rules:
        if ph.lower() in lc:
            print(f"RULE phrase in an option: \"{ph}\" (brand rules restrict it)")
            issues += 1
    site = " ".join(parse(p)["text"] for p in files([src])).lower()
    uk = sum(site.count(a) for a, _ in SPELL)
    us = sum(site.count(b) for _, b in SPELL)
    if brand and os.path.isfile(os.path.join(brand, "voice.md")):
        vt = read(os.path.join(brand, "voice.md")).lower()
        if "us spelling" in vt or "american spelling" in vt:
            us, uk = us + 10, uk
        elif "canadian spelling" in vt or "british spelling" in vt:
            uk += 10
    for a, b in SPELL:
        if us > uk and re.search(r"\b" + a, lc):
            print(f"SPELLING: '{a}' in an option; this site uses US spelling ('{b}')")
            issues += 1
        if uk > us and re.search(r"\b" + b, lc):
            print(f"SPELLING: '{b}' in an option; this site uses Canadian/British spelling ('{a}')")
            issues += 1
    print("PASS: every number and name in the options traces to the sources" if not issues
          else f"{issues} item(s) to fix or justify")
    return 1 if issues else 0


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("scan", "score", "trace"):
        print(__doc__)
        return 2
    cmd, args = sys.argv[1], sys.argv[2:]
    return {"scan": scan, "score": score, "trace": trace}[cmd](args)


if __name__ == "__main__":
    sys.exit(main())
