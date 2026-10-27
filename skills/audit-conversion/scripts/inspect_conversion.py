#!/usr/bin/env python3
"""Extract the conversion facts visible in saved pages. Standard library only. Reads files; never fetches.

Usage:
    python3 scripts/inspect_conversion.py site/*.html            # readable summary, one block per page
    python3 scripts/inspect_conversion.py site/*.html --json     # the same facts as JSON

Per page: viewport (and whether it blocks zoom), calls to action (hero, nav, body; how many are styled as primary),
forms field by field (label, type, required, autocomplete, sensitive), submit text, error-handling markup,
privacy notice and next-step text near the form, proof on the page and near the form, prices and currency codes,
render-blocking scripts and stylesheets in the head, images without width/height or alt, small tap targets set in
inline styles, and icon-only links. Across pages: CTA labels and destinations, and "no credit card" claims set
against forms that ask for a card.

Markdown or plain text input is reported as NOT HTML: viewport, scripts, image sizes and form markup can't be
checked from it. Copy-level facts (CTA text, prices, quotes, field labels with *) are still listed.
"""

import json
import re
import sys
from html.parser import HTMLParser

ACTION = re.compile(r"\b(book|start|get|try|request|contact|buy|sign ?up|subscribe|download|demo|talk|schedule|join|"
                    r"apply|call|quote|review|watch|register|submit|send|claim|see|create)\b", re.I)
SENSITIVE = re.compile(r"phone|tel\b|mobile|revenue|budget|income|salary|turnover|card|cvc|cvv|expir|ssn|\bsin\b|"
                       r"birth|dob|social.?security", re.I)
EMAILISH = re.compile(r"e-?mail", re.I)
PHONEISH = re.compile(r"phone|tel\b|mobile", re.I)
CARD = re.compile(r"card|cvc|cvv|expir", re.I)
NEXT_STEP = re.compile(r"we'll (email|call|reply|be in touch|send|get back)|we will (email|call|reply|send)|within (one|1|\d+|a) "
                       r"(business )?(day|hour)|you'll (get|receive|hear)|what happens next|next step", re.I)
PRIVACY = re.compile(r"privacy|never share|won't share|no spam", re.I)
PRICE = re.compile(r"(?:[$€£]\s?\d[\d,]*(?:\.\d+)?(?:\s?(?:USD|CAD|AUD|NZD|EUR|GBP))?(?:\s?/\s?\w+(?:/\w+)?)?)")
CURRENCY_CODE = re.compile(r"\b(USD|CAD|AUD|NZD|EUR|GBP|US dollars|Canadian dollars)\b", re.I)
QUOTED = re.compile(r"\b(quoted|contact (us|sales) for pricing|custom pricing|request a quote)\b", re.I)
NO_CARD = re.compile(r"no credit card|no card required|without a credit card", re.I)
WINDOW = 700  # characters of raw HTML before and after a form that count as "near the form"


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.title, self.viewport = "", None
        self.in_head, self.in_nav, self.seen_h2 = False, 0, False
        self.head_scripts_blocking, self.head_stylesheets = [], 0
        self.ctas, self.forms, self.labels_for, self.ids = [], [], set(), {}
        self.images = []
        self.small_targets, self.icon_links = [], 0
        self.quotes, self.text = [], []
        self._stack, self._buf, self._form, self._label_depth, self._in_script = [], [], None, 0, False
        self._bq, self._bqbuf = False, []

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        if tag == "head":
            self.in_head = True
        if tag == "body":
            self.in_head = False
        if tag == "nav":
            self.in_nav += 1
        if tag == "h2":
            self.seen_h2 = True
        if tag == "meta" and a.get("name", "").lower() == "viewport":
            self.viewport = a.get("content", "")
        if tag == "link" and "stylesheet" in a.get("rel", "").lower() and self.in_head:
            self.head_stylesheets += 1
        if tag == "script":
            self._in_script = True
            src = a.get("src", "")
            if self.in_head and src and "async" not in a and "defer" not in a and a.get("type", "") != "module":
                self.head_scripts_blocking.append(src)
        if tag == "img":
            self.images.append({"src": a.get("src", ""), "alt": "alt" in a and bool(a.get("alt", "").strip()),
                                "sized": bool(a.get("width")) and bool(a.get("height")), "lazy": a.get("loading") == "lazy"})
        if tag == "label":
            self._label_depth += 1
            if a.get("for"):
                self.labels_for.add(a["for"])
        if tag == "blockquote":
            self._bq, self._bqbuf = True, []
        if tag == "form":
            self._form = {"action": a.get("action", ""), "novalidate": "novalidate" in a, "fields": [], "submit": [],
                          "error_markup": False}
        if self._form is not None:
            if any(k in a for k in ("aria-live", "aria-describedby", "aria-invalid", "pattern")) or a.get("role") == "alert" \
                    or re.search(r"error|invalid", a.get("class", "") + " " + a.get("id", ""), re.I):
                self._form["error_markup"] = True
            if tag in ("input", "select", "textarea"):
                typ = a.get("type", "text" if tag == "input" else tag).lower()
                if typ in ("submit", "button", "image"):
                    self._form["submit"].append(a.get("value", typ))
                elif typ != "hidden":
                    name = a.get("name") or a.get("id") or a.get("placeholder") or tag
                    hint = " ".join([name, a.get("placeholder", ""), a.get("aria-label", ""), a.get("id", "")])
                    self._form["fields"].append({
                        "name": name, "tag": tag, "type": typ, "required": "required" in a,
                        "label": (a.get("id", "") and a["id"] in self.labels_for) or self._label_depth > 0
                        or bool(a.get("aria-label") or a.get("aria-labelledby")),
                        "placeholder": a.get("placeholder", ""), "autocomplete": a.get("autocomplete", ""),
                        "id": a.get("id", ""), "hint": hint})
        style = a.get("style", "")
        if tag in ("a", "button") and style:
            for prop, limit in (("height", 44), ("min-height", 44), ("font-size", 12)):
                m = re.search(rf"(?<![-\w]){prop}\s*:\s*(\d+(?:\.\d+)?)px", style)
                if m and float(m.group(1)) < limit:
                    self.small_targets.append(f"{tag} {prop}:{m.group(1)}px")
        if tag in ("title", "a", "button"):
            self._stack.append((tag, a, self.in_nav > 0, self.seen_h2))
            self._buf = []

    def handle_endtag(self, tag):
        if tag == "head":
            self.in_head = False
        if tag == "nav":
            self.in_nav = max(0, self.in_nav - 1)
        if tag == "label":
            self._label_depth = max(0, self._label_depth - 1)
        if tag == "script":
            self._in_script = False
        if tag == "blockquote" and self._bq:
            self._bq = False
            self.quotes.append(" ".join("".join(self._bqbuf).split()))
        if tag == "form" and self._form is not None:
            self.forms.append(self._form)
            self._form = None
        if self._stack and self._stack[-1][0] == tag:
            t, a, nav, after_h2 = self._stack.pop()
            txt = " ".join("".join(self._buf).split())
            if t == "title":
                self.title = txt
            elif t == "button":
                if self._form is not None:
                    self._form["submit"].append(txt or "(no text)")
                elif txt:
                    self.ctas.append({"text": txt, "href": "[button]", "zone": "nav" if nav else "body" if after_h2 else "hero",
                                      "primary": "primary" in a.get("class", "")})
            elif t == "a":
                href = a.get("href", "")
                if not txt and not a.get("aria-label") and not a.get("title"):
                    self.icon_links += 1
                cls = a.get("class", "")
                if txt and (ACTION.search(txt) or re.search(r"\b(btn|button|cta)\b", cls)):
                    self.ctas.append({"text": txt, "href": href, "zone": "nav" if nav else "body" if after_h2 else "hero",
                                      "primary": bool(re.search(r"primary", cls))})

    def handle_data(self, data):
        if self._in_script:
            return
        self._buf.append(data)
        self.text.append(data)
        if self._bq:
            self._bqbuf.append(data)


def prices(text):
    """Price strings, skipping revenue bands such as "$1M" or "$20K"."""
    return [m.group(0).strip() for m in PRICE.finditer(text) if not re.match(r"[\d.,]*\s?[MKBmkb]\b", text[m.end():m.end() + 3])
            and not re.search(r"[MKB]$", m.group(0))]


def near_form(raw):
    """Text within WINDOW characters of each form (inside it, just before it, just after it), tags stripped."""
    out = []
    for m in re.finditer(r"<form\b.*?</form>", raw, re.I | re.S):
        chunk = raw[max(0, m.start() - WINDOW):m.end() + WINDOW]
        out.append(re.sub(r"<[^>]+>", " ", chunk))
    return out


def inspect_markdown(path, raw):
    labels = re.findall(r"^\s*([A-Z][^\n*]{1,60}?)\s*\*\s*(?:\(|$)", raw, re.M)
    links = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", raw)
    return {
        "file": path, "is_html": False,
        "ctas": [{"text": t, "href": h} for t, h in links if ACTION.search(t)],
        "required_labels_marked": labels,
        "sensitive_required": [l for l in labels if SENSITIVE.search(l)],
        "quotes": re.findall(r"^>\s*(.+)$", raw, re.M),
        "prices": prices(raw), "currency_codes": sorted({c.upper() for c in CURRENCY_CODE.findall(raw)}),
        "privacy_text": bool(PRIVACY.search(raw)), "next_step_text": bool(NEXT_STEP.search(raw)),
        "no_card_claim": bool(NO_CARD.search(raw)),
    }


def inspect(path):
    raw = open(path, encoding="utf-8", errors="replace").read()
    if not re.search(r"<html|<!doctype html|<head|<body", raw, re.I):
        return inspect_markdown(path, raw)
    p = Page()
    p.feed(raw)
    text = " ".join(p.text)
    vp = p.viewport
    zoom_blocked = bool(vp) and bool(re.search(r"user-scalable\s*=\s*(no|0)|maximum-scale\s*=\s*1(\.0)?\b", vp, re.I))
    windows = near_form(raw)
    forms = []
    for i, f in enumerate(p.forms):
        near = windows[i] if i < len(windows) else ""
        fields = f["fields"]
        forms.append({
            "action": f["action"], "fields": len(fields), "required": sum(x["required"] for x in fields),
            "optional": [x["name"] for x in fields if not x["required"]],
            "sensitive_required": [x["name"] for x in fields if x["required"] and SENSITIVE.search(x["hint"])],
            "card_fields": [x["name"] for x in fields if CARD.search(x["hint"])],
            "placeholder_only": [x["name"] for x in fields if not x["label"]],
            "wrong_type": [f"{x['name']} (type={x['type']})" for x in fields
                           if (EMAILISH.search(x["hint"]) and x["type"] not in ("email",))
                           or (PHONEISH.search(x["hint"]) and x["type"] not in ("tel",))],
            "autocomplete_missing": [x["name"] for x in fields if not x["autocomplete"] and x["tag"] == "input"
                                     and x["type"] not in ("password",)],
            "submit": f["submit"] or ["(none)"],
            "novalidate": f["novalidate"], "error_markup": f["error_markup"],
            "privacy_near": bool(PRIVACY.search(near)), "next_step_near": bool(NEXT_STEP.search(near)),
            "proof_near": bool(re.search(r"<blockquote|testimonial|[\"“][^\"”]{12,}[\"”]\s*[—–-]\s*[A-Z]", raw[max(0, raw.lower().find("<form") - WINDOW):raw.lower().find("<form") + WINDOW], re.I)),
            "field_names": [x["name"] + ("*" if x["required"] else "") for x in fields],
        })
    return {
        "file": path, "is_html": True, "title": p.title,
        "viewport": vp, "viewport_present": vp is not None, "zoom_blocked": zoom_blocked,
        "ctas": p.ctas,
        "hero_primary_ctas": [c["text"] for c in p.ctas if c["zone"] == "hero" and c["primary"]],
        "forms": forms,
        "mailto_only": not p.forms and any(c["href"].startswith("mailto:") for c in p.ctas)
        and not any(c["href"].startswith("/") or c["href"].startswith("#") or c["href"].startswith("http") for c in p.ctas),
        "privacy_on_page": bool(PRIVACY.search(raw)),
        "quotes": p.quotes,
        "prices": prices(text), "currency_codes": sorted({c.upper() for c in CURRENCY_CODE.findall(text)}),
        "quoted_pricing": QUOTED.findall(text) and True or False,
        "no_card_claim": bool(NO_CARD.search(text)),
        "render_blocking_scripts": p.head_scripts_blocking, "head_stylesheets": p.head_stylesheets,
        "images": len(p.images), "images_unsized": sum(not i["sized"] for i in p.images),
        "images_no_alt": sum(not i["alt"] for i in p.images),
        "small_tap_targets": p.small_targets, "icon_only_links": p.icon_links,
    }


def yn(v):
    return "yes" if v else "NO"


def main():
    args = [a for a in sys.argv[1:] if a != "--json"]
    if not args:
        print(__doc__)
        return 2
    pages = [inspect(a) for a in args]
    if "--json" in sys.argv:
        print(json.dumps(pages, indent=1, ensure_ascii=False))
        return 0
    for r in pages:
        print(f"== {r['file']}")
        if not r["is_html"]:
            print("   NOT HTML: viewport, zoom, render-blocking scripts, image sizes and form markup (labels, types,")
            print("   error handling) can't be checked from this file. Ask for the raw HTML source to complete them.")
            print(f"   CTAs: {'; '.join(c['text'] + ' -> ' + c['href'] for c in r['ctas']) or 'none'}")
            if r["required_labels_marked"]:
                print(f"   fields marked required (*): {len(r['required_labels_marked'])}: {', '.join(r['required_labels_marked'])}")
                if r["sensitive_required"]:
                    print(f"   sensitive fields required: {', '.join(r['sensitive_required'])}")
            print(f"   quotes: {' | '.join(r['quotes']) or 'none'}")
            print(f"   prices: {', '.join(r['prices']) or 'none'} | currency codes: {', '.join(r['currency_codes']) or 'none'}")
            print(f"   privacy text: {yn(r['privacy_text'])} | next-step text: {yn(r['next_step_text'])}")
            continue
        vp = "MISSING" if not r["viewport_present"] else ("present, BLOCKS ZOOM (" + r["viewport"] + ")" if r["zoom_blocked"] else "present")
        print(f"   title: {r['title'] or '(none)'} | viewport: {vp}")
        for zone in ("nav", "hero", "body"):
            items = [c for c in r["ctas"] if c["zone"] == zone]
            if items:
                print(f"   CTAs ({zone}): " + "; ".join(f"{c['text']} -> {c['href']}{' [primary style]' if c['primary'] else ''}" for c in items))
        if len(r["hero_primary_ctas"]) > 1:
            print(f"   COMPETING: {len(r['hero_primary_ctas'])} primary-styled CTAs in the hero: {' | '.join(r['hero_primary_ctas'])}")
        if r["mailto_only"]:
            print("   PATH: mailto only, no form")
        for f in r["forms"]:
            print(f"   form -> {f['action'] or '(no action)'}: {f['fields']} fields, {f['required']} required: {', '.join(f['field_names'])}")
            if f["sensitive_required"]:
                print(f"      sensitive fields required: {', '.join(f['sensitive_required'])}")
            if f["card_fields"]:
                print(f"      card fields: {', '.join(f['card_fields'])}")
            if f["placeholder_only"]:
                print(f"      no visible label (placeholder only): {', '.join(f['placeholder_only'])}")
            if f["wrong_type"]:
                print(f"      input type doesn't match the field (mobile keyboard): {', '.join(f['wrong_type'])}")
            if f["autocomplete_missing"]:
                print(f"      no autocomplete attribute: {', '.join(f['autocomplete_missing'])}")
            err = "custom error markup present" if f["error_markup"] else ("NONE visible (novalidate set, no error markup)" if f["novalidate"] else "browser validation only (no error markup)")
            print(f"      submit: {' / '.join(f['submit'])} | error handling: {err}")
            print(f"      near the form: privacy {yn(f['privacy_near'])} | what happens next {yn(f['next_step_near'])} | proof {yn(f['proof_near'])}")
        print(f"   quotes on page: {' | '.join(r['quotes']) or 'none'} | privacy anywhere on page: {yn(r['privacy_on_page'])}")
        print(f"   prices: {', '.join(r['prices']) or 'none'} | currency codes: {', '.join(r['currency_codes']) or 'none'}{' | quoted pricing' if r['quoted_pricing'] else ''}")
        print(f"   speed: {len(r['render_blocking_scripts'])} render-blocking script(s) in head{(': ' + ', '.join(r['render_blocking_scripts'])) if r['render_blocking_scripts'] else ''}"
              f" | {r['head_stylesheets']} stylesheet(s) | images without width/height: {r['images_unsized']}/{r['images']} | without alt: {r['images_no_alt']}")
        if r["small_tap_targets"] or r["icon_only_links"]:
            print(f"   tap targets: small inline sizes: {', '.join(r['small_tap_targets']) or 'none'} | links with no text or label: {r['icon_only_links']}")
    html = [r for r in pages if r["is_html"]]
    labels = {}
    for r in pages:
        for c in r["ctas"]:
            labels.setdefault(c["text"], set()).add(r["file"].split("/")[-1])
    if len(pages) > 1 and labels:
        print(f"\n== across pages: {len(labels)} distinct CTA labels")
        for t, files in sorted(labels.items()):
            print(f"   {t}: {', '.join(sorted(files))}")
    claims = [r["file"] for r in pages if r.get("no_card_claim")]
    cards = [r["file"] for r in html for f in r["forms"] if f["card_fields"]]
    if claims and cards:
        print(f"   CONFLICT: 'no credit card' claimed on {', '.join(claims)} but a form asks for card details on {', '.join(cards)}")
    missing_vp = [r["file"] for r in html if not r["viewport_present"]]
    if html:
        print(f"   viewport on {len(html) - len(missing_vp)}/{len(html)} HTML pages{(' (missing: ' + ', '.join(missing_vp) + ')') if missing_vp else ''}")
    if len(html) < len(pages):
        print(f"   {len(pages) - len(html)} file(s) not HTML: markup checks incomplete for them")
    return 0


if __name__ == "__main__":
    sys.exit(main())
