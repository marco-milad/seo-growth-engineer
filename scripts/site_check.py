#!/usr/bin/env python3
"""Polite public SEO check: robots.txt, XML sitemaps, and on-page signals for a set of URLs.

What it fetches:
  1. <site>/robots.txt                     -> status, Sitemap: lines, allow/deny per checked URL
                                              (200 = rules read; 404/other 4xx = no rules; 401/403 = access denied and
                                              5xx/429/network error = unavailable: both leave crawl permissions unknown)
  2. sitemaps (robots.txt + /sitemap.xml)  -> URL inventory (sitemap indexes and .gz followed, capped)
  3. pages: --urls file, or an evenly spread sample of sitemap URLs (+ homepage)

Per page it records: redirect chain, final status, content type, response time, X-Robots-Tag,
<title>, meta description, meta robots/googlebot, canonical(s), hreflang alternates, html lang/dir,
H1s, heading-level skips, viewport, Open Graph basics, JSON-LD @types (+ parse errors),
images without alt, internal/external link counts, approximate visible word count.

Limits (state them in reports): raw HTML only. JavaScript is NOT executed, so content or tags
injected client-side are invisible here. That is useful (it shows what non-rendering crawlers and
the initial HTML contain), but rendered checks (Search Console URL Inspection, Rich Results Test,
a headless browser) are needed before concluding "missing" on JS-heavy sites.

Politeness: identifies itself, respects robots.txt for its own user agent by default, 1 request/sec
by default, hard page cap. Use only on sites the user owns or is authorized to audit, or for light
public checks of competitors.

Usage:
  python site_check.py https://example.com --out ./03-audit/evidence/site-check-2026-11-24
  python site_check.py https://example.com --urls urls.txt --delay 1.5 --out ./evidence/run-2
  python site_check.py https://example.com --sample 40 --max-sitemap-urls 20000 --out ./evidence/run-3
Outputs in --out: robots.txt, sitemap_urls.txt, pages.csv, pages.json, issues.csv, summary.md

Evidence safety: --out must be a new or empty folder (checked before any network request); reuse a
non-empty folder only with --overwrite. Only pages on the audited site (same host, with or without
"www.", same port) are fetched. Off-host URLs from the sitemap or from --urls are listed and reported, not
fetched, unless --allow-off-host is given. Sitemap files on another host that robots.txt or a sitemap
index points to are still read, and listed as external. Redirects are followed wherever they lead and
recorded in the chain.
Stdlib only.
"""
from __future__ import annotations

import argparse
import csv
import gzip
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import urllib.robotparser
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict
from html.parser import HTMLParser

UA = "SEO-Growth-Engineer-site-check/1.0 (+public SEO audit; python-urllib)"
TIMEOUT = 20
MAX_BYTES = 5_000_000


# --------------------------------------------------------------------------- HTTP
class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


_opener = urllib.request.build_opener(_NoRedirect)


def fetch_once(url: str):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip",
                                               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"})
    t0 = time.time()
    try:
        resp = _opener.open(req, timeout=TIMEOUT)
        status, headers = resp.status, resp.headers
        body = resp.read(MAX_BYTES)
    except urllib.error.HTTPError as e:
        status, headers = e.code, e.headers
        try:
            body = e.read(MAX_BYTES)
        except Exception:
            body = b""
    except Exception as e:  # DNS, TLS, timeout
        return {"url": url, "status": None, "error": f"{type(e).__name__}: {e}", "headers": {}, "body": b"",
                "ms": int((time.time() - t0) * 1000)}
    if headers.get("Content-Encoding", "").lower() == "gzip" and body:
        try:
            body = gzip.decompress(body)
        except OSError:
            pass
    return {"url": url, "status": status, "error": None, "headers": headers, "body": body,
            "ms": int((time.time() - t0) * 1000)}


def fetch(url: str, max_hops: int = 10):
    """Follow redirects manually so the chain is recorded."""
    chain, cur = [], url
    for _ in range(max_hops + 1):
        r = fetch_once(cur)
        chain.append((cur, r["status"]))
        if r["status"] in (301, 302, 303, 307, 308) and r["headers"].get("Location"):
            cur = urllib.parse.urljoin(cur, r["headers"]["Location"])
            if any(cur == c[0] for c in chain):
                r["error"] = "redirect loop"
                break
            continue
        break
    r["chain"] = chain
    r["final_url"] = cur
    return r


def decode(body: bytes, headers) -> str:
    ctype = headers.get("Content-Type", "") if headers else ""
    m = re.search(r"charset=([\w-]+)", ctype, re.I)
    enc = m.group(1) if m else None
    if not enc:
        m = re.search(rb"<meta[^>]+charset=[\"']?([\w-]+)", body[:4096], re.I)
        enc = m.group(1).decode("ascii", "ignore") if m else "utf-8"
    try:
        return body.decode(enc, errors="replace")
    except LookupError:
        return body.decode("utf-8", errors="replace")


# --------------------------------------------------------------------------- HTML parsing
class PageParser(HTMLParser):
    SKIP_TEXT = {"script", "style", "noscript", "template", "svg"}

    def __init__(self, base_url):
        super().__init__(convert_charrefs=True)
        self.base = base_url
        self.host = urllib.parse.urlparse(base_url).netloc.lower()
        self.title, self._in_title, self._title_done = "", False, False
        self.meta_desc, self.meta_robots, self.viewport = [], [], None
        self.og = {}
        self.canonicals, self.hreflang = [], []
        self.lang = self.dir = None
        self.headings, self._hstack = [], None
        self.imgs = self.imgs_no_alt = self.imgs_empty_alt = 0
        self.links_int = self.links_ext = self.links_nofollow = 0
        self.jsonld_raw, self._in_jsonld = [], False
        self._skip = 0
        self.text_parts = []

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "html":
            self.lang, self.dir = a.get("lang"), a.get("dir")
        elif tag == "title" and not self._title_done:
            self._in_title = True
        elif tag == "meta":
            name = (a.get("name") or "").lower()
            prop = (a.get("property") or "").lower()
            if name == "description":
                self.meta_desc.append(a.get("content", ""))
            elif name in ("robots", "googlebot"):
                self.meta_robots.append(f"{name}:{a.get('content', '')}")
            elif name == "viewport":
                self.viewport = a.get("content", "")
            if prop in ("og:title", "og:description", "og:image", "og:url"):
                self.og[prop] = a.get("content", "")
        elif tag == "link":
            rel = (a.get("rel") or "").lower().split()
            if "canonical" in rel:
                self.canonicals.append(a.get("href", ""))
            if "alternate" in rel and a.get("hreflang"):
                self.hreflang.append((a["hreflang"], urllib.parse.urljoin(self.base, a.get("href", ""))))
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._hstack = [int(tag[1]), ""]
        elif tag == "img":
            self.imgs += 1
            if "alt" not in a:
                self.imgs_no_alt += 1
            elif not a["alt"].strip():
                self.imgs_empty_alt += 1
        elif tag == "a" and a.get("href"):
            href = a["href"].strip()
            if href.startswith(("mailto:", "tel:", "javascript:", "#")):
                return
            netloc = urllib.parse.urlparse(urllib.parse.urljoin(self.base, href)).netloc.lower()
            if netloc.removeprefix("www.") == self.host.removeprefix("www."):
                self.links_int += 1
            else:
                self.links_ext += 1
            if "nofollow" in (a.get("rel") or "").lower():
                self.links_nofollow += 1
        elif tag == "script" and (a.get("type") or "").lower() == "application/ld+json":
            self._in_jsonld = True
            self.jsonld_raw.append("")
        if tag in self.SKIP_TEXT:
            self._skip += 1

    def handle_endtag(self, tag):
        if tag == "title" and self._in_title:
            self._in_title, self._title_done = False, True
        elif tag in ("h1", "h2", "h3", "h4", "h5", "h6") and self._hstack:
            self.headings.append((self._hstack[0], " ".join(self._hstack[1].split())))
            self._hstack = None
        elif tag == "script" and self._in_jsonld:
            self._in_jsonld = False
        if tag in self.SKIP_TEXT and self._skip:
            self._skip -= 1

    def handle_data(self, data):
        if self._in_title:
            self.title += data
        if self._in_jsonld:
            self.jsonld_raw[-1] += data
            return
        if self._hstack is not None:
            self._hstack[1] += data
        if not self._skip:
            self.text_parts.append(data)


def jsonld_types(raw_blocks):
    types, errors = [], 0

    def walk(node):
        if isinstance(node, dict):
            t = node.get("@type")
            if isinstance(t, list):
                types.extend(str(x) for x in t)
            elif t:
                types.append(str(t))
            for v in node.values():
                if isinstance(v, (dict, list)):
                    walk(v)
        elif isinstance(node, list):
            for x in node:
                walk(x)

    for raw in raw_blocks:
        try:
            walk(json.loads(raw.strip()))
        except (json.JSONDecodeError, ValueError):
            errors += 1
    return sorted(set(types)), errors


def word_count(text: str) -> int:
    return len(re.findall(r"[\w؀-ۿ]+", text))


# --------------------------------------------------------------------------- sitemaps
NS = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9", "xhtml": "http://www.w3.org/1999/xhtml"}


def _local(tag):
    """Element name without its namespace ({ns}url -> url); works with or without a namespace."""
    return tag.split("}")[-1] if isinstance(tag, str) else ""


def _namespace(tag):
    return tag[1:].split("}")[0] if isinstance(tag, str) and tag.startswith("{") else ""


def _children(el, name):
    return [c for c in el if _local(c.tag) == name]


def _child(el, name):
    kids = _children(el, name)
    return kids[0] if kids else None


def parse_sitemap(url, max_urls, delay, log, depth=0, seen=None):
    seen = seen if seen is not None else set()
    out = {"urls": [], "with_lastmod": 0, "with_hreflang": 0, "files": [], "errors": []}
    if url in seen or depth > 3:
        return out
    seen.add(url)
    r = fetch(url)
    time.sleep(delay)
    out["files"].append((url, r["status"], r["final_url"]))
    if r["status"] != 200:
        out["errors"].append(f"{url} -> {r['status'] or r['error']}")
        return out
    body = r["body"]
    if url.endswith(".gz") or body[:2] == b"\x1f\x8b":
        try:
            body = gzip.decompress(body)
        except OSError:
            pass
    try:
        root = ET.fromstring(body)
    except ET.ParseError as e:
        out["errors"].append(f"{url} -> XML parse error: {e}")
        return out
    # Elements are matched by local name, so namespace-less or non-standard-namespace sitemaps still parse.
    tag, ns = _local(root.tag), _namespace(root.tag)
    if tag not in ("sitemapindex", "urlset"):
        out["errors"].append(f"{url} -> unexpected root element <{tag}> (not a sitemap); 0 URLs read")
        return out
    if ns != NS["sm"]:
        out["errors"].append(f"{url} -> warning: {'non-standard sitemap namespace (' + ns + ')' if ns else 'missing sitemap namespace'};"
                             " parsed anyway - confirm Search Console accepts it (Sitemaps report)")
    if tag == "sitemapindex":
        entries = [_child(s, "loc") for s in _children(root, "sitemap")]
        entries = [e for e in entries if e is not None and (e.text or "").strip()]
        if not entries:
            out["errors"].append(f"{url} -> warning: sitemap index lists 0 sitemaps (empty or unexpected format)")
        for loc in entries:
            if len(out["urls"]) >= max_urls:
                break
            child = parse_sitemap(loc.text.strip(), max_urls - len(out["urls"]), delay, log, depth + 1, seen)
            for k in ("urls", "files", "errors"):
                out[k].extend(child[k])
            out["with_lastmod"] += child["with_lastmod"]
            out["with_hreflang"] += child["with_hreflang"]
    else:
        read_here = 0
        for u in _children(root, "url"):
            loc = _child(u, "loc")
            if loc is None or not (loc.text or "").strip():
                continue
            out["urls"].append(loc.text.strip())
            read_here += 1
            if _child(u, "lastmod") is not None:
                out["with_lastmod"] += 1
            if _children(u, "link"):
                out["with_hreflang"] += 1
            if len(out["urls"]) >= max_urls:
                break
        if read_here == 0:
            out["errors"].append(f"{url} -> warning: 0 URLs found (empty or unexpected format)")
    log(f"  sitemap {url}: {len(out['urls'])} URLs so far")
    return out


def spread_sample(urls, n):
    if len(urls) <= n:
        return list(urls)
    step = len(urls) / n
    return [urls[int(i * step)] for i in range(n)]


# --------------------------------------------------------------------------- analysis
ROBOTS_STATES = {
    "parsed": "rules read",
    "no-rules": "no robots.txt published (4xx): no rules apply",
    "denied": "ACCESS DENIED (401/403): rules unknown, crawl permissions unknown",
    "unavailable": "UNAVAILABLE (5xx/429/network error): crawl permissions unknown",
}


def host_key(url):
    """Same-site key: lowercased hostname without a leading 'www.', plus any non-default port. Scheme ignored."""
    p = urllib.parse.urlparse(url)
    host = (p.hostname or "").lower().removeprefix("www.")
    try:
        port = p.port
    except ValueError:
        port = None
    return host + (f":{port}" if port and port not in (80, 443) else "")


def classify_robots(status):
    """Map the robots.txt HTTP result to a state. Never treat an error as permission to crawl."""
    if status == 200:
        return "parsed"
    if status in (401, 403):
        return "denied"
    if status is None or status == 429 or status >= 500:
        return "unavailable"
    if 400 <= status < 500:
        return "no-rules"
    return "unavailable"  # e.g. a redirect chain that never resolved


def robots_permission(robots, robots_state, url):
    """allowed / disallowed (rules read), no-rules (4xx), or unknown (denied/unavailable)."""
    if robots_state == "parsed":
        return "allowed" if robots.can_fetch("Googlebot", url) else "disallowed"
    if robots_state == "no-rules":
        return "no-rules"
    return "unknown"


VALUE_DIRECTIVES = {"max-snippet", "max-image-preview", "max-video-preview", "unavailable_after"}


def is_noindex_directive(token):
    """Exact directive match only: 'noindex' or 'none' (= noindex, nofollow). 'noimageindex' etc. don't match."""
    return token.strip().lower() in ("noindex", "none")


def meta_noindex(meta_entries):
    """meta_entries are 'robots:<content>' / 'googlebot:<content>' strings (both apply to Google)."""
    return any(is_noindex_directive(t) for e in meta_entries for t in e.split(":", 1)[-1].split(","))


def parse_x_robots(values):
    """Return (google_noindex, other_agents_with_noindex). A 'name:' prefix that isn't a known value directive
    is a user-agent prefix; it applies to the directives after it in the same header."""
    google, others = False, []
    for value in values:
        agent = None
        for part in value.split(","):
            part = part.strip()
            m = re.match(r"^([A-Za-z0-9_.\-]+)\s*:\s*(.*)$", part)
            if m and m.group(1).lower() not in VALUE_DIRECTIVES:
                agent, part = m.group(1).lower(), m.group(2).strip()
            if is_noindex_directive(part):
                if agent in (None, "googlebot"):
                    google = True
                else:
                    others.append(agent)
    return google, sorted(set(others))


def analyse_page(url, r, robots, robots_state, sitemap_set):
    headers = r.get("headers")
    xr_values = (headers.get_all("X-Robots-Tag") or []) if hasattr(headers, "get_all") else []
    xr_google, xr_others = parse_x_robots(xr_values)
    rec = {"url": url, "final_url": r.get("final_url"), "status": r.get("status"), "error": r.get("error"),
           "redirect_hops": max(len(r.get("chain", [])) - 1, 0),
           "chain": " -> ".join(f"{u} [{s}]" for u, s in r.get("chain", [])),
           "ms": r.get("ms"), "content_type": (r["headers"].get("Content-Type", "") if r.get("headers") else ""),
           "x_robots_tag": " | ".join(xr_values),
           "robots_allowed_googlebot": robots_permission(robots, robots_state, url),
           "in_sitemap": url in sitemap_set,
           "_xr_google_noindex": xr_google, "_xr_other_noindex": xr_others, "_meta_noindex": False}
    if r.get("status") == 200 and "html" in rec["content_type"].lower():
        p = PageParser(rec["final_url"])
        try:
            p.feed(decode(r["body"], r["headers"]))
        except Exception as e:  # malformed markup should not kill the run
            rec["error"] = f"parse: {e}"
        types, jerr = jsonld_types(p.jsonld_raw)
        h1s = [t for lvl, t in p.headings if lvl == 1]
        skips, prev = 0, 0
        for lvl, _ in p.headings:
            if prev and lvl > prev + 1:
                skips += 1
            prev = lvl
        canon_abs = [urllib.parse.urljoin(rec["final_url"], c) for c in p.canonicals]
        rec.update({
            "title": " ".join(p.title.split()), "title_len": len(" ".join(p.title.split())),
            "meta_description": " ".join((p.meta_desc[0] if p.meta_desc else "").split()),
            "meta_description_len": len(" ".join((p.meta_desc[0] if p.meta_desc else "").split())),
            "meta_description_count": len(p.meta_desc),
            "meta_robots": "; ".join(p.meta_robots), "_meta_noindex": meta_noindex(p.meta_robots),
            "canonical": canon_abs[0] if canon_abs else "", "canonical_count": len(canon_abs),
            "canonical_is_relative": bool(p.canonicals and not re.match(r"^https?://", p.canonicals[0])),
            "canonical_self": bool(canon_abs and canon_abs[0].rstrip("/") == rec["final_url"].rstrip("/")),
            "hreflang": "; ".join(f"{l}={u}" for l, u in p.hreflang), "hreflang_count": len(p.hreflang),
            "html_lang": p.lang or "", "html_dir": p.dir or "",
            "h1_count": len(h1s), "h1": " || ".join(h1s)[:300], "heading_count": len(p.headings), "heading_skips": skips,
            "viewport": p.viewport or "",
            "og_title": bool(p.og.get("og:title")), "og_image": bool(p.og.get("og:image")),
            "jsonld_types": ", ".join(types), "jsonld_errors": jerr,
            "img_total": p.imgs, "img_missing_alt": p.imgs_no_alt, "img_empty_alt": p.imgs_empty_alt,
            "links_internal": p.links_int, "links_external": p.links_ext, "links_nofollow": p.links_nofollow,
            "word_count": word_count(" ".join(p.text_parts)),
            "_hreflang_pairs": p.hreflang,
        })
    return rec


def issues_for(rec):
    out = []

    def add(check, level, detail=""):
        out.append({"url": rec["url"], "check": check, "level": level, "detail": detail})

    if rec.get("error") and not rec.get("status"):
        add("fetch-error", "high", rec["error"])
        return out
    if rec["redirect_hops"] >= 1:
        add("redirected", "info" if rec["redirect_hops"] == 1 else "medium", rec["chain"])
    if rec["redirect_hops"] >= 2:
        add("redirect-chain", "medium", f"{rec['redirect_hops']} hops")
    if rec["status"] != 200:
        add("non-200-final", "high", str(rec["status"]))
        if rec["in_sitemap"]:
            add("sitemap-url-not-200", "medium", str(rec["status"]))
        return out
    if rec["in_sitemap"] and rec["redirect_hops"]:
        add("sitemap-url-redirects", "medium", rec["final_url"])
    if rec["redirect_hops"]:
        # page-level checks belong to the final URL; check it directly to avoid double counting
        return out
    if rec["robots_allowed_googlebot"] == "disallowed":
        add("blocked-by-robots", "high" if rec["in_sitemap"] else "medium",
            "listed in sitemap but disallowed" if rec["in_sitemap"] else "")
    if rec.get("_xr_google_noindex"):
        add("x-robots-noindex", "high", rec["x_robots_tag"])
    if rec.get("_xr_other_noindex"):
        add("x-robots-noindex-other-agent", "info",
            f"noindex for {', '.join(rec['_xr_other_noindex'])} only (not a Google noindex): {rec['x_robots_tag']}")
    if "title" not in rec:
        add("not-html", "info", rec["content_type"])
        return out
    if rec.get("_meta_noindex"):
        add("meta-noindex", "high" if rec["in_sitemap"] else "medium", rec["meta_robots"])
    if not rec["title"]:
        add("title-missing", "high")
    elif rec["title_len"] > 65:
        add("title-long", "low", f"{rec['title_len']} chars (truncation depends on pixel width; Arabic glyph widths differ)")
    elif rec["title_len"] < 15:
        add("title-short", "low", f"{rec['title_len']} chars")
    if not rec["meta_description"]:
        add("meta-description-missing", "low")
    elif rec["meta_description_len"] > 170:
        add("meta-description-long", "low", f"{rec['meta_description_len']} chars")
    if rec["meta_description_count"] > 1:
        add("meta-description-multiple", "medium", str(rec["meta_description_count"]))
    if rec["canonical_count"] == 0:
        add("canonical-missing", "medium")
    elif rec["canonical_count"] > 1:
        add("canonical-multiple", "high", str(rec["canonical_count"]))
    elif not rec["canonical_self"]:
        add("canonical-points-elsewhere", "medium", rec["canonical"])
    if rec.get("canonical_is_relative"):
        add("canonical-relative", "low", "absolute URLs are recommended")
    if rec["h1_count"] == 0:
        add("h1-missing", "medium", "in raw HTML; verify rendered DOM if JS framework")
    elif rec["h1_count"] > 1:
        add("h1-multiple", "low", rec["h1"])
    if rec["heading_skips"]:
        add("heading-level-skip", "info", str(rec["heading_skips"]))
    if not rec["html_lang"]:
        add("html-lang-missing", "low")
    if not rec["viewport"]:
        add("viewport-missing", "medium")
    if rec["jsonld_errors"]:
        add("jsonld-parse-error", "medium", f"{rec['jsonld_errors']} block(s)")
    if rec["img_missing_alt"]:
        add("img-alt-attribute-missing", "low", f"{rec['img_missing_alt']}/{rec['img_total']} (empty alt is fine for decorative images)")
    if rec["word_count"] < 150:
        add("low-word-count", "info", f"{rec['word_count']} words in raw HTML; may be JS-rendered or intentionally short; verify")
    if rec["hreflang_count"]:
        langs = [l.lower() for l, _ in rec["_hreflang_pairs"]]
        urls = [u.rstrip("/") for _, u in rec["_hreflang_pairs"]]
        if rec["final_url"].rstrip("/") not in urls:
            add("hreflang-no-self-reference", "medium")
        if "x-default" not in langs:
            add("hreflang-no-x-default", "info")
        bad = [l for l in langs if l != "x-default" and not re.match(r"^[a-z]{2,3}(-([a-z]{4}|[a-z]{2}|\d{3}))?$", l)]
        if bad:
            add("hreflang-invalid-code", "medium", ", ".join(bad))
        dup = [l for l, c in Counter(langs).items() if c > 1]
        if dup:
            add("hreflang-duplicate-code", "medium", ", ".join(dup))
    return out


def cross_page_issues(records):
    out = []
    ok = [r for r in records if r.get("title") is not None and r.get("status") == 200 and not r.get("redirect_hops")]
    for field, check in (("title", "title-duplicate"), ("meta_description", "meta-description-duplicate")):
        groups = defaultdict(list)
        for r in ok:
            if r.get(field):
                groups[r[field].strip().lower()].append(r["url"])
        for val, urls in groups.items():
            if len(urls) > 1:
                for u in urls:
                    out.append({"url": u, "check": check, "level": "medium", "detail": f"shared by {len(urls)} sampled URLs"})
    # hreflang reciprocity among fetched pages
    by_url = {r["final_url"].rstrip("/"): r for r in ok}
    for r in ok:
        for lang, target in r.get("_hreflang_pairs", []):
            t = by_url.get(target.rstrip("/"))
            if t is None or t is r:
                continue
            back = [u.rstrip("/") for _, u in t.get("_hreflang_pairs", [])]
            if r["final_url"].rstrip("/") not in back:
                out.append({"url": r["url"], "check": "hreflang-not-reciprocal", "level": "medium",
                            "detail": f"{lang} -> {target} does not link back"})
    return out


# --------------------------------------------------------------------------- main
def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("site", help="site root, e.g. https://example.com")
    ap.add_argument("--urls", help="file with one URL per line (otherwise sample from sitemap)")
    ap.add_argument("--sample", type=int, default=25, help="pages to sample from the sitemap (default 25)")
    ap.add_argument("--max-pages", type=int, default=200, help="hard cap on pages fetched (default 200)")
    ap.add_argument("--max-sitemap-urls", type=int, default=50000)
    ap.add_argument("--delay", type=float, default=1.0, help="seconds between requests (default 1.0)")
    ap.add_argument("--ignore-robots", action="store_true",
                    help="fetch URLs even if robots.txt disallows this tool (only for sites you are authorized to audit)")
    ap.add_argument("--out", default="site-check-output",
                    help="output folder; must be new or empty unless --overwrite (default: site-check-output)")
    ap.add_argument("--overwrite", action="store_true",
                    help="allow writing into a non-empty --out folder (replaces the six output files)")
    ap.add_argument("--allow-off-host", action="store_true",
                    help="also fetch page URLs on other hosts (from the sitemap or --urls)")
    args = ap.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    log = lambda m: print(m, flush=True)  # noqa: E731

    site = args.site.rstrip("/")
    if not re.match(r"^https?://", site):
        site = "https://" + site

    # evidence safety: refuse to overwrite earlier output before any network request
    if os.path.isfile(args.out):
        print(f"ERROR: --out {args.out} is an existing file; give a folder. Nothing was fetched or written.")
        return 2
    if os.path.isdir(args.out) and os.listdir(args.out) and not args.overwrite:
        print(f"ERROR: --out {args.out} already contains files (earlier evidence?). Use a new dated folder, or add "
              "--overwrite to replace the output files there. Nothing was fetched or written.")
        return 2
    os.makedirs(args.out, exist_ok=True)
    started = time.strftime("%Y-%m-%d %H:%M:%S")
    site_key = host_key(site)
    same_site = lambda u: host_key(u) == site_key  # noqa: E731

    # robots.txt
    log(f"[1/3] robots.txt for {site}")
    rr = fetch(site + "/robots.txt")
    robots_state = classify_robots(rr["status"])
    robots_text = decode(rr["body"], rr["headers"]) if robots_state == "parsed" else ""
    with open(os.path.join(args.out, "robots.txt"), "w", encoding="utf-8") as fh:
        fh.write(robots_text or f"# status {rr['status']} {rr['error'] or ''} -> {robots_state}\n")
    robots = urllib.robotparser.RobotFileParser()
    robots.parse(robots_text.splitlines() if robots_text else [])
    if robots_state in ("denied", "unavailable"):
        log(f"  WARNING robots.txt {ROBOTS_STATES[robots_state]}")
    sitemap_lines = re.findall(r"(?im)^\s*sitemap:\s*(\S+)", robots_text)
    time.sleep(args.delay)

    # sitemaps
    log("[2/3] sitemaps")
    candidates = sitemap_lines or [site + "/sitemap.xml"]
    sm = {"urls": [], "with_lastmod": 0, "with_hreflang": 0, "files": [], "errors": []}
    seen = set()
    for s in candidates:
        part = parse_sitemap(s, args.max_sitemap_urls - len(sm["urls"]), args.delay, log, seen=seen)
        for k in ("urls", "files", "errors"):
            sm[k].extend(part[k])
        sm["with_lastmod"] += part["with_lastmod"]
        sm["with_hreflang"] += part["with_hreflang"]
    sitemap_urls = list(dict.fromkeys(sm["urls"]))
    with open(os.path.join(args.out, "sitemap_urls.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(sitemap_urls))
    off_host = [u for u in sitemap_urls if not same_site(u)]
    external_sitemaps = [f[0] for f in sm["files"] if not same_site(f[0])]
    for x in external_sitemaps:
        log(f"  note: external sitemap file read (another host): {x}")

    # pages: only the audited site unless --allow-off-host
    if args.urls:
        with open(args.urls, encoding="utf-8-sig") as fh:
            urls = [l.strip() for l in fh if l.strip() and not l.startswith("#")]
    else:
        pool = sitemap_urls if args.allow_off_host else [u for u in sitemap_urls if same_site(u)]
        urls = [site + "/"] + spread_sample(pool, max(args.sample - 1, 0))
    urls = list(dict.fromkeys(urls))
    off_host_skipped = [] if args.allow_off_host else [u for u in urls if not same_site(u)]
    urls = [u for u in urls if u not in off_host_skipped][: args.max_pages]
    own_robots_ok = lambda u: args.ignore_robots or not robots_text or robots.can_fetch(UA, u)  # noqa: E731
    log(f"[3/3] checking {len(urls)} pages (delay {args.delay}s)")
    sitemap_set = set(sitemap_urls)
    records, skipped = [], []
    for i, u in enumerate(urls, 1):
        if not own_robots_ok(u):
            skipped.append(u)
            continue
        r = fetch(u)
        records.append(analyse_page(u, r, robots, robots_state, sitemap_set))
        log(f"  {i}/{len(urls)} {r.get('status')} {u}")
        time.sleep(args.delay)

    issues = [i for rec in records for i in issues_for(rec)] + cross_page_issues(records)
    if robots_state == "denied":
        issues.insert(0, {"url": site + "/robots.txt", "check": "robots-txt-access-denied", "level": "high",
                          "detail": f"HTTP {rr['status']} for this tool; rules and crawl permissions unknown. Googlebot may "
                                    "receive a different response (firewall/bot protection). Confirm in Search Console's "
                                    "robots.txt report before drawing any crawl conclusion."})
    elif robots_state == "unavailable":
        issues.insert(0, {"url": site + "/robots.txt", "check": "robots-txt-unavailable", "level": "high",
                          "detail": f"{('HTTP ' + str(rr['status'])) if rr['status'] else ('network error: ' + str(rr['error']))}: crawl permissions unknown. Google can reduce or stop "
                                    "crawling while robots.txt returns server errors (see Google's robots.txt documentation; "
                                    "verify current behaviour). Re-check, and confirm in Search Console."})
    for u in skipped:
        googlebot_blocked = not robots.can_fetch("Googlebot", u)
        in_sm = u in sitemap_set
        issues.append({"url": u, "check": "robots-disallowed-not-fetched",
                       "level": "high" if (googlebot_blocked and in_sm) else "info",
                       "detail": ("listed in sitemap but disallowed for Googlebot" if (googlebot_blocked and in_sm)
                                  else "disallowed for this tool; Googlebot " + ("blocked" if googlebot_blocked else "allowed"))})
    if off_host:
        issues.append({"url": site + " (sitemap)", "check": "sitemap-off-host-urls", "level": "medium",
                       "detail": f"{len(off_host)} sitemap URL(s) on other hosts, "
                                 + ("fetched because --allow-off-host was given" if args.allow_off_host else "not fetched")
                                 + f"; e.g. {', '.join(off_host[:3])}"})
    for u in off_host_skipped:
        issues.append({"url": u, "check": "off-host-url-not-fetched", "level": "info",
                       "detail": "not on the audited site; add --allow-off-host to include it (e.g. old-domain URLs "
                                 "after a domain move)"})

    # write outputs
    cols = ["url", "final_url", "status", "redirect_hops", "chain", "ms", "content_type", "x_robots_tag",
            "robots_allowed_googlebot", "in_sitemap", "title", "title_len", "meta_description", "meta_description_len",
            "meta_description_count", "meta_robots", "canonical", "canonical_count", "canonical_self", "hreflang",
            "hreflang_count", "html_lang", "html_dir", "h1_count", "h1", "heading_count", "heading_skips", "viewport",
            "og_title", "og_image", "jsonld_types", "jsonld_errors", "img_total", "img_missing_alt", "img_empty_alt",
            "links_internal", "links_external", "links_nofollow", "word_count", "error"]
    with open(os.path.join(args.out, "pages.csv"), "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(records)
    with open(os.path.join(args.out, "pages.json"), "w", encoding="utf-8") as fh:
        json.dump([{k: v for k, v in r.items() if not k.startswith("_")} for r in records], fh, ensure_ascii=False, indent=1)
    with open(os.path.join(args.out, "issues.csv"), "w", newline="", encoding="utf-8-sig") as fh:
        w = csv.DictWriter(fh, fieldnames=["url", "check", "level", "detail"])
        w.writeheader()
        w.writerows(issues)

    counts = Counter((i["check"], i["level"]) for i in issues)
    status_counts = Counter(str(r["status"]) for r in records)
    L = [f"# Site check: {site}", "",
         f"- Run: {started} (local time) · tool: site_check.py · raw HTML, JavaScript not executed",
         f"- robots.txt: {('HTTP ' + str(rr['status'])) if rr['status'] else ('network error (' + str(rr['error']) + ')')}"
         f" → {ROBOTS_STATES[robots_state]} · Sitemap lines: {len(sitemap_lines)}",
         f"- Sitemap files read: {len(sm['files'])} (external hosts: {len(external_sitemaps)}) · URLs found: {len(sitemap_urls)}"
         f" · with lastmod: {sm['with_lastmod']} · with hreflang: {sm['with_hreflang']}"
         f" · off-host URLs: {len(off_host)} ({'fetchable: --allow-off-host' if args.allow_off_host else 'not fetched'})",
         f"- Pages checked: {len(records)} (status: {dict(status_counts)})"
         + (f" · skipped by robots.txt for this tool: {len(skipped)}" if skipped else "")
         + (f" · off-host URLs from --urls not fetched: {len(off_host_skipped)}" if off_host_skipped else ""), ""]
    if external_sitemaps:
        L += ["## External sitemap files read", ""] + [f"- {x}" for x in external_sitemaps] + [""]
    if off_host:
        L += ["## Off-host URLs listed in the sitemap" + ("" if args.allow_off_host else " (not fetched)"), ""] \
             + [f"- {u}" for u in off_host[:10]] + ([f"- ... and {len(off_host) - 10} more"] if len(off_host) > 10 else []) + [""]
    if sm["errors"]:
        L += ["## Sitemap errors and warnings", ""] + [f"- {e}" for e in sm["errors"]] + [""]
    L += ["## Issue counts (signals to review, not final priorities)", "", "| Check | Level | Pages |", "|---|---|---|"]
    order = {"high": 0, "medium": 1, "low": 2, "info": 3}
    for (check, level), n in sorted(counts.items(), key=lambda kv: (order.get(kv[0][1], 9), -kv[1])):
        L.append(f"| {check} | {level} | {n} |")
    L += ["", "## Limits", "",
          "- Sample, not a full crawl: absence of an issue here does not mean it is absent site-wide.",
          "- Raw HTML only. Confirm 'missing' tags on JS-rendered sites with URL Inspection or a rendered check.",
          "- robots_allowed_googlebot is allowed/disallowed only when robots.txt was read (HTTP 200), no-rules when it "
          "returned 404 or another 4xx, and unknown when it was denied (401/403) or unavailable (5xx/429/network error). "
          "It uses Python's robots.txt parser, which can differ from Google's on edge cases; confirm important blocks in "
          "Search Console's robots.txt report.",
          "- Details per URL: pages.csv / issues.csv in this folder."]
    with open(os.path.join(args.out, "summary.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
    log(f"\nDone. {len(records)} pages, {len(issues)} issue signals. Outputs in {os.path.abspath(args.out)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
