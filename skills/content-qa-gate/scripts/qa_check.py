#!/usr/bin/env python3
"""Mechanical pre-publish checks for a content piece (Markdown or HTML). Standard library only.

Usage:
    python3 scripts/qa_check.py content/post.md --brief content/brief.md --brand brand/ --channel blog
    python3 scripts/qa_check.py page.html --channel landing --publish-date 2026-10-20

Channels: blog, landing, web, email, newsletter, social. Search checks (title, description, H1) run for blog/landing/web.

Levels:
    BLOCKER  placeholders, empty or '#' links, a forbidden phrase from brand rules, an affiliate link with no
             disclosure in the first paragraph, the brief's CTA URL missing
    FIX      heading problems, missing alt text, vague link text, title or description length, repeated words,
             length outside the brief, primary keyword missing, dates before the publish date, never-use words
    CLAIM    statistics, prices, superlatives and quotes to check against sources (judgment: blocker if unsupported)

Exit code: 0 if no BLOCKER, 1 if any BLOCKER, 2 on bad input.
"""

import argparse
import datetime
import html
import os
import re
import sys

PLACEHOLDER = re.compile(r"\[(insert|link|add|tbd|todo|placeholder|url|source|stat|name|company)[^\]]*\]|\bTODO\b|\bTBD\b|"
                         r"\bXX+\b|lorem ipsum|\{\{[^}]*\}\}|<placeholder>", re.I)
VAGUE_LINK = {"click here", "here", "read more", "learn more", "this link", "link", "more", "this"}
SUPERLATIVE = re.compile(r"#\s?1\b|\bnumber one\b|\b(best|leading|top-rated|fastest|the only|most trusted|largest|cheapest)\b", re.I)
AFFILIATE = re.compile(r"[?&](ref|aff|affiliate|via|tag|partner)=|/go/|/recommends/", re.I)
DISCLOSURE = re.compile(r"commission|affiliate|sponsored|paid partnership|we may earn", re.I)
MONTHS = {m: i for i, m in enumerate(["january", "february", "march", "april", "may", "june", "july", "august",
                                      "september", "october", "november", "december"], 1)}
SEARCH_CHANNELS = {"blog", "landing", "web", "website", "page", "article"}


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def parse(text, is_html):
    """Return dict: title, description, headings [(level, text)], images [(alt|None, src)], links [(text, url)],
    body (plain text), first_para."""
    d = {"title": None, "description": None, "headings": [], "images": [], "links": []}
    if is_html:
        m = re.search(r"<title>(.*?)</title>", text, re.S | re.I)
        d["title"] = html.unescape(m.group(1).strip()) if m else None
        m = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', text, re.I)
        d["description"] = m.group(1) if m else None
        d["headings"] = [(int(l), re.sub(r"<[^>]+>", "", t).strip()) for l, t in re.findall(r"<h([1-6])[^>]*>(.*?)</h\1>", text, re.S | re.I)]
        for tag in re.findall(r"<img\b[^>]*>", text, re.I):
            alt = re.search(r'\balt=["\'](.*?)["\']', tag, re.I)
            src = re.search(r'\bsrc=["\'](.*?)["\']', tag, re.I)
            d["images"].append((alt.group(1) if alt else None, src.group(1) if src else ""))
        d["links"] = [(re.sub(r"<[^>]+>", "", t).strip(), u) for u, t in re.findall(r'<a\b[^>]*href=["\'](.*?)["\'][^>]*>(.*?)</a>', text, re.S | re.I)]
        body = re.sub(r"<(script|style|head)\b.*?</\1>", " ", text, flags=re.S | re.I)
        body = html.unescape(re.sub(r"<[^>]+>", "\n", body))
    else:
        fm = re.match(r"^---\n(.*?)\n---\n", text, re.S)
        if fm:
            for key in ("title", "description"):
                m = re.search(rf"^{key}\s*:\s*(.+)$", fm.group(1), re.M | re.I)
                if m:
                    d[key] = m.group(1).strip().strip("\"'")
            text = text[fm.end():]
        in_code = False
        for line in text.splitlines():
            if line.strip().startswith("```"):
                in_code = not in_code
            m = re.match(r"^(#{1,6})\s+(.+)$", line)
            if m and not in_code:
                d["headings"].append((len(m.group(1)), m.group(2).strip()))
        d["images"] = [(alt, src) for alt, src in re.findall(r"!\[([^\]]*)\]\(([^)]*)\)", text)]
        d["links"] = [(t, u) for t, u in re.findall(r"(?<!!)\[([^\]]+)\]\(((?:[^()]|\([^)]*\))*)\)", text)]
        body = text
        if not d["title"]:
            d["title"] = next((t for l, t in d["headings"] if l == 1), None)
    d["body"] = body
    paras = [p.strip() for p in re.split(r"\n\s*\n", re.sub(r"^#.*$", "", body, flags=re.M)) if len(p.split()) > 6]
    d["first_para"] = paras[0] if paras else ""
    return d


def parse_brief(path):
    b = {}
    if not path:
        return b
    for line in read(path).splitlines():
        m = re.match(r"^\s*[-*]\s*([\w ]+?)\s*:\s*(.+)$", line)
        if m:
            b[m.group(1).strip().lower()] = m.group(2).strip()
    return b


def brand_rules(brand_dir):
    never, forbidden, corpus = [], [], ""
    if not brand_dir or not os.path.isdir(brand_dir):
        return never, forbidden, corpus
    for name in sorted(os.listdir(brand_dir)):
        if name.endswith(".md"):
            corpus += read(os.path.join(brand_dir, name)) + "\n"
    voice = os.path.join(brand_dir, "voice.md")
    if os.path.exists(voice):
        m = re.search(r"^## Words we never use\n(.*?)(?=^## |\Z)", read(voice), re.M | re.S)
        if m:
            for line in m.group(1).splitlines():
                line = re.sub(r"\[source:[^\]]*\]", "", line).strip("-* ").strip()
                if line and not line.upper().startswith("TBD"):
                    never += [w.strip() for w in line.split(",") if w.strip()]
    rules = os.path.join(brand_dir, "rules.md")
    if os.path.exists(rules):
        m = re.search(r"^## Everywhere\n(.*?)(?=^## |\Z)", read(rules), re.M | re.S)
        for line in (m.group(1).splitlines() if m else []):
            if re.search(r"\b(never|don'?t|do not|avoid)\b", line, re.I):
                forbidden += re.findall(r"[\"“]([^\"”]{2,60})[\"”]", line)
    return never, forbidden, corpus


def phrase_in(text, phrase):
    parts = re.split(r"([\s\-]+)", phrase.lower().strip())
    pat = "".join(r"[\s\-–—]+" if re.fullmatch(r"[\s\-]+", x) else re.escape(x) for x in parts if x)
    return re.search(r"(?<!\w)" + pat, text.lower())


def words(s):
    return re.findall(r"[A-Za-z0-9$%'’]+", s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--brief")
    ap.add_argument("--brand")
    ap.add_argument("--channel", default="")
    ap.add_argument("--publish-date", help="YYYY-MM-DD; defaults to the brief's publish date")
    a = ap.parse_args()
    try:
        raw = read(a.file)
        brief = parse_brief(a.brief)
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    is_html = a.file.lower().endswith((".html", ".htm")) or raw.lstrip().lower().startswith(("<!doctype", "<html"))
    d = parse(raw, is_html)
    body, low = d["body"], d["body"].lower()
    channel = (a.channel or brief.get("channel", "")).split()[0].lower() if (a.channel or brief.get("channel")) else ""
    out = []
    add = lambda level, msg: out.append((level, msg))

    # Placeholders and links
    for m in PLACEHOLDER.finditer(raw):
        add("BLOCKER", f"placeholder left in: \"{m.group(0)}\"")
    for text, url in d["links"]:
        u = url.strip()
        if not u or u == "#" or PLACEHOLDER.search(u):
            add("BLOCKER", f"link \"{text}\" has no real URL ({u or 'empty'})")
        if text.strip().lower().strip(".!") in VAGUE_LINK:
            add("FIX", f"vague link text \"{text}\": say where it goes")
        if AFFILIATE.search(u):
            if DISCLOSURE.search(d["first_para"]):
                add("CLAIM", f"affiliate link {u}: disclosure found in the first paragraph, check its wording")
            else:
                add("BLOCKER", f"affiliate-style link {u} with no disclosure in the first paragraph")
    m = re.search(r"https?://\S+", brief.get("cta", ""))
    if m:
        want = m.group(0).rstrip(").,")
        if not any(want.rstrip("/") == u.strip().rstrip("/") for _, u in d["links"]):
            add("BLOCKER", f"the brief's CTA URL {want} isn't linked anywhere")

    # Structure, search and accessibility
    levels = [l for l, _ in d["headings"]]
    if channel in SEARCH_CHANNELS or is_html or not channel:
        h1 = levels.count(1)
        if h1 == 0:
            add("FIX", "no H1 heading" + (f" (first heading is H{levels[0]})" if levels else ""))
        elif h1 > 1:
            add("FIX", f"{h1} H1 headings; use one")
        if channel in SEARCH_CHANNELS or is_html:
            if not d["title"]:
                add("FIX", "no page title")
            elif len(d["title"]) > 60:
                add("FIX", f"title is {len(d['title'])} characters (keep it under 60): \"{d['title'][:70]}\"")
            if not d["description"]:
                add("FIX", "no meta description")
            elif not 70 <= len(d["description"]) <= 160:
                add("FIX", f"meta description is {len(d['description'])} characters (aim for 70–160)")
    for prev, cur in zip(levels, levels[1:]):
        if cur > prev + 1:
            add("FIX", f"heading level skips from H{prev} to H{cur}")
            break
    for alt, src in d["images"]:
        if alt is None or not alt.strip():
            add("FIX", f"image {src or '(no src)'} has no alt text")
    for m in re.finditer(r"\b(\w+)\s+\1\b", body, re.I):
        if m.group(1).lower() not in {"that", "had", "very", "ha"}:
            add("FIX", f"repeated word: \"{m.group(0)}\"")

    # Brief: length and keyword
    n = len(words(body))
    m = re.search(r"(\d[\d,]*)\s*[–-]\s*(\d[\d,]*)\s*words", brief.get("length", ""))
    if m:
        lo, hi = int(m.group(1).replace(",", "")), int(m.group(2).replace(",", ""))
        if not lo <= n <= hi:
            add("FIX", f"{n} words; the brief asks for {lo}–{hi}")
    kw = brief.get("primary keyword", "").strip().strip("\"'")
    if kw and channel in SEARCH_CHANNELS:
        h1_text = " ".join(t for l, t in d["headings"] if l == 1)
        first100 = " ".join(words(body)[:100])
        missing = [where for where, txt in (("title", d["title"] or ""), ("H1", h1_text), ("first 100 words", first100)) if kw.lower() not in txt.lower()]
        if missing:
            add("FIX", f"primary keyword \"{kw}\" missing from: {', '.join(missing)}")

    # Dates before publish
    pub = a.publish_date or (re.search(r"\d{4}-\d{2}-\d{2}", brief.get("publish date", "")) or [None])[0]
    if pub:
        pd = datetime.date.fromisoformat(pub)
        for mon, day, year in re.findall(r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+(\d{1,2})(?:,?\s+(\d{4}))?", body):
            try:
                dt = datetime.date(int(year or pd.year), MONTHS[mon.lower()], int(day))
            except ValueError:
                continue
            if dt < pd:
                add("FIX", f"\"{mon} {day}\" is before the publish date {pub}")

    # Brand rules
    never, forbidden, corpus = brand_rules(a.brand)
    for w in never:
        if phrase_in(body, w):
            add("FIX", f"never-use word \"{w}\"")
    for p in forbidden:
        if phrase_in(body, p):
            add("BLOCKER", f"\"{p}\" is forbidden by a brand rule")

    # Claims for review
    known = corpus + "\n" + (read(a.brief) if a.brief else "")
    for m in re.finditer(r"[^.!?\n]*?(\$\s?\d[\d,.]*|(?<![\d.,])\d[\d,.]*\s?%|(?<![\d.,])\d[\d,.]*\s+(?:hours|days|weeks|clients|customers|restaurants|clinics|merchants))[^.!?\n]*", body):
        figure = re.sub(r"[\s,]", "", m.group(1))
        lines = [l.strip("-* ").strip() for l in known.splitlines() if figure and figure in re.sub(r"[\s,]", "", l)]
        if lines:
            ctx = re.sub(r"\s*\[source:[^\]]*\]", "", lines[0])[:90]
            status = f"brand memory says: \"{ctx}\" (check it applies to this reader)"
        else:
            status = "NOT in brand memory or the brief"
        add("CLAIM", f"figure {m.group(1).strip()}, {status}: \"{m.group(0).strip()[:90]}\"")
    for m in SUPERLATIVE.finditer(body):
        line = body[max(0, m.start() - 40):m.end() + 40].replace("\n", " ")
        add("CLAIM", f"superlative \"{m.group(0)}\": \"…{line.strip()}…\"")
    flat = lambda x: re.sub(r"\W+", " ", x.lower()).strip()
    for q in re.findall(r"[\"“]([^\"”]{20,300})[\"”]", body):
        line = next((l for l in corpus.splitlines() if flat(q) and flat(q) in flat(l)), None)
        if not line:
            add("BLOCKER" if corpus else "CLAIM", f"quote not recorded word for word in brand memory: \"{q[:70]}\"")
        elif re.search(r"named:\s*(no|unconfirmed)", line, re.I):
            perm = re.search(r"named:\s*(no|unconfirmed)", line, re.I).group(1)
            add("BLOCKER", f"quote is recorded, but permission to name the customer is {perm}: \"{q[:60]}\"")
        else:
            add("CLAIM", f"quote recorded in brand memory: \"{q[:60]}\"")

    order = {"BLOCKER": 0, "FIX": 1, "CLAIM": 2}
    seen = set()
    for level, msg in sorted(out, key=lambda x: order[x[0]]):
        if (level, msg) not in seen:
            seen.add((level, msg))
            print(f"{level} {msg}")
    b = sum(1 for l, _ in seen if l == "BLOCKER")
    f = sum(1 for l, _ in seen if l == "FIX")
    c = sum(1 for l, _ in seen if l == "CLAIM")
    print(f"{'BLOCKED' if b else 'OK'}: {b} blocker, {f} fix, {c} claim(s) to verify; {n} words")
    return 1 if b else 0


if __name__ == "__main__":
    sys.exit(main())
