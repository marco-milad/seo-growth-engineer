# Stages 3–4: Running the Audit and Prioritizing Findings

This file describes *how* an audit runs: scope, order, evidence, writing findings, priority, and the G2 review. The *what* to check lives in the domain files (technical-seo.md, on-page-seo.md, content-strategy.md, local-seo.md, off-page-seo.md, analytics-and-measurement.md, plus the lenses). The conventions (finding schema, ID prefixes, buckets, confidence, priority formula, status vocabulary, gates) are defined in SKILL.md and are not repeated here. This file shows how to apply them.

Outputs: `03-audit/audit.md`, `03-audit/findings.csv`, `03-audit/evidence/`. Templates: `templates/seo-audit-template.md`, `templates/findings-template.csv`.

## Contents

1. Preconditions
2. Scoping the audit
3. Audit order and why
4. Tracking gaps first
5. Evidence capture rules
6. Writing a finding
7. Bucket classification rules
8. Applying the priority model (worked examples)
9. Using prioritize_findings.py
10. audit.md structure
11. G2 review
12. "Not checked / why"
13. Escalating P0 issues mid-audit

## 1. Preconditions

Before Stage 3 starts:
- G1 passed: business summary, mode, and module selection confirmed (`01-discovery.md`).
- `02-access-and-data.md` exists. You know which data sources are verified, which are untested, and which are missing. The audit plan adapts to it. Missing GSC changes *how* you audit indexing; it doesn't cancel the audit.
- The page types and templates are known (from discovery or a first crawl).

## 2. Scoping the audit

### Unit of analysis: templates, not pages

Most SEO issues are template-level. A wrong canonical in the product template affects every product. Audit per **page type** first, then sample individual URLs inside each type:

| Page type | Examples | Typical sample |
|---|---|---|
| Home | `/`, `/ar`, `/en` | All language versions |
| Category / listing | `/c/shoes`, `/services` | Top by business priority + top by traffic + 2–3 deep or filtered ones |
| Detail | product, service, course, doctor, location | Top sellers/leads, random sample, out-of-stock / old ones |
| Content | blog, guides, news | Top by traffic, newest, oldest, thinnest |
| Utility | contact, about, policies, search results, cart, account | One each; check that indexability is intended |
| Location pages | `/branches/nasr-city` | All (they're few and high value) |
| Language variants | each page type in every language | Pairs, to check hreflang/canonical reciprocity |

### Sampling for large sites

- **Up to ~500 URLs:** check everything you can (sitemap list + crawl).
- **500–50,000 URLs:** full crawl if a crawler is available and approved (Screaming Frog, or `site_check.py` on a sitemap sample). Otherwise a stratified sample: every template, ~20–50 URLs per template, weighted toward pages with traffic or revenue.
- **50,000+ URLs:** template-level analysis + stratified samples + GSC Pages report (indexing patterns by URL pattern) + server logs if available. State the sample size and method in `audit.md`. A finding found in the sample is reported as "observed in N of M sampled URLs", never extrapolated to an exact site-wide count.

### Scope decisions to write down

- Hosts and properties in scope (www/non-www, subdomains, old domains still resolving).
- Languages and countries in scope.
- Page types in and out of scope (e.g. "the help centre at help.example.com is out of scope by user request").
- Rendering checked: raw HTML only, or rendered too (and how).
- Sample size per template.

## 3. Audit order and why

Run the domains in this order. Measurement runs alongside all of them.

1. **Technical:** can search engines crawl, render, and index the pages? If the answer is no, everything downstream is moot. A perfect title on a `noindex` page earns nothing.
2. **On-page:** does each indexable page clearly serve one intent with sound titles, headings, internal links, and media?
3. **Content:** does the site cover what the audience searches for, with enough quality, depth, and trust? Gaps, thin pages, cannibalization.
4. **Local** (if in scope): GBP, NAP, citations, local pages, reviews.
5. **Off-page:** authority, links, mentions, brand. Last, because link gains are wasted on pages that can't rank for technical or content reasons.

**Measurement throughout:** before interpreting any trend, confirm the data is trustworthy (section 4). During each domain, pull the relevant first-party data (e.g. indexing status during Technical, query/page performance during On-page and Content).

The lenses (Arabic/multilingual, industry, AI-search) apply inside each domain, not as a separate pass. For example, hreflang belongs to Technical, Arabic keyword variants to On-page and Content.

Order of work is not order of reporting. In `audit.md`, findings are presented by priority.

## 4. Tracking gaps first

Performance conclusions drawn from broken measurement are the most expensive audit error. Before stating "organic traffic dropped" or "page X converts poorly", check:

- Is GA4 installed on all templates, all languages, all subdomains? Is consent mode suppressing a large share of data?
- Are key events (conversions) defined and firing for the actual business conversions (calls, WhatsApp clicks, form submits, purchases)?
- Is internal/developer traffic filtered? Any spam referrers?
- Is the GSC property type right (Domain property vs URL-prefix), and does it cover all hosts?
- Were there tracking changes (new GA4 property, GTM changes, consent banner launch, site migration) inside the comparison window?

The full checklist is in analytics-and-measurement.md ("Tracking-gap audit"). Each gap becomes an `ANL-` finding, usually high urgency because it blocks the baseline. Where data is unreliable, say so next to every number that depends on it.

## 5. Evidence capture rules

Evidence is what makes a finding reviewable by someone who wasn't there.

- Save evidence under `03-audit/evidence/` with dated, descriptive names: `2026-11-24_site-check_products-sample.csv`, `2026-11-24_gsc-pages-report_not-indexed.png`, `2026-11-24_home-ar_rendered-vs-raw.html`.
- Raw exports go to `data/` with the date range in the name: `data/gsc_queries_2026-08-01_2026-10-31.csv`.
- For every finding, the `evidence` field points to a specific file or reproducible check (URL + method), and `data_source` and `data_date` are filled.
- Screenshots of logged-in tools: crop or redact other clients' data, personal emails, and anything not needed.
- Never store credentials, cookies, tokens, or session exports in evidence.
- Third-party tool numbers are copied with the tool name and its own label ("Ahrefs DR, estimate").
- If the evidence is a single observation that couldn't be reproduced, confidence is at most Medium.

## 6. Writing a finding

A good finding lets a developer fix it and a manager understand why it matters, without a follow-up question.

### Good example

```text
id: TEC-004
bucket: Confirmed issue
domain: Technical
title: Product variant URLs are indexable duplicates with no canonical
scope: Product template; all ?color= and ?size= variant URLs (observed 38 of 40 sampled products)
description: Each colour/size selection creates a URL with query parameters that returns 200, has no canonical tag,
  and repeats the main product's title and description. Google may index variants instead of the main product
  and split signals across them.
evidence: 03-audit/evidence/2026-11-24_site-check_variants.csv (rows 2–39); GSC Pages report shows 1,214
  "Duplicate without user-selected canonical" URLs matching ?color= (screenshot 2026-11-24_gsc-duplicates.png)
data_source: site_check.py (raw HTML), Google Search Console Pages report
data_date: 2026-11-24
business_impact: Product pages are the purchase pages; diluted or wrong URLs in results reduce clicks to buyable pages.
seo_impact: Duplicate clustering, wasted crawling, possible wrong URL shown in results.
impact: 4 | urgency: 3 | business_relevance: 5 | effort: 2 | confidence: High (1.0)
priority_score: 8.0 → P1, quick win: yes
recommendation: Add a self-referencing canonical on the main product URL and a canonical from variant URLs to it,
  OR stop generating crawlable variant URLs (state in the client) — choose per architecture review. Keep variants
  out of the sitemap.
dependencies: Developer access to product template; decision on whether variants deserve their own landing pages
validation_method: site_check.py on the same 40 URLs shows canonical present and correct; URL Inspection on 5
  variants shows Google-selected canonical = main product (after recrawl); GSC duplicate count trend
owner_role: Frontend developer
status: open
```

### Bad example (and what's wrong)

```text
TEC-4 | Fix canonicals | High priority | Canonical issues found on the site, which hurts SEO. Add canonical tags.
```

- No scope: which URLs, which template, how many?
- No evidence or source, so nobody can verify it.
- "Hurts SEO" is not an impact statement, and there's no business impact.
- No scores, so the priority can't be explained.
- The recommendation is not actionable: canonical to what?
- No validation method, so nobody knows when it's done.
- The ID format is wrong (`TEC-4` instead of `TEC-004`).

## 7. Bucket classification rules

Choose exactly one bucket (definitions in SKILL.md). The bucket says **what the evidence shows**; confidence says **how reliable and representative that evidence is**. Decide them separately, in this order. Decision rules:

1. Was the problem itself directly observed in first-party data, the source code, or a reproducible check of the live site (including a reproducible sample, for the sampled scope)? → **Confirmed issue**.
2. Do only indirect signals point to it: a third-party estimate, a pattern or inference, a single observation that couldn't be reproduced, or an absence in raw HTML on a JS site before a rendered check? → **Potential issue**. The recommendation starts with the check that would confirm it.
3. Is there a symptom confirmed by data but with an unknown cause (e.g. a GSC impressions drop of [X]% on one page group since a date)? → **Needs investigation**. List the hypotheses and the data needed.
4. Is nothing wrong, but a measurable gain is available (a new page type for an uncovered intent, schema eligibility, GBP features unused)? → **Opportunity**.
5. Can't assess at all because data or access is missing? → **Missing data**. The recommendation is the specific access or export required. Missing-data items carry no impact score claims beyond "unknown". Score them on the value of getting the data.

Then set confidence (SKILL.md Evidence standard) for that evidence. Allowed combinations:
- **Confirmed:** High, or Medium (e.g. when a sample is extrapolated to a whole template).
- **Potential:** Medium or Low.
- **Needs investigation:** the symptom itself is High or Medium.
- **Low is never Confirmed.**

| Evidence | Bucket | Confidence |
|---|---|---|
| GSC Pages report lists 1,214 "Duplicate without user-selected canonical" URLs | Confirmed | High |
| Canonical missing on 12 of 12 sampled category URLs, reproducible; claim covers the whole template | Confirmed | Medium |
| Semrush shows a ranking drop for a page group | Potential | Medium (third-party estimate) |
| One 5xx response on a single fetch that couldn't be reproduced | Potential | Medium |
| H1 missing in raw HTML on a JS-rendered site, before a rendered check | Potential | Low |

A pending client decision is never a bucket or a priority. Classify the underlying issue as usual and record the decision in `dependencies` (e.g. `client decision: AI-crawler policy`).

Don't upgrade a Potential issue to Confirmed because it's "usually true". Don't downgrade a Confirmed issue because the fix is inconvenient.

## 8. Applying the priority model (worked examples)

Formula and bands are in SKILL.md:
`priority_score = (2×Impact + Urgency + Business relevance) × Confidence ÷ Effort`; P1 ≥ 6, P2 3–<6, P3 < 3, P0 override; quick win = Impact ≥ 3, Effort ≤ 2, Confidence ≥ 0.8.

Score each factor from the evidence and the business facts in `01-discovery.md`, not from habit. Write a one-line rationale per score in the finding's description or notes, so the client can challenge it.

**Example 1: Product template canonical points to the homepage** (Confirmed, source code + live HTML)
Impact 5 (all product pages may drop from the index), Urgency 4 (pages already dropping in the GSC Pages report), Business relevance 5 (purchase pages), Effort 2 (one template change), Confidence 1.0.
Score = (10 + 4 + 5) × 1.0 ÷ 2 = **9.5 → P1, quick win**. If GSC shows product pages already de-indexed at scale, this becomes **P0** by override: tell the user now.

**Example 2: 40 blog posts have missing meta descriptions** (Confirmed, site_check)
Impact 2 (snippets can still be generated; the blog drives few conversions), Urgency 1, Business relevance 2, Effort 2, Confidence 1.0.
Score = (4 + 1 + 2) × 1.0 ÷ 2 = **3.5 → P2**, not a quick win (Impact < 3). Batch it with other blog work.

**Example 3: Suspected cannibalization between two category pages** (Potential, based on a third-party rank tracker estimate)
Impact 4, Urgency 2, Business relevance 4, Effort 3 (content merge + redirects), Confidence 0.5. The rank tracker itself is a Medium-confidence source (a third-party estimate), but the *cannibalization conclusion* is inferred from those estimates, so the inference is Low. The reliability of a source and the reliability of a conclusion drawn from it are scored separately.
Score = (8 + 2 + 4) × 0.5 ÷ 3 = **2.3 → P3**. But Impact is high and confidence low, so per SKILL.md it becomes a **"validate first" task**: check GSC query → page data for both URLs. If confirmed (by the canonical rule in on-page-seo.md, Cannibalization), re-score with Confidence 1.0: (14 × 1.0 ÷ 3) = 4.7 → P2.

Calibration tips:
- Impact is about pages that matter to *this* business. The same issue on a revenue template and on a forgotten tag archive scores differently.
- Effort includes coordination: a one-line fix that needs a third-party agency's release cycle is not Effort 1.
- Don't inflate Urgency to push favourite items up. Urgency is the cost of waiting.

## 9. Using prioritize_findings.py

After the findings are drafted in `03-audit/findings.csv` (columns per `templates/findings-template.csv`):

```bash
# validate and print the ranked table (writes nothing)
python <skill-dir>/scripts/prioritize_findings.py seo-engagement/<slug>/03-audit/findings.csv
# update the computed columns in place; the original is kept as findings.csv.bak-YYYYMMDD-HHMMSS
python <skill-dir>/scripts/prioritize_findings.py seo-engagement/<slug>/03-audit/findings.csv --write
# or leave the input untouched and write the scored copy and the ranked table to new files
python <skill-dir>/scripts/prioritize_findings.py seo-engagement/<slug>/03-audit/findings.csv --out seo-engagement/<slug>/03-audit/findings-scored.csv --md seo-engagement/<slug>/03-audit/findings-ranked.md
```

`--out` and `--md` refuse to replace an existing file unless `--overwrite` is given. `--write` never overwrites an earlier backup. The script:
- Validate required fields, ID format, bucket, status, and score ranges. Fix every validation error it reports; don't bypass them.
- Compute `priority_score`, `priority` band, and `quick_win` deterministically.
- Produce a ranked Markdown table for `audit.md`.

P0 is an override the script can't infer from scores alone. Set it explicitly per SKILL.md criteria and say why in the finding. Re-run the script whenever scores change, and never hand-edit computed columns.

## 10. audit.md structure

Use `templates/seo-audit-template.md`. The finished document should read in this order:

1. **Summary** (half a page): the 3–5 things that matter most, in plain language, with their priority. Any P0 first.
2. **Scope and method:** hosts, languages, page types, sample sizes, rendering method, tools used, data dates.
3. **Data reliability:** tracking gaps and their effect on conclusions.
4. **Findings by priority:** the ranked table (from the script), then detail blocks for P0/P1 findings.
5. **Findings by domain:** short sections (Technical, On-page, Content, Local, Off-page, Analytics, lenses) linking to finding IDs. This is useful for the people who will fix them.
6. **Opportunities:** separate from issues, so the client doesn't read an opportunity as a defect.
7. **Missing data and items needing investigation:** what's needed, from whom.
8. **Not checked / why** (section 12).
9. **Next step:** G2 review, then Stage 5 or the roadmap, depending on mode.

Keep jargon out of the summary. "Google can't see the prices on product pages because they load after the page opens" beats "client-side rendered Offer data absent from initial HTML". Put the technical version in the finding.

## 11. G2 review

Present the summary and the ranked findings to the user and ask them to:
- Correct factual errors (e.g. "that subdomain is retired", "those pages are intentionally noindex").
- Flag disagreements on priority, with reasons. Adjust scores where the business context justifies it, and record the change.
- Mark findings they won't act on (`won't-fix`, with the reason).

G2 passes when the user explicitly accepts the findings, with corrections applied. Record the date and any changes in `PROJECT_STATE.md`. In Audit Only mode, G2 completes the engagement deliverable. Offer the strategy stage, but don't push it.

## 12. "Not checked / why"

Every audit ends with this list. It protects the client from assuming coverage that didn't happen, and it protects you from implied claims.

```text
Not checked / why / what would unlock it
- Query-level performance — no Search Console access → Performance exports from the user (or a connector they set up; a human consultant can be added as a Restricted user)
- Core Web Vitals field data — not enough Chrome traffic for CrUX → lab data only (Lighthouse), labelled as lab
- Backlink profile — no Ahrefs/Semrush access; GSC Links report not available → GSC access or a tool export
- JavaScript-rendered content — raw HTML checks only → approval to run a rendering crawler, or rendered HTML via URL Inspection
- GBP for branch 2 — no account view; public view only → a Performance export or screenshots from the owner (or manager access for a human team member)
```

## 13. Escalating P0 issues mid-audit

If you find a P0 condition (site-wide noindex or robots block, hacked/spam content, manual action, revenue pages erroring, an accidental `Disallow: /` after a deploy), stop and tell the user immediately. Give the evidence, the likely impact, and a proposed fix. If the fix is executed by you (or touches code/config), it goes through a G4 change proposal. Urgency shortens the conversation, but it never skips approval. In Audit Only or Strategy mode, report the issue and the recommended fix. The user decides who implements it. If they ask you to, only that change set moves to Execution under G4 (SKILL.md, Approval gates). Log it in `findings.csv` with priority P0 and note the time the user was informed.
