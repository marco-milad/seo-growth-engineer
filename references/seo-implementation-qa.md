# Stages 6–8: Roadmap, Implementation, and QA

This file covers turning approved findings into a roadmap (Stage 6), executing changes safely behind the G4 gate (Stage 7), and proving each change works before it counts as done (Stage 8, G5). Conventions (status vocabulary, gates, priority bands, engagement folder) are in SKILL.md.

Templates: `templates/roadmap-template.md`, `templates/implementation-tracker-template.md` / `.csv`, `templates/change-proposal-template.md`, `templates/change-log-template.md`, `templates/qa-checklist-template.md`.

## Contents

1. Roadmap construction
2. Task fields
3. G3: approving the roadmap
4. Change proposals and the G4 workflow
5. Working in a codebase
6. Working in a CMS
7. Redirects and migrations
8. Rollback
9. QA methods by change type
10. G5 and status rules
11. Change log / audit trail

## 1. Roadmap construction

Inputs: the G2-accepted `findings.csv`, the strategy (`05-strategy.md` in Strategy/Execution modes), the discovery constraints (capacity, deadlines, who owns the platform).

Group tasks into horizons. The horizon follows from priority, effort, and dependencies, not from the calendar alone:

| Horizon | What belongs here |
|---|---|
| **Quick wins** | Quick-win findings (Impact ≥ 3, Effort ≤ 2, Confidence ≥ 0.8). Usually configuration, template tweaks, titles on priority pages, missing canonicals, sitemap fixes, GSC/GA4 setup gaps |
| **High-priority fixes** | P0 (immediately) and P1 items that aren't quick wins: indexing blockers, rendering problems on revenue templates, broken conversion tracking |
| **Short-term** (next ~1–2 months) | P2 template-level improvements, internal linking, structured data, local fixes, content updates to existing priority pages |
| **Medium-term** (~2–6 months) | New page types and content clusters, architecture changes, location page programs, link-earning assets, multilingual expansion |
| **Long-term** (6+ months) | Brand/authority programs, digital PR, new markets, major replatforming, ongoing content operations |

Sequencing rules:
- Technical blockers before on-page and content work on the same pages. Content before links to it.
- Measurement fixes (tracking gaps, baseline capture) go at the very start. Otherwise nothing after them can be evaluated.
- Low-confidence, high-impact items enter as **"validate first"** tasks before the fix task.
- Bundle changes to the same template into one change set, to reduce release cycles and simplify QA, but keep unrelated risks apart so a rollback doesn't undo good work.
- Respect capacity from discovery: don't schedule 30 content pieces a month for a team that can approve four.

## 2. Task fields

Each task is a row in `06-tracker.csv`, the single source of truth for its full details. `06-roadmap.md` lists it only by task ID, short title, priority and owner, without repeating the fields below:

| Field | Content |
|---|---|
| Task ID | `T-###`, never reused |
| Description | What will be done, concretely (template/URLs/files) |
| SEO category | On-page / Off-page / Technical / Local / Analytics / Content / International / AI-search |
| Finding IDs | The findings it resolves (e.g. `TEC-004, ONP-012`) |
| Priority | P0–P3 (inherited from the highest-priority linked finding unless justified otherwise) |
| Expected impact | Mechanism and direction, e.g. "consolidates duplicate variants so the main product URL is indexed". No numeric promises |
| Effort | 1–5, consistent with the finding score |
| Owner / role | Accountable party, e.g. frontend developer, content writer (Arabic), client marketing manager, SEO (us) |
| Executor | Party that performs the change: `claude`, `owner`, or a named role (e.g. `client-developer`). It doesn't bypass approval: the approval path still follows SKILL.md (Approval gates) |
| Dependencies | Other task IDs, access, decisions, content inputs |
| Acceptance criteria | Observable conditions that define "done", e.g. "all 40 sampled product URLs return a self-canonical; variant URLs canonicalize to the main URL; none in the sitemap" |
| Validation method | How it'll be proven (section 9), and when (immediately vs after recrawl) |
| Status | SKILL.md vocabulary: `open`, `proposed`, `approved`, `in-progress`, `implemented`, `validated`, `monitoring`, `won't-fix`, `blocked` |

## 3. G3: approving the roadmap

Present the roadmap with the strategy: horizons, owners, the first change sets proposed, and what is needed from the client. G3 approves *the plan*. It does **not** approve any individual change: each change set still needs G4. Record the G3 date in `PROJECT_STATE.md`.

## 4. Change proposals and the G4 workflow

For every change set (template: `templates/change-proposal-template.md`):

1. **Prepare:** inspect the current state, then draft the exact change (diff, config values, copy, redirect map).
2. **Propose:** the five elements from SKILL.md (what and why with task/finding IDs, affected resources, expected impact and risks, rollback plan, validation method). Add the environment (staging/production), timing (avoid peak sales windows), and who deploys.
3. **Wait for an explicit "yes" to this proposal.** Partial approval ("do the canonicals, not the redirects") narrows the scope. Re-confirm the narrowed set.
4. **Log** the proposal and the decision in `07-changes/change-log.md` with a `CHG-###` ID.
5. **Execute** only the approved scope. If you discover something new mid-change, stop and propose it separately.
6. **Report:** files/resources changed, what changed, anything that deviated from the proposal.
7. **QA** (section 9) → evidence in `08-qa/` → G5.

Actions that always need explicit approval, even when small: indexing or removal requests, IndexNow or Bing URL submissions, sitemap submission changes, disavow, any GBP edit/reply/post, outreach messages, publishing content, robots.txt changes, redirects, analytics or tracking configuration, adding a team member, bulk operations, anything touching production.

Which approval path applies:
- **The full G4 proposal** (the five elements above) when you execute the change, and, whoever executes it, for:
  - code, redirects, robots.txt/sitemaps, bulk operations, and any site, server, CMS or analytics configuration change;
  - analytics and tracking configuration: GA4 filters, key events, data streams, data retention, GTM tags and triggers, consent configuration, the GSC↔GA4 link, and defining or changing the UTM convention. You audit and propose these; you never apply them on your own;
  - IndexNow setup or configuration changes, and bulk or submit-all URL submissions (IndexNow or Bing);
  - GSC removal requests, disavow files, and changes to a GBP business name, address or primary category.
- **The owner-executed path** for everything else the owner performs from their own account using your draft:
  - review replies, GBP posts, hours, photos;
  - UTMs on a GBP link using an already-approved UTM convention;
  - GSC indexing requests, and manual one-off IndexNow or Bing URL submissions;
  - adding a team member, after the user approves that person's identity and the access role.

  See below.
- **Automatic IndexNow pings** from an approved setup are covered by that setup's G4 approval. Record the approved scope (which events ping which URLs) in the change log; there's no per-ping approval.

### Owner-executed changes

Many actions can only be performed by the owner, because Claude has no Google account (SKILL.md, Tool and data access protocol, rule 7). For these:
1. Give the exact draft (text, values, or click path), say where it goes, and give the risk in a line or two.
2. Wait for explicit approval of that draft. Log it in `07-changes/change-log.md` with Executor = owner and status `proposed`, then `approved`.
3. The action is `implemented` only after the owner confirms it's done **and** provides evidence, e.g. a screenshot of the posted reply or the saved hours. Until then it stays `approved` or `in-progress`. A recommendation or a sent draft is never "done".
4. QA and G5 apply as usual. You check the evidence, or the live result (e.g. the public listing), before marking it `validated`.

## 5. Working in a codebase

1. **Inspect the architecture first.** Framework and version, rendering mode per route (SSR/SSG/ISR/CSR), how metadata is generated (Next.js `metadata`/`generateMetadata`, `next/head`, Nuxt `useHead`, Angular `Meta`/`Title`, React Helmet), how robots/sitemap are built, the i18n routing, and existing schema components. Read the existing SEO helpers before writing new ones.
2. **Understand current behaviour.** Reproduce the issue locally or on the live site (raw HTML via `site_check.py`, rendered HTML in a browser) so you can show before/after.
3. **Follow project conventions:** file structure, naming, lint rules, component patterns, i18n handling, commit style. Reuse existing utilities (e.g. a `buildMetadata()` helper) instead of adding parallel ones.
4. **Focused diffs.** Change only what the approved proposal covers. No drive-by refactors, formatting churn, or dependency upgrades.
5. **Preserve functionality.** SEO changes can break things: a new canonical helper that throws on missing data, a middleware redirect loop, a sitemap generator that times out at build. Consider edge cases: empty translations, missing images, unpublished items, query parameters.
6. **Run the project's own checks:** type-check, lint, tests, and the production build. Run *all* of them. A type-check can pass while the build fails, and vice versa. Report the exact commands and results. If a check fails, say so. Never claim success.
7. **Verify the output, not just the code:** run the production build/start (or a preview deployment) and inspect the actual HTML responses.
8. **Report** files changed (paths), what changed in each, commands run with results, and anything still unverified.
9. **Version control:** commit or push only when the user asks. Never commit client data, exports, or secrets. Keep the engagement folder out of the repo unless agreed.

Framework notes:
- **Next.js App Router:** metadata must be resolvable server-side for crawlers. Check `alternates.canonical` and `alternates.languages` per locale. Note that a child `openGraph` object replaces (doesn't merge) the parent's, which drops `og:image` unless it's repeated. Watch `notFound()` vs soft 404s, and `redirect()` vs permanent redirects (`permanentRedirect()` / `next.config` `permanent: true`).
- **Client-rendered SPAs:** critical content, links, and metadata should be in the initial HTML (SSR/SSG/prerender). Confirm with raw-vs-rendered comparison and URL Inspection.
- **Status codes:** routing frameworks often return 200 for "not found" UI. Verify real 404/410 statuses.

## 6. Working in a CMS

- **Backups first:** confirm a recent backup (database + files) or a version history exists before bulk changes. Record its timestamp in the change proposal.
- **Staging:** prefer staging when available, then replicate to production. Note that many plugin settings are stored in the database and don't move with code deploys.
- **WordPress:** identify the SEO plugin (Yoast, Rank Math, AIOSEO, SEOPress) and change settings there, not in theme code, to avoid duplicate tags. Avoid stacking SEO plugins. Check caching/CDN plugins (purge after changes). Plugin and theme updates are separate decisions with their own risk.
- **Shopify:** the platform controls `robots.txt` (editable via the `robots.txt.liquid` template), sitemaps, and the URL structure (`/products/`, `/collections/`; collection-scoped product URLs canonicalize to `/products/`). Theme edits should go to a duplicated, unpublished theme first. Apps can inject duplicate schema; check after installing.
- **Webflow / Wix / Squarespace:** use the built-in SEO settings, 301 redirect manager, and custom code areas. Know the platform's limits (e.g. sitemap or hreflang control) before proposing a change that requires them.
- **Bulk edits** (CSV imports, bulk meta updates): run them on a small batch first, verify it, then do the rest. Keep the export of the "before" state as the rollback source.
- **Content publishing:** never auto-publish at scale. Each batch needs approval, and copy must not invent business facts (prices, materials, credentials, claims).

## 7. Redirects and migrations

High risk: a bad redirect map can remove a site's history from search.

- **Redirect map:** old URL → new URL, one-to-one to the closest equivalent. Never mass-redirect everything to the homepage (treated as soft 404s). Prefer 301/308 for permanent moves.
- **Avoid** chains (A→B→C) and loops. Update internal links to point to final URLs. Update the sitemap with the final URLs only.
- **Before a migration:** crawl and save the full old URL list (sitemaps, crawl, GSC top pages, top linked pages from link tools, GA4 landing pages), baseline metrics, and confirm the old domain keeps redirecting for the long term (at least a year; ideally permanently).
- **Domain moves:** use GSC's Change of Address tool after redirects are live (with approval). Verify the new property, and submit the new sitemaps.
- **Language/URL structure changes:** keep hreflang and canonicals consistent with the new URLs on day one.
- **After launch:** monitor 404s, the GSC Pages report, crawl stats, and top pages' traffic daily for the first weeks.

## 8. Rollback

Every change proposal names its rollback before execution:
- Code: revert the commit or redeploy the previous build. Confirm the host supports instant rollback.
- CMS: restore from a backup/revision, or re-import the "before" export.
- Redirects: keep the previous rules file. Know how long caches/CDNs hold redirects (301s are cached by browsers).
- robots.txt/sitemaps: keep the previous file. An accidental `Disallow: /` must be reverted immediately and treated as P0.
- GBP: record field values before editing. Some edits trigger re-verification or Google review, so rollback may not be instant. Say so in the proposal.
- Content: keep previous copies. Unpublishing is reversible, but indexed copies may persist for a while.

Define a **rollback trigger**: what observation would make you roll back (e.g. 5xx errors, a canonical pointing to the wrong host, conversion tracking breaking).

## 9. QA methods by change type

"Done" requires evidence. Store it in `08-qa/` (dated), using `templates/qa-checklist-template.md`.

| Change type | QA method | Evidence required |
|---|---|---|
| Rendered content / JS rendering | Compare raw HTML (`site_check.py` / curl) with the rendered DOM (browser); GSC URL Inspection live test → view rendered HTML/screenshot | Before/after raw vs rendered snippets for sample URLs per template; URL Inspection result |
| Titles, meta descriptions, headings | `site_check.py` on the affected URL list | CSV diff before/after; spot-check screenshots of the HTML head |
| Canonicals | `site_check.py`; check self-canonical, absolute URLs, correct host/protocol, matching language version; later, URL Inspection "Google-selected canonical" | CSV showing canonical per URL; URL Inspection on a sample after recrawl (done during `monitoring`; the task can be `validated` on the live-HTML evidence) |
| Structured data | Google Rich Results Test (for Google-supported types) and Schema Markup Validator (general schema.org validity); check the visible content matches the markup; GSC enhancement reports later | Test result links/screenshots per template; note any warnings accepted and why |
| robots.txt | Fetch the live file; test key URLs against the rules (GSC robots.txt report for Google's fetched version) | Live file copy with date; list of key URLs tested and the result |
| XML sitemaps | Fetch, validate XML, all listed URLs return 200, are canonical and indexable; GSC Sitemaps status after submission (with approval) | `site_check.py` output on sitemap URLs; GSC sitemap status screenshot |
| Status codes / 404 / 410 | Request URLs and check the real HTTP status (not just the UI) | Status table per URL |
| Redirects | Request each old URL; confirm a single hop to the right target with the intended code; no chains/loops | Redirect test table: old, status, location, final URL, hops |
| Mobile rendering / RTL | Real or emulated mobile viewport (e.g. 360–414 px); check layout, tap targets, no horizontal scroll, RTL mirroring, mixed Arabic/English text | Screenshots per template and language |
| Page speed / CWV | Lighthouse or PSI on fixed URLs, same device/throttling, median of several runs (lab); later, CrUX/GSC CWV field data | Before/after lab metrics with settings; field data when available (labelled lab vs field) |
| Internal links | Crawl or `site_check.py` link counts; confirm targets are 200 and canonical; orphan check for new pages | Link count/target table |
| hreflang | Reciprocal return links, valid language-region codes, self-reference, x-default where used, hreflang targets are canonical and 200 | Per-URL hreflang cluster table |
| Indexing | GSC URL Inspection (live and indexed), Pages report trends | Inspection results; trend screenshot after recrawl |
| Analytics events / key events | GA4 DebugView or Realtime with a test conversion; GTM preview; confirm parameters | Screenshot/export of the event arriving with correct parameters; test date/time |
| GBP edits | Re-open the public listing after Google processes the edit; confirm no pending review or suspension notice | Before/after screenshots of the public view |
| Content publishing | Page live, indexable, in the sitemap, internal links added, facts checked against the client's confirmed facts | URL list with status, sitemap inclusion, link sources |

Validation has two layers. Keep them apart:
- **Technical validation (G5):** the change itself works as specified, shown by evidence you can collect right away (live HTML, status codes, structured-data test, screenshot). That moves the item to `validated`.
- **Search-side confirmation:** Google has picked the change up and its effect shows (recrawl, Google-selected canonical, indexing, performance). This takes days to weeks and happens during `monitoring`. If it fails, open a new finding or reopen the task. Never silently downgrade a `validated` item.

Say in the tracker which search-side check is pending and when it's due.

## 10. G5 and status rules

- The lifecycle and the meaning of each status are defined once, in SKILL.md (Finding schema, Status lifecycle). In short: `implemented` = deployed or performed and confirmed live (owner actions only with the owner's confirmation and evidence); `validated` = G5 technical QA evidence accepted; `monitoring` = validated, with the search-side effect still being watched. Never mark `validated` because code was written, a deploy finished, or a draft was sent.
- A task with failed QA goes back to `in-progress` (or gets rolled back), with the failure noted.
- Deploy visibility: confirm that the deployment actually succeeded and is serving the new version (check the deployment dashboard or the live response), since failed deploys can be silent.
- G5 is the user seeing the evidence and accepting the item. Record it in the tracker and the change log.

## 11. Change log / audit trail

`07-changes/change-log.md` (template: `templates/change-log-template.md`) records every proposed and executed change, including rejected ones:

- `CHG-###`, date, linked task/finding IDs
- Proposal summary and affected resources
- Decision: approved / rejected / narrowed, by whom, when (quote the approval message briefly)
- Executor: Claude, the owner, or another named role (e.g. the client's developer). Approval path: full G4 or owner-executed
- Execution: date/time, who, what was actually changed (files, commits, settings, URLs). For owner-executed changes: the date the owner confirmed it was done, and the evidence
- QA result and evidence link, and the G5 date
- Rollback performed? When and why

Rules: append-only (don't rewrite history; add corrections as new entries), no secrets, no personal data beyond what's needed to identify the approver's role. The log also feeds report annotations (analytics-and-measurement.md, section 12).
