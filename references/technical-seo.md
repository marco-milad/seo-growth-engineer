# Technical SEO

Can search engines discover, crawl, render, and index the pages that matter, and can they understand which version to show? Technical problems cap everything else: a perfect page that is not indexed earns nothing. Use this file in Stage 3 (audit), Stage 7 (execution), and Stage 8 (QA). Finding IDs use the `TEC-` prefix (`INT-` for hreflang/international). Buckets, confidence, priority, and status follow SKILL.md.

## Contents

1. [Evidence: raw HTML vs rendered checks](#1-evidence-raw-html-vs-rendered-checks)
2. [Audit order](#2-audit-order)
3. [Crawlability: robots.txt](#3-crawlability-robotstxt)
4. [XML sitemaps](#4-xml-sitemaps)
5. [Indexability](#5-indexability)
6. [Canonicalization and URL variants](#6-canonicalization-and-url-variants)
7. [Status codes, redirects, 404 / soft 404](#7-status-codes-redirects-404--soft-404)
8. [JavaScript rendering](#8-javascript-rendering)
9. [Next.js specifics](#9-nextjs-specifics)
10. [Other frameworks](#10-other-frameworks)
11. [Mobile](#11-mobile)
12. [Page speed and Core Web Vitals](#12-page-speed-and-core-web-vitals)
13. [HTTPS and security](#13-https-and-security)
14. [Structured data](#14-structured-data)
15. [Pagination and faceted navigation](#15-pagination-and-faceted-navigation)
16. [International / hreflang](#16-international--hreflang)
17. [Architecture, internal crawl depth](#17-architecture-internal-crawl-depth)
18. [Log analysis and crawl budget](#18-log-analysis-and-crawl-budget)
19. [Site migrations](#19-site-migrations)
20. [Indexing tools and gotchas](#20-indexing-tools-and-gotchas)
21. [Typical findings and severity](#21-typical-findings-and-severity)

---

## 1. Evidence: raw HTML vs rendered checks

Different tools see different versions of a page. State which one each finding is based on.

| Method | Sees | Good for | Limits |
|---|---|---|---|
| `scripts/site_check.py` | Raw server HTML + headers, no JavaScript | Status codes, redirects, `X-Robots-Tag`, metadata present in initial HTML, canonicals, hreflang, JSON-LD in source, robots.txt and sitemaps at scale | Does not execute JS: content or tags injected client-side appear "missing". That is a true finding for non-rendering crawlers (many AI crawlers, social previews), but not proof Google can't see it |
| `curl -sI` / `curl -sL -A "<UA>"` | Headers, redirect chain, response for a given user agent | Redirect chains, user-agent-dependent responses, header-level noindex | One URL at a time |
| GSC **URL Inspection** (index status + live test) | Google's indexed version and Google's rendered HTML, screenshot, resources | Ground truth for "is it indexed / which canonical did Google pick / can Googlebot render it" | Needs GSC access; one URL at a time in the UI; API has quotas (2,000/day, 600/min per property; Source: Search Console API Usage Limits, https://developers.google.com/webmaster-tools/limits, checked 2026-11-24) |
| **Rich Results Test** | Google-rendered HTML + detected structured data | Rendered metadata and rich-result eligibility without GSC access | Public URLs only; shows eligibility, not whether Google will display it |
| Headless browser (Playwright/Puppeteer, an existing Lighthouse) | Fully rendered DOM | Comparing raw vs rendered, CWV lab data, hydration-only content | Not Googlebot; install only with approval (SKILL.md tool protocol) |
| Screaming Frog (if licensed and available) | Raw or JS-rendered crawl | Large-scale crawl, orphan pages via GSC/GA integration | The user's licence and machine |

**Rule:** a "Confirmed issue" about indexing or rendering needs either first-party data (GSC) or a reproducible check that matches the claim. "Title missing in raw HTML" is confirmed by site_check; "Google can't see the title" needs URL Inspection or the Rich Results Test.

## 2. Audit order

Work top-down. Each layer depends on the one above it:

1. **Host and protocol.** Does exactly one canonical origin answer 200? Do the others 301 to it?
2. **robots.txt + sitemaps**: discoverability.
3. **Index status**: GSC Pages report if available; otherwise sample checks.
4. **Status codes and redirects** across sitemap URLs and internal links.
5. **Canonicals, duplicates, URL variants.**
6. **Rendering**: is the important content and metadata in the initial HTML?
7. **Mobile, speed, CWV.**
8. **Structured data.**
9. **Architecture, internal links, crawl depth.**
10. Specialty: international, pagination, facets, logs, migration, as scoped.

A P0 found in steps 1–3 (site-wide noindex, robots.txt `Disallow: /`, the production host serving 5xx) is reported to the user immediately, per SKILL.md.

## 3. Crawlability: robots.txt

Check:
- Fetch `/robots.txt` on every host and protocol variant. Expect a 200, or a 404 (allow all). A **5xx** on robots.txt can make Google pause crawling the site; treat a persistent 5xx as urgent.
- `Disallow` rules blocking revenue pages, CSS/JS needed for rendering, or `/_next/` and similar asset paths.
- Rules meant for staging that leaked to production (`Disallow: /`).
- `Sitemap:` lines present, absolute, and pointing at the right host.
- AI-crawler rules (`Google-Extended`, `GPTBot`, `OAI-SearchBot`, `ClaudeBot`, `PerplexityBot`, …) are a **business decision**. Record what exists; recommend a policy in [ai-search-visibility.md](ai-search-visibility.md); don't change it without G4.

Facts to keep straight:
- robots.txt controls **crawling, not indexing**. A disallowed URL can still be indexed (URL only) if linked. To keep a page out of the index, it must be crawlable and carry `noindex`.
- `noindex` inside robots.txt is not supported by Google.
- Blocking a URL in robots.txt also hides its `noindex` and its canonical from Google.

## 4. XML sitemaps

Check (site_check.py expands sitemap indexes and samples status codes):
- Only canonical, indexable URLs that return 200. No redirects, 404s, noindexed URLs, parameter duplicates, or other hosts.
- Each language version is listed (or hreflang is declared in the sitemap; see section 16).
- `lastmod` is real (it changes when content changes), not "now" on every build. Google uses `lastmod` only when it is consistently accurate. Ignore `priority` and `changefreq`; Google doesn't use them.
- Size limits: 50,000 URLs or 50 MB uncompressed per file. Split large sites by type (products, categories, articles) so GSC coverage can be read per segment.
- Submitted in GSC and Bing Webmaster Tools (submission needs G4 approval; see SKILL.md).
- Compare sitemap URLs against crawlable URLs. Important pages missing from the sitemap and sitemap URLs with no internal links (orphans) are both findings.

## 5. Indexability

A page is indexable when it returns 200, is not blocked by robots.txt, has no `noindex` (meta robots or `X-Robots-Tag` header), and its canonical points to itself (or is absent).

Sources of truth:
- **GSC Pages report** (Indexing → Pages). Read the reasons, not just the totals. "Discovered – currently not indexed" usually means low crawl demand or priority (weak internal linking, few links into a new domain, thin or duplicate pages). "Crawled – currently not indexed" usually points to quality or duplication. "Duplicate, Google chose different canonical than user" means conflicting signals.
- Without GSC, a `site:` search is only a rough, unreliable sample; label it Low confidence. The URL Inspection live test isn't available without access either. Report the gap as Missing data (`ANL-`).

Common causes:
- Leftover staging `noindex`.
- `X-Robots-Tag: noindex` set by the host or CDN on HTML.
- Canonical pointing to the homepage.
- Pages reachable only via JS-triggered navigation or search.
- Thin templated pages (empty categories, tag pages).
- Locale redirects that hide variants (section 9).

## 6. Canonicalization and URL variants

Check every variant collapses to one URL with a single **301** hop:
- `http://` → `https://`
- `www` ↔ apex (pick one)
- trailing slash vs none (pick one; framework default is fine if consistent)
- uppercase vs lowercase paths
- `index.html` / `index.php`
- tracking parameters (`utm_*`, `gclid`, `fbclid`), which should canonicalize to the clean URL
- hosting default domains (e.g. a `*.vercel.app`, `*.netlify.app`, or `*.pages.dev` preview/production alias still serving the site). Each should redirect, or at least canonicalize, to the custom domain.

Canonical tag rules:
- Absolute URL, in the initial HTML `<head>`, one per page, self-referencing on indexable pages.
- Must not point to a redirected, 404, or noindexed URL.
- Must not conflict with hreflang (each language version canonicals to itself, never to another language).
- Paginated pages self-canonicalize (not all to page 1).
- `rel=canonical` is a strong hint, not a directive. Google may choose differently when other signals (internal links, sitemap, redirects) disagree; align all of them.

## 7. Status codes, redirects, 404 / soft 404

- **301/308** for permanent moves, **302/307** only for genuinely temporary ones. Google treats long-standing temporary redirects much like permanent ones, but intent matters for other engines and for clarity.
- **Redirect chains**: more than one hop wastes crawl and dilutes clarity. Long chains hurt crawling (Source: Google, Crawl Budget Management, https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget, checked 2026-11-24). Point internal links and redirects directly at the final URL.
- **Redirect loops** and redirects to irrelevant pages (e.g. everything → homepage). Google may treat mass homepage redirects as soft 404s.
- **404 vs 410**: both fine for removed content. Don't redirect removed products to the homepage; redirect to the closest equivalent, or return 404/410.
- **Soft 404**: a "not found" or empty page that returns 200. Common with JS frameworks and empty search/category results. Detect it via GSC ("Soft 404") or by comparing thin 200 pages in site_check output.
- **5xx**: intermittent server errors on important pages reduce crawl rate. Check GSC Crawl stats (host status) when available.
- Internal links pointing to 3xx/4xx URLs: fix at the source.

## 8. JavaScript rendering

Google renders JavaScript, but rendering can be deferred, can fail on blocked resources or errors, and other crawlers often don't render at all. Goals:
- **Critical content, links, and metadata in the initial HTML** (SSR/SSG). That includes the title, meta description, canonical, robots, hreflang, JSON-LD, H1, main copy, and internal links.
- Real `<a href="…">` links for navigation; not `onClick` handlers or `href="#"`.
- Distinct URLs for distinct content; no fragment-only (`#/route`) routing for indexable pages.
- Correct HTTP status per route (a missing product must not return 200 with a "not found" component).
- Don't block JS/CSS needed for rendering in robots.txt.
- No content that appears only after user interaction (click to expand is fine if the content is in the DOM; content fetched only on click is not indexed).

How to test: compare site_check output (raw) with the URL Inspection rendered HTML, or the Rich Results Test. Differences in title, canonical, robots, hreflang, H1, or body copy are findings. Their severity depends on whether Google's render includes them.

## 9. Next.js specifics

First inspect the codebase: `package.json` (Next version), `app/` vs `pages/`, `next.config.*`, middleware (`middleware.ts`, or `proxy.ts` in newer versions; check the docs for the installed version), and i18n setup.

**App Router (`app/`)**
- Metadata comes from the `metadata` export or `generateMetadata()` in `layout`/`page`. Set `metadataBase` in the root layout so relative canonical and OG URLs resolve to the production origin, not a preview domain.
- Canonical and hreflang go in `alternates: { canonical, languages: { 'ar-EG': …, en: …, 'x-default': … } }`. A common bug is a canonical inherited from the layout, so every page canonicals to `/`. Child `metadata` objects override parent keys shallowly. Overriding `openGraph` in a page replaces the layout's whole `openGraph` object, which drops images and other defaults.
- **Streaming metadata (Next.js ≥ 15.2):** for user agents not on the `htmlLimitedBots` list, `generateMetadata` output can be streamed after the initial HTML instead of blocking. Next.js says HTML-limited bots get blocking metadata in `<head>`, and that JS-executing bots read streamed metadata correctly (Source: Next.js docs, htmlLimitedBots, https://nextjs.org/docs/app/api-reference/config/next-config-js/htmlLimitedBots, checked 2026-11-24). Verify the actual output: fetch raw HTML with a browser user agent and with a Googlebot user agent (`curl -A`), then compare with URL Inspection. Exactly which bots are on the default list: verify at time of use.
- `app/sitemap.ts` and `app/robots.ts` generate these files. Check they read production URLs, include every locale, exclude noindexed or empty routes, and emit real `lastmod` values. For large catalogues, use `generateSitemaps` to split them.
- **`notFound()` status:** if it is called before streaming starts, the response is a 404. If it is called after streaming has started (e.g. inside a Suspense boundary or under `loading.tsx`), the status stays **200**, and Next.js injects `<meta name="robots" content="noindex">` (Source: Next.js docs, not-found, https://nextjs.org/docs/app/api-reference/file-conventions/not-found, checked 2026-11-24). To get a true 404 for missing records, fetch and check the record in the page before any streamed boundary.
- Rendering modes: static/SSG and ISR give full HTML. Dynamic SSR is fine. Client components still render on the server, but data fetched in `useEffect` doesn't appear in the initial HTML. Flag any SEO-critical content that's loaded client-side.
- `redirect()` / `permanentRedirect()` give 307/308. Redirects in `next.config` support `permanent: true` (308).

**Pages Router (`pages/`)**
- Metadata via `next/head`, set per page. Check for duplicate `<title>` tags from `_app`/`_document` plus the page.
- `getStaticProps`/`getServerSideProps` → full HTML. Data fetched client-side → not in the initial HTML.
- `notFound: true` from data functions returns a real 404.
- Built-in i18n routing (`i18n` in next.config) can auto-redirect on `Accept-Language`. Check `localeDetection`.

**Locale middleware (both routers)**
- Avoid redirecting the root (or any URL) based on `Accept-Language` or IP alone. Googlebot mostly crawls from the US without an `Accept-Language` header, so it may never see other variants. Google advises against automatic redirects by presumed language (Source: Google, Managing multi-regional and multilingual sites, https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites, checked 2026-11-24). Prefer stable locale URLs, a visible language switcher, hreflang, and an `x-default`.
- If a root redirect is kept, it must be consistent, cacheable correctly (`Vary`), and every locale URL must stay directly reachable with a 200.

**Hydration-only content:** compare raw vs rendered for prices, stock, reviews, and FAQ blocks. If they render only on the client, they are invisible to non-rendering crawlers and are delayed for Google.

## 10. Other frameworks

- **React SPA (CRA/Vite, client-only):** usually one HTML shell for every route, so metadata is set client-side and every route returns 200. Recommend SSR/SSG (Next.js, Remix/React Router framework mode, Astro) or prerendering for indexable routes. Dynamic rendering (serving bots different HTML) is a workaround Google no longer recommends. Treat it as a temporary bridge only, with G4.
- **Vue / Nuxt:** Nuxt SSR/SSG is fine. Check `useHead`/`useSeoMeta` output in raw HTML, `nuxt.config` route rules, and `@nuxtjs/i18n` redirect behaviour (`detectBrowserLanguage`).
- **Angular:** SSR via Angular's server rendering/prerendering. Without it, the same issues as an SPA. Check `Meta`/`Title` service output in raw HTML.
- **Hosted CMS / site builders (Shopify, WordPress, Wix, Webflow…):** issues are usually templates, apps/plugins, and duplicate paths (e.g. Shopify `/collections/x/products/y` vs `/products/y`). Work within the platform's controls; don't propose a re-platform as a fix for SEO details.

## 11. Mobile

Google uses mobile-first indexing; the mobile version is what gets indexed. Check:
- Mobile and desktop serve the same content, links, structured data, and metadata. Hidden-on-mobile content counts as missing.
- Viewport meta, no horizontal overflow at ~360–390 px, readable font sizes, tap targets, no intrusive interstitials over the main content.
- Images and lazy-loaded content load without user interaction.

Google retired its standalone Mobile-Friendly Test (late 2023). Use Lighthouse, a real-device check, or the rendered screenshot in URL Inspection. Don't cite the retired tool.

## 12. Page speed and Core Web Vitals

Thresholds, assessed at the **75th percentile** of real page loads, mobile and desktop separately (Source: web.dev, Web Vitals, https://web.dev/articles/vitals, checked 2026-11-24):

| Metric | Good | Needs improvement | Poor |
|---|---|---|---|
| LCP (loading) | ≤ 2.5 s | 2.5–4.0 s | > 4.0 s |
| INP (responsiveness; replaced FID in March 2024) | ≤ 200 ms | 200–500 ms | > 500 ms |
| CLS (visual stability) | ≤ 0.1 | 0.1–0.25 | > 0.25 |

**Field vs lab.** Never mix them in one claim:
- **Field** (real users): GSC Core Web Vitals report, CrUX (the PageSpeed Insights top section, the CrUX API, the CrUX History API). This is what Google's page experience assessment uses. Low-traffic sites often have **no field data**; say so rather than substituting lab numbers.
- **Lab** (simulated): Lighthouse / the PSI lab section. Useful for diagnosis and before/after comparisons. TBT is a lab proxy for INP, not INP.
- Lab scores vary run to run. Use the same URL, device profile, and tool, and take the median of several runs for before/after QA.
- PSI's keyless API quota is often exhausted. Ask the user for an API key set as an environment variable (never written to files), or have them run pagespeed.web.dev manually.

Core Web Vitals are part of page experience signals. Google describes them as aligned with what its ranking systems reward, but relevance and content quality dominate. Frame CWV work by its user and conversion impact; don't promise ranking gains.

Usual fixes, by metric:
- **LCP:** server response time (TTFB, caching, CDN); the hero image (preload, `fetchpriority="high"`, correct sizing, AVIF/WebP, never lazy-load above the fold); render-blocking CSS/JS; web fonts (see the Arabic file for subsetting).
- **INP:** long main-thread tasks; heavy hydration; third-party scripts (chat widgets, tag managers, pixels); expensive event handlers.
- **CLS:** width/height or aspect-ratio on images and embeds; reserved space for banners and ads; font swap metrics (`size-adjust`); late-injected content above existing content.

## 13. HTTPS and security

- Valid certificate on every served host, HSTS where appropriate, no mixed content.
- HTTP → HTTPS 301 site-wide; internal links, canonicals, and sitemaps all use HTTPS.
- Check GSC **Security issues** and **Manual actions** when access exists. A hacked-content or manual-action finding is P0.
- Look for injected spam (unexpected pages in `site:` results, Japanese/pharma keyword hacks, cloaked redirects for mobile or Googlebot only). Compare responses across user agents.

## 14. Structured data

Use JSON-LD in the initial HTML. Mark up only content visible on the page. Validate with the Rich Results Test (Google features) and the Schema.org validator (syntax).

**Current Google rich result support changes often.** Check the live gallery before recommending a type (Source: Google, Structured data markup that Google Search supports, https://developers.google.com/search/docs/appearance/structured-data/search-gallery, checked 2026-11-24). As of 2026-11-24:

| Status | Types |
|---|---|
| Commonly useful and supported | Organization (logo, sameAs, contact), LocalBusiness, Product + Offer (product snippets, merchant listings), ProductGroup (variants), Review snippet / AggregateRating (with eligibility limits), BreadcrumbList, Article, VideoObject, Event, JobPosting, Recipe, Course list (carousel, ≥3 courses), Dataset (Dataset Search only), Discussion forum / Q&A page, ProfilePage, Software app, Image metadata |
| Retired / no longer shown | **FAQ rich results**: restricted to well-known, authoritative government and health sites (announced Aug 2023, in effect from Sept 2023), then deprecated: "no longer appear in Google Search starting May 7, 2026" (changelog, May 2026; documentation removed June 2026). Google still says it uses the markup for understanding (Sources: Google Search Central Blog, Changes to HowTo and FAQ rich results, https://developers.google.com/search/blog/2023/08/howto-faq-changes; Search documentation updates, https://developers.google.com/search/updates, checked 2026-11-24). **HowTo** (deprecated Sept 2023). **Sitelinks search box** (removed Nov 2024). **Book Actions (still used by a feature, per Nov 2025 update), Course Info, ClaimReview, Estimated Salary, Learning Video, Special Announcement, Vehicle Listing**: phase-out announced June 2025. **Practice Problem**: phased out from Jan 2026. Dataset markup is used only by Dataset Search, not Google Search (Sources: Simplifying the search results page, https://developers.google.com/search/blog/2025/06/simplifying-search-results; Update on our efforts to simplify the search results page, https://developers.google.com/search/blog/2025/11/update-on-our-efforts, checked 2026-11-24) |

Rules:
- Unsupported markup causes no errors or penalties. There's no need to rip it out, but don't sell new implementations of retired types as a rich-result win. FAQ content can still be valuable on the page for users and AI answers (see ai-search-visibility.md).
- Self-serving reviews (a business marking up reviews about itself on its own LocalBusiness/Organization pages) aren't eligible for review stars.
- Markup must match visible content (prices, availability, ratings). A mismatch is a spam-policy risk, not just an error.
- One consistent entity graph: `Organization`/`LocalBusiness` with `@id`, referenced by `WebSite`, `Product`, and `Article`, keeping NAP identical to GBP and the site (local-seo.md).

## 15. Pagination and faceted navigation

**Pagination**
- Google no longer uses `rel=next/prev` as an indexing signal. Give each page a unique, crawlable URL (`?page=2` or `/page/2`) with a self-canonical, linked via plain `<a href>`.
- "Load more" / infinite scroll must also have paginated URLs behind it, or items beyond the first batch are undiscoverable.
- Don't noindex page 2+ by reflex if those pages are the only path to deeper items.

**Faceted navigation** (filters: color, size, price, sort)
- Combinations explode the crawlable URL space and create near-duplicates. Decide per facet: **indexable landing page** (real search demand, e.g. "men's leather wallets"), **crawlable but canonicalized** to the base, or **not crawlable** (sort orders, price sliders, multi-select combinations), handled via robots.txt patterns or by not generating links.
- Keep a stable parameter order, so the same filter set always gives the same URL.
- Indexable facet pages need unique titles, H1s, and intro copy, plus enough products. Empty or one-item facet pages are thin.
- Base the decision on keyword data (keyword-research.md) and, where available, GSC/log evidence of crawl waste.

## 16. International / hreflang

The essentials are below. Arabic/English specifics, URL strategy, and market notes live in [arabic-and-multilingual-seo.md](arabic-and-multilingual-seo.md).
- Every language/region version lists **all** versions including itself, with codes in ISO 639-1 language format plus an optional ISO 3166-1 region (`ar`, `ar-EG`, `ar-SA`, `en`), plus `x-default`.
- **Reciprocity:** if page A references B, B must reference A, or Google ignores the pair (Source: Google, Tell Google about localized versions of your page, https://developers.google.com/search/docs/specialty/international/localized-versions, checked 2026-11-24).
- hreflang URLs must be canonical, indexable, and return 200. Each version self-canonicalizes.
- Implement it via `<link>` in the head, HTTP headers (for non-HTML), or the XML sitemap. Pick one method per URL set; mixing methods invites conflicts.
- Google doesn't use the HTML `lang` attribute or hreflang to *detect* a page's language; it uses the content. hreflang only maps alternates.
- site_check.py collects hreflang per URL; check reciprocity across the result set.

## 17. Architecture, internal crawl depth

- Important pages (money pages, top categories, location pages) should be reachable within ~3 clicks of the homepage through crawlable links. Deep pages earn less crawl and less internal authority.
- Orphan pages (in the sitemap or receiving traffic, with no internal links) are findings. Detect them by comparing sitemap/GSC/GA URLs with crawl-discovered URLs.
- Use hub-and-spoke linking: category ↔ subcategory ↔ product/article, breadcrumbs (with BreadcrumbList), and related-item links with descriptive anchors.
- Navigation rendered only by JS, or behind hover-only menus with no `<a href>`, may leave pages undiscoverable.
- URL structure: readable, stable, lowercase, hyphenated, in language folders. Don't restructure URLs that already rank without a strong reason; any change needs a redirect map (section 19).

## 18. Log analysis and crawl budget

**Crawl budget matters mainly for large sites.** Google's guidance targets sites with ~1M+ unique pages changing about weekly, or ~10k+ pages changing very rapidly (Source: Crawl Budget Management, https://developers.google.com/search/docs/crawling-indexing/large-site-managing-crawl-budget, checked 2026-11-24). For a typical small or medium site, "Discovered – not indexed" is a priority/quality/linking problem, not a budget problem. Don't sell crawl-budget work to a 200-page site.

**Logs** (only when the user supplies them; they can contain personal data, so handle per SKILL.md):
- Verify Googlebot by reverse DNS or Google's published IP ranges; user-agent strings are spoofed.
- Questions to answer: which sections get crawled and how often; crawl waste on parameters, facets, or redirects; 4xx/5xx served to Googlebot; important pages never crawled; time from publish to first crawl.
- Without logs, use the GSC **Crawl stats** report (requests by response, file type, purpose, and host status) as the first-party proxy.

## 19. Site migrations

Migrations cause most catastrophic traffic losses. Any domain change, URL restructure, platform change, HTTPS move, or locale restructure is a high-risk change set that requires a dedicated G4 proposal.

1. **Before:** export a baseline (GSC performance by page, GA4 organic landing pages, a full URL list from crawl + sitemap + GSC + analytics + backlink tool). Identify the top pages by clicks, conversions, and links.
2. **Redirect map:** one-to-one, old URL → closest new equivalent, with 301/308, no chains. Test it on staging against the full old URL list.
3. **Keep the signals:** titles, content, structured data, internal links, and hreflang carried over; canonicals and sitemaps updated to the new URLs; staging noindex removed at launch; analytics and GSC verification moved over.
4. **At launch:** for a domain move, verify the new property and use GSC's Change of Address tool. Submit the new sitemaps (with approval). Keep the old sitemap briefly so Google recrawls the redirects.
5. **After:** monitor 404s, the redirect hit list, the indexed counts of both properties, and clicks by page group, daily for 2 weeks and weekly for 2–3 months. Keep the redirects for at least a year, preferably permanently.

### 19a. Diagnosing a migration that already happened (traffic dropped after a redesign or URL change)

Common in practice: the user arrives months later with "traffic dropped X% since the redesign". Treat the drop as **Needs investigation** until the evidence separates the causes. Don't assume the migration caused it.

1. **Secure the history first.** Search Console keeps 16 months. If the pre-change period has partly aged out, ask for the oldest window still available plus the most recent equal-length window. State the shortened baseline as a limitation, and use GA4 or older reports for earlier history if they exist. UI exports are capped at 1,000 rows per table: on large sites, filter by folder (`/services/` vs `/solutions/`) to get the pages that matter. Ask immediately for these exports, before the pre-change months age out:
   - Performance by page and by query, comparing an equal-length window before vs after, plus the same period a year earlier for seasonality.
   - The Pages (indexing) report, with example URLs for "Not found (404)", "Page with redirect", and "Duplicate…" reasons.
2. **Rebuild the old URL list** from the GSC pages export (pre-change period), GA4 landing pages, backlink tool "top pages", old sitemaps, the CMS export, and, when nothing else exists, public archives such as the Internet Archive's Wayback Machine (public data; label as such).
3. **Test every old URL** with `python <skill-dir>/scripts/site_check.py https://<site-host> --urls old-urls.txt --max-pages <number of URLs in the list>`. The site root comes first, and `--max-pages` must cover the whole list, because the default cap of 200 silently truncates longer lists. Old URLs on another host (a domain move) are skipped and reported unless you add `--allow-off-host`, or pass the old domain as the site. Use a new `--out` folder for each run. Check for:
   - 404s and soft 404s.
   - Redirect chains.
   - Redirects to the homepage or to irrelevant pages (those are treated like soft 404s).
   - 302s that should be 301s.
   - Redirects to URLs that are noindexed or canonicalized elsewhere.
4. **Compare page groups:** which old pages lost clicks, and do their new equivalents receive them? A loss concentrated on URLs that 404 or redirect badly points to the migration. A broad loss across unchanged pages points elsewhere: an algorithm update, seasonality, tracking, or demand.
5. **Check what else changed in the redesign:**
   - Content removed or thinned.
   - Internal links and navigation reduced.
   - Titles and H1s rewritten.
   - Structured data dropped.
   - Rendering moved to client-side.
   - hreflang broken.
   - The analytics tag missing on new templates. This shows up as a drop in GA4 but not in GSC.
6. **Check the external context:** confirmed Google updates in the window (Search Status Dashboard), seasonality, and campaign or brand changes.
7. **Links to old URLs:** list top-linked old URLs from GSC Links or a backlink tool. Each must redirect one-to-one to its closest equivalent.
8. **Findings and priority:**
   - Old high-value URLs returning 404: usually P1, urgent, because link equity and rankings keep decaying while they're broken.
   - Site-wide de-indexing, a manual action, or Googlebot being blocked: P0.
   - Fixes (redirect map repairs, restored content) go through G4. Measure recovery against the pre-change baseline by page group.

## 20. Indexing tools and gotchas

Field notes, labeled by type:
- **Sitemap "Couldn't fetch" on day one** (field observation + official docs): a freshly submitted sitemap can show "Couldn't fetch" while it's actually still pending. Confirm with a URL Inspection live test of the sitemap URL. If the page fetch succeeds and crawling is allowed, wait. If it fails, fix and resubmit. Google retries for a few days after a real failure (Source: Search Console Help, Sitemaps report, https://support.google.com/webmasters/answer/7451001, checked 2026-11-24).
- **GSC verification:** the HTML-file method can fail on framework hosts that rewrite unknown paths or add trailing slashes (field observation). Prefer a **DNS TXT record** (a domain property covers all hosts and protocols) or the **HTML meta tag** (e.g. a Next.js `metadata.verification.google` value from an env var). Verification changes are G4 items.
- **Indexing API:** officially only for pages with `JobPosting` or `BroadcastEvent` embedded in a `VideoObject`. Don't use it to push ordinary pages (Source: Google, Indexing API, https://developers.google.com/search/apis/indexing-api/v3/using-api, checked 2026-11-24).
- **URL Inspection "Request indexing"** has a small daily per-property quota in the UI (field observation: roughly ten requests a day before "quota exceeded"; the exact limit is unpublished). Use it for a few priority URLs after fixes, not as an indexing strategy. Each request needs explicit approval. The owner usually clicks it, which is the owner-executed path. The full G4 proposal applies if you execute it yourself (SKILL.md, Approval gates).
- **IndexNow** notifies Bing, Yandex, and other participating engines of changed URLs. **Google doesn't use IndexNow.** Implement it with a key file at the root; ping on publish or update. A first submission may return 403 until the key file is verifiable (field observation). Approval (SKILL.md, Approval gates):
  - Setup and any configuration change are a code change and need full G4.
  - Automatic pings from the approved setup are covered by that approval, with the scope recorded in the change log (no per-ping approval).
  - Each manual one-off submission (IndexNow or Bing URL Submission) needs explicit approval.
  - Bulk or submit-all submissions need full G4.
- **Bing Webmaster Tools** can import sites from GSC, which saves a separate verification.
- **Removals tool** in GSC hides URLs temporarily (about 6 months); it doesn't de-index permanently. Pair it with noindex/404/410. It's a high-risk action that requires G4.

## 21. Typical findings and severity

Bands below are indicative only. The SKILL.md formula decides P1–P3 from the actual scores. P0 applies only to SKILL.md's override conditions (e.g. site-wide indexing loss).

| Finding | Typical bucket / indicative band |
|---|---|
| Site-wide `noindex` or `Disallow: /` on production | Confirmed, **P0** (override: site-wide indexing loss) |
| Production served on multiple hosts with no redirect/canonical (e.g. preview domain indexed) | Confirmed, P1 |
| Money-page template missing from initial HTML (CSR-only) | Confirmed (raw) / Potential (Google) until URL Inspection confirms |
| Canonical on every page → homepage | Confirmed, P1 (P0 only if it's already causing site-wide indexing loss) |
| Missing records return 200 (soft 404) | Confirmed, P1–P2 |
| Sitemap full of redirects/404s/noindex URLs | Confirmed, P2 |
| Redirect chains on internal links | Confirmed, P2–P3 |
| Locale redirect by Accept-Language hides variants | Potential until verified with URL Inspection / crawl, P1 |
| hreflang not reciprocal / wrong codes | Confirmed, P2 (P1 if wrong language ranking in a target market) |
| CWV poor in field data on key templates | Confirmed, P2 (P1 if conversion-critical) |
| No field CWV data | Missing data (not a problem in itself) |
| Retired schema type implemented (FAQ, HowTo) | Opportunity to stop spending effort, not an error |
| Faceted URLs crawlable at scale on a large catalogue | Potential → Confirmed with GSC/log evidence |
