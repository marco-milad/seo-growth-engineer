#!/usr/bin/env python3
"""Normalize and group Arabic (and mixed Arabic/Latin) keyword variants.

Arabic search queries for the same intent appear in many spellings: different
hamza/alef forms, ta marbuta vs ha, alef maqsura vs ya, diacritics, tatweel,
Arabic-Indic vs Western digits, with or without the definite article. Without
normalization these look like separate keywords and inflate topic counts.

This script groups variants deterministically. It does NOT invent search volume:
if the input has a volume column it is carried through and summed per group,
and the source of that volume should be stated in the report.

Usage:
  python arabic_keywords.py keywords.txt                       # one keyword per line
  python arabic_keywords.py export.csv --column Keyword --volume-column Volume
  python arabic_keywords.py export.csv --column Keyword --level aggressive --out groups.csv

Also importable: from arabic_keywords import normalize_arabic, detect_script
Stdlib only.
"""
from __future__ import annotations

import argparse
import csv
import io
import re
import sys
import unicodedata
from collections import OrderedDict

# --- normalization tables -------------------------------------------------

_DIACRITICS = re.compile(r"[ؐ-ًؚ-ٰٟۖ-ۭ]")
_TATWEEL = "ـ"
_ALEF_FORMS = str.maketrans({"أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا"})
_STANDARD_MAP = str.maketrans({
    "ى": "ي",  # alef maqsura -> ya
    "ة": "ه",  # ta marbuta -> ha
    "ک": "ك",  # Persian kaf -> Arabic kaf
    "ی": "ي",  # Persian ya -> Arabic ya
})
_AGGRESSIVE_MAP = str.maketrans({
    "ؤ": "و",  # waw with hamza -> waw
    "ئ": "ي",  # ya with hamza -> ya
    "ء": "",        # standalone hamza removed
})
_DIGITS = str.maketrans("٠١٢٣٤٥٦٧٨٩۰۱۲۳۴۵۶۷۸۹", "01234567890123456789")
_PUNCT = re.compile(r"[،؛؟٪-٭.,;:!?\"'()\[\]{}<>«»/\\|+*=_~`^%$#@&-]+")
_ARABIC_CHAR = re.compile(r"[؀-ۿݐ-ݿࢠ-ࣿ]")
_LATIN_CHAR = re.compile(r"[A-Za-z]")
# Arabizi / Franco-Arabic: Latin words that use digits for Arabic letters (2,3,5,6,7,8,9).
# A digit counts only when it LEADS a word followed by >= 2 letters (7aga, 3arabia) or sits BETWEEN letters
# with >= 3 letters around it (ma3a, sa7eb). A trailing digit never counts, so product/tech tokens such as
# ps5, mp3, 3d, 5g, b2b, h2o aren't flagged. Trade-off: end-digit words like "sa7" are missed; "7up"/"mp3s"
# may still be flagged.
_TOKEN = re.compile(r"[A-Za-z0-9']+")
_ARABIZI_LEAD = re.compile(r"^[2356789]+[A-Za-z']{2,}")
_ARABIZI_MID = re.compile(r"([A-Za-z']+)[2356789]+([A-Za-z']+)")


def _is_arabizi_token(tok: str) -> bool:
    if _ARABIZI_LEAD.match(tok):
        return True
    return any(len(m.group(1)) + len(m.group(2)) >= 3 for m in _ARABIZI_MID.finditer(tok))


def normalize_arabic(text: str, level: str = "standard") -> str:
    """Return a comparison key for `text`.

    level="standard": diacritics, tatweel, alef forms, alef maqsura->ya,
        ta marbuta->ha, Persian kaf/ya, digits -> ASCII, punctuation -> space,
        Latin lowercased, whitespace collapsed.
    level="aggressive": standard + hamza carriers flattened and the Arabic
        definite article "ال" stripped from words longer than 3 letters.
    The key is for grouping only; never publish the normalized form.
    """
    if text is None:
        return ""
    t = unicodedata.normalize("NFKC", str(text))
    t = _DIACRITICS.sub("", t).replace(_TATWEEL, "")
    t = t.translate(_ALEF_FORMS).translate(_STANDARD_MAP).translate(_DIGITS)
    if level == "aggressive":
        t = t.translate(_AGGRESSIVE_MAP)
    t = _PUNCT.sub(" ", t).lower()
    words = t.split()
    if level == "aggressive":
        words = [w[2:] if w.startswith("ال") and len(w) > 4 else w for w in words]
        # also "وال" / "بال" / "لل" prefixes are left alone on purpose: too ambiguous
    return " ".join(words)


def detect_script(text: str) -> str:
    """Classify a keyword as arabic, latin, arabizi (likely), mixed or other."""
    has_ar = bool(_ARABIC_CHAR.search(text or ""))
    has_lat = bool(_LATIN_CHAR.search(text or ""))
    if has_ar and has_lat:
        return "mixed"
    if has_ar:
        return "arabic"
    if has_lat:
        return "arabizi-likely" if any(_is_arabizi_token(t) for t in _TOKEN.findall(text)) else "latin"
    return "other"


# --- IO ----------------------------------------------------------------------

def _read_rows(path: str, column: str | None, volume_column: str | None):
    with open(path, "rb") as fh:
        raw = fh.read()
    # UTF-16 only with a BOM: trying it blindly mis-decodes Windows-1256 (Arabic Excel) files as garbage.
    encodings = ("utf-16", "latin-1") if raw.startswith((b"\xff\xfe", b"\xfe\xff")) else ("utf-8-sig", "cp1256", "latin-1")
    for enc in encodings:
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    is_csv = path.lower().endswith((".csv", ".tsv")) or column is not None
    if not is_csv:
        for line in text.splitlines():
            if line.strip():
                yield line.strip(), None
        return
    dialect = "excel-tab" if path.lower().endswith(".tsv") or ("\t" in text.splitlines()[0] and "," not in text.splitlines()[0]) else "excel"
    reader = csv.DictReader(io.StringIO(text), dialect=dialect)
    fields = reader.fieldnames or []
    col = column or next((f for f in fields if f.strip().lower() in {"keyword", "query", "top queries", "queries", "الكلمة", "كلمة"}), fields[0] if fields else None)
    if col not in fields:
        sys.exit(f"Column '{col}' not found. Available: {fields}")
    if volume_column and volume_column not in fields:
        sys.exit(f"Volume column '{volume_column}' not found. Available: {fields}")
    for row in reader:
        kw = (row.get(col) or "").strip()
        if not kw:
            continue
        vol = None
        if volume_column:
            v = (row.get(volume_column) or "").replace(",", "").strip()
            try:
                vol = float(v) if v else None
            except ValueError:
                vol = None
        yield kw, vol


def group_keywords(rows, level: str):
    groups: "OrderedDict[str, dict]" = OrderedDict()
    for kw, vol in rows:
        key = normalize_arabic(kw, level)
        if not key:
            continue
        g = groups.setdefault(key, {"variants": OrderedDict(), "volume": None, "has_volume": False})
        g["variants"].setdefault(kw, 0.0)
        if vol is not None:
            g["variants"][kw] += vol
            g["volume"] = (g["volume"] or 0.0) + vol
            g["has_volume"] = True
    out = []
    for key, g in groups.items():
        variants = list(g["variants"].items())
        if g["has_volume"]:
            representative = max(variants, key=lambda kv: kv[1])[0]
        else:
            representative = variants[0][0]
        out.append({
            "group_key": key,
            "representative": representative,
            "variant_count": len(variants),
            "variants": " | ".join(v for v, _ in variants),
            "script": detect_script(representative),
            "total_volume": "" if not g["has_volume"] else (int(g["volume"]) if g["volume"].is_integer() else round(g["volume"], 2)),
        })
    out.sort(key=lambda r: (-(r["total_volume"] or 0) if r["total_volume"] != "" else 0, -r["variant_count"], r["group_key"]))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="TXT (one keyword per line) or CSV/TSV export")
    ap.add_argument("--column", help="keyword column name in CSV (auto-detected if omitted)")
    ap.add_argument("--volume-column", help="optional volume column to carry through (state its source in reports)")
    ap.add_argument("--level", choices=["standard", "aggressive"], default="standard")
    ap.add_argument("--out", help="write groups CSV here (default: print to stdout)")
    ap.add_argument("--only-multi", action="store_true", help="only output groups with 2+ variants")
    args = ap.parse_args(argv)

    groups = group_keywords(_read_rows(args.input, args.column, args.volume_column), args.level)
    if args.only_multi:
        groups = [g for g in groups if g["variant_count"] > 1]
    fields = ["group_key", "representative", "variant_count", "variants", "script", "total_volume"]
    if args.out:
        with open(args.out, "w", newline="", encoding="utf-8-sig") as fh:
            w = csv.DictWriter(fh, fieldnames=fields)
            w.writeheader()
            w.writerows(groups)
        total_in = sum(g["variant_count"] for g in groups)
        print(f"{total_in} keywords -> {len(groups)} groups ({args.level}). Written: {args.out}")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        w = csv.DictWriter(sys.stdout, fieldnames=fields)
        w.writeheader()
        w.writerows(groups)


if __name__ == "__main__":
    main()
