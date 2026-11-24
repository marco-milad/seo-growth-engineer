# 03 · SEO audit: [Business name]

Audit date(s): [YYYY-MM-DD] · Mode: [mode] · Status: [draft / reviewed at G2 on YYYY-MM-DD]
Findings register: `03-audit/findings.csv` · Evidence: `03-audit/evidence/`

## 1. Summary (plain language, half a page)

[3-5 things that matter most, with priority. Any P0 first. No jargon. Example shape:
"Google can only see about half of the product pages because ... (P1)."]

## 2. Scope and method

| Item | Value |
|---|---|
| Hosts / properties | |
| Languages / markets | |
| Page types (templates) audited | |
| Sample sizes per template | |
| Rendering method | [raw HTML via site_check.py / rendered via URL Inspection / headless browser] |
| Tools and data sources (with dates) | |
| Modules run / skipped (with reason) | |

## 3. Data reliability

[Tracking gaps found first, e.g. GA4 missing on checkout, consent mode, duplicated tags, GSC domain vs URL-prefix property. How they limit conclusions.]

## 4. Findings by priority

[Paste the ranked table from `python scripts/prioritize_findings.py 03-audit/findings.csv --md ...`]

### Detail: P0 / P1 findings

#### [ID] [Title]
- **Bucket / domain:**
- **Scope:** [URLs / template / locations]
- **What we saw:** [description]
- **Evidence:** [file paths, screenshots, export rows, with dates]
- **Why it matters:** business impact / SEO impact
- **Recommendation:**
- **Effort / dependencies:**
- **How we'll validate:**
- **Confidence:** [High/Medium/Low] because [reason]

## 5. Findings by domain

### Technical
[short narrative + IDs]
### On-page
### Content
### Local
[or "Skipped: purely online business, no customer-facing location (see 01-discovery.md §9)"]
### Off-page
### Analytics & measurement
### International / Arabic
### AI-search visibility

## 6. Opportunities (not defects)

| ID | Opportunity | Why it fits this business | Effort |
|---|---|---|---|

## 7. Missing data and items needing investigation

| ID | What is unknown | Needed from | How to get it |
|---|---|---|---|

## 8. Not checked / why

| Area | Why not checked | What would unlock it |
|---|---|---|

## 9. Next step

G2: please review the findings. Mark any you disagree with. Then: [Stage 5 strategy / roadmap / end of Audit-Only engagement].
