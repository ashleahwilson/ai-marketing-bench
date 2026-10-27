#!/usr/bin/env python3
"""Mechanical checks for a draft against brand memory. Standard library only.

Usage:
    python3 scripts/check_voice.py revised.md --brand brand/ --channel linkedin --original draft.md
    python3 scripts/check_voice.py draft.md                       # no brand memory: general checks only
    cat revised.md | python3 scripts/check_voice.py - --brand brand/ --channel email

Channels: email, linkedin, social, website, ad, proposal. The matching "### <Channel>" section under
"## By channel" in brand/voice.md supplies word limits, exclamation and hashtag limits.

Checks:
    FAIL  a never-use word from voice.md, or a phrase a rules.md line forbids ("Never ... 'X'")
    FAIL  a number in the text that is in neither the original draft nor brand/ (possible invention)
    FAIL  over the channel's word, exclamation-mark or hashtag limit
    WARN  stock phrases, spelling against the brand's stated convention, quotes not recorded in proof.md,
          three sentences of similar length in a row, em-dash density, markdown in email,
          capitalised names not found in the draft or brand/

Exit code: 0 if no FAIL, 1 if any FAIL, 2 on bad input.
"""

import argparse
import os
import re
import sys

STOCK = [
    "in today's fast-paced", "fast-paced world", "landscape", "delve", "tapestry", "testament to", "pivotal",
    "game-changer", "game-changing", "game changer", "cutting-edge", "unlock", "unlocking", "elevate", "empower",
    "empowering", "leverage", "seamless", "seamlessly", "streamline", "robust", "holistic", "navigate",
    "what matters most", "we've got you covered", "partner in your success", "take it to the next level",
    "i hope this email finds you well", "i hope this finds you well", "my name is", "reaching out",
    "thrilled to announce", "excited to announce", "valued customer", "commitment to excellence",
    "full potential", "shaping the future", "revolutionize", "revolutionise", "transformative", "synergy",
    "actionable insights", "data-driven", "best-in-class", "world-class", "look no further",
]
NOT_X_BUT_Y = re.compile(r"\bnot (just|only|merely)\b[^.!?\n]{0,80}[,;—–-]\s*(but|it'?s|we'?re|they'?re|a)\b", re.I)
SIGNIFICANCE = re.compile(r",\s*(highlighting|underscoring|empowering|enabling|helping|ensuring|allowing|making it|paving the way|reflecting|showcasing)\b", re.I)

# (US form, UK/Canadian form). Canadian keeps -our and -re but uses -ize.
OUR = [("color", "colour"), ("labor", "labour"), ("favor", "favour"), ("behavior", "behaviour"), ("honor", "honour"),
       ("neighbor", "neighbour"), ("flavor", "flavour"), ("humor", "humour"), ("rumor", "rumour")]
RE_ = [("center", "centre"), ("theater", "theatre"), ("meter", "metre"), ("liter", "litre")]
IZE = [("organize", "organise"), ("analyze", "analyse"), ("optimize", "optimise"), ("prioritize", "prioritise"),
       ("recognize", "recognise"), ("realize", "realise"), ("customize", "customise"), ("finalize", "finalise")]
CHANNEL_ALIASES = {"social": "linkedin", "dm": "email", "web": "website", "page": "website", "landing": "website"}
WORD_NUMBERS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10}


def read(path):
    if path == "-":
        return sys.stdin.read()
    with open(path, encoding="utf-8") as f:
        return f.read()


def strip_tags(s):
    return re.sub(r"\[source:[^\]]*\]|\|.*$", "", s).strip()


def section(text, heading, level=2):
    """Body of the first '#'*level heading whose title starts with `heading` (case-insensitive)."""
    hashes = "#" * level
    m = re.search(rf"^{hashes}\s+{re.escape(heading)}[^\n]*\n(.*?)(?=^#{{1,{level}}}\s|\Z)", text, re.I | re.M | re.S)
    return m.group(1) if m else ""


def bullets(text):
    return [strip_tags(l[1:]) for l in text.splitlines() if l.strip().startswith(("-", "*"))]


def load_brand(brand_dir):
    b = {"never": [], "forbidden": [], "spelling": None, "channels": {}, "corpus": "", "proof": ""}
    if not brand_dir or not os.path.isdir(brand_dir):
        return None
    for name in sorted(os.listdir(brand_dir)):
        if name.endswith(".md"):
            b["corpus"] += read(os.path.join(brand_dir, name)) + "\n"
    voice = read(os.path.join(brand_dir, "voice.md")) if os.path.exists(os.path.join(brand_dir, "voice.md")) else ""
    rules = read(os.path.join(brand_dir, "rules.md")) if os.path.exists(os.path.join(brand_dir, "rules.md")) else ""
    if os.path.exists(os.path.join(brand_dir, "proof.md")):
        b["proof"] = read(os.path.join(brand_dir, "proof.md"))
    for line in bullets(section(voice, "Words we never use")):
        if not line.upper().startswith("TBD"):
            b["never"] += [w.strip().strip("'\"“”") for w in line.split(",") if w.strip()]
    for line in bullets(section(rules, "Everywhere")):
        if re.search(r"\b(never|don'?t|do not|avoid|no)\b", line, re.I):
            b["forbidden"] += re.findall(r"[\"“]([^\"”]{2,60})[\"”]", line) + re.findall(r"(?<!\w)'([^']{2,60})'(?!\w)", line)
    m = re.search(r"\b(US|American|UK|British|Canadian)\s+spelling\b", voice, re.I)
    if m:
        b["spelling"] = {"us": "us", "american": "us", "uk": "uk", "british": "uk", "canadian": "ca"}[m.group(1).lower()]
    by_channel = section(voice, "By channel")
    for m in re.finditer(r"^###\s+(.+?)\s*\n(.*?)(?=^###\s|\Z)", by_channel, re.M | re.S):
        b["channels"][m.group(1).strip().lower()] = " ".join(bullets(m.group(2)))
    return b


def channel_limits(rule_text):
    lim = {}
    t = rule_text.lower()
    m = re.search(r"under (\d+) words", t)
    if m:
        lim["words"] = int(m.group(1))
    if re.search(r"no exclamation marks?", t):
        lim["exclaim"] = 0
    else:
        m = re.search(r"(?:at most |max(?:imum)? )?(one|two|three|\d+) exclamation marks?", t)
        if m:
            lim["exclaim"] = WORD_NUMBERS.get(m.group(1), None) or int(m.group(1))
    if re.search(r"no hashtags", t):
        lim["hashtags"] = 0
    else:
        m = re.search(r"(?:at most |max(?:imum)? )?(?:[a-z ,]*?\band )?(one|two|three|\d+) hashtags?", t)
        if m:
            lim["hashtags"] = WORD_NUMBERS.get(m.group(1), None) or int(m.group(1))
    return lim


def norm(s):
    return re.sub(r"[\s\-–—]+", " ", s.lower()).strip()


def contains_phrase(text, phrase):
    p = norm(phrase)
    pattern = r"\b" + re.escape(p).replace(r"\ ", r"[\s\-–—]+") + r"\w*"
    return re.search(pattern, text.lower())


def message_body(text):
    """Text minus subject line, greeting, hashtag-only lines and short sign-off lines."""
    lines = [l for l in text.splitlines() if not re.match(r"^\s*subject\s*:", l, re.I)]
    lines = [l for l in lines if not re.match(r"^\s*(#\w+\s*)+$", l)]
    while lines and not lines[0].strip():
        lines.pop(0)
    if lines and re.match(r"^\s*(hi|hey|hello|dear)\b[^.!?]{0,40}[,!]?\s*$", lines[0], re.I):
        lines.pop(0)
    while lines and (not lines[-1].strip() or len(re.findall(r"\w+", lines[-1])) <= 3):
        lines.pop()
    return "\n".join(lines)


def words(s):
    return re.findall(r"[A-Za-z0-9$%'’]+", s)


def numbers(s):
    out = set()
    for tok in re.findall(r"\d[\d,.]*", s):
        tok = tok.rstrip(".,").replace(",", "")
        if tok:
            out.add(tok)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--brand")
    ap.add_argument("--channel", default="")
    ap.add_argument("--original")
    a = ap.parse_args()
    try:
        text = read(a.file)
        original = read(a.original) if a.original else ""
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    # A -gated.md file carries the verdict and checks under a trailing '---'; check only the text above it.
    text = re.split(r"(?m)^---\s*\n(?=\s*\*\*Verdict)", text)[0]
    brand = load_brand(a.brand)
    findings = []
    add = lambda level, code, msg: findings.append((level, code, msg))
    low = text.lower()

    # Brand words and rules
    if brand:
        for w in brand["never"]:
            if contains_phrase(text, w):
                add("FAIL", "never-use", f"'{w}' is on the brand's never-use list")
        for p in brand["forbidden"]:
            if contains_phrase(text, p):
                add("FAIL", "rule", f"'{p}' is forbidden by a rule in rules.md")
    else:
        add("WARN", "no-brand", "no brand memory: brand words, channel rules and claims were not checked")

    # Channel limits
    ch = CHANNEL_ALIASES.get(a.channel.lower(), a.channel.lower())
    lim = {}
    if brand and ch:
        rule = next((v for k, v in brand["channels"].items() if k.startswith(ch) or ch.startswith(k)), "")
        lim = channel_limits(rule)
    body = message_body(text)
    n_words = len(words(body))
    if "words" in lim and n_words >= lim["words"]:
        add("FAIL", "length", f"{n_words} words; the brand's {ch} limit is under {lim['words']}")
    n_ex = text.count("!")
    if "exclaim" in lim and n_ex > lim["exclaim"]:
        add("FAIL", "exclamation", f"{n_ex} exclamation mark(s); the brand's {ch} limit is {lim['exclaim']}")
    elif not lim.get("exclaim") and ch == "email" and n_ex:
        add("WARN", "exclamation", f"{n_ex} exclamation mark(s) in an email")
    n_tags = len(re.findall(r"(?<![\w&])#[A-Za-z]\w*", text))
    if "hashtags" in lim and n_tags > lim["hashtags"]:
        add("FAIL", "hashtags", f"{n_tags} hashtag(s); the brand's {ch} limit is {lim['hashtags']}")

    # General tells
    hits = [s for s in STOCK if contains_phrase(text, s) and not (brand and any(norm(s) in norm(w) for w in re.findall(r"[A-Z][\w-]+(?: [A-Z][\w-]+)+", text)))]
    if hits:
        add("WARN", "stock", "stock phrasing: " + ", ".join(sorted(set(hits))))
    if NOT_X_BUT_Y.search(text):
        add("WARN", "not-x-but-y", f"'not just X, but Y' construction: \"{NOT_X_BUT_Y.search(text).group(0)[:60]}\"")
    if SIGNIFICANCE.search(text):
        add("WARN", "significance", f"'-ing' significance clause: \"{SIGNIFICANCE.search(text).group(0)}\"")
    sents = [s for s in re.split(r"(?<=[.!?])\s+|\n+", body) if len(words(s)) >= 8]
    for i in range(len(sents) - 2):
        lens = [len(words(s)) for s in sents[i:i + 3]]
        if max(lens) - min(lens) <= 2:
            add("WARN", "rhythm", f"three sentences in a row of {lens} words, starting \"{sents[i][:40]}\"")
            break
    dashes = text.count("—") + len(re.findall(r"\s–\s|\s--\s", text))
    if dashes > max(1, n_words // 300):
        add("WARN", "em-dash", f"{dashes} em dashes in {n_words} words")
    if ch == "email" and re.search(r"^\s*(#{1,6}\s|[-*]\s)|\*\*", body, re.M):
        add("WARN", "markdown", "markdown (headers, bullets or bold) in an email")

    # Spelling against the brand's convention
    conv = brand["spelling"] if brand else None
    if conv:
        wrong = []
        pairs = [(us, uk, conv == "us") for us, uk in OUR + RE_] + [(us, uk, conv in ("us", "ca")) for us, uk in IZE]
        for us, uk, want_us in pairs:
            bad = uk if want_us else us
            if re.search(rf"\b{bad}\w*", low):
                wrong.append(bad)
        if wrong:
            add("WARN", "spelling", f"spelling doesn't match the brand's {conv.upper()} convention: {', '.join(wrong)}")

    # Facts: numbers and names must come from the original or brand memory
    known = original + "\n" + (brand["corpus"] if brand else "")
    if a.original or brand:
        new_nums = sorted(n for n in numbers(text) if n not in numbers(known))
        if new_nums:
            add("FAIL", "new-number", f"numbers not in the draft or brand memory: {', '.join(new_nums)}")
        names = set(re.findall(r"(?<=[a-z,;:] )([A-Z][a-z]+(?: [A-Z][a-z]+)*)", text))
        new_names = sorted(n for n in names if n.lower() not in known.lower())
        if new_names:
            add("WARN", "new-name", f"names not in the draft or brand memory (check they're real): {', '.join(new_names[:8])}")
    if brand:
        for q in re.findall(r"[\"“]([^\"”]{25,300})[\"”]", text):
            if norm(q) not in norm(brand["proof"]) and norm(q) not in norm(brand["corpus"]):
                add("WARN", "quote", f"quote not recorded word for word in brand memory: \"{q[:60]}\"")

    fails = sum(1 for f in findings if f[0] == "FAIL")
    for level, code, msg in findings:
        print(f"{level} {code}: {msg}")
    print(f"{'FAIL' if fails else 'PASS'}: {fails} fail, {len(findings) - fails} warn; {n_words} words in the message")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
