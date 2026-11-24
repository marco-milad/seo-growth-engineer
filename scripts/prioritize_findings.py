#!/usr/bin/env python3
"""Validate findings.csv and compute priority score, band and quick-win flag.

Implements the model defined in SKILL.md:
  priority_score = (2*impact + urgency + business_relevance) * confidence / effort
  confidence: High=1.0, Medium=0.8, Low=0.5
  bands: P1 >= 6, P2 3..<6, P3 < 3; P0 is a manual override (set priority=P0 in the CSV
         and justify it in the description) and is never computed or removed here.
  quick_win: impact >= 3 and effort <= 2 and confidence >= 0.8
  validate-first flag: confidence Low and impact >= 4

Rows in bucket "missing-data" may leave the scoring fields empty; they get priority "n/a".

Usage:
  python prioritize_findings.py findings.csv                     # validate + print ranked table
  python prioritize_findings.py findings.csv --write             # update score/priority/quick_win in place
  python prioritize_findings.py findings.csv --out scored.csv    # write the scored CSV elsewhere; input untouched
  python prioritize_findings.py findings.csv --md ranked.md      # write ranked Markdown table

Evidence safety:
  --write first copies the original to findings.csv.bak-YYYYMMDD-HHMMSS (never overwriting an existing
  backup: a collision gets -2, -3, ...), then replaces the file atomically. --out and --md refuse to
  replace an existing file unless --overwrite is given; --out may not point at the input file.
  All output paths are checked before anything is written.
Exit code 1 when validation errors exist (use --lenient to score valid rows anyway); 2 for unsafe/invalid
output options.
Stdlib only.
"""
from __future__ import annotations

import argparse
import csv
import io
import os
import re
import sys
import tempfile
import time

COLUMNS = ["id", "bucket", "domain", "title", "scope", "description", "evidence", "data_source", "data_date",
           "business_impact", "seo_impact", "impact", "urgency", "business_relevance", "effort", "confidence",
           "priority_score", "priority", "quick_win", "recommendation", "dependencies", "validation_method",
           "owner_role", "status"]
BUCKETS = {"confirmed-issue", "potential-issue", "opportunity", "missing-data", "needs-investigation"}
DOMAINS = {"ONP": "on-page", "OFF": "off-page", "TEC": "technical", "LOC": "local", "ANL": "analytics",
           "CNT": "content", "INT": "international", "AIS": "ai-search"}
STATUSES = {"open", "proposed", "approved", "in-progress", "implemented", "validated", "monitoring",
            "won't-fix", "blocked"}
CONFIDENCE = {"high": 1.0, "medium": 0.8, "low": 0.5}
ID_RE = re.compile(r"^(ONP|OFF|TEC|LOC|ANL|CNT|INT|AIS)-\d{3}$")
REQUIRED_TEXT = ["id", "bucket", "domain", "title", "scope", "description", "data_source", "data_date",
                 "recommendation", "validation_method", "status"]


def _norm_bucket(v: str) -> str:
    return re.sub(r"[\s_]+", "-", (v or "").strip().lower())


def _int_1_5(v, field, errs):
    try:
        n = int(float(str(v).strip()))
    except (TypeError, ValueError):
        errs.append(f"{field} must be an integer 1-5 (got '{v}')")
        return None
    if not 1 <= n <= 5:
        errs.append(f"{field} must be 1-5 (got {n})")
        return None
    return n


def _confidence(v, errs):
    s = str(v or "").strip().lower()
    if s in CONFIDENCE:
        return CONFIDENCE[s]
    try:
        f = float(s)
        if f in (1.0, 0.8, 0.5):
            return f
    except ValueError:
        pass
    errs.append(f"confidence must be High/Medium/Low (got '{v}')")
    return None


def band(score: float) -> str:
    if score >= 6:
        return "P1"
    if score >= 3:
        return "P2"
    return "P3"


def process(rows):
    results, all_errors, seen = [], [], set()
    for i, row in enumerate(rows, start=2):  # header is line 1
        errs = []
        r = {c: (row.get(c) or "").strip() for c in COLUMNS}
        for c in REQUIRED_TEXT:
            if not r[c]:
                errs.append(f"'{c}' is empty")
        if r["id"]:
            if not ID_RE.match(r["id"]):
                errs.append(f"id '{r['id']}' must look like TEC-001 (prefixes: {', '.join(DOMAINS)})")
            elif r["id"] in seen:
                errs.append(f"duplicate id {r['id']}")
            seen.add(r["id"])
            prefix = r["id"][:3]
            if prefix in DOMAINS and r["domain"] and r["domain"].lower() != DOMAINS[prefix]:
                errs.append(f"domain '{r['domain']}' does not match id prefix {prefix} (expected '{DOMAINS[prefix]}')")
        bucket = _norm_bucket(r["bucket"])
        if r["bucket"] and bucket not in BUCKETS:
            errs.append(f"bucket '{r['bucket']}' not in {sorted(BUCKETS)}")
        r["bucket"] = bucket or r["bucket"]
        if r["status"] and r["status"].lower() not in STATUSES:
            errs.append(f"status '{r['status']}' not in {sorted(STATUSES)}")
        if bucket in {"confirmed-issue", "potential-issue", "needs-investigation"} and not r["evidence"]:
            errs.append("evidence is required for confirmed/potential/needs-investigation findings")

        scoring_fields = [r["impact"], r["urgency"], r["business_relevance"], r["effort"], r["confidence"]]
        manual_p0 = r["priority"].upper() == "P0"
        flags = []
        if bucket == "missing-data" and not all(scoring_fields):
            r["priority_score"], r["quick_win"] = "", "no"
            r["priority"] = "P0" if manual_p0 else "n/a"
        else:
            imp = _int_1_5(r["impact"], "impact", errs)
            urg = _int_1_5(r["urgency"], "urgency", errs)
            bus = _int_1_5(r["business_relevance"], "business_relevance", errs)
            eff = _int_1_5(r["effort"], "effort", errs)
            conf = _confidence(r["confidence"], errs)
            if None not in (imp, urg, bus, eff, conf):
                score = round((2 * imp + urg + bus) * conf / eff, 2)
                r["priority_score"] = f"{score:.2f}"
                r["priority"] = "P0" if manual_p0 else band(score)
                r["quick_win"] = "yes" if (imp >= 3 and eff <= 2 and conf >= 0.8) else "no"
                if conf == 0.5 and imp >= 4:
                    flags.append("validate-first")
                if manual_p0:
                    flags.append("manual-P0")
        r["_flags"] = ",".join(flags)
        r["_line"] = i
        if errs:
            all_errors.append((i, r["id"] or "(no id)", errs))
            if not r["priority_score"]:
                r["priority"], r["quick_win"] = "invalid", "no"
        results.append(r)
    return results, all_errors


def sort_key(r):
    order = {"P0": 0, "P1": 1, "P2": 2, "P3": 3, "n/a": 4}
    try:
        s = float(r["priority_score"])
    except ValueError:
        s = -1
    return (order.get(r["priority"], 5), -s, r["id"])


def markdown(results):
    lines = ["| Priority | Score | Quick win | ID | Bucket | Title | Scope | Effort | Confidence | Status | Flags |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(results, key=sort_key):
        lines.append("| {priority} | {priority_score} | {quick_win} | {id} | {bucket} | {title} | {scope} | {effort} | {confidence} | {status} | {_flags} |"
                     .format(**{k: str(v).replace("|", "/") for k, v in r.items()}))
    counts = {}
    for r in results:
        counts[r["priority"]] = counts.get(r["priority"], 0) + 1
    qw = sum(1 for r in results if r["quick_win"] == "yes")
    summary = "Counts: " + ", ".join(f"{k}={v}" for k, v in sorted(counts.items())) + f"; quick wins={qw}"
    return summary + "\n\n" + "\n".join(lines)


def read(path):
    with open(path, "rb") as fh:
        raw = fh.read()
    # UTF-16 only with a BOM: trying it blindly mis-decodes Windows-1256 (Arabic Excel) files as garbage.
    encodings = ("utf-16",) if raw.startswith((b"\xff\xfe", b"\xfe\xff")) else ("utf-8-sig", "cp1256")
    for enc in encodings:
        try:
            text = raw.decode(enc)
            break
        except UnicodeDecodeError:
            continue
    else:
        text = raw.decode("latin-1")
    reader = csv.DictReader(io.StringIO(text))
    header = [h.strip() for h in (reader.fieldnames or [])]
    missing = [c for c in COLUMNS if c not in header]
    rows = [{(k or "").strip(): v for k, v in row.items()} for row in reader]
    return rows, missing, header


def _same_path(a: str, b: str) -> bool:
    if os.path.exists(a) and os.path.exists(b):
        return os.path.samefile(a, b)
    return os.path.normcase(os.path.abspath(a)) == os.path.normcase(os.path.abspath(b))


def _unique_backup(path: str, raw: bytes) -> str:
    """Copy raw bytes to path.bak-YYYYMMDD-HHMMSS[-N]; exclusive create, so an existing file is never replaced."""
    base = f"{path}.bak-{time.strftime('%Y%m%d-%H%M%S')}"
    n = 1
    while True:
        candidate = base if n == 1 else f"{base}-{n}"
        try:
            with open(candidate, "xb") as fh:
                fh.write(raw)
            return candidate
        except FileExistsError:
            n += 1


def _write_csv_atomic(target: str, fieldnames, out_rows) -> None:
    """Write to a temp file in the target's folder, then swap it in, so a crash never leaves a partial CSV."""
    folder = os.path.dirname(os.path.abspath(target))
    fd, tmp = tempfile.mkstemp(prefix=".tmp-findings-", suffix=".csv", dir=folder)
    try:
        with os.fdopen(fd, "w", newline="", encoding="utf-8-sig") as fh:
            w = csv.DictWriter(fh, fieldnames=fieldnames, extrasaction="ignore")
            w.writeheader()
            w.writerows(out_rows)
        os.replace(tmp, target)
    except BaseException:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


def _check_outputs(args) -> str | None:
    """Return an error message if any requested output is unsafe; checked before anything is written."""
    if args.write and args.out:
        return "--write and --out are mutually exclusive: choose in-place (with backup) or a separate output file."
    for flag, path in (("--out", args.out), ("--md", args.md)):
        if not path:
            continue
        if _same_path(path, args.csv):
            return f"{flag} points at the input file. Use --write for in-place updates (it keeps a backup)."
        if os.path.isdir(path):
            return f"{flag} {path} is a folder; give a file path."
        if os.path.exists(path) and not args.overwrite:
            return f"{flag} {path} already exists. Choose a new file name or add --overwrite to replace it."
    if args.out and args.md and _same_path(args.out, args.md):
        return "--out and --md point at the same file."
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("csv")
    ap.add_argument("--write", action="store_true",
                    help="update priority_score/priority/quick_win in the CSV (a timestamped backup is kept)")
    ap.add_argument("--out", help="write the scored CSV to this new file instead (input left untouched)")
    ap.add_argument("--md", help="write ranked Markdown table to this new file")
    ap.add_argument("--overwrite", action="store_true", help="allow --out/--md to replace an existing file")
    ap.add_argument("--lenient", action="store_true", help="exit 0 even with validation errors")
    args = ap.parse_args(argv)
    sys.stdout.reconfigure(encoding="utf-8")

    problem = _check_outputs(args)
    if problem:
        print(f"ERROR: {problem} Nothing was written.")
        return 2

    rows, missing, header = read(args.csv)
    if missing:
        print(f"ERROR: missing columns: {missing}\nExpected header: {','.join(COLUMNS)}")
        return 1
    results, errors = process(rows)
    for line, fid, errs in errors:
        for e in errs:
            print(f"line {line} [{fid}]: {e}")
    if not results:
        print("No findings rows.")
        return 0
    md = markdown(results)
    if args.md:
        with open(args.md, "w" if args.overwrite else "x", encoding="utf-8") as fh:
            fh.write(md + "\n")
        print(f"Ranked table written: {args.md}")
    else:
        print(md)
    if args.write or args.out:
        extra = [h for h in header if h not in COLUMNS]
        out_rows = [{**{h: orig.get(h, "") for h in extra}, **{c: r[c] for c in COLUMNS}}
                    for r, orig in zip(results, rows)]
        normalized = sum(1 for r, orig in zip(results, rows) if (orig.get("bucket") or "").strip() != r["bucket"])
        computed = sum(1 for r, orig in zip(results, rows) for c in ("priority_score", "priority", "quick_win")
                       if (orig.get(c) or "").strip() != r[c])
        if args.write:
            with open(args.csv, "rb") as fh:
                original = fh.read()
            backup = _unique_backup(args.csv, original)
            _write_csv_atomic(args.csv, COLUMNS + extra, out_rows)
            print(f"Updated: {args.csv} (backup of the original: {backup})")
        else:
            _write_csv_atomic(args.out, COLUMNS + extra, out_rows)
            print(f"Scored CSV written: {args.out} (input left untouched)")
        print(f"Bucket values normalized: {normalized}; computed cells changed: {computed}.")
    print(f"\n{len(results)} findings, {len(errors)} with validation errors.")
    return 1 if errors and not args.lenient else 0


if __name__ == "__main__":
    sys.exit(main())
