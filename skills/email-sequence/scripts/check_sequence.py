#!/usr/bin/env python3
"""Mechanical checks for a lifecycle email sequence file. Standard library only.

Usage:
    python3 scripts/check_sequence.py email/sequence-checklist.md --brand brand/
    python3 scripts/check_sequence.py email/sequence-trial.md --max-words 150 --summary

File format (also in references/sequence-file.md): a header, an optional FACTS / OPEN ledger, then one block
per email. Blocks are separated by lines containing only ---. In each email, the footer starts at a line that
is exactly "--" (the usual signature separator).

    SEQUENCE: Prime Cost Checklist nurture
    Type: nurture            # welcome | onboarding | nurture | trial | re-engagement | post-purchase | event | newsletter
    Audience: single-location owners who ticked the checklist form's consent box
    Consent basis: express consent, checkbox on the checklist form (timestamped)
    Sender: Hannah Ruiz, Co-founder, Tallyhouse
    Mailing address: Tallyhouse Inc., 410 Adelaide St W, Suite 300, Toronto, ON M5V 1S8
    Goal: book a free month-end review
    FACTS
    - offer: free month-end review, 30-minute call | brand/offer.md · confirmed
    - deadline: none on record          # a line starting "deadline:" or "limit:" or "sunset:" licenses that language
    OPEN
    - customer result for email 4 | not in brand memory
    ---
    Email: 1
    Job: deliver the checklist
    Trigger: ticks the box and submits the checklist form
    Timing: immediately
    Kind: marketing          # marketing (default) | service (onboarding steps, receipts: no unsubscribe required)
    Subject: Your Prime Cost Checklist
    Preview: Two pages. Fill it in with last month's numbers.
    CTA: Download the checklist -> https://tallyhouse.example/checklist.pdf
    Exit: unsubscribes, or books a review (leaves the sequence)

    Hi {{first_name}},

    Body...

    Hannah
    --
    Tallyhouse Inc., 410 Adelaide St W, Suite 300, Toronto, ON M5V 1S8
    Unsubscribe: {{unsubscribe_link}}

Levels:
    FAIL   rewrite before it goes to the user: missing fields, subject or preview problems, more than one link,
           no unsubscribe or address on a marketing email, over the word limit, banned words or phrases,
           exclamation marks the voice forbids, scarcity or deadline language with no basis in FACTS,
           figures or quotes that trace to nothing, naming a customer without permission, a bought list
    OPEN   needs a fact only the user has (placeholder, missing address or sender); list it, never invent it
    WARN   look at it: subject or preview length, all-caps words, urgent-sounding subjects, long sequences

Word counts exclude the greeting line, the sign-off (a short last paragraph) and the footer.
Exit code: 0 if no FAIL, 1 if any FAIL, 2 on bad input.
"""

import argparse
import os
import re
import sys

SUBJECT_MAX, SUBJECT_WARN = 60, 50            # most phones show 35-50 characters of a subject
PREVIEW_MIN, PREVIEW_MAX = 35, 140
MAX_EMAILS_WARN = 7                           # unsubscribes climb on long sequences; give a reason past 7
REQUIRED = ["job", "subject", "preview", "cta", "exit"]
URL = re.compile(r"https?://[^\s)>\]]+")
MERGE = re.compile(r"\{\{[^}]*\}\}|\{[a-z_]+\}|\*\|[A-Z_]+\|\*")
UNSUB = re.compile(r"unsubscribe|opt[- ]?out|manage (your )?preferences|\{\{[^}]*(unsub|opt|preference)[^}]*\}\}", re.I)
ADDRESS = re.compile(r"\b[A-Z]\d[A-Z] ?\d[A-Z]\d\b|\b[A-Z]{2} \d{5}(-\d{4})?\b|\b\d+\s+\w+(\s\w+)?\s(St|Street|Ave|Avenue|Rd|Road|Blvd|Drive|Dr|Way|Lane)\b")
PLACEHOLDER = re.compile(r"\[[a-z][a-z /-]*:[^\]]*\]|\[(your|insert|add|tbd|todo|link|url|address|mailing|placeholder|customer|name|company|real)[^\]]*\]|\bTBD\b|\bXX+\b", re.I)
SCARCITY = re.compile(r"only \d+ (spots?|seats?|places?|left)|\b(spots?|seats?|places?) (left|remaining)|\bcountdown\b|\bhurry\b|"
                      r"limited time|last chance|ends (tonight|today|tomorrow|soon|monday|tuesday|wednesday|thursday|friday|saturday|sunday)|"
                      r"expires? (tonight|today|tomorrow|soon|on)|before (it's|they're) gone|don'?t miss out|final hours", re.I)
DECEPTIVE = re.compile(r"\b(urgent|action required|final notice|account (suspended|locked|closed)|your (invoice|order|receipt)|payment failed)\b", re.I)
FIGURE = re.compile(r"\$\s?\d[\d,.]*\+?|(?<![\w.])\d[\d,.]*\s?%|(?<![\w.$])\d[\d,.]*[- ](?:x|hours?|days?|weeks?|months?|minutes?|clients?|customers?|"
                    r"restaurants?|clinics?|merchants?|locations?|owners?|users?|people|stores?)\b", re.I)
CAPS_OK = {"P&L", "POS", "CPA", "PDF", "FAQ", "USA", "CASL", "SMS", "HIPAA", "CEO", "CFO", "ROI", "US", "ET", "PT"}


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def norm(s):
    return re.sub(r"[\s,]", "", s.lower())


def flat(s):
    return re.sub(r"[^a-z0-9$%]+", " ", s.lower()).strip()


def section(text, heading):
    """Lines under a markdown heading (any level) until the next heading of the same or higher level."""
    m = re.search(rf"^(#+)\s*{re.escape(heading)}\s*$", text, re.M | re.I)
    if not m:
        return ""
    level = len(m.group(1))
    rest = text[m.end():]
    stop = re.search(rf"^#{{1,{level}}}\s", rest, re.M)
    return rest[:stop.start()] if stop else rest


def load_brand(path):
    b = {"corpus": "", "files": {}, "never": [], "banned": [], "no_bang": False, "max_words": None, "unnamed": []}
    if not path or not os.path.isdir(path):
        return b
    for name in sorted(os.listdir(path)):
        if name.endswith(".md"):
            b["files"][name] = read(os.path.join(path, name))
    b["corpus"] = "\n".join(b["files"].values())
    voice = b["files"].get("voice.md", "")
    for line in section(voice, "Words we never use").splitlines():
        line = re.sub(r"\[source:[^\]]*\]", "", line).strip("-* \t")
        b["never"] += [w.strip(" .") for w in line.split(",") if w.strip(" .")]
    email = section(voice, "Email")
    if re.search(r"no exclamation", email + section(voice, "Don't"), re.I) and re.search(r"no exclamation", email or voice, re.I):
        b["no_bang"] = True
    m = re.search(r"under (\d+) words", email, re.I)
    if m:
        b["max_words"] = int(m.group(1))
    for line in b["files"].get("rules.md", "").splitlines():
        if re.match(r"\s*-\s*(never|don'?t|do not|avoid)\b", line, re.I):
            b["banned"] += re.findall(r"[\"“]([^\"”]{2,60})[\"”]", line)
    for line in b["files"].get("proof.md", "").splitlines():
        if re.search(r"named:\s*(no|unconfirmed)", line, re.I):
            head = line.split(":")[0]
            b["unnamed"] += [n.strip() for n in re.findall(r"[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+", head)]
    return b


def parse(text):
    blocks = re.split(r"^\s*---\s*$", text, flags=re.M)
    head = blocks[0]
    meta = dict((k.strip().lower(), v.strip()) for k, v in re.findall(r"^([A-Za-z ]+):\s*(.*)$", head.split("FACTS")[0], re.M))
    facts = ""
    m = re.search(r"^FACTS\s*$(.*?)(?=^OPEN\s*$|\Z)", head, re.S | re.M)
    if m:
        facts = m.group(1)
    emails = []
    for blk in blocks[1:]:
        if not blk.strip():
            continue
        lines = blk.strip("\n").splitlines()
        fields, i = {}, 0
        while i < len(lines) and (re.match(r"^[A-Za-z][A-Za-z /-]*:\s", lines[i]) or not lines[i].strip() and not fields):
            if lines[i].strip():
                k, v = lines[i].split(":", 1)
                fields[k.strip().lower()] = v.strip()
            i += 1
        rest = lines[i:]
        cut = next((j for j, l in enumerate(rest) if l.strip() in ("--", "-- ", "[footer]")), None)
        body_lines = rest[:cut] if cut is not None else rest
        footer = "\n".join(rest[cut + 1:]) if cut is not None else ""
        emails.append({"fields": fields, "body": "\n".join(body_lines).strip(), "footer": footer})
    return meta, facts, emails


def countable(body):
    paras = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
    if paras and len(paras[0].split()) <= 6 and paras[0].rstrip().endswith(","):
        paras = paras[1:]
    elif paras and re.match(r"^(hi|hello|hey|dear)\b[^\n]{0,40},\s*\n", paras[0], re.I):
        paras[0] = paras[0].split("\n", 1)[1]
    if len(paras) > 1 and len(paras[-1].split()) <= 6:
        paras = paras[:-1]
    return " ".join(paras)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--brand", default="brand" if os.path.isdir("brand") else None)
    ap.add_argument("--max-words", type=int)
    ap.add_argument("--summary", action="store_true")
    a = ap.parse_args()
    try:
        text = read(a.file)
    except OSError as e:
        print(f"cannot read {a.file}: {e}")
        return 2
    brand = load_brand(a.brand)
    meta, facts, emails = parse(text)
    out = []
    add = lambda lvl, where, msg: out.append((lvl, where, msg))
    seq_type = meta.get("type", "").lower()
    max_words = a.max_words or brand["max_words"]
    known = facts + "\n" + brand["corpus"]

    # Sequence level
    consent = meta.get("consent basis", "")
    if not consent:
        add("FAIL", "sequence", "no 'Consent basis:' line: say how these people agreed to hear from you")
    elif PLACEHOLDER.search(consent):
        add("OPEN", "sequence", f"consent basis not confirmed: \"{consent}\"")
    elif re.search(r"\b(bought|purchased|rented|scraped|enriched)\s+(an?\s+|the\s+)?(\w+\s+)?(list|contacts|data|leads|emails)\b|data vendor|list vendor|list broker", consent, re.I):
        add("FAIL", "sequence", "consent basis is a bought, rented or scraped list: that's cold outreach, not a lifecycle sequence")
    sender, address = meta.get("sender", ""), meta.get("mailing address", "")
    if not address:
        m = re.search(r"Mailing address:\s*([^\[\n]+)", brand["files"].get("senders.md", ""))
        address = m.group(1).strip() if m and not PLACEHOLDER.search(m.group(1)) else ""
    if not sender or PLACEHOLDER.search(sender):
        add("OPEN", "sequence", "sender not confirmed")
    if not address or PLACEHOLDER.search(address):
        add("OPEN", "sequence", "mailing address not on file: required on marketing email (CASL, CAN-SPAM)")
    if not emails:
        add("FAIL", "sequence", "no emails found (separate blocks with a line containing only ---)")
    if len(emails) > MAX_EMAILS_WARN:
        add("WARN", "sequence", f"{len(emails)} emails: give a reason for more than {MAX_EMAILS_WARN}")
    licensed = bool(re.search(r"^\s*-\s*(deadline|limit|sunset)\s*:\s*(?!none)", facts, re.M | re.I))

    for n, e in enumerate(emails, 1):
        f, body, footer = e["fields"], e["body"], e["footer"]
        where = f"email {f.get('email', n)}"
        kind = f.get("kind", "marketing").lower()
        for k in REQUIRED:
            if not f.get(k):
                add("FAIL", where, f"missing '{k.upper() if k == 'cta' else k.capitalize()}:'")
        if not (f.get("timing") or f.get("trigger")):
            add("FAIL", where, "missing 'Timing:' or 'Trigger:'")
        subj, prev = f.get("subject", ""), f.get("preview", "")
        if subj:
            if len(subj) > SUBJECT_MAX:
                add("FAIL", where, f"subject is {len(subj)} characters (keep it to {SUBJECT_MAX}; phones cut it off)")
            elif len(subj) > SUBJECT_WARN:
                add("WARN", where, f"subject is {len(subj)} characters; under {SUBJECT_WARN} shows in full on most phones")
            if re.match(r"\s*(re|fwd?)\s*:", subj, re.I):
                add("FAIL", where, f"subject \"{subj}\" fakes a reply or forward: misleading subject line")
            if DECEPTIVE.search(subj):
                add("WARN", where, f"subject \"{subj}\" sounds like an account or transaction notice: make sure it's literally true")
            caps = [w for w in re.findall(r"\b[A-Z]{3,}\b", subj) if w not in CAPS_OK]
            if caps:
                add("WARN", where, f"all-caps in subject: {', '.join(caps)}")
        if prev:
            if flat(prev) == flat(subj):
                add("FAIL", where, "preview text repeats the subject")
            elif not PREVIEW_MIN <= len(prev) <= PREVIEW_MAX:
                add("WARN", where, f"preview is {len(prev)} characters (aim for {PREVIEW_MIN}-{PREVIEW_MAX})")

        # One primary CTA
        cta_urls = URL.findall(f.get("cta", ""))
        links = sorted({u.rstrip(".,;:") for u in URL.findall(body)})
        if seq_type != "newsletter" and len(links) > 1:
            add("FAIL", where, f"{len(links)} different links in the body ({', '.join(links)}): keep one primary call to action")
        if cta_urls and cta_urls[0].rstrip(".,;:") not in links:
            add("FAIL", where, f"the CTA link {cta_urls[0]} isn't in the body")

        # Footer
        if kind != "service":
            if not UNSUB.search(footer + "\n" + body):
                add("FAIL", where, "no unsubscribe link or instruction (required on marketing email)")
            addr_text = footer or body
            if address and not PLACEHOLDER.search(address):
                if norm(address[:20]) not in norm(addr_text) and not ADDRESS.search(addr_text):
                    add("FAIL", where, "no mailing address in the footer")
            elif PLACEHOLDER.search(addr_text):
                pass  # reported once at sequence level as OPEN
            elif not ADDRESS.search(addr_text):
                add("FAIL", where, "no mailing address in the footer (use a marked placeholder if it's unknown)")

        # Length and voice
        words = countable(body).split()
        if max_words and len(words) > max_words:
            add("FAIL", where, f"{len(words)} words; the limit is {max_words}")
        copy = "\n".join([subj, prev, body])
        if brand["no_bang"] and "!" in copy:
            add("FAIL", where, "exclamation mark (the brand's email voice has none)")
        for w in brand["never"]:
            if re.search(rf"(?<!\w){re.escape(w)}(?!\w)", copy, re.I):
                add("FAIL", where, f"never-use word \"{w}\"")
        for p in brand["banned"]:
            pat = re.escape(p).replace(r"\-", "[- ]?").replace(r"\ ", r"[\s-]+")
            if re.search(pat, copy, re.I):
                add("FAIL", where, f"\"{p}\" is banned by a brand rule")
        for name in brand["unnamed"]:
            if name.lower() in copy.lower():
                add("FAIL", where, f"names {name}, but permission to name them isn't confirmed in proof")

        # Honesty
        if SCARCITY.search(copy) and not licensed:
            add("FAIL", where, f"scarcity or deadline language (\"{SCARCITY.search(copy).group(0)}\") with no deadline or limit in FACTS")
        for m in FIGURE.finditer(copy):
            fig = m.group(0).strip()
            digits = re.sub(r"[^\d.]", "", fig).strip(".")
            unit = re.sub(r"[\d$,.%+\s-]", "", fig).lower()[:4]
            if not digits:
                continue
            hits = [l for l in known.splitlines() if re.search(rf"(?<![\d.]){re.escape(digits)}(?![\d])", l.replace(",", ""))
                    and (not unit or unit in l.lower()) and ("%" not in fig or "%" in l) and ("$" not in fig or "$" in l)]
            if not hits:
                add("FAIL", where, f"figure \"{fig}\" isn't in FACTS or brand memory")
            elif not any(re.search(r"confirmed|\|\s*(user|brief)", l) and not re.search(r"needs substantiation|don'?t use|never", l, re.I)
                         for l in hits):
                if any(re.search(r"needs substantiation|·\s*assumed|don'?t use|never", l, re.I) for l in hits):
                    add("FAIL", where, f"figure \"{fig}\" only traces to an unsubstantiated, assumed or banned claim")
                else:
                    add("WARN", where, f"figure \"{fig}\" traces only to a provisional fact: flag it for review")
        for q in re.findall(r"[\"“]([^\"”]{20,300})[\"”]", body):
            if flat(q) not in flat(known):
                add("FAIL", where, f"quote not on record word for word: \"{q[:60]}\"")
        for m in PLACEHOLDER.finditer(copy + "\n" + footer):
            if not (address and PLACEHOLDER.search(address) and m.group(0) in footer):
                add("OPEN", where, f"placeholder {m.group(0)}")

    order = {"FAIL": 0, "OPEN": 1, "WARN": 2}
    seen = []
    for item in sorted(out, key=lambda x: order[x[0]]):
        if item not in seen:
            seen.append(item)
    counts = {k: sum(1 for s in seen if s[0] == k) for k in order}
    if a.summary:
        print(f"{'FAIL' if counts['FAIL'] else 'PASS'}: {len(emails)} emails, {counts['FAIL']} fail, {counts['OPEN']} open, {counts['WARN']} warn")
    else:
        for lvl, where, msg in seen:
            print(f"{lvl} {where}: {msg}")
        print(f"{'FAIL' if counts['FAIL'] else 'PASS'}: {len(emails)} emails; {counts['FAIL']} fail, {counts['OPEN']} open, {counts['WARN']} warn")
    return 1 if counts["FAIL"] else 0


if __name__ == "__main__":
    sys.exit(main())
