#!/usr/bin/env python3
"""Measure how a brand shows up in words across saved pages and channel pieces. Standard library only.
Reads files; never fetches.

Usage:
    python3 scripts/brand_scan.py site/*.html channels/*.md --company "Tallyhouse"
    python3 scripts/brand_scan.py site/*.html --company "Tallyhouse" --brand brand/
    python3 scripts/brand_scan.py site/*.md --json > scan.json

Inputs: .html/.htm pages (visible text, titles, images and links are read) and .md/.txt pieces. A .md/.txt file
holding several posts is split on lines of '---' or headings starting 'Post', and each part is measured alone.

Reports:
  VOICE      per piece: words, sentences (4+ words), average and spread of sentence length, contractions per
             100 words, person (we / you / I / the company in the third person), future "will" per 100 words,
             spelling forms found, stock words, exclamation marks, hashtags. Customer quotes (blockquotes) are
             left out of voice measures because they are the customer's voice, not the brand's.
  SPELLING   the convention each piece uses (US, Canadian, British) and whether the set mixes them
  OUTLIERS   pieces whose register differs from the rest (sentence length, contractions, person)
  NAMING     terms that appear in more than one written form (TallyHouse / Tallyhouse, Deal Radar / DealRadar)
  TRUST      per page: email, phone, street address, policy links, testimonials (named or role-only),
             ratings (with or without a named source), credentials, team mentions, vague proof phrases
  ASSETS     HTML only: images with no alt text or a filename or generic alt, page title formats, placeholders
  BRAND      with --brand: whose brand memory it is. Only if BRAND.md names the --company are its rules used:
             never-use words, forbidden phrases, stated spelling, product-name forms, channel limits,
             claims that need substantiation, quotes whose naming permission is unconfirmed, and figures
             not found anywhere in brand memory.
  NOT OBSERVABLE  what words can't show (logo, colour palette, typography, imagery)

Exit code: 0 on success, 2 on bad input.
"""

import argparse
import json
import os
import re
import statistics
import sys
from html.parser import HTMLParser

BLOCK = {"p", "li", "h1", "h2", "h3", "h4", "h5", "h6", "div", "blockquote", "footer", "nav", "td", "th", "br",
         "section", "article", "header", "tr", "ul", "ol", "form", "button", "a", "title", "figcaption"}
SKIP_VOICE = {"nav", "footer", "blockquote", "script", "style", "title", "button"}

STOCK = ["in today's fast-paced", "fast-paced world", "landscape", "delve", "tapestry", "testament to", "pivotal",
         "game-changer", "game-changing", "cutting-edge", "unlock", "unlocking", "elevate", "empower", "empowering",
         "empowers", "leverage", "leverages", "seamless", "seamlessly", "streamline", "robust", "holistic",
         "best-in-class", "world-class", "solutions", "solution", "stakeholders", "ecosystem", "cross-functional", "synergy",
         "actionable insights", "data-driven", "innovative", "enterprise-grade", "revolutionize", "revolutionise",
         "transformative", "next level", "full potential", "committed to delivering", "drive results",
         "at scale", "thrilled", "excited to announce", "valued customer", "passionate about"]

# (US form, Commonwealth form) stems. Canadian and British share the Commonwealth forms here.
PAIRS = [("color", "colour"), ("labor", "labour"), ("favor", "favour"), ("behavior", "behaviour"), ("honor", "honour"),
         ("neighbor", "neighbour"), ("flavor", "flavour"), ("humor", "humour"), ("center", "centre"),
         ("theater", "theatre"), ("liter", "litre"), ("catalog", "catalogue"), ("defense", "defence"),
         ("gray", "grey"), ("jewelry", "jewellery"), ("traveled", "travelled"), ("traveling", "travelling"),
         ("canceled", "cancelled"), ("canceling", "cancelling"), ("modeling", "modelling")]
SUFFIX = r"(?:s|es|d|ed|ing|ite|ites|ful|ly|ers?)?"
IZE_STEMS = ["organ", "optim", "maxim", "minim", "priorit", "real", "recogn", "custom", "final", "util", "special",
             "apolog", "summar", "standard", "central", "personal", "author", "capital", "emphas", "categor",
             "visual", "normal", "synchron", "digit", "monet", "critic", "modern", "stabil", "memor", "general"]
IZE_RE = re.compile(r"\b(" + "|".join(IZE_STEMS) + r")(is|iz)(e|es|ed|ing|ation|ations|er|ers)\b", re.I)
ANALY_RE = re.compile(r"\banaly(s|z)(e|es|ed|ing)\b", re.I)

CONTRACTION = re.compile(r"\b\w+(?:n['’]t|['’](?:re|ve|ll|d|m))\b|\b(?:it|that|there|here|what|who|let|he|she|where|how)['’]s\b", re.I)
WE = re.compile(r"\b(?:we|our|ours|us|we're|we'll|we've|we'd)\b", re.I)
YOU = re.compile(r"\b(?:you|your|yours|you're|you'll|you've|you'd)\b", re.I)
I_ = re.compile(r"\b(?:I|my|me|I'm|I've|I'll)\b")
FUTURE = re.compile(r"\b(?:will|won't|\w+'ll)\b", re.I)
SELF_VERBS = r"(?:is|was|provides|offers|enables|delivers|has|seeks|helps|connects|pulls|reads|shows|does|serves|comprises|believes|was founded)"

EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
PHONE = re.compile(r"(?:\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}")
ADDRESS = re.compile(r"\b\d{1,5} [A-Z][\w.]*(?: [A-Z][\w.]*)* (?:St|Street|Ave|Avenue|Rd|Road|Blvd|Boulevard|Way|Dr|Drive|Lane|Ln|Pl|Place|Cres|Sq)\b\.?")
POLICY = re.compile(r"\b(privacy|terms|refund|cancellation|cookie|accessibility|returns?)\b", re.I)
RATING = re.compile(r"\b\d(?:\.\d)?\s*/\s*5\b|★|\b\d(?:\.\d)?\s*stars?\b|\brated\b", re.I)
RATING_SOURCE = re.compile(r"\b(G2|Capterra|Google|Trustpilot|Yelp|App Store|Google Play|TrustRadius|BBB)\b")
CREDENTIAL = re.compile(r"\b(CPA|CA|CFA|certified|licensed|accredited|registered|SOC ?2|ISO ?27001|HIPAA|PIPEDA|GDPR|member of)\b")
TEAM = re.compile(r"\b(founded (?:in \d{4} )?by|founders?|CEO|CTO|team of \d+|our team|we.re \d+ people|\d+ of us)\b", re.I)
VAGUE = re.compile(r"\b(trusted by|worldwide|industry-leading|leading|thousands of|hundreds of|countless|"
                   r"companies of all sizes|teams of every size|\d[\d,]*\+)", re.I)
PLACEHOLDER = re.compile(r"lorem ipsum|\bTBD\b|\bTODO\b|\[placeholder\]|\bXXX\b|coming soon|your text here|\{\{", re.I)
FIGURE = re.compile(r"\$\s?\d[\d,.]*(?:/\w+)?|\b\d[\d,.]*\s?(?:%|percent|hours?|days?|weeks?|minutes?|months?|x\b|\+)"
                    r"|\b\d(?:\.\d)?\s*/\s*5\b", re.I)
FILENAME_ALT = re.compile(r"\.(?:jpe?g|png|gif|webp|svg)$|^(?:img|image|dsc|photo|pic)[_-]?\d*$", re.I)
GENERIC_ALT = {"image", "photo", "picture", "logo", "banner", "graphic", "icon", "customer logos", "logos", "screenshot", "hero"}
STOP = {"the", "a", "an", "of", "and", "to", "for", "you", "your", "what", "how", "our", "we", "in", "on", "with",
        "new", "why", "about", "at", "by", "is", "it", "get", "from", "subject", "hi", "post", "dear"}


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack, self.voice, self.all, self.quotes = [], [], [], []
        self.title, self.images, self.links, self._href, self._ltext = "", [], [], None, []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in BLOCK:
            self.voice.append("\n")
            self.all.append("\n")
        if tag not in ("br", "img", "meta", "link", "input"):
            self.stack.append(tag)
        if tag == "img":
            self.images.append({"src": a.get("src", ""), "alt": a.get("alt")})
        if tag == "a":
            self._href, self._ltext = a.get("href", ""), []

    def handle_endtag(self, tag):
        if tag == "a" and self._href is not None:
            self.links.append({"href": self._href, "text": " ".join("".join(self._ltext).split())})
            self._href = None
        if tag in self.stack:
            while self.stack and self.stack.pop() != tag:
                pass
        if tag in BLOCK:
            self.voice.append("\n")
            self.all.append("\n")

    def handle_data(self, data):
        if "script" in self.stack or "style" in self.stack:
            return
        if "title" in self.stack:
            self.title += data
            return
        self.all.append(data)
        if self._href is not None:
            self._ltext.append(data)
        if "blockquote" in self.stack:
            self.quotes.append(" ".join(data.split()))
        if not any(t in SKIP_VOICE for t in self.stack):
            self.voice.append(data)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def strip_md(text):
    quotes = re.findall(r"^\s*>\s?(.*)$", text, re.M)
    voice = re.sub(r"^\s*>.*$", "", text, flags=re.M)
    clean = lambda s: re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", re.sub(r"^\s*(#+|[-*]|\d+\.)\s+", "", s, flags=re.M)).replace("**", "").replace("__", "")
    return clean(voice), clean(text), quotes


def load_pieces(paths):
    pieces = []
    for p in paths:
        name = os.path.basename(p)
        raw = read(p)
        if p.lower().endswith((".html", ".htm")):
            pg = Page()
            pg.feed(raw)
            pieces.append({"name": name, "kind": "html", "title": " ".join(pg.title.split()), "voice": "".join(pg.voice),
                           "all": "".join(pg.all), "quotes": pg.quotes, "images": pg.images, "links": pg.links, "raw": raw})
            continue
        parts = re.split(r"(?m)^\s*---\s*$|(?=^#{1,3}\s*Post\b)", raw)
        parts = [x for x in parts if x and x.strip()]
        for i, part in enumerate(parts, 1):
            voice, alltext, quotes = strip_md(part)
            links = [{"href": h, "text": t} for t, h in re.findall(r"\[([^\]]*)\]\(([^)]*)\)", part)]
            label = name if len(parts) == 1 else f"{name}#{i}"
            pieces.append({"name": label, "kind": "text", "title": "", "voice": voice, "all": alltext,
                           "quotes": quotes, "images": [], "links": links, "raw": part})
    return pieces


def sentences(text):
    out = []
    for line in text.split("\n"):
        for s in re.split(r"(?<=[.!?])\s+", line.strip()):
            w = re.findall(r"[A-Za-z0-9$%'’&-]+", s)
            if len(w) >= 4:
                out.append(w)
    return out


def spelling(text):
    us, cw, ise, ize = [], [], [], []
    for a, b in PAIRS:
        us += [m.group(0) for m in re.finditer(rf"\b{a}{SUFFIX}\b", text, re.I)]
        cw += [m.group(0) for m in re.finditer(rf"\b{b}{SUFFIX}\b", text, re.I)]
    for m in IZE_RE.finditer(text):
        (ise if m.group(2).lower() == "is" else ize).append(m.group(0))
    for m in ANALY_RE.finditer(text):
        (ise if m.group(1).lower() == "s" else ize).append(m.group(0))
    return us, cw, ise, ize


def convention(us, cw, ise, ize):
    if us and cw:
        return "mixed (US and Commonwealth forms)"
    if ise and ize:
        return "mixed (-ise and -ize)"
    if cw:
        return "British" if ise else ("Canadian" if ize else "Canadian or British")
    if us:
        return "British-leaning? check" if ise else "US"
    if ise:
        return "British"
    return "no marker words"


def stock_words(text, name_keys):
    found = []
    low = text.lower()
    for w in STOCK:
        for m in re.finditer(r"(?<![\w-])" + re.escape(w) + r"(?![\w-])", low):
            nxt = re.match(r"[\s-]*(\w+)", low[m.end():])
            key = (w + (nxt.group(1) if nxt else "")).replace(" ", "").replace("-", "")
            if key in name_keys:
                continue  # part of a product name such as "Seamless Sync"
            found.append(w)
    return found


def voice_metrics(pc, name_keys, company):
    text = pc["voice"]
    words = re.findall(r"[A-Za-z0-9$%'’&-]+", text)
    n = max(len(words), 1)
    sents = sentences(text)
    lens = [len(s) for s in sents]
    us, cw, ise, ize = spelling(pc["all"])
    third = 0
    if company:
        third += len(re.findall(rf"\b{re.escape(company)}(?:\s+Inc\.?)?\s+{SELF_VERBS}\b", text, re.I))
    third += len(re.findall(r"\bthe (?:company|organization|organisation|firm|team at)\b", text, re.I))
    return {
        "words": len(words), "sentences": len(sents),
        "avg_sentence": round(statistics.mean(lens), 1) if lens else 0,
        "sentence_spread": round(statistics.pstdev(lens), 1) if len(lens) > 1 else 0,
        "contractions_per_100": round(100 * len(CONTRACTION.findall(text)) / n, 1),
        "we": len(WE.findall(text)), "you": len(YOU.findall(text)), "i": len(I_.findall(text)), "third_person_self": third,
        "will_per_100": round(100 * len(FUTURE.findall(text)) / n, 1),
        "spelling": {"us": us, "commonwealth": cw, "ise": ise, "ize": ize, "convention": convention(us, cw, ise, ize)},
        "stock": stock_words(text, name_keys),
        "exclamations": pc["raw"].count("!") if pc["kind"] == "text" else text.count("!"),
        "hashtags": len(re.findall(r"(?<![\w&])#[A-Za-z]\w+", pc["raw"] if pc["kind"] == "text" else text)),
    }


URLISH = re.compile(r"\S+@\S+|https?://\S+|\b[\w-]+\.(?:example|com|ca|io|co|net|org)\b\S*", re.I)
CAND = re.compile(r"\b[A-Z][a-z]+[A-Z][A-Za-z]+\b|\b[A-Z][a-z]+(?:[ -][A-Z][a-z]+){1,2}\b")


def naming(pieces, extra_terms):
    """Group terms that appear in more than one written form across the pieces."""
    texts = {pc["name"]: URLISH.sub(" ", pc["all"] + "\n" + pc["title"]) for pc in pieces}
    ordered = {}
    for text in texts.values():
        for line in text.split("\n"):
            for m in CAND.finditer(line):
                parts = re.findall(r"[A-Z][a-z]+", m.group(0))
                if len(parts) < 2 or all(p.lower() in STOP for p in parts):
                    continue
                ordered.setdefault("".join(parts).lower(), [p.lower() for p in parts])
    for t in extra_terms:
        parts = [p.lower() for p in re.findall(r"[A-Z]?[a-z]+", t)]
        if parts:
            ordered.setdefault("".join(parts), parts)
    groups = []
    for key, parts in ordered.items():
        rx = re.compile(r"(?<![\w-])" + r"[\s-]?".join(map(re.escape, parts)) + r"(?![\w-])", re.I)
        forms = {}
        for name, text in texts.items():
            for m in rx.finditer(text):
                forms.setdefault(m.group(0), set()).add(name)
        # a capital letter only at the start of a sentence or heading isn't a second form
        if len({f[:1].lower() + f[1:] for f in forms}) > 1:
            groups.append({"term": key, "forms": {f: sorted(w) for f, w in forms.items()}})
    return groups


def trust(pc):
    text = pc["all"]
    hrefs = " ".join(l["href"] + " " + l["text"] for l in pc["links"])
    quotes = pc["quotes"] or [f'"{q}" {a}' for q, a in re.findall(r"[\"“]([^\"”]{15,})[\"”]\s*[—–-]?\s*([^\n]{0,80})", text)]
    tests = []
    for q in quotes or []:
        att = re.search(r"[\"”]\s*[—–-]?\s*(.*)$", q)
        tail = att.group(1) if att else ""
        named = bool(re.search(r"\b[A-Z][a-z]+ [A-Z][a-z'-]+\b", tail))
        tests.append({"quote": q[:140], "attribution": tail.strip()[:80], "named_person": named})
    ratings, seen = [], set()
    for line in text.split("\n"):
        if RATING.search(line) and line.strip() not in seen:
            seen.add(line.strip())
            ratings.append({"text": " ".join(line.split())[:160], "source_named": bool(RATING_SOURCE.search(line))})
    vague = {}
    for m in VAGUE.finditer(text):
        line = next((l for l in text.split("\n") if m.group(0) in l), "")
        vague.setdefault(" ".join(line.split())[:160], None)
    return {
        "email": sorted(set(EMAIL.findall(text + " " + hrefs))),
        "phone": sorted(set(PHONE.findall(text))),
        "address": sorted(set(ADDRESS.findall(text))),
        "policy_links": sorted(set(m.group(1).lower() for m in POLICY.finditer(hrefs))),
        "testimonials": tests,
        "ratings": ratings,
        "credentials": sorted(set(CREDENTIAL.findall(text))),
        "team": sorted(set(m.group(1) for m in TEAM.finditer(text))),
        "vague_proof": list(vague),
    }


def assets(pc, company):
    out = {"images": [], "title": pc["title"], "title_format": "", "placeholders": []}
    for im in pc["images"]:
        alt = im["alt"]
        if alt is None or not alt.strip():
            issue = "no alt text"
        elif FILENAME_ALT.search(alt.strip()):
            issue = "alt is a filename"
        elif alt.strip().lower() in GENERIC_ALT:
            issue = "alt names nothing specific"
        else:
            issue = ""
        out["images"].append({"src": im["src"], "alt": alt, "issue": issue})
    t = pc["title"]
    if t:
        sep = next((s for s in (" | ", " – ", " — ", " - ", ": ") if s in t), "")
        if company and company.lower() in t.lower():
            pos = "brand first" if t.lower().startswith(company.lower()) else "brand last"
        else:
            pos = "no brand name"
        out["title_format"] = f"{pos}, separator '{sep.strip() or 'none'}'"
    out["placeholders"] = sorted(set(m.group(0) for m in PLACEHOLDER.finditer(pc["all"] + " " + " ".join(i["src"] for i in pc["images"]))))
    return out


def norm(s):
    return " ".join(re.findall(r"[a-z0-9$%]+", s.lower()))


def ngram_hit(needle, hay, n=5):
    t = norm(needle).split()
    h = " " + norm(hay) + " "
    if len(t) < n:
        return (" " + " ".join(t) + " ") in h if t else False
    return any((" " + " ".join(t[i:i + n]) + " ") in h for i in range(len(t) - n + 1))


def section(text, heading, level=2):
    hashes = "#" * level
    m = re.search(rf"^{hashes}\s+{re.escape(heading)}[^\n]*\n(.*?)(?=^#{{1,{level}}}\s|\Z)", text, re.I | re.M | re.S)
    return m.group(1) if m else ""


def bullets(text):
    return [re.sub(r"\[source:[^\]]*\]", "", l.strip()[1:]).strip() for l in text.splitlines() if l.strip().startswith(("-", "*"))]


def brand_owner(brand_dir):
    p = os.path.join(brand_dir, "BRAND.md")
    if not os.path.isfile(p):
        return None
    m = re.search(r"^#\s*Brand memory:\s*(.+)$", read(p), re.M)
    return m.group(1).strip() if m else ""


def same_company(a, b):
    k = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
    a, b = k(a), k(b)
    return bool(a and b) and (a in b or b in a)


def load_brand(brand_dir):
    get = lambda f: read(os.path.join(brand_dir, f)) if os.path.isfile(os.path.join(brand_dir, f)) else ""
    voice, rules, claims, proof = get("voice.md"), get("rules.md"), get("claims.md"), get("proof.md")
    corpus = "\n".join(get(f) for f in sorted(os.listdir(brand_dir)) if f.endswith(".md"))
    b = {"never": [], "forbidden": [], "spelling": None, "terms": [], "channels": {}, "claims": [], "unconfirmed": [], "corpus": corpus}
    for line in bullets(section(voice, "Words we never use")):
        if not line.upper().startswith("TBD"):
            b["never"] += [w.strip().strip("'\"“”") for w in re.sub(r"\(.*?\)", "", line).split(",") if w.strip()]
    for line in bullets(section(rules, "Everywhere")):
        if re.search(r"\b(never|don'?t|do not|avoid|no)\b", line, re.I):
            b["forbidden"] += re.findall(r"[\"“]([^\"”]{2,60})[\"”]", line) + re.findall(r"(?<!\w)'([^']{2,60})'(?!\w)", line)
    m = re.search(r"\b(US|American|UK|British|Canadian)\s+spelling\b", voice, re.I)
    if m:
        b["spelling"] = {"us": "US", "american": "US", "uk": "British", "british": "British", "canadian": "Canadian"}[m.group(1).lower()]
    for line in bullets(section(voice, "Words we use")):
        for item in re.sub(r"\(.*?\)", "", line).split(","):
            item = item.strip()
            if re.search(r"[A-Z]", item) and len(item.split()) <= 4 and not re.fullmatch(r"[A-Z&%]+", item):
                b["terms"].append(item)
    for mm in re.finditer(r"^###\s+(.+?)\s*\n(.*?)(?=^###\s|^##\s|\Z)", section(voice, "By channel"), re.M | re.S):
        b["channels"][mm.group(1).strip().lower()] = " ".join(bullets(mm.group(2))).lower()
    for line in bullets(section(claims, "Needs substantiation")):
        q = re.findall(r"[\"“]([^\"”]{6,})[\"”]", line)
        if q:
            b["claims"].append(q[0])
    for line in proof.splitlines():
        if re.search(r"named:\s*(unconfirmed|no|tbd)", line, re.I):
            q = re.findall(r"[\"“]([^\"”]{10,})[\"”]", line)
            who = re.findall(r"\b([A-Z][a-z]+ [A-Z][a-z'-]+)\b", line.split(":")[0])
            b["unconfirmed"].append({"quote": q[0] if q else "", "who": who[-1] if who else line[:60]})
    return b


def channel_of(name):
    n = name.lower()
    if "linkedin" in n:
        return "linkedin"
    if any(k in n for k in ("email", "newsletter", "mail")):
        return "email"
    if any(k in n for k in ("instagram", "social", "x-posts", "twitter")):
        return "social"
    return ""


def limits(rule):
    lim = {}
    m = re.search(r"under (\d+) words", rule)
    if m:
        lim["words"] = int(m.group(1))
    if re.search(r"no exclamation", rule):
        lim["exclaim"] = 0
    else:
        m = re.search(r"(one|two|three|\d+) exclamation", rule)
        if m:
            lim["exclaim"] = {"one": 1, "two": 2, "three": 3}.get(m.group(1)) or int(m.group(1))
    if re.search(r"no hashtags", rule):
        lim["hashtags"] = 0
    return lim


def phrase_rx(p):
    """A phrase as a regex where spaces and hyphens match each other ('real-time' finds 'real time')."""
    return r"[\s-]+".join(re.escape(w) for w in re.split(r"[\s-]+", p.lower().strip()) if w)


def brand_checks(b, pieces, metrics):
    out = []
    add = lambda kind, where, msg: out.append({"kind": kind, "where": where, "detail": msg})
    for pc in pieces:
        text = pc["all"] + "\n" + pc["title"]
        low = text.lower()
        for w in b["never"]:
            if re.search(r"(?<![\w-])" + phrase_rx(w) + r"(?:s|d|ed|ing)?(?![\w-])", low):
                add("never-use word", pc["name"], f"'{w}' is on the never-use list in voice.md")
        for p in b["forbidden"]:
            if re.search(r"(?<![\w-])" + phrase_rx(p) + r"(?![\w])", low):
                add("rule breach", pc["name"], f"'{p}' is forbidden by rules.md")
        sp = metrics[pc["name"]]["spelling"]
        if b["spelling"] == "US" and (sp["commonwealth"] or sp["ise"]):
            add("spelling", pc["name"], f"brand memory says US spelling; found {', '.join(sp['commonwealth'] + sp['ise'])}")
        if b["spelling"] == "Canadian" and (sp["us"] or sp["ise"]):
            add("spelling", pc["name"], f"brand memory says Canadian spelling; found {', '.join(sp['us'] + sp['ise'])}")
        if b["spelling"] == "British" and (sp["us"] or sp["ize"]):
            add("spelling", pc["name"], f"brand memory says British spelling; found {', '.join(sp['us'] + sp['ize'])}")
        for t in b["terms"]:
            parts = re.findall(r"[A-Za-z]+", t)
            rx = re.compile(r"\b" + r"[\s-]?".join(map(re.escape, parts)) + r"\b", re.I)
            bad = sorted(set(m.group(0) for m in rx.finditer(text) if m.group(0) != t))
            if bad:
                add("product-name form", pc["name"], f"brand memory writes '{t}'; found {', '.join(repr(x) for x in bad)}")
        for c in b["claims"]:
            if ngram_hit(c, text):
                add("claim needs substantiation", pc["name"], f"\"{c}\" is listed under Needs substantiation in claims.md")
        for u in b["unconfirmed"]:
            if (u["quote"] and ngram_hit(u["quote"], text)) or (u["who"] and u["who"] in text):
                add("naming permission", pc["name"], f"{u['who']}: proof.md records naming permission as unconfirmed")
        ch = channel_of(pc["name"])
        if ch:
            rule = next((v for k, v in b["channels"].items() if k.startswith(ch) or ch.startswith(k)), "")
            lim, m = limits(rule), metrics[pc["name"]]
            if "words" in lim and m["words"] >= lim["words"]:
                add("channel rule", pc["name"], f"{m['words']} words; the {ch} rule is under {lim['words']}")
            if "exclaim" in lim and m["exclamations"] > lim["exclaim"]:
                add("channel rule", pc["name"], f"{m['exclamations']} exclamation mark(s); the {ch} rule allows {lim['exclaim']}")
            if "hashtags" in lim and m["hashtags"] > lim["hashtags"]:
                add("channel rule", pc["name"], f"{m['hashtags']} hashtag(s); the {ch} rule allows none")
        corpus = norm(b["corpus"])
        for f in sorted(set(FIGURE.findall(text))):
            if norm(f) and norm(f) not in corpus:
                add("figure not in brand memory", pc["name"], f"'{f.strip()}' is not recorded anywhere in brand memory")
    return out


def outliers(metrics):
    out = []
    names = [n for n, m in metrics.items() if m["sentences"] >= 2]
    if len(names) < 3:
        return out
    med_len = statistics.median(metrics[n]["avg_sentence"] for n in names)
    med_con = statistics.median(metrics[n]["contractions_per_100"] for n in names)
    for n in names:
        m = metrics[n]
        if med_len and (m["avg_sentence"] > 1.5 * med_len or m["avg_sentence"] < 0.6 * med_len):
            out.append(f"{n}: average sentence {m['avg_sentence']} words against a median of {med_len}")
        if med_con >= 1.0 and m["contractions_per_100"] == 0:
            out.append(f"{n}: no contractions, while the median piece has {med_con} per 100 words")
        if m["third_person_self"] >= 2 and not m["we"]:
            out.append(f"{n}: refers to the company in the third person ({m['third_person_self']}x) and never says 'we'")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--company", default="")
    ap.add_argument("--brand")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    paths = [f for f in a.files if os.path.isfile(f)]
    missing = [f for f in a.files if not os.path.isfile(f)]
    if not paths:
        print("error: no readable files", file=sys.stderr)
        return 2
    pieces = load_pieces(paths)

    owner, b, brand_note = None, None, "no brand/ folder given"
    if a.brand:
        owner = brand_owner(a.brand)
        if owner is None:
            brand_note = f"{a.brand} has no BRAND.md: not used"
        elif not a.company:
            brand_note = f"brand memory belongs to '{owner}'. Pass --company to confirm it is the audited company before using it"
        elif same_company(owner, a.company):
            b = load_brand(a.brand)
            brand_note = f"brand memory belongs to '{owner}', the audited company: used"
        else:
            brand_note = f"brand memory belongs to '{owner}', NOT '{a.company}': not used for judging this site"

    extra = list(b["terms"]) if b else []
    if a.company:
        extra.append(a.company)
    groups = naming(pieces, extra)
    name_keys = {g["term"] for g in groups} | {re.sub(r"[^a-z]", "", t.lower()) for t in extra}
    # name keys from any capitalised two-word term, so "seamless sync" is treated as a name, not a stock word
    for pc in pieces:
        for m in re.finditer(r"\b([A-Z][a-z]+)[ -]?([A-Z][a-z]+)\b", pc["all"]):
            name_keys.add((m.group(1) + m.group(2)).lower())
    metrics = {pc["name"]: voice_metrics(pc, name_keys, a.company) for pc in pieces}
    conv_by_piece = {n: m["spelling"]["convention"] for n, m in metrics.items()}
    all_us = sorted({w for m in metrics.values() for w in m["spelling"]["us"]})
    all_cw = sorted({w for m in metrics.values() for w in m["spelling"]["commonwealth"]})
    all_ise = sorted({w for m in metrics.values() for w in m["spelling"]["ise"]})
    all_ize = sorted({w for m in metrics.values() for w in m["spelling"]["ize"]})
    mixed = bool(all_us and all_cw) or bool(all_ise and all_ize)
    result = {
        "pieces": [pc["name"] for pc in pieces], "missing_files": missing, "brand_memory": brand_note,
        "voice": metrics, "spelling": {"by_piece": conv_by_piece, "mixed": mixed, "us": all_us, "commonwealth": all_cw,
                                       "ise": all_ise, "ize": all_ize},
        "outliers": outliers(metrics), "naming": groups,
        "trust": {pc["name"]: trust(pc) for pc in pieces},
        "assets": {pc["name"]: assets(pc, a.company) for pc in pieces if pc["kind"] == "html"},
        "brand": brand_checks(b, pieces, metrics) if b else [],
        "not_observable": ["logo design and placement", "colour palette", "typography", "photography and imagery style"]
                          + ([] if any(pc["kind"] == "html" for pc in pieces) else ["alt text and page titles (no HTML supplied)"]),
    }
    if a.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0

    print(f"Pieces: {len(pieces)} ({', '.join(result['pieces'])})")
    if missing:
        print(f"Missing files: {', '.join(missing)}")
    print(f"BRAND MEMORY: {brand_note}\n")
    print("VOICE")
    print("| Piece | Words | Sentences | Avg len | Spread | Contr/100 | we | you | I | 3rd-person self | will/100 | Spelling | Stock words | ! | # |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for n, m in metrics.items():
        print(f"| {n} | {m['words']} | {m['sentences']} | {m['avg_sentence']} | {m['sentence_spread']} | {m['contractions_per_100']} | "
              f"{m['we']} | {m['you']} | {m['i']} | {m['third_person_self']} | {m['will_per_100']} | {m['spelling']['convention']} | "
              f"{', '.join(m['stock']) or '-'} | {m['exclamations']} | {m['hashtags']} |")
    print("\nSPELLING")
    print(f"  {'MIXED' if mixed else 'consistent'}: US forms {all_us or '-'}; Commonwealth forms {all_cw or '-'}; -ise {all_ise or '-'}; -ize {all_ize or '-'}")
    for n, c in conv_by_piece.items():
        print(f"  {n}: {c}")
    print("\nOUTLIERS (register)")
    for o in result["outliers"] or ["none found"]:
        print(f"  {o}")
    print("\nNAMING (one term, several written forms)")
    for g in groups:
        print(f"  {g['term']}: " + "; ".join(f"'{f}' in {', '.join(w)}" for f, w in g["forms"].items()))
    if not groups:
        print("  none found")
    print("\nTRUST")
    for n, t in result["trust"].items():
        bits = []
        for k in ("email", "phone", "address", "policy_links", "credentials", "team"):
            bits.append(f"{k}: {', '.join(t[k]) if t[k] else '-'}")
        print(f"  {n}: " + " · ".join(bits))
        for q in t["testimonials"]:
            print(f"    testimonial ({'named person' if q['named_person'] else 'NOT named'}): {q['quote'][:100]}")
        for r in t["ratings"]:
            print(f"    rating ({'source named' if r['source_named'] else 'NO source named'}): {r['text']}")
        for v in t["vague_proof"]:
            print(f"    vague proof: {v}")
    if result["assets"]:
        print("\nASSETS")
        for n, s in result["assets"].items():
            print(f"  {n}: title '{s['title']}' ({s['title_format'] or 'no title'})")
            for im in s["images"]:
                if im["issue"]:
                    print(f"    image {im['src']}: {im['issue']} (alt={im['alt']!r})")
            for p in s["placeholders"]:
                print(f"    placeholder: {p}")
    if b is not None:
        print("\nBRAND (against the company's own brand memory)")
        for c in result["brand"] or [{"kind": "none", "where": "", "detail": "no breaches found"}]:
            print(f"  {c['kind'].upper()} · {c['where']} · {c['detail']}")
    print("\nNOT OBSERVABLE FROM TEXT: " + "; ".join(result["not_observable"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
