#!/usr/bin/env python3
"""Read a public Luma event without signing in and print clean JSON.

Usage: python3 luma-event.py https://luma.com/<slug>

Method: Luma's public API (https://api.lu.ma/url?url=<slug>), which returns the
same data the event page renders. Falls back to the __NEXT_DATA__ JSON embedded
in the event page. Stdlib only.
"""
import json, re, sys, urllib.parse, urllib.request

UA = {"User-Agent": "Mozilla/5.0 (grokbot-meetup luma-event.py)", "Accept": "application/json,text/html"}


def get(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode("utf-8", "replace")


def slug_of(url):
    p = urllib.parse.urlparse(url if "://" in url else "https://luma.com/" + url)
    return p.path.strip("/").split("/")[-1]


def find_payload(obj):
    """Find the dict holding both 'event' and 'hosts' anywhere in a JSON tree."""
    if isinstance(obj, dict):
        if isinstance(obj.get("event"), dict) and "hosts" in obj:
            return obj
        for v in obj.values():
            r = find_payload(v)
            if r:
                return r
    elif isinstance(obj, list):
        for v in obj:
            r = find_payload(v)
            if r:
                return r
    return None


def fetch(url):
    slug = slug_of(url)
    errors = []
    try:
        j = json.loads(get("https://api.lu.ma/url?url=" + urllib.parse.quote(slug)))
        d = find_payload(j)
        if d:
            return d, "api.lu.ma/url"
    except Exception as e:
        errors.append("api: %s" % e)
    try:
        html = get("https://luma.com/" + slug)
        m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
        if m:
            d = find_payload(json.loads(m.group(1)))
            if d:
                return d, "__NEXT_DATA__"
    except Exception as e:
        errors.append("page: %s" % e)
    sys.exit("could not read Luma event %s (%s)" % (slug, "; ".join(errors)))


def doc_text(node):
    """ProseMirror doc (description_mirror) to plain text with line breaks."""
    if not isinstance(node, dict):
        return ""
    t = node.get("type")
    if t == "text":
        return node.get("text", "")
    if t == "hard_break":
        return "\n"
    inner = "".join(doc_text(c) for c in node.get("content", []) or [])
    if t == "list_item":
        return "- " + inner.strip() + "\n"
    if t in ("paragraph", "heading"):
        return inner.strip() + "\n\n"
    return inner


def link(base, handle):
    if not handle:
        return None
    if handle.startswith("http"):
        return handle
    return base + handle.lstrip("/@") if base.endswith("/") else base + "/" + handle.lstrip("/")


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    d, source = fetch(sys.argv[1])
    e = d["event"]
    geo = e.get("geo_address_info") or {}
    li = lambda h: None if not h else (h if h.startswith("http") else "https://www.linkedin.com" + ("/" + h.lstrip("/") if h.startswith(("/in/", "in/", "/company/")) else "/in/" + h.lstrip("/")))
    hosts = [{
        "name": h.get("name"),
        "linkedin": li(h.get("linkedin_handle")),
        "x": ("https://x.com/" + h["twitter_handle"].lstrip("@")) if h.get("twitter_handle") else None,
        "website": h.get("website") or None,
        "luma": ("https://luma.com/user/" + h["username"]) if h.get("username") else None,
    } for h in d.get("hosts") or []]
    cover = e.get("cover_url") or (d.get("cover_image") or {}).get("url")
    out = {
        "name": e.get("name"),
        "start": e.get("start_at"),
        "end": e.get("end_at"),
        "timezone": e.get("timezone"),
        "venue": geo.get("address"),
        "address": geo.get("full_address"),
        "description": re.sub(r"\n{3,}", "\n\n", doc_text(d.get("description_mirror") or {})).strip(),
        "hosts": hosts,
        "cover_url": cover,
        "url": "https://luma.com/" + (e.get("url") or slug_of(sys.argv[1])),
        "source": source,
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
