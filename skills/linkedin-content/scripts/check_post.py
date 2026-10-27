#!/usr/bin/env python3
"""Mechanical checks for LinkedIn posts against brand memory and the user's material. Standard library only.

Usage:
    python3 scripts/check_post.py linkedin/post.md --brand brand/ --sources notes/talk.md --kind personal
    python3 scripts/check_post.py linkedin/s-1.md linkedin/s-2.md --brand brand/ --sources notes/call.md
    python3 scripts/check_post.py linkedin/deck.md --format carousel --brand brand/
    python3 scripts/check_post.py linkedin/post.md --sources-text "facts the user typed in chat"
    python3 scripts/check_post.py --reply reply.md          # measure a short reply (needs-input, guided): under 200 words

Each file holds one post (or one carousel: slides, then a "Caption" section). --sources may repeat; it is the
user's material (notes, transcript, draft). Brand memory facts count as sources too.

Checks:
    FAIL  over the brand's LinkedIn word limit (voice.md, "## By channel" > "### LinkedIn"), or over 3,000 characters
    FAIL  more hashtags or exclamation marks than the brand allows (default: at most 3 hashtags)
    FAIL  engagement bait ("Agree?", "Thoughts?", "Comment YES", "Tag someone", "Follow for more", "Repost if")
    FAIL  broetry: three or more one-sentence lines or paragraphs in a row (list items don't count)
    FAIL  a population opener on the first line ("Most leaders...", "Every founder...", "Too many teams...")
    FAIL  a never-use word from voice.md, or a phrase a rules.md "Everywhere" line forbids
    FAIL  a number that is in neither the sources nor brand memory (possible invention)
    FAIL  a person or company that proof.md marks "named: no" or "named: unconfirmed"
    FAIL  a leftover placeholder ([name], TBD, TODO, XX)
    WARN  performed candour or manufactured friction, stock phrases, "not X, but Y", em-dash density,
          spelling against the brand's convention, first line over 200 characters, links in the body,
          names and quotes not found in the sources or brand memory, person (I vs we) against --kind,
          slides over 30 words (carousel)

Exit code: 0 if no FAIL, 1 if any FAIL, 2 on bad input.
"""

import argparse
import os
import re
import sys

BAIT = [
    r"\bagree\s*\?", r"(^|\n)\s*thoughts\s*\?", r"\b(?i:comment)\s+[\"'“]?[A-Z]{2,}[\"'”]?", r"\bcomment\s+(yes|below|['\"“]\w+)",
    r"\b(?i:type)\s+[\"'“]?[A-Z]{2,}", r"\btag\s+(someone|a friend|a colleague|3|three)\b", r"\bfollow\s+(me\s+)?for\s+more\b",
    r"\brepost\s+if\b", r"\blike\s+if\b", r"\bsmash\s+(that|the)\b", r"\bwho\s+else\b[^.?!\n]{0,40}\?", r"\bdrop\s+an?\s+\S+\s+(below|in the comments)",
    r"♻️", r"\bhit\s+(the\s+)?(like|follow|bell)\b", r"\bshare\s+(this\s+)?if\b", r"\blet me know in the comments\b",
    r"\bcomment\s+and\s+i'?ll\b", r"\b(?i:dm\s+me)\s+[\"'“]?[A-Z]{2,}",
]
CANDOUR = [
    "i'll be honest", "let me be honest", "unpopular opinion", "hot take", "let that sink in", "read that again",
    "here's the thing", "nobody talks about", "no one talks about", "i almost didn't post this", "this changed everything",
    "plot twist", "stop scrolling", "i was today years old", "i'm humbled", "humbled to announce", "thrilled to announce",
    "excited to announce", "here's what happened next", "and then it hit me", "the result?", "the truth is",
    "i'm not going to lie", "not gonna lie", "this is your sign", "controversial, but", "i need to get this off my chest",
    "i was wrong about", "what nobody tells you", "lessons i learned", "here are 5", "here are 3", "here are 7",
]
STOCK = [
    "in today's fast-paced", "fast-paced world", "landscape", "delve", "game-changer", "game changer", "cutting-edge",
    "unlock", "elevate", "empower", "leverage", "seamlessly", "streamline", "robust", "holistic", "navigate",
    "what matters most", "we've got you covered", "partner in your success", "take it to the next level",
    "revolutionize", "transformative", "synergy", "actionable insights", "data-driven", "best-in-class", "world-class",
    "journey", "deep dive", "move the needle", "thought leader",
]
POP_OPENER = re.compile(
    r"^\W*(most|many|too many|so many|every|all|nearly all|almost every)\s+"
    r"(leaders?|companies|teams|people|founders?|owners?|ceos?|marketers?|businesses|organizations|managers?|"
    r"restaurants?|clinics?|dental|merchants?|brands?|startups?|professionals?|executives?|small|of you|of us)\b", re.I)
NOT_X_BUT_Y = re.compile(r"\bnot (just|only|merely)\b[^.!?\n]{0,80}[,;—–-]\s*(but|it'?s|we'?re|they'?re|a)\b", re.I)
PLACEHOLDER = re.compile(r"\[(?:[^\]]{0,40})\]|\bTBD\b|\bTODO\b|\bXX+\b|<[a-z][^>]{0,30}>")
OUR = [("color", "colour"), ("labor", "labour"), ("favor", "favour"), ("behavior", "behaviour"), ("honor", "honour"),
       ("neighbor", "neighbour"), ("flavor", "flavour"), ("humor", "humour")]
RE_ = [("center", "centre"), ("theater", "theatre"), ("liter", "litre")]
IZE = [("organize", "organise"), ("analyze", "analyse"), ("optimize", "optimise"), ("prioritize", "prioritise"),
       ("recognize", "recognise"), ("realize", "realise"), ("customize", "customise")]
WORD_NUMBERS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}
CALENDAR = {"January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
            "November", "December", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"}
DEFAULT_HASHTAGS = 3
HARD_CHARS = 3000


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def strip_tags(s):
    return re.sub(r"\[source:[^\]]*\]", "", s).strip()


def section(text, heading, level=2):
    hashes = "#" * level
    m = re.search(rf"^{hashes}\s+{re.escape(heading)}[^\n]*\n(.*?)(?=^#{{1,{level}}}\s|\Z)", text, re.I | re.M | re.S)
    return m.group(1) if m else ""


def bullets(text):
    return [strip_tags(l.strip()[1:]) for l in text.splitlines() if l.strip().startswith(("-", "*"))]


def load_brand(brand_dir):
    if not brand_dir or not os.path.isdir(brand_dir):
        return None
    b = {"never": [], "forbidden": [], "spelling": None, "linkedin": "", "corpus": "", "unnamed": []}
    files = {}
    for name in sorted(os.listdir(brand_dir)):
        if name.endswith(".md"):
            files[name] = read(os.path.join(brand_dir, name))
            b["corpus"] += files[name] + "\n"
    voice, rules, proof = files.get("voice.md", ""), files.get("rules.md", ""), files.get("proof.md", "")
    for line in bullets(section(voice, "Words we never use")):
        if not line.upper().startswith("TBD"):
            b["never"] += [w.strip().strip("'\"“”") for w in line.split(",") if w.strip()]
    for line in bullets(section(rules, "Everywhere")):
        if re.search(r"\b(never|don'?t|do not|avoid|no)\b", line, re.I):
            b["forbidden"] += re.findall(r"[\"“]([^\"”]{2,60})[\"”]", line)
    m = re.search(r"\b(US|American|UK|British|Canadian)\s+spelling\b", voice, re.I)
    if m:
        b["spelling"] = {"us": "us", "american": "us", "uk": "uk", "british": "uk", "canadian": "ca"}[m.group(1).lower()]
    by_channel = section(voice, "By channel")
    for m in re.finditer(r"^###\s+(.+?)\s*\n(.*?)(?=^###\s|\Z)", by_channel, re.M | re.S):
        if m.group(1).strip().lower().startswith(("linkedin", "social")):
            b["linkedin"] = " ".join(bullets(m.group(2)))
    for line in proof.splitlines():
        if re.search(r"named:\s*(no|unconfirmed)\b", line, re.I):
            head = strip_tags(line.lstrip("-* ")).split(":")[0]
            for part in re.split(r"[,()]", head):
                part = part.strip()
                if re.match(r"^[A-Z][\w'’-]+(?: [A-Z][\w'’-]+)+$", part):
                    b["unnamed"].append(part)
    return b


def limits(rule):
    lim, t = {}, rule.lower()
    m = re.search(r"under (\d+) words", t)
    if m:
        lim["words"] = int(m.group(1))
    if re.search(r"no exclamation marks?", t):
        lim["exclaim"] = 0
    else:
        m = re.search(r"(one|two|three|\d+) exclamation marks?", t)
        if m:
            lim["exclaim"] = WORD_NUMBERS.get(m.group(1)) or int(m.group(1))
    if re.search(r"no hashtags", t):
        lim["hashtags"] = 0
    else:
        m = re.search(r"(one|two|three|\d+) hashtags?", t)
        if m:
            lim["hashtags"] = WORD_NUMBERS.get(m.group(1)) or int(m.group(1))
    return lim


def norm(s):
    return re.sub(r"[\s\-–—]+", " ", s.lower()).strip()


def has_phrase(text, phrase):
    pattern = r"(?<!\w)" + re.escape(norm(phrase)).replace(r"\ ", r"[\s\-–—]+") + r"\w*"
    return re.search(pattern, text.lower())


def words(s):
    return re.findall(r"[A-Za-z0-9$%'’]+", s)


def numbers(s):
    out = set()
    for tok in re.findall(r"\d[\d,.]*", s):
        tok = tok.rstrip(".,").replace(",", "")
        if tok:
            out.add(tok)
    low = s.lower()
    for w, n in WORD_NUMBERS.items():
        if re.search(rf"\b{w}\b", low):
            out.add(str(n))
    return out


def split_carousel(text):
    m = re.search(r"(?im)^#{1,4}\s*caption\b.*$|^\*\*caption\b.*$", text)
    if not m:
        return text, ""
    return text[:m.start()], text[m.end():]


def body_lines(text):
    """Post lines minus markdown headings and hashtag-only lines."""
    return [l for l in text.splitlines() if not re.match(r"^\s*#{1,6}\s", l) and not re.match(r"^\s*(#\w+\s*)+$", l)]


def is_list(line):
    return bool(re.match(r"^\s*([-*•→✓]|\d+[.)])\s+", line))


def one_sentence(line):
    s = line.strip()
    parts = [p for p in re.split(r"(?<=[.!?])\s+", s) if p]
    return s and len(parts) == 1 and len(words(s)) <= 15


def check(path, brand, sources, kind, fmt):
    raw = read(path)
    text = raw
    slides = ""
    if fmt == "carousel":
        slides, text = split_carousel(raw)
    findings = []
    add = lambda level, msg: findings.append((level, msg))
    lines = body_lines(text)
    post = "\n".join(lines).strip()
    n_words = len(words(re.sub(r"(?<![\w&])#[A-Za-z]\w*", "", post)))

    lim = limits(brand["linkedin"]) if brand else {}
    if "words" in lim and n_words >= lim["words"]:
        add("FAIL", f"length: {n_words} words; the brand's LinkedIn limit is under {lim['words']}")
    if len(post) > HARD_CHARS:
        add("FAIL", f"length: {len(post)} characters; LinkedIn's limit is {HARD_CHARS}")
    n_tags = len(re.findall(r"(?<![\w&/])#[A-Za-z]\w*", raw))
    max_tags = lim.get("hashtags", DEFAULT_HASHTAGS)
    if n_tags > max_tags:
        add("FAIL", f"hashtags: {n_tags}; the limit is {max_tags}" + ("" if "hashtags" in lim else " (default)"))
    n_ex = raw.count("!")
    if "exclaim" in lim and n_ex > lim["exclaim"]:
        add("FAIL", f"exclamation marks: {n_ex}; the brand's LinkedIn limit is {lim['exclaim']}")

    for pat in BAIT:
        m = re.search(pat, post, re.I if not re.search(r"\[A-Z\]", pat) else 0)
        if m:
            add("FAIL", f"engagement bait: \"{m.group(0).strip()}\"")
            break

    run, worst = 0, 0
    paras = [l for l in lines if l.strip()]
    for l in paras:
        if is_list(l):
            run = 0
            continue
        run = run + 1 if one_sentence(l) else 0
        worst = max(worst, run)
    if worst >= 3:
        add("FAIL", f"broetry: {worst} one-sentence lines in a row; join them into paragraphs")

    first = next((l for l in paras), "")
    if POP_OPENER.search(first):
        add("FAIL", f"population opener: \"{first[:60]}\"")
    if len(first) > 200:
        add("WARN", f"first line is {len(first)} characters; the hook is cut off after about 200")

    if brand:
        for w in brand["never"]:
            if has_phrase(raw, w):
                add("FAIL", f"never-use word: '{w}'")
        for p in brand["forbidden"]:
            if has_phrase(raw, p):
                add("FAIL", f"forbidden by rules.md: '{p}'")
        for name in brand["unnamed"]:
            if has_phrase(raw, name) or has_phrase(raw, name.split()[0] + " " + name.split()[-1]):
                add("FAIL", f"naming permission: proof.md doesn't confirm permission to name '{name}'")
            elif len(name.split()) == 2 and re.search(rf"\b{re.escape(name.split()[0])}\b", raw) and not re.search(r"\b(bar|grill|cafe|kitchen|house)\b", name, re.I):
                add("WARN", f"naming permission: '{name.split()[0]}' may identify '{name}', whose permission is unconfirmed")

    m = PLACEHOLDER.search(raw.replace("[source:", ""))
    if m:
        add("FAIL", f"placeholder left in: \"{m.group(0)}\"")

    known = sources + "\n" + (brand["corpus"] if brand else "")
    if known.strip():
        unlabelled = re.sub(r"(?im)^\s*(?:#{1,4}\s*)?(?:\*\*)?slide\s*\d+.*$", "", raw)
        new = sorted(n for n in numbers(unlabelled) if n not in numbers(known))
        if new:
            add("FAIL", f"numbers not in the sources or brand memory: {', '.join(new)}")
        names = set(re.findall(r"(?<=[a-z,;:] )([A-Z][a-z]+(?: [A-Z][a-z]+)*)", raw))
        new_names = sorted(n for n in names if n.lower() not in known.lower() and n.split()[0] not in CALENDAR)
        if new_names:
            add("WARN", f"names not in the sources or brand memory: {', '.join(new_names[:8])}")
        for q in re.findall(r"[\"“]([^\"”]{20,300})[\"”]", raw):
            if norm(q) not in norm(known):
                add("WARN", f"quote not found word for word in the sources or brand memory: \"{q[:60]}\"")
    else:
        add("WARN", "no sources given: numbers and names were not traced")

    low = raw.lower()
    hits = [c for c in CANDOUR if c in low]
    if hits:
        add("WARN", "performed candour or manufactured friction: " + ", ".join(hits))
    stock = [s for s in STOCK if has_phrase(raw, s) and not (brand and norm(s) in norm(brand["corpus"]))]
    if stock:
        add("WARN", "stock phrasing: " + ", ".join(stock))
    if NOT_X_BUT_Y.search(raw):
        add("WARN", f"'not X, but Y': \"{NOT_X_BUT_Y.search(raw).group(0)[:60]}\"")
    dashes = raw.count("—") + len(re.findall(r"\s–\s|\s--\s", raw))
    if dashes > max(1, n_words // 150):
        add("WARN", f"{dashes} em dashes in {n_words} words")
    links = re.findall(r"https?://\S+|\b[\w-]+\.(?:com|ca|io|co|org|example)(?:/\S*)?", post)
    if links:
        add("WARN", f"link in the post body ({links[0]}): fine if the user chose it, otherwise move it to the first comment")
    emoji = len(re.findall(r"[\U0001F300-\U0001FAFF☀-➿]", raw))
    if emoji > 3:
        add("WARN", f"{emoji} emoji")

    conv = brand["spelling"] if brand else None
    if conv:
        pairs = [(us, uk, conv == "us") for us, uk in OUR + RE_] + [(us, uk, conv in ("us", "ca")) for us, uk in IZE]
        wrong = [(uk if want_us else us) for us, uk, want_us in pairs if re.search(rf"\b{(uk if want_us else us)}\w*", low)]
        if wrong:
            add("WARN", f"spelling against the brand's {conv.upper()} convention: {', '.join(wrong)}")

    first_person = re.search(r"\b(I|I'm|I've|I'd|my|me)\b", post)
    if kind == "personal" and not first_person:
        add("WARN", "person: a personal post with no 'I' or 'my'")
    if kind == "company" and first_person:
        add("WARN", f"person: a company-page post that says '{first_person.group(0)}'")

    if fmt == "carousel":
        n_slides = 0
        for block in re.split(r"(?m)^\s*(?:#{1,4}\s*)?(?:\*\*)?slide\s*\d+", slides, flags=re.I)[1:]:
            n_slides += 1
            w = len(words(block))
            if w > 30:
                add("WARN", f"slide {n_slides}: {w} words; keep each slide under 30")
        if not n_slides:
            add("WARN", "carousel: no 'Slide 1', 'Slide 2'... headings found")

    fails = sum(1 for f in findings if f[0] == "FAIL")
    print(f"== {path}")
    for level, msg in findings:
        print(f"{level} {msg}")
    print(f"{'FAIL' if fails else 'PASS'}: {fails} fail, {len(findings) - fails} warn; {n_words} words")
    return fails


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--reply", help="measure a reply file's words against --reply-limit")
    ap.add_argument("--reply-limit", type=int, default=200)
    ap.add_argument("--brand")
    ap.add_argument("--sources", action="append", default=[])
    ap.add_argument("--sources-text", default="")
    ap.add_argument("--kind", choices=["personal", "company"], default=None)
    ap.add_argument("--format", choices=["post", "carousel"], default="post")
    a = ap.parse_args()
    if a.reply:
        try:
            n = len(words(read(a.reply)))
        except OSError as e:
            print(f"error: {e}", file=sys.stderr)
            return 2
        ok = n < a.reply_limit
        print(f"{'PASS' if ok else 'FAIL'}: reply is {n} words; the limit is under {a.reply_limit}")
        if not a.files:
            return 0 if ok else 1
    if not a.files:
        ap.error("give at least one post file, or --reply")
    try:
        sources = "\n".join(read(s) for s in a.sources) + "\n" + a.sources_text
        brand = load_brand(a.brand)
        if a.brand and brand is None:
            print(f"note: no brand memory at {a.brand}; brand rules were not checked")
        total = sum(check(f, brand, sources, a.kind, a.format) for f in a.files)
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
