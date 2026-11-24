# Keyword Research

Load this at Stage 5, or earlier if the user asks for keyword research directly. It covers how to find what the target audience searches, how to classify intent, how to cluster, how to map clusters to pages, and how to prioritize, all without inventing numbers.

Outputs go to `04-research/keyword-research.md` (template: `templates/keyword-research-template.md`) and `04-research/keyword-map.csv` (template: `templates/keyword-map-template.csv`). Conventions are in `SKILL.md`.

Contents:
1. Ground rules
2. Inputs
3. Data sources and what each can honestly claim
4. Procedure
5. Intent classification
6. Clustering
7. Keyword-to-page mapping and cannibalization check
8. Prioritization (with and without volume data)
9. Arabic and multilingual notes
10. Pitfalls

---

## 1. Ground rules

- **Never invent search volume, difficulty, CPC, or trend numbers.** Every number carries its source and pull date, e.g. `Semrush, EG database, 2026-11-24`. Different tools disagree. Pick one tool as the primary source for volume, and don't mix tools in one column.
- **Volumes are estimates even from paid tools.** Google Keyword Planner shows rounded averages or ranges. Third-party tools model their figures. Present them as relative signals, not counts.
- Keyword research serves the business. A high-volume term that doesn't match what the business sells, where it sells, is a distraction.
- Research in the audience's language and market, not by translating an English list (section 9).

## 2. Inputs

From discovery (`01-discovery.md`): products/services, which ones matter most (margin, capacity, strategy), markets/locations, languages, audience segments, conversion goals, known competitors. Also an existing site inventory, and GSC data if available.

If discovery doesn't say which offerings matter most, ask that one question before researching. It changes everything downstream.

## 3. Data sources and what each can honestly claim

| Source | Gives | Honest label | Access |
|---|---|---|---|
| **GSC Performance (queries)** | Real queries the site already gets impressions/clicks for, by page, country, device | First-party, High confidence. Includes anonymized-query gaps; low-volume queries are partly hidden | User grants access or exports |
| **Ahrefs / Semrush / similar** | Volume estimates by country, difficulty scores, SERP features, competitor keywords, question keywords | "Tool estimate". Difficulty scores are proprietary | Paid account, MCP, or user exports |
| **Google Keyword Planner** | Average monthly searches (rounded, 12-month average, close variants grouped), forecasts | Google Ads data. Precision depends on account status. Some low-volume/sensitive terms aren't shown (Source: About Keyword Planner forecasts, https://support.google.com/google-ads/answer/3022575, checked 2026-11-24). Accounts without active spend reportedly see ranges, according to a community forum, not an official statement; verify at time of use | User's Google Ads account |
| **Google Trends** | Relative interest over time and by region, 0–100, normalized to the peak in the chosen range. Low-volume terms show 0. Small noise is added for privacy (Source: FAQ about Google Trends data, https://support.google.com/trends/answer/4365533, checked 2026-11-24) | Relative only. Never convert it to volumes | Public |
| **Google autocomplete, People Also Ask, related searches** | How people phrase queries and the questions they ask | Qualitative, no volume. Varies by location, language, and personalization | Public (sample logged-out, correct country/language) |
| **SERP inspection** | Intent, result types, competing page types, SERP features (local pack, shopping, video, AI Overview) | Observed on a date, in a location. Medium confidence for a single sample | Public |
| **Site search logs, customer support, sales calls, reviews, marketplaces** | The customer's own vocabulary, objections, product attributes | First-party qualitative, very valuable | From the business |
| **Competitor pages and navigation** | How the market labels categories and services | Qualitative | Public |
| **Bing Webmaster Tools keyword research** | Bing query volumes | Bing's data, not Google's | Free with a verified site |

If no volume tool is available, say so in the research doc and use **relevance-only prioritization** (section 8). Don't hold the plan hostage to a paid tool, and offer to plug in exports later.

## 4. Procedure

1. **Seed list by offering × market × language.** For each priority product/service, write the terms the business uses, then the terms customers use (from reviews, support, sales, marketplaces). Add modifiers: price/cost, best, near me / city names, brand, comparison ("vs"), problem/symptom, and how-to questions.
2. **Harvest what's already working.** Pull GSC queries (last 3–12 months, by page) and group them by page. These are proven relevance and quick-win candidates: positions 4–20 with decent impressions.
3. **Expand.** Use the volume tool's keyword ideas/matching terms, competitor keywords (for 3–5 search competitors), and question reports. Without a tool, use autocomplete (alphabet/modifier patterns), PAA, and related searches, logged-out, in the right market.
4. **Clean.** Remove irrelevant terms: products not sold, areas not served, wrong intent such as jobs/free/DIY where the business sells a service. Normalize spelling variants (Arabic: `scripts/arabic_keywords.py`). Dedupe.
5. **Classify intent** for each term or cluster (section 5). Verify by SERP sample for the head terms of each cluster.
6. **Cluster** (section 6).
7. **Map clusters to pages** (section 7), marking `mapping_status` as `existing`, `improve`, `new`, `gap`, or `merge`.
8. **Prioritize** (section 8).
9. **Write up**: method, sources and dates, coverage limits, clusters with their mapped pages, priorities, and "not covered / why".

## 5. Intent classification

Use the SERP, not the word alone. The dominant result types tell you what Google thinks searchers want.

| Intent | Signals | Typical page type |
|---|---|---|
| **Informational** | how/what/why, guides, PAA-heavy SERP, articles/videos ranking | Guide, article, FAQ hub |
| **Commercial investigation** | best, top, vs, review, comparison, "for [use case]"; listicles and reviews ranking | Comparison, buying guide, category with guidance |
| **Transactional** | buy, price, order, specific product/model, shopping results | Product, category, pricing, booking page |
| **Local** | near me, city/area names, local pack shown | Location page + GBP |
| **Navigational** | brand or site names | Home / brand page; protect, don't chase |

Record mixed SERPs as mixed (e.g. "transactional + local pack"). A mixed SERP often means two page types can rank. Note which type dominates the top positions.

## 6. Clustering

Goal: one cluster = one search intent that one page can satisfy.

- **SERP-overlap method (preferred when a tool provides it, or by manual sampling for head terms):** if two keywords share several of the same top-10 URLs, one page can usually target both. The common heuristic is "3+ shared URLs in the top 10". It's a convention, not an official rule.
- **Semantic method (fallback):** group by product/attribute/problem and intent. Validate the largest clusters with SERP samples.
- Name each cluster by its primary keyword, the clearest and most representative term. It isn't necessarily the highest-volume one.
- Keep spelling and script variants inside the same cluster (Arabic variants, Arabic vs English terms with identical intent where the SERP overlaps).
- Separate clusters when the intent differs even though the words are similar ("split AC price" transactional vs "how to choose a split AC" commercial investigation).

## 7. Keyword-to-page mapping and cannibalization check

`keyword-map.csv` columns (from the template): `cluster_id, page_group, primary_keyword, secondary_keywords, language, market, intent, serp_features, volume, volume_source, volume_date, target_url, alternate_language_url, language_pair_status, page_type, mapping_status, keyword_priority, notes`.

**Language pairing.** Each row is one cluster in **one** language. Arabic and English keywords are researched independently; never force a direct translation pair.
- `page_group` links the rows (in any language) that serve the same page group.
- `alternate_language_url` is the equivalent page in the other language. Leave it empty when no matching page exists.
- `language_pair_status` is one of `both`, `ar-only`, `en-only` or `mismatch`. A cluster that exists in one language only is valid.

Rules:
- **One primary cluster per URL, one URL per primary cluster.** Secondary keywords support the primary. They don't make the page "about everything".
- Map to the existing page that best matches the intent before proposing a new page. New pages need a reason (a gap, or an intent mismatch).
- `mapping_status`: `existing` (already targets it well), `improve` (right page, needs work), `new` (create), `gap` (no page; decide later), `merge` (consolidate pages).
- **Cannibalization check after mapping:** list primary keywords assigned to more than one URL, then cross-check with GSC query→page data. A shared keyword in the map is only **Potential**. Whether it's **Confirmed** is decided solely by the canonical rule in on-page-seo.md (Cannibalization): first-party split, same intent, and a documented harm signal. Resolve per on-page-seo.md.
- Every row with a number in `volume` must have `volume_source` and `volume_date`. Otherwise leave `volume` empty.

## 8. Prioritization

### With volume data
For each cluster, consider:
- **Business value** (1–5): how close it is to revenue, and how important the offering is.
- **Demand**: the tool's volume, as a relative band (high/medium/low within this market), not an exact figure.
- **Winnability**: current position (GSC), competitor strength on that SERP (qualitative or the tool's difficulty, labelled), and whether the site can produce a better page.
- **Effort**: does it need a new page, an improvement, or a technical fix?

Clusters then become roadmap tasks, which are prioritized with the SKILL.md model.

### Keyword priority (`keyword_priority`: High / Medium / Low)
Record one value per cluster in `keyword-map.csv`:

| Value | Meaning |
|---|---|
| **High** | Business value 4–5 and realistically winnable |
| **Medium** | Business value 3, or high value but low winnability or high effort |
| **Low** | Business value 1–2, or informational with a weak link to conversion |

Without volume data, apply the same scale using the relevance-only factors below.

This is **not** finding severity. P0–P3 belong to findings and tasks (the tracker's `priority` column) and come only from the SKILL.md formula. When a cluster becomes a task, its keyword priority informs that task's *Business relevance* score; it never sets or overrides the task's P-band.

### Without volume data: relevance-only prioritization
When no volume source exists, prioritize transparently by:
1. Business value (from discovery).
2. Evidence of demand **without numbers**: the term appears in autocomplete, PAA, or related searches; competitors build pages for it; customers use it (support/sales); Trends shows non-zero interest in the region (relative).
3. Current visibility, if GSC is available.
4. Effort.

Label the research "relevance-prioritized, no volume data" at the top of the document and in every client-facing summary. Offer to re-rank once exports from a tool are supplied.

## 9. Arabic and multilingual notes

Brief pointers. The detail is in arabic-and-multilingual-seo.md.
- Don't translate keyword lists. Research each language natively: Arabic searchers may use MSA, dialect (Egyptian, Gulf), English product terms, or Arabizi (Latin-script Arabic, e.g. "takyeef"), depending on the product and market.
- Spelling variants (أ/ا/إ, ة/ه, ى/ي, with or without "ال") can look like separate keywords in tools. Normalize and group them with `python <skill-dir>/scripts/arabic_keywords.py`, then check whether the SERPs actually differ before treating variants as separate targets.
- Research per country: Egypt and Saudi vocabulary and SERPs differ. Use country-specific databases in tools, and sample SERPs with the right country/language settings.
- Many queries in Egypt mix scripts ("سعر iphone 15"). Keep mixed-script queries.

## 10. Pitfalls

- Reporting tool volumes as fact, or adding volumes from different tools together.
- Targeting high-volume head terms the site can't realistically win, or that don't convert.
- Ignoring the queries the site already ranks for (GSC is the cheapest research there is).
- One page per keyword variant, which leads to thin pages and cannibalization.
- Treating Trends 0–100 as volume.
- Skipping the SERP check and mapping a transactional page to an informational SERP.
- Not dating the research. SERPs and tools change.
