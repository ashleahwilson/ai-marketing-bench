#!/usr/bin/env python3
"""Check a content brief before it's handed on. Standard library only.

Usage:
    python3 scripts/check_brief.py briefs/<slug>.md [--brand brand/] [--keywords research/keywords.csv]
                                   [--request "the user's request text"]

Checks:
  FAIL   a missing or empty field of the nine content-qa-gate reads; a field name repeated later in the file
         (content-qa-gate keeps the last one); a CTA with no URL and no TBD; a Length that isn't
         "<low>-<high> words"; a Publish date that isn't YYYY-MM-DD or TBD; a primary keyword line carrying
         numbers, brackets or notes; a figure attached to a keyword with no keyword data supplied
  CHECK  every figure in the brief that isn't found in brand memory, the keyword data or the request;
         a phrase brand rules forbid, or a never-use word, outside the Avoid section; a held claim
         ("Needs substantiation" in claims.md) outside the Avoid section; keyword status not stated
  OK     a summary of what passed
Exit code: 1 if any FAIL, else 0.
"""

import argparse
import csv
import os
import re
import sys

FIELDS = ["goal", "audience", "channel", "key message", "must include", "cta",
          "primary keyword", "length", "publish date"]
SEARCH_CHANNELS = {"blog", "landing", "web", "article", "seo"}


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def strip_tags(s):
    return re.sub(r"\[source:[^\]]*\]", "", s)


def brand_corpus(brand_dir):
    text, never, forbidden, held = "", [], [], []
    if not brand_dir or not os.path.isdir(brand_dir):
        return text, never, forbidden, held
    for name in sorted(os.listdir(brand_dir)):
        if name.endswith(".md"):
            text += read(os.path.join(brand_dir, name)) + "\n"
    voice = os.path.join(brand_dir, "voice.md")
    if os.path.exists(voice):
        m = re.search(r"^## Words we never use\n(.*?)(?=^## |\Z)", read(voice), re.M | re.S)
        for line in (m.group(1).splitlines() if m else []):
            line = strip_tags(line).strip("-* ").strip()
            if line and not line.upper().startswith("TBD"):
                never += [w.strip() for w in line.split(",") if w.strip()]
    rules = os.path.join(brand_dir, "rules.md")
    if os.path.exists(rules):
        m = re.search(r"^## Everywhere\n(.*?)(?=^## |\Z)", read(rules), re.M | re.S)
        for line in (m.group(1).splitlines() if m else []):
            if re.search(r"\b(never|don'?t|do not|avoid)\b", line, re.I):
                forbidden += re.findall(r"[\"“]([^\"”]{2,60})[\"”]", line)
    claims = os.path.join(brand_dir, "claims.md")
    if os.path.exists(claims):
        m = re.search(r"^## Needs substantiation\n(.*?)(?=^## |\Z)", read(claims), re.M | re.S)
        for line in (m.group(1).splitlines() if m else []):
            held += re.findall(r"[\"“]([^\"”]{2,80})[\"”]", line)
    return text, never, forbidden, held


def keyword_rows(path):
    if not path:
        return [], ""
    raw = read(path)
    rows = []
    try:
        rows = list(csv.reader(raw.splitlines()))
    except csv.Error:
        pass
    return rows, raw


def phrase_in(text, phrase):
    parts = re.split(r"([\s\-]+)", phrase.lower().strip())
    pat = "".join(r"[\s\-–—]+" if re.fullmatch(r"[\s\-]+", x) else re.escape(x) for x in parts if x)
    return re.search(r"(?<!\w)" + pat, text.lower())


def norm_num(s):
    return s.replace(",", "").rstrip(".")


def figures(text):
    """Figures worth tracing: money, percentages, numbers with units or of 2+ digits. Skips dates and URLs."""
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"\b\d{4}-\d{2}-\d{2}\b", " ", text)
    text = re.sub(r"^\s*\d+\.\s", " ", text, flags=re.M)      # numbered list markers
    text = re.sub(r"^#+.*$", " ", text, flags=re.M)            # headings
    out = []
    for m in re.finditer(r"\$?\d[\d,]*(?:\.\d+)?\s?(?:%|percent|k\b|x\b)?", text):
        tok = m.group(0).strip()
        digits = re.sub(r"[^\d.]", "", tok)
        if not digits:
            continue
        if tok.startswith("$") or tok.endswith(("%", "percent", "k", "x")) or len(digits.replace(".", "")) >= 2:
            out.append(tok)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("brief")
    ap.add_argument("--brand")
    ap.add_argument("--keywords")
    ap.add_argument("--request", default="")
    a = ap.parse_args()

    text = read(a.brief)
    res = []
    add = lambda lvl, msg: res.append((lvl, msg))

    # 1. The nine fields, as content-qa-gate parses them (every "- words: value" line; the last one wins).
    seen, values = {}, {}
    for i, line in enumerate(text.splitlines(), 1):
        m = re.match(r"^\s*[-*]\s*([\w ]+?)\s*:\s*(.*)$", line)
        if m:
            key = m.group(1).strip().lower()
            if key in FIELDS:
                seen.setdefault(key, []).append(i)
                values[key] = m.group(2).strip()
    for f in FIELDS:
        if f not in seen:
            add("FAIL", f"no '- {f.capitalize()}:' line")
        elif not values[f]:
            add("FAIL", f"'{f.capitalize()}' is empty (write TBD: <what's missing> instead)")
        elif len(seen[f]) > 1:
            add("FAIL", f"'{f.capitalize()}' appears on lines {seen[f]}; content-qa-gate keeps the last one. "
                        "Reword the later bullet so it doesn't start with the field name and a colon")
    tbd = [f for f in FIELDS if re.search(r"\bTBD\b", values.get(f, ""))]

    cta = values.get("cta", "")
    if cta and not re.search(r"https?://\S+", cta) and "TBD" not in cta:
        add("FAIL", "CTA has no URL; add the real one or write → TBD: URL")
    length = values.get("length", "")
    if length and "TBD" not in length and not re.search(r"\d[\d,]*\s*[–-]\s*\d[\d,]*\s*words", length):
        add("FAIL", f"Length '{length}' must read '<low>–<high> words'")
    pub = values.get("publish date", "")
    if pub and "TBD" not in pub and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", pub):
        add("FAIL", f"Publish date '{pub}' must be YYYY-MM-DD or TBD")
    kw = values.get("primary keyword", "")
    if kw and "TBD" not in kw and (re.search(r"\d|\(|\[|unvalidated|volume|/mo", kw, re.I)):
        add("FAIL", f"Primary keyword '{kw}' must be the keyword phrase only (status and figures go under ### Search)")

    # 2. Sections: everything after "## For the writer"; Avoid is exempt from banned-phrase checks.
    split = re.split(r"^## For the writer\s*$", text, maxsplit=1, flags=re.M)
    if len(split) < 2:
        add("CHECK", "no '## For the writer' section after the fields")
    avoid = re.search(r"^###\s*Avoid\b.*?(?=^###|\Z)", text, re.M | re.S)
    outside_avoid = text.replace(avoid.group(0), "") if avoid else text

    corpus, never, forbidden, held = brand_corpus(a.brand)
    rows, kw_raw = keyword_rows(a.keywords)
    sources = corpus + "\n" + kw_raw + "\n" + a.request

    # 3. Keyword status and keyword figures.
    channel = values.get("channel", "").split()[0].lower().strip(",") if values.get("channel") else ""
    has_status = re.search(r"keyword status\s*:", text, re.I)
    if not a.keywords:
        if channel in SEARCH_CHANNELS and not re.search(r"unvalidated", text, re.I):
            add("CHECK", "no keyword data was supplied, but the brief doesn't mark the keyword unvalidated")
        if re.search(r"\b\d[\d,]*\s*(?:searches|monthly searches|/mo\b|per month|search volume)|(?:volume|difficulty|KD)\s*[:=]?\s*\d", text, re.I):
            add("FAIL", "a search volume or difficulty figure appears, but no keyword data was supplied")
    elif channel in SEARCH_CHANNELS and not has_status:
        add("CHECK", "say under ### Search which keyword data the keyword was chosen from")
    if a.keywords and kw and "TBD" not in kw:
        listed = [r[0].strip().lower() for r in rows[1:] if r]
        if kw.strip("\"' ").lower() not in listed:
            add("CHECK", f"primary keyword '{kw}' isn't in the keyword data")

    # 4. Figures traced to brand memory, keyword data or the request.
    plain_sources = norm_num(sources)
    lines_to_scan = "\n".join(l for l in outside_avoid.splitlines()
                              if not re.match(r"^\s*[-*]\s*(length|publish date)\s*:", l, re.I))
    missing = []
    for tok in figures(lines_to_scan):
        core = norm_num(re.sub(r"\s?(percent|k|x)$", "", tok).replace(" ", ""))
        bare = core.lstrip("$").rstrip("%")
        if bare and bare not in plain_sources:
            missing.append(tok)
    for tok in sorted(set(missing)):
        add("CHECK", f"figure '{tok}' isn't in brand memory, the keyword data or the request: trace it or remove it")

    # 5. Banned phrases, never-use words and held claims outside Avoid.
    body_lower = outside_avoid
    for p in forbidden:
        if phrase_in(body_lower, p):
            add("CHECK", f"'{p}' is forbidden by brand rules and appears outside Avoid")
    for w in never:
        if phrase_in(body_lower, w):
            add("CHECK", f"never-use word '{w}' appears outside Avoid")
    for h in held:
        if phrase_in(body_lower, h):
            add("CHECK", f"held claim '{h}' (needs substantiation) appears outside Avoid")
    if not a.brand or not os.path.isdir(a.brand):
        if not re.search(r"provisional", text, re.I):
            add("CHECK", "no brand memory: mark the brief 'Status: provisional (no brand memory)'")

    fails = [r for r in res if r[0] == "FAIL"]
    for lvl, msg in res:
        print(f"{lvl:<6} {msg}")
    print(f"OK     {sum(1 for f in FIELDS if f in seen)}/9 fields present"
          + (f"; TBD: {', '.join(tbd)}" if tbd else "")
          + f"; {len([r for r in res if r[0] == 'CHECK'])} item(s) to check")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
