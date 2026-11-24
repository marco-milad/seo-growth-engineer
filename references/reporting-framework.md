# Reporting framework (Stage 9)

Load this when producing any recurring report, the first post-implementation report, or a one-off "how are we doing" review. Measurement mechanics (GSC, GA4, GBP data, baselines, period comparisons, correlation vs causation) live in [analytics-and-measurement.md](analytics-and-measurement.md). This file covers **what to report, to whom, and how to say it honestly**.

## Contents
1. Principles
2. Cadence
3. Before writing: the reporting checklist
4. Output A: technical / internal report
5. Output B: client-facing executive report
6. Output C: next-period action plan
7. Presenting wins and losses honestly
8. Attribution language
9. Metrics to lead with, and vanity metrics to avoid
10. Roadmap status in reports
11. Arabic-first reporting
12. Common reporting mistakes

## 1. Principles

- **A report explains what changed, why we think it changed, and what we'll do next.** A dashboard dump is not a report.
- **Every number has a source, a date range, and a scope** (property, country, device, page group). Numbers without these are removed, not rounded off.
- **Same definitions every period.** If a definition changes (a new GA4 key event, a GSC property switch, a new country filter), say so at the top and break the trend line there.
- **First-party and tool-estimated numbers never share a column.** Ahrefs/Semrush figures are labelled "tool estimate (tool, date)".
- **No forecasts dressed as facts.** Direction and mechanism are fine. "We expect impressions for the category cluster to grow as the new pages are indexed" is acceptable; "traffic will grow 40%" is not.
- **Missing data is reported as missing.** If GA4 broke for 9 days, the report says so and excludes or flags that window.

## 2. Cadence

| Report | Typical cadence | Audience |
|---|---|---|
| Technical / internal | Monthly (weekly during a migration or launch) | SEO team, developers, project owner |
| Executive | Monthly or quarterly, depending on the client's rhythm | Owner, management, marketing lead |
| Next-period plan | With every executive report | Both |
| Incident note | Immediately on a P0 (index loss, manual action, outage, hacked content) | Owner + whoever can fix it |

Use the cadence agreed at discovery. A small local business usually wants a short monthly note. A large e-commerce site may need weekly technical monitoring and a monthly executive report.

GSC data typically lags by a couple of days. Don't close a period until the data for its last days is available, and state the pull date (verify the current delay in analytics-and-measurement.md section 2).

## 3. Before writing: the reporting checklist

1. **Periods:** equal length; same weekday mix where it matters. Prefer year-over-year for seasonal businesses (Ramadan, Eid, back-to-school, White Friday/11.11 sales shift dates every year: align by event, not by calendar date).
2. **Tracking integrity:** any GA4 tag gaps, consent-mode changes, property or filter changes, GSC property changes in either period? (analytics-and-measurement.md section 9.)
3. **Annotations:** list everything that happened in both periods: deploys and changes from `07-changes/change-log.md`, content published, confirmed Google updates (from the Google Search Status Dashboard, not rumours), outages, campaigns, PR, seasonality.
4. **Run comparisons** with `scripts/gsc_compare.py` (queries and pages), GA4 organic landing-page exports, GBP performance exports, and the latest `site_check.py` run for technical health.
5. **Roadmap status:** pull `06-tracker.csv`, and count tasks by status.
6. **Save raw data** under `data/` with dates in file names, and the report under `09-reports/YYYY-MM/`.

## 4. Output A: technical / internal report

File: `09-reports/YYYY-MM/technical-report.md` (template: `templates/performance-report-template.md`, Part A).

Structure:
1. **Period, sources, data caveats.**
2. **Search performance:** GSC clicks, impressions, CTR, average position. Use property totals from the chart for headlines and exported rows for breakdowns, and say which is which. Break down by page group (template), country, device, and brand vs non-brand where a brand regex was agreed.
3. **Movers:** top gaining and losing queries/pages with a hypothesis for each, labelled as a hypothesis, plus the evidence that would confirm it.
4. **Indexing and technical health:** indexed vs not-indexed trend by reason, sitemap status, CWV status (field data if it exists, lab otherwise and labelled so), new crawl errors, the `site_check.py` issue counts compared to last run.
5. **Organic conversions** (GA4): organic sessions, key events, and conversion rate by landing-page group. Revenue only if e-commerce tracking is verified.
6. **Local** (if in scope): GBP interactions (calls, direction requests, website clicks) per location, review count and average rating trend, response rate, and the status of NAP fixes.
7. **Off-page:** new and lost referring domains (from a backlink tool, labelled as an estimate) and the outcome of outreach / digital PR, all labelled.
8. **AI-search** (if in scope): only the measurable signals described in ai-search-visibility.md, with the method stated.
9. **Roadmap status** (section 10).
10. **Findings opened or closed this period** (IDs).
11. **Not checked / why.**

## 5. Output B: client-facing executive report

File: `09-reports/YYYY-MM/executive-report.md` (Part B of the template). One to two pages. Written for someone who will read it in five minutes and has no SEO vocabulary.

Structure:
1. **The headline:** 2–3 sentences. What happened, in business terms.
2. **Three to five numbers** that map to the goals agreed at discovery (e.g. organic enquiries, organic orders, calls from Google Maps, non-brand clicks to service pages). Each with the previous period and the change, and one line of interpretation.
3. **What we did:** completed (validated) work in plain language, with no IDs.
4. **What we learned:** one or two insights (e.g. "GSC shows [term A] gets more impressions than [term B] on the [category] page, so we've adjusted the heading").
5. **Risks or blockers that need the client:** access, approvals, content inputs, decisions. Each with a date it's needed by.
6. **Next month:** the 3–5 priorities from Output C.

Sample executive summary (placeholders only, never fill with invented values):

> This month, organic search brought [X] enquiries through the website, compared with [Y] last month ([±Z%]). Most of the increase came from the new [service] pages, which started appearing in Google in [week]. Clicks from Google Maps to call the [branch] location were [steady / down], which matches the [holiday] period last year. Next month we will finish the product-page fixes approved on [date] and need your team's answers on [topic] by [date] to publish the remaining location pages.

If a goal metric cannot be measured yet (e.g. GA4 key events not set up), the executive report says so in the numbers section and explains when it will be measurable.

## 6. Output C: next-period action plan

File: `09-reports/YYYY-MM/next-period-plan.md` (Part C of the template).

- 3–7 tasks for the next period, pulled from the roadmap (task IDs), in order.
- For each: owner/role, the dependency or approval needed (G4 proposals coming), and the acceptance criteria.
- Items carried over from last period, with the reason.
- New findings that change the roadmap, and whether they need a G3 re-approval (if priorities or scope shift materially, they do).
- Measurement items: anything to set up or fix so next month's report is better.

## 7. Presenting wins and losses honestly

- **Report losses with the same prominence as wins.** A drop explained early builds trust; a drop discovered by the client destroys it.
- **For each significant change, give:** the size, the scope (which pages/queries), the most likely explanations ranked by evidence, and what you'll do or watch.
- **Small changes are noise until proven otherwise.** Low-volume pages swing by chance. State the absolute numbers, not only percentages ("+200%" from 1 to 3 clicks is meaningless).
- **Don't cherry-pick windows** to make a trend look better. Use the agreed cadence.
- **Don't hide a regression caused by our own change.** Log it, explain it, show the fix or rollback.

## 8. Attribution language

Use the canonical causal ladder from analytics-and-measurement.md §13, with the same phrases and the same conditions:

| Evidence (all conditions must hold) | Wording |
|---|---|
| Only the timing aligns | "The change on [pages] coincided with [change]." |
| Timing and the mechanism align, and controls didn't move | "The change on [pages] is consistent with [change]." |
| The mechanism, timing, a control group, and a URL-level check (e.g. URL Inspection shows the new canonical selected) all agree | "The improvement on [pages] was likely caused by [change]." |
| Change site-wide during a confirmed Google update | "This coincides with Google's [update name] ([dates]). It isn't possible to separate our work's effect from the update." |
| Change with seasonal precedent | "A similar rise happened in the same period last year; this looks largely seasonal." |
| No clear explanation | "We don't yet know the cause. We're checking [x] and [y]." |

"Likely caused by" is the top tier. Never write "caused by" or "thanks to our work". Never claim causation from a single before/after comparison. Label attributed numbers (observed, assisted/modelled, inferred, unavailable) per analytics-and-measurement.md §13. GA4 crediting Organic Search with a conversion is not evidence that our work caused it.

## 9. Metrics to lead with, and vanity metrics to avoid

Lead with metrics tied to the discovery goals (analytics-and-measurement.md section 11, KPI tree): organic conversions, revenue or leads from organic landing pages, non-brand clicks to priority page groups, local actions (calls, directions) per location, and indexed coverage of priority templates.

Treat these as supporting or diagnostic, not as headlines:
- **Average position, site-wide.** It's an impression-weighted average that moves when you start ranking for new long-tail queries, even if the important rankings improved. Report position per query or page group.
- **Total impressions alone.** They can rise from irrelevant queries.
- **Third-party "authority scores" (DR, DA, AS).** These are vendor metrics, not Google signals.
- **Keyword counts from tools** ("ranking for 1,200 keywords"): an estimate, and most are irrelevant.
- **Lighthouse performance score.** It's a lab score. Report CWV field data where it exists.
- **Number of backlinks.** Relevance and referring domains matter more than raw link counts.

## 10. Roadmap status in reports

Show counts by status from `06-tracker.csv` and distinguish them clearly:

| Status | Meaning in the report |
|---|---|
| validated | Done and proven working (with QA evidence) |
| implemented | Deployed, QA pending. **Not** "done" |
| in-progress / approved | Being worked on / approved, not started |
| proposed | Waiting for the client's approval (G4) |
| blocked | Waiting on something. Name what and who |
| monitoring | Change verified (G5 passed); its search-side effect is still being measured. **Not** a proven result |

The meanings come from SKILL.md (Status lifecycle). In the executive report:
- **"What we did"** lists only `validated` and `monitoring` items, both of which have accepted QA evidence. Describe `monitoring` items as "verified changes whose effect we're still measuring".
- `implemented` items are listed as "deployed, being verified".
- Nothing `proposed`, `approved` or `in-progress` is presented as done. That includes owner actions that were recommended but not yet confirmed.

## 11. Arabic-first reporting

When the client reads Arabic:
- Write the executive report in Arabic. Keep standard terms such as Search Console, Google Business Profile, CTR and Core Web Vitals in English, with a one-time short Arabic explanation.
- Use the number format the client uses. Many Egyptian business readers are comfortable with Western digits in reports, so ask once and stay consistent.
- Dates: state the Gregorian date. Add the Hijri date or the event name when seasonality is tied to Ramadan/Eid.
- Right-to-left tables: keep the metric names short. Put the numbers in their own cells, not in mixed Arabic/English sentences, to avoid bidi reordering problems.
- The technical report can stay in English if the technical team prefers that. Ask.

## 12. Common reporting mistakes

- Sum-of-rows totals presented as property totals (see gsc_compare.py caveats).
- Comparing a 31-day month with a 28-day month without normalizing or noting it.
- Mixing GA4 "sessions" with GSC "clicks" as if they were the same thing. They are measured differently and will never match.
- Reporting a fix as done because it was deployed (implemented ≠ validated).
- Burying a tracking outage in a footnote.
- Changing the report structure every month, so trends can't be followed.
- Reports that list activities ("optimized 20 pages") without the outcome or the next step.
