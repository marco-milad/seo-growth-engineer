#!/usr/bin/env python3
"""Compare business Name / Address / Phone (+ optional hours, website) across sources.

Input: a CSV with one row per source (website footer, contact page, schema,
Google Business Profile, directories, social profiles...). Columns:
  source, name, address, phone            (required)
  hours, website, location_id             (optional; location_id for multi-location)

Every value is normalized before comparing, so that harmless formatting differences
are separated from real inconsistencies:
- name, address, hours: Arabic letter variants, diacritics, Arabic-Indic digits,
  punctuation. A close-but-different value is reported as "similar" (review it).
- phone: digits only (Arabic-Indic digits converted). "+" or "00" marks an international
  number. A leading national "0" is converted to the country code ONLY when --country is
  given and that country uses 0 as its trunk prefix; bare national numbers in closed
  numbering plans (KW, QA, BH, OM, TN) get the country code. Otherwise nothing is
  inferred. Phones must match exactly after this normalization: no "similar".
- website: scheme, "www.", host case, trailing slash and #fragment ignored; known tracking
  parameters (utm_*, gclid, fbclid, ...) ignored; every other query parameter and the
  path (case-sensitive) are kept. Websites must match exactly after this: no "similar".

The canonical value per field is taken from --canonical-source (recommended:
the owner-confirmed master record), otherwise the most common normalized value.
The script never decides which value is *true*: the business owner confirms that.

Usage:
  python nap_check.py nap.csv --country EG --canonical-source "Owner master"
  python nap_check.py nap.csv --country SA --out-md nap-report.md --out-csv nap-matrix.csv
Stdlib only.
"""
from __future__ import annotations

import argparse
import csv
import io
import os
import re
import sys
from collections import Counter, defaultdict
from difflib import SequenceMatcher
from urllib.parse import parse_qsl, unquote, urlencode, urlsplit

sys.dont_write_bytecode = True  # never write __pycache__ into the skill's scripts folder when importing the sibling
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from arabic_keywords import normalize_arabic  # noqa: E402

CALLING_CODES = {"EG": "20", "SA": "966", "AE": "971", "KW": "965", "QA": "974", "BH": "973",
                 "OM": "968", "JO": "962", "LB": "961", "MA": "212", "TN": "216", "DZ": "213",
                 "IQ": "964", "US": "1", "CA": "1", "GB": "44", "DE": "49", "FR": "33", "TR": "90"}
FIELDS = ["name", "address", "phone", "hours", "website"]
EXACT_FIELDS = {"phone", "website"}  # no fuzzy "similar" for these: one wrong digit or path is a real mismatch
SIMILAR = 0.85
# Countries whose national format starts with trunk prefix "0" (e.g. EG 010..., SA 05...). Verify for other markets.
TRUNK_ZERO = {"EG", "SA", "AE", "JO", "LB", "MA", "DZ", "IQ", "GB", "DE", "FR", "TR"}
# Closed numbering plans: national numbers are dialled without a trunk prefix (8 digits).
CLOSED_PLAN = {"KW", "QA", "BH", "OM", "TN"}
TRACKING_PARAMS = {"gclid", "fbclid", "msclkid", "gbraid", "wbraid", "dclid", "yclid", "_ga", "mc_cid",
                   "mc_eid", "igshid", "srsltid"}


def norm_phone(value: str, country: str | None) -> str:
    raw = (value or "").strip()
    digits = re.sub(r"\D", "", normalize_arabic(raw))
    if not digits:
        return ""
    intl = raw.startswith("+")
    if not intl and digits.startswith("00"):
        intl, digits = True, digits[2:]
    if intl:
        return "+" + digits
    c = (country or "").upper()
    cc = CALLING_CODES.get(c)
    if cc and c in TRUNK_ZERO and digits.startswith("0") and len(digits) > 1:
        return "+" + cc + digits[1:]
    if cc and c in CLOSED_PLAN and len(digits) == 8:
        return "+" + cc + digits
    # No safe inference (no country, unknown plan, short hotline such as 19xxx): compare as written.
    return digits


def norm_website(value: str) -> str:
    v = (value or "").strip()
    if not v:
        return ""
    if not re.match(r"^[a-z][a-z0-9+.-]*://", v, re.I):
        v = "http://" + v
    p = urlsplit(v)
    host = (p.hostname or "").lower()
    if host.startswith("www."):
        host = host[4:]
    try:
        port = f":{p.port}" if p.port and p.port not in (80, 443) else ""
    except ValueError:
        port = ""
    path = unquote(p.path).rstrip("/")
    query = [(k, val) for k, val in parse_qsl(p.query, keep_blank_values=True)
             if not (k.lower().startswith("utm_") or k.lower() in TRACKING_PARAMS)]
    query.sort()
    return host + port + path + ("?" + urlencode(query) if query else "")


def norm_text(value: str) -> str:
    return normalize_arabic(value or "", "aggressive")


# --- phones: a cell may hold several numbers -------------------------------------------------
_PHONE_SPLIT = re.compile(r"\s*(?:/|,|;|\||،|&|\n|\bor\b|\sأو\s|\sاو\s|\sو\s)\s*", re.I)


def split_phones(value: str):
    """Split on list separators only if every part looks like a full number (>= 5 digits)."""
    raw = (value or "").strip()
    parts = [p for p in _PHONE_SPLIT.split(raw) if p and p.strip()]
    digits = lambda p: len(re.sub(r"\D", "", normalize_arabic(p)))  # noqa: E731
    if len(parts) > 1 and all(digits(p) >= 5 for p in parts):
        return parts
    return [raw]


def phone_key(value: str, country: str | None) -> str:
    nums = sorted({norm_phone(p, country) for p in split_phones(value)} - {""})
    return "|".join(nums)


# --- opening hours ------------------------------------------------------------------------
_AR_MARKS = re.compile(r"[ؐ-ًؚ-ٰٟـ]")
_HOUR_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789")
_TIME = r"(\d{1,2})(?:[:.](\d{2}))?\s*(a\.?m\.?|p\.?m\.?|صباحا|ص|مساءا|مساء|م)?(?![\w])"
_RANGE = re.compile(_TIME + r"\s*(?:-|–|—|~|\bto\b|\btill\b|\buntil\b|إلى|الى|حتى|لحد|لغاية)\s*" + _TIME, re.I)
_NEUTRAL = re.compile(r"\b(daily|every\s*day|everyday|from|open|and)\b|يوميا|كل يوم|مفتوح|من|و|[,;؛/&،\s]", re.I)
_ALWAYS_OPEN = re.compile(r"^(open\s*)?24\s*/\s*7$|^(open\s*)?24\s*(hours|hrs|h)$|^(مفتوح\s*)?24\s*(ساعة|ساعه)$"
                          r"|^(مفتوح\s*)?(طوال اليوم|على مدار الساعة)$", re.I)
_CLOSED = {"closed", "مغلق", "مغلقة", "مغلقه", "مقفول"}


def parse_hours(value: str):
    """Return a tuple of (start, end) minute ranges, ("closed",), the string "ambiguous", or None (unparseable).
    Accepts 24h and 12h times (am/pm, Arabic ص/م), Arabic-Indic digits, several ranges and neutral words such
    as 'daily' / 'يوميا'. Anything else left over (e.g. day names) makes it unparseable on purpose."""
    s = _AR_MARKS.sub("", (value or "").translate(_HOUR_DIGITS)).strip().lower()
    if not s:
        return None
    if s in _CLOSED:
        return ("closed",)
    if _ALWAYS_OPEN.match(s):
        return ((0, 1440),)
    ranges, ambiguous = [], False
    for m in _RANGE.finditer(s):
        h1, m1, s1, h2, m2, s2 = m.groups()
        h1, h2 = int(h1), int(h2)
        m1, m2 = int(m1 or 0), int(m2 or 0)
        if m1 > 59 or m2 > 59:
            return None

        def to_min(h, mm, suf):
            if suf:
                if not 1 <= h <= 12:
                    return None
                pm = suf.startswith("p") or suf in ("م", "مساء", "مساءا")
                return (h % 12 + (12 if pm else 0)) * 60 + mm
            if h > 24 or (h == 24 and mm):
                return None
            return h * 60 + mm

        a, b = to_min(h1, m1, s1), to_min(h2, m2, s2)
        if a is None or b is None:
            return None
        if (not s1 and not s2 and h1 <= 12 and h2 <= 12 and b <= a) or \
           (bool(s1) != bool(s2) and ((not s1 and h1 <= 12) or (not s2 and h2 <= 12))):
            ambiguous = True
        if b == 0 and a > 0:
            b = 1440  # closes at midnight
        ranges.append((a, b))
    if not ranges:
        return None
    if _NEUTRAL.sub("", _RANGE.sub("", s)):
        return None  # leftover text such as day names: don't guess
    return "ambiguous" if ambiguous else tuple(sorted(ranges))


def hours_key(value: str) -> str:
    p = parse_hours(value)
    if p is None:
        return norm_text(value)
    if p == "ambiguous":
        return "ambiguous:" + norm_text(value)
    return "hours:" + repr(p)


def normalizer(field: str, country: str | None):
    if field == "phone":
        return lambda v: phone_key(v, country)
    if field == "website":
        return norm_website
    if field == "hours":
        return hours_key
    return norm_text


def compare(canon_raw: str, canon_norm: str, raw: str, norm: str, fuzzy: bool = True) -> str:
    if not (raw or "").strip():
        return "missing"
    if not canon_norm:
        return "no-canonical"
    if raw.strip() == (canon_raw or "").strip():
        return "exact"
    if norm == canon_norm:
        return "format-only"
    if fuzzy and SequenceMatcher(None, norm, canon_norm).ratio() >= SIMILAR:
        return "similar"
    return "MISMATCH"


def compare_phone(canon_raw: str, canon_key: str, raw: str, key: str) -> str:
    """Set comparison so a cell listing several numbers isn't a mismatch just because it has extras."""
    if not (raw or "").strip():
        return "missing"
    if not canon_key:
        return "no-canonical"
    if raw.strip() == (canon_raw or "").strip():
        return "exact"
    c, s = set(canon_key.split("|")), set(key.split("|"))
    if s == c:
        return "format-only"
    if c < s:
        return "contains-canonical"   # all canonical numbers present, plus others: review the extras
    if c & s:
        return "partial-match"        # shares some numbers but not all: review
    return "MISMATCH"


def compare_hours(canon_raw: str, raw: str) -> str:
    if not (raw or "").strip():
        return "missing"
    if not (canon_raw or "").strip():
        return "no-canonical"
    if raw.strip() == canon_raw.strip():
        return "exact"
    pc, ps = parse_hours(canon_raw), parse_hours(raw)
    if "ambiguous" in (pc, ps):
        return "format-only" if norm_text(raw) == norm_text(canon_raw) else "review"  # ambiguous AM/PM
    if pc is not None and ps is not None:
        return "format-only" if pc == ps else "MISMATCH"
    return compare(canon_raw, norm_text(canon_raw), raw, norm_text(raw), fuzzy=True)  # unparseable: text comparison


def read_csv(path: str):
    with open(path, "rb") as fh:
        raw = fh.read()
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        encodings = ("utf-16",)  # UTF-16 only with a BOM: guessing it mis-decodes Windows-1256 files
    else:
        encodings = ("utf-8-sig", "cp1256")
    for enc in encodings:
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        text = raw.decode("latin-1")
    reader = csv.DictReader(io.StringIO(text))
    rows = [{(k or "").strip().lower(): (v or "").strip() for k, v in r.items()} for r in reader]
    missing = [c for c in ("source", "name", "address", "phone") if c not in (reader.fieldnames and [f.strip().lower() for f in reader.fieldnames] or [])]
    if missing:
        sys.exit(f"Missing required columns: {missing}. Found: {reader.fieldnames}")
    return rows


def analyse(rows, country, canonical_source):
    by_loc = defaultdict(list)
    for r in rows:
        by_loc[r.get("location_id") or "(single location)"].append(r)
    results = []
    present_fields = [f for f in FIELDS if any(r.get(f) for r in rows)]
    for loc, items in by_loc.items():
        canon = {}
        canon_row = next((r for r in items if canonical_source and r["source"].lower() == canonical_source.lower()), None)
        for f in present_fields:
            n = normalizer(f, country)
            if canon_row and canon_row.get(f):
                canon[f] = (canon_row[f], n(canon_row[f]), f"from '{canon_row['source']}'")
            else:
                vals = [(r.get(f), n(r.get(f))) for r in items if r.get(f)]
                if not vals:
                    canon[f] = ("", "", "no value in any source")
                    continue
                common_norm, cnt = Counter(v[1] for v in vals).most_common(1)[0]
                raw = next(v[0] for v in vals if v[1] == common_norm)
                basis = f"most common ({cnt}/{len(vals)} sources)"
                if cnt == 1 and len(vals) > 1:
                    basis += " - NO MAJORITY, owner must confirm"
                canon[f] = (raw, common_norm, basis)
        for r in items:
            row = {"location_id": loc, "source": r["source"]}
            for f in present_fields:
                n = normalizer(f, country)
                if f == "phone":
                    row[f] = compare_phone(canon[f][0], canon[f][1], r.get(f, ""), n(r.get(f, "")))
                elif f == "hours":
                    row[f] = compare_hours(canon[f][0], r.get(f, ""))
                else:
                    row[f] = compare(canon[f][0], canon[f][1], r.get(f, ""), n(r.get(f, "")), fuzzy=f not in EXACT_FIELDS)
                row[f + "_value"] = r.get(f, "")
            results.append(row)
        results.append({"location_id": loc, "source": "__canonical__", **{f + "_value": canon[f][0] for f in present_fields},
                        **{f: canon[f][2] for f in present_fields}})
    return results, present_fields


def to_markdown(results, fields, country, canonical_source):
    lines = ["# NAP consistency check", "",
             f"- Country code normalization: {country or 'none'}",
             f"- Canonical basis: {'source ' + repr(canonical_source) if canonical_source else 'most common normalized value per field'}",
             "- Status legend: exact = identical text; format-only = same after normalization (cosmetic); "
             "similar = close but different, name/address/hours only (review); MISMATCH = different value "
             "(phone and website must match exactly after normalization, so one wrong digit or path is a MISMATCH); "
             "missing = field empty in this source. "
             "Review statuses (shown, not counted as hard mismatches): contains-canonical = the cell lists every "
             "canonical phone number plus others (check the extras); partial-match = the cell shares some canonical "
             "numbers but not all; review = opening hours with ambiguous AM/PM (e.g. '9-5') that can't be compared "
             "safely. Hours are compared as times when both sides parse (e.g. 11:00-22:00 = 11 AM-10 PM); "
             "schedules with day names are compared as text.",
             "- The canonical value is a comparison basis, not proof of truth. The business owner confirms the correct NAP.", ""]
    locs = OrderedSet(r["location_id"] for r in results)
    mismatch_total = 0
    for loc in locs:
        lines.append(f"## Location: {loc}")
        canon = next(r for r in results if r["location_id"] == loc and r["source"] == "__canonical__")
        lines.append("")
        lines.append("| Field | Canonical value | Basis |")
        lines.append("|---|---|---|")
        for f in fields:
            lines.append(f"| {f} | {canon.get(f + '_value', '')} | {canon.get(f, '')} |")
        lines.append("")
        lines.append("| Source | " + " | ".join(fields) + " |")
        lines.append("|---|" + "---|" * len(fields))
        for r in results:
            if r["location_id"] != loc or r["source"] == "__canonical__":
                continue
            cells = []
            for f in fields:
                s = r[f]
                if s in ("MISMATCH", "similar", "contains-canonical", "partial-match", "review"):
                    mismatch_total += 1 if s == "MISMATCH" else 0
                    cells.append(f"**{s}**: {r[f + '_value']}")
                else:
                    cells.append(s)
            lines.append(f"| {r['source']} | " + " | ".join(cells) + " |")
        lines.append("")
    lines.insert(2, f"- Hard mismatches found: {mismatch_total}")
    return "\n".join(lines)


def OrderedSet(it):
    seen, out = set(), []
    for x in it:
        if x not in seen:
            seen.add(x)
            out.append(x)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="CSV with source,name,address,phone[,hours,website,location_id]")
    ap.add_argument("--country", help="ISO country code for phone normalization, e.g. EG, SA, AE")
    ap.add_argument("--canonical-source", help="source name holding the owner-confirmed master record")
    ap.add_argument("--out-md", help="Markdown report path (default: stdout)")
    ap.add_argument("--out-csv", help="matrix CSV path")
    args = ap.parse_args(argv)

    rows = read_csv(args.input)
    results, fields = analyse(rows, args.country, args.canonical_source)
    md = to_markdown(results, fields, args.country, args.canonical_source)
    if args.out_md:
        with open(args.out_md, "w", encoding="utf-8") as fh:
            fh.write(md + "\n")
        print(f"Report written: {args.out_md}")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(md)
    if args.out_csv:
        cols = ["location_id", "source"] + [c for f in fields for c in (f, f + "_value")]
        with open(args.out_csv, "w", newline="", encoding="utf-8-sig") as fh:
            w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
            w.writeheader()
            w.writerows(results)
        print(f"Matrix written: {args.out_csv}")


if __name__ == "__main__":
    main()
