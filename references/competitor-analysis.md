# Competitor Analysis

Load this at Stage 5 (strategy), or during the audit when context about competitors is needed to judge a finding (e.g. "is our category content thin compared with what ranks?"). It covers identifying the right competitors, comparing them on evidence, and turning gaps into specific opportunities.

Output: `04-research/competitor-analysis.md` (template: `templates/competitor-analysis-template.md`). Conventions are in `SKILL.md`.

---

## 1. Ground rules

- **Evidence or nothing.** Every competitor number (traffic estimate, keyword count, referring domains, authority score) names its tool and date, and is labelled as an estimate. Never produce competitor "traffic" figures without a tool.
- **Public data only,** collected respectfully: normal page fetches, no logins, no aggressive crawling, no bypassing access controls. Research browsing uses plain web fetches or an isolated, logged-out browser profile, never a session logged into client accounts (SKILL.md).
- The goal is to find **specific, actionable gaps for this client**, not to describe competitors for their own sake.
- Keep the client's sensitivities in mind. Some clients don't want certain competitors named in client-facing reports. Ask.

## 2. Identify the right competitors

There are three kinds; you usually need the first two:

| Type | Definition | How to find |
|---|---|---|
| **Business competitors** | Who the client loses customers to | Ask the client (discovery) |
| **Search competitors** | Who ranks for the client's priority clusters, regardless of business model | SERP samples for head terms of each priority cluster (logged-out, correct country/language, dated); the tool's "competitors"/"organic competitors" report |
| **SERP occupiers** | Marketplaces, directories, publishers, aggregators that hold positions the client wants | Same SERP samples |

Select 3–5 search competitors per market/language. Include at least one business competitor the client named. Note when marketplaces or aggregators dominate. That changes the strategy: the client may need to compete *on* those platforms too, or target different intents.

## 3. Inputs

- Priority clusters from the keyword map (keyword-research.md), or at least the priority offerings + markets if keyword research isn't done yet.
- Client-named competitors.
- Tool access (Ahrefs/Semrush/Similarweb) if available, or user exports.
- If no tool is available, do the analysis qualitatively from SERPs and public pages, and say so at the top of the document.

## 4. Comparison dimensions

Pick the dimensions that matter for this business model (industry-adaptations.md). Don't fill every row for every project.

| Dimension | What to compare | Evidence |
|---|---|---|
| **SERP presence** | Which competitors appear for which priority clusters, and with which page types | SERP sample table (cluster × competitor, page type, date, location) |
| **Site architecture** | Category/service structure, depth, use of hub pages, location pages, filters indexed or not | Navigation, sitemaps, `scripts/site_check.py` sample on their public pages (polite, small sample) |
| **Page-type quality** | For each priority page type: content depth, unique elements (specs, prices, comparisons, FAQs, reviews, media), trust signals | Side-by-side review of 1–3 ranking pages per type |
| **On-page patterns** | Title/H1 conventions, use of prices/locations in titles | Page fetches |
| **Technical** | Rendering approach, structured data types, speed indicators (PSI/CrUX public data if it exists for their origin), mobile UX | PSI (origin-level CrUX shows only if the origin has enough data), `site_check.py` JSON-LD types |
| **Content coverage** | Clusters they cover that the client doesn't; formats (guides, tools, video) | The tool's keyword gap, or a manual sitemap/blog review |
| **Authority / links** | Referring domains (tool estimate), the types of sites linking, linkable assets | The tool's backlink overview and link intersect (off-page-seo.md) |
| **Local** | GBP presence, categories, review count/recency, photos (public view) | Public Maps/GBP view; local-seo.md |
| **AI search** | Whether competitors are cited for sampled prompts (indicator only) | ai-search-visibility.md method |
| **Conversion approach** | CTAs, contact methods, pricing transparency, offers | Page review |

## 5. Procedure

1. **Define the cluster set** (5–15 priority clusters) and markets.
2. **Sample the SERPs** for the head term of each cluster. Record the date, location/language settings, top 10 domains + page types, and SERP features. Save it as `04-research/serp-samples-YYYY-MM-DD.csv` or a table in the doc.
3. **Choose competitors** from the samples plus the client-named list.
4. **Run the dimension comparisons** that apply. Keep evidence links/paths.
5. **Gap analysis**, expressed as opportunities:
   - **Content gaps:** clusters where competitors have a page and the client doesn't (→ `CNT-` opportunity).
   - **Quality gaps:** the client has a page, but the ranking competitors' pages offer specific things it lacks, e.g. "price ranges", "size guide", "comparison table", "doctor bio" (→ `ONP-`/`CNT-`).
   - **Structure gaps:** e.g. competitors have indexable subcategory/location pages that match search demand (→ `ONP-`/`TEC-`/`LOC-`).
   - **Authority gaps:** link sources competitors share (→ `OFF-`).
   - **Local gaps:** GBP categories, review velocity, photos (→ `LOC-`).
6. **Advantages to exploit:** what the client has that competitors don't (real expertise, inventory, locations, price transparency, faster delivery, bilingual content). These feed the strategy's positioning.
7. **Write it up:** competitor set and why, method/sources/dates, comparison tables, prioritized opportunities with IDs, and the limits ("traffic estimates not used: no tool access").

## 6. Interpreting competitors honestly

- Correlation is not a recipe. "The top results all have 2,000 words" doesn't mean length makes them rank. Look for what *serves the searcher*.
- Big brands rank partly on brand strength and links. Don't copy their tactics where the client lacks their authority. Find intents and niches where the client's specific advantages win.
- Competitors may use risky tactics (bought links, doorway pages). Note them neutrally. Never recommend copying them, and don't assume they'll keep working.
- Tool traffic estimates for small sites in Arabic markets can be very unreliable. Prefer SERP presence and page-quality evidence there.

## 7. Typical outputs

| Opportunity example | Prefix | Bucket |
|---|---|---|
| Competitors rank with city-specific service pages; the client has one generic page | LOC / ONP | Opportunity |
| Ranking category pages include buying guidance and FAQs; the client's are bare grids | ONP / CNT | Opportunity |
| Three competitors are listed by the national industry association; the client isn't | OFF | Opportunity |
| Competitors use Product markup with offers; the client has none | TEC | Opportunity (or Confirmed issue if markup is broken) |
| Marketplaces hold 6 of the top 10 for transactional terms | — | Strategy note: target long-tail/commercial-investigation terms, and consider marketplace presence |

## 8. Pitfalls

- Choosing competitors only from the client's list and missing who actually ranks.
- Presenting tool estimates as fact or as precise.
- Overly broad comparisons that don't lead to actions.
- Copying competitor content structure wholesale instead of out-serving it.
- For Arabic/multi-market work, competitors differ per country and language. Sample each market separately (arabic-and-multilingual-seo.md).
