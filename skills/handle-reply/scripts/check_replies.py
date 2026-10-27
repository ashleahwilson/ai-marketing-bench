#!/usr/bin/env python3
"""Mechanical checks for a reply-handling file. Standard library only.

Usage:
    python3 scripts/check_replies.py outreach/replies-2026-10-23.txt --today 2026-10-23
        [--brand brand/] [--suppression outreach/suppression.csv] [--log outreach/reply-log.csv]
        [--thread outreach/drafts-<name>.txt ...] [--summary]

File format: one block per contact who replied, blocks separated by a line of ===== (five or more).
Inside a block, header lines come first, then zero or more messages, each starting after a line of ---.

    CONTACT: Greg Pollard <greg@talvo.example> | Talvo
    CLASS: unsubscribe     # interested | question | objection | not-now | referral | wrong-person
                           # | out-of-office | unsubscribe | hostile | bounce
    ACTION: confirm        # reply | hold | confirm | none
    NEXT: suppressed; all sequences stopped
    FOLLOW-UP: none        # YYYY-MM-DD or none
    REPLY:
    > Stop emailing me.
    FACTS
    - none
    NEEDS YOU
    - none
    ---
    To: greg@talvo.example
    Kind: confirm          # reply | holding | confirm | ack | thanks | referral-first
    Subject: Re: forecast calls

    Done, you're off the list. Maya

Word counts exclude the greeting line, the sign-off and signature block, and the opt-out line.

Exit code: 0 if no FAIL, 1 if any FAIL, 2 on bad input.
"""

import argparse
import csv
import datetime
import os
import re
import sys

CLASSES = {"interested", "question", "objection", "not-now", "referral", "wrong-person",
           "out-of-office", "unsubscribe", "hostile", "bounce"}
ACTIONS = {"reply", "hold", "confirm", "none"}
KINDS = {"reply", "holding", "confirm", "ack", "thanks", "referral-first"}

# --- Limits (and why) -------------------------------------------------------
# A reply answers what was asked; past ~90 words it turns into a pitch. 120 is the hard ceiling.
REPLY_TARGET, REPLY_MAX = 90, 120
# An opt-out confirmation is one line. Anything longer starts to argue or sell.
CONFIRM_MAX, HOSTILE_MAX = 20, 50
# A "not now" acknowledgement or a thank-you to a referrer is a sentence or two.
ACK_MAX, THANKS_MAX = 40, 30
# A first email to a referred person follows cold first-touch limits.
FIRST_MIN, FIRST_MAX, FIRST_HARD = 50, 90, 110

OPT_OUT = re.compile(r"\b(remove me|take me off|unsubscribe|stop (emailing|e-mailing|contacting|sending|messaging)|"
                     r"don'?t (email|contact|message) me|do not (email|contact|message) me|opt(ed)? out|"
                     r"no more emails|off (your|the|this) (mailing )?list|leave me alone)\b", re.I)
OOO = re.compile(r"\b(out of (the )?office|away (from the office )?until|on (annual |parental |medical )?leave|"
                 r"limited access to (my )?e-?mail|automatic reply|auto-?reply|on vacation|back in the office)\b", re.I)
BOUNCE = re.compile(r"\b(delivery (has )?failed|undeliverable|address not found|user unknown|mailbox unavailable|"
                    r"recipient address rejected|5\.1\.1|delivery status notification|could not be delivered)\b", re.I)
HOSTILE = re.compile(r"\b(spam|spammer|reporting you|report you|how did you get|where did you get|scam|"
                     r"harass|f\*+|wtf)\b", re.I)
PITCH = re.compile(r"\b(review|demo|offer|free|call|chat|pricing|price|colleague|in case|change your mind|"
                   r"if you ever|door|keep in touch|future|down the road|reconsider|before you go|"
                   r"one last|quick look|worth a look|book)\b", re.I)
ENDORSE = re.compile(r"\b(recommended (you|that|we|us|i)|suggested (i|we) (reach|talk|contact|get in touch|email|speak)|"
                     r"suggested (you|that you|a call|we talk)|introduced|asked me to (reach|contact|email|get in touch)|"
                     r"referred me|thought you'?d be interested|said you'?d be interested|would love to hear|"
                     r"is a fan|vouched)\b", re.I)
HOLDING = re.compile(r"\b(i'?ll (confirm|check|find out|come back|get back|follow up with)|let me (check|confirm|find out)|"
                     r"i'?ll have (an )?answer|confirm and come back|check and come back)\b", re.I)
URL = re.compile(r"(https?://\S+|\bwww\.\S+|\b[\w-]+\.(?:com|ca|io|co|example|net|org)/\S*)", re.I)
NUMBER = re.compile(r"\$?\d[\d,]*(?:\.\d+)?%?")
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september",
          "october", "november", "december"]
SIGNOFF = re.compile(r"^(thanks|thank you|best|cheers|regards|all the best|talk soon|warmly|-|--)[,.!]?\s*$", re.I)
OPTOUT_LINE = re.compile(r"(reply \"?no\"?|unsubscribe|won'?t follow up|opt out|\{\{unsubscribe)", re.I)

findings = []


def add(level, where, msg):
    findings.append((level, where, msg))


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def words(text):
    return len(re.findall(r"[A-Za-z0-9$%][\w'’$%.,/&-]*", text))


def body_core(body, signer_names):
    """Strip greeting, sign-off/signature block and opt-out line; return text that counts."""
    lines = [l.rstrip() for l in body.strip().splitlines()]
    while lines and not lines[0].strip():
        lines.pop(0)
    if lines and re.match(r"^(hi|hello|hey|dear|good (morning|afternoon))\b.{0,40}[,:]?\s*$", lines[0], re.I):
        lines.pop(0)
    out = []
    for l in lines:
        s = l.strip()
        if OPTOUT_LINE.search(s) and len(s.split()) < 20:
            continue
        out.append(l)
    # cut the signature block: from the first sign-off line, or a line that is just the signer's name
    cut = len(out)
    for i, l in enumerate(out):
        s = l.strip()
        if SIGNOFF.match(s) or (s and any(s.lower().startswith(n.lower()) for n in signer_names) and len(s.split()) <= 8):
            cut = i
            break
    core = "\n".join(out[:cut])
    # one-liners like "Done, you're off the list. Maya": drop a trailing signer name
    for n in signer_names:
        core = re.sub(rf"[\s,–-]*{re.escape(n)}\s*$", "", core.strip())
    return core


def parse_blocks(text):
    blocks = [b for b in re.split(r"^={5,}\s*$", text, flags=re.M) if b.strip()]
    out = []
    for raw in blocks:
        parts = re.split(r"^---\s*$", raw, flags=re.M)
        head, msgs = parts[0], parts[1:]
        h = {"REPLY": [], "FACTS": [], "NEEDS YOU": []}
        section = None
        for line in head.splitlines():
            s = line.strip()
            if not s or s.startswith("#"):
                continue
            m = re.match(r"^(CONTACT|CLASS|ACTION|NEXT|FOLLOW-UP)\s*:\s*(.*)$", s)
            if m:
                h[m.group(1)] = m.group(2).split("#")[0].strip() if m.group(1) != "CONTACT" else m.group(2).strip()
                section = None
                continue
            if re.match(r"^REPLY\s*:?\s*$", s):
                section = "REPLY"
                continue
            if s in ("FACTS", "NEEDS YOU"):
                section = s
                continue
            if section == "REPLY":
                h["REPLY"].append(s.lstrip("> ").strip())
            elif section in ("FACTS", "NEEDS YOU") and s.startswith("-"):
                item = s[1:].strip()
                if item.lower() not in ("none", "(none)", "nothing"):
                    h[section].append(item)
        messages = []
        for m in msgs:
            if not m.strip():
                continue
            mh, body, in_body = {}, [], False
            for line in m.strip("\n").splitlines():
                if not in_body:
                    mm = re.match(r"^(To|Kind|Subject|Cc)\s*:\s*(.*)$", line.strip())
                    if mm:
                        mh[mm.group(1)] = mm.group(2).split("#")[0].strip() if mm.group(1) == "Kind" else mm.group(2).strip()
                        continue
                    if not line.strip():
                        in_body = True
                        continue
                    in_body = True
                body.append(line)
            mh["body"] = "\n".join(body)
            messages.append(mh)
        out.append((h, messages))
    return out


def email_of(s):
    m = re.search(r"[\w.+'-]+@[\w-]+(\.[\w-]+)+", s or "")
    return m.group(0).lower() if m else ""


def load_suppression(path):
    emails = set()
    if path and os.path.exists(path):
        for row in csv.DictReader(open(path, encoding="utf-8")):
            e = (row.get("email") or "").strip().lower()
            if e:
                emails.add(e)
    return emails


def brand_text(brand):
    if not brand or not os.path.isdir(brand):
        return {}
    return {f: read(os.path.join(brand, f)) for f in os.listdir(brand) if f.endswith(".md")}


def brand_rules(files):
    never, banned, no_bang, hidden = [], [], False, []
    voice = files.get("voice.md", "")
    m = re.search(r"## Words we never use\s*\n(.*?)(\n## |\Z)", voice, re.S)
    if m:
        for line in m.group(1).splitlines():
            line = re.sub(r"\[source:.*?\]", "", line).strip("- ").strip()
            never += [w.strip() for w in line.split(",") if w.strip()]
    em = re.search(r"### Email\s*\n(.*?)(\n### |\n## |\Z)", voice, re.S)
    if em and re.search(r"no exclamation", em.group(1), re.I):
        no_bang = True
    for line in files.get("rules.md", "").splitlines():
        if re.search(r"\b(don'?t|never|do not)\b", line, re.I):
            banned += [q for q in re.findall(r"\"([^\"]{4,})\"", line)]
    for line in files.get("proof.md", "").splitlines():
        if re.search(r"named:\s*(no|unconfirmed)", line, re.I):
            head = re.sub(r"^-\s*", "", line).split(":")[0]
            names = re.findall(r"^([^(,]+)", head) + re.findall(r"\),\s*([^,]+),", head)
            hidden += [n.strip() for n in names if len(n.strip()) > 3]
    return never, banned, no_bang, hidden


def parse_date(s):
    try:
        return datetime.date.fromisoformat(s.strip())
    except (ValueError, AttributeError):
        return None


def mentioned_date(text, today):
    """First 'Month D' date in the reply, as the next occurrence on or after today."""
    m = re.search(r"\b(" + "|".join(MONTHS) + r")\s+(\d{1,2})\b", text, re.I)
    if not m:
        return None
    mon, day = MONTHS.index(m.group(1).lower()) + 1, int(m.group(2))
    for y in (today.year, today.year + 1):
        try:
            d = datetime.date(y, mon, day)
        except ValueError:
            return None
        if d >= today:
            return d
    return None


def mentioned_month(text):
    m = re.search(r"\b(?:in|until|after|from|early|late|mid-?)\s+(" + "|".join(MONTHS) + r")\b", text, re.I)
    return MONTHS.index(m.group(1).lower()) + 1 if m else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--today", help="YYYY-MM-DD (default: system date)")
    ap.add_argument("--brand")
    ap.add_argument("--suppression")
    ap.add_argument("--log")
    ap.add_argument("--thread", nargs="*", default=[])
    ap.add_argument("--summary", action="store_true")
    a = ap.parse_args()

    try:
        text = read(a.file)
    except OSError as e:
        print(f"Cannot read {a.file}: {e}")
        sys.exit(2)
    today = parse_date(a.today) if a.today else datetime.date.today()
    blocks = parse_blocks(text)
    if not blocks:
        print("No blocks found. See the format in this script's header.")
        sys.exit(2)

    bfiles = brand_text(a.brand)
    never, banned, no_bang, hidden = brand_rules(bfiles)
    sources_text = "\n".join(bfiles.values()) + "\n" + "\n".join(read(t) for t in a.thread if os.path.exists(t))
    suppressed = load_suppression(a.suppression)
    log_text = read(a.log).lower() if a.log and os.path.exists(a.log) else None
    signer_names = []
    for line in bfiles.get("senders.md", "").splitlines():
        m = re.match(r"^## (.+)$", line)
        if m:
            full = m.group(1).strip()
            signer_names += [full, full.split()[0]]

    for i, (h, msgs) in enumerate(blocks, 1):
        contact = email_of(h.get("CONTACT"))
        where = f"block {i} ({contact or 'no contact'})"
        cls, act = h.get("CLASS", "").lower(), h.get("ACTION", "").lower()
        reply = " ".join(h["REPLY"])
        for k in ("CONTACT", "CLASS", "ACTION", "NEXT", "FOLLOW-UP"):
            if not h.get(k):
                add("FAIL", where, f"missing {k}:")
        if not contact:
            add("FAIL", where, "CONTACT has no email address")
        if cls and cls not in CLASSES:
            add("FAIL", where, f"unknown CLASS '{cls}'")
        if act and act not in ACTIONS:
            add("FAIL", where, f"unknown ACTION '{act}'")
        if not reply:
            add("WARN", where, "no REPLY: text quoted, so the class can't be cross-checked")

        # --- classification cross-checks
        if BOUNCE.search(reply) and cls != "bounce":
            add("FAIL", where, "reply reads as a bounce or delivery failure: CLASS should be bounce")
        elif OPT_OUT.search(reply) and cls not in ("unsubscribe", "hostile"):
            add("FAIL", where, f"reply contains an opt-out ('{OPT_OUT.search(reply).group(0)}'): CLASS must be unsubscribe or hostile")
        elif OOO.search(reply) and cls != "out-of-office" and not BOUNCE.search(reply):
            add("WARN", where, "reply reads like an automatic out-of-office: check CLASS")
        # an opt-out anywhere in the reply governs suppression and what may be said, whatever CLASS says
        if OPT_OUT.search(reply) and cls not in ("unsubscribe", "hostile") and not BOUNCE.search(reply):
            cls = "unsubscribe"
        if cls in ("out-of-office", "bounce") and act not in ("", "none"):
            add("FAIL", where, f"{cls}: ACTION must be none")
        if HOSTILE.search(reply) and cls not in ("hostile", "unsubscribe"):
            add("WARN", where, "reply sounds hostile: check CLASS")

        # --- follow-up dates
        fu = h.get("FOLLOW-UP", "").lower()
        fu_date = parse_date(fu)
        if cls in ("out-of-office", "not-now") and not fu_date:
            add("FAIL", where, f"{cls} needs a FOLLOW-UP date (YYYY-MM-DD)")
        if cls in ("unsubscribe", "hostile") and fu not in ("", "none"):
            add("FAIL", where, f"{cls}: FOLLOW-UP must be none (they asked not to be contacted)")
        if fu_date and fu_date <= today:
            add("FAIL", where, f"FOLLOW-UP {fu_date} is not after today ({today})")
        if cls == "out-of-office" and fu_date:
            back = mentioned_date(reply, today)
            if back and fu_date <= back:
                add("FAIL", where, f"follow-up {fu_date} is not after the return date {back}")
        if cls == "not-now" and fu_date:
            mon = mentioned_month(reply)
            if mon and fu_date.month != mon:
                add("WARN", where, f"they named {MONTHS[mon - 1].title()}; follow-up is {fu_date}")

        # --- suppression
        if cls in ("unsubscribe", "hostile", "bounce"):
            if a.suppression is None:
                add("WARN", where, f"{cls}: pass --suppression to confirm the address was added")
            elif contact and contact not in suppressed:
                add("FAIL", where, f"{cls}: {contact} is not in the suppression list")
            if log_text is not None and contact and contact not in log_text:
                add("FAIL", where, "contact missing from the status log")
        elif log_text is not None and contact and contact not in log_text:
            add("FAIL", where, "contact missing from the status log")

        if act in ("none",) and msgs:
            add("FAIL", where, "ACTION is none but a message is drafted")
        if act in ("reply", "hold", "confirm") and not msgs:
            add("FAIL", where, f"ACTION is {act} but no message is drafted")

        holding_used = False
        for j, m in enumerate(msgs, 1):
            mw = f"{where} msg {j}"
            to, kind, body = email_of(m.get("To")), (m.get("Kind") or "").lower(), m.get("body", "")
            if not to:
                add("FAIL", mw, "message has no To: address")
            if kind not in KINDS:
                add("FAIL", mw, f"Kind must be one of {', '.join(sorted(KINDS))}")
            core = body_core(body, signer_names or [""])
            n = words(core)
            low = core.lower()

            if to and to in suppressed and not (kind == "confirm" and to == contact):
                add("FAIL", mw, f"{to} is on the suppression list: draft nothing to them")
            if to and to != contact and kind != "referral-first":
                add("FAIL", mw, f"message to {to}, who isn't the contact: only a referral-first message may go to someone else")
            if kind == "referral-first":
                if cls not in ("referral", "unsubscribe", "hostile"):
                    add("FAIL", mw, f"a referral-first message needs a referral in the reply (CLASS is {cls})")
                if cls == "out-of-office":
                    add("FAIL", mw, "an out-of-office naming a colleague is not a referral")
                if to == contact:
                    add("FAIL", mw, "referral-first must go to the referred person, not the person who replied")
                if ENDORSE.search(core):
                    add("FAIL", mw, f"overstates the referral: '{ENDORSE.search(core).group(0)}'. Say only what they said")
                if not (FIRST_MIN <= n <= FIRST_MAX):
                    add("FAIL" if n > FIRST_HARD else "WARN", mw, f"first email to referred person is {n} words (target {FIRST_MIN}-{FIRST_MAX})")
                addr = re.search(r"Mailing address:\s*(.+?)\s*\[", bfiles.get("senders.md", ""))
                if addr and addr.group(1).split(",")[1].strip()[:12].lower() not in body.lower():
                    add("FAIL", mw, "cold first email to a new person needs the mailing address in the signature")
                if not OPTOUT_LINE.search(body):
                    add("FAIL", mw, "cold first email to a new person needs an opt-out line")
            elif cls in ("unsubscribe", "hostile"):
                limit = CONFIRM_MAX if cls == "unsubscribe" else HOSTILE_MAX
                if kind not in ("confirm",):
                    add("FAIL", mw, f"{cls}: the only message allowed to them is a confirmation (Kind: confirm)")
                if n > limit:
                    add("FAIL", mw, f"{cls} confirmation is {n} words (max {limit})")
                if "?" in core:
                    add("FAIL", mw, f"{cls}: no questions after an opt-out")
                if PITCH.search(core):
                    add("FAIL", mw, f"{cls}: pitch or door-opener after an opt-out ('{PITCH.search(core).group(0)}')")
                if URL.search(core):
                    add("FAIL", mw, f"{cls}: no links after an opt-out")
            elif cls in ("out-of-office", "bounce"):
                add("FAIL", mw, f"{cls}: draft nothing (no reply to an auto-reply or a dead address)")
            else:
                if kind == "ack" and n > ACK_MAX:
                    add("FAIL", mw, f"acknowledgement is {n} words (max {ACK_MAX})")
                elif kind == "thanks" and n > THANKS_MAX:
                    add("FAIL", mw, f"thank-you is {n} words (max {THANKS_MAX})")
                elif kind == "thanks" and PITCH.search(core):
                    add("WARN", mw, f"thank-you to a referrer reads as a pitch ('{PITCH.search(core).group(0)}')")
                elif n > REPLY_MAX:
                    add("FAIL", mw, f"reply is {n} words (max {REPLY_MAX})")
                elif n > REPLY_TARGET:
                    add("WARN", mw, f"reply is {n} words (aim for {REPLY_TARGET} or fewer)")
                if not m.get("Subject", "").lower().startswith("re:") and kind != "referral-first":
                    add("WARN", mw, "reply subject should be 'Re: ' plus the thread's subject")

            if HOLDING.search(core):
                holding_used = True
            # facts: numbers and links must trace
            facts = " ".join(h["FACTS"])
            for num in NUMBER.findall(core):
                bare = num.strip("$%").replace(",", "")
                if not bare or bare in ("1",) or len(bare) == 4 and bare.startswith("20"):
                    continue
                if bare in reply.replace(",", ""):
                    continue  # their own number (seats, locations, dates) from their reply
                if num not in facts and bare not in facts.replace(",", ""):
                    add("FAIL", mw, f"'{num}' isn't in this block's FACTS: add its source or cut it")
                elif sources_text.strip() and bare not in sources_text.replace(",", ""):
                    add("FAIL", mw, f"'{num}' isn't in brand memory or the thread")
            for u in URL.findall(core):
                u = u.rstrip(".,)")
                if sources_text.strip() and u.lower() not in sources_text.lower():
                    add("FAIL", mw, f"link {u} isn't in brand memory or the thread")
            for w in never:
                if re.search(rf"\b{re.escape(w)}\b", core, re.I):
                    add("FAIL", mw, f"brand never-use word: '{w}'")
            for p in banned:
                if p.lower() in low:
                    add("FAIL", mw, f"brand rule bans: \"{p}\"")
            for nm in hidden:
                if nm.lower() in low:
                    add("FAIL", mw, f"names '{nm}': proof not cleared for naming")
            if no_bang and "!" in core:
                add("FAIL", mw, "brand email voice: no exclamation marks")
            for f in h["FACTS"]:
                if "|" not in f:
                    add("FAIL", where, f"FACTS line has no source: '{f[:60]}'")

        if holding_used and not h["NEEDS YOU"]:
            add("FAIL", where, "a message promises to confirm something, but NEEDS YOU is empty")
        if h["NEEDS YOU"] and cls in ("question", "interested") and not holding_used:
            add("WARN", where, "NEEDS YOU has items, but no message tells them you'll come back on it")
        for f in h["FACTS"]:
            if re.search(r"·\s*assumed|\bassumed\b", f, re.I):
                add("FAIL", where, f"assumed fact used as a source: '{f[:60]}'")

    fails = sum(1 for f in findings if f[0] == "FAIL")
    warns = sum(1 for f in findings if f[0] == "WARN")
    if a.summary:
        print(f"{len(blocks)} replies checked: {fails} FAIL, {warns} WARN")
    else:
        for lvl, where, msg in findings:
            print(f"{lvl:4}  {where}: {msg}")
        print(f"\n{len(blocks)} replies checked: {fails} FAIL, {warns} WARN")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
