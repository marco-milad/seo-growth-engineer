# Example: auditing when Search Console and GA4 are unavailable

> FICTIONAL. Shows how to proceed honestly when first-party data is missing.

## Situation

A local physiotherapy clinic (fictional) asks for "a full SEO audit". The owner doesn't know whether Search Console or GA4 exist, and the previous web developer is unreachable.

## Stage 2 output, abbreviated `02-access-and-data.md`

| Source | Status | Effect on conclusions |
|---|---|---|
| Google Search Console | Needs user action (unknown if a property exists) | No query, click, indexing-reason or CWV field data. Indexing findings max **Medium** confidence |
| GA4 | Needs user action (a tag `G-…` is present in the page source, but nobody has access) | No traffic or conversion numbers anywhere in the audit |
| Google Business Profile | Public view only (date) | Completeness and reviews observed publicly. Insights and owner settings unknown |
| Backlink tool | Unavailable | Off-page limited to brand-mention search and visible citations. No link counts |
| Live site | Verified (site_check.py, date) | Technical and on-page findings can be High confidence where reproducible |

**Required user actions** (ordered):
1. Check whether the clinic's Google account owns a Search Console property. If not, Claude can propose creating and verifying one. That's a G4 change because it touches the site or DNS.
2. Recover the GA4 property: the account owner, or Google's own recovery path. Until then, propose setting up a fresh property, also as a G4 change.

## What the audit still delivers

- Technical and on-page findings from the live site (indexability, canonicals, titles, schema, mobile rendering, speed in lab, labelled "lab").
- A local audit from the public GBP view and the NAP comparison (`nap_check.py`).
- **ANL-001**, a Missing-data finding: "No access to Search Console". **ANL-002**: "GA4 present but inaccessible: no conversion measurement". These are listed first under Data reliability, because they limit every performance conclusion.

## Phrases the skill uses and avoids

Use:
- "We can't see how many people find the site through Google until Search Console access is set up."
- "Lab speed test (not real visitors): LCP 4.1 s on the homepage, tested [date]."

Avoid:
- "Your traffic is probably around 500 visits a month." That's an invented number.
- "Audit complete." Say "Audit complete for what was accessible. See *Not checked / why*."
- Estimating rankings by hand-checking a few searches and calling them positions. A manual SERP sample (date, location, language, logged-out) can be reported **as a sample**, never as a ranking metric.

## Not checked / why (excerpt)

| Area | Why | Unlocks with |
|---|---|---|
| Query and click performance | No GSC | GSC access |
| Organic conversions | GA4 inaccessible | GA4 recovery or a new property |
| Backlink profile | No tool | GSC Links report, or a backlink tool trial the user approves |
