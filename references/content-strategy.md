# Content Strategy

Load this at Stage 5, when turning keyword clusters, content gaps, and audit findings into a content plan. It is also relevant at Stage 7 when drafting or reviewing content. It covers what to create, improve, merge, or remove; how to brief it; how to keep it trustworthy; and how to publish safely.

Outputs feed `05-strategy.md` (template: `templates/seo-strategy-template.md`), the roadmap, and the tracker. Content findings and opportunities use the `CNT-` prefix (SKILL.md).

Contents:
1. Principles (official guidance)
2. Inputs
3. Content inventory and decisions
4. Building the plan
5. Content briefs
6. Writing and review rules
7. AI-assisted content: what is and isn't acceptable
8. Publishing, updating, and pruning
9. Measurement
10. Pitfalls

---

## 1. Principles (official guidance)

- **People-first content.** Google's systems aim to reward content created primarily to help people, not to rank. Use Google's self-assessment questions: originality, completeness, insight beyond the obvious, a trustworthy presentation, and whether a visitor leaves satisfied. Think in terms of **Who** created it (clear authorship where readers expect it), **How** (process, testing, use of automation), and **Why** (to help people, not mainly to attract search visits) (Source: Creating helpful, reliable, people-first content, https://developers.google.com/search/docs/fundamentals/creating-helpful-content, checked 2026-11-24).
- **E-E-A-T** (experience, expertise, authoritativeness, trust; trust matters most) is a concept from the Search Quality Rater Guidelines. It isn't a single ranking factor. Use it as a quality lens, especially for YMYL topics.
- The **helpful content system** became part of Google's core ranking systems in March 2024. There's no separate "HCU" to recover from; quality improvements are assessed by the core systems over time.
- **Non-commodity content** is Google's own emphasis for AI-era search. Content that adds something only this business can say (first-hand experience, its own data, real photos, specific policies) beats generic summaries (Source: Optimizing your website for generative AI features on Google Search, https://developers.google.com/search/docs/fundamentals/ai-optimization-guide, checked 2026-11-24). See ai-search-visibility.md.

## 2. Inputs

- The keyword map with clusters and `mapping_status` (keyword-research.md).
- On-page findings: thin, duplicate, cannibalized, and intent-mismatched pages (on-page-seo.md).
- GSC page/query performance, if available.
- Competitor content patterns (competitor-analysis.md).
- **Business capacity:** who can write, who can approve (subject-matter expert), which languages, what cadence is realistic, and what proof assets exist (photos, case studies, data, credentials). Ask this explicitly. A plan the business can't sustain is a bad plan.
- Facts the business has confirmed: prices, policies, service areas, materials, credentials. Keep a "confirmed facts" list in `01-discovery.md` and write only from it.

## 3. Content inventory and decisions

For the indexable pages (or a template-level sample on big sites), decide one action per page:

| Decision | When | Notes |
|---|---|---|
| **Keep** | Performs and matches its intent | Light refresh only if facts are stale |
| **Improve** | Right page for the cluster, but thin, outdated, poor intent fit, or weak E-E-A-T signals | Most common and usually the best ROI |
| **Merge** | Several weak pages on one intent (cannibalization) | 301 the weaker pages into the strongest one; update internal links (G4) |
| **Re-target** | Page is good but competes with a sibling, or targets the wrong intent | Change its primary cluster |
| **Create** | A cluster with business value and no suitable page | Needs a brief and an owner |
| **Noindex** | Needed for users but has no search value (thin filters, internal search, thank-you pages) | Technical decision; see technical-seo.md |
| **Remove** | No users, no links, no value, nothing to merge into | Return 404/410, or 301 if there's a close equivalent with links/traffic. G4 gate |

Evidence for each decision: traffic/impressions (GSC), links (off-page data), conversions (GA4), and a quality judgement written as a reason. Pruning without data is risky. If data is missing, prefer **improve** or **merge** over **remove**.

## 4. Building the plan

1. **Group the work by cluster and funnel stage**: transactional/commercial first for most businesses (closest to revenue), then commercial investigation (buying guides, comparisons), then informational content that supports and links to the commercial pages.
2. **Pillar/hub structure** where topics are broad: a hub page for the topic, with spokes for subtopics that link to each other and to the money pages. Internal linking is part of the content plan, not an afterthought.
3. **Fix before you create.** Improving existing pages that already have impressions usually beats publishing new ones. Sequence improvements first, unless a gap is clearly more valuable.
4. **Match formats to SERPs.** If the SERP shows videos, comparison tables, or local packs, plan for them (e.g. video embeds, comparison tables, a local landing page plus GBP).
5. **Calendar at a cadence the business can sustain.** State the assumption ("2 improved pages + 1 new guide per month, assuming the owner reviews within 5 days").
6. **Each content item becomes a roadmap task** with an ID, cluster, target URL, owner, acceptance criteria, and validation method.

## 5. Content briefs

Each brief (one per new or substantially improved page) includes:
- Target URL (existing or proposed slug) and page type.
- Primary keyword/cluster, secondary terms, and the intent, with the SERP sample date.
- The searcher's job: what they need to know or decide, and the next action we want them to take (the CTA).
- Required sections and questions to answer, from PAA, support questions, and competitor coverage. Note what competitors *miss*.
- **Unique value to include:** the business's own data, photos, process, pricing logic, policies, expert quotes, case examples. If none exists, say so; the brief is weaker for it.
- Facts to confirm with the business, marked `[CONFIRM]`.
- Author/reviewer (for YMYL: a credentialed reviewer), and sources to cite.
- Internal links in (which pages should link here) and out (which money pages it supports).
- Metadata pattern (title/description direction, not stuffed), schema type if relevant (technical-seo.md), and the image plan (original images, alt text).
- Language/market specifics. For Arabic, write natively; don't translate (arabic-and-multilingual-seo.md).

## 6. Writing and review rules

- Never publish claims the business hasn't confirmed: prices, guarantees, materials, certifications, results, medical or legal statements, competitor comparisons. Wrong claims damage trust and can create legal exposure.
- Write for the reader's decision. Put the answer early, then the detail. Clear headings. Tables for specs and comparisons.
- Show expertise honestly. Use a real author or reviewer with real credentials. No fabricated personas, reviews, testimonials, or case studies.
- Cite sources for factual or YMYL claims. Use primary sources where possible.
- Keep consistency with structured data. Visible content must match the markup (technical-seo.md).
- Accessibility basics: descriptive alt text, readable contrast, meaningful link text.
- Content drafts go to the user for review. **Publishing is a public action that needs approval** (SKILL.md gates).

## 7. AI-assisted content: what is and isn't acceptable

Official position: using generative AI is not against Google's guidelines in itself. Generating many pages without adding value for users may violate the **scaled content abuse** policy (Source: Google Search's guidance on using generative AI content on your website, https://developers.google.com/search/docs/fundamentals/using-gen-ai-content, checked 2026-11-24; Spam policies, https://developers.google.com/search/docs/essentials/spam-policies, checked 2026-11-24).

In this skill:
- **Fine:** using AI to outline, draft from the business's confirmed facts, summarize the business's own data, translate as a first draft that a native speaker then edits, or suggest titles. Always followed by human review for accuracy and voice.
- **Not fine without explicit discussion:** bulk generation of location/service/product pages that differ only by swapped variables; publishing unreviewed drafts; programmatic pages without unique, useful data per page.
- **Never:** fabricated experience ("I tested…" when nobody did), fake reviews or authors, mass automated publishing without explicit approval.
- Programmatic SEO can be legitimate when each page has unique, useful data (e.g. real inventory, real location data). Assess it page type by page type, and pilot with a small batch before scaling. Scaling needs explicit approval.

## 8. Publishing, updating, and pruning

- Publishing is a G4 change set: the pages, the URL, internal links added, the sitemap update, and the rollback (unpublish).
- Updates: change the content meaningfully, not just the date. Don't fake freshness by bumping dates without changes.
- Pruning/merging: follow section 3, with redirects mapped, internal links updated, and the sitemap updated (seo-implementation-qa.md).
- After publishing: confirm indexability, that the page is in the sitemap, and the internal links. Optionally request indexing in GSC for key pages; that's an approval-gated action (SKILL.md), and quotas apply.

## 9. Measurement

Per content item or cluster, track:
- Indexed status (URL Inspection).
- GSC impressions, clicks, CTR, and average position for the page and its cluster queries.
- GA4 engagement and conversions from organic landing sessions.
- Assisted conversions where tracked.

Compare equal periods. Allow time: new content often takes weeks to months to settle. Separate correlation from causation (reporting-framework.md). AI-feature visibility is measured per ai-search-visibility.md.

## 10. Pitfalls

- A content calendar built from keyword volume alone, disconnected from business priorities.
- Publishing new posts while existing pages with impressions stay weak.
- Thin "SEO blog posts" with no unique value, and no links to the commercial pages they're meant to support.
- Location or service pages made by swapping city names (doorway pages). See local-seo.md.
- Translated content that ignores how the market actually searches. See arabic-and-multilingual-seo.md.
- Updating dates without updating content.
- Treating word count as a quality target.
- For industry-specific requirements (YMYL reviews, product data, SaaS comparison pages), see industry-adaptations.md.
