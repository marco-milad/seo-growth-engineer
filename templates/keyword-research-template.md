# 04 · Keyword research: [Business name]

Date: [YYYY-MM-DD] · Markets: [e.g. EG, SA] · Languages: [ar (Egyptian + MSA), en] · Map: `04-research/keyword-map.csv`

> Never invent volume, difficulty, CPC or trend numbers. Every number names its tool, database/country and pull date.
> One tool is the primary volume source; don't mix tools in one column.

## 1. Method and sources

| Source | Used for | Scope | Pulled |
|---|---|---|---|
| Google Search Console (queries) | What already brings impressions | [property, country filter, 16-month range] | |
| [Ahrefs / Semrush / Keyword Planner] | Volume [range/estimate], difficulty | [database] | |
| Google Trends | Relative interest / seasonality (0-100, not volume) | | |
| Autocomplete / People Also Ask / related searches | Qualitative phrasing, questions | [language, location, date] | |
| Customer language (sales, WhatsApp, reviews, support) | Real wording | | |
| Competitor pages | Topic coverage | | |

If no volume tool is available: prioritization is **relevance-only** (business relevance × intent × current GSC impressions where available), and the document says so.

## 2. Seed terms (from discovery)

| Product / service / location | Seeds (Arabic variants, English, Arabizi where real) |
|---|---|

## 3. Variant normalization

`python scripts/arabic_keywords.py raw-keywords.csv --column Keyword --out 04-research/keyword-groups.csv`
Variants grouped: [N keywords → M groups]. Notes on dialect vs MSA choices:

## 4. Intent classification

| Intent | Meaning here | Example clusters |
|---|---|---|
| Transactional | Ready to buy/book/contact | |
| Commercial investigation | Comparing options | |
| Informational | Learning / problem-solving | |
| Navigational | Looking for a brand/site | |
| Local | Near-me / city / branch | |

Head terms verified by SERP sample (date, location, language): [list]

## 5. Clusters → pages

| Cluster | Primary keyword | Intent | Target URL | mapping_status (existing / improve / new / gap / merge) | keyword_priority (High / Medium / Low) | Why |
|---|---|---|---|---|---|---|

## 6. Cannibalization check

| Query / cluster | Competing URLs | Evidence (GSC query → page split, dates) | Proposed resolution |
|---|---|---|---|

## 7. Priorities

[Top clusters in order, with the reasoning. Volume only with its source.]

## 8. Not covered / why

| Area | Reason | What would unlock it |
|---|---|---|
