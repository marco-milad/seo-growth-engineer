# SEO Growth Engineer

**Version 1.1.0** (2026-11-24) · A Claude Code skill · Private repository

SEO Growth Engineer turns Claude into an SEO consultant and implementer. It runs an evidence-based SEO engagement from business discovery to measured results, for a site you own or a client you already work with. It doesn't produce generic checklists. Every recommendation traces back to the business, its pages, and evidence with a named source and date.

## Workflow

Nine stages, each with a defined output and exit point:

1. Discovery
2. Access & data
3. Audit
4. Findings & prioritization
5. Strategy
6. Roadmap
7. Execution
8. QA
9. Monitoring & reporting

Operating modes: **Audit Only**, **Strategy & Planning**, **Execution**, and a **Focused task** for single jobs. Engagement state is kept in a project folder (`PROJECT_STATE.md`), so work can resume across sessions.

## Approval-gated by design

Nothing that affects production happens without explicit approval:

- **G1–G3**: the user confirms the discovery summary, reviews the findings, and approves the strategy and roadmap.
- **G4**: every change set needs its own approval. Sensitive changes always need the full proposal (what, affected resources, risks, rollback, validation), whoever executes them: code, redirects, robots/sitemaps, removals, disavow, analytics configuration, bulk operations.
- **G5**: a change counts as done only with QA evidence. `implemented` ≠ `validated`.

The skill never invents metrics, never promises rankings, follows Google's spam policies, and doesn't give legal advice.

## Capabilities

- **Five domains:** on-page, off-page, technical (including JavaScript and Next.js rendering), local (Google Business Profile, NAP, multi-location), and analytics.
- **Two lenses:** Arabic, RTL and multilingual SEO (Egypt, Saudi Arabia, the Gulf); AI-search visibility.
- **A transparent priority model:** `(2×Impact + Urgency + Business relevance) × Confidence ÷ Effort`, with a P0 override.
- **Five standard-library Python scripts:**
  - `site_check.py`: a public crawl check.
  - `prioritize_findings.py`: validates and scores findings.
  - `gsc_compare.py`: compares Search Console periods.
  - `nap_check.py`: NAP consistency.
  - `arabic_keywords.py`: Arabic keyword normalization.
- **18 templates** for every deliverable.

## Integrations

The skill works with Google Search Console, GA4, Google Business Profile, Bing Webmaster Tools, PageSpeed Insights / Lighthouse / CrUX, Ahrefs, Semrush and Screaming Frog.

**None of these are connected by default.** Data comes from exports you provide, from a connector you configure with your own credentials, or from public checks. The skill checks what's actually available before relying on it, and never asks for passwords. See `references/tools-and-integrations.md`.

## Installation and use

1. Place this folder at `~/.claude/skills/seo-growth-engineer/`, your personal Claude Code skills directory.
2. Start Claude Code and invoke `/seo-growth-engineer`, or describe an SEO task. The skill also triggers on natural requests such as an SEO audit, indexing problems, local SEO, or an SEO report, in Arabic or English.
3. The scripts need Python 3.9 or newer and no extra packages. Run any of them with `--help` for usage.

## Documentation

- [`HANDOVER.md`](HANDOVER.md): full documentation (structure, modes, tool connections, limitations, test history).
- [`SKILL.md`](SKILL.md): the orchestrator Claude loads.
- [`CHANGELOG.md`](CHANGELOG.md): release history (1.0.0 → 1.1.0).

## License

No license is granted. This is a private repository; all rights reserved.
