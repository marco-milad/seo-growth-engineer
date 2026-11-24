# SEO Analytics and Measurement

Measurement answers three questions: *Where are we now?* (baseline), *What changed?* (comparison), and *Did our work cause it?* (attribution, handled cautiously). This file covers the data sources, their limits, how to build a baseline, how to compare periods honestly, and how to audit tracking gaps. Reporting formats are in reporting-framework.md. AI-search visibility measurement is in ai-search-visibility.md. Tool access and connection methods are in tools-and-integrations.md.

Findings from this domain use the `ANL-` prefix (SKILL.md).

## Contents

1. Principles
2. Google Search Console
3. Google Analytics 4
4. Google Business Profile performance
5. Bing Webmaster Tools
6. Backlink tracking
7. Technical health tracking
8. AI-search measurement
9. Tracking-gap audit checklist
10. Baseline before changes
11. KPI tree by business model
12. Period comparisons
13. Correlation vs causation
14. Using gsc_compare.py

## 1. Principles

- **Validate the instrument before reading the needle.** Run the tracking-gap audit (section 9) before drawing performance conclusions.
- **First-party beats third-party.** GSC, GA4, and GBP are measurements of the actual site. Ahrefs/Semrush traffic and keyword numbers are modelled estimates. Never mix them in one column or chart without labels.
- **Every number gets a source, a date range, and the filters applied.** "Clicks: [X]" is incomplete. "GSC, Web search, all countries, 2026-09-01 → 2026-10-31, clicks: [X]" is complete.
- **Sums of rows don't equal totals** in GSC (anonymized queries, row limits). Say so when it matters.
- **Business outcomes outrank vanity metrics.** Impressions growth on irrelevant queries isn't a win.

## 2. Google Search Console

Official. Free. The only first-party view of Google Search visibility.

### Property types

- **Domain property** (DNS-verified): covers all protocols and subdomains. Preferred for audits because it catches duplicate hosts.
- **URL-prefix property:** covers only that exact prefix. Useful for per-folder or per-language views (`https://example.com/ar/`), and needed by some legacy tools.
- Some newer features are limited to top-level properties or to sites with enough volume (see the branded filter below). Verify which property type a feature needs at time of use.

### Performance report (Search results)

- **Metrics:** clicks, impressions, CTR, average position. Position is an impression-weighted average of the topmost position. Interpret it per query/page, never site-wide in isolation.
- **Dimensions:** query, page, country, device, search appearance, date.
- **Search types:** Web, Image, Video, News (plus separate Discover and Google News reports). Filter to **Web** for most SEO analysis; mixing types distorts CTR and position.
- **Filters:** query/page contains, does not contain, exact, and **custom regex** (RE2 syntax). Useful patterns:
  - Brand vs non-brand: `brandname|براند|brand name` (include Arabic spellings and common misspellings).
  - Question queries: `^(how|what|why|كيف|ما|ماذا|ليه|ازاي|إزاي)([\s?؟]|$)`. This matches a question word at the start of the query, followed by a space, `?` or `؟`, or the end of the query. In RE2, `\b` and `\w` are ASCII-oriented, so they don't recognise Arabic word boundaries; use `\s`, punctuation or `$` around Arabic words instead.
  - Page groups: `/ar/` vs `/en/`, `/products/`, `/blog/`.
- **Branded queries filter:** Google announced a built-in branded/non-branded filter in November 2025, classified by an AI-assisted system and available only to eligible (top-level, sufficient-volume) properties. (Source: Introducing the branded queries filter in Search Console, https://developers.google.com/search/blog/2025/11/search-console-branded-filter, checked 2026-11-24.) The Search Analytics API gained a branded dimension/filter in November 2026, with data from 2026-02-21 onward. (Source: New filtering and reporting capabilities in the Search Analytics API, https://developers.google.com/search/blog/2026/11/search-analytics-api-update, checked 2026-11-24.) Help-centre dates for data availability differed from the API post when checked, so verify the start date at time of use. When the filter isn't available, use your own regex and document it.
- **Query groups** in the Search Console Insights report cluster similar queries with AI, for high-volume properties only (October 2025). Treat the groups as a convenience view, not a stable taxonomy, because Google says they can change. (Source: Introducing Query groups in Search Console Insights, https://developers.google.com/search/blog/2025/10/search-console-query-groups, checked 2026-11-24.)
- **Comparison:** the date comparison mode gives side-by-side period columns. Exports of comparison views can be fed to `gsc_compare.py`.
- **Country and language analysis:** GSC has a country dimension but no language dimension. Approximate language by query script (Arabic vs Latin characters via regex, e.g. `[؀-ۿ]`) and by page folder (`/ar/`, `/en/`). For Arabic markets, compare countries (EG, SA, AE…) separately. Intent and competition differ.
- **Device:** always split mobile vs desktop for CTR and position. Most Arabic-market traffic is mobile.

### AI features in GSC

- **AI Mode** clicks, impressions, and positions count toward Performance report totals under the Web search type (documented June 2025). A follow-up question in AI Mode is treated as a new query. (Source: What are impressions, position, and clicks?, https://support.google.com/webmasters/answer/7042828, and Latest Google Search Documentation Updates, https://developers.google.com/search/updates, checked 2026-11-24.)
- **Generative AI performance report:** shows impressions for AI Overviews and AI Mode, derived from Web search data. Rolled out to all sites worldwide by 2026-08-31. (Source: Introducing Search Generative AI performance reports in Search Console, https://developers.google.com/search/blog/2026/06/gen-ai-performance-reports; Generative AI performance report help, https://support.google.com/webmasters/answer/16984139, checked 2026-11-24.) Metrics as of 2026-11-24: **impressions only**, by page, country, device and date. No clicks, CTR or position (confirmed on the help page and the launch post; Google says more metrics may be added, so re-check at time of use). Details are in ai-search-visibility.md.

### Data limits (verify at time of use; Google changes these)

- **Retention:** 16 months of performance data. Export and archive monthly if longer history matters. (Source: Connect Search Console to Google Analytics, https://support.google.com/analytics/answer/10737381, checked 2026-11-24.)
- **Freshness:** a "24 hours" view with hourly data arrives with a delay of a few hours. Recent days can be preliminary. (Source: An improved way to view your recent performance data, https://developers.google.com/search/blog/2024/12/recent-data-search-console, checked 2026-11-24.) The Search Analytics API supports an HOUR dimension, covering up to about 10 recent days. (Source: https://developers.google.com/search/blog/2025/04/san-hourly-data, checked 2026-11-24.) Don't report on the last 2–3 days as final.
- **Anonymized queries:** rare queries are omitted from query rows to protect privacy but still counted in chart totals. That's why row sums < totals.
- **Row limits:** the UI shows/exports up to 1,000 rows per table. The Search Analytics API returns up to about 50,000 rows per day per site per search type (figure from a 2022 Google post). The **BigQuery bulk export** is not subject to that daily row limit but still excludes anonymized queries. (Sources: A deep dive into Search Console performance data filtering and limits, https://developers.google.com/search/blog/2022/10/performance-data-deep-dive; About bulk data export, https://support.google.com/webmasters/answer/12918484, checked 2026-11-24.) For large sites needing long-tail analysis, recommend the bulk export (requires a Google Cloud project with billing; client-owned).
- Known data anomalies are listed on the Search Console "Data anomalies" help page. Check it before explaining a sudden step change. (Source: https://support.google.com/webmasters/answer/6211453, checked 2026-11-24.)

### Other GSC reports used in audits

| Report | Use |
|---|---|
| Pages (Page indexing) | Indexed vs not-indexed counts and reasons ("Crawled – currently not indexed", "Discovered – currently not indexed", "Duplicate without user-selected canonical", "Excluded by noindex", soft 404, redirect, 404). Inspect example URLs per reason; look at patterns, not single URLs |
| Sitemaps | Submitted sitemaps, last read, discovered URLs, errors. A "Couldn't fetch" on the first day after submission is common and often resolves; re-check after a few days before raising a finding |
| URL Inspection | Google's indexed version: Google-selected vs user-declared canonical, last crawl, crawl allowed, page fetch, rendered HTML/screenshot (live test). API quota: 2,000 queries/day and 600/minute per property. (Source: Usage Limits, https://developers.google.com/webmaster-tools/limits, checked 2026-11-24.) Manual "Request indexing" in the UI has a small daily quota and needs G4-style approval per SKILL.md |
| Links | Top linked pages, top linking sites, top anchor text, internal links. A sample, not a complete backlink list |
| Core Web Vitals | Field data (CrUX-based) grouped by URL pattern, mobile/desktop. Needs enough Chrome traffic; small sites often show "not enough data" |
| HTTPS, Manual actions, Security issues | P0 checks. Look at them in every audit |
| Crawl stats (Settings) | Requests per day, response codes, file types, host status, response time. Useful for large sites and server problems |
| Removals, Disavow (separate tool) | Read-only during audit. Any action needs approval |

## 3. Google Analytics 4

Official. Measures what users do after arriving.

- **Organic channel:** In the Default channel group, *Organic Search* is a session whose source matches Google's list of search sites or whose medium is exactly `organic`. Per Google's current documentation, it includes traffic from Google's AI Overviews and AI Mode. (Source: Default channel group, https://support.google.com/analytics/answer/9756891, checked 2026-11-24.)
- **AI Assistant channel:** added to the Default channel group in 2026 (release note dated 2026-05-13) for referrals from assistants such as ChatGPT, Gemini, Claude, Copilot, DeepSeek, and Grok. It sets medium `ai-assistant` and excludes Google AI Overviews/AI Mode. (Sources: Default channel group, https://support.google.com/analytics/answer/9756891; What's new in Google Analytics, https://support.google.com/analytics/answer/9164320, checked 2026-11-24.) Many app-based assistant clicks arrive without a referrer and land in Direct, so treat AI Assistant numbers as a lower bound (community advice, not official).
- **Organic Shopping / Organic Video / Organic Social** are separate channels. Decide with the client whether "organic" in reports means Organic Search only (default in this skill) or all of them, and state it.
- **Landing page analysis:** use the Landing page report or an Exploration with dimension "Landing page + query string", filtered to Session default channel group = Organic Search. Landing page is session-scoped, which aligns with session channel.
- **Key events:** GA4 calls conversions **key events** (events marked as key). Conversions shared with Google Ads are created from key events. Confirm the key events match the business conversions from discovery (purchase, generate_lead, call click, WhatsApp click, booking). (Source: API dimensions and metrics, https://developers.google.com/analytics/devguides/reporting/data/v1/api-schema, checked 2026-11-24.)
- **Engagement:** engaged sessions, engagement rate, average engagement time. Use them to compare page groups, not as absolute quality scores.
- **Attribution caveats:** the default reporting attribution is data-driven. Traffic-acquisition (session-scoped) and user-acquisition (first-user) reports give different organic numbers by design. Name the scope you report. Key event credit to organic depends on the attribution model and lookback window. Report "organic-attributed key events (data-driven, GA4)" rather than "conversions from SEO".
- **Consent mode:** where a consent banner is used (common with EU visitors), denied consent reduces observed data. Behavioural modelling may fill gaps only above traffic thresholds. Compare periods only when the consent setup is unchanged, and annotate banner launches. Verify modelling eligibility in the property at time of use.
- **Data hygiene:** internal traffic filters (office IPs, developers), unwanted referrals, cross-domain measurement for checkout or booking domains (otherwise organic sessions break at the payment step and get credited to referral), and unassigned/(not set) traffic.
- **Data retention setting** (2 or 14 months for explorations on standard properties) limits how far back Explorations go. Standard reports aren't affected.
- **GSC ↔ GA4 link:** brings GSC query/landing page reports into GA4. Useful, but the GSC limits above still apply.

## 4. Google Business Profile performance

For Local-module engagements. Metrics (Performance view in GBP, or the Business Profile Performance API): Search and Maps impressions (by device), website clicks, call clicks, direction requests, messaging clicks, bookings. Search keywords that triggered impressions are reported monthly. The API's daily metrics have daily granularity only. (Sources: fetchMultiDailyMetricsTimeSeries, https://developers.google.com/my-business/reference/performance/rest/v1/locations/fetchMultiDailyMetricsTimeSeries; Business Profile Performance API, https://developers.google.com/my-business/reference/performance/rest, checked 2026-11-24.)

- Analyse **per location**. Aggregates hide a failing branch.
- Add UTM parameters to the GBP website link (e.g. `utm_source=google&utm_medium=organic&utm_campaign=gbp_<location>`) so GA4 can separate GBP visits. The values above are only an example: defining or changing the UTM convention is analytics configuration and needs full G4. Applying an already-approved convention to the GBP link is a GBP edit on the owner-executed path. Note that tagging with medium `organic` keeps the visits in Organic Search; settle that when the convention is approved.
- Keyword impression counts below a threshold appear as ranges/"<15"-style values. Don't present them as exact.
- Rank-grid tools for Maps (third-party) give point-in-time, location-dependent snapshots. Label them as such.

## 5. Bing Webmaster Tools

Official (Microsoft). Free. Bing's performance, indexing, backlinks, site scan, and IndexNow submission. It can import sites from GSC. In 2026 Bing added an **AI Performance** report (public preview) covering how content is used in Copilot and partner AI answers, later extended with intents/topics/citation share. (Sources: Introducing AI Performance in Bing Webmaster Tools Public Preview, https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview; New AI Visibility Insights in Bing Webmaster Tools, https://blogs.bing.com/search/2026/6/New-AI-Visibility-Insights-in-Bing-Webmaster-Tools-Intents-Topics-Citation-Share-Compare/, checked 2026-11-24.) No confirmed API export for the AI report was found, so verify at time of use.

## 6. Backlink tracking

- **Sources:** GSC Links report (first-party sample), Bing Webmaster Tools backlinks, Ahrefs/Semrush (third-party indexes with their own crawl coverage; numbers are not comparable across tools).
- **Track:** referring domains (not raw backlinks), new/lost referring domains, links to priority pages, anchor distribution, and links from relevant sites.
- Always use the **same tool and same settings** across periods. Switching tools mid-engagement invalidates trends.
- Authority scores (DR, Authority Score) are vendor metrics. Report them as trend context, never as a goal in themselves.

## 7. Technical health tracking

Re-run the same checks on the same URL sets each period:
- `site_check.py` on a fixed URL list per template (status, canonical, indexability, titles, hreflang, schema types). Diff the CSVs between runs.
- GSC Pages report counts by reason (indexed, not indexed; top reasons) and Crawl stats.
- Lighthouse/PSI lab metrics on fixed URLs with the same device/throttling settings. Field CWV from the GSC CWV report or CrUX where available.
- Structured data reports in GSC (enhancements) for eligible types.
Lab metrics vary run to run, so take the median of several runs per URL and report the method.

## 8. AI-search measurement

See ai-search-visibility.md. In short:
- Google's first-party signals are the Generative AI performance report and AI Mode data inside Performance totals.
- GA4 provides the AI Assistant channel (a lower bound) and Organic Search (which includes AIO/AI Mode clicks).
- Bing has its AI Performance report.
- Prompt-sampling across assistants is an *indicator*, with the date, engine, language, and run count stated, never a precise metric.

## 9. Tracking-gap audit checklist

Run before interpreting performance. These are audit checks: each failed item becomes an `ANL-` finding with a proposed fix. Analytics and tracking configuration (filters, key events, data streams, retention, GTM, consent, the GSC↔GA4 link, the UTM convention) is changed only through a full G4 proposal, whoever executes it (SKILL.md, Approval gates). Never apply it on your own.

- [ ] GSC property exists, is verified, and covers all hosts (Domain property preferred). Ownership is with the client, not an ex-agency.
- [ ] Sitemaps submitted and read successfully.
- [ ] GA4 tag present on every template, language, and subdomain (check rendered pages, not just the codebase).
- [ ] One GA4 property per site (no duplicate tags double-counting; no old UA leftovers confusing the team).
- [ ] Key events defined for the real business conversions, and firing (test with DebugView or Realtime).
- [ ] Phone/WhatsApp/email clicks tracked as events where they are conversions.
- [ ] Cross-domain measurement for checkout/booking/payment domains. Unwanted referrals excluded (payment gateways).
- [ ] Internal traffic filter active. Developer/staging traffic excluded.
- [ ] Consent setup as determined by the owner and, where needed, qualified counsel (the skill checks only that it works as configured). Its effect on data volume understood and annotated.
- [ ] GSC ↔ GA4 linked (optional but useful).
- [ ] GBP website links carry UTMs (if Local is in scope).
- [ ] Bing Webmaster Tools set up (optional; low effort).
- [ ] Known changes inside comparison windows recorded: migrations, redesigns, tag changes, consent banner, CMS switches.
- [ ] Staging/preview environments are not indexed and don't send data to the production GA4 property.

## 10. Baseline before changes

A baseline is what lets anyone judge later whether the work helped. Capture it **before** G4 changes ship, and store it under `data/` and in the first report:

- GSC: last 3 months and the same 3 months last year (if history exists), Web search type, by page group and top queries. Brand vs non-brand split. Mobile vs desktop. Key countries.
- GA4: organic sessions, engaged sessions, key events by landing page group, for the same windows.
- GBP (if local): per-location actions and impressions.
- Technical: `site_check.py` CSVs per template, GSC Pages report counts, Lighthouse lab metrics (method stated), CWV field status.
- Off-page: referring domain count and list export from the chosen tool (tool + date).
- AI-search: Generative AI report snapshot, and prompt sample results if that method is used.
- Annotations: known events in the window.

If there's no history (new site, or tracking only just installed), the baseline is "starting from zero on [date]". No performance claims can be made until enough data accrues; say so in reports.

## 11. KPI tree by business model

Report from business outcome down to SEO drivers. Pick only KPIs that can actually be measured with the available data.

| Model | Business outcome | Organic outcome KPIs | Leading SEO indicators |
|---|---|---|---|
| E-commerce | Revenue, orders | Organic-attributed purchases/revenue (GA4), organic sessions to product/category pages | Non-brand clicks to category/product groups, indexed product share, Product rich-result eligibility, merchant listing appearances |
| Lead-gen / corporate / SaaS | Qualified leads, demos, trials | Organic-attributed lead key events, organic landing pages driving leads | Non-brand clicks on solution/feature/comparison pages, impressions for priority clusters, indexed priority pages |
| Local / multi-location | Calls, visits, bookings per location | GBP calls/directions/website clicks per location, organic bookings | GBP impressions per location, local pack visibility (snapshot tool, labelled), review count/rating trend, NAP consistency score (nap_check.py) |
| Healthcare | Appointments | Booking key events, calls (per branch) | Service/condition page clicks, doctor profile visibility, GBP actions per branch |
| Education | Applications, enquiries | Enquiry/application key events | Program page clicks, intake-season query visibility |
| Content/media | Ad revenue, subscriptions | Organic sessions × engagement, subscriptions | Clicks by topic cluster, Discover/News traffic, indexed article share |

## 12. Period comparisons

- **Equal-length windows:** compare 28 vs 28 days, or month vs the same month, never 31 vs 28 days without normalizing.
- **Same weekdays:** for short windows, align by weekday (weekly patterns are strong).
- **YoY vs MoM:** YoY removes seasonality but mixes in a year of site and market changes. MoM is more current but seasonal. Use YoY for seasonal businesses (travel, education intakes, Ramadan/Eid retail) and state the choice.
- **Seasonality in Arabic markets:** Ramadan and the two Eids move about 11 days earlier each Gregorian year, so a "same month last year" comparison may straddle Ramadan differently. Align by the event, not the calendar month, when it matters. Also watch school calendars, White Friday, and summer travel peaks.
- **Annotations:** maintain a timeline of site changes (from `07-changes/change-log.md`), tracking changes, and Google updates. Use the Google Search Status Dashboard (status.search.google.com) for confirmed core/spam updates and dates. Note an update as context, not as a cause, unless the evidence pattern supports it.
- **Data delays:** exclude the most recent 2–3 days from GSC comparisons.
- **Same filters and property** on both sides of the comparison.

## 13. Correlation vs causation

Rules for every claim in a report:
- "Clicks to the product group rose [X]% after the canonical fix" is a **correlation** unless other explanations are ruled out.
- Before attributing a change to SEO work, check: seasonality (YoY), Google updates in the window, tracking changes, brand campaigns (branded query spikes), competitor changes, site outages, and whether the change also happened on untouched page groups (a control).
- Use language that matches the evidence:
  - "coincided with" when only timing aligns;
  - "consistent with" when timing and the mechanism align, and controls didn't move;
  - "likely caused by" only when the mechanism, timing, a control group, and a URL-level check (e.g. URL Inspection shows the new canonical selected) all agree.
- These three tiers are the canonical causal ladder; reporting-framework.md §8 reuses them. "Likely caused by" is the top tier: never write "caused by" or "thanks to our work".
- Never present an estimated revenue impact unless it's built from the client's own conversion values, with the method shown.

**Measurement attribution is a different question.** It's about which channel or page the analytics data credits, not whether our work caused a change. Label every attributed number with one of:
- **Observed:** recorded directly (GSC clicks; GA4 session-scoped organic sessions and key events).
- **Assisted/modelled:** credit assigned by a model: GA4's attribution model (name it), conversion paths, or consent-mode modelling.
- **Inferred:** estimated from indirect data (ratios, third-party estimates).
- **Unavailable:** not tracked or no access. Say so; don't fill the gap.

None of these labels says our work caused the result. GA4 crediting Organic Search with a conversion is not evidence that an SEO change produced it. Causal claims always use the ladder above.

## 14. Using gsc_compare.py

`scripts/gsc_compare.py` compares two GSC Performance exports (period A and period B) by query or by page: it computes deltas, winners/losers, and CTR outliers.

```bash
python <skill-dir>/scripts/gsc_compare.py --help
```

English exports are recognized automatically. For an export from a Search Console interface in another language (e.g. Arabic), map the columns explicitly with `--columns`, using header names or 1-based column numbers, e.g. `--columns "key=1,clicks=2,impressions=3,position=5"`. Nothing is guessed, and a wrong or incomplete mapping is refused with a numbered list of the file's columns. Files saved by Excel as Windows-1256 or UTF-16 are read correctly, and comma, tab or semicolon delimiters are detected.

Workflow:
1. Export the same table (Queries or Pages) from GSC for both periods, with identical filters (search type, country, device), or one comparison-mode export. Save both under `data/` with the date ranges in the filenames.
2. Run the script with the options its `--help` shows. Save its output under `09-reports/YYYY-MM/` or `03-audit/evidence/`.
3. Interpret: the script finds movements, but explaining them is your job (section 13). Check whether losers are seasonal, cannibalized (another page gained the same query), or tied to a change in the change log.
4. Remember the UI export limit of 1,000 rows. For bigger sites, use API or bulk-export data and say which source the comparison used.
