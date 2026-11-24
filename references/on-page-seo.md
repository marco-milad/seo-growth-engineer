# On-Page SEO

Load this when the On-Page module is in scope. That's almost always, at a depth scaled to the site. It covers what is on each page and how pages relate to each other: titles, descriptions, headings, intent fit, content quality, images, internal links, URLs, duplication, cannibalization, and conversion relevance.

It assumes the conventions in `SKILL.md`: finding schema, ID prefixes, buckets, confidence, priority model, and gates. It doesn't repeat them.

Contents:
1. Inputs
2. Audit procedure
3. Check-by-check guidance
4. Typical findings
5. Implementation guidance
6. Validation
7. Pitfalls and myths

---

## 1. Inputs

| Input | Why | If missing |
|---|---|---|
| List of important URLs/templates (from discovery: money pages, categories, services, locations) | On-page work is judged against the pages that matter | Build it from the sitemap + main navigation, then confirm with the user at G1/G2 |
| Keyword-to-page map (`04-research/keyword-map.csv`) | Placement, intent, and cannibalization checks need a target per page | Do the structural checks now (missing, duplicate, length, H1 count). Run placement/intent checks after keyword research, and label them "pending keyword map" |
| GSC Performance by page + query (export or API) | Shows which queries each page actually gets, CTR, and which pages compete for the same query | Infer from crawl + SERP sampling. Cannibalization becomes **Potential**, never Confirmed |
| Crawl data (`scripts/site_check.py` output, Screaming Frog export, or a codebase inspection) | Bulk evidence for titles, descriptions, headings, alt, canonicals, word counts | Manual sample of key templates; say so in "Not checked / why" |
| Rendered HTML for JS sites | `site_check.py` reads raw HTML only | Compare raw vs rendered for one URL per template (URL Inspection "View crawled page", or a headless browser with an isolated profile). See technical-seo.md |

## 2. Audit procedure

Work **by template first, then by page**. Most on-page issues are template issues: fix the template once and hundreds of pages change.

1. **Inventory templates.** Group URLs by type: home, category/listing, product/service, location, article, landing, utility (cart, account, search). Pick 3–5 representative URLs per template, plus every money page.
2. **Collect evidence in bulk.** Run:
   ```
   python <skill-dir>/scripts/site_check.py https://www.example.com --urls urls.txt --out 03-audit/evidence/onpage-YYYY-MM-DD
   ```
   The first argument is always the site root being audited: robots.txt and the sitemaps are read from it. Without `--urls`, the script samples URLs from the sitemap instead (`--sample N`, default 25). If the URL list has more than 200 entries, raise `--max-pages`, which defaults to 200. Use a new dated `--out` folder for every run: the script refuses a non-empty folder (so earlier evidence isn't overwritten) unless `--overwrite` is given. URLs on other hosts are reported but not fetched unless `--allow-off-host` is given. See `--help`. Save the CSV/JSON outputs as evidence with the date. For larger sites, prefer a Screaming Frog export if the user has a license, or one they supply.
3. **Run the structural checks** (section 3) across the whole crawl. These are deterministic, so they are usually **High** confidence.
4. **Run the judgement checks** on the key URLs: intent fit, content quality, conversion relevance. Each needs a short, specific justification as its evidence ("the page targets 'dental implants cost' but contains no price information or range, while the top 5 results all show price ranges, SERP sampled 2026-11-24 from Egypt, logged-out").
5. **Cross-check with GSC.** Are pages ranking for the queries they were meant for? Are high-impression/low-CTR pages candidates for title/snippet work?
6. **Write findings** at template level where possible (`scope = "all /product/* pages (≈1,240 URLs)"`). Give the page level only for money pages.

## 3. Check-by-check guidance

### Title elements
Official guidance (Source: Influencing title links in Google Search, https://developers.google.com/search/docs/appearance/title-link, checked 2026-11-24):
- Every page has a unique, descriptive, concise `<title>`.
- No keyword repetition, and no boilerplate repeated across pages.
- The site name appears on the home page, and elsewhere where it helps, separated by a delimiter.
- The title uses the page's language and script.

Google builds the title link from several sources: `<title>`, the main visible heading, other headings, `og:title`, anchor text. It rewrites titles that are empty, outdated, inaccurate, boilerplate, or repetitive.

Checks:
- Missing / empty title.
- Duplicate titles across distinct pages: group them and count.
- Boilerplate-only titles ("Product | Brand", "Home").
- Title doesn't match the page's main intent or primary keyword (needs the keyword map).
- Title contradicts the H1 (a frequent cause of Google rewrites).
- Keyword stuffing or repeated terms.
- Very long titles. **There's no official character limit.** The display is truncated by pixel width. Treat "about 50–60 characters" as a third-party display heuristic, not a rule, and never file a finding purely on length unless truncation hides the important part.
- Arabic/English: the title language matches the page language. See arabic-and-multilingual-seo.md.

How to tell whether Google rewrote a title: compare the live SERP (logged-out, the right country) with `<title>`. Rewrites are evidence the title is weak. They are not a penalty.

### Meta descriptions
Official guidance (Source: Control your snippets in search results, https://developers.google.com/search/docs/appearance/snippet, checked 2026-11-24):
- Google mostly generates snippets from page content, and uses the meta description when it describes the page better.
- Unique per page. Site-level descriptions only on the home page and aggregation pages.
- There is no length limit; snippets are truncated to fit.
- Keyword-stuffed descriptions are less likely to be shown.

Meta descriptions are **not a ranking factor**. Their value is CTR. So prioritize by impressions: a missing description on a page with 50k impressions/month matters more than one on 500 never-shown tag pages.

Checks:
- Missing.
- Duplicated across many pages.
- Boilerplate.
- Doesn't reflect the content or offer.
- Contains claims that aren't true. Check against what the business confirmed. Never invent offers, prices, or "free shipping".

### Headings (H1–H6)
- One clear main heading that states the page topic. Multiple H1s are **not** a Google problem by themselves. Google representatives have said so publicly, though it's not stated in the formal docs, so treat it as Google commentary. Report them only when they cause ambiguity: logo-as-H1 on every page, empty H1, or an H1 that's the same across all pages of a template.
- Headings used for styling instead of structure. Missing hierarchy on long content: does the outline make sense if you read only the headings?
- The H1 is in the initial HTML on JS sites (check raw vs rendered).
- Confidence: missing/duplicate H1 = High (deterministic); "the heading doesn't express the intent" = Medium (judgement, so write the reasoning).

### Keyword placement and search intent
Placement is a hygiene check, not a formula. Google's systems understand synonyms and topics, so the question is "does the page clearly signal what it's about, in the words the audience uses?":
- The primary term (or a close variant in the audience's language) is in the title, the H1, and early in the body. Supporting terms appear naturally in subheadings.
- **Intent fit matters more than placement.** Classify the dominant SERP intent for the primary keyword (see keyword-research.md: informational, commercial investigation, transactional, local, navigational). Then compare it with the page type. A blog post can't win a SERP full of category pages, and a product page rarely wins a "how to choose" SERP.
- Evidence for intent: sample the SERP (logged-out, correct country/language, date it). Record the result types and the page types of the top results. That sample is evidence; a hunch is not.

### Content quality and relevance
Official framing (Source: Creating helpful, reliable, people-first content, https://developers.google.com/search/docs/fundamentals/creating-helpful-content, checked 2026-11-24): content made primarily for people. Demonstrate experience, expertise, authoritativeness, and trust. Trust is the most important part. Think about Who created it, How, and Why. E-E-A-T is a framework from the Search Quality Rater Guidelines; it isn't a single ranking factor.

Practical checks per key page:
- Does it answer what the searcher needs to decide or act? Specs, prices or price ranges, availability, delivery areas, process, and who it's for.
- Original information: first-hand photos, real data, the business's actual policies and differentiators. "Commodity" content that any competitor could have written is the main weakness to flag.
- Accuracy against facts the business confirmed. Never make the copy say something the business hasn't confirmed: materials, certifications, guarantees, medical claims.
- For YMYL sites, apply the stricter checks in industry-adaptations.md: authorship, review, sources.

### Content gaps
A content gap is a demand the site has no adequate page for. Evidence sources, strongest first:
1. GSC queries with impressions where the ranking page is a poor fit, or where position > 20 with no dedicated page.
2. Competitor pages ranking for clusters the site lacks (competitor-analysis.md).
3. Keyword research clusters with no mapped page (keyword-map `mapping_status = gap`).

Gaps are **Opportunities** (`CNT-`), not issues. Hand them to content-strategy.md.

### Thin, duplicate, and low-value indexable pages
- **Thin:** indexable pages with little unique main content relative to their purpose, e.g. empty category pages, tag pages with one post, location pages that only swap the city name. Word count from `site_check.py` is a *signal* for triage, never proof. A 120-word product page with full specs can be fine.
- **Duplicate:** the same or near-same main content on several URLs. Separate *technical* duplication (parameters, http/https, trailing slashes; handled in technical-seo.md) from *content* duplication: manufacturer descriptions copied across products and competitors, or templated service pages.
- **Index bloat:** low-value pages (internal search results, filtered combinations, empty archives) that are indexable. Decide per page type: improve, consolidate (301 or canonical), `noindex`, or leave. Record the decision rule in the strategy.

### Cannibalization
Cannibalization means several URLs on the site competing for the same query and intent, so that neither performs well. It is often over-diagnosed.

This is the skill's **canonical cannibalization rule**; other references point here.

- **Confirmed** only when **all three** hold:
  1. **First-party split:** GSC query → page data shows the same query, in the same period, with impressions or clicks split across two or more URLs.
  2. **Same intent:** a SERP check shows both pages target the same search intent.
  3. **At least one clear, documented harm signal:**
     - URL alternation for that query over a relevant period; **or**
     - clear, sustained underperformance compared with the stronger page's own earlier performance, using a meaningful, comparable position or CTR comparison (same query, comparable periods).

  Arbitrary or one-off CTR/position differences are not harm.
- **Potential** when only part of this holds:
  - GSC shows a split with the same intent, but harm isn't sufficiently demonstrated;
  - the keyword map assigns the same primary keyword to more than one URL, or titles/H1s target the same term;
  - normalized-equal Arabic spelling variants sit on separate pages;
  - a third-party rank tracker shows alternation;
  - or GSC data isn't available.
- **A keyword appearing on several URLs is never, on its own, Confirmed cannibalization.**
- **Not cannibalization:** a category and a product both ranking for a broad term with different intents, or two results from the same site occupying top positions (that's a good outcome).
- Fixes: re-target one page to a distinct intent, merge (301 the weaker one into the stronger), canonicalize true duplicates, or adjust internal links so the preferred page is clearly the primary one. Merges and redirects go through the G4 gate.

### Images
Official guidance (Source: Image SEO best practices, https://developers.google.com/search/docs/appearance/google-images, checked 2026-11-24):
- Use standard `<img>` elements so images are discoverable.
- Alt text is the most important image metadata: descriptive, in context, not keyword-stuffed. Empty `alt=""` for decorative images.
- Filenames give only light clues: short and descriptive, hyphens rather than underscores.
- Use one consistent URL per image.

Checks (from `site_check.py` alt columns): content images with no `alt` attribute; meaningful images with empty alt; alt stuffed with keywords; product images all sharing the same alt; images in CSS backgrounds that should be content; huge image weights (a performance overlap, so hand it to technical-seo.md). Arabic pages: alt text in Arabic, not left in English from the template.

### Internal linking
Official guidance (Source: SEO link best practices for Google, https://developers.google.com/search/docs/crawling-indexing/links-crawlable, checked 2026-11-24):
- Links must be crawlable `<a href>` elements.
- Anchor text should be descriptive and concise.
- The image alt acts as anchor text for image links.

Checks:
- Orphan pages: in the sitemap or in GSC, but with no internal links found in the crawl.
- Money pages buried deep (crawl depth from technical-seo.md).
- Generic anchors ("click here", "read more") on key links.
- JavaScript-only navigation (`onclick`, buttons without `href`).
- Links pointing to redirected or 404 URLs.
- Faceted links flooding the crawl.
- Missing contextual links from informational content to the commercial pages it supports.
- Breadcrumbs missing on deep hierarchies.

Strategy: a hub-and-spoke structure per topic cluster (category ↔ subcategory ↔ product, or pillar ↔ supporting articles). Contextual links use the target page's primary term or a natural variant. Don't make every anchor an exact match; it reads unnaturally and isn't needed.

### URL structure
- Readable, stable, lowercase, hyphenated. One URL per piece of content. Avoid session IDs and unnecessary parameters in internal links.
- URL changes cost signals and carry risk. **Don't recommend changing working URLs for cosmetic keyword gains.** If a change is justified (a migration, a broken structure), it requires a 301 map, an internal link update, a sitemap update, and the G4 gate. See technical-seo.md and seo-implementation-qa.md.
- Arabic slugs vs transliterated vs English: see arabic-and-multilingual-seo.md.

### Conversion relevance
SEO traffic that can't convert is a business finding. Check key landing pages for:
- A clear primary CTA visible on mobile.
- Trust elements the business can truthfully show (reviews, policies, guarantees, credentials).
- Contact options matching the market (e.g. WhatsApp or click-to-call where that's how customers reach the business).
- Price/availability clarity.
- Form friction.

Prefix `ONP-` if the issue is page-level, `ANL-` if it's a missing conversion measurement.

## 4. Typical findings

| Example finding | Prefix | Typical bucket | Impact | Effort | Notes |
|---|---|---|---|---|---|
| Product template outputs the same title on all products | ONP | Confirmed | 4 | 1–2 | Template fix; usually a quick win |
| 60% of categories have no meta description | ONP | Confirmed | 2–3 | 2 | Priority scales with impressions |
| Category pages have no unique copy, only a product grid | ONP / CNT | Confirmed / Opportunity | 3 | 3 | Needs real copy from the business |
| Two service pages target the same term; GSC shows split impressions | ONP | Confirmed (with GSC) / Potential (without) | 3 | 2–3 | Merge or re-target via G4 |
| Blog posts don't link to the services they discuss | ONP | Confirmed | 3 | 2 | Contextual linking pass |
| Logo is the H1 site-wide; the real heading is an H2 | ONP | Confirmed | 2 | 1 | Template fix |
| Location pages identical except the city name | ONP / LOC | Confirmed | 3–4 | 3 | Doorway risk; see local-seo.md |
| Content images missing alt on product galleries | ONP | Confirmed | 2 | 2 | Also an accessibility gain |
| Demand cluster with no matching page | CNT | Opportunity | 3–4 | 3–4 | Into content-strategy.md |

## 5. Implementation guidance

- **Fix templates, not pages,** wherever possible. In code: find where metadata is generated (e.g. Next.js `generateMetadata`/`metadata` exports, a CMS SEO plugin, theme templates) and change the pattern. Respect the existing conventions.
- **Title/description patterns** per template, with variables that exist in the data: `{Product name} – {key attribute} | {Brand}`. Check that variables are never empty, and decide a fallback for when they are.
- **Hand-written copy** for money pages. Use facts the business confirmed. Flag every claim that needs confirmation as `[CONFIRM: …]` in drafts.
- **Bulk changes** (hundreds of titles, mass rewrites) are bulk operations, so they need a G4 proposal showing a sample of before/after rows, plus a rollback (keep the old values in a backup file).
- Don't use AI to generate large numbers of near-identical pages. That falls under scaled content abuse (off-page-seo.md has the spam policy references).

## 6. Validation

| Change | Validate with |
|---|---|
| Titles/descriptions/headings | Re-run `site_check.py` on the affected URLs. Check the rendered HTML for JS sites. Confirm no empty variables. Watch the GSC CTR for the page group (after recrawl, typically days to weeks) |
| Internal links | Re-crawl: orphan count down, depth of key pages reduced, no links to redirects or 404s |
| Merges/redirects | Old URL returns a 301 to the target, the target is 200 + self-canonical, internal links updated, sitemap updated. GSC shows the target gaining the query over the following weeks |
| Content improvements | The page is indexed (URL Inspection). Query coverage for the page in GSC is compared over equal periods, which is correlation, not proof; see reporting-framework.md |

A change is `implemented` when deployed and `validated` only when this evidence exists (SKILL.md G5).

## 7. Pitfalls and myths

- "Titles must be under 60 characters" / "descriptions under 160": display heuristics, not rules (no official limit).
- "Keyword density X%": not a Google concept. Write for the reader, and check clarity and intent.
- "Multiple H1s hurt rankings": not per Google. Fix only real ambiguity.
- "Meta keywords tag": Google ignores it. Don't spend client time on it.
- "Every page needs 1,000+ words": length isn't quality. Match what the intent needs.
- Rewriting URLs for keywords: a high risk with little gain. Avoid it unless the structure is genuinely broken.
- Declaring cannibalization without query-level evidence.
- Writing copy with unverified claims to "sound better": it damages trust and may be legally risky.
- For Arabic or bilingual sites, keyword placement must use the variants the audience actually searches. See arabic-and-multilingual-seo.md and `scripts/arabic_keywords.py`.
