#!/usr/bin/env python3
"""List what a site can measure, from files the user supplied. Standard library only. Reads files; never fetches.

Usage:
    python3 scripts/inspect_tracking.py site/*.html                       # page HTML: tags, consent, events, forms, UTMs
    python3 scripts/inspect_tracking.py gtm/GTM-XXXX.json [site/*.html]    # a Tag Manager container export (+ cross-check)
    python3 scripts/inspect_tracking.py data/*.csv                         # analytics exports: key events, sources
    add --json for machine-readable output

The mode is picked per file by extension. Every line it prints is an observation from the files, never data a tag
collected. Lines starting with FLAG need a judgment in the report; INFO lines are context.
"""

import csv
import html as htmllib
import json
import os
import re
import sys

TAGS = [  # name, pattern that proves the tag is in the source, pattern capturing its ID (optional)
    ("Google Tag Manager", r"googletagmanager\.com/gtm\.js|GTM-[A-Z0-9]{4,}", r"(GTM-[A-Z0-9]{4,})"),
    ("GA4 (gtag.js)", r"gtag/js\?id=G-", r"gtag/js\?id=(G-[A-Z0-9]+)"),
    ("Universal Analytics (retired)", r"google-analytics\.com/analytics\.js|['\"]UA-\d+-\d+['\"]", r"(UA-\d+-\d+)"),
    ("Google Ads", r"['\"]AW-\d+|googleadservices", r"(AW-\d+)"),
    ("Meta Pixel", r"connect\.facebook\.net/[^\"']*fbevents|fbq\(", r"fbq\(\s*['\"]init['\"]\s*,\s*['\"](\d+)"),
    ("LinkedIn Insight", r"snap\.licdn\.com|_linkedin_partner_id", r"_linkedin_partner_id\s*=\s*['\"]?(\d+)"),
    ("TikTok Pixel", r"analytics\.tiktok\.com|ttq\.load", r"ttq\.load\(\s*['\"]([A-Z0-9]+)"),
    ("HubSpot", r"js\.hs-scripts\.com|hs-analytics", r"hs-scripts\.com/(\d+)"),
    ("Segment", r"cdn\.segment\.com|analytics\.load\(", None),
    ("Hotjar", r"static\.hotjar\.com|hjid", r"hjid\s*:\s*(\d+)"),
    ("Microsoft Clarity", r"clarity\.ms", None),
    ("Plausible", r"plausible\.io/js", None),
    ("PostHog", r"posthog", None),
]
CMP = r"onetrust|cookielaw\.org|cookiebot|cookieyes|osano|termly|iubenda|usercentrics|didomi|cookiebar|cookie-banner|cookie-consent|cookieconsent"
PERSONAL = re.compile(r"e-?mail|phone|tel\b|full_?name|first_?name|last_?name|\bname\b|address|postal|zip|birth", re.I)
AUTO_EVENTS = {"page_view", "session_start", "first_visit", "user_engagement", "scroll", "click", "view_search_results", "file_download"}
CONVERSION_WORDS = re.compile(r"lead|sign_?up|signup|purchase|conversion|submit|demo|trial|book|registration|contact|subscribe", re.I)
ALL_PAGES = "2147479553"
BUILT_IN = {ALL_PAGES: "All Pages", "2147479572": "Consent Initialization - All Pages", "2147479573": "Initialization - All Pages"}


def first_pos(raw, pattern):
    m = re.search(pattern, raw, re.I)
    return m.start() if m else None


def events_in(raw):
    """Event calls in the source with their parameter keys and how they're triggered."""
    found = []
    onclick_spans = [(m.start(), m.end()) for m in re.finditer(r"on(?:click|mousedown)\s*=\s*\"[^\"]*\"|on(?:click|mousedown)\s*=\s*'[^']*'", raw, re.I)]
    calls = [
        ("GA4", r"gtag\(\s*['\"]event['\"]\s*,\s*['\"]([\w-]+)['\"]\s*(?:,\s*(\{.*?\}))?\s*\)"),
        ("dataLayer", r"dataLayer\.push\(\s*(\{.*?['\"]?event['\"]?\s*:\s*['\"]([\w-]+)['\"].*?\})\s*\)"),
        ("Meta Pixel", r"fbq\(\s*['\"](?:track|trackCustom)['\"]\s*,\s*['\"](\w+)['\"]\s*(?:,\s*(\{.*?\}))?\s*\)"),
        ("LinkedIn", r"lintrk\(\s*['\"]track['\"]\s*,\s*(\{.*?\})\s*\)"),
    ]
    for platform, rx in calls:
        for m in re.finditer(rx, raw, re.I | re.S):
            if platform == "dataLayer":
                name, params = m.group(2), m.group(1)
            elif platform == "LinkedIn":
                name, params = "conversion", m.group(1)
            else:
                name, params = m.group(1), m.group(2) or ""
            if platform == "Meta Pixel" and name == "PageView":
                continue
            keys = [k for k in re.findall(r"[{,]\s*['\"]?([\w-]+)['\"]?\s*:", params) if k != "event"]
            values = re.findall(r":\s*((?:\{\{[^}]*\}\}|[^,}])+)", params)
            pos = m.start()
            window = raw[max(0, pos - 400):pos]
            if any(a <= pos < b for a, b in onclick_spans):
                when = "on click (fires before the outcome is known)"
            elif re.search(r"\.ok\b|status\s*===?\s*20\d|success", window, re.I):
                when = "after a successful response (check it runs only on success)"
            elif re.search(r"addEventListener\(\s*['\"]submit", window, re.I):
                when = "on submit attempt (before the server confirms)"
            else:
                when = "on page load (an outcome only if this page is the confirmation page; read the script)"
            pii = [k for k in keys if PERSONAL.search(k)] + [v.strip() for v in values if PERSONAL.search(v) and "team_size" not in v]
            found.append({"platform": platform, "event": name, "params": keys, "when": when, "personal_data": pii})
    return found


def inspect_html(path):
    raw = htmllib.unescape(open(path, encoding="utf-8", errors="replace").read())
    tags = []
    for name, rx, idrx in TAGS:
        pos = first_pos(raw, rx)
        if pos is None:
            continue
        ids = sorted(set(re.findall(idrx, raw))) if idrx else []
        tags.append({"tag": name, "ids": ids, "pos": pos})
    loaded = sorted(set(re.findall(r"gtag/js\?id=(G-[A-Z0-9]+)", raw)))
    configs = re.findall(r"gtag\(\s*['\"]config['\"]\s*,\s*['\"]([GA]W?-[A-Z0-9-]+)['\"]", raw)
    config_counts = {i: configs.count(i) for i in sorted(set(configs))}
    gtm = sorted(set(re.findall(r"GTM-[A-Z0-9]{4,}", raw)))
    consent_default = bool(re.search(r"gtag\(\s*['\"]consent['\"]\s*,\s*['\"]default['\"]", raw))
    cmp_pos = first_pos(raw, CMP)
    tracker_pos = [t for t in tags if t["tag"] not in ("Plausible",)]
    blocked = bool(re.search(r"<script[^>]+type=['\"]text/plain['\"]", raw, re.I))
    google = ("Google Tag Manager", "GA4 (gtag.js)", "Google Ads", "Universal Analytics (retired)")
    # Consent mode governs Google tags only; any other tag outside a blocked script loads regardless.
    before = [t["tag"] for t in tracker_pos if (cmp_pos is None or t["pos"] < cmp_pos or not blocked)
              and not (t["tag"] in google and (consent_default or blocked))]
    forms = []
    for fm in re.finditer(r"<form\b([^>]*)>(.*?)</form>", raw, re.I | re.S):
        attrs, body = fm.group(1), fm.group(2)
        names = re.findall(r"<(?:input|select|textarea)\b[^>]*?name=['\"]([\w-]+)['\"]", body, re.I)
        types = dict(re.findall(r"<input\b[^>]*?name=['\"]([\w-]+)['\"][^>]*?type=['\"](\w+)['\"]", body, re.I))
        names = [n for n in names if types.get(n, "") not in ("hidden", "submit")]
        action = re.search(r"action=['\"]([^'\"]*)['\"]", attrs)
        forms.append({"id": (re.search(r"id=['\"]([^'\"]+)['\"]", attrs) or [None, ""])[1], "action": action.group(1) if action else "",
                      "fields": names, "personal_fields": [n for n in names if PERSONAL.search(n) or types.get(n) in ("email", "tel")]})
    hrefs = re.findall(r"href=['\"]([^'\"]+)['\"]", raw)
    internal_utm = [h for h in hrefs if "utm_" in h and not h.startswith("http")]
    external = [h for h in hrefs if h.startswith("http")]
    return {
        "file": path, "tags": [{k: v for k, v in t.items() if k != "pos"} for t in tags],
        "ga4_loaded": loaded, "ga4_config_calls": config_counts, "gtm_containers": gtm,
        "ga4_loaded_not_configured": [i for i in loaded if i not in config_counts] if not gtm else [],
        "consent_mode_default": consent_default, "consent_banner_or_cmp": cmp_pos is not None,
        "tags_before_consent": before,
        "events": events_in(raw), "forms": forms, "internal_utm_links": internal_utm,
        "external_links": len(external), "external_links_with_utm": sum("utm_" in h for h in external),
        "privacy_link": bool(re.search(r"href=['\"][^'\"]*privacy", raw, re.I)),
    }


def report_html(pages):
    for p in pages:
        print(f"== {p['file']}")
        tl = "; ".join(f"{t['tag']}{' ' + ', '.join(t['ids']) if t['ids'] else ''}" for t in p["tags"]) or "none"
        print(f"   tags in source: {tl}")
        for i in p["ga4_loaded"]:
            n = p["ga4_config_calls"].get(i, 0)
            state = "configured" if n == 1 else ("configured TWICE (duplicate pageviews)" if n > 1 else
                    "LOADED BUT NOT CONFIGURED (no gtag config call" + ("; GTM present, may configure it)" if p["gtm_containers"] else ", no GTM: sends nothing)"))
            print(f"   {'FLAG' if n != 1 else 'INFO'} GA4 {i}: {state}")
        if p["gtm_containers"] and p["ga4_config_calls"]:
            print(f"   FLAG GTM {', '.join(p['gtm_containers'])} and hard-coded GA4 both load: if the container also has a Google tag for the same ID, pageviews double. Needs the container export to check.")
        if any("Universal Analytics" in t["tag"] for t in p["tags"]):
            print("   FLAG Universal Analytics tag still in the source (retired; collects nothing usable)")
        print(f"   consent: banner/CMP {'found' if p['consent_banner_or_cmp'] else 'not found'} | consent mode default {'set' if p['consent_mode_default'] else 'NOT set'}")
        if p["tags_before_consent"]:
            print(f"   FLAG loads before any consent choice: {', '.join(p['tags_before_consent'])}")
        for e in p["events"]:
            pii = f" | FLAG personal data in params: {', '.join(e['personal_data'])}" if e["personal_data"] else ""
            print(f"   event: {e['platform']} '{e['event']}' params [{', '.join(e['params']) or 'none'}] fires {e['when']}{pii}")
        if not p["events"]:
            print("   events in source: none (only pageviews, if anything)")
        for f in p["forms"]:
            print(f"   form{' #' + f['id'] if f['id'] else ''} -> {f['action'] or '(js)'}: fields {', '.join(f['fields'])} | personal: {', '.join(f['personal_fields']) or 'none'}")
        for u in p["internal_utm_links"]:
            print(f"   FLAG internal link carries UTMs (starts a new session, overwrites the real source): {u}")
        print(f"   privacy link: {'yes' if p['privacy_link'] else 'NO'} | external links: {p['external_links']} ({p['external_links_with_utm']} with UTMs, info only)")
    if len(pages) > 1:
        print("\n== across pages")
        ga = sorted({i for p in pages for i in p["ga4_loaded"]})
        for i in ga:
            ok = sum(1 for p in pages if p["ga4_config_calls"].get(i) or p["gtm_containers"])
            print(f"   GA4 {i} configured (or GTM present) on {ok}/{len(pages)} pages")
        names = sorted({t["tag"] for p in pages for t in p["tags"]})
        for n in names:
            on = [os.path.basename(p["file"]) for p in pages if any(t["tag"] == n for t in p["tags"])]
            print(f"   {n}: {len(on)}/{len(pages)} pages ({', '.join(on)})")
        if not any(p["events"] for p in pages):
            print("   FLAG no conversion or custom event appears in the source of any page")


def walk_values(obj):
    if isinstance(obj, dict):
        for v in obj.values():
            yield from walk_values(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk_values(v)
    elif isinstance(obj, str):
        yield obj


def param(tag, key):
    for p in tag.get("parameter", []):
        if p.get("key") == key:
            return p.get("value", "")
    return ""


def inspect_gtm(path, html_pages):
    data = json.load(open(path, encoding="utf-8"))
    cv = data.get("containerVersion", data)
    tags, triggers, variables = cv.get("tag", []), cv.get("trigger", []), cv.get("variable", [])
    trig_name = dict(BUILT_IN, **{t["triggerId"]: t["name"] for t in triggers})
    trig_by_id = {t["triggerId"]: t for t in triggers}
    flags, rows = [], []
    used_trig = set()
    blob = json.dumps(tags) + json.dumps(triggers) + json.dumps(variables)
    pageview_senders = {}
    for t in tags:
        fire = t.get("firingTriggerId", [])
        used_trig.update(fire + t.get("blockingTriggerId", []))
        kind = {"googtag": "Google tag", "gaawc": "GA4 config", "gaawe": "GA4 event", "html": "Custom HTML", "ua": "Universal Analytics",
                "awct": "Google Ads conversion", "sp": "Google Ads remarketing"}.get(t.get("type"), t.get("type"))
        event = param(t, "eventName")
        mid = param(t, "tagId") or param(t, "measurementId") or param(t, "measurementIdOverride")
        html_code = param(t, "html")
        if not event and "fbq(" in html_code:
            m = re.search(r"fbq\(\s*['\"]track\w*['\"]\s*,\s*['\"](\w+)", html_code)
            event = f"Meta {m.group(1)}" if m else "Meta pixel code"
        consent = (t.get("consentSettings") or {}).get("consentStatus", "missing")
        rows.append(f"   tag: {t['name']} [{kind}{' ' + event if event else ''}{' ' + mid if mid else ''}] fires on: "
                    f"{', '.join(trig_name.get(i, i) for i in fire) or 'NOTHING'}{' | PAUSED' if t.get('paused') else ''} | consent: {consent}")
        if not fire and not t.get("paused"):
            flags.append(f"FLAG tag '{t['name']}' has no firing trigger: it never fires")
        if t.get("paused"):
            flags.append(f"FLAG tag '{t['name']}' is paused")
        if t.get("type") == "ua":
            flags.append(f"FLAG tag '{t['name']}' is Universal Analytics (retired)")
        if ALL_PAGES in fire and (t.get("type") in ("googtag", "gaawc") or event == "page_view"):
            pageview_senders.setdefault(mid or "?", []).append(t["name"])
        conv = (event and (CONVERSION_WORDS.search(event)) and event not in AUTO_EVENTS) or t.get("type") == "awct"
        if conv:
            for i in fire:
                tr = trig_by_id.get(i, {})
                broad = i == ALL_PAGES or (tr.get("type") in ("CLICK", "LINK_CLICK") and not tr.get("filter") and not tr.get("autoEventFilter"))
                attempt = tr.get("type") == "FORM_SUBMISSION" and str((tr.get("checkValidation") or {}).get("value", "false")).lower() == "false"
                if broad:
                    flags.append(f"FLAG conversion-like tag '{t['name']}' ({event or kind}) fires on '{trig_name.get(i, i)}': counts any page or click, not an outcome")
                elif attempt:
                    flags.append(f"FLAG '{t['name']}' fires on '{trig_name.get(i, i)}' without validation checks: counts submit attempts, not successful submissions")
        for p in t.get("parameter", []):
            for m in p.get("list", []):
                kv = {x.get("key"): x.get("value", "") for x in m.get("map", [])}
                name, value = kv.get("parameter") or kv.get("name") or "", kv.get("parameterValue") or kv.get("value") or ""
                if PERSONAL.search(name) or PERSONAL.search(value):
                    flags.append(f"FLAG tag '{t['name']}' sends parameter '{name}' = {value}: looks like personal data")
    for mid, names in pageview_senders.items():
        if len(names) > 1:
            flags.append(f"FLAG duplicate pageviews for {mid}: {', '.join(names)} all send a page_view on All Pages")
        for p in html_pages:
            if p["ga4_config_calls"].get(mid):
                flags.append(f"FLAG {mid} is also configured in the page source ({os.path.basename(p['file'])}): the container and the hard-coded tag both send pageviews")
                break
    for tr in triggers:
        users = [t["name"] for t in tags if tr["triggerId"] in t.get("firingTriggerId", []) + t.get("blockingTriggerId", [])]
        filt = "; ".join(" ".join(x.get("value", "") for x in f.get("parameter", [])) for f in tr.get("filter", [])) or "no filter"
        rows.append(f"   trigger: {tr['name']} [{tr.get('type')}, {filt}] used by: {', '.join(users) or 'NOTHING'}")
        if not users:
            flags.append(f"FLAG trigger '{tr['name']}' is not used by any tag")
    for v in variables:
        refs = blob.count("{{" + v["name"] + "}}")
        code = " ".join(walk_values(v.get("parameter", [])))
        rows.append(f"   variable: {v['name']} [{v.get('type')}] referenced {refs} time(s)")
        if not refs:
            flags.append(f"INFO variable '{v['name']}' is not referenced")
        if PERSONAL.search(v["name"]) or re.search(r"input\[name=['\"]?(e-?mail|phone|name)", code, re.I):
            flags.append(f"FLAG variable '{v['name']}' reads personal data (a form field or identity value)")
    unset = [t["name"] for t in tags if (t.get("consentSettings") or {}).get("consentStatus", "NOT_SET") == "NOT_SET"]
    if unset and len(unset) == len(tags):
        flags.append("FLAG no tag has consent settings, and no tag waits for a consent signal")
    pub = (cv.get("container") or {}).get("publicId", os.path.basename(path))
    return {"file": path, "container": pub, "rows": rows, "flags": flags,
            "counts": {"tags": len(tags), "triggers": len(triggers), "variables": len(variables)}}


def inspect_csv(path):
    lines = [l for l in open(path, encoding="utf-8-sig") if l.strip() and not l.lstrip().startswith("#")]
    notes = [l.strip("# \n") for l in open(path, encoding="utf-8-sig") if l.lstrip().startswith("#")]
    rows = list(csv.DictReader(lines))
    if not rows:
        return {"file": path, "notes": notes, "rows": [], "flags": ["INFO no rows"], "totals": {}}
    cols = list(rows[0].keys())
    num = lambda s: float(str(s).replace(",", "")) if re.fullmatch(r"-?[\d,]+(\.\d+)?", str(s).strip()) else None
    totals = {c: sum(num(r[c]) for r in rows) for c in cols if all(num(r[c]) is not None for r in rows) and not re.search(r"user", c, re.I)}  # users overlap across rows: never summed
    flags = []
    key_col = next((c for c in cols if re.search(r"key_?event|conversion|is_key", c, re.I) and c not in totals), None)
    name_col = next((c for c in cols if re.search(r"event_?name", c, re.I)), None)
    count_col = next((c for c in cols if re.search(r"event_?count|count", c, re.I) and c in totals), None)
    if key_col and name_col:
        for r in rows:
            if str(r[key_col]).strip().lower() in ("true", "yes", "1", "y"):
                if r[name_col] in AUTO_EVENTS:
                    flags.append(f"FLAG '{r[name_col]}' is marked as a key event: it counts automatic activity, not an outcome")
                if count_col and num(r[count_col]) == 0:
                    flags.append(f"FLAG key event '{r[name_col]}' has 0 events in this export: nothing sends it, or it's misnamed")
            elif CONVERSION_WORDS.search(r[name_col]) and r[name_col] not in AUTO_EVENTS:
                flags.append(f"INFO '{r[name_col]}' looks like an outcome but isn't marked as a key event ({count_col}: {r.get(count_col, '?')})")
    src_col = next((c for c in cols if re.search(r"source|medium|channel", c, re.I)), None)
    if src_col:
        for r in rows:
            if re.search(r"\b(website|homepage|banner|internal|nav|footer|popup)\b", r[src_col], re.I):
                flags.append(f"FLAG source '{r[src_col]}' looks like an internal UTM, not a real traffic source ({', '.join(f'{c} {r[c]}' for c in totals)})")
    return {"file": path, "notes": notes, "columns": cols, "rows": rows, "totals": totals, "flags": flags}


def main():
    args = [a for a in sys.argv[1:] if a != "--json"]
    if not args:
        print(__doc__)
        return 2
    html_files = [a for a in args if a.lower().endswith((".html", ".htm"))]
    pages = [inspect_html(a) for a in html_files]
    gtm = [inspect_gtm(a, pages) for a in args if a.lower().endswith(".json")]
    exports = [inspect_csv(a) for a in args if a.lower().endswith((".csv", ".tsv"))]
    if "--json" in sys.argv:
        print(json.dumps({"pages": pages, "containers": gtm, "exports": exports}, indent=1))
        return 0
    if pages:
        report_html(pages)
    for g in gtm:
        print(f"\n== container {g['container']} ({g['counts']['tags']} tags, {g['counts']['triggers']} triggers, {g['counts']['variables']} variables)")
        print("\n".join(g["rows"]))
        print("\n".join("   " + f for f in g["flags"]) or "   no flags")
    for e in exports:
        print(f"\n== export {e['file']}")
        for n in e["notes"]:
            print(f"   note: {n}")
        for r in e["rows"]:
            print("   " + " | ".join(f"{k}: {v}" for k, v in r.items()))
        if e["totals"]:
            print("   totals: " + ", ".join(f"{k} {int(v) if v == int(v) else v}" for k, v in e["totals"].items()))
        print("\n".join("   " + f for f in e["flags"]) or "   no flags")
    print("\nThese are observations from the files. Nothing here is data a tag collected unless it came from an export.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
