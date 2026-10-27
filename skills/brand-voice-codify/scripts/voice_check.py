#!/usr/bin/env python3
"""Check a brand/voice.md, and measure writing samples. Standard library only. Reads files; changes nothing.

Usage:
    python3 scripts/voice_check.py check brand/voice.md
    python3 scripts/voice_check.py check brand/voice.md --evidence samples/ edits.md --previous old-voice.md
    python3 scripts/voice_check.py stats samples/*.md

check: the voice.md format other skills read (brand-voice-gate parses it).
    FAIL  a required section missing; template leftovers (YYYY-MM-DD, <placeholder>); an empty section with no
          "TBD:" line; a rule bullet with no [source: <where>, <YYYY-MM-DD> · confirmed|provisional] tag;
          text under "## By channel" outside a "### <Channel>" subsection, or a subsection with no bullets;
          a never-use entry with an explanation in it (parentheses, quotes, more than four words);
          a word on both the use and never-use lists, or a never-use word inside a word we use
          ("seamless" would flag the product "Seamless Sync"); more than one spelling convention named;
          a TBD line in a channel that states a limit (another skill would enforce an unresolved rule);
          a new Examples quote not found word for word in the evidence (with --evidence);
          a confirmed rule from the previous version that is gone (with --previous)
    WARN  no spelling convention and no TBD for it; a channel limit worded so it can't be read
          ("max 120 words", "avoid exclamation marks"); an "assumed" status; duplicate never-use words

stats: per file and in total: words, sentences, average and longest sentence, contractions per 100 words,
    exclamation and question marks, em dashes, hashtags, I/we/you counts, and spelling variants
    (US, UK, Canadian markers). Evidence for rules; it doesn't decide them.

Exit code: 0 if no FAIL, 1 if any FAIL, 2 on bad input.
"""

import argparse
import os
import re
import sys

REQUIRED = ["Principles", "Do", "Don't", "Words we use", "Words we never use", "By channel", "Examples"]
RULE_SECTIONS = ["Principles", "Do", "Don't", "Words we use", "Words we never use", "Examples"]
TAG = re.compile(r"\[source:\s*([^\]]+)\]", re.I)
STATUS = re.compile(r"\b(confirmed|provisional|assumed)\b", re.I)
DATE = re.compile(r"\b20\d\d-\d\d-\d\d\b")
LEFTOVER = re.compile(r"YYYY-MM-DD|<[^>\n]{2,60}>|\[(?:insert|todo|placeholder)[^\]]*\]", re.I)
SPELLING = re.compile(r"\b(US|American|UK|British|Canadian)\s+spelling\b", re.I)
LIMIT = re.compile(r"under \d+ words|no exclamation marks?|(?:one|two|three|\d+) exclamation marks?|no hashtags|"
                   r"(?:one|two|three|\d+) hashtags?", re.I)

OUR = [("color", "colour"), ("labor", "labour"), ("favor", "favour"), ("behavior", "behaviour"), ("honor", "honour"),
       ("neighbor", "neighbour"), ("flavor", "flavour"), ("humor", "humour"), ("rumor", "rumour")]
RE_ = [("center", "centre"), ("theater", "theatre"), ("meter", "metre"), ("liter", "litre")]
LL = [("canceled", "cancelled"), ("canceling", "cancelling"), ("traveled", "travelled"), ("traveling", "travelling"),
      ("modeling", "modelling"), ("labeled", "labelled")]
IZE = [("organize", "organise"), ("analyze", "analyse"), ("optimize", "optimise"), ("prioritize", "prioritise"),
       ("recognize", "recognise"), ("realize", "realise"), ("customize", "customise"), ("finalize", "finalise"),
       ("apologize", "apologise"), ("summarize", "summarise")]
CONTRACTION = re.compile(r"\b\w+(?:'|’)(?:s|re|ve|ll|d|t|m)\b", re.I)
NOT_CONTRACTION = re.compile(r"\b\w+(?:'|’)s\b")  # possessives look the same; counted separately


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def sections(text, level=2):
    """{title: body} for every heading at exactly this level."""
    hashes = "#" * level
    out = {}
    for m in re.finditer(rf"^{hashes}\s+(.+?)\s*\n(.*?)(?=^#{{1,{level}}}\s|\Z)", text, re.M | re.S):
        out.setdefault(m.group(1).strip(), m.group(2))
    return out


def find(secs, name):
    for k, v in secs.items():
        if re.match(rf"{re.escape(name)}(?![\w'])", k.replace("’", "'"), re.I):
            return v
    return None


def bullets(body):
    return [l.strip()[1:].strip() for l in body.splitlines() if l.strip().startswith(("-", "*"))]


def strip_tag(line):
    return re.sub(r"\[source:[^\]]*\]|\|.*$", "", line).strip()


def norm(s):
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", s).strip().lower()


def check_tag(line, where, add):
    if line.upper().startswith("TBD"):
        return
    m = TAG.search(line)
    if not m:
        add("FAIL", "untagged", f"{where}: no source tag: \"{line[:70]}\"")
        return
    tag = m.group(1)
    if not DATE.search(tag):
        add("FAIL", "tag-date", f"{where}: source tag has no YYYY-MM-DD date: \"{line[:70]}\"")
    st = STATUS.search(tag)
    if not st:
        add("FAIL", "tag-status", f"{where}: source tag has no status (confirmed or provisional): \"{line[:70]}\"")
    elif st.group(1).lower() == "assumed":
        add("WARN", "assumed", f"{where}: a voice rule shouldn't be assumed; make it provisional or TBD: \"{line[:60]}\"")


def word_list(body):
    out = []
    for line in bullets(body):
        if line.upper().startswith("TBD"):
            continue
        out += [w.strip().strip("'\"“”") for w in strip_tag(line).split(",") if w.strip()]
    return out


def check(a):
    try:
        text = read(a.file)
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    findings = []
    add = lambda level, code, msg: findings.append((level, code, msg))
    clean = re.sub(r"<!--.*?-->", "", text, flags=re.S)

    if not re.search(r"^#\s+\S", clean, re.M):
        add("FAIL", "title", "no '# Voice' title")
    lr = re.search(r"^Last reviewed:\s*(\S+)", clean, re.M)
    if not lr or not DATE.match(lr.group(1)):
        add("FAIL", "reviewed", "no 'Last reviewed: YYYY-MM-DD' line with a real date")
    for m in LEFTOVER.finditer(clean):
        add("FAIL", "leftover", f"template leftover: {m.group(0)}")

    secs = sections(clean, 2)
    for name in REQUIRED:
        body = find(secs, name)
        if body is None:
            add("FAIL", "section", f"missing section: ## {name}")
            continue
        if name == "By channel":
            continue
        if not bullets(body):
            add("FAIL", "empty", f"## {name} is empty; add the rules or a '- TBD: <what evidence is needed>' line")
    for name in RULE_SECTIONS:
        body = find(secs, name)
        for line in bullets(body or ""):
            check_tag(line, name, add)

    # By channel: only ### subsections, each with tagged bullets and readable limits
    bc = find(secs, "By channel")
    if bc is not None:
        pre = re.split(r"^###\s", bc, maxsplit=1, flags=re.M)[0]
        if bullets(pre):
            add("FAIL", "channel-format", "text under ## By channel that isn't inside a '### <Channel>' subsection")
        if re.search(r"^#{4,}\s", bc, re.M):
            add("FAIL", "channel-format", "channel headings must be '###', not '####'")
        subs = list(re.finditer(r"^###\s+(.+?)\s*\n(.*?)(?=^###\s|\Z)", bc, re.M | re.S))
        if not subs and not bullets(pre):
            add("FAIL", "empty", "## By channel has no '### <Channel>' subsections (or a TBD line)")
        for m in subs:
            ch, lines = m.group(1), bullets(m.group(2))
            if not lines:
                add("FAIL", "channel-empty", f"### {ch} has no bullets")
            for line in lines:
                check_tag(line, f"By channel / {ch}", add)
                body = strip_tag(line).lower()
                if line.upper().startswith("TBD"):
                    if LIMIT.search(body):
                        add("FAIL", "tbd-limit", f"### {ch}: a TBD line states a limit another skill would enforce: "
                                                 f"\"{LIMIT.search(body).group(0)}\"; reword the open question")
                    continue
                if re.search(r"exclamation", body) and not re.search(r"no exclamation marks?|(?:one|two|three|\d+) "
                                                                     r"exclamation marks?", body):
                    add("WARN", "limit-wording", f"### {ch}: exclamation rule isn't a clear limit; write 'No exclamation "
                                                 f"marks' or 'At most one exclamation mark'")
                if re.search(r"\bhashtag", body) and not re.search(r"no hashtags|(?:one|two|three|\d+) hashtags?", body):
                    add("WARN", "limit-wording", f"### {ch}: hashtag rule isn't a clear limit; write 'No hashtags' or "
                                                 f"'At most two hashtags'")
                if re.search(r"\d+\s*words", body) and not re.search(r"under \d+ words", body):
                    add("WARN", "limit-wording", f"### {ch}: write a word limit as 'Under N words'")

    # Word lists
    never = word_list(find(secs, "Words we never use") or "")
    use = word_list(find(secs, "Words we use") or "")
    seen = set()
    for w in never:
        if re.search(r"[()\"“”]", w) or len(w.split()) > 4:
            add("FAIL", "never-format", f"never-use entry isn't a plain word or phrase: \"{w[:60]}\"; move the reason "
                                        f"to ## Don't")
        if w.lower() in seen:
            add("WARN", "duplicate", f"'{w}' is on the never-use list twice")
        seen.add(w.lower())
    for w in never:
        for u in use:
            if not w or not u:
                continue
            if w.lower() == u.lower():
                add("FAIL", "both-lists", f"'{w}' is on both the use and never-use lists")
            elif re.search(rf"\b{re.escape(w.lower())}\b", u.lower()):
                add("FAIL", "never-in-use", f"never-use '{w}' is part of '{u}' on the use list; another skill would "
                                            f"flag every mention of '{u}'")

    # Spelling
    conv = {m.group(1).lower().replace("american", "us").replace("british", "uk") for m in SPELLING.finditer(clean)}
    if len(conv) > 1:
        add("FAIL", "spelling", f"more than one spelling convention named ({', '.join(sorted(conv))}); "
                                f"other skills read only the first")
    elif not conv and not re.search(r"TBD[^\n]*spelling", clean, re.I):
        add("WARN", "spelling", "no spelling convention stated (write 'US spelling', 'UK spelling' or 'Canadian "
                                "spelling', or a TBD line)")

    # Examples are quoted word for word from the evidence
    if a.evidence:
        corpus = ""
        for p in a.evidence:
            paths = [os.path.join(r, f) for r, _, fs in os.walk(p) for f in fs] if os.path.isdir(p) else [p]
            for f in paths:
                try:
                    corpus += norm(read(f)) + "\n"
                except (OSError, UnicodeDecodeError):
                    pass
        prev_text = ""
        if a.previous and os.path.exists(a.previous):
            prev_text = norm(read(a.previous))
        for line in bullets(find(secs, "Examples") or ""):
            if prev_text and norm(strip_tag(line)) in prev_text:
                continue  # an example kept from the previous version; its source was checked then
            for q in re.findall(r"[\"“]([^\"”]{8,400})[\"”]", strip_tag(line)):
                if norm(q) not in corpus:
                    add("FAIL", "example", f"example not found word for word in the evidence: \"{q[:60]}\"")

    # Confirmed rules from the previous version are kept
    if a.previous:
        try:
            prev = read(a.previous)
        except OSError as e:
            print(f"error: {e}", file=sys.stderr)
            return 2
        now = norm(clean)
        for line in prev.splitlines():
            s = line.strip()
            if s.startswith(("-", "*")) and re.search(r"·\s*confirmed", s, re.I):
                rule = norm(strip_tag(s[1:]))
                if rule and rule not in now:
                    add("FAIL", "dropped", f"confirmed rule from the previous version is gone or reworded: "
                                           f"\"{strip_tag(s[1:])[:70]}\"")

    fails = sum(1 for f in findings if f[0] == "FAIL")
    for level, code, msg in findings:
        print(f"{level} {code}: {msg}")
    print(f"{'FAIL' if fails else 'PASS'}: {fails} fail, {len(findings) - fails} warn")
    return 1 if fails else 0


def plain(text):
    text = re.sub(r"\[source:[^\]]*\]", " ", text)
    text = re.sub(r"(?m)^\s*(channel|approved by|written by|status|page|edits by|notes?)\b[^\n]*:\s.*$", " ", text, flags=re.I)
    text = re.sub(r"[#*_>`]", " ", text)
    return text


def stats_for(text):
    t = plain(text)
    words = re.findall(r"[A-Za-z0-9][A-Za-z0-9'’\-]*", t)
    sents = [s for s in re.split(r"(?<=[.!?])\s+|\n\s*\n|\n", t) if re.search(r"[A-Za-z]", s)]
    lens = [len(re.findall(r"[A-Za-z0-9][A-Za-z0-9'’\-]*", s)) for s in sents]
    low = t.lower()
    contr = [c for c in CONTRACTION.findall(t) if not re.search(r"(?:'|’)s$", c, re.I)
             or c.lower().split("'")[0].split("’")[0] in {"it", "that", "there", "here", "what", "who", "he", "she", "let"}]
    marks = {"us": [], "uk/ca -our/-re": [], "-ize": [], "-ise": [], "us -l-": [], "uk/ca -ll-": []}
    for us, uk in OUR + RE_:
        if re.search(rf"\b{us}\w*", low):
            marks["us"].append(us)
        if re.search(rf"\b{uk}\w*", low):
            marks["uk/ca -our/-re"].append(uk)
    for us, uk in LL:
        if re.search(rf"\b{us}\b", low):
            marks["us -l-"].append(us)
        if re.search(rf"\b{uk}\b", low):
            marks["uk/ca -ll-"].append(uk)
    for z, s in IZE:
        if re.search(rf"\b{z}\w*", low):
            marks["-ize"].append(z)
        if re.search(rf"\b{s}\w*", low):
            marks["-ise"].append(s)
    n = max(len(words), 1)
    return {
        "words": len(words), "sentences": len(sents),
        "avg_sentence": round(sum(lens) / max(len(lens), 1), 1), "longest_sentence": max(lens) if lens else 0,
        "contractions": len(contr), "contractions_per_100": round(100 * len(contr) / n, 1),
        "exclamation": t.count("!"), "question": t.count("?"), "em_dash": t.count("—") + t.count(" -- "),
        "hashtags": len(re.findall(r"(?<!\w)#[A-Za-z]\w+", text)),
        "i": len(re.findall(r"\b(I|I'm|I've|I'll|me|my)\b", t)), "we": len(re.findall(r"\b(we|we're|we've|our|us)\b", low)),
        "you": len(re.findall(r"\b(you|you're|you'll|your)\b", low)), "spelling": {k: v for k, v in marks.items() if v},
    }


def spelling_hint(sp):
    our = bool(sp.get("uk/ca -our/-re") or sp.get("uk/ca -ll-"))
    us = bool(sp.get("us") or sp.get("us -l-"))
    if not sp:
        return "no distinguishing words"
    if our and us:
        return "mixed (both US and UK/Canadian forms)"
    if us:
        return "US forms" + (" (with -ise: mixed)" if sp.get("-ise") else "")
    if sp.get("-ise") and sp.get("-ize"):
        return "mixed -ize/-ise"
    if our and sp.get("-ise"):
        return "UK forms"
    if our and sp.get("-ize"):
        return "Canadian forms (-our/-re with -ize)"
    if our:
        return "UK or Canadian (-our/-re; no -ize/-ise word to tell them apart)"
    return "-ize only (US or Canadian)" if sp.get("-ize") else "-ise only (UK)"


def stats(a):
    files = []
    for p in a.files:
        files += sorted(os.path.join(r, f) for r, _, fs in os.walk(p) for f in fs) if os.path.isdir(p) else [p]
    if not files:
        print("error: no files", file=sys.stderr)
        return 2
    total = ""
    for f in files:
        try:
            text = read(f)
        except (OSError, UnicodeDecodeError) as e:
            print(f"error: {f}: {e}", file=sys.stderr)
            return 2
        total += text + "\n\n"
        s = stats_for(text)
        print(f"{f}: {s['words']} words, {s['sentences']} sentences, avg {s['avg_sentence']}, longest "
              f"{s['longest_sentence']} | contractions {s['contractions']} ({s['contractions_per_100']}/100 words) | "
              f"! {s['exclamation']}  ? {s['question']}  em dash {s['em_dash']}  # {s['hashtags']} | "
              f"I {s['i']}  we {s['we']}  you {s['you']} | spelling: {spelling_hint(s['spelling'])} {s['spelling'] or ''}")
    if len(files) > 1:
        s = stats_for(total)
        print(f"TOTAL ({len(files)} files): {s['words']} words, avg sentence {s['avg_sentence']}, contractions "
              f"{s['contractions_per_100']}/100 words, ! {s['exclamation']}, spelling: {spelling_hint(s['spelling'])}")
    if sum(stats_for(read(f))["words"] for f in files) < 300 or len(files) < 3:
        print("NOTE: thin evidence (under 300 words or fewer than 3 files): rules from it are provisional")
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("file")
    c.add_argument("--evidence", nargs="*", help="sample, edit and feedback files or folders the examples must quote")
    c.add_argument("--previous", help="the voice.md before this change; its confirmed rules must survive")
    s = sub.add_parser("stats")
    s.add_argument("files", nargs="+")
    a = ap.parse_args()
    return check(a) if a.cmd == "check" else stats(a)


if __name__ == "__main__":
    sys.exit(main())
