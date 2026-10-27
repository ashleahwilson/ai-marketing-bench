#!/usr/bin/env python3
"""Extract the observable marketing facts from saved HTML pages. Standard library only. Reads files; never fetches.

Usage:
    python3 scripts/inspect_page.py page.html [more.html ...]          # human-readable summary
    python3 scripts/inspect_page.py site/*.html --json > briefing.json  # for the shared briefing

Per page it reports: title, meta description, canonical, Open Graph tags, H1-H3, calls to action (links and buttons
that read as actions), forms (field count, required fields, field names), structured data types, tracking tags
detected in the source, images missing alt text, internal/external links, and word count.

To get HTML: save pages from a browser, or fetch them with your web tool and write the raw HTML to a file.
Tracking tags are only visible in raw HTML source, not in rendered or markdown text.
"""

import json
import re
import sys
from html.parser import HTMLParser

TRACKERS = [
    ("Google Analytics 4", r"gtag/js\?id=G-|['\"]G-[A-Z0-9]{6,}['\"]"),
    ("Google Tag Manager", r"googletagmanager\.com/gtm\.js|GTM-[A-Z0-9]{4,}"),
    ("Universal Analytics (retired)", r"google-analytics\.com/analytics\.js|['\"]UA-\d+-\d+['\"]"),
    ("Google Ads", r"['\"]AW-\d+['\"]|googleadservices"),
    ("Meta Pixel", r"connect\.facebook\.net/[^\"']*fbevents|fbq\("),
    ("LinkedIn Insight", r"snap\.licdn\.com|_linkedin_partner_id"),
    ("TikTok Pixel", r"analytics\.tiktok\.com|ttq\.load"),
    ("HubSpot", r"js\.hs-scripts\.com|hs-analytics"),
    ("Segment", r"cdn\.segment\.com|analytics\.load\("),
    ("Hotjar", r"static\.hotjar\.com|hjid"),
    ("Microsoft Clarity", r"clarity\.ms"),
    ("Plausible", r"plausible\.io/js"),
    ("PostHog", r"posthog"),
    ("Intercom", r"widget\.intercom\.io|Intercom\("),
]
CONVERSION_EVENT = re.compile(r"gtag\(\s*['\"]event['\"]|fbq\(\s*['\"]track['\"]|dataLayer\.push\(\s*\{[^}]*['\"]event['\"]|lintrk\(", re.I)
ACTION_WORDS = re.compile(r"\b(book|start|get|try|request|contact|buy|sign ?up|subscribe|download|demo|talk|schedule|join|apply|call|quote|review)\b", re.I)


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title, self.meta, self.og, self.canonical = "", {}, {}, ""
        self.headings, self.ctas, self.forms, self.jsonld_types = [], [], [], []
        self.img_total, self.img_no_alt, self.links = 0, 0, []
        self.text, self._stack, self._buf, self._form, self._in_script, self._script_type = [], [], [], None, False, ""

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "meta":
            if a.get("name", "").lower() == "description":
                self.meta["description"] = a.get("content", "")
            if a.get("property", "").startswith("og:"):
                self.og[a["property"]] = a.get("content", "")
        elif tag == "link" and a.get("rel", "").lower() == "canonical":
            self.canonical = a.get("href", "")
        elif tag == "img":
            self.img_total += 1
            if not (a.get("alt") or "").strip():
                self.img_no_alt += 1
        elif tag == "form":
            self._form = {"action": a.get("action", ""), "fields": [], "required": []}
        elif tag in ("input", "select", "textarea") and self._form is not None:
            if a.get("type", "").lower() not in ("hidden", "submit", "button"):
                name = a.get("name") or a.get("placeholder") or tag
                self._form["fields"].append(name)
                if "required" in a:
                    self._form["required"].append(name)
        elif tag == "script":
            self._in_script, self._script_type = True, a.get("type", "")
        if tag in ("title", "h1", "h2", "h3", "a", "button"):
            self._stack.append((tag, a))
            self._buf = []

    def handle_endtag(self, tag):
        if tag == "form" and self._form is not None:
            self.forms.append(self._form)
            self._form = None
        if tag == "script":
            self._in_script = False
        if self._stack and self._stack[-1][0] == tag:
            t, a = self._stack.pop()
            txt = " ".join("".join(self._buf).split())
            if t == "title":
                self.title = txt
            elif t in ("h1", "h2", "h3"):
                self.headings.append((t, txt))
            elif t == "a":
                self.links.append(a.get("href", ""))
                if txt and (ACTION_WORDS.search(txt) or "btn" in a.get("class", "")):
                    self.ctas.append(f"{txt} -> {a.get('href', '')}")
            elif t == "button" and txt:
                self.ctas.append(f"{txt} [button]")

    def handle_data(self, data):
        if self._in_script:
            if "ld+json" in self._script_type:
                self.jsonld_types += re.findall(r'"@type"\s*:\s*"([^"]+)"', data)
            return
        self._buf.append(data)
        self.text.append(data)


def inspect(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    is_html = bool(re.search(r"<html|<!doctype html|<head|<body", raw, re.I))
    p = Page()
    p.feed(raw)
    words = len(re.findall(r"[A-Za-z0-9']+", " ".join(p.text)))
    trackers = [name for name, rx in TRACKERS if re.search(rx, raw, re.I)]
    return {
        "file": path, "is_html": is_html,
        "viewport_meta": bool(re.search(r'<meta[^>]+name=["\']viewport', raw, re.I)),
        "privacy_link_or_notice": bool(re.search(r"privacy", raw, re.I)),
        "title": p.title, "meta_description": p.meta.get("description", ""), "canonical": p.canonical,
        "open_graph": p.og, "headings": p.headings, "ctas": p.ctas,
        "forms": [{"fields": len(f["fields"]), "required": len(f["required"]), "names": f["fields"]} for f in p.forms],
        "structured_data": p.jsonld_types, "tracking": trackers,
        "conversion_events_in_source": bool(CONVERSION_EVENT.search(raw)),
        "ga4_configured": bool(re.search(r"gtag\(\s*['\"]config['\"]", raw)) or bool(re.search(r"GTM-[A-Z0-9]{4,}", raw)),
        "nav_present": bool(re.search(r"<nav[\s>]", raw, re.I)),
        "images": p.img_total, "images_missing_alt": p.img_no_alt,
        "links_internal": sum(1 for l in p.links if l.startswith("/") or l.startswith("#")),
        "links_external": sum(1 for l in p.links if l.startswith("http")),
        "mailto_only_contact": bool(p.links) and all(l.startswith("mailto:") for l in p.links if ACTION_WORDS.search(l) or l.startswith("mailto:")) and not p.forms,
        "words": words,
    }


def main():
    args = [a for a in sys.argv[1:] if a != "--json"]
    if not args:
        print(__doc__)
        return 2
    pages = [inspect(a) for a in args]
    if "--json" in sys.argv:
        print(json.dumps(pages, indent=1))
        return 0
    for r in pages:
        print(f"== {r['file']}")
        if not r["is_html"]:
            print("   NOT HTML: tracking, metadata and viewport can't be assessed from this file. Use raw HTML source.")
            continue
        print(f"   title: {r['title'] or '(none)'} | meta description: {'yes' if r['meta_description'] else 'MISSING'} | canonical: {r['canonical'] or 'none'} | words: {r['words']}")
        for t, h in r["headings"][:8]:
            print(f"   {t}: {h}")
        print(f"   CTAs: {'; '.join(r['ctas']) or 'none'}")
        for f in r["forms"]:
            print(f"   form: {f['fields']} fields ({f['required']} required): {', '.join(f['names'])}")
        ga = ""
        if "Google Analytics 4" in r["tracking"]:
            ga = " (GA4 configured)" if r["ga4_configured"] else " (GA4 library loaded but NOT configured on this page)"
        print(f"   tracking: {', '.join(r['tracking']) or 'none detected'}{ga} | conversion events in source: {'yes' if r['conversion_events_in_source'] else 'no'} | nav: {'yes' if r['nav_present'] else 'NONE'}")
        print(f"   structured data: {', '.join(r['structured_data']) or 'none'} | images missing alt: {r['images_missing_alt']}/{r['images']}")
        print(f"   mobile viewport tag: {'yes' if r['viewport_meta'] else 'MISSING'} | privacy link/notice: {'yes' if r['privacy_link_or_notice'] else 'none'}{' (form on page)' if r['forms'] else ''}")
    labels = sorted({c.split(" -> ")[0].split(" [")[0] for r in pages if r.get("is_html") for c in r["ctas"]})
    if len(pages) > 1 and labels:
        print(f"\n== across pages: {len(labels)} distinct CTA labels: {' | '.join(labels)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
