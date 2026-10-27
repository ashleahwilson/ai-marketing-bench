#!/usr/bin/env python3
"""Measure the search and discovery facts in saved pages. Standard library only. Reads files; never fetches.

Usage:
    python3 scripts/check_pages.py site/*.html
    python3 scripts/check_pages.py site/*.html --robots robots.txt --sitemap sitemap.xml \
        --domain example.com --key /,/pricing,/contact --date 2026-10-24
    python3 scripts/check_pages.py site/*.html --json        # machine-readable, for the checks file

Page paths come from file names: index.html -> /, pricing.html -> /pricing, blog/post.html -> /blog/post.
--key   paths that matter most (default: /, plus any page whose path holds pricing, contact, demo, book or signup).
--date  the audit date, used to age the newest dated content (default: today).

Per page: title and meta description (with lengths and duplicates), H1 count, H2s and skipped heading levels,
canonical (self, missing, or pointing elsewhere), robots meta (noindex, nofollow), whether robots.txt blocks the
path, whether the sitemap lists it, structured data types (with any rating claims), FAQ signals, internal links in
and out, navigation, social, review, partner and ad-tag channel signals, newsletter signup, phone numbers,
postcodes, opening hours, map embeds, dates found, images missing alt text, and word count.
The summary lists BLOCKER (a key page that can't be indexed), ISSUE and NOTE lines. It can't judge whether a
sentence is clear or whether content answers a buyer's question: that needs reading.
"""

import datetime as dt
import json
import os
import re
import sys
from html.parser import HTMLParser
from urllib.parse import urlparse

MONTHS = "january february march april may june july august september october november december".split()
SOCIAL = {"linkedin.com": "LinkedIn", "instagram.com": "Instagram", "facebook.com": "Facebook", "x.com": "X",
          "twitter.com": "X", "youtube.com": "YouTube", "tiktok.com": "TikTok", "pinterest.": "Pinterest",
          "threads.net": "Threads", "bsky.app": "Bluesky"}
REVIEWS = {"g2.com": "G2", "capterra.": "Capterra", "trustpilot.": "Trustpilot", "yelp.": "Yelp",
           "tripadvisor.": "Tripadvisor", "google.com/maps": "Google Maps", "g.page": "Google Business Profile",
           "maps.app.goo.gl": "Google Maps", "goo.gl/maps": "Google Maps", "opentable.": "OpenTable",
           "clutch.co": "Clutch"}
PARTNERS = {"appexchange.salesforce.com": "Salesforce AppExchange", "ecosystem.hubspot.com": "HubSpot marketplace",
            "apps.shopify.com": "Shopify App Store", "marketplace.": "marketplace listing",
            "apps.apple.com": "App Store", "play.google.com": "Google Play", "ubereats.": "Uber Eats",
            "doordash.": "DoorDash", "skipthedishes.": "SkipTheDishes"}
AD_TAGS = [("Google Ads", r"['\"]AW-\d+['\"]|googleadservices"), ("Meta Pixel", r"fbevents|fbq\("),
           ("LinkedIn Insight", r"snap\.licdn\.com|_linkedin_partner_id"), ("TikTok Pixel", r"analytics\.tiktok\.com")]
PHONE = re.compile(r"(?:\+?1[\s.-]?)?\(?\b(\d{3})\)?[\s.-]?(\d{3})[\s.-](\d{4})\b")
POSTCODE = re.compile(r"\b([A-Z]\d[A-Z])\s?(\d[A-Z]\d)\b|\b[A-Z]{2}\s\d{5}(?:-\d{4})?\b")
HOURS = re.compile(r"\b(?:mon|tues?|wed|thu|thurs?|fri|sat|sun)(?:day|nesday|urday|sday)?\b[^<\n]{0,40}?\d{1,2}(?::\d{2})?\s?(?:am|pm|h)\b", re.I)


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title = ""
        self.meta_desc = None
        self.robots = ""
        self.canonical = None
        self.hreflang = []
        self.headings = []
        self.links = []          # (href, text)
        self.nav = False
        self.jsonld = []
        self.microdata = []
        self.forms = []
        self.img_total = 0
        self.img_no_alt = 0
        self.details = 0
        self.iframes = []
        self.time_tags = []
        self.text = []
        self._stack = []
        self._buf = []
        self._script = None
        self._form = None
        self._skip = 0
        self.lang = ""

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "html":
            self.lang = a.get("lang", "")
        if tag == "meta":
            name = a.get("name", "").lower()
            if name == "description":
                self.meta_desc = a.get("content", "")
            if name in ("robots", "googlebot"):
                self.robots = (self.robots + "," + a.get("content", "")).strip(",")
        elif tag == "link":
            rel = a.get("rel", "").lower()
            if rel == "canonical":
                self.canonical = a.get("href", "")
            if rel == "alternate" and a.get("hreflang"):
                self.hreflang.append(a["hreflang"])
        elif tag == "nav":
            self.nav = True
        elif tag == "img":
            self.img_total += 1
            if not a.get("alt", "").strip():
                self.img_no_alt += 1
        elif tag == "iframe":
            self.iframes.append(a.get("src", ""))
        elif tag == "time" and a.get("datetime"):
            self.time_tags.append(a["datetime"])
        elif tag == "details":
            self.details += 1
        elif tag == "form":
            self._form = {"fields": [], "email": False}
        elif tag in ("input", "select", "textarea") and self._form is not None:
            if a.get("type", "").lower() not in ("hidden", "submit", "button"):
                self._form["fields"].append(a.get("name") or a.get("placeholder") or tag)
                if a.get("type", "").lower() == "email" or "email" in a.get("name", "").lower():
                    self._form["email"] = True
        elif tag == "script":
            self._script = a.get("type", "")
        if a.get("itemtype"):
            self.microdata.append(a["itemtype"].rstrip("/").split("/")[-1])
        if tag in ("style",):
            self._skip += 1
        if tag in ("title", "h1", "h2", "h3", "h4", "h5", "h6", "a"):
            self._stack.append((tag, a))
            self._buf = []

    def handle_endtag(self, tag):
        if tag == "form" and self._form is not None:
            self.forms.append(self._form)
            self._form = None
        if tag == "script":
            self._script = None
        if tag == "style":
            self._skip = max(0, self._skip - 1)
        if self._stack and self._stack[-1][0] == tag:
            t, a = self._stack.pop()
            txt = " ".join("".join(self._buf).split())
            if t == "title":
                self.title = txt
            elif t == "a":
                self.links.append((a.get("href", ""), txt))
            else:
                self.headings.append((int(t[1]), txt))

    def handle_data(self, data):
        if self._script is not None:
            if "ld+json" in self._script.lower():
                self.jsonld.append(data)
            return
        if self._skip:
            return
        self._buf.append(data)
        self.text.append(data)


def page_path(filename, root):
    rel = os.path.relpath(filename, root).replace(os.sep, "/")
    rel = re.sub(r"\.html?$", "", rel)
    if rel == "index":
        return "/"
    if rel.endswith("/index"):
        rel = rel[:-6]
    return "/" + rel


def norm_href(href, domain):
    """Return an internal path for an internal link, or None."""
    if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
        return None
    u = urlparse(href)
    if u.scheme in ("http", "https"):
        host = u.netloc.lower().removeprefix("www.")
        if not domain or host != domain:
            return None
        path = u.path or "/"
    elif u.scheme:
        return None
    else:
        path = u.path or "/"
        if not path.startswith("/"):
            path = "/" + path
    path = re.sub(r"\.html?$", "", path)
    path = re.sub(r"/index$", "/", path)
    return path.rstrip("/") or "/"


def jsonld_types(blocks):
    types, ratings, faq_q, errors = [], [], 0, 0

    def walk(node):
        nonlocal faq_q
        if isinstance(node, dict):
            t = node.get("@type")
            for x in (t if isinstance(t, list) else [t] if t else []):
                types.append(str(x))
                if x == "Question":
                    faq_q += 1
            r = node.get("aggregateRating")
            if isinstance(r, dict):
                ratings.append(f"ratingValue {r.get('ratingValue')} from {r.get('reviewCount') or r.get('ratingCount')} reviews")
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    for b in blocks:
        try:
            walk(json.loads(b))
        except ValueError:
            errors += 1
    return types, ratings, faq_q, errors


def robots_rules(path):
    """Parse robots.txt groups that apply to * or Googlebot. Returns (rules, sitemaps)."""
    rules, sitemaps, agents, applies, in_rules = [], [], [], False, False
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.split("#")[0].strip()
        if ":" not in line:
            continue
        k, v = [s.strip() for s in line.split(":", 1)]
        k = k.lower()
        if k == "sitemap":
            sitemaps.append(v)
        elif k == "user-agent":
            if in_rules:
                agents, in_rules = [], False
            agents.append(v.lower())
            applies = any(x in ("*", "googlebot") for x in agents)
        elif k in ("allow", "disallow"):
            in_rules = True
            if applies and v:
                rules.append((k, v))
    return rules, sitemaps


def blocked(path, rules):
    best = None
    for kind, pat in rules:
        rx = "^" + re.escape(pat).replace(r"\*", ".*").replace(r"\$", "$")
        if re.match(rx, path) or re.match(rx, path + "/"):
            if best is None or len(pat) > len(best[1]) or (len(pat) == len(best[1]) and kind == "allow"):
                best = (kind, pat)
    return best[1] if best and best[0] == "disallow" else None


def sitemap_paths(path, domain):
    raw = open(path, encoding="utf-8", errors="replace").read()
    out = []
    for loc in re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", raw):
        u = urlparse(loc)
        host = u.netloc.lower().removeprefix("www.")
        out.append((loc, host, re.sub(r"\.html?$", "", u.path).rstrip("/") or "/"))
    return out


def dates_in(text, time_tags):
    found = []
    for m in re.finditer(r"\b(" + "|".join(MONTHS) + r")\s+(?:(\d{1,2}),?\s+)?(20\d\d)\b", text, re.I):
        found.append(dt.date(int(m.group(3)), MONTHS.index(m.group(1).lower()) + 1, int(m.group(2) or 1)))
    for m in re.finditer(r"\b(20\d\d)-(\d\d)-(\d\d)\b", text + " " + " ".join(time_tags)):
        try:
            found.append(dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3))))
        except ValueError:
            pass
    return found


def inspect(f, root, domain):
    raw = open(f, encoding="utf-8", errors="replace").read()
    p = Page()
    p.feed(raw)
    text = " ".join(" ".join(p.text).split())
    path = page_path(f, root)
    types, ratings, faq_q, ld_err = jsonld_types(p.jsonld)
    canon = p.canonical
    canon_state = "missing"
    if canon is not None:
        u = urlparse(canon)
        host = u.netloc.lower().removeprefix("www.")
        cpath = re.sub(r"\.html?$", "", u.path).rstrip("/") or "/"
        if u.netloc and host != (domain or host):
            canon_state = f"points to another domain: {canon}"
        elif cpath != path:
            canon_state = f"points to another page: {canon}"
        else:
            canon_state = "self"
    levels = [h for h, _ in p.headings]
    skips = [f"H{a} -> H{b}" for a, b in zip(levels, levels[1:]) if b > a + 1]
    if levels and levels[0] != 1 and 1 in levels:
        skips.insert(0, f"starts at H{levels[0]}")
    internal = sorted({x for x in (norm_href(h, domain) for h, _ in p.links) if x and x != path})
    ext = [h for h, _ in p.links if h.startswith("http") and norm_href(h, domain) is None]
    srcs = ext

    def kinds(table):
        return sorted({name for h in srcs for k, name in table.items() if k in h.lower()})

    phones = sorted({"({}) {}-{}".format(*m.groups()) for m in PHONE.finditer(text)} |
                    {"({}) {}-{}".format(*m.groups()) for h, _ in p.links if h.startswith("tel:")
                     for m in [PHONE.search(h)] if m})
    dates = dates_in(text, p.time_tags)
    return {
        "file": f, "path": path, "lang": p.lang,
        "title": p.title, "title_chars": len(p.title),
        "meta_description": p.meta_desc, "meta_chars": len(p.meta_desc or ""),
        "robots_meta": p.robots, "noindex": "noindex" in p.robots.lower() or "none" == p.robots.lower().strip(),
        "nofollow": "nofollow" in p.robots.lower(),
        "canonical": canon_state, "hreflang": p.hreflang,
        "h1": [t for h, t in p.headings if h == 1], "h2_count": levels.count(2), "heading_skips": skips,
        "question_headings": [t for h, t in p.headings if t.endswith("?")], "details_blocks": p.details,
        "structured_data": types + [f"{m} (microdata)" for m in p.microdata], "rating_claims": ratings,
        "faq_schema_questions": faq_q, "jsonld_parse_errors": ld_err,
        "nav": p.nav, "links_out_internal": internal,
        "social": kinds(SOCIAL), "reviews": kinds(REVIEWS), "partners": kinds(PARTNERS),
        "ad_tags": [n for n, rx in AD_TAGS if re.search(rx, raw, re.I)],
        "newsletter": any(fm["email"] and len(fm["fields"]) <= 2 for fm in p.forms)
        or bool(re.search(r"newsletter|subscribe", text, re.I)),
        "phones": phones, "postcodes": sorted({m.group(0) for m in POSTCODE.finditer(text)}),
        "hours_found": bool(HOURS.search(text)), "map_embed": any("map" in s.lower() for s in p.iframes),
        "first_paragraph": (re.search(r"<p[^>]*>(.*?)</p>", raw, re.S | re.I) or [None, ""])[1],
        "newest_date": max(dates).isoformat() if dates else None,
        "images": p.img_total, "images_missing_alt": p.img_no_alt,
        "words": len(re.findall(r"[A-Za-z0-9']+", text)),
    }


def main():
    args = sys.argv[1:]
    opts = {}
    for flag in ("--robots", "--sitemap", "--domain", "--key", "--date", "--root"):
        if flag in args:
            i = args.index(flag)
            opts[flag] = args[i + 1]
            del args[i:i + 2]
    as_json = "--json" in args
    files = [a for a in args if a != "--json" and os.path.isfile(a)]
    if not files:
        print(__doc__)
        return 2
    root = opts.get("--root") or os.path.commonpath([os.path.dirname(os.path.abspath(f)) for f in files])
    domain = re.sub(r"^https?://", "", (opts.get("--domain") or "").lower()).split("/")[0].removeprefix("www.")
    if not domain:  # the host most canonical and og:url tags agree on
        hosts = []
        for f in files:
            raw = open(f, encoding="utf-8", errors="replace").read()
            hosts += [h.lower().removeprefix("www.") for h in re.findall(
                r"<(?:link[^>]+rel=[\"']canonical[\"'][^>]+href|meta[^>]+property=[\"']og:url[\"'][^>]+content)=[\"']https?://([^/\"']+)", raw, re.I)]
        if hosts:
            domain = max(set(hosts), key=hosts.count)
    pages = [inspect(os.path.abspath(f), root, domain) for f in files]
    today = dt.date.fromisoformat(opts["--date"]) if "--date" in opts else dt.date.today()
    paths = {pg["path"] for pg in pages}
    key = [k.rstrip("/") or "/" for k in opts["--key"].split(",")] if "--key" in opts else \
        sorted(p for p in paths if p == "/" or re.search(r"pricing|plans|contact|demo|book|signup|trial|locations?", p))
    rules, robot_sitemaps = robots_rules(opts["--robots"]) if "--robots" in opts else ([], [])
    smap = sitemap_paths(opts["--sitemap"], domain) if "--sitemap" in opts else None
    inbound = {p: 0 for p in paths}
    for pg in pages:
        for t in pg["links_out_internal"]:
            if t in inbound:
                inbound[t] += 1
    titles, metas = {}, {}
    for pg in pages:
        pg["links_in_from_reviewed_pages"] = inbound[pg["path"]]
        pg["robots_txt_blocks"] = blocked(pg["path"], rules) if "--robots" in opts else "not supplied"
        pg["in_sitemap"] = (pg["path"] in {x[2] for x in smap}) if smap is not None else "not supplied"
        pg["key_page"] = pg["path"] in key
        if pg["title"]:
            titles.setdefault(pg["title"].lower(), []).append(pg["path"])
        if pg["meta_description"]:
            metas.setdefault(pg["meta_description"].lower(), []).append(pg["path"])

    findings = []
    add = lambda lvl, msg: findings.append((lvl, msg))
    for pg in pages:
        where = pg["path"]
        k = " (key page)" if pg["key_page"] else ""
        lvl = "BLOCKER" if pg["key_page"] else "ISSUE"
        if pg["noindex"]:
            add(lvl, f"{where}{k}: robots meta '{pg['robots_meta']}' keeps it out of search results")
        if pg["robots_txt_blocks"] not in (None, "not supplied"):
            add(lvl, f"{where}{k}: robots.txt 'Disallow: {pg['robots_txt_blocks']}' blocks crawling"
                + (" (and hides its noindex tag from crawlers)" if pg["noindex"] else ""))
        if pg["canonical"].startswith("points"):
            add(lvl, f"{where}{k}: canonical {pg['canonical']}, so search engines are told to index that URL instead")
        if not pg["title"]:
            add("ISSUE", f"{where}: no title")
        elif pg["title_chars"] > 60:
            add("NOTE", f"{where}: title is {pg['title_chars']} characters (over 60 may be cut off)")
        if pg["meta_description"] is None or not pg["meta_description"].strip():
            add("ISSUE", f"{where}: no meta description")
        elif pg["meta_chars"] > 160:
            add("NOTE", f"{where}: meta description is {pg['meta_chars']} characters (over 160 may be cut off)")
        if len(pg["h1"]) != 1:
            add("ISSUE", f"{where}: {len(pg['h1'])} H1 headings")
        if pg["heading_skips"]:
            add("NOTE", f"{where}: heading levels skip ({', '.join(pg['heading_skips'])})")
        if pg["canonical"] == "missing":
            add("NOTE", f"{where}: no canonical tag")
        if not pg["structured_data"]:
            add("NOTE", f"{where}: no structured data")
        if pg["rating_claims"]:
            add("ISSUE", f"{where}: structured data claims a rating ({'; '.join(pg['rating_claims'])}): check reviews are visible on the page")
        if pg["jsonld_parse_errors"]:
            add("ISSUE", f"{where}: {pg['jsonld_parse_errors']} structured data block(s) don't parse as JSON")
        if not pg["nav"]:
            add("ISSUE", f"{where}: no navigation element")
        if len(pages) > 1 and pg["links_in_from_reviewed_pages"] == 0 and pg["path"] != "/":
            add("ISSUE", f"{where}: no links to it from any other reviewed page")
        if pg["images_missing_alt"]:
            add("NOTE", f"{where}: {pg['images_missing_alt']} of {pg['images']} images have no alt text")
        if smap is not None and pg["in_sitemap"] is False and not pg["noindex"]:
            add("NOTE", f"{where}: not listed in the sitemap")
    for t, ps in titles.items():
        if len(ps) > 1:
            add("ISSUE", f"duplicate title on {', '.join(ps)}")
    for t, ps in metas.items():
        if len(ps) > 1:
            add("ISSUE", f"duplicate meta description on {', '.join(ps)}")
    for kp in key:
        if kp not in paths:
            add("NOTE", f"key page {kp} wasn't among the pages supplied")
    if smap is not None:
        byp = {pg["path"]: pg for pg in pages}
        for loc, host, sp in smap:
            pg = byp.get(sp)
            if domain and host and host != domain:
                add("ISSUE", f"sitemap lists a URL on another domain: {loc}")
            if pg and (pg["noindex"] or pg["canonical"].startswith("points")):
                add("ISSUE", f"sitemap lists {sp}, which is noindexed or canonicalised elsewhere (conflicting signals)")
            if blocked(sp, rules):
                add("ISSUE", f"sitemap lists {sp}, which robots.txt blocks (conflicting signals)")
    if "--robots" in opts and not robot_sitemaps:
        add("NOTE", "robots.txt doesn't reference a sitemap")
    phones = {}
    for pg in pages:
        for ph in pg["phones"]:
            phones.setdefault(ph, []).append(pg["path"])
    if len(phones) > 1:
        add("NOTE", "several phone numbers appear: " + "; ".join(f"{ph} on {', '.join(ps)}" for ph, ps in phones.items())
            + " (check each location's number matches everywhere it appears)")
    dated = [(pg["newest_date"], pg["path"]) for pg in pages if pg["newest_date"]]
    newest = max(dated) if dated else None
    if newest:
        age = (today - dt.date.fromisoformat(newest[0])).days
        add("NOTE", f"newest date found: {newest[0]} on {newest[1]} ({age} days before {today.isoformat()})")
    else:
        add("NOTE", "no dated content found in the pages supplied")
    ch = {
        "social profiles": sorted({s for pg in pages for s in pg["social"]}),
        "third-party reviews": sorted({s for pg in pages for s in pg["reviews"]}),
        "partner or marketplace listings": sorted({s for pg in pages for s in pg["partners"]}),
        "ad tags": sorted({s for pg in pages for s in pg["ad_tags"]}),
    }
    summary = {"domain": domain or "unknown", "date": today.isoformat(), "key_pages": key,
               "robots_txt": "supplied" if "--robots" in opts else "not supplied",
               "robots_txt_sitemaps": robot_sitemaps,
               "sitemap": f"{len(smap)} URLs" if smap is not None else "not supplied",
               "channel_kinds_seen": {k: v for k, v in ch.items() if v},
               "newsletter_signup_on": [pg["path"] for pg in pages if pg["newsletter"]],
               "newest_dated_content": newest, "findings": findings}
    if as_json:
        print(json.dumps({"summary": summary, "pages": pages}, indent=1, default=str))
        return 0
    print(f"Domain: {summary['domain']} · audit date {summary['date']} · key pages: {', '.join(key) or 'none'}")
    print(f"robots.txt: {summary['robots_txt']} · sitemap: {summary['sitemap']}\n")
    print("| Page | Title (chars) | Meta desc | H1s | Canonical | Robots meta | robots.txt | Sitemap | Links in |")
    print("|---|---|---|---|---|---|---|---|---|")
    for pg in pages:
        rt = pg["robots_txt_blocks"]
        print(f"| {pg['path']}{' *' if pg['key_page'] else ''} | {(pg['title'] or '(none)').replace('|', chr(92) + '|')} ({pg['title_chars']}) | "
              f"{'yes (' + str(pg['meta_chars']) + ')' if pg['meta_description'] else 'MISSING'} | {len(pg['h1'])} | "
              f"{pg['canonical']} | {pg['robots_meta'] or '-'} | {'blocked: ' + rt if rt not in (None, 'not supplied') else ('-' if rt is None else rt)} | "
              f"{pg['in_sitemap']} | {pg['links_in_from_reviewed_pages']} |")
    print("\n* key page\n")
    for pg in pages:
        print(f"== {pg['path']}: H1 {pg['h1'] or 'none'} · H2s {pg['h2_count']} · schema {', '.join(pg['structured_data']) or 'none'}"
              f" · nav {'yes' if pg['nav'] else 'NO'} · words {pg['words']} · alt missing {pg['images_missing_alt']}/{pg['images']}")
        extra = []
        if pg["question_headings"] or pg["faq_schema_questions"] or pg["details_blocks"]:
            extra.append(f"FAQ signals: {len(pg['question_headings'])} question headings, {pg['faq_schema_questions']} FAQ schema questions, {pg['details_blocks']} expandable blocks")
        if pg["phones"] or pg["postcodes"]:
            extra.append(f"phones {', '.join(pg['phones']) or 'none'} · postcodes {', '.join(pg['postcodes']) or 'none'} · hours {'yes' if pg['hours_found'] else 'not found'} · map {'yes' if pg['map_embed'] else 'no'}")
        chans = pg["social"] + pg["reviews"] + pg["partners"] + pg["ad_tags"]
        if chans:
            extra.append("channels: " + ", ".join(chans))
        if pg["newest_date"]:
            extra.append(f"newest date {pg['newest_date']}")
        for e in extra:
            print(f"   {e}")
    print("\nChannel kinds seen: " + ("; ".join(f"{k}: {', '.join(v)}" for k, v in summary["channel_kinds_seen"].items()) or "none"))
    print(f"Newsletter signup on: {', '.join(summary['newsletter_signup_on']) or 'none found'}\n")
    order = {"BLOCKER": 0, "ISSUE": 1, "NOTE": 2}
    for lvl, msg in sorted(findings, key=lambda x: order[x[0]]):
        print(f"{lvl}: {msg}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
