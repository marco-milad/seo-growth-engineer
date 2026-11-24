# Handover: SEO Growth Engineer skill (v1.1.0, 2026-11-24)

For: the skill's owner and anyone extending it. Claude does not load this file during use. It documents what exists, how to use it, and what is still open.

## 1. What was built

A personal Claude Code skill that runs a complete, evidence-based SEO engagement. It works as an operating system with gates, not as a checklist.

- **Orchestrator** (`SKILL.md`, 308 lines as of v1.1.0):
  - The 9-stage workflow and the 4 operating modes.
  - Start-of-engagement rules: the first turn's shape, mode timing, uninspectable sites, outcome questions.
  - The engagement folder, with `PROJECT_STATE.md` for resuming in a later session.
  - Module selection by business signal, including businesses with no website.
  - The evidence standard, finding schema, priority formula, and gates G1–G5, including owner-executed changes and P0 handling outside Execution mode.
  - The tool-access protocol.
- **16 references**, loaded only when relevant (progressive disclosure). Key facts were checked against Google sources on 2026-11-24.
- **18 templates** (13 Markdown + 5 CSV) for every deliverable.
- **5 deterministic scripts** using only the Python standard library, so there's nothing to install.
- **3 fictional examples** showing the expected interaction quality.
- **Changes since v1.0.0:** see CHANGELOG.md (1.0.1 and 1.1.0). The test history in sections 9 and 9a below describes the original v1.0.0 testing.

## 2. Folder structure

```text
~/.claude/skills/seo-growth-engineer/
├── SKILL.md
├── CHANGELOG.md
├── HANDOVER.md
├── references/
│   ├── project-discovery.md          ├── seo-audit-framework.md
│   ├── on-page-seo.md                ├── off-page-seo.md
│   ├── technical-seo.md              ├── local-seo.md
│   ├── analytics-and-measurement.md  ├── reporting-framework.md
│   ├── keyword-research.md           ├── content-strategy.md
│   ├── competitor-analysis.md        ├── seo-implementation-qa.md
│   ├── industry-adaptations.md       ├── arabic-and-multilingual-seo.md
│   ├── ai-search-visibility.md       └── tools-and-integrations.md
├── templates/
│   ├── project-state-template.md            ├── project-discovery-template.md
│   ├── access-and-data-template.md          ├── seo-audit-template.md
│   ├── findings-template.csv                ├── keyword-research-template.md
│   ├── keyword-map-template.csv             ├── competitor-analysis-template.md
│   ├── seo-strategy-template.md             ├── roadmap-template.md
│   ├── implementation-tracker-template.md   ├── implementation-tracker-template.csv
│   ├── change-proposal-template.md          ├── change-log-template.md
│   ├── qa-checklist-template.md             ├── performance-report-template.md
│   ├── locations-master-template.csv        └── nap-input-template.csv
├── scripts/
│   ├── site_check.py          (robots, sitemaps, raw-HTML on-page signals, hreflang reciprocity)
│   ├── prioritize_findings.py (validates findings.csv, computes score / band / quick win)
│   ├── gsc_compare.py         (GSC period comparison, movers, CTR outliers)
│   ├── nap_check.py           (Arabic-aware NAP consistency)
│   └── arabic_keywords.py     (Arabic variant normalization and grouping)
└── examples/
    ├── example-kickoff-arabic-ecommerce.md
    ├── example-findings-and-change-proposal.md
    └── example-no-analytics-access.md
```

## 3. How to invoke

- Explicitly: `/seo-growth-engineer`, optionally followed by the request, e.g. `/seo-growth-engineer audit https://example.com, audit only`.
- Naturally: the description triggers on SEO audits, strategy, keyword research, indexing/ranking problems, SEO fixes in code, GBP/local SEO, backlinks, SEO reports, and Arabic requests (سيو، تحسين محركات البحث، تصدر جوجل), for a site you own or a client already engaged. Pitching or winning a new client (proposals, offers, pitch audits) belongs to `client-proposal`, and the description says so.
- The skill was confirmed as discoverable in this session's skill list right after creation.

## 4. Starting a new SEO project

1. Open Claude Code in the site's repository (best, because Claude can inspect the code), or anywhere if you only have the URL.
2. Describe the business and the goal in one or two sentences, in Arabic or English.
3. Claude infers what it can, then asks one decision question at a time. That question is usually the mode first, if you didn't name it.
4. After you confirm the G1 summary, it creates `seo-engagement/<slug>/`. If you're inside a git repository, it asks first where the folder should go.
5. In later sessions it reads `PROJECT_STATE.md` and resumes from the recorded stage.

## 5. Operating modes

| Mode | Stages | Changes made? |
|---|---|---|
| Audit Only | 1–4 | No (a P0 fix only if you ask; that one change set then goes through G4) |
| Strategy & Planning | 1–6 | No |
| Execution | 1–9 | Yes: one approved change set at a time (G4), validated with evidence (G5) |
| Focused task | minimal 1 + the relevant slice | Only with explicit approval (full G4, or the owner-executed path for actions you perform yourself) |

## 6. Connecting external tools

Nothing is connected today. No SEO MCP servers or API keys were found in this environment on 2026-11-24, and no integration was claimed as working. Options, from simplest:

- **Exports (works now):** CSV exports from Search Console, GA4, GBP, Ahrefs/Semrush and Screaming Frog. Put them in the engagement's `data/` folder. `gsc_compare.py` reads GSC Performance exports directly.
- **PageSpeed Insights API:** no bundled script calls the PSI API or reads an API key. If you want Claude to call the API directly (with your approval), create a free key in Google Cloud and keep it in an environment variable you set yourself. The keyless API often returns 429. The web UI (pagespeed.web.dev) needs no key.
- **Official MCP or API connectors** for GSC, GA4, Ahrefs or Semrush: see `references/tools-and-integrations.md` for each tool's official vs community status, required plan, and limits. Claude will explain the option and ask before installing anything.
- **Browser automation:** a logged-in browser on a client account is used only with explicit authorization and stays read-only by default. Research always uses plain fetches or an isolated, logged-out browser.
- **Three kinds of access** (SKILL.md, Tool and data access protocol, rule 7): an authorized human account; a connector or service identity you configure; and Claude itself, which has no Google account and can never be added, invited or made a manager. Without a verified connector, data comes through exports, screenshots, or an authorized read-only browser look.

## 7. What requires manual configuration

- Granting access, exporting data, and setting API keys. Always done by you, in your own accounts.
- Lighthouse / Screaming Frog. Not installed. Claude will ask before installing either.
- Verifying Search Console / GA4 for new sites. This is a G4 change when Claude edits the site, or your own action in your account.

## 8. Current limitations

- `site_check.py` reads raw HTML only; it doesn't execute JavaScript. On JS-heavy sites, confirm "missing" tags with URL Inspection or a rendered check. It is a sampler, not a full crawler. For large sites, use Screaming Frog or GSC data.
- No live connector was tested, because none is installed. Every tool section describes the documented capabilities, not ones tested here.
- Google features and documentation change often. Facts carry "checked 2026-11-24" stamps. Re-verify the dated facts (structured data support, GSC reports, GBP features, API quotas) when they matter to a decision.
- Arabic market notes are partly field observations, labelled as such. There are no market statistics without sources.
- The scenario tests checked the first turn of each conversation. No full end-to-end engagement against a real site has been run with the skill yet.

## 9. Tests and results

### Script tests (local fixture site + fixture CSVs; all pass after fixes)

| Script | Planted cases | Result |
|---|---|---|
| site_check.py | 2-hop redirect chain, 404 in sitemap, meta + X-Robots noindex, 2 canonicals, relative canonical, broken JSON-LD, non-reciprocal hreflang, robots-blocked URL in sitemap, duplicate titles, missing alt/lang/viewport | All detected. Two fixes made: redirected URLs no longer double-count their target's issues, and robots-blocked sitemap URLs are now reported |
| prioritize_findings.py | Manual P0, quick win, low-confidence/high-impact, missing-data row, a row with 6 errors | Correct scores and bands; all 6 errors reported; invalid row labelled |
| gsc_compare.py | Two-file mode, comparison-export mode with prefix auto-detection, Arabic queries, new/lost rows | Correct deltas and CTR-outlier detection |
| nap_check.py | Arabic letter variants, Arabic-Indic digits, +20 phone formats, www/https, a keyword-stuffed GBP name | Cosmetic differences separated from real mismatches; stuffed name flagged |
| arabic_keywords.py | Diacritics, tatweel, hamza/alef, ta marbuta, Arabic-Indic digits, Arabizi | Variants grouped; volume carried through only when supplied; Arabizi flagged |

### Scenario tests (independent agents loading the skill fresh and answering the first turn)

| # | Scenario | Core behaviour | Issues found → fixed |
|---|---|---|---|
| 1 | New Arabic/English e-commerce (Next.js) | Pass: Egyptian Arabic with English terms, nothing invented, Local held pending a question, measurement first | Mode-timing contradiction; folder timing; uninspectable site; "young site" wording → fixed in SKILL.md and project-discovery |
| 2 | Dental group, 6 branches in two countries, listings held by ex-staff | Pass: ownership is the owner's job, no passwords, Local dominant, YMYL bar | No owner-side recovery playbook; booking platforms; practitioner listings → added to local-seo and industry-adaptations |
| 3 | GCC payroll SaaS with GSC/GA4/Semrush but no connector | Pass: Strategy mode recommended, exports-first, Semrush labelled estimate | "Add the analyst" assumes a human; Content not a selectable module; planned Arabic; payroll as YMYL → fixed |
| 4 | Bakery, incomplete Maps listing, wants fake reviews and #1 | Pass: fake reviews refused with legitimate alternative, no #1 promise, every edit owner-approved | No path for businesses with no website; G4 too heavy for owner-executed changes → fixed |
| 5 | Corporate site, 40% drop after URL migration, Audit Only | Pass: mode not re-asked, drop not blamed prematurely, 16-month urgency, exact export paths | No post-migration playbook; P0 vs Audit Only; Wayback as a source → added |
| 6 | Kids' courses site, no GSC/GA4, "how much traffic will I get" | Pass: "any number would be made up", setup framed as a gated change, mode recommended | No standard wording for outcome questions; classifying missing tracking → fixed |

### 9a. Retest after the fixes (scenarios 4 and 5, fresh agents)

| # | Result | Remaining issues found → fixed |
|---|---|---|
| 4 Bakery, no website | **Pass.** Focused task confirmed in one line. Fake reviews refused with alternative. Owner-executed light approval path used. No folder created in an unrelated repo; state kept in the conversation | local-seo said "every reply is G4" (now points to the owner-executed path); no single-listing claim check (added); Focused-task G1 (now a one-line confirmation); a cap on quick items (now up to 3) |
| 5 Migration audit | **Pass.** Audit Only confirmed without re-asking. Fetch failure handled as our limitation with a P0 check. Drop classified Needs investigation. §19a playbook used. 16-month urgency computed. P0-in-Audit-Only path correct | Two leftover "add us as a user" phrases (fixed in the audit framework, the example and the access template); no export click paths (added to tools §5); expired-window and 1,000-row guidance (added to §19a); a first-turn tie-breaker (added to SKILL.md) |

After this round, a contradiction sweep finds no remaining "add the analyst / add us as a user" conflicts, and every internal link and path resolves.

## 10. Recommended next improvements

1. **Run one real engagement end to end** on a site you own (e.g. a client in Audit Only mode), and fix what real data exposes.
2. **Connect Search Console properly:** decide between exports, the official API with a service account set up by you, or a vetted MCP. Then add a tested adapter section to tools-and-integrations.md.
3. **Add a rendered check** (headless browser) as an optional, approval-gated companion to `site_check.py` for JS sites.
4. **Trigger-accuracy evaluation:** run skill-creator's description optimizer with about 20 should/shouldn't-trigger queries, especially to separate it from the `client-proposal` skill. That skill is for winning a client; this one is for doing the work.
5. **Quarterly fact refresh:** re-check every "checked YYYY-MM-DD" stamp and log the updates in CHANGELOG.md.
