# Arabic, RTL and Multilingual SEO

Apply this lens to any site with Arabic content, RTL layout, more than one language, or more than one target country. It changes keyword research, content, metadata, URLs, rendering, and targeting. Finding IDs: `INT-` for targeting/hreflang/language mapping, `ONP-`/`CNT-`/`TEC-` for issues that are Arabic-specific but belong to those domains. Everything else follows SKILL.md.

The core rule: **an Arabic page is its own SEO target, not a translation of the English one.** Different words, different intent, often different competitors.

## Contents

1. [Discovery questions for multilingual projects](#1-discovery-questions-for-multilingual-projects)
2. [Arabic keyword research](#2-arabic-keyword-research)
3. [Search intent in Arabic](#3-search-intent-in-arabic)
4. [Arabic content quality](#4-arabic-content-quality)
5. [Titles and meta descriptions in Arabic](#5-titles-and-meta-descriptions-in-arabic)
6. [Arabic URLs](#6-arabic-urls)
7. [Arabic/English page mapping](#7-arabicenglish-page-mapping)
8. [RTL rendering](#8-rtl-rendering)
9. [Language and regional targeting](#9-language-and-regional-targeting)
10. [Search Console analysis by country and language](#10-search-console-analysis-by-country-and-language)
11. [Market behaviour: Egypt, Saudi Arabia, UAE, Gulf](#11-market-behaviour-egypt-saudi-arabia-uae-gulf)
12. [Arabic fonts and performance](#12-arabic-fonts-and-performance)
13. [Audit checklist](#13-audit-checklist)

---

## 1. Discovery questions for multilingual projects

Ask progressively, only what isn't visible on the site:
- Which **countries** are targeted, and which language does each market search in (e.g. Egypt: Arabic + English; KSA: Arabic first)?
- Is the content **different per country** (prices, currency, shipping, legal) or only per language?
- Who writes and reviews Arabic content: a native speaker from the target market, or machine translation?
- Which dialect does the brand speak in (MSA, Egyptian, Gulf)? Is that a brand decision or an accident?
- Do Arabic and English pages correspond one to one, or does one language have pages the other lacks?
- Which language is the default/root, and does the site redirect by browser language or IP?

## 2. Arabic keyword research

Do Arabic research from scratch, with the method in keyword-research.md. Translating English keywords gives terms nobody searches, or misses the terms people do use.

**Sources of real Arabic queries:** GSC queries filtered by country (the best evidence); Google autocomplete and "People also ask" in Arabic, from the target country (use a country-appropriate setting such as `google.com.eg` / `gl=EG&hl=ar`, in an isolated logged-out browser or via fetch); keyword tools with the country database selected (label their volumes as tool estimates); competitor Arabic titles; GBP Performance queries; customer language from reviews, WhatsApp chats, and sales staff.

**Variant families to collect and cluster.** The same intent often appears as several spellings:

| Variation | Examples | Note |
|---|---|---|
| Hamza / alef forms | أ إ آ ا (أسعار / اسعار) | Users often type bare alef |
| Ta marbuta vs ha | ة / ه (ثلاجة / ثلاجه) | Very common in Egyptian typing |
| Ya vs alef maqsura | ي / ى (مستشفى / مستشفي) | Common in Egyptian typing |
| Diacritics (tashkeel) | rarely typed | Strip for matching |
| Tatweel (kashida) | ـ used for stretching | Strip for matching |
| Digits | Arabic-Indic ٠١٢٣ vs Western 0123 | Both appear; sizes, prices, years |
| Definite article | ال + noun vs bare noun | Often the same intent |
| Plural / singular | ثلاجات / ثلاجة | Can differ in intent (category vs product) |
| Dialect vocabulary | Egyptian تكييف vs Gulf مكيف for an air conditioner (MSA مكيف هواء); usage differs by market | Choose per market, cover both where volume exists |
| English loanwords in Arabic script | لابتوب, موبايل, سكين كير | Often higher volume than the "pure" Arabic word |
| English queries | "split ac price egypt" | Common in Egypt for tech, fashion, products, B2B |
| Arabizi / Franco-Arabic | "takyeef split", "a7san doctor" | Present in Egypt, mostly social/informal; check GSC before investing |

**Use `scripts/arabic_keywords.py`** to normalize a keyword list (hamza/alef, ta marbuta, ya/alef maqsura, diacritics, tatweel, digits) and group spelling variants. Variants that collapse to one normalized form are the **same topic**: target one page, not several (avoid self-made cannibalization). Variants that differ in vocabulary (تكييف vs مكيف) aren't merged by normalization. Decide by checking the SERPs: if Google shows the same results, one page can target both.

Google generally handles orthographic variants well, so the page should use the most common, natural form in its title and H1, and work the other forms in naturally where a person would. Don't stuff every variant into the copy.

**Volumes:** keyword tools under-report Arabic and long-tail local queries. "Below the tool's threshold" is common. Report it as such, never as zero, and lean on GSC impressions where they exist.

## 3. Search intent in Arabic

- Classify intent the same way (informational, commercial investigation, transactional, navigational, local), but expect **price** and **location** modifiers to be very frequent: سعر / أسعار, أرخص, عروض, فين / أين, قريب مني, في + city/district.
- Commercial queries in Egypt often mix Arabic and English: "سعر iphone 16", "أفضل laptop للبرمجة".
- Look at the actual SERP in the target country before assigning a page type. If Arabic results are forums, YouTube, or marketplaces, a thin product page won't win, and a guide or category page may.
- Question queries (إزاي / كيف, ليه / لماذا, هل, أفضل) suit guide content and AI-answer visibility (ai-search-visibility.md).

## 4. Arabic content quality

- **Raw machine translation** reads unnaturally, misses local terms, and often mis-handles gender, number, and register. Treat it as low quality. Google's guidance targets content made primarily for ranking without adding value, including scaled auto-generated pages (spam policy: scaled content abuse). MT plus a native human editor is acceptable; unreviewed MT across hundreds of pages is a risk.
- **Pick a register per market and stay consistent.** MSA is safe for KSA and the Gulf and for formal sectors (health, finance, government). Egyptian colloquial can work for consumer brands in Egypt, especially in UI microcopy and social content. Many sites use light MSA for body copy and keep product names as people say them.
- **Localize facts:** currency (ج.م / EGP, ر.س / SAR, د.إ / AED), units, phone formats, address formats, payment methods (cash on delivery, local wallets), shipping areas, holidays (Ramadan, Eid hours).
- **Never write product, medical, or legal facts that the business hasn't confirmed,** in either language. If the Arabic and English pages disagree on a fact, that's a finding.
- Keep brand and product names consistent. Decide when to write them in Latin script, when in Arabic script, and when in both.
- **E-E-A-T signals in Arabic:** author names and credentials, a real address, a contact page, and policies, all *in Arabic* on the Arabic version. An Arabic site whose trust pages exist only in English looks incomplete to users.

## 5. Titles and meta descriptions in Arabic

- Google truncates titles by **pixel width**, not character count. Arabic glyphs and mixed scripts render at different widths, so check a SERP preview tool, or judge from the actual SERPs. Treat ~50–60 characters as a rough guide only.
- Put the main term early. Arabic is read right to left, so "early" means the right-hand (first) side of the string.
- **Mixing Arabic and English** (brand names, model numbers) triggers bidirectional reordering. Punctuation and separators next to Latin text can jump to the wrong side. Prefer separators that render predictably (`|` or `–` with spaces), and check how it looks in the actual SERP or rendered title.
- Use Arabic punctuation (، ؛ ؟) in Arabic sentences, not Latin comma or semicolon.
- Write titles and descriptions natively for each language. Don't put the English title on the Arabic page or vice versa. A cross-language mismatch (e.g. an English meta description on an Arabic page) is a common, real finding in frameworks where locale metadata falls back to the default language.
- Brand suffix: decide whether it's Arabic, English, or both, and keep it consistent per language. Avoid a doubled brand (the template adds it, and the page title already includes it).

## 6. Arabic URLs

Options for the slug of an Arabic page:

| Option | Example path | Pros | Cons |
|---|---|---|---|
| Arabic slug | `/ar/مكيفات-سبليت` | Readable for Arabic users; matches the query in the displayed URL | Percent-encoded when copied/shared (`%D9%85…`), looks broken in some tools and messengers; long encoded URLs |
| Transliteration | `/ar/mukayyifat-split` | ASCII-safe | Nobody searches it; inconsistent spellings |
| English slug | `/ar/split-air-conditioners` | ASCII-safe, identical structure across languages, easy hreflang mapping and maintenance | No keyword benefit in the URL for Arabic queries (minor) |

Facts and guidance:
- Google supports non-ASCII URLs; use UTF-8 and percent-encode them in hreflang, sitemaps, and canonicals as needed. The keyword-in-URL benefit is small. Choose for maintainability and shareability.
- **Recommendation:** a language folder (`/ar/`, `/en/`) plus either English slugs shared across languages (simplest operationally) or Arabic slugs, if the business values Arabic-readable URLs and the stack handles encoding correctly end to end (sitemaps, canonicals, redirects, analytics). Whichever you choose, use it consistently.
- **Don't change slugs of URLs that are already indexed** just to switch the style. If you must, every change needs a 301 map (technical-seo.md section 19) and a G4 proposal.
- Check that the server, CDN, and framework don't create duplicates: encoded vs decoded forms, or different Unicode normalization forms of the same slug. A crawl should show one canonical form.
- Avoid diacritics and tatweel in slugs. Use hyphens between words.

## 7. Arabic/English page mapping

Record the mapping in the keyword map (`04-research/keyword-map.csv`). Each row is one cluster in one language, with its own `primary_keyword` from that language's research. `page_group` links the Arabic and English rows that serve the same page group. `alternate_language_url` holds the equivalent page in the other language (empty if none). `language_pair_status` is `both`, `ar-only`, `en-only` or `mismatch`. Don't force a translation pair where none exists (keyword-research.md §7).

Check:
- Every page that exists in both languages is linked as an hreflang pair, and the switcher links to the **equivalent page**, not the other language's homepage.
- Pages existing in only one language are deliberate. Don't create empty stub translations. A thin or placeholder translation is worse than no translation.
- Content parity on facts: prices, specs, policies.
- The keyword target per language comes from that language's research, not from a translation of the other column.

### Planned language not live yet

When Arabic (or another language) is planned, put these decisions on the roadmap *before* launch. Changing URLs afterwards costs a migration.
1. **URL structure:** subfolder (`/ar/`), subdomain, or ccTLD. The trade-offs are in section 9, and they depend on what the platform supports. Hosted builders differ in native localization and hreflang support, so verify the current platform documentation.
2. **Default and x-default behaviour,** plus the language switcher linking to equivalent pages.
3. **Keyword research in the new language,** done separately (section 2), to decide which page groups launch first. A smaller, fully localized set beats a full machine-translated mirror.
4. **Translation and review workflow:** who writes and who reviews for each market variant.
5. **Measurement:** GSC and GA4 segments by language folder, ready on launch day.
6. **Launch QA:** the hreflang pairs, RTL rendering, and NAP/price parity checks from this file's audit checklist.

## 8. RTL rendering

Check in raw HTML and at mobile width:
- `<html lang="ar" dir="rtl">` on Arabic pages (`lang="ar-EG"` where region matters) and `lang="en" dir="ltr"` on English ones. Fragments in the other language get their own `lang`/`dir` (e.g. `<span lang="en" dir="ltr">`). These attributes matter for accessibility, browser rendering, and screen readers, and some search engines use them as signals (section 9).
- Mirrored layout: navigation, breadcrumbs, arrows, carousels, progress indicators, and icons with direction (back/forward) flip. Logos, media controls, and numbers don't.
- Use **CSS logical properties** (`margin-inline-start`, `padding-inline-end`, `inset-inline-start`, `text-align: start`) instead of left/right, so a single stylesheet serves both directions.
- Mixed bidi text: product codes, prices, phone numbers, emails, and URLs inside Arabic sentences can render out of order. Use `<bdi>` or `dir="ltr"` spans, and test with real data.
- Numbers: decide between Western (0–9) and Arabic-Indic (٠–٩) digits per market and brand. Western digits are common online in Egypt and the Gulf. Keep the choice consistent within a page and in structured data. Structured data values (prices, phone, dates) use machine formats regardless of display.
- Forms: RTL input alignment, phone inputs left-to-right, validation messages in Arabic.
- RTL bugs that hide content, overlap the CTA, or cause horizontal overflow on mobile are real findings (UX, and mobile-first indexing via hidden content). They're `TEC-` or `ONP-` depending on cause.

## 9. Language and regional targeting

**Structure options:**

| Structure | Example | Notes |
|---|---|---|
| ccTLD per country | `example.com.eg`, `example.sa` | Strongest country signal; separate authority, hosting, and operations per domain; good when the business and content truly differ by country |
| Subfolder | `example.com/ar-eg/`, `/en/` | Shares domain authority; easiest to maintain; usual recommendation |
| Subdomain | `ar.example.com` | Works, but Google treats each hostname separately for some purposes (e.g. crawl budget); more setup |
| Parameters / cookies | `?lang=ar` or cookie-only | **Avoid**: cookie- or session-based language is invisible to crawlers |

**hreflang** (Source: Google, Tell Google about localized versions of your page, https://developers.google.com/search/docs/specialty/international/localized-versions, checked 2026-11-24):
- Codes are an ISO 639-1 language (`ar`, `en`) plus an optional ISO 3166-1 alpha-2 region (`ar-EG`, `ar-SA`, `ar-AE`, `en-EG`). A region alone isn't valid (`EG` alone is wrong), and neither is `ar-AR`.
- Use **language-only** (`ar`) when one Arabic version serves all Arabic markets. Use **language-region** only when content genuinely differs per country (currency, prices, shipping, legal). You can combine them: `ar-EG`, `ar-SA`, plus `ar` as the generic Arabic fallback.
- **`x-default`** marks the fallback for users matching no listed version, typically the language selector or the main version.
- Every version lists all versions **including itself**. Pairs must be **reciprocal** or Google ignores them.
- Each version **self-canonicalizes**. Never canonical the Arabic page to the English page (or `ar-SA` to `ar-EG`); that tells Google to drop it. For near-identical regional versions (same Arabic text, different currency), keep them distinct with real localized elements, or consolidate to one `ar` version.
- Implement via `<link rel="alternate" hreflang>` in the head, the XML sitemap (`xhtml:link`), or HTTP headers for non-HTML. Use one method per URL set.

**Language detection:**
- Google uses the visible content to determine a page's language. It doesn't use the HTML `lang` attribute or hreflang for language detection (same Google source as above).
- Bing has historically given weight to `lang`, the `Content-Language` meta/header, and other signals; third-party sources disagree on how much it uses hreflang. Set `lang` correctly anyway, and optionally `content-language`, for Bing and for accessibility. Exact Bing behaviour: verify at time of use in Bing Webmaster guidelines.
- **Avoid automatic redirects by browser language or IP.** Googlebot crawls mostly from the US without `Accept-Language`, so it may never reach the Arabic version. Use a suggestion banner instead of a forced redirect (Source: Google, Managing multi-regional and multilingual sites, https://developers.google.com/search/docs/specialty/international/managing-multi-regional-sites, checked 2026-11-24). Framework specifics are in technical-seo.md section 9.
- Translate the full page (navigation, footer, metadata, alt text, and structured data text), not only the main copy. Mixed-language pages confuse language detection and users.

## 10. Search Console analysis by country and language

- Filter the Performance report by **Country**: impressions/clicks per market, and whether the right language version is shown in each country. For example, English URLs getting Egyptian Arabic-query impressions indicates mapping or hreflang problems.
- Filter by **page path** (`/ar/` vs `/en/`) and compare query sets. Check Arabic queries landing on English pages and vice versa.
- Use query regex filters to split Arabic-script queries from Latin-script ones (e.g. a custom regex containing the Arabic Unicode range `[؀-ۿ]`). GSC supports RE2 regex in query and page filters.
- Use `scripts/gsc_compare.py` for period comparisons per segment. Export separate files per country or per language folder.
- For domain properties, add URL-prefix properties per language folder if the team wants separate views (no re-verification is needed when the domain property is verified via DNS; the user adds them).
- International targeting report: Google retired the legacy country-targeting setting; geotargeting now relies on ccTLDs, hreflang, and content signals. Don't recommend the old setting.

## 11. Market behaviour: Egypt, Saudi Arabia, UAE, Gulf

Each statement is labeled. Don't put unlabeled claims into client documents.
- **Data:** Google holds ~95–96% search share in Egypt and Saudi Arabia (StatCounter, June 2026, all platforms; Egypt ~96.4%, KSA ~95.8%). Mobile is the majority of traffic in both (Egypt mobile ~75% of search traffic in June 2026) (Sources: https://gs.statcounter.com/search-engine-market-share/all/egypt, https://gs.statcounter.com/search-engine-market-share/all/saudi-arabia, checked 2026-11-24). Bing is a small second, though a larger one on desktop. Bing data still matters because some AI assistants draw on it.
- **Field observation (Egypt):** English and mixed-language queries are common for products, tech, fashion, education, and B2B services. Arabic dominates local services, health, and price-check queries. Egyptian colloquial spellings (ه for ة, ي for ى) are frequent.
- **Field observation (KSA/Gulf):** Arabic queries dominate most consumer verticals. MSA content is the safe default. Expatriate audiences (especially in the UAE) also search in English, plus other languages. Check GSC by language.
- **Field observation (conversion paths):** WhatsApp and phone calls are major conversion paths, and cash on delivery remains common for e-commerce in Egypt. Track WhatsApp and call clicks as GA4 events (analytics-and-measurement.md). Show payment and delivery terms clearly on Arabic product pages.
- **Field observation (seasonality):** Ramadan, Eid, back-to-school, White Friday (the regional name for Black Friday sales), and summer travel shift demand and hours. Compare year over year, not month over month, around these periods (reporting-framework.md).
- **Verify at time of use:** any market-size, e-commerce penetration, or payment-share statistic. Cite a dated source or leave it out.

## 12. Arabic fonts and performance

Arabic web fonts are large (many glyph forms and ligatures), and often hurt LCP and CLS.
- **Subset** to the needed scripts (Arabic + Basic Latin), using `unicode-range` so the Latin subset isn't downloaded on Arabic-only text or vice versa. Self-host WOFF2 or use a provider that serves subsets (e.g. Google Fonts serves `unicode-range` subsets automatically).
- Limit families and weights; each weight is another file. Two weights are usually enough.
- Use `font-display: swap` (or `optional` for non-critical fonts), plus metric overrides (`size-adjust`, `ascent-override`) on the fallback, to reduce CLS from the font swap. In Next.js, `next/font` handles subsetting and fallback metrics for supported fonts.
- Preload only the one font file used in the LCP element.
- Make sure the fallback stack includes a system Arabic font, so text renders during loading.

## 13. Audit checklist

Bands shown are indicative only. The SKILL.md formula decides P1–P3, and P0 applies only to SKILL.md's override conditions.

| Check | Evidence | Typical finding ID/bucket |
|---|---|---|
| `lang`/`dir` correct per page | site_check.py `lang`/`dir` columns | `TEC-` Confirmed |
| hreflang present, valid codes, reciprocal, self-referencing, x-default | site_check.py hreflang output across the URL set | `INT-` Confirmed |
| Canonicals don't cross languages | site_check.py | `INT-` Confirmed, indicative P1 |
| Auto-redirect by Accept-Language/IP | `curl` with and without `Accept-Language`; code inspection | `INT-` Potential → Confirmed |
| Metadata in the wrong language | site_check.py title/description vs page language | `ONP-` Confirmed |
| Arabic pages are machine-translated or thin | Native review of a sample | `CNT-` Potential (human judgment) |
| Arabic keyword targeting is a translation of English | Keyword map vs Arabic SERP/GSC | `CNT-`/`ONP-` Opportunity |
| Spelling-variant cannibalization (separate pages for normalized-equal terms) | arabic_keywords.py + URL list | `ONP-` Potential. Confirmed only by the canonical rule in on-page-seo.md (Cannibalization) |
| Slug encoding duplicates | Crawl shows encoded and decoded variants | `TEC-` Confirmed |
| RTL layout breaks on mobile | Screenshot at ~390 px | `TEC-`/`ONP-` Confirmed |
| Font weight hurting LCP | Lighthouse / network waterfall | `TEC-` Confirmed (lab) |
| Language switcher links to homepage, not the equivalent page | Crawl / manual | `INT-` Confirmed |
| Arabic/English facts disagree | Side-by-side check | `CNT-` Confirmed |
