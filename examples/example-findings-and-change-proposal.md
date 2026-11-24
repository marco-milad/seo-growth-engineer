# Example: well-formed findings, priority scoring, and a G4 change proposal

> FICTIONAL. URLs, dates and evidence paths are invented to show the format only.

## A good finding (Confirmed issue)

| Field | Value |
|---|---|
| id | TEC-004 |
| bucket | confirmed-issue |
| domain | technical |
| title | Category pages have no canonical; filter URLs are indexable duplicates |
| scope | Category template: `/ar/category/*` and `/en/category/*`, including `?sort=`, `?brand=` and `?capacity=` variants |
| description | Category pages emit no `<link rel="canonical">`. Filter and sort parameters create crawlable URLs with the same main content, and none of them carries `noindex`. |
| evidence | `03-audit/evidence/site-check-2026-11-24/issues.csv` (canonical-missing on 15/15 sampled category URLs); GSC Pages report export `data/gsc-pages-2026-11-24.csv` showing 380 "Duplicate without user-selected canonical" URLs, all parameter variants |
| data_source | site_check.py; Google Search Console |
| data_date | 2026-11-24 |
| business_impact | Category pages are the main entry point for "مكيف سبليت"-type queries that lead to orders |
| seo_impact | Google chooses canonicals itself; ranking signals are split; crawl is spent on duplicates |
| impact / urgency / business_relevance / effort / confidence | 4 / 3 / 5 / 2 / High |
| recommendation | Self-referencing absolute canonical on category pages; parameter variants canonicalize to the clean category URL; keep parameter URLs out of the sitemap |
| dependencies | None |
| validation_method | site_check.py on the same sample; GSC URL Inspection on 5 URLs (user-declared vs Google-selected canonical) after recrawl |
| owner_role | Frontend developer |
| status | open |

Score: (2×4 + 3 + 5) × 1.0 ÷ 2 = **8.0 → P1**. Quick win: impact 4 ≥ 3, effort 2 ≤ 2, confidence 1.0 ≥ 0.8 → **yes**.

## A bad finding, and what's wrong with it

> "ONP-009: Titles are not optimized. Impact high. Fix all titles to include keywords. This will boost rankings by 30%."

- No scope: which templates or URLs?
- No evidence and no data source or date.
- "Not optimized" isn't an observation. It needs to say what was seen (missing, duplicated, truncated, mismatched with the query).
- The prediction is invented, which is a promise the skill forbids.
- "Fix all titles" isn't actionable. It needs the pattern per template and the priority pages.

## A Low-confidence item that must not be silently dropped

OFF-002, potential-issue: "Possible lost links after the 2025 domain change". Impact 4, urgency 2, relevance 3, effort 3, confidence Low.
Score: (8 + 2 + 3) × 0.5 ÷ 3 = 2.17 → P3, flagged **validate-first** by `prioritize_findings.py`. The roadmap gets a task "Pull referring domains for the old domain from a backlink tool or GSC Links (old property) to confirm".

## G4 change proposal (abbreviated)

> **CHG-003: Canonicals on category pages** (T-006, from TEC-004) · production · deployed by: the client's developer via their usual deployment pipeline
>
> **What and why:** Add a self-referencing canonical to category pages. Point filter and sort variants to the clean category URL. Google currently treats 380 variants as duplicates and chooses canonicals by itself.
>
> **Affected:** `pages/category/[slug].vue` (canonical set with `useHead`), plus a helper in `composables/useCanonical.ts`. No URL or content changes.
>
> **Expected impact:** Signals consolidate on the clean category URLs, and crawling of duplicates should drop over the following weeks. There's no guaranteed ranking change.
>
> **Risks:** A wrong base URL could canonicalize every page to the homepage. Mitigation: unit check plus site_check.py on a staging preview before deploy.
>
> **Rollback:** Revert the single commit. Canonicals return to absent, which is the current state.
>
> **Validation:** site_check.py on the same 15 URLs right after deploy. Then GSC URL Inspection on 5 URLs once they're recrawled.
>
> Reply "approve CHG-003", or narrow the scope.

After the user approves, the change-log row records the quote, the commit, the QA evidence path, and the G5 date. The tracker moves T-006 through `approved → in-progress → implemented`. It only becomes `validated` once the QA evidence is accepted.
