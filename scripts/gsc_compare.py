#!/usr/bin/env python3
"""Compare two Google Search Console performance exports (previous vs current period).

Accepted inputs (CSV exported from the Search Console Performance report, or from the API):
  A) two files:   --previous Queries_prev.csv --current Queries_curr.csv
  B) one comparison export (date-range "Compare" mode), with paired columns such as
     "Last 28 days Clicks" / "Previous 28 days Clicks":
                  --compare-file Queries.csv [--current-prefix "Last 28 days" --previous-prefix "Previous 28 days"]
The first column (or one named Top queries / Query / Top pages / Page / Country / Device) is the key.

Outputs: totals of the exported rows, top gainers/losers by clicks, new/lost keys,
position movers, and CTR outliers (rows with many impressions whose CTR is low compared to
other rows *in the same export* at a similar position). No external CTR benchmarks are used.

Important caveats printed in every report:
- Exported rows exclude anonymized queries and are capped (UI export ~1,000 rows), so row
  totals are lower than the property totals shown in the Search Console chart.
- CTR is recomputed from clicks/impressions; position is the impression-weighted average
  reported by Google, compared only for rows with enough impressions in both periods.
- A change is a correlation with whatever happened in the period, not proof of cause.

Usage:
  python gsc_compare.py --previous prev.csv --current curr.csv --out-md compare.md --out-csv compare.csv
  python gsc_compare.py --compare-file Queries.csv --min-impressions 50 --top 25

Exports in another interface language (e.g. Arabic) or with unusual headers: map the columns explicitly.
Each value is a header name or a 1-based column number (numbers avoid typing Arabic in a Windows shell):
  --previous p.csv --current c.csv --columns "key=1,clicks=2,impressions=3,position=5"
  --compare-file q.csv --columns "key=1,clicks.current=2,clicks.previous=3,impressions.current=4,impressions.previous=5"
Without --columns, English headers are detected automatically (unchanged behaviour). No column meaning is
guessed: unknown headers must be mapped.

Reading: UTF-8 (with or without BOM); UTF-16 only when the file has a UTF-16 BOM; otherwise Windows-1256
(Arabic Excel "CSV"). A non-UTF-8 encoding is reported on stderr. Delimiter: comma, tab or semicolon,
detected from the header line. Numbers may use Arabic-Indic digits, the Arabic decimal mark (٫) and
percent sign (٪).
Stdlib only.
"""
from __future__ import annotations

import argparse
import csv
import io
import re
import statistics
import sys

KEY_NAMES = {"top queries", "query", "queries", "top pages", "page", "pages", "country", "device",
             "search appearance", "date"}
METRICS = ("clicks", "impressions", "ctr", "position")


def _num(v):
    s = str(v or "").strip().replace(",", "").replace("٬", "").replace("٫", ".").replace("٪", "%")
    if not s or s in {"-", "—"}:
        return None
    pct = s.endswith("%")
    s = s.rstrip("%")
    try:
        n = float(s)
    except ValueError:
        return None
    return n / 100 if pct else n


def _read(path):
    with open(path, "rb") as fh:
        raw = fh.read()
    # UTF-16 only with a BOM: trying it blindly mis-decodes Windows-1256 (Arabic Excel) files as garbage.
    encodings = ("utf-16",) if raw.startswith((b"\xff\xfe", b"\xfe\xff")) else ("utf-8-sig", "cp1256")
    used = "latin-1"
    for enc in encodings:
        try:
            text = raw.decode(enc)
            used = enc
            break
        except UnicodeDecodeError:
            continue
    else:
        text = raw.decode("latin-1")
    if used != "utf-8-sig":
        print(f"note: {path} read as {used}", file=sys.stderr)
    first = text.splitlines()[0] if text else ""
    tabs, commas, semis = first.count("\t"), first.count(","), first.count(";")
    if "\t" in first and tabs >= commas and tabs >= semis:
        dialect = "excel-tab"
    elif semis > commas:
        dialect = _Semicolon
    else:
        dialect = "excel"
    reader = csv.DictReader(io.StringIO(text), dialect=dialect)
    return [h.strip() for h in reader.fieldnames or []], [{(k or "").strip(): v for k, v in r.items()} for r in reader]


class _Semicolon(csv.excel):
    delimiter = ";"


# --- explicit column mapping (--columns) -------------------------------------------------
TWO_FILE_KEYS = ("key", "clicks", "impressions", "ctr", "position")
COMPARE_KEYS = ("key",) + tuple(f"{m}.{p}" for m in ("clicks", "impressions", "ctr", "position")
                                 for p in ("current", "previous"))


def _numbered(header):
    return ", ".join(f"{i}: {h!r}" for i, h in enumerate(header, 1))


def _fail(msg, code=2):
    print(f"ERROR: {msg}", file=sys.stderr)
    sys.exit(code)


def parse_columns(spec, header, allowed, required, label):
    """Resolve 'name=value' pairs, where value is a header name or a 1-based column number, against header."""
    mapping, used = {}, {}
    for part in [p.strip() for p in (spec or "").split(",") if p.strip()]:
        if "=" not in part:
            _fail(f"--columns entry {part!r} must look like name=value. Allowed names: {', '.join(allowed)}")
        name, value = (x.strip() for x in part.split("=", 1))
        name = name.lower()
        if name not in allowed:
            _fail(f"--columns: unknown name {name!r}. Allowed: {', '.join(allowed)}")
        if name in mapping:
            _fail(f"--columns: {name!r} is mapped twice")
        if value.isdigit():
            idx = int(value)
            if not 1 <= idx <= len(header):
                _fail(f"--columns: {name}={idx} is out of range for {label} (it has {len(header)} columns: {_numbered(header)})")
            col = header[idx - 1]
        else:
            exact = [h for h in header if h == value]
            loose = [h for h in header if h.casefold() == value.casefold()]
            if exact:
                col = exact[0]
            elif len(loose) == 1:
                col = loose[0]
            else:
                _fail(f"--columns: no column {value!r} in {label}. Columns: {_numbered(header)}")
        if col in used:
            _fail(f"--columns: column {col!r} is mapped to both {used[col]!r} and {name!r}")
        mapping[name], used[col] = col, name
    missing = [r for r in required if r not in mapping]
    if missing:
        _fail(f"--columns is missing {', '.join(missing)} for {label}. Columns: {_numbered(header)}")
    return mapping


def _check_numeric(rows, col, name, label):
    if not any(_num(r.get(col)) is not None for r in rows):
        _fail(f"--columns: {name} -> {col!r} in {label} has no numeric values; check the mapping")


def load_mapped(args):
    if args.compare_file:
        header, rows = _read(args.compare_file)
        m = parse_columns(args.columns, header, COMPARE_KEYS,
                          ("key", "clicks.current", "clicks.previous", "impressions.current", "impressions.previous"),
                          args.compare_file)
        for k in ("clicks.current", "clicks.previous", "impressions.current", "impressions.previous"):
            _check_numeric(rows, m[k], k, args.compare_file)
        cols = lambda p: {met: m[f"{met}.{p}"] for met in ("clicks", "impressions", "position") if f"{met}.{p}" in m}  # noqa: E731
        return m["key"], _rows_to_map(rows, m["key"], cols("previous")), _rows_to_map(rows, m["key"], cols("current")), \
            args.previous_prefix or "previous", args.current_prefix or "current"
    if not (args.previous and args.current):
        _fail("Provide --previous and --current, or --compare-file.")
    out = []
    for label in (args.previous, args.current):
        header, rows = _read(label)
        m = parse_columns(args.columns, header, TWO_FILE_KEYS, ("key", "clicks", "impressions"), label)
        for k in ("clicks", "impressions"):
            _check_numeric(rows, m[k], k, label)
        out.append((m["key"], rows, {met: m[met] for met in ("clicks", "impressions", "position") if met in m}))
    (kp, rp, cp), (kc, rc, cc) = out
    return kc, _rows_to_map(rp, kp, cp), _rows_to_map(rc, kc, cc), "previous", "current"


def _key_col(header):
    for h in header:
        if h.lower() in KEY_NAMES:
            return h
    return header[0]


def _metric_cols(header, prefix=""):
    found = {}
    for m in METRICS:
        for h in header:
            hl = h.lower()
            if prefix and not hl.startswith(prefix.lower()):
                continue
            if hl == m or hl.endswith(" " + m) or (m == "ctr" and hl.endswith("ctr")):
                found[m] = h
                break
    return found


def _rows_to_map(rows, key, cols):
    out = {}
    for r in rows:
        k = (r.get(key) or "").strip()
        if not k:
            continue
        clicks = _num(r.get(cols.get("clicks"))) or 0.0
        impr = _num(r.get(cols.get("impressions"))) or 0.0
        pos = _num(r.get(cols.get("position"))) if cols.get("position") else None
        out[k] = {"clicks": clicks, "impressions": impr, "position": pos}
    return out


def detect_prefixes(header):
    prefixes = []
    for h in header:
        m = re.match(r"^(.*?)\s*(clicks)$", h, re.I)
        if m and m.group(1).strip():
            prefixes.append(m.group(1).strip())
    return prefixes


def load(args):
    if getattr(args, "columns", None):
        return load_mapped(args)
    if args.compare_file:
        header, rows = _read(args.compare_file)
        key = _key_col(header)
        prefixes = detect_prefixes(header)
        cur, prev = args.current_prefix, args.previous_prefix
        if not (cur and prev):
            if len(prefixes) == 2:
                guess_cur = next((p for p in prefixes if p.lower().startswith(("last", "current"))), None)
                guess_prev = next((p for p in prefixes if p.lower().startswith(("previous", "prior"))), None)
                if guess_cur and guess_prev:
                    cur, prev = guess_cur, guess_prev
            if not (cur and prev):
                sys.exit(f"Could not tell which columns are current vs previous. Detected prefixes: {prefixes}. "
                         f"Pass --current-prefix and --previous-prefix.")
        cc, pc = _metric_cols(header, cur), _metric_cols(header, prev)
        if "clicks" not in cc or "clicks" not in pc:
            sys.exit(f"Clicks columns not found for prefixes '{cur}' / '{prev}'. Header: {header}")
        return key, _rows_to_map(rows, key, pc), _rows_to_map(rows, key, cc), prev, cur
    if not (args.previous and args.current):
        sys.exit("Provide --previous and --current, or --compare-file.")
    hp, rp = _read(args.previous)
    hc, rc = _read(args.current)
    kp, kc = _key_col(hp), _key_col(hc)
    pcols, ccols = _metric_cols(hp), _metric_cols(hc)
    for name, cols, h in (("previous", pcols, hp), ("current", ccols, hc)):
        if "clicks" not in cols or "impressions" not in cols:
            sys.exit(f"{name} file needs Clicks and Impressions columns. Header: {h}")
    return kc, _rows_to_map(rp, kp, pcols), _rows_to_map(rc, kc, ccols), "previous", "current"


def ctr(c, i):
    return c / i if i else 0.0


def pos_bucket(p):
    if p is None:
        return None
    if p <= 3:
        return "1-3"
    if p <= 10:
        return "4-10"
    if p <= 20:
        return "11-20"
    return "21+"


def analyse(prev, cur, min_impr, top):
    keys = set(prev) | set(cur)
    rows = []
    for k in keys:
        p = prev.get(k, {"clicks": 0.0, "impressions": 0.0, "position": None})
        c = cur.get(k, {"clicks": 0.0, "impressions": 0.0, "position": None})
        status = "new" if k not in prev else "lost" if k not in cur else "both"
        dpos = None
        if p["position"] is not None and c["position"] is not None and p["impressions"] >= min_impr and c["impressions"] >= min_impr:
            dpos = round(c["position"] - p["position"], 2)
        rows.append({
            "key": k, "status": status,
            "clicks_prev": p["clicks"], "clicks_curr": c["clicks"], "clicks_delta": c["clicks"] - p["clicks"],
            "impr_prev": p["impressions"], "impr_curr": c["impressions"], "impr_delta": c["impressions"] - p["impressions"],
            "ctr_prev": round(ctr(p["clicks"], p["impressions"]), 4), "ctr_curr": round(ctr(c["clicks"], c["impressions"]), 4),
            "pos_prev": p["position"], "pos_curr": c["position"], "pos_delta": dpos,
        })
    # CTR outliers in current period, within position bucket, relative to the export's own median
    by_bucket = {}
    for r in rows:
        b = pos_bucket(r["pos_curr"])
        if b and r["impr_curr"] >= min_impr:
            by_bucket.setdefault(b, []).append(r)
    outliers = []
    medians = {}
    for b, items in by_bucket.items():
        if len(items) < 5:
            continue
        med = statistics.median(i["ctr_curr"] for i in items)
        medians[b] = med
        for i in items:
            if med > 0 and i["ctr_curr"] < med * 0.5:
                outliers.append({**i, "bucket": b, "bucket_median_ctr": round(med, 4)})
    outliers.sort(key=lambda r: -r["impr_curr"])
    tot = {
        "clicks_prev": sum(r["clicks_prev"] for r in rows), "clicks_curr": sum(r["clicks_curr"] for r in rows),
        "impr_prev": sum(r["impr_prev"] for r in rows), "impr_curr": sum(r["impr_curr"] for r in rows),
        "rows_prev": len(prev), "rows_curr": len(cur),
    }
    tot["ctr_prev"] = ctr(tot["clicks_prev"], tot["impr_prev"])
    tot["ctr_curr"] = ctr(tot["clicks_curr"], tot["impr_curr"])
    return {
        "rows": rows, "totals": tot, "medians": medians,
        "gainers": sorted([r for r in rows if r["clicks_delta"] > 0], key=lambda r: -r["clicks_delta"])[:top],
        "losers": sorted([r for r in rows if r["clicks_delta"] < 0], key=lambda r: r["clicks_delta"])[:top],
        "new": sorted([r for r in rows if r["status"] == "new"], key=lambda r: -r["impr_curr"])[:top],
        "lost": sorted([r for r in rows if r["status"] == "lost"], key=lambda r: -r["impr_prev"])[:top],
        "pos_up": sorted([r for r in rows if r["pos_delta"] is not None and r["pos_delta"] < 0], key=lambda r: r["pos_delta"])[:top],
        "pos_down": sorted([r for r in rows if r["pos_delta"] is not None and r["pos_delta"] > 0], key=lambda r: -r["pos_delta"])[:top],
        "ctr_outliers": outliers[:top],
    }


def _pct(a, b):
    if not a:
        return "n/a" if b else "0%"
    return f"{(b - a) / a * 100:+.1f}%"


def _f(n, d=0):
    if n is None:
        return "-"
    return f"{n:,.{d}f}"


def to_md(res, label_prev, label_cur, key_name, min_impr, args):
    t = res["totals"]
    L = [f"# Search Console comparison: {label_prev} vs {label_cur}", "",
         f"Key: **{key_name}** · rows: {t['rows_prev']} -> {t['rows_curr']} · min impressions for position/CTR checks: {min_impr}", ""]
    if args.days_previous and args.days_current and args.days_previous != args.days_current:
        L += [f"> WARNING: unequal period lengths ({args.days_previous} vs {args.days_current} days). Totals are not comparable.", ""]
    L += ["## Caveats", "",
          "- Totals below are sums of exported rows only. They exclude anonymized queries and rows beyond the export limit, "
          "so they are lower than the property totals in the Search Console chart. Use the chart totals for headline numbers.",
          "- Check seasonality (compare year-over-year if possible), tracking or site changes, and known Google updates in both periods before attributing a change.",
          "- Movement shows correlation with events in the period, not proof of cause.", "",
          "## Totals of exported rows", "",
          "| Metric | Previous | Current | Change |", "|---|---|---|---|",
          f"| Clicks | {_f(t['clicks_prev'])} | {_f(t['clicks_curr'])} | {_pct(t['clicks_prev'], t['clicks_curr'])} |",
          f"| Impressions | {_f(t['impr_prev'])} | {_f(t['impr_curr'])} | {_pct(t['impr_prev'], t['impr_curr'])} |",
          f"| CTR (recomputed) | {t['ctr_prev']*100:.2f}% | {t['ctr_curr']*100:.2f}% | {(t['ctr_curr']-t['ctr_prev'])*100:+.2f} pp |", ""]

    def table(title, items, cols):
        nonlocal L
        L += [f"## {title}", ""]
        if not items:
            L += ["None.", ""]
            return
        L.append("| " + " | ".join(c[0] for c in cols) + " |")
        L.append("|" + "---|" * len(cols))
        for r in items:
            L.append("| " + " | ".join(str(c[1](r)).replace("|", "/") for c in cols) + " |")
        L.append("")

    base = [(key_name, lambda r: r["key"]),
            ("Clicks prev", lambda r: _f(r["clicks_prev"])), ("Clicks curr", lambda r: _f(r["clicks_curr"])),
            ("Δ clicks", lambda r: f"{r['clicks_delta']:+,.0f}"),
            ("Impr prev", lambda r: _f(r["impr_prev"])), ("Impr curr", lambda r: _f(r["impr_curr"])),
            ("Pos prev", lambda r: _f(r["pos_prev"], 1)), ("Pos curr", lambda r: _f(r["pos_curr"], 1))]
    table("Top gainers (clicks)", res["gainers"], base)
    table("Top losers (clicks)", res["losers"], base)
    table("New in current period", res["new"], base)
    table("Lost (absent from current export)", res["lost"], base)
    pos = base[:1] + [("Impr curr", lambda r: _f(r["impr_curr"])), ("Pos prev", lambda r: _f(r["pos_prev"], 1)),
                      ("Pos curr", lambda r: _f(r["pos_curr"], 1)), ("Δ pos (neg = better)", lambda r: f"{r['pos_delta']:+.1f}")]
    table("Biggest position improvements", res["pos_up"], pos)
    table("Biggest position declines", res["pos_down"], pos)
    table("CTR outliers (snippet/title opportunities)", res["ctr_outliers"], base[:1] + [
        ("Impr curr", lambda r: _f(r["impr_curr"])), ("Pos curr", lambda r: _f(r["pos_curr"], 1)),
        ("CTR curr", lambda r: f"{r['ctr_curr']*100:.2f}%"), ("Median CTR in bucket", lambda r: f"{r['bucket_median_ctr']*100:.2f}% ({r['bucket']})")])
    L += ["CTR outliers = CTR below half the median CTR of rows at a similar position in this same export. "
          "They are candidates to review (title, snippet, intent match, SERP features), not confirmed problems.", ""]
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--previous")
    ap.add_argument("--current")
    ap.add_argument("--compare-file")
    ap.add_argument("--current-prefix")
    ap.add_argument("--previous-prefix")
    ap.add_argument("--min-impressions", type=float, default=20)
    ap.add_argument("--top", type=int, default=20)
    ap.add_argument("--days-previous", type=int, help="length of previous period in days (for an equal-length check)")
    ap.add_argument("--days-current", type=int)
    ap.add_argument("--out-md")
    ap.add_argument("--out-csv")
    ap.add_argument("--columns", help="explicit column mapping, e.g. key=1,clicks=2,impressions=3 (names or 1-based numbers)")
    args = ap.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")  # Arabic headers in errors stay readable

    key, prev, cur, lp, lc = load(args)
    res = analyse(prev, cur, args.min_impressions, args.top)
    md = to_md(res, lp, lc, key, args.min_impressions, args)
    if args.out_md:
        with open(args.out_md, "w", encoding="utf-8") as fh:
            fh.write(md + "\n")
        print(f"Report written: {args.out_md}")
    else:
        print(md)
    if args.out_csv:
        cols = list(res["rows"][0].keys()) if res["rows"] else ["key"]
        with open(args.out_csv, "w", newline="", encoding="utf-8-sig") as fh:
            w = csv.DictWriter(fh, fieldnames=cols)
            w.writeheader()
            w.writerows(sorted(res["rows"], key=lambda r: r["clicks_delta"]))
        print(f"Row-level CSV written: {args.out_csv}")


if __name__ == "__main__":
    main()
