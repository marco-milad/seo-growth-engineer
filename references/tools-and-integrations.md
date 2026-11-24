# Tools and Integrations (Stage 2: Access and Data Collection)

A skill grants no access to anything. This file explains how to find out what is actually available in the current environment, how each SEO data source can be connected, what each one contributes and where it stops, and how to record all of it in `02-access-and-data.md` (template: `templates/access-and-data-template.md`). SKILL.md's "Tool and data access protocol" is the short version; this is the detail.

Status labels: **official** = provided by the vendor; **community** = third-party/open-source, unvetted. Claims about tools change quickly. Items marked "verify at time of use" weren't confirmable on 2026-11-24.

## Contents

1. Environment inspection procedure
2. Access-status classification
3. Rules: installation, secrets, browsers
4. Tool reference (one entry per tool)
5. Exports and user-supplied data
6. Public competitor data
7. Extending the skill with a new tool
8. 02-access-and-data.md checklist

## 1. Environment inspection procedure

Do this at the start of Stage 2, before asking the user for access.

1. **Your own tool list.** Look at the tools available in this session for MCP tools related to Search Console, Analytics, Business Profile, Ahrefs, Semrush, Bing, a browser (e.g. Claude in Chrome), docs/sheets connectors, or a database. Tool names usually follow `mcp__<server>__<tool>`. A tool appearing in the list is "available but untested" until a harmless read call succeeds (e.g. list properties or accounts).
2. **Local CLIs, without installing anything:**
   - `python --version`, `node --version`
   - Lighthouse: `npx --no-install lighthouse --version` (fails instead of downloading if absent); also `lighthouse --version`
   - Screaming Frog: look for `ScreamingFrogSEOSpiderCli.exe` (Windows) or `screamingfrogseospider` (Linux/macOS) on PATH or in the default install folder
   - Browsers for headless checks: system Chrome/Edge paths
   - `gcloud --version` (if Google Cloud APIs might be used)
3. **Environment variables: check presence only, never print values.**
   - Bash: `[ -n "$PSI_API_KEY" ] && echo "PSI_API_KEY is set" || echo "not set"`
   - PowerShell: `if ($env:PSI_API_KEY) { "PSI_API_KEY is set" } else { "not set" }`
   - Never `echo $VAR`, `env`, `printenv`, or `cat .env`. Reading `.env.example` (names only) is fine.
4. **Project files:** existing exports (`*.csv`, `*.xlsx`) from GSC/GA4/Ahrefs/Semrush/Screaming Frog, previous audits, the engagement folder's `data/`.
5. **Repository / CMS:** is the site's code in the working directory? Is there a deployment config (Vercel/Netlify), a CMS admin the user can operate?
6. **Record** each source in `02-access-and-data.md` with its status (section 2), the date checked, and the method.

## 2. Access-status classification

| Status | Meaning | Next action |
|---|---|---|
| **Verified** | A read call or file read succeeded today | Use; record data date and scope |
| **Available, untested** | The tool/file exists but hasn't been exercised | Test with a harmless read before relying on it |
| **Needs user action** | Requires a grant, an export, an API key the user sets, or an MCP the user connects | Give the exact steps (section 4); continue with other sources |
| **Unavailable** | Not obtainable in this engagement | Record the limitation and its effect on confidence; pick an alternative |

For every source also record: **data freshness** (date range and pull date), **scope** (which property/host/locations), and **confidence** impact (e.g. "no GSC → Google-side indexing status (what Google actually indexed) at most Medium confidence; a reproducible live check, such as `noindex` in the HTML, is still High").

## 3. Rules: installation, secrets, browsers

- **Never install** MCP servers, npm/pip packages, browser extensions, CLIs, or WordPress/Shopify apps without first explaining what it is, why it's needed, the alternatives, and getting approval. Prefer what already exists.
- **Three kinds of access** (defined in SKILL.md, Tool and data access protocol, rule 7). Every "Access" line in this file uses them:
  - **(a) An authorized human account:** a person on the engagement whom the property owner adds as a user, viewer or manager. Every role, viewer or manager instruction below applies only to this case.
  - **(b) A connector or service identity the user configures:** an API or MCP connector the user signs into, or a service account the user creates and grants access to. It's used only if the environment supports it and a real call has verified it.
  - **(c) Claude itself:** has no Google account and can never be added, invited or made a manager.

  When Claude is doing the analysis without a verified (b), the routes are, in order:
  1. The user exports reports (give exact click paths; section 5).
  2. The user configures (b), after you explain the option and they approve.
  3. The user shares screenshots.
  4. With explicit authorization, a read-only look in the user's own logged-in browser.
- **Secrets:** never ask for passwords. Prefer delegated access, (a) or (b), or OAuth flows the user completes. API keys are set by the user as environment variables or in the MCP config. Never pasted into chat, written into files, reports, evidence, the skill, or command lines that get logged. If a user pastes a secret, don't repeat it; suggest they rotate it.
- **Least privilege:** ask for read/restricted roles for audits. Write access only for approved Execution work.
- **Research browsing is isolated.** Competitor research, SERP checks, and documentation lookups use plain web fetches or an isolated, logged-out browser profile (e.g. headless Chrome/Edge with a fresh temporary profile). They never use a browser session holding a client's logged-in accounts, because one stray click or search there touches a live business account.
- **Logged-in client sessions** (e.g. Claude in Chrome on the user's browser) are used only with explicit authorization, read-only by default. Re-take a screenshot before every click (panels shift after modals close), and never click Save/Verify/Request access/Transfer/Accept without a G4 approval for that exact action.
- **Terms of service:** respect robots.txt and rate limits for crawling and scraping. Don't scrape Google SERPs at scale. Use official APIs or the user's tools.

## 4. Tool reference

### Google Search Console (official, free)
- **Contributes:** first-party Google Search performance (queries, pages, countries, devices, search appearance), indexing status and reasons, URL Inspection (Google-selected canonical, rendered HTML, last crawl), sitemaps status, links sample, Core Web Vitals field groups, manual actions, security issues, crawl stats, the Generative AI performance report, branded/non-branded filter (eligible properties).
- **Domains:** Technical, On-page, Content, Analytics, Off-page (links sample), AI-search.
- **Access:** exports from the user, a connector the user sets up, or, when a human consultant is involved, the client adds that person's Google account as a user (Restricted is enough for audits; Full for sitemap submission/inspection actions; Owner never needed). The Domain property is preferred.
- **Connection:** UI; exports (CSV/Sheets/Excel); Search Console API (Search Analytics, URL Inspection, Sitemaps); BigQuery bulk export (client's Cloud project). **MCP:** no official Google Search Console MCP server found as of 2026-11-24; community servers exist (unvetted; needs approval to install, OAuth by the user). (Third-party roundups, e.g. https://www.popmcp.com/blog/best-seo-mcp-servers/, checked 2026-11-24, which is not authoritative. Verify at time of use.)
- **Limits:** 16-month retention; anonymized queries excluded from rows; UI exports 1,000 rows; Search Analytics API row limits (about 50k rows/day/site/search type per a 2022 post); URL Inspection API 2,000/day and 600/minute per property. (Source: Usage Limits, https://developers.google.com/webmaster-tools/limits, checked 2026-11-24.) Details in analytics-and-measurement.md.
- **Alternatives:** Bing Webmaster Tools for a second index view; crawl-based indicators for indexing (lower confidence).

### Google Analytics 4 (official, free)
- **Contributes:** organic sessions, landing pages, engagement, key events (conversions), revenue, the AI Assistant channel.
- **Domains:** Analytics, Content, CRO input.
- **Access:** exports from the user, or (b) a connector or service identity the user configures. For (a), a human account: the Viewer role on the property (Analyst for sharing explorations; Editor only to apply a configuration change approved through full G4, such as key events). Claude itself is never given a role. Adding any person needs the user's approval of their identity and access role first.
- **Connection:** UI; exports; GA4 Data API; BigQuery export. **MCP:** official open-source Google Analytics MCP server (`googleanalytics/google-analytics-mcp`, PyPI `analytics-mcp`), read-only by default with core tools such as `run_report`, `get_account_summaries`, and `run_realtime_report`; uses Application Default Credentials set up by the user. Google's MCP catalogue notes it isn't an officially *supported* Google product. (Sources: Try the Google Analytics MCP server, https://developers.google.com/analytics/devguides/MCP; https://github.com/googleanalytics/google-analytics-mcp, checked 2026-11-24.)
- **Limits:** Data API quotas (tokens per property), thresholding with Google signals, consent-mode data loss, data retention for explorations.
- **Alternatives:** server logs; platform analytics (Shopify, WordPress plugins), labelled as such.

### Google Business Profile (official, free)
- **Contributes:** listing data (categories, hours, attributes, services/products), reviews, photos, posts, and performance (Search/Maps impressions, calls, directions, website clicks, bookings, monthly search keywords).
- **Domains:** Local, Analytics.
- **Access:** Performance exports and screenshots from the owner, or (a), a human account with the Manager role on the location or business group (the owner stays with the client). Claude itself is never made a manager. Read-only use by default. Every edit needs explicit approval: the owner-executed path when the owner makes it, and the full G4 proposal when anyone else does or when it changes the business name, address or primary category (SKILL.md, Approval gates). Never change ownership, managers, or verification without explicit authorization.
- **Connection:** UI (business.google.com / Search & Maps); Business Profile APIs, which require an **application for API access**. Eligibility per Google: a verified, active profile for 60+ days, a website listed on the profile, a Google Cloud project, and an applicant email listed as an owner/manager (domain matching the website). Review takes up to ~14 days. The project quota shows 0 QPM until approved, 300 QPM after. (Sources: Prerequisites, https://developers.google.com/my-business/content/prereqs; FAQ, https://developers.google.com/my-business/content/faq, checked 2026-11-24.) Performance metrics come from the Business Profile Performance API (daily metrics; monthly keyword impressions). **MCP:** no official Google Business Profile MCP found (verify at time of use).
- **Limits:** API approval friction; some features vary by country/category; keyword impressions shown as thresholded values.
- **Alternatives:** public listing observation (low/medium confidence), screenshots supplied by the client, Insights exports by the client.

### Ahrefs (official vendor, paid)
- **Contributes:** backlink index (referring domains, anchors, new/lost), organic keyword and traffic **estimates**, keyword difficulty and volume **estimates**, competitor gaps, Site Audit crawler, rank tracking.
- **Domains:** Off-page, Keyword research, Competitor analysis, Technical (Site Audit).
- **Access:** the client's or the agency's subscription. Ahrefs Webmaster Tools (free) covers verified owned sites with limited data.
- **Connection:** UI exports; API v3; **official remote MCP server** at `https://api.ahrefs.com/mcp/mcp`, available on paid plans from Lite upward. MCP, Ahrefs Connect, and API v3 share the plan's API units (a minimum of 50 units per call; monthly units vary by plan). Ahrefs' docs say unsupported bridges/custom clients for the MCP endpoint aren't permitted, so use a documented client setup. (Sources: What is Ahrefs MCP, https://docs.ahrefs.com/en/mcp/docs/introduction; Getting started with Ahrefs MCP, https://help.ahrefs.com/en/articles/13913559-getting-started-with-ahrefs-mcp, checked 2026-11-24.)
- **Limits:** third-party estimates (label them); unit consumption; index coverage differs from Semrush.
- **Alternatives:** Semrush; GSC Links + Bing backlinks (first-party samples); Ahrefs Webmaster Tools.

### Semrush (official vendor, paid)
- **Contributes:** keyword database and volume **estimates**, position tracking, competitor domain analytics, backlink analytics, Site Audit, local listing tools (add-ons).
- **Domains:** Keyword research, Competitor analysis, Off-page, Technical (Site Audit), Local (add-ons).
- **Access:** a subscription; API access requires API units.
- **Connection:** UI exports; Semrush API; **official Semrush MCP**. Requests consume the same API units as direct API calls, with no extra MCP fee, and the cost varies by report. The developer docs list the endpoint `https://mcp.semrush.com/v2/mcp` (some Semrush pages still show v1), and auth details differ between pages (API key vs OAuth). Check the current developer docs when configuring. (Sources: Semrush MCP overview, https://developer.semrush.com/api/v4/introduction/semrush-mcp/; https://www.semrush.com/kb/1618-mcp, checked 2026-11-24.)
- **Limits:** estimates; unit costs (Site Audit MCP requests can be expensive); database coverage varies by country. Check that the Egypt/Saudi databases have adequate data for the niche.
- **Alternatives:** Ahrefs; Google Keyword Planner; GSC queries.

### Screaming Frog SEO Spider (official vendor; free up to 500 URLs, paid licence)
- **Contributes:** full-site crawl: status codes, redirects, canonicals, directives, titles/meta/headings, hreflang, structured data, internal links and depth, JavaScript rendering (licensed), custom extraction, API integrations (GSC/GA/PSI), sitemap generation.
- **Domains:** Technical, On-page, International.
- **Access:** installed by the user. The free version crawls up to 500 URLs with restricted configuration, no saving, and no JS rendering. (Source: Screaming Frog SEO Spider, https://www.screamingfrog.co.uk/seo-spider/, checked 2026-11-24.)
- **Connection:** GUI exports; headless CLI (`ScreamingFrogSEOSpiderCli.exe --crawl <url> --headless --output-folder <dir> --export-tabs ...`). Whether CLI save/exports work on the free tier: verify at time of use. (Source: SEO Spider user guide, https://www.screamingfrog.co.uk/seo-spider/user-guide/general/, checked 2026-11-24.)
- **Limits:** a desktop app; memory-bound on huge sites; crawl politeness settings matter.
- **Alternatives:** `scripts/site_check.py` (raw HTML, sample-based); Ahrefs/Semrush Site Audit; Sitebulb (paid).

### PageSpeed Insights (official, free)
- **Contributes:** Lighthouse lab data plus CrUX field data (URL and origin) when available.
- **Domains:** Technical (performance, CWV).
- **Access:** none for the web UI (pagespeed.web.dev). The API works without a key, but keyless calls often hit quota errors (HTTP 429). A free API key from a Google Cloud project (Credentials → Create credentials → API key) fixes it. The user creates it and sets it as an environment variable. (Source: Get Started with the PageSpeed Insights API, https://developers.google.com/speed/docs/insights/v5/get-started, checked 2026-11-24.) Check the exact daily quota in the Cloud Console, as it wasn't confirmed from the docs.
- **Limits:** lab variance between runs; field data only for URLs/origins with enough Chrome traffic.
- **Alternatives:** local Lighthouse; CrUX API.

### Lighthouse (official, open source)
- **Contributes:** lab performance, accessibility, best practices, and SEO basics, with repeatable settings.
- **Domains:** Technical.
- **Access:** local CLI (Node) or Chrome DevTools. Check for an existing install with `npx --no-install lighthouse --version`. Installing it is an approval decision.
- **Limits:** lab only, not real users; the SEO category score is a basic checklist, not an SEO assessment. Report the device, throttling, and the median of several runs.
- **Alternatives:** PSI; WebPageTest.

### CrUX: Chrome UX Report (official, free)
- **Contributes:** real-user Core Web Vitals (LCP, INP, CLS) at the 75th percentile, by origin or URL, phone/desktop.
- **Connection:** CrUX API and CrUX History API share 150 queries/minute per Google Cloud project, free, and the quota can't be increased. The History API provides about six months of weekly history (verify the current window). The BigQuery CrUX dataset is monthly at origin level. (Sources: CrUX API, https://developer.chrome.com/docs/crux/api; CrUX History API, https://developer.chrome.com/docs/crux/history-api, checked 2026-11-24.)
- **Limits:** eligibility thresholds. Small sites often have no data, so say "not enough field data" rather than substituting lab numbers as if they were field data.

### Bing Webmaster Tools (+ IndexNow) (official, free)
- **Contributes:** Bing performance, indexing, backlinks, site scan, URL submission, the AI Performance report (public preview, 2026) for Copilot/partner AI answers. (Source: https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview, checked 2026-11-24.)
- **Access:** verify the site, or import from GSC.
- **Connection:** UI; Bing Webmaster API / URL Submission; **IndexNow** (a key file on the site plus pings to notify participating engines of changes; Google doesn't use IndexNow). Approval (SKILL.md, Approval gates):
  - Setting up or changing the IndexNow configuration is a code change and needs full G4.
  - Automatic pings from that approved setup are covered by its approval (record the scope in the change log), with no per-ping approval.
  - Each manual one-off submission (IndexNow or the Bing URL Submission tool) needs explicit approval.
  - Bulk or submit-all submissions need full G4.
- **Limits:** no confirmed API for the AI Performance report (verify at time of use).

### Google Keyword Planner (official, free with a Google Ads account)
- **Contributes:** keyword ideas and search volume. Accounts without active ad spend typically see volume **ranges** rather than exact figures (verify for the account in use). Location/language targeting is useful for Arabic markets.
- **Access:** the user's Google Ads account.
- **Limits:** groups close variants; built for advertisers; ranges aren't precise volumes. Label the source and any range.

### Google Trends (official, free)
- **Contributes:** relative interest over time (0–100 index), regional interest, rising queries, seasonality (Ramadan/Eid peaks), and comparisons of spellings/dialect variants.
- **Limits:** relative, not absolute volumes; sampled; low-volume Arabic terms may show no data. Google has announced a Trends API in limited alpha (verify availability at time of use).

### Rich Results Test / Schema Markup Validator (official, free)
- **Rich Results Test** (Google): checks eligibility for Google-supported rich result types, on a URL or code snippet, with rendering.
- **Schema Markup Validator** (schema.org): generic schema.org validation for all types, including ones Google doesn't use for rich results.
- Use both: the validator for correctness, the Rich Results Test for Google eligibility. Don't upload confidential client code to third-party validators without the user's OK.

### Google Indexing API (official), and why it is usually *not* the answer
Only for pages with `JobPosting` or `BroadcastEvent` (embedded in `VideoObject`). Default quota 200 publish requests/day per project. Using it for ordinary pages is outside its documented scope. (Source: Indexing API quota, https://developers.google.com/search/apis/indexing-api/v3/quota-pricing; How to Use the Indexing API, https://developers.google.com/search/apis/indexing-api/v3/using-api, checked 2026-11-24.) For normal pages, use sitemaps, internal links, and GSC URL Inspection requests (small manual quota, with approval).

### Browser automation (Claude in Chrome, Playwright, headless Chrome/Edge)
- **Contributes:** rendered-DOM checks, mobile/RTL screenshots, viewing logged-in tools when the user authorizes it (GSC, GA4, GBP UIs) when no API/MCP exists.
- **Rules:** section 3. An isolated profile for public research; the user's logged-in session only with explicit authorization, read-only by default, and re-screenshot before clicks. Installing Playwright browsers or extensions needs approval.
- **Limits:** slower; UI changes break flows; screenshots may contain personal data (redact).

### CMS and repository access
- **Contributes:** the ability to implement (Execution mode), source-of-truth inspection of templates, rendering, and metadata.
- **Access:** a repo in the working directory, or CMS accounts the user operates or grants (an editor role, not admin, when possible). Staging preferred.
- **Rules:** G4 per change set; see seo-implementation-qa.md.

## 5. Exports and user-supplied data

When direct access is unavailable, ask for exports. They're often faster and safer:

| Source | Export to request |
|---|---|
| GSC | Performance → Queries and Pages tables (Web, last 3 months + comparison period, with country/device filters as needed); Pages report examples per reason; Links export |
| GA4 | Traffic acquisition and Landing page reports filtered to Organic Search, with key events, same windows |
| GBP | Performance export per location; screenshots of listing fields |
| Ahrefs/Semrush | Referring domains, backlinks, organic keywords (labelled estimates), competitor overview |
| Screaming Frog | Internal (all), response codes, canonicals, directives, hreflang, structured data |
| CMS | URL list/product export with titles, descriptions, slugs, stock status |

Click paths to give the user (UI labels change, so confirm against the current interface if the user can't find a step):
- **GSC Performance:** Performance → Search results → set the search type (Web) and date range. For a comparison, open the Date filter → Compare tab. Then pick the Queries or Pages tab → Export (top right) → CSV or Google Sheets. The UI export is capped at 1,000 rows per table, so for bigger sites ask for filtered exports (e.g. per folder) or API/bulk-export data.
- **GSC indexing:** Indexing → Pages → click a reason (e.g. "Not found (404)") → Export the example URLs.
- **GSC links:** Links → "Top linked pages" (external) → Export.
- **GA4 organic landing pages:** Reports → Engagement → Landing page → add a filter: Session default channel group = Organic Search → set dates → Share this report → Download file → CSV.
- **GBP performance:** from the profile in Search or Maps → Performance → choose dates → screenshot or download where offered.

Handling:
- Save to `data/` with source and date range in the filename. Note who supplied it and when.
- CSV/XLSX/JSON: read directly (Python standard library for CSV/JSON; for XLSX ask the user to save as CSV, or use an existing library with approval). PDFs: read the text; treat figures as reported by that document, with its date.
- Treat supplied reports from previous agencies as claims to verify, not as facts.
- Strip personal data you don't need (customer emails in GA4 or CMS exports).

## 6. Public competitor data

Available without access: competitors' live pages (structure, schema, content depth), their robots/sitemaps, public GBP listings and reviews, social profiles, press mentions, and SERP observations from manual checks (noting the date, location, language, and device, and that personalization and location affect results). Third-party estimates of competitor traffic come only from a connected tool and are labelled as such. Keep crawling of competitor sites light and polite (small samples, robots.txt respected).

## 7. Extending the skill with a new tool

To add a tool (e.g. a new MCP, a rank tracker, a log analyzer), add an entry to section 4 with:

```text
### <Tool name> (official | community, free | paid)
- Contributes: <data/capabilities>
- Domains: <On-page | Off-page | Technical | Local | Analytics | lenses>
- Access: <role/plan needed; who grants it>
- Connection: <API | MCP (endpoint/package, official?) | export | UI>; auth method (user-completed OAuth / env var name)
- Useful data: <specific reports/endpoints to pull>
- Limits & quotas: <with source + date>
- Alternatives: <fallbacks>
- Verified: <date, what call succeeded> | not yet verified
```

Then:
- Map its outputs to the finding schema (which `data_source` label, which confidence: first-party = High possible; estimates = Medium at most).
- If it produces files, define the naming convention under `data/`.
- If a deterministic transform is repeated across engagements, consider a script in `scripts/` (standard library only) and document it in SKILL.md.
- Never mark it "connected" in any document until a real call has succeeded in the current environment.

## 8. 02-access-and-data.md checklist

- [ ] Every candidate source listed with status (Verified / Available, untested / Needs user action / Unavailable) and the date checked.
- [ ] For verified sources: scope (property/host/locations), date range, pull date.
- [ ] Required user actions written as exact steps, ordered by value (usually GSC first, then GA4, then GBP if local, then backlink tool).
- [ ] Access limitations and their effect on confidence per domain.
- [ ] No secrets in the document, and none requested in chat.
- [ ] Any proposed installs listed as *options awaiting approval*, not done.
- [ ] Next step: start the audit with what's available. Missing data never blocks the whole audit.
