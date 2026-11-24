# 02 · Access & data collection status: [Business name]

Checked: [YYYY-MM-DD] · By: [Claude session / person] · Mode: [mode]

> Status values: **Verified** (a read succeeded today) · **Available, untested** · **Needs user action** · **Unavailable**.
> Never write credentials, tokens or API keys here. Access is granted through each tool's own sharing to (a) an authorized human account or (b) a connector or service identity the user configures, never to "Claude" (SKILL.md, Tool and data access protocol, rule 7).

## 1. Environment inspection

| Check | Result |
|---|---|
| MCP tools in this session relevant to SEO | [list names, or "none found"] |
| Browser automation available | [yes: which; logged-in client session? → read-only rules apply / no] |
| Local CLIs (checked without installing) | python [ver], node [ver], lighthouse [found / not installed], Screaming Frog CLI [found / not] |
| Environment variables present (names only, values not printed) | [e.g. PSI_API_KEY set / not set] |
| Existing exports/reports in project folder | [paths] |
| Codebase access | [repo path / none] |

## 2. Source inventory

| Source | Status | Scope (property / host / locations) | Data range | Pulled on | Method (API / MCP / export / browser / public) | Confidence effect |
|---|---|---|---|---|---|---|
| Google Search Console | | | | | | |
| Google Analytics 4 | | | | | | |
| Google Business Profile | | | | | | |
| Bing Webmaster Tools | | | | | | |
| Ahrefs / Semrush | | | | | | |
| Screaming Frog crawl | | | | | | |
| PageSpeed Insights / CrUX | | | | | | |
| Lighthouse (lab) | | | | | | |
| Website source code | | | | | | |
| CMS admin | | | | | | |
| Existing SEO reports / exports | | | | | | |
| Public data (live site, SERPs, competitor sites) | Verified | | | | site_check.py / web fetch | |

## 3. Required user actions (ordered by value)

| # | Action | Exact steps | Unblocks | Priority |
|---|---|---|---|---|
| 1 | Share Search Console data | Export Performance (Queries + Pages) and indexing reports. Click paths are in tools-and-integrations.md §5. Or connect an approved connector. If a human consultant is involved: Settings → Users and permissions → Add user → Restricted | Indexing, queries, CWV field data | High |
| 2 | | | | |

## 4. Access limitations and effect on conclusions

| Domain | Limitation | Effect |
|---|---|---|
| Technical | | |
| On-page | | |
| Local | | |
| Off-page | | |
| Analytics | | |

Example: "No GSC → Google-side indexing status (what Google actually indexed) is at most Medium confidence; reproducible live checks (e.g. `noindex` in the HTML) stay High. No query data, so cannibalization can only be Potential (on-page-seo.md, Cannibalization)."

## 5. Proposed installs or connections (awaiting approval, none done)

| Option | What it adds | Cost / risk | Decision |
|---|---|---|---|
| | | | pending |

## 6. Baseline captured

| Metric | Value | Source | Range | Saved file |
|---|---|---|---|---|
| | | | | data/[file] |

## 7. Checklist

- [ ] Every candidate source listed with status and date checked
- [ ] Verified sources have scope, date range, pull date
- [ ] User actions written as exact steps
- [ ] Limitations and confidence effects stated per domain
- [ ] No secrets in this document or requested in chat
- [ ] Installs listed as options only
- [ ] Next step: audit proceeds with what is available
