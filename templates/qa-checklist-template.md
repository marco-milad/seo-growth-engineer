# 08 · QA: CHG-[###] / [T-...]

Date: [YYYY-MM-DD] · Environment checked: [production URL / staging URL] · Deployed version confirmed: [commit / build ID / CMS revision, how verified]

> Every line needs evidence (a file path in 08-qa/, a command output, a screenshot, a tool result with date).
> Remove rows that don't apply to this change. "Looks fine" is not evidence.

## Deployment

| Check | Result | Evidence |
|---|---|---|
| Deploy succeeded and live response serves the new version | | |
| No unrelated pages broken (spot check of key templates, status 200) | | |

## Indexing controls

| Check | Result | Evidence |
|---|---|---|
| Status codes as intended (200 / 301 / 404 / 410) | | site_check.py output |
| Redirects: single hop, correct target, no loops | | |
| robots.txt: intended rules only; key pages allowed | | |
| meta robots / X-Robots-Tag as intended | | |
| Canonical: absolute, self (or intended target), one per page | | |
| XML sitemap: only 200, canonical, indexable URLs; updated lastmod | | |

## Content and metadata (raw HTML AND rendered)

| Check | Result | Evidence |
|---|---|---|
| Title / meta description present in initial HTML | | |
| One H1, matches intent | | |
| Body content present without JS (or rendered check passed) | | |
| Internal links render as crawlable `<a href>` | | |
| Image alt text where meaningful | | |

## Structured data

| Check | Result | Evidence |
|---|---|---|
| JSON-LD parses; types as intended | | |
| Rich Results Test (supported types) / Schema Markup Validator | | screenshot / result URL, date |
| Values match visible page content and business facts | | |

## International / Arabic

| Check | Result | Evidence |
|---|---|---|
| hreflang: valid codes, self-reference, reciprocal, x-default where used | | |
| `lang` / `dir` attributes correct | | |
| RTL layout at ~390 px: no overflow, mirrored correctly | | screenshot |
| Language switcher links to equivalent page | | |

## Performance and mobile

| Check | Result | Evidence |
|---|---|---|
| Lighthouse mobile, same URL and settings as baseline (lab) | | report file |
| Field CWV (CrUX/GSC), if data exists, after the agreed window | | |
| Mobile rendering screenshot | | |

## Measurement

| Check | Result | Evidence |
|---|---|---|
| Analytics tag fires on changed pages | | |
| Key events / conversions still recorded | | |
| GSC URL Inspection (live test) for sample URLs | | |

## Result

- Outcome: [pass / fail / partial]
- Follow-ups:
- G5: presented [date], accepted by user [date, quote]
- Tracker status set to: [validated / in-progress]
