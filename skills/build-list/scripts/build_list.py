#!/usr/bin/env python3
"""Merge, dedupe, suppress and score prospect accounts from the user's own files. Standard library only.

Build:
    python3 scripts/build_list.py build --source data/crm.csv --source data/expo.csv [--urls data/urls.txt]
        [--suppress data/suppression.csv] [--customers data/customers.csv] [--customer-name "Lantern Noodle Bar"]
        [--rubric icp/scoring.md] --out lists/prospects.csv

    Writes the scored list (--out) and <out>-excluded.csv, never touching the inputs, and prints a report:
    rows in, accounts after dedupe, merges, possible duplicates, exclusions by reason, suppressed contacts,
    personal emails, tiers, missing data, rubric lines it could not score, and countries (for the lawful-basis note).

Verify (self-check after any hand edit):
    python3 scripts/build_list.py verify lists/prospects.csv --source data/crm.csv [--urls ...] [--suppress ...]
    FAIL if any email, company or domain in the list isn't in a source, or a suppressed email or domain appears.

Rubric format (tolerant): one criterion per line, "criterion | points", a Markdown table, or "- criterion: +points".
Points may be negative, or DQ / disqualify / exclude. Criteria the script can read:
    "<field>: a, b, c" (text match any)   "<field> 2-15" / "2 to 15"   "<field> 15+" / "over 15" / "under 10" / "3"
Tier line, optional: "Tiers: A 70+, B 45+" (default: A at 70% of the maximum, B at 40%).

Words (reply length check):
    python3 scripts/build_list.py words lists/prospects-summary.md --max 300

Exit code: 0 OK, 1 verify or words FAIL, 2 bad input.
"""

import argparse
import csv
import os
import re
import sys
from collections import Counter, OrderedDict

LEGAL = {"inc", "incorporated", "ltd", "limited", "llc", "llp", "lp", "corp", "corporation", "co", "plc", "gmbh",
         "ag", "sa", "sarl", "ltee", "ulc", "pty", "bv", "nv", "srl", "spa", "kg", "the"}
GENERIC = {"group", "hospitality", "restaurant", "restaurants", "company", "holdings", "enterprises", "kitchen",
           "kitchens", "clinic", "dental", "services", "solutions", "and"}
PERSONAL = {"gmail.com", "googlemail.com", "hotmail.com", "hotmail.ca", "outlook.com", "live.com", "live.ca",
            "msn.com", "yahoo.com", "yahoo.ca", "ymail.com", "icloud.com", "me.com", "mac.com", "aol.com",
            "proton.me", "protonmail.com", "gmx.com", "gmx.de", "web.de", "shaw.ca", "telus.net", "rogers.com",
            "sympatico.ca", "bell.net", "videotron.ca", "cogeco.ca", "comcast.net", "verizon.net", "att.net",
            "sbcglobal.net", "mail.com", "zoho.com", "fastmail.com", "hey.com"}
MULTI_SUFFIX = {"co.uk", "org.uk", "ac.uk", "com.au", "net.au", "co.nz", "com.br", "co.jp", "com.mx", "co.za"}
ROLE = {"info", "hello", "contact", "sales", "admin", "office", "support", "team", "orders", "enquiries", "inquiries"}
CA_PROV = {"AB", "BC", "MB", "NB", "NL", "NS", "NT", "NU", "ON", "PE", "QC", "SK", "YT"}
COUNTRY = {"canada": "Canada", "ca": "Canada", "can": "Canada", "us": "US", "usa": "US", "united states": "US",
           "united states of america": "US", "u.s.": "US", "u.s.a.": "US", "america": "US", "uk": "UK",
           "united kingdom": "UK", "gb": "UK", "great britain": "UK", "england": "UK", "germany": "Germany",
           "de": "Germany", "deutschland": "Germany", "france": "France", "fr": "France", "ireland": "Ireland",
           "ie": "Ireland", "netherlands": "Netherlands", "nl": "Netherlands", "spain": "Spain", "es": "Spain",
           "italy": "Italy", "it": "Italy", "australia": "Australia", "au": "Australia", "mexico": "Mexico"}
EU_UK = {"UK", "Germany", "France", "Ireland", "Netherlands", "Spain", "Italy"}
H = {  # header synonyms, normalised (lowercase alphanumerics)
    "company": {"company", "companyname", "account", "accountname", "organization", "organisation", "org",
                "business", "businessname", "employer", "restaurant", "clinic", "practice", "firm", "store",
                "storename", "shop", "shopname", "brand", "merchant", "merchantname", "vendor", "vendorname",
                "exhibitor", "exhibitorname", "sponsor"},
    "domain": {"domain", "website", "web", "url", "site", "companywebsite", "companydomain", "websiteurl"},
    "email": {"email", "emailaddress", "workemail", "businessemail", "mail", "contactemail", "owneremail"},
    "first": {"firstname", "first", "givenname"},
    "last": {"lastname", "last", "surname", "familyname"},
    "person": {"name", "fullname", "contact", "contactname", "attendee", "attendeename", "person", "owner",
               "ownername"},
    "title": {"title", "jobtitle", "role", "position", "contacttitle"},
    "phone": {"phone", "phonenumber", "telephone", "mobile"},
    "city": {"city", "town"},
    "region": {"province", "state", "provincestate", "stateprovince", "region"},
    "country": {"country", "countrycode"},
}
DNC = {"donotcontact", "dnc", "optout", "emailoptout", "unsubscribed", "unsubscribe", "donotemail"}
STAGE = {"lifecyclestage", "lifecycle", "stage", "status", "accounttype", "type", "customerstatus", "relationship"}
TRUE = {"yes", "y", "true", "1", "x"}
GENERATED = {"rank", "tier", "score", "maxpossible", "reasons", "missing", "flags", "sources", "status", "emailtype",
             "othercontacts"}
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+'-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
DOMAIN_RE = re.compile(r"^(?:https?://)?(?:www\.)?([a-z0-9-]+(?:\.[a-z0-9-]+)+)(?:[:/?#].*)?$", re.I)


def norm_h(s):
    return re.sub(r"[^a-z0-9]", "", (s or "").lower())


def norm_domain(v):
    v = (v or "").strip().lower().lstrip("@")
    if not v or " " in v:
        return ""
    if "@" in v:
        v = v.split("@", 1)[1]
    m = DOMAIN_RE.match(v)
    return m.group(1).rstrip(".") if m else ""


def domain_root(d):
    parts = d.split(".")
    if len(parts) >= 3 and ".".join(parts[-2:]) in MULTI_SUFFIX:
        return parts[-3]
    return parts[-2] if len(parts) >= 2 else d


def name_tokens(name):
    s = (name or "").lower().replace("&", " and ").replace("+", " and ")
    s = re.sub(r"['’`]", "", s)
    toks = re.findall(r"[a-z0-9]+", s)
    while toks and toks[-1] in LEGAL:
        toks.pop()
    return [t for t in toks if t != "the"]


def name_key(name):
    if norm_domain(name) and "." in name and " " not in name.strip():
        return domain_root(norm_domain(name)).replace("-", "")
    return "".join(name_tokens(name))


def loose_key(name):
    return "".join(t for t in name_tokens(name) if t not in GENERIC)


def norm_country(v):
    return COUNTRY.get((v or "").strip().lower(), (v or "").strip())


def read_rows(path):
    if path.lower().endswith((".txt", ".lst")):
        with open(path, encoding="utf-8-sig") as f:
            return [{"line": ln.strip()} for ln in f if ln.strip() and not ln.startswith("#")]
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def map_headers(headers):
    m = {}
    for h in headers:
        n = norm_h(h)
        for k, syn in H.items():
            if n in syn and k not in m:
                m[k] = h
    if "person" in m and "company" not in m and norm_h(m["person"]) == "name":
        m["company"] = m.pop("person")
    return m


class Account:
    def __init__(self):
        self.names, self.domains, self.fields, self.contacts, self.sources = [], [], OrderedDict(), [], []
        self.flags, self.customer, self.country_from = [], False, ""


def parse_source(path, kind="csv"):
    """Yield (account_fragment, source_label) per row."""
    base = os.path.basename(path)
    if kind == "urls":
        with open(path, encoding="utf-8-sig") as f:
            for i, ln in enumerate(f, 1):
                d = norm_domain(ln.strip())
                if d:
                    a = Account()
                    a.domains.append(d)
                    a.sources.append(f"{base}:{i}")
                    yield a
        return
    rows = read_rows(path)
    if not rows:
        return
    hm = map_headers(rows[0].keys())
    used = set(hm.values())
    for i, r in enumerate(rows, 2):
        g = lambda k: (r.get(hm[k]) or "").strip() if k in hm else ""
        a = Account()
        a.sources.append(f"{base}:{i}")
        comp, web, email = g("company"), g("domain"), g("email").lower()
        if comp:
            a.names.append(comp)
            if norm_domain(comp) and " " not in comp:
                a.domains.append(norm_domain(comp))
        if norm_domain(web):
            a.domains.append(norm_domain(web))
        edom = email.split("@", 1)[1] if "@" in email else ""
        if edom and edom not in PERSONAL:
            a.domains.append(edom)
        person = g("person") or " ".join(x for x in (g("first"), g("last")) if x)
        for col, val in r.items():
            if col in used or val is None or not str(val).strip():
                continue
            n, v = norm_h(col), str(val).strip()
            if n in GENERATED:
                continue
            if n in DNC:
                if v.lower() in TRUE:
                    a.flags.append("dnc")
                continue
            if n in STAGE and re.match(r"^(current |active |existing )?(customer|client)s?$", v.lower()):
                a.customer = True
                continue
            a.fields[col.strip()] = v
        for k in ("city", "region", "country"):
            if g(k):
                a.fields[k] = g(k)
        if a.fields.get("country"):
            a.fields["country"] = norm_country(a.fields["country"])
        elif a.fields.get("region", "").upper() in CA_PROV:
            a.fields["country"] = "Canada"
            a.country_from = "province"
        if person or email:
            a.contacts.append({"name": person, "title": g("title"), "email": email, "phone": g("phone"),
                               "personal": edom in PERSONAL, "dnc": "dnc" in a.flags, "source": a.sources[0]})
        if not a.names and not a.domains:
            if not a.contacts:
                continue
        yield a


def merge(frags):
    """Union by domain, then by name key where domains don't conflict. Returns accounts, merge log, possible dupes."""
    parent = list(range(len(frags)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    doms = [set(f.domains) for f in frags]

    def union(a, b, need_compat):
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        if need_compat and doms[ra] and doms[rb] and not (doms[ra] & doms[rb]):
            return
        parent[rb] = ra
        doms[ra] |= doms[rb]

    by_dom, by_key = {}, {}
    for i, f in enumerate(frags):
        for d in f.domains:
            if d in by_dom:
                union(by_dom[d], i, False)
            else:
                by_dom[d] = i
    for i, f in enumerate(frags):
        keys = {name_key(n) for n in f.names if name_key(n)} | {domain_root(d).replace("-", "") for d in f.domains}
        for k in keys:
            if k in by_key:
                union(by_key[k], i, True)
            else:
                by_key[k] = i
    groups = OrderedDict()
    for i in range(len(frags)):
        groups.setdefault(find(i), []).append(frags[i])
    accounts, log = [], []
    for members in groups.values():
        a = Account()
        for m in members:
            a.names += m.names
            a.domains += [d for d in m.domains if d not in a.domains]
            a.sources += m.sources
            a.customer |= m.customer
            a.country_from = a.country_from or m.country_from
            for k, v in m.fields.items():
                if k in a.fields and a.fields[k].lower() != v.lower():
                    a.flags.append(f"conflict: {k} '{a.fields[k]}' vs '{v}' ({m.sources[0]}); kept the first")
                a.fields.setdefault(k, v)
            for c in m.contacts:
                dup = next((x for x in a.contacts if (c["email"] and x["email"] == c["email"]) or
                            (c["name"] and x["name"].lower() == c["name"].lower())), None)
                if dup:
                    for k in ("title", "email", "phone"):
                        dup[k] = dup[k] or c[k]
                    dup["dnc"] |= c["dnc"]
                else:
                    a.contacts.append(dict(c))
        real = [n for n in a.names if not (norm_domain(n) and " " not in n)]
        a.company = (real or a.names or [""])[0]
        a.domain = a.domains[0] if a.domains else ""
        if len(members) > 1:
            log.append(f"{a.company or a.domain} <- {', '.join(a.sources)}")
        accounts.append(a)
    loose = {}
    for a in accounts:
        k = loose_key(a.company) if a.company else ""
        if len(k) >= 4:
            loose.setdefault(k, []).append(a)
    possible = [" / ".join(f"{x.company} ({x.domain or 'no domain'}, {x.fields.get('city', '?')})" for x in v)
                for v in loose.values() if len(v) > 1]
    return accounts, log, possible


def load_exclusions(paths):
    emails, domains, keys = set(), set(), set()
    for p in paths or []:
        for r in read_rows(p):
            hm = map_headers(r.keys())
            for col, val in r.items():
                v = (val or "").strip()
                if not v:
                    continue
                for e in EMAIL_RE.findall(v):
                    emails.add(e.lower())
                if EMAIL_RE.search(v):
                    continue
                if norm_domain(v) and " " not in v:
                    domains.add(norm_domain(v))
                elif col == hm.get("company") or col == "line":
                    keys.add(name_key(v))
    return emails, domains, keys


# ---------- rubric ----------
NUM = r"(\d+(?:\.\d+)?)"


def parse_points(s):
    s = s.strip().lower()
    if re.search(r"\b(dq|disqualif\w*|exclude\w*|knock-?out|reject)\b", s):
        return "DQ"
    m = re.search(r"([+-]?\s*\d+)\s*(?:pts?|points?)?\s*$", s)
    return int(m.group(1).replace(" ", "")) if m else None


def parse_rubric(text):
    crits, tiers, section_dq = [], {}, False
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith("#"):
            section_dq = bool(re.search(r"disqualif|exclu|knock|deal-?breaker", line, re.I))
            continue
        if re.search(r"\btiers?\b", line, re.I) and re.search(r"\b[A-D]\b", line):
            for t, n in re.findall(r"\b([A-D])\b\s*(?:tier)?\s*(?::|=|≥|>=|at)?\s*(\d+)\s*(?:\+|–|-|or more|and up|to)",
                                   line):
                tiers[t] = int(n)
            if tiers:
                continue
        if line.startswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c) or norm_h(cells[0]) in {"criterion", "criteria",
                                                                                            "signal", "attribute"}:
                continue
            pts = next((parse_points(c) for c in cells[1:] if parse_points(c) is not None), None)
            if pts is None and section_dq:
                pts = "DQ"
            if pts is not None and cells[0]:
                crits.append((cells[0], pts))
            continue
        line = re.sub(r"^([-*•]|\d+[.)])\s*", "", line)
        m = re.match(r"^(dq|disqualify|exclude|knockout)\s*[:\-–—]\s*(.+)$", line, re.I)
        if m:
            crits.append((m.group(2).strip(), "DQ"))
            continue
        if "|" in line:
            left, right = line.rsplit("|", 1)
            pts = parse_points(right)
            if pts is not None:
                crits.append((left.strip(), pts))
                continue
        m = re.match(r"^(.+?)\s*[:=\-–—]\s*([+-]?\s*\d+\s*(?:pts?|points?)?|dq|disqualif\w*|exclude\w*)\s*$", line, re.I)
        if m:
            crits.append((m.group(1).strip(), parse_points(m.group(2))))
            continue
        m = re.match(r"^([+-]\s*\d+)\s*(?:pts?|points?)?\s*[:\-–—]?\s*(.+)$", line)
        if m:
            crits.append((m.group(2).strip(), int(m.group(1).replace(" ", ""))))
            continue
        if section_dq and len(line) < 80:
            crits.append((line, "DQ"))
    return crits, tiers


def parse_numeric(v):
    v = v.lower().replace("–", "-").replace("—", "-").strip()
    pats = [(rf"^(?:between\s*)?{NUM}\s*(?:-|to|and)\s*{NUM}$", lambda a, b: (float(a), float(b))),
            (rf"^{NUM}\s*(?:\+|or more|and up|plus)$", lambda a: (float(a), float("inf"))),
            (rf"^(?:at least|>=|≥|min(?:imum)?)\s*{NUM}$", lambda a: (float(a), float("inf"))),
            (rf"^(?:over|more than|above|>)\s*{NUM}$", lambda a: (float(a) + 1e-9, float("inf"))),
            (rf"^(?:under|less than|below|fewer than|<)\s*{NUM}$", lambda a: (float("-inf"), float(a) - 1e-9)),
            (rf"^(?:at most|<=|≤|up to)\s*{NUM}$", lambda a: (float("-inf"), float(a))),
            (rf"^{NUM}$", lambda a: (float(a), float(a)))]
    for p, f in pats:
        m = re.match(p, v)
        if m:
            return f(*m.groups())
    return None


def parse_rule(text):
    t = text.replace("–", "-").replace("—", "-").strip()
    m = re.match(r"^(.+?)\s*(?::|=|\bis\b|\bin\b|\bincludes?\b|\bcontains?\b|\buses\b)\s*(.+)$", t, re.I)
    if m:
        field, val = m.group(1).strip(), m.group(2).strip()
        rng = parse_numeric(val)
        if rng:
            return {"field": field, "num": rng}
        vals = [x.strip().lower() for x in re.split(r",|/|\bor\b|;", val) if x.strip()]
        return {"field": field, "vals": vals}
    m = re.match(r"^([a-z][a-z /_]*?)\s+((?:over|under|more than|less than|fewer than|at least|at most|up to|above|"
                 r"below|between|>=|<=|>|<)?\s*\d[\d.]*\s*(?:\+|or more|and up|-\s*\d+|to\s*\d+|and\s*\d+)?)$", t, re.I)
    if m:
        rng = parse_numeric(m.group(2))
        if rng:
            return {"field": m.group(1).strip(), "num": rng}
    return None


FIELD_SYN = {"locations": {"location", "locations", "sites", "units", "outlets", "restaurants", "stores", "branches"},
             "employees": {"employees", "headcount", "staff", "employeecount", "teamsize"},
             "title": {"title", "contacttitle", "jobtitle", "role", "contactrole", "persona"},
             "pos": {"pos", "pointofsale", "possystem"}, "country": {"country"},
             "region": {"province", "state", "region", "provincestate"}}


def resolve_field(field, columns):
    n = norm_h(field)
    if n in FIELD_SYN["title"] or n.endswith("title"):
        return "@title"
    cols = {norm_h(c): c for c in columns}
    if n in cols:
        return cols[n]
    for group in FIELD_SYN.values():
        if n in group:
            for c in cols:
                if c in group:
                    return cols[c]
    for c, orig in cols.items():
        if len(n) >= 3 and (n in c or c in n):
            return orig
    return None


def first_range(v):
    v = v.replace("–", "-").replace(",", "")
    m = re.search(rf"{NUM}\s*-\s*{NUM}", v)
    if m:
        return float(m.group(1)), float(m.group(2))
    m = re.search(NUM, v)
    return (float(m.group(1)), float(m.group(1))) if m else None


def evaluate(rule, col, a):
    """Return True/False, or None when the data is missing or unclear."""
    if col == "@title":
        vals = [c["title"].lower() for c in a.contacts if c["title"] and not c["dnc"]]
        if not vals:
            return None
        return any(re.search(rf"\b{re.escape(x)}", t) for x in rule.get("vals", []) for t in vals)
    v = a.fields.get(col, "")
    if not v:
        return None
    if "num" in rule:
        r = first_range(v)
        if not r:
            return None
        lo, hi = rule["num"]
        if lo <= r[0] and r[1] <= hi:
            return True
        if r[1] < lo or r[0] > hi:
            return False
        return None
    lv = v.lower()
    if norm_h(col) == "country":
        lv = norm_country(v).lower()
        return any(norm_country(x).lower() == lv for x in rule["vals"])
    return any(re.search(rf"\b{re.escape(x)}\b", lv) for x in rule["vals"])


# ---------- build ----------
def build(a):
    frags, counts = [], OrderedDict()
    for p in a.existing or []:
        rows = list(parse_source(p))
        counts[p + " (existing list)"] = len(rows)
        frags += rows
    for p in a.source or []:
        rows = list(parse_source(p))
        counts[p] = len(rows)
        frags += rows
    for p in a.urls or []:
        rows = list(parse_source(p, "urls"))
        counts[p] = len(rows)
        frags += rows
    old = {os.path.basename(p) for p in a.existing or []}
    if not frags:
        sys.exit("No rows found in the sources.")
    accounts, merged, possible = merge(frags)
    s_em, s_dom, s_key = load_exclusions(a.suppress)
    c_em, c_dom, c_key = load_exclusions(a.customers)
    c_key = c_key | {name_key(n) for n in a.customer_name or []}
    columns = sorted({k for x in accounts for k in x.fields})
    crits, tiers = parse_rubric(open(a.rubric, encoding="utf-8").read()) if a.rubric else ([], {})
    rules, unscored, nocol = [], [], []
    for text, pts in crits:
        r = parse_rule(text)
        col = resolve_field(r["field"], columns) if r else None
        if not r:
            unscored.append(f"{text} ({pts})")
        elif not col:
            nocol.append(f"{text} ({pts}): no column for '{r['field']}'")
            rules.append((text, pts, r, None))
        else:
            rules.append((text, pts, r, col))
    per_field = {}
    for text, pts, r, col in rules:
        if isinstance(pts, int) and pts > 0:
            k = col or r["field"]
            per_field[k] = max(per_field.get(k, 0), pts)
    max_total = sum(per_field.values())
    if not tiers and max_total:
        tiers = {"A": round(max_total * 0.7), "B": round(max_total * 0.4)}

    kept, excluded, removed, personal, missing_ct = [], [], [], [], Counter()
    for x in accounts:
        keys = {name_key(n) for n in x.names} | {domain_root(d).replace("-", "") for d in x.domains}
        emails = {c["email"] for c in x.contacts if c["email"]}
        label = x.company or x.domain or (x.contacts[0]["name"] if x.contacts else "?")
        if set(x.domains) & s_dom or keys & s_key:
            excluded.append((x, "suppression list", "company or domain is on the suppression list"))
            continue
        named = {name_key(n) for n in a.customer_name or []}
        if x.customer or set(x.domains) & c_dom or keys & c_key or emails & c_em:
            why = ("CRM stage is Customer" if x.customer else
                   "named as a client in brand memory" if keys & named and not (set(x.domains) & c_dom or emails & c_em
                                                                               or keys & (c_key - named)) else
                   "on the customer list")
            excluded.append((x, "existing customer", why))
            continue
        rm_here = 0
        for c in list(x.contacts):
            if c["email"] in s_em or c["dnc"]:
                rm_here += 1
                removed.append(f"{c['name'] or c['email']} ({label}): {'do-not-contact flag' if c['dnc'] else 'suppression list'}")
                x.contacts.remove(c)
        if not x.contacts and rm_here:
            x.flags.append("no contact left after suppression: find another contact")
        x.score, x.maxp, x.reasons, x.missing, dq = 0, 0, [], [], None
        miss_fields = {}
        for text, pts, r, col in rules:
            res = evaluate(r, col, x) if col else None
            if res is None:
                if isinstance(pts, int) and pts > 0:
                    k = col or r["field"]
                    miss_fields[k] = max(miss_fields.get(k, 0), pts)
                elif pts == "DQ" and col:
                    x.flags.append(f"not checked (data missing): {text}")
                continue
            if res and pts == "DQ":
                dq = text
            elif res and isinstance(pts, int):
                x.score += pts
                shown = "; ".join(c["title"] for c in x.contacts if c["title"]) if col == "@title" else x.fields.get(col, "")
                x.reasons.append(f"{pts:+d} {'title' if col == '@title' else col} ({shown})")
        if dq:
            col = next(c for t, p, r, c in rules if t == dq)
            excluded.append((x, "disqualified by rubric", f"{dq} ({x.fields.get(col, '') if col != '@title' else 'title'})"))
            continue
        for k in miss_fields:
            if not any(k in r for r in x.reasons):
                x.missing.append({"@title": "title", "region": "province/state"}.get(k, k))
                missing_ct["title" if k == "@title" else k] += 1
        x.maxp = x.score + sum(v for k, v in miss_fields.items() if not any(k in r for r in x.reasons))
        x.tier = next((t for t in sorted(tiers) if x.score >= tiers[t]), chr(ord(max(tiers or {"B": 0})) + 1)) if rules else ""
        if rules:
            best = next((t for t in sorted(tiers) if x.maxp >= tiers[t]), "")
            if best and best < x.tier:
                x.flags.append(f"could reach tier {best} once missing data is filled")
        if x.country_from:
            x.flags.append("country taken from province code")
        for c in x.contacts:
            if c["personal"]:
                personal.append(f"{c['name'] or c['email']} ({label}): {c['email']}")
                x.flags.append(f"personal email {c['email']}: not for cold email without consent")
        if not x.company:
            x.missing.append("company name")
        if not x.contacts:
            x.missing.append("contact")
        elif not any(c["email"] for c in x.contacts):
            x.missing.append("email")
        kept.append(x)
    for x in kept + [e[0] for e in excluded]:
        x.status = ("on existing list" if any(s.split(":")[0] in old for s in x.sources) else "new") if old else ""
    kept.sort(key=lambda x: (-x.score, -x.maxp, (x.company or x.domain).lower()))
    columns = [c for c in columns if norm_h(c) not in {"rank", "tier", "score", "maxpossible", "reasons", "missing",
                                                       "flags", "sources", "status", "otheremails", "othercontacts",
                                                       "emailtype"}]
    write_out(a.out, kept, excluded, columns)

    total_rows = sum(counts.values())
    print("INPUT")
    for p, n in counts.items():
        print(f"  {p}: {n} rows")
    print(f"ACCOUNTS: {total_rows} rows -> {len(accounts)} unique accounts ({total_rows - len(accounts)} rows merged)")
    for m in merged:
        print(f"  merged: {m}")
    for p in possible:
        print(f"  POSSIBLE DUPLICATE (not merged, review): {p}")
    print(f"EXCLUDED: {len(excluded)}")
    for reason, n in Counter(r for _, r, _ in excluded).items():
        names = ", ".join(x.company or x.domain for x, r, _ in excluded if r == reason)
        print(f"  {reason}: {n} ({names})")
    for x, r, d in excluded:
        if r == "disqualified by rubric":
            print(f"    {x.company or x.domain}: {d}")
    print(f"CONTACTS REMOVED: {len(removed)}")
    for r in removed:
        print(f"  {r}")
    print(f"PERSONAL EMAILS (flagged): {len(personal)}")
    for p in personal:
        print(f"  {p}")
    print(f"KEPT: {len(kept)}")
    if old:
        new = [x.company or x.domain for x in kept if x.status == "new"]
        print(f"  new accounts not on the existing list: {len(new)} ({', '.join(new)})")
        print(f"  already on the existing list: {sum(1 for x in kept if x.status != 'new')}")
        dup = [x.company or x.domain for x in kept + [e[0] for e in excluded] if x.status != "new"
               and any(s.split(':')[0] not in old for s in x.sources)]
        print(f"  incoming rows that matched an account already on the list: {', '.join(dup) or 'none'}")
    if rules:
        tc = Counter(x.tier for x in kept)
        print("  tiers: " + ", ".join(f"{t}: {tc[t]}" for t in sorted(tc)) + f"  (thresholds {tiers}, max {max_total})")
        top = [f"{x.company or x.domain} {x.score}" for x in kept if x.tier == "A"]
        print("  tier A: " + (", ".join(top) or "none"))
    print("MISSING DATA: " + (", ".join(f"{k} {v}" for k, v in missing_ct.items()) or "none"))
    flagged = [x for x in kept if any(f.startswith("conflict") for f in x.flags)]
    for x in flagged:
        print(f"  {x.company}: " + "; ".join(f for f in x.flags if f.startswith("conflict")))
    print("RUBRIC: " + (f"{len(rules)} criteria scored" if rules else "none given"))
    for u in unscored:
        print(f"  NOT SCORED (no rule could be read, rewrite as field: value): {u}")
    for n in nocol:
        print(f"  NO DATA COLUMN: {n}")
    cc = Counter(x.fields.get("country", "unknown") or "unknown" for x in kept)
    print("COUNTRIES: " + ", ".join(f"{k} {v}" for k, v in cc.most_common()))
    regimes = sorted({"CASL" if k == "Canada" else "CAN-SPAM" if k == "US" else "GDPR/PECR" if k in EU_UK else
                      "check local rules" for k in cc})
    print("LAWFUL BASIS TO COVER: " + ", ".join(regimes))
    print(f"WROTE: {a.out}, {excl_path(a.out)}")


def excl_path(out):
    root, ext = os.path.splitext(out)
    return f"{root}-excluded{ext or '.csv'}"


def write_out(out, kept, excluded, columns):
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    extra = [c for c in columns if c not in ("city", "region", "country")]
    head = ["rank", "tier", "score", "max_possible", "status", "company", "domain", "country", "region", "city"] + extra + [
        "contact_name", "contact_title", "contact_email", "email_type", "other_contacts", "reasons", "missing",
        "flags", "sources"]
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(head)
        for i, x in enumerate(kept, 1):
            cs = sorted(x.contacts, key=lambda c: (c["personal"], not c["email"]))
            p = cs[0] if cs else {"name": "", "title": "", "email": "", "personal": False}
            role = p["email"].split("@")[0] in ROLE if p["email"] else False
            others = "; ".join(f"{c['name']} ({c['title']})" + ("" if c["personal"] else f" <{c['email']}>") for c in cs[1:])
            w.writerow([i, x.tier, x.score, x.maxp, x.status, x.company, x.domain, x.fields.get("country", ""),
                        x.fields.get("region", ""), x.fields.get("city", "")] + [x.fields.get(c, "") for c in extra] +
                       [p["name"], p["title"], "" if p["personal"] else p["email"],
                        ("personal (withheld, see flags)" if p["personal"] else "role" if role else "business") if p["email"] else "",
                        others, "; ".join(x.reasons), "; ".join(x.missing), "; ".join(dict.fromkeys(x.flags)),
                        "; ".join(x.sources)])
    with open(excl_path(out), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["company", "domain", "reason", "detail", "sources"])
        for x, r, d in excluded:
            w.writerow([x.company, x.domain, r, d, "; ".join(x.sources)])


def verify(a):
    src_text, fails = "", []
    for p in (a.source or []) + (a.urls or []):
        src_text += open(p, encoding="utf-8-sig").read().lower() + "\n"
    src_keys = {name_key(t) for t in re.split(r"[,\n\"]", src_text) if t.strip()}
    by_acct = {}
    for p in a.source or []:
        for fr, r in zip(parse_source(p), read_rows(p)):
            for k in {name_key(n) for n in fr.names} | set(fr.domains):
                by_acct.setdefault(k, []).append({norm_h(c): (v or "").strip().lower() for c, v in r.items()})
    s_em, s_dom, s_key = load_exclusions(a.suppress)
    rows = read_rows(a.list)
    for i, r in enumerate(rows, 2):
        comp = (r.get("company") or "").strip()
        if comp and name_key(comp) not in src_keys and comp.lower() not in src_text:
            fails.append(f"row {i}: company '{comp}' isn't in any source")
        dom = (r.get("domain") or "").strip().lower()
        if dom and dom not in src_text:
            fails.append(f"row {i}: domain '{dom}' isn't in any source")
        if dom and dom in s_dom:
            fails.append(f"row {i}: domain '{dom}' is on the suppression list")
        srcs = by_acct.get(name_key(comp), []) + by_acct.get(dom, [])
        for col, val in r.items():
            v, n = (val or "").strip().lower(), norm_h(col or "")
            if not v or n in GENERATED or EMAIL_RE.search(v) or n in {"company", "domain", "contactname", "contacttitle"}:
                continue
            seen = [s_[n] for s_ in srcs if n in s_]
            if n == "country":
                seen, v = [norm_country(x).lower() for x in seen], norm_country(v).lower()
            if (seen and v not in seen) or (not seen and n not in {"country", "region", "city"} and v not in src_text):
                fails.append(f"row {i}: {col} '{val}' doesn't match the source rows for this account (invented?)")
        for e in EMAIL_RE.findall(" ".join(str(v) for v in r.values())):
            if e.lower() not in src_text:
                fails.append(f"row {i}: email '{e}' isn't in any source (invented?)")
            if e.lower() in s_em:
                fails.append(f"row {i}: email '{e}' is on the suppression list")
    for f in fails:
        print("FAIL " + f)
    print("PASS: every company, domain and email traces to a source; nothing suppressed" if not fails else
          f"{len(fails)} FAIL")
    return 1 if fails else 0


def words(a):
    text = open(a.file, encoding="utf-8").read()
    text = "\n".join(l for l in text.splitlines() if not re.fullmatch(r"\s*\|?[\s:|-]+\|?\s*", l))
    n = len(re.findall(r"\S+", re.sub(r"[*#|`>]", " ", text)))
    ok = n <= a.max
    print(f"{'PASS' if ok else 'FAIL'}: {n} words (limit {a.max})")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build")
    v = sub.add_parser("verify")
    w = sub.add_parser("words")
    w.add_argument("file")
    w.add_argument("--max", type=int, default=300)
    v.add_argument("list")
    for p in (b, v):
        p.add_argument("--source", action="append", help="CSV export (repeatable)")
        p.add_argument("--urls", action="append", help="text file, one URL per line (repeatable)")
        p.add_argument("--suppress", action="append", help="suppression list: emails, domains or company names")
    b.add_argument("--existing", action="append", help="an earlier list to add to (read, never overwritten)")
    b.add_argument("--customers", action="append", help="current customers: names, domains or emails")
    b.add_argument("--customer-name", action="append", help="a customer named elsewhere (e.g. brand memory)")
    b.add_argument("--rubric", help="scoring rubric, e.g. icp/scoring.md, or a criteria file you wrote")
    b.add_argument("--out", required=True)
    a = ap.parse_args()
    if a.cmd == "words":
        sys.exit(words(a))
    for p in (a.source or []) + (a.urls or []) + (a.suppress or []) + (getattr(a, "customers", None) or []):
        if not os.path.isfile(p):
            print(f"No such file: {p}", file=sys.stderr)
            sys.exit(2)
    if a.cmd == "build":
        if any(os.path.abspath(a.out) == os.path.abspath(p) for p in (a.source or []) + (a.urls or []) + (a.existing or [])):
            sys.exit("--out would overwrite a source file; choose a new path")
        build(a)
    else:
        sys.exit(verify(a))


if __name__ == "__main__":
    main()
