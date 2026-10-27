#!/usr/bin/env python3
"""Mechanical analysis for a content audit. Standard library only. Reads only what it is given; never estimates.

Usage:
    # 1. Analyse and write a draft inventory (decisions are suggestions for you to confirm or change)
    python3 scripts/audit_content.py --csv data/export.csv --posts posts/ --sitemap sitemap.xml \
        --brand brand/ --today 2026-10-24 --draft audits/content/inventory.csv

    # 2. After editing the inventory and writing AUDIT.md, check both
    python3 scripts/audit_content.py --check audits/content/inventory.csv --report audits/content/AUDIT.md \
        --csv data/export.csv --posts posts/ --sitemap sitemap.xml --today 2026-10-24

Any input can be left out: with only --posts, only content-based flags are raised and metric rules are skipped.
Thresholds (change with --set name=value, repeatable):
    low_traffic=100       traffic below this (in the export's own period) counts as low
    stale_months=18       last updated longer ago than this counts as stale
    new_months=6          published more recently than this is too new to judge on traffic
    thin_words=150        fewer words than this counts as thin
    title_similarity=0.6  title/slug word overlap (Jaccard) that counts as a competing pair
    body_similarity=0.25  body text similarity (TF-IDF cosine) that flags an overlap to check (closest match for both)

Report sections: INPUTS, BRAND, PIECES, PAIRS, FACTS, SITEMAP, SUGGESTED. Check mode prints PASS or FAIL lines.
Exit code: 0 clean, 1 if any FAIL in check mode, 2 on bad input.
"""

import argparse
import csv
import datetime
import html
import math
import os
import re
import sys
from collections import Counter

DEFAULTS = {"low_traffic": 100, "stale_months": 18, "new_months": 6, "thin_words": 150,
            "title_similarity": 0.6, "body_similarity": 0.25}
ALIASES = {
    "url": ["url", "page url", "page", "pages", "top pages", "address", "landing page", "page path", "path", "loc"],
    "title": ["title", "page title", "post title", "h1"],
    "published": ["published", "publish date", "date published", "published date", "created", "post date"],
    "last_updated": ["last updated", "updated", "last modified", "modified", "lastmod", "date modified"],
    "sessions": ["sessions", "visits", "entrances"],
    "clicks": ["clicks", "organic clicks", "url clicks"],
    "pageviews": ["pageviews", "page views", "views", "screen page views"],
    "users": ["users", "total users", "visitors"],
    "conversions": ["conversions", "key events", "goals", "goal completions", "leads", "signups", "sign-ups",
                    "demo requests"],
    "impressions": ["impressions"],
    "word_count": ["word count", "words", "wordcount"],
    "primary_keyword": ["primary keyword", "keyword", "target keyword", "focus keyword", "top query", "query"],
    "notes": ["notes", "note", "comments"],
}
METRICS = ["sessions", "clicks", "pageviews", "users", "conversions", "impressions"]
TRAFFIC_ORDER = ["sessions", "clicks", "pageviews", "users"]
DECISIONS = {"keep", "update", "merge", "redirect", "remove", "needs data"}
STOP = set("a an and are as at be by can do does for from how i in is it its of on or our the this to vs what "
           "when where which who why with you your we us new guide tips ways explained best".split())
HIST_HEAD = re.compile(r"history|discontinued|retired|withdrawn|superseded|archive|no longer", re.I)
RETIRED_HEAD = re.compile(r"discontinued|retired|withdrawn|superseded|no longer", re.I)
HIST_LINE = re.compile(r"\b(discontinued|withdrawn|retired|superseded|no longer|replaced by|don't reuse|do not reuse)\b", re.I)
HELD_HEAD = re.compile(r"needs substantiation|restricted|held|banned", re.I)
NOTFOR_HEAD = re.compile(r"not for|we don't do|don't serve|out of scope|exclude", re.I)
MONEY = re.compile(r"\$\s?\d[\d,]*(?:\.\d+)?(?:\s?[kKmM]\b)?")
YEAR = re.compile(r"(?<![\d$])(20[12]\d)(?!\d)")
QUOTED = re.compile(r"[\"“]([^\"”]{3,80})[\"”]")


def die(msg):
    print(f"ERROR: {msg}")
    sys.exit(2)


def norm_header(h):
    h = re.sub(r"\(.*?\)", "", h or "").lower().replace("_", " ")
    return re.sub(r"[^a-z0-9 -]", "", h).strip()


def norm_url(u):
    u = (u or "").strip()
    u = re.sub(r"^[a-z]+://[^/]+", "", u, flags=re.I)
    u = u.split("#")[0].split("?")[0]
    u = re.sub(r"\.(html?|md|markdown)$", "", u, flags=re.I)
    u = "/" + u.strip("/")
    return u.lower()


def slug(u):
    return norm_url(u).rstrip("/").split("/")[-1]


def tokens(text):
    out = []
    for t in re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)*", (text or "").lower()):
        if t in STOP or t.isdigit():
            continue
        out.append(t[:-1] if len(t) > 4 and t.endswith("s") and not t.endswith("ss") else t)
    return out


def parse_date(s):
    s = (s or "").strip()[:10]
    try:
        return datetime.date.fromisoformat(s)
    except ValueError:
        return None


def months(d, today):
    return None if d is None else (today.year - d.year) * 12 + today.month - d.month - (today.day < d.day)


def num(v):
    v = (v or "").strip().replace(",", "").replace("%", "")
    try:
        return float(v)
    except ValueError:
        return None


def fmt(v):
    return "" if v is None else (str(int(v)) if float(v).is_integer() else str(v))


# ---------- loading ----------

def load_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))
    if not rows:
        die(f"{path} is empty")
    header, mapping, unmapped, periods = rows[0], {}, [], []
    for i, h in enumerate(header):
        n, found = norm_header(h), None
        for key, names in ALIASES.items():
            if key not in mapping and (n in names or any(n.startswith(a + " ") for a in names)):
                found = key
                break
        if found:
            mapping[found] = i
            p = re.search(r"\((.*?)\)", h)
            if p and found in METRICS:
                periods.append(p.group(1))
        else:
            unmapped.append(h)
    if "url" not in mapping:
        die(f"no URL column found in {path} (headers: {', '.join(header)})")
    data = {}
    for r in rows[1:]:
        if not any(c.strip() for c in r):
            continue
        rec = {k: (r[i].strip() if i < len(r) else "") for k, i in mapping.items()}
        data[norm_url(rec["url"])] = rec
    return data, mapping, unmapped, periods


def front_matter(text):
    meta = {}
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            for line in text[3:end].splitlines():
                m = re.match(r"^([\w-]+)\s*:\s*(.*)$", line)
                if m:
                    meta[m.group(1).lower()] = m.group(2).strip().strip("\"'")
            text = text[end + 4:]
    return meta, text


def load_posts(folder):
    posts = {}
    for root, _, files in os.walk(folder):
        for fn in sorted(files):
            if not re.search(r"\.(md|markdown|html?)$", fn, re.I):
                continue
            path = os.path.join(root, fn)
            raw = open(path, encoding="utf-8", errors="replace").read()
            meta, body = front_matter(raw)
            if fn.lower().endswith((".html", ".htm")):
                for key, pat in (("title", r"<title[^>]*>(.*?)</title>"),
                                 ("url", r"<link[^>]+rel=[\"']canonical[\"'][^>]+href=[\"']([^\"']+)"),
                                 ("published", r"published_time[\"'][^>]+content=[\"']([^\"']+)"),
                                 ("updated", r"modified_time[\"'][^>]+content=[\"']([^\"']+)")):
                    m = re.search(pat, raw, re.I | re.S)
                    if m and key not in meta:
                        meta[key] = html.unescape(m.group(1)).strip()
                body = re.sub(r"(?is)<(script|style|head)[^>]*>.*?</\1>", " ", body)
                body = html.unescape(re.sub(r"<[^>]+>", " ", body))
            h1 = re.search(r"^#\s+(.+)$", body, re.M)
            stem = os.path.splitext(fn)[0]
            posts[stem] = {
                "file": os.path.relpath(path), "stem": stem, "body": body,
                "title": meta.get("title") or (h1.group(1).strip() if h1 else stem),
                "url": meta.get("url") or meta.get("permalink") or meta.get("canonical") or "",
                "published": meta.get("published") or meta.get("date") or "",
                "updated": meta.get("updated") or meta.get("last_updated") or meta.get("modified") or "",
                "words": len(re.findall(r"[A-Za-z0-9'’$%]+", re.sub(r"[#*_>`|-]", " ", body))),
            }
    return posts


def load_sitemap(path):
    text = open(path, encoding="utf-8", errors="replace").read()
    out = {}
    for block in re.findall(r"<url>(.*?)</url>", text, re.S | re.I) or [text]:
        for loc in re.findall(r"<loc>\s*(.*?)\s*</loc>", block, re.I):
            lm = re.search(r"<lastmod>\s*(.*?)\s*</lastmod>", block, re.I)
            out[norm_url(html.unescape(loc))] = lm.group(1)[:10] if lm else ""
    return out


def load_brand(folder):
    lines = []
    for fn in sorted(os.listdir(folder)):
        if not fn.endswith(".md"):
            continue
        heads = []
        for raw in open(os.path.join(folder, fn), encoding="utf-8").read().splitlines():
            m = re.match(r"^(#+)\s+(.*)$", raw)
            if m:
                heads = heads[:len(m.group(1)) - 1] + [m.group(2)]
                continue
            t = raw.strip().lstrip("-* ").strip()
            if not t or t.lower().startswith(("last reviewed", "status:", "|")):
                continue
            head = " / ".join(heads[1:]) if len(heads) > 1 else ""
            lines.append({"file": fn, "head": head, "text": t,
                          "history": bool(HIST_HEAD.search(head) or HIST_LINE.search(t)),
                          "retired": bool(RETIRED_HEAD.search(head)),
                          "held": bool(HELD_HEAD.search(head)) or fn == "rules.md",
                          "notfor": bool(NOTFOR_HEAD.search(head))})
    return lines


def brand_phrases(blines):
    """Phrases a piece shouldn't carry: retired offers/proof (label before ':' or ','), held or banned quoted claims."""
    out = []
    for b in blines:
        if b["retired"]:
            label = re.split(r"[:,(\[]", b["text"])[0].strip()
            if len(label) >= 4:
                out.append((label, "RETIRED", b))
        if b["retired"] or b["held"]:
            for q in QUOTED.findall(b["text"]):
                out.append((q.strip(), "RETIRED" if b["retired"] else "HELD", b))
    return out


# ---------- analysis ----------

def money_key(m):
    return re.sub(r"[\s,$]", "", m).lower()


def sentence_around(text, start, end):
    left = max(text.rfind(".", 0, start), text.rfind("\n", 0, start)) + 1
    right_dot = [i for i in (text.find(".", end), text.find("\n", end)) if i != -1]
    right = min(right_dot) if right_dot else len(text)
    return re.sub(r"\s+", " ", text[left:right]).strip()


def overlap(a, b):
    a, b = set(tokens(a)), set(tokens(b))
    return len(a & b) / len(a | b) if a and b else 0.0


def cosine(a, b, idf):
    ca = {t: v * idf.get(t, 0) for t, v in Counter(tokens(a)).items()}
    cb = {t: v * idf.get(t, 0) for t, v in Counter(tokens(b)).items()}
    dot = sum(ca[t] * cb.get(t, 0) for t in ca)
    na, nb = math.sqrt(sum(v * v for v in ca.values())), math.sqrt(sum(v * v for v in cb.values()))
    return dot / (na * nb) if na and nb else 0.0


def build(a):
    th = dict(DEFAULTS)
    for s in a.set or []:
        k, _, v = s.partition("=")
        if k not in th:
            die(f"unknown threshold '{k}' (known: {', '.join(th)})")
        th[k] = float(v)
    today = parse_date(a.today) if a.today else datetime.date.today()
    data, mapping, unmapped, periods = load_csv(a.csv) if a.csv else ({}, {}, [], [])
    posts = load_posts(a.posts) if a.posts else {}
    smap = load_sitemap(a.sitemap) if a.sitemap else {}
    blines = load_brand(a.brand) if a.brand and os.path.isdir(a.brand) else []

    pieces = {}
    for u, rec in data.items():
        pieces[u] = {"url": u, "row": rec, "post": None}
    by_slug = {slug(u): u for u in pieces}
    for stem, p in posts.items():
        u = norm_url(p["url"]) if p["url"] else None
        if not u or u not in pieces:
            u = by_slug.get(slug(p["url"]) if p["url"] else stem) or by_slug.get(stem) or u or "/" + stem
        pieces.setdefault(u, {"url": u, "row": None, "post": None})["post"] = p
    for u in smap:
        pieces.setdefault(u, {"url": u, "row": None, "post": None})

    traffic = next((m for m in TRAFFIC_ORDER if m in mapping), None)
    has_conv = "conversions" in mapping
    phrases = brand_phrases(blines)
    hist_money = [(money_key(m), b) for b in blines for m in MONEY.findall(b["text"])]

    for u, pc in pieces.items():
        row, post = pc["row"] or {}, pc["post"]
        pc["title"] = row.get("title") or (post["title"] if post else "")
        pc["published"] = row.get("published") or (post["published"] if post else "")
        pc["updated"] = row.get("last_updated") or (post["updated"] if post else "") or smap.get(u, "") or pc["published"]
        pc["words"] = num(row.get("word_count")) if row.get("word_count") else (post["words"] if post else None)
        pc["keyword"] = (row.get("primary_keyword") or "").lower().strip()
        pc["traffic"] = num(row.get(traffic)) if traffic and pc["row"] else None
        pc["conv"] = num(row.get("conversions")) if has_conv and pc["row"] else None
        pc["flags"], pc["facts"] = [], []
        f = pc["flags"]
        pub_age, upd_age = months(parse_date(pc["published"]), today), months(parse_date(pc["updated"]), today)
        pc["pub_age"], pc["upd_age"] = pub_age, upd_age
        if not pc["row"] and data:
            f.append("NO-DATA (not in the export)")
        if smap and u not in smap and pc["row"]:
            f.append("NOT-IN-SITEMAP")
        if pub_age is not None and pub_age < th["new_months"]:
            f.append(f"NEW (published {pc['published']}, {pub_age} months ago)")
        if upd_age is not None and upd_age > th["stale_months"]:
            f.append(f"STALE (last updated {pc['updated']}, {upd_age} months ago)")
        if pc["words"] is not None and pc["words"] < th["thin_words"]:
            f.append(f"THIN ({fmt(pc['words'])} words)")
        if pc["traffic"] is not None and pc["traffic"] < th["low_traffic"]:
            f.append(f"LOW-TRAFFIC ({fmt(pc['traffic'])} {traffic})")
        if row.get("notes"):
            f.append(f"NOTE: {row['notes']}")
        if pc["conv"]:
            f.append(f"CONVERTS ({fmt(pc['conv'])} conversions)")
        surface = " ".join([pc["title"], u.replace("-", " "), u])
        text = (post["body"] if post else "") + "\n" + surface
        body = post["body"] if post else ""
        for y in sorted({int(y) for y in YEAR.findall(text)}):
            if y < today.year - 1:
                m = re.search(rf"(?<!\d){y}(?!\d)", body)
                where = f"\"{sentence_around(body, m.start(), m.end())[:90]}\"" if m else "in the title or URL"
                f.append(f"OLD-YEAR {y}: {where}")
        low = text.lower().replace("’", "'")
        for phrase, kind, b in phrases:
            p = phrase.lower().replace("’", "'")
            if p in low or p.replace(" ", "-") in low:
                f.append(f"{kind} \"{phrase}\" (brand/{b['file']}: {b['text'][:110]})")
        for m in re.finditer(r"(?:pric\w*|from|plans?|only|just)[\s-]+\$?(\d{2,5})\b", surface, re.I):
            k = m.group(1)
            hits = [b for kk, b in hist_money if kk == k]
            if hits and all(b["history"] for b in hits):
                f.append(f"OLD-FIGURE ${k} in the title or URL: only in brand history (brand/{hits[0]['file']}: {hits[0]['text'][:100]})")
                break
        if post:
            for m in MONEY.finditer(post["body"]):
                sent = sentence_around(post["body"], m.start(), m.end())
                hits = [b for k, b in hist_money if k == money_key(m.group())]
                if not blines:
                    pc["facts"].append((m.group(), sent, "no brand memory to check against", None))
                    continue
                if not hits:
                    pc["facts"].append((m.group(), sent, "NOT FOUND in brand memory", None))
                    continue
                best = max(hits, key=lambda b: overlap(sent, b["text"]))
                status = "HISTORY" if best["history"] else "current"
                pc["facts"].append((m.group(), sent, status, best))
                if best["history"]:
                    f.append(f"OLD-FIGURE {m.group()}: closest brand line is history (brand/{best['file']}: {best['text'][:110]})")
        if any(b["notfor"] for b in blines):
            positive = " ".join(re.sub(r"\[source:[^\]]*\]", "", x["text"]).lower() for x in blines
                                if not x["notfor"] and x["file"] in ("audiences.md", "BRAND.md")
                                and not x["head"].lower().startswith(("files", "in one page")) and "not for" not in x["text"].lower())
            for b in (x for x in blines if x["notfor"]):
                for term in re.split(r",|\bor\b|\band\b", b["text"].split("[")[0]):
                    if re.search(r"\bnot\b|\bnon-|\bwithout\b", term, re.I):
                        continue
                    tk = [t.replace("e-", "") for t in tokens(term)]
                    if not tk:
                        continue
                    stem_ = tk[0] if len(tk[0]) >= 5 or len(tk) == 1 else " ".join(tk[:2])
                    if len(stem_) >= 5 and stem_ in low and stem_ not in positive:
                        f.append(f"EXCLUDED-AUDIENCE? \"{term.strip()}\" (brand/{b['file']})")
    pairs = find_pairs(pieces, th)
    for pc in pieces.values():
        pc["suggest"] = suggest(pc, pairs, th, has_conv, traffic)
    return {"th": th, "today": today, "pieces": pieces, "pairs": pairs, "mapping": mapping, "unmapped": unmapped,
            "periods": periods, "traffic": traffic, "has_conv": has_conv, "blines": blines, "smap": smap,
            "data": data, "posts": posts}


def strength(pc):
    return (pc["traffic"] or 0, pc["conv"] or 0, pc["updated"] or "")


def find_pairs(pieces, th):
    out, items = [], list(pieces.values())
    bodies = [set(tokens(x["post"]["body"])) for x in items if x["post"]]
    df = Counter(t for b in bodies for t in b)
    idf = {t: math.log(len(bodies) / n) for t, n in df.items()} if len(bodies) > 2 else {t: 1.0 for t in df}
    sims, best = {}, {}
    for i, x in enumerate(items):
        for y in items[i + 1:]:
            if x["post"] and y["post"]:
                c = cosine(x["post"]["body"], y["post"]["body"], idf)
                sims[(x["url"], y["url"])] = c
                for u in (x["url"], y["url"]):
                    best[u] = max(best.get(u, 0), c)
    for i, x in enumerate(items):
        for y in items[i + 1:]:
            why, strong_signal = [], False
            if x["keyword"] and x["keyword"] == y["keyword"]:
                why.append(f"same primary keyword \"{x['keyword']}\"")
                strong_signal = True
            tx, ty = x["title"] or slug(x["url"]).replace("-", " "), y["title"] or slug(y["url"]).replace("-", " ")
            sx, sy = set(tokens(tx)), set(tokens(ty))
            j = len(sx & sy) / len(sx | sy) if sx and sy else 0
            if j >= th["title_similarity"]:
                why.append(f"similar titles ({j:.2f})")
                strong_signal = True
            c = sims.get((x["url"], y["url"]), 0)
            mutual = c > 0 and c == best.get(x["url"]) and c == best.get(y["url"])
            if c >= th["body_similarity"] and (mutual or strong_signal):
                why.append(f"similar text ({c:.2f}{', closest match for both' if mutual else ''})")
            if why:
                known = x["traffic"] is not None and y["traffic"] is not None
                strong, weak = (x, y) if strength(x) >= strength(y) else (y, x)
                out.append({"a": strong["url"], "b": weak["url"], "why": "; ".join(why), "ranked": known,
                            "competing": strong_signal})
    return out


def suggest(pc, pairs, th, has_conv, traffic):
    f = " ".join(pc["flags"])
    fact = any(k in f for k in ("RETIRED", "HELD", "OLD-FIGURE"))
    weak_in = [p for p in pairs if p["b"] == pc["url"] and p["competing"]]
    retired_title = any(x.startswith("RETIRED") and x.split('"')[1].lower() in (pc["title"] + pc["url"]).lower()
                        for x in pc["flags"] if '"' in x)
    if pc["traffic"] is None:
        if fact:
            return ("update", "", "carries a retired, held or outdated fact (content only; no traffic data)")
        mates = [p for p in pairs if p["competing"] and pc["url"] in (p["a"], p["b"])]
        if mates:
            other = mates[0]["a"] if mates[0]["b"] == pc["url"] else mates[0]["b"]
            return ("needs data", other, "competes with another piece; pick which to keep with traffic data")
        return ("needs data", "", "no traffic or conversion data for this piece")
    if retired_title:
        return ("redirect", "", "the piece is about a retired offer or proof: redirect to the nearest current page, or remove")
    if fact:
        return ("update", "", "carries a retired, held or outdated fact")
    if "EXCLUDED-AUDIENCE" in f and not pc["conv"]:
        return ("remove", "", "may serve an audience brand memory excludes: confirm, and redirect if a close match exists")
    if weak_in and weak_in[0]["ranked"]:
        return ("merge", weak_in[0]["a"], f"weaker of a competing pair ({weak_in[0]['why']})")
    if "NEW" in f:
        return ("keep", "", "too new to judge on traffic")
    if pc["conv"]:
        return ("update", "", "converts but is stale") if "STALE" in f else ("keep", "", "converts")
    if "LOW-TRAFFIC" in f:
        if has_conv:
            return ("remove", "", "low traffic and no conversions: check audience and sales use before removing")
        return ("needs data", "", "low traffic, but conversions weren't supplied: check them before removing")
    if any(k in f for k in ("STALE", "THIN", "OLD-YEAR")):
        return ("update", "", "stale, thin or dated")
    return ("keep", "", "no problems found in the data")


# ---------- output ----------

def report(r):
    p, th = r["pieces"], r["th"]
    print("INPUTS")
    print(f"  today: {r['today']} · thresholds: " + ", ".join(f"{k}={fmt(v)}" for k, v in th.items()))
    if r["data"]:
        print(f"  export rows: {len(r['data'])} · columns used: " + ", ".join(sorted(r["mapping"])))
        print(f"  traffic metric: {r['traffic'] or 'NOT SUPPLIED'} · conversions: {'supplied' if r['has_conv'] else 'NOT SUPPLIED'}"
              + (f" · period: {', '.join(sorted(set(r['periods'])))}" if r["periods"] else " · period: not stated"))
        if r["unmapped"]:
            print("  columns not used: " + ", ".join(r["unmapped"]))
    else:
        print("  export: NOT SUPPLIED (no traffic, conversion or impression data; metric rules skipped)")
    print(f"  posts read: {len(r['posts'])} · sitemap URLs: {len(r['smap'])} · brand memory lines: {len(r['blines'])}"
          + ("" if r["blines"] else " (NO BRAND MEMORY: facts can't be checked against it)"))
    if r["blines"]:
        print("\nBRAND (audiences and lines to check pieces against)")
        for b in r["blines"]:
            if b["file"] == "audiences.md" or b["notfor"] or b["retired"] or b["history"]:
                tag = "NOT-FOR" if b["notfor"] else ("RETIRED" if b["retired"] else ("HISTORY" if b["history"] else "audience"))
                print(f"  [{tag}] brand/{b['file']}{' / ' + b['head'] if b['head'] else ''}: {b['text'][:140]}")
    print("\nPIECES")
    for u in sorted(p):
        pc = p[u]
        m = []
        if pc["traffic"] is not None:
            m.append(f"{fmt(pc['traffic'])} {r['traffic']}")
        if pc["conv"] is not None:
            m.append(f"{fmt(pc['conv'])} conversions")
        print(f"  {u} · \"{pc['title'][:70]}\" · " + (", ".join(m) or "no metrics")
              + f" · updated {pc['updated'] or '?'}" + (f" · post: {pc['post']['file']}" if pc["post"] else ""))
        for fl in pc["flags"]:
            print(f"      {fl}")
    print("\nPAIRS (competing pieces: first is stronger by the data" + ("" if r["traffic"] else "; NO DATA to rank them") + ")")
    for pr in r["pairs"] or []:
        kind = "COMPETING" if pr["competing"] else "OVERLAP (check; text only)"
        print(f"  {kind}: {pr['a']}  <->  {pr['b']} · {pr['why']}" + ("" if pr["ranked"] else " · not ranked (no data)"))
    if not r["pairs"]:
        print("  none found")
    print("\nFACTS (every price in the posts, with the closest brand-memory line)")
    any_fact = False
    for u in sorted(p):
        for fig, sent, status, b in p[u]["facts"]:
            any_fact = True
            src = f" · brand/{b['file']}: {b['text'][:110]}" if b else ""
            print(f"  {u} · {fig} · \"{sent[:100]}\" · {status}{src}")
    if not any_fact:
        print("  none" if r["posts"] else "  posts not supplied: facts in the pieces were not checked")
    if r["smap"]:
        print("\nSITEMAP")
        only_s = [u for u in r["smap"] if r["data"] and u not in r["data"]]
        only_d = [u for u in r["data"] if u not in r["smap"]]
        print("  in the sitemap, not in the export: " + (", ".join(only_s) or "none"))
        print("  in the export, not in the sitemap: " + (", ".join(only_d) or "none"))
    print("\nSUGGESTED (rules only: confirm or change each with judgment)")
    for u in sorted(p, key=lambda x: order_key(p[x])):
        d, t, why = p[u]["suggest"]
        print(f"  {d.upper():10} {u}" + (f" -> {t}" if t else "") + f" · {why}")


def order_key(pc):
    d = pc["suggest"][0]
    band = {"update": 0, "merge": 1, "redirect": 2, "remove": 3, "needs data": 4, "keep": 5}[d]
    if d == "update" and not any(k in " ".join(pc["flags"]) for k in ("RETIRED", "HELD", "OLD-FIGURE")):
        band = 1.5
    return (band, -(pc["traffic"] or 0) - 50 * (pc["conv"] or 0))


COLUMNS = ["url", "title", "published", "last_updated"]
PLAIN = {"NO-DATA": "no data", "NOT-IN-SITEMAP": "not in sitemap", "NEW": "too new to judge", "STALE": "stale",
         "THIN": "thin", "LOW-TRAFFIC": "low traffic", "CONVERTS": "converts", "NOTE": "note", "OLD-YEAR": "dated",
         "OLD-FIGURE": "outdated price", "RETIRED": "retired offer or proof", "HELD": "held claim",
         "EXCLUDED-AUDIENCE?": "audience check"}


def plain_flag(x):
    code = re.split(r"[ :(]", x, 1)[0]
    return PLAIN.get(code, code.lower())


def write_draft(r, out):
    p = r["pieces"]
    metrics = [m for m in METRICS if m in r["mapping"]]
    cols = COLUMNS + metrics + ["word_count", "primary_keyword", "flags", "audience", "decision", "target", "reason",
                                "evidence", "priority"]
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    ranked = sorted(p, key=lambda x: order_key(p[x]))
    with open(out, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for i, u in enumerate(ranked, 1):
            pc, row = p[u], p[u]["row"] or {}
            d, t, why = pc["suggest"]
            ev = [f"{row[m]} {m}" for m in metrics if row.get(m)]
            w.writerow([u, pc["title"], pc["published"], pc["updated"]] + [row.get(m, "") for m in metrics]
                       + [fmt(pc["words"]), pc["keyword"], "; ".join(dict.fromkeys(plain_flag(x) for x in pc["flags"])), "",
                          d, t, re.sub(r"\s*\(\d\.\d\d[^)]*\)", "", why), "; ".join(ev) or "no metrics supplied", i if d != "keep" else ""])
    print(f"\nDraft inventory written: {out} ({len(ranked)} rows). Fill 'audience' and confirm every decision.")


def check(r, inv_path, report_path):
    fails, warns = [], []
    with open(inv_path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    seen = {}
    for i, row in enumerate(rows, 2):
        u = norm_url(row.get("url", ""))
        seen[u] = row
        d = (row.get("decision") or "").strip().lower()
        if d not in DECISIONS:
            fails.append(f"line {i} {u}: decision '{row.get('decision')}' is not one of {sorted(DECISIONS)}")
        for c in ("reason", "evidence"):
            if not (row.get(c) or "").strip():
                fails.append(f"line {i} {u}: empty {c}")
        if "audience" in row and not (row.get("audience") or "").strip():
            fails.append(f"line {i} {u}: empty audience (name the audience it serves, 'none', or 'unknown')")
        src = r["data"].get(u, {})
        for m in METRICS:
            if m in row and (row.get(m) or "").strip():
                given = src.get(m, "")
                if num(row[m]) != num(given):
                    fails.append(f"line {i} {u}: {m} '{row[m]}' doesn't match the export ('{given or 'not supplied'}')")
        pc = r["pieces"].get(u)
        if d == "remove" and pc:
            if pc["conv"]:
                fails.append(f"line {i} {u}: marked remove but has {fmt(pc['conv'])} conversions")
            if pc["pub_age"] is not None and pc["pub_age"] < r["th"]["new_months"]:
                fails.append(f"line {i} {u}: marked remove but published {pc['pub_age']} months ago (too new)")
            if pc["traffic"] is None and not any(k in " ".join(pc["flags"]) for k in ("RETIRED", "HELD")):
                warns.append(f"line {i} {u}: marked remove with no traffic data; say what the decision rests on")
        if d in ("merge", "redirect"):
            t = norm_url(row.get("target", "")) if (row.get("target") or "").strip() else ""
            if not t:
                fails.append(f"line {i} {u}: {d} with no target")
    for i, row in enumerate(rows, 2):
        d = (row.get("decision") or "").strip().lower()
        t = norm_url(row.get("target", "")) if (row.get("target") or "").strip() else ""
        if d in ("merge", "redirect") and t in seen and (seen[t].get("decision") or "").lower() in ("merge", "redirect", "remove"):
            fails.append(f"line {i}: {d} target {t} is itself marked {seen[t].get('decision')}")
    for u in r["pieces"]:
        if u not in seen:
            fails.append(f"missing from the inventory: {u}")
    if report_path:
        if not os.path.exists(report_path):
            fails.append(f"report not found: {report_path}")
        else:
            text = open(report_path, encoding="utf-8").read()
            if not re.search(r"\*\*Recommendation:?\*\*", text[:600]):
                fails.append("report doesn't open with a **Recommendation:** line")
            top = re.search(r"##\s*Top actions?(.*?)(\n## |\Z)", text, re.S | re.I)
            if not top:
                fails.append("report has no '## Top actions' section")
            elif len(re.findall(r"^\s*\d+\.\s", top.group(1), re.M)) > 10:
                fails.append("more than 10 top actions")
            for need in ("Decisions", "Topic gaps", "How this was done"):
                if not re.search(rf"^##\s*{need}", text, re.M | re.I):
                    warns.append(f"report has no '## {need}' section")
            known = set(r["pieces"]) | {norm_url(x) for x in r["smap"]}
            for m in re.findall(r"(?<![\w.])(/[a-z0-9][a-z0-9/_-]*[a-z0-9])", text.lower()):
                if m.count("/") >= 2 and norm_url(m) not in known and not m.startswith(("/audits", "/brand", "/data", "/posts")):
                    warns.append(f"report mentions {m}, which isn't in the inventory (gap ideas are fine; a page isn't)")
            values = {num(v) for rec in r["data"].values() for k, v in rec.items() if k in METRICS and num(v) is not None}
            total = sum(num(v) for rec in r["data"].values() for k, v in rec.items() if k in METRICS and num(v) is not None)
            for m in re.finditer(r"(\d[\d,]*)\s+(sessions|clicks|visits|pageviews|views|conversions|impressions)\b", text, re.I):
                n = num(m.group(1))
                if n in values or n == 0 or re.search(r"(under|below|over|than|threshold[^.]{0,20})\s*$", text[max(0, m.start() - 25):m.start()], re.I):
                    continue
                if r["data"] and n <= total:
                    warns.append(f"report says '{m.group(0)}', not a single value in the export: make sure it's a total you added up")
                else:
                    fails.append(f"report says '{m.group(0)}', which isn't in the export")
            if re.search(r"\b(estimated?|projected|would gain|could gain|expected) (traffic|sessions|visits|clicks|conversions)", text, re.I):
                fails.append("report estimates traffic or conversions it wasn't given")
            if re.search(r"audit_content|\.py\b|--draft|\bthe script\b|\bchecker\b|\bSKILL\.md\b|content-audit", text):
                fails.append("report mentions internals (a script, its flags, or a skill name)")
    for w_ in warns:
        print(f"WARN {w_}")
    for f_ in fails:
        print(f"FAIL {f_}")
    print("PASS" if not fails else f"{len(fails)} FAIL")
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--csv")
    ap.add_argument("--posts")
    ap.add_argument("--sitemap")
    ap.add_argument("--brand")
    ap.add_argument("--today")
    ap.add_argument("--set", action="append")
    ap.add_argument("--draft")
    ap.add_argument("--check")
    ap.add_argument("--report")
    a = ap.parse_args()
    if not (a.csv or a.posts or a.sitemap):
        die("give at least one of --csv, --posts, --sitemap")
    for path in (a.csv, a.sitemap):
        if path and not os.path.isfile(path):
            die(f"not found: {path}")
    if a.posts and not os.path.isdir(a.posts):
        die(f"not a folder: {a.posts}")
    r = build(a)
    if a.check:
        sys.exit(check(r, a.check, a.report))
    report(r)
    if a.draft:
        write_draft(r, a.draft)


if __name__ == "__main__":
    main()
