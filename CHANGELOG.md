# Changelog: seo-growth-engineer

All notable changes to this skill. Dates are ISO (YYYY-MM-DD). Versioning: MAJOR changes the workflow, gates or finding schema; MINOR adds references, templates or scripts; PATCH is wording, fact updates or fixes.

## [1.1.0] - 2026-11-24

Phase 2 of the audit remediation (batches B1–B7). A minor release, because it adds templates. Finding IDs refer to the audit.

### B1 - Script safety
- [F-26] prioritize_findings.py:
  - `--write` copies the original to `findings.csv.bak-YYYYMMDD-HHMMSS` with exclusive creation, so a timestamp collision gets `-2`, `-3`, … and an existing backup is never overwritten. It then replaces the file atomically (temp file + swap).
  - New `--out` writes the scored CSV elsewhere and leaves the input untouched. `--out` and `--md` refuse an existing file unless `--overwrite` is given. `--out` may not point at the input, and `--write`/`--out` are mutually exclusive.
  - All output paths are checked before anything is written (exit 2).
  - The number of normalized bucket values and changed computed cells is reported.
- [F-27] site_check.py:
  - `--out` must be a new or empty folder, unless `--overwrite` is given. This is checked before any network request (exit 2), and an existing file path is refused.
  - Only same-site pages are fetched (same host, ignoring `www.`; same port). Off-host sitemap URLs are listed and reported (`sitemap-off-host-urls`); off-host `--urls` entries are skipped and reported (`off-host-url-not-fetched`). New `--allow-off-host` fetches them.
  - Sitemap files on other hosts are still read and listed as external.
  - The script now returns its exit code.
- [F-28a] nap_check.py no longer writes `__pycache__` into the skill when importing its sibling module.
- site_check.py: network failures read "network error (…)" instead of "HTTP URLError …".
- Docs: SKILL.md scripts table; on-page-seo.md and technical-seo.md §19a command notes; seo-audit-framework.md §9 now shows the real usage instead of a `--help` placeholder.

### B2 - Script accuracy
- [F-10a] site_check.py:
  - Sitemap elements are matched by local name, so namespace-less and non-standard-namespace sitemaps and indexes parse.
  - New summary warnings: missing or non-standard namespace, an unexpected root element, a sitemap or index with 0 entries. The summary section is now "Sitemap errors and warnings". `issues.csv` is unchanged.
- [F-10b] site_check.py:
  - noindex is detected by exact directive (`noindex` or `none`), not by substring.
  - All X-Robots-Tag headers are read. A user-agent prefix applies to the directives after it.
  - Only directives with no prefix or with a `googlebot` prefix raise `x-robots-noindex`. Other crawlers' noindex raises the new info issue `x-robots-noindex-other-agent`.
- [F-28b] nap_check.py: opening hours are compared as times when both sides parse:
  - 24h, AM/PM, Arabic ص/م, Arabic-Indic digits, several ranges, "daily"/"يوميا", 24/7, closed/مغلق.
  - Ambiguous AM/PM (e.g. `9-5`) → new review status `review`.
  - Day-name schedules and invalid times keep the previous text comparison.
- [F-28c] nap_check.py: a cell with several phone numbers is compared as a set:
  - New review statuses `contains-canonical` (all canonical numbers plus others) and `partial-match` (some shared). Disjoint sets stay MISMATCH.
  - The review statuses are shown in bold but not counted as hard mismatches.
- [F-28d] arabic_keywords.py: a digit counts as Arabizi only when it leads a word followed by ≥2 letters or sits between letters with ≥3 letters around it. `ps5`, `mp3`, `3d`, `5g`, `b2b` and `h2o` are no longer flagged.
- [F-11] gsc_compare.py:
  - New `--columns` mapping (header names or 1-based numbers; bounds, duplicate, unknown/missing-name and non-numeric checks). No guessed aliases.
  - Comma/tab/semicolon detection. The Arabic decimal mark (٫) and percent sign (٪) are parsed.
  - stderr uses UTF-8. A non-UTF-8 input encoding is noted on stderr.
  - English auto-detection is unchanged. Existing error paths keep exit code 1; new mapping errors exit 2.
- [B2-c] CSV decoding in gsc_compare, nap_check, arabic_keywords and prioritize_findings: UTF-16 is used only when the file has a UTF-16 BOM. Trying it blindly mis-decoded Windows-1256 Arabic files as garbage (reproduced with 60 realistic header lines).
- Docs: SKILL.md scripts table; analytics-and-measurement.md §14.

### B3 - Gates and safety wording (no script changes)
- [F-19] Legal and compliance:
  - SKILL.md non-negotiable 2 now states that the skill gives no legal advice and guarantees no regulatory compliance; legal, privacy and consent questions go to the owner and qualified counsel.
  - The P0 band says "suspected legal or compliance exposure (escalate…; the skill doesn't determine legality)".
  - The consent checklist item no longer says "as legally required".
  - The industry pitfall no longer states "violations" as fact.
- [F-22] IndexNow and Bing URL submissions, one four-case rule in SKILL.md, seo-implementation-qa.md, technical-seo.md, tools-and-integrations.md and the change-proposal template. The "low-risk" exemption was removed.
  - Setup and configuration: full G4.
  - Automatic pings from an approved setup: covered by that approval (scope logged, no per-ping approval).
  - Manual one-off submissions: explicit approval.
  - Bulk or submit-all: full G4.
- [F-23] Analytics and tracking configuration needs full G4 whoever executes it: GA4 filters, key events, data streams, data retention, GTM tags and triggers, consent configuration, the GSC↔GA4 link, and defining or changing the UTM convention.
  - Applying an already-approved UTM convention to a GBP link stays on the owner-executed path.
  - The skill audits and proposes, never applies.
  - "Analytics sets up measurement first" became "plans measurement first; any setup is a change set".
  - The tracking-gap checklist is now explicitly an audit; UTM examples are marked illustrative.
- [G4] The gate table row now names the owner-executed approval and says sensitive changes always need the full proposal. "Configuration" in the full-G4 list is clarified as site, server, CMS or analytics configuration. Adding a team member stays owner-executed, but only after the user approves the person's identity and access role.

### B4 - Evidence and priority consistency (no script changes)
- [F-12] analytics-and-measurement.md: the question-query regex is now `^(how|what|why|كيف|ما|ماذا|ليه|ازاي|إزاي)([\s?؟]|$)`, with the same word list and start anchoring. The old `\b` never matched after Arabic letters under RE2's ASCII-oriented word boundary. Added a note that `\b`/`\w` don't suit Arabic.
- [F-13] seo-audit-framework.md: the good-finding example score was corrected from 8.5 to 8.0. The formula is unchanged.
- [F-14] The bucket (what the evidence shows) is now decided separately from confidence (how reliable it is):
  - Rules, an allowed-combinations list and five examples were added to seo-audit-framework.md §7, plus one line in SKILL.md.
  - Example 3 keeps Low confidence, with the reason given: the conclusion is inferred from a Medium-confidence third-party source.
  - The "no GSC → at most Medium" caps in tools-and-integrations.md and the access template now apply only to Google-side indexing status.
- [F-15] One canonical cannibalization rule in on-page-seo.md, which keyword-research.md and arabic-and-multilingual-seo.md now point to.
  - **Confirmed** needs a GSC query→page split for the same query and period, the same intent by SERP, and at least one documented harm signal (URL alternation, or sustained underperformance compared with the stronger page's earlier performance).
  - Otherwise it stays **Potential**. A keyword on several URLs alone is never Confirmed.
- [F-16] ai-search-visibility.md: "decision needed" is no longer a bucket. The issue is Potential, with the client decision recorded in `dependencies`. seo-audit-framework.md §7 states the rule.
- [F-17] The technical, local and Arabic typical-findings tables are marked indicative (the formula decides; P0 only under SKILL.md's global override conditions).
  - "Canonical on every page → homepage" is P1, or P0 only if site-wide indexing loss is already happening.
  - GBP profile suspended is indicative P1, with immediate escalation. The global P0 list is unchanged.
- [F-18] analytics §13 is the canonical causal ladder (coincided with / consistent with / likely caused by; never "caused by" or "thanks to our work"). It also adds four measurement-attribution labels (observed, assisted/modelled, inferred, unavailable), kept separate from causation. reporting-framework.md §8 reuses the same phrases and conditions; "most likely related" was removed.

### B5 - Fictional example replaced (F-20)
- The fictional bag store ("Rihla Bags": Egyptian Arabic, Next.js, travel bags) was replaced by **"Example Appliances KSA" (أجهزة المثال)**, a deliberately fictional business.
  - A Saudi online home-appliance retailer: split ACs, refrigerators, washing machines; no showroom; nationwide delivery.
  - Built on Nuxt (`nuxt.config.ts` i18n `/ar` + `/en`, `pages/`, `useSeoMeta`/`useHead`, `public/robots.txt`). No hosting provider is named.
  - Primary conversion: online orders. Secondary: a business quote-request form.
  - The opening message, Turn 1 and the G1 summary are in Saudi Arabic with English SEO terms.
- example-findings-and-change-proposal.md: the filters are now `?brand=`/`?capacity=`; the counts are 15 sampled URLs and 380 duplicates; the query flavour is "مكيف سبليت"; the change set is now in Nuxt files. Scores are unchanged (8.0 → P1, quick win; OFF-002 2.17 validate-first).
- The "What this example demonstrates" block and the example filenames are unchanged.
- Bag vocabulary in references replaced with appliance terms. The Arabic lessons are preserved:
  - arabic-and-multilingual-seo.md: ta marbuta ثلاجة/ثلاجه; plural ثلاجات/ثلاجة; dialect Egyptian تكييف vs Gulf مكيف (MSA مكيف هواء); "split ac price egypt"; the Arabizi example "takyeef split"; the normalization note's vocabulary pair (تكييف vs مكيف); slugs `/ar/مكيفات-سبليت`, `/ar/mukayyifat-split`, `/ar/split-air-conditioners`, with the percent-encoding sample corrected to `%D9%85…`.
  - keyword-research.md: the cluster example is now "split AC price" vs "how to choose a split AC"; the Arabizi example is now "takyeef".
  - reporting-framework.md: the unsourced search-volume comparison became a neutral placeholder.

### B6 - Official source check (F-24)
- ai-search-visibility.md: the Search Console claim, previously labelled Official without a source, was checked against official pages and is supported.
  - It now uses Google's name, **Search generative AI control**, and the menu path Settings → Search generative AI.
  - Covered features: AI Overviews, AI Mode, Generative AI features in Google Discover.
  - The details bullet was relabelled from [Third-party] to **[Official]**: the include, exclude and inherit options with their defaults, and "isn't used as a ranking or inclusion signal affecting other parts of Search".
  - Rollout: Google blog, 3 June 2026 UK-only start; worldwide 31 August 2026, a date the Help page confirms itself.
  - The preferred-sources line, the control matrix and audit step 4 use the official name. The two "(verify)" notes the evidence resolves were removed. No snippet claim was added.
  - Sources:
    - https://support.google.com/webmasters/answer/16908024
    - https://developers.google.com/search/docs/appearance/preferred-sources
    - https://blog.google/products-and-platforms/products/search/new-opportunities-control-and-insights-for-website-owners/

### B7 - Templates, documentation and release
- **Added** `templates/locations-master-template.csv`:
  - `location_id` is the internal, stable store ID and is distinct from `gbp_profile_id`, the Google Business Profile ID.
  - Arabic and English NAP; owner and manager **roles only** (no names, emails or passwords).
  - local-seo.md links to it.
- **Added** `templates/nap-input-template.csv` (`location_id,source,name,address,phone,hours,website`):
  - Compatible with `nap_check.py`, which is unchanged.
  - The first row per location is `Owner master`, for `--canonical-source`. Use one file per language.
  - local-seo.md documents how to use it.
- **Keyword map:**
  - New columns `page_group`, `alternate_language_url` and `language_pair_status` (`both`/`ar-only`/`en-only`/`mismatch`). Each row is one cluster in one language, with no forced translation pairs.
  - `priority` was renamed to **`keyword_priority`** (High/Medium/Low), defined in keyword-research.md §8. It's separate from the P0–P3 finding/task priority, informing Business relevance only.
  - arabic-and-multilingual-seo.md §7 now points to these columns.
- **`mapping_status`** uses the same five values (`existing`, `improve`, `new`, `gap`, `merge`) in keyword-research.md (step 7 and §7), on-page-seo.md and keyword-research-template.md.
- **Tracker:** new `executor` column after `owner_role` (`claude`, `owner`, or a named role). `owner_role` is the accountable party. The executor doesn't change approval rules. Documented in the tracker template and seo-implementation-qa.md §2.
- **Roadmap:** the five 12-column task tables became Task / Title / Priority / Owner tables. `06-tracker.csv` is the single source of truth for task details; seo-implementation-qa.md §2 updated to match.
- **Counts:** there are 18 templates, **13 Markdown + 5 CSV**. SKILL.md's template list and HANDOVER.md (version, counts, folder tree, SKILL.md line count, a CHANGELOG pointer) were updated; HANDOVER's historical test sections are unchanged.
- **Correction:** the 1.0.1 documentation stated the then-16 templates as "12 Markdown + 4 CSV". The actual split was 13 + 3. The 1.0.0 entry below has been corrected in place.

## [1.0.1] - 2026-11-24

Phase 1 of the audit remediation (pilot readiness). Audit finding IDs are in brackets.

### Fixed
- [F-02] on-page-seo.md: the `site_check.py` command used a nonexistent `pages` mode, which silently audited the host `https://pages`. It now passes the site root first, and documents sampling (`--sample`) and the 200-page `--max-pages` default.
- [F-03] technical-seo.md §19a: the old-URL check had no site argument (the command would exit with an error), and the default cap silently truncated long lists. Both corrected.
- [F-04] Access wording: SKILL.md now defines three kinds of access in rule 7: an authorized human account; a connector or service identity the user configures; and Claude itself, which can never be added, invited or made a manager. SKILL.md rules 5 and 2, tools-and-integrations.md (GA4/GBP access lines), project-discovery.md T1.9, seo-audit-framework.md and the access template were aligned.
- [F-05] One status lifecycle, defined in SKILL.md: `implemented` ≠ `validated` (G5 technical QA) ≠ `monitoring` (validated, search-side effect still being measured). seo-implementation-qa.md, reporting-framework.md, the tracker template and the performance-report template now use these meanings. Reports present only `validated`/`monitoring` items as done, and never present `monitoring` as a proven result.
- [F-06] Owner-executed changes:
  - Count as `implemented` only after the owner confirms them with evidence.
  - Removal requests, disavow files and GBP name/address/primary-category changes always need the full G4 proposal, whoever executes them.
  - The "needs G4" wording for owner-only actions was replaced in seo-implementation-qa.md, industry-adaptations.md, local-seo.md and technical-seo.md.
  - The change-proposal template gained Executor and Approval-path fields plus an owner-executed variant; the change-log template gained executor and owner-confirmation columns.
- [F-07] The description and a new "Scope" note separate SEO delivery (this skill) from pitching or winning a client (`client-proposal`). The over-broad clause "even if 'SEO' is never said" was removed. Description: 1,013 characters.
- [F-08] site_check.py: robots.txt results are now classified as follows. The per-page `robots_allowed_googlebot` is now `allowed`/`disallowed`/`no-rules`/`unknown`, and no crawl-permission conclusion is drawn when the rules are unknown.

  | robots.txt response | Treated as |
  |---|---|
  | 200 | Rules read |
  | 404 and other 4xx | No published rules |
  | 401/403 | Access denied, permissions unknown; a high issue `robots-txt-access-denied` |
  | 5xx, 429, network error | Unavailable, permissions unknown; a high issue `robots-txt-unavailable` |
- [F-09] nap_check.py:
  - Phone and website must match exactly after normalization; there is no more fuzzy "similar" for them.
  - Phone normalization is country-aware: a leading `0` converts only for trunk-zero countries given via `--country`; closed-plan countries (KW, QA, BH, OM, TN) get their code on 8-digit numbers; otherwise nothing is inferred. The old fallback that prepended the country code to any number was removed.
  - Websites ignore only known tracking parameters (`utm_*`, `gclid`, `fbclid`, …), keep every other parameter (order-insensitive), and keep path case.
- [F-21] HANDOVER.md and CHANGELOG.md: the template count was corrected from 17 to 16, the SKILL.md line count is now exact, and the PSI API key note no longer implies that a bundled script uses it.

## [1.0.0] - 2026-11-24

### Added
- `SKILL.md` orchestrator, covering:
  - The 9-stage workflow (discovery → access & data → audit → findings & priority → strategy → roadmap → execution → QA → monitoring & reporting).
  - The three operating modes plus a Focused-task path.
  - The engagement folder with `PROJECT_STATE.md` for resuming across sessions.
  - Module selection by business signal.
  - The evidence standard (High/Medium/Low confidence; five buckets).
  - The finding schema with domain ID prefixes, and the shared status vocabulary.
  - A transparent priority formula: `(2×Impact + Urgency + Business relevance) × Confidence ÷ Effort`, with P0 override, P1–P3 bands and a quick-win rule.
  - Approval gates G1–G5, including a per-change-set G4 proposal.
  - The tool-access protocol and safety rules.
- 16 reference files, covering:
  - Workflow: `project-discovery`, `seo-audit-framework`, `seo-implementation-qa`, `reporting-framework`, `tools-and-integrations`.
  - Domains: `on-page-seo`, `off-page-seo`, `technical-seo`, `local-seo`, `analytics-and-measurement`.
  - Strategy: `keyword-research`, `content-strategy`, `competitor-analysis`.
  - Cross-cutting lenses: `industry-adaptations`, `arabic-and-multilingual-seo`, `ai-search-visibility` (added beyond the original brief because AI Overviews / AI Mode now affect organic visibility).
- 16 templates (13 Markdown + 3 CSV; originally miscounted as 17, total corrected in 1.0.1; the Markdown/CSV split corrected in 1.1.0): project state, discovery, access & data, audit, findings CSV, keyword research + keyword-map CSV, competitor analysis, strategy, roadmap, implementation tracker (MD + CSV), change proposal, change log, QA checklist, performance report (technical / executive / next-period plan).
- 5 stdlib-only Python scripts (no installs):
  - `site_check.py`: robots, sitemaps and raw-HTML on-page signals, hreflang reciprocity.
  - `prioritize_findings.py`: schema validation and scoring.
  - `gsc_compare.py`: period comparison, movers, CTR outliers.
  - `nap_check.py`: Arabic-aware NAP comparison.
  - `arabic_keywords.py`: variant normalization and grouping.
- 3 fictional examples: an Arabic e-commerce kickoff, findings plus a G4 proposal, and auditing without GSC/GA4.

### Verified facts (checked 2026-11-24 against Google sources; re-check at time of use)
- FAQ rich results were deprecated and no longer appear in Google Search from 2026-05-07. HowTo was deprecated in Sept 2023. The sitelinks search box was removed in Nov 2024. Several more types were phased out from June 2025 (technical-seo.md §14).
- The Search Console Generative AI performance report (AI Overviews + AI Mode) was rolled out to all sites by 2026-08-31 and shows impressions only.
- Core Web Vitals "good" thresholds: LCP ≤ 2.5 s, INP ≤ 200 ms (INP replaced FID in March 2024), CLS ≤ 0.1.
- The Indexing API is only for JobPosting / BroadcastEvent pages.

### Tested
- All scripts run against a local fixture site and fixture CSVs, which deliberately include redirect chains, a 404, meta + header noindex, multiple canonicals, broken JSON-LD, non-reciprocal hreflang, a robots-blocked URL listed in the sitemap, Arabic NAP variants and Arabic keyword variants.
- Six scenario tests (see `HANDOVER.md`).

### Fixed during validation
- `site_check.py`: page-level checks no longer run on redirected URLs, which had double-counted their issues against the final URL. Sitemap URLs disallowed by robots.txt are now reported instead of silently skipped.
- `prioritize_findings.py`: rows with validation errors are labelled `invalid`, not left blank.
- The SKILL.md description was shortened to fit the 1,024-character limit.
- FAQ / Generative-AI-report wording was aligned with the verified Google sources across the technical, analytics and AI-search references.

### Changed after scenario testing (6 scenarios, same day)
- SKILL.md "Start of every engagement" rewritten:
  - Language comes first.
  - The mode is settled within the first two turns, or confirmed in one line if the user already named it, with recommendation rules.
  - A turn shape: one decision question plus optional one-line facts.
  - A fallback for when nothing can be inspected.
  - Provisional answers to "where do I start?".
  - Standard handling of "rank #1 / how much traffic" questions.
  - The engagement folder is created only after the mode and location are agreed, and Claude asks first in any git or unrelated repository.
- Module table gained rows for: no website (Focused local path), planned-but-not-live language, young live sites, Content as an explicit module, and payroll/tax/HR as YMYL.
- Approval gates: lighter handling for owner-executed changes; P0 handling in Audit Only / Strategy modes.
- Evidence standard: a never-installed GSC/GA4 counts as a Confirmed issue, and the metrics it would have provided are Missing data.
- Access protocol: Claude can't be added as a Google user (exports, a connector the user sets up, screenshots, or an authorized read-only browser instead), plus the 16-month urgency for GSC history.
- New playbooks:
  - Diagnosing a migration that already happened (technical-seo.md §19a).
  - Recovering GBP listings held by former staff or agencies, practitioner profiles, platform listings as citations, the website field when there's no site (local-seo.md).
  - Planned-language pre-launch decisions (arabic-and-multilingual-seo.md §7).
  - Healthcare booking platforms and no-website local businesses (industry-adaptations.md).
- project-discovery.md, seo-audit-framework.md and tools-and-integrations.md aligned with the above.
