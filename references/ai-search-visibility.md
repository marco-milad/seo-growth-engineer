# AI-Search Visibility (AI Overviews, AI Mode, LLM assistants)

Load this when the user asks about AI Overviews, AI Mode, ChatGPT/Perplexity/Copilot/Gemini/Claude visibility, "GEO"/"AEO"/"LLM SEO", AI crawlers, or `llms.txt`. Also load it when an audit touches robots.txt rules for AI bots, or when reporting on AI-feature traffic. Findings use the `AIS-` prefix (SKILL.md).

This area changes quickly and attracts many unverified claims. Every statement below is labelled:
- **[Official]**: from the platform's own documentation.
- **[Third-party]**: industry research or reporting.
- **[Hypothesis]**: plausible but unproven.

Re-verify the official docs at time of use. Most of these were checked 2026-11-24.

Contents:
1. What the platforms officially say
2. Crawler and control matrix
3. Audit procedure
4. Strategy: what actually helps
5. Measurement, honestly
6. Typical findings
7. Myths and risky advice

---

## 1. What the platforms officially say

### Google (AI Overviews, AI Mode)
- **[Official]** To appear as a supporting link in AI Overviews or AI Mode, a page must be indexed and eligible to show in Google Search with a snippet. **There are no additional technical requirements** (Source: AI features and your website, https://developers.google.com/search/docs/appearance/ai-features, checked 2026-11-24).
- **[Official]** You don't need `llms.txt`, "AI text files", special markup, or content chunking for Google's AI features. Google Search ignores machine-readable AI files: they neither help nor hurt (same source; also Optimizing your website for generative AI features on Google Search, https://developers.google.com/search/docs/fundamentals/ai-optimization-guide, checked 2026-11-24).
- **[Official]** The emphasis is standard SEO plus **non-commodity, people-first content**: content with first-hand experience, original information, and clear expertise. The guide advises against chasing tactics such as AI-specific rewrites (same guide; read it for the full list of "what you don't need").
- **[Official]** Controls:
  - The snippet directives `nosnippet`, `data-nosnippet`, `max-snippet`, and `noindex` limit what can be shown, including in AI features.
  - Search Console has a property-level **Search generative AI control** (Settings → Search generative AI). It manages a site's inclusion in Google's generative AI features: **AI Overviews**, **AI Mode**, and **Generative AI features in Google Discover**, as one control (Source: Search generative AI control, Search Console Help, https://support.google.com/webmasters/answer/16908024, checked 2026-11-24).
  - **Google-Extended** (a robots.txt product token) controls use of content for Gemini model training and grounding in Gemini Apps/Vertex AI. It **does not affect inclusion or ranking in Google Search** (Source: Google's common crawlers, https://developers.google.com/crawling/docs/crawlers-fetchers/google-common-crawlers, checked 2026-11-24).
  - Googlebot rules are the control for Search, including its AI features.
- **[Official]** Details of the Search generative AI control (Source: Search Console Help, https://support.google.com/webmasters/answer/16908024, checked 2026-11-24):
  - **Options:**
    - "Include my site's links and content in Search generative AI features" is the default for all properties.
    - "Exclude my site's links and content from Search generative AI features".
    - "Inherit control from parent" is the default when the property has a parent property.
  - **Effect on the rest of Search:** Google says the control "isn't used as a ranking or inclusion signal affecting other parts of Search", and it doesn't affect AI training (Google-Extended governs that).
  - **Rollout:** Google's blog announced it on 3 June 2026 as a test with "a subset of website owners in the UK". An update dated 31 August 2026 says it reached all websites worldwide (Source: New opportunities, control and insights for website owners, Google blog, https://blog.google/products-and-platforms/products/search/new-opportunities-control-and-insights-for-website-owners/, published 2026-06-03, updated 2026-08-31, checked 2026-11-24). The Help page itself confirms the worldwide date: "As of August 31, 2026, we've rolled out this control to all websites worldwide."
- **[Official]** In an October 2026 post, Google said it plans to honor a shared, AIPREF-based AI-training preference signal, treating an opt-out there like a Google-Extended disallow when Google-Extended isn't named (Source: Supporting a shared AI training control for websites, https://developers.google.com/search/blog/2026/10/ai-training-control, checked 2026-11-24). Check its implementation status at time of use.
- **[Official]** Preferred sources can appear in AI Mode and AI Overviews only if the site is included via the Search generative AI control (Source: Preferred sources guide, https://developers.google.com/search/docs/appearance/preferred-sources, checked 2026-11-24).

### Microsoft (Bing, Copilot)
- **[Official]** Bing Webmaster Tools has an **AI Performance** report, launched in public preview in February 2026 and expanded in 2026. It covers how a site is cited in Microsoft Copilot, Bing AI summaries, and some partner integrations: citations, cited pages, grounding queries, and later intents/topics/citation share (Source: Bing Webmaster Blog, https://blogs.bing.com/webmaster/February-2026/Introducing-AI-Performance-in-Bing-Webmaster-Tools-Public-Preview, and https://blogs.bing.com/search/June-2026/New-AI-Visibility-Insights-in-Bing-Webmaster-Tools-Intents-Topics-Citation-Share-Compare, checked 2026-11-24).
- **[Third-party]** It reportedly shows citations but not clicks. Verify in the tool.
- Bing indexing supports IndexNow, which matters because Bing feeds Copilot.

### OpenAI (ChatGPT search)
- **[Official]** Three separate user agents (Source: Overview of OpenAI crawlers, https://developers.openai.com/api/docs/bots, checked 2026-11-24):
  - `OAI-SearchBot`: search. Sites that disallow it won't appear in ChatGPT search answers, though they may still appear as navigational links.
  - `GPTBot`: training. Disallowing it signals that content shouldn't be used for training foundation models. It's independent of search.
  - `ChatGPT-User`: user-initiated fetches. robots.txt may not apply, and it isn't used to decide search inclusion.
- **[Official]** robots.txt changes for search can take about 24 hours to take effect. To keep a page from being surfaced as a link and title, use `noindex`, and the crawler must be allowed to read it (OpenAI publishers FAQ, https://help.openai.com/en/articles/12627856, checked 2026-11-24).

### Anthropic (Claude)
- **[Official]** Three bots, each controlled separately in robots.txt (Source: Anthropic crawler documentation, https://support.claude.com/en/articles/8896518, checked 2026-11-24):
  - `ClaudeBot`: training data.
  - `Claude-SearchBot`: indexing to improve Claude's search results.
  - `Claude-User`: fetches when a user's question needs a page.
  
  Anthropic supports the non-standard `Crawl-delay` directive.

### Perplexity
- **[Official]** `PerplexityBot` is for search discovery and is controllable via robots.txt. `Perplexity-User` fetches on a user's request and, according to Perplexity's docs, generally ignores robots.txt (Source: Perplexity crawlers docs, https://docs.perplexity.ai/guides/perplexitybot, checked 2026-11-24).
- **[Third-party]** Cloudflare (2025) reported undeclared crawling by Perplexity. The compliance record is disputed.

### llms.txt
- **[Official]** Google does not use it (see above).
- **[Third-party]** Large crawl studies in 2026 found most published `llms.txt` files receive no AI-bot requests at all (e.g. Ahrefs, https://ahrefs.com/blog/llmstxt-study/, checked 2026-11-24).
- No major AI search provider has documented using it for retrieval or ranking.
- **Position for this skill:** optional and low-cost. Fine if the client wants it, especially for developer documentation, where coding tools may read it. Never present it as a visibility lever, and never prioritize it above real issues.

## 2. Crawler and control matrix

| Goal | Control | Effect on Google Search |
|---|---|---|
| Stay out of Google AI Overviews/AI Mode but keep normal results | The Search Console **Search generative AI control** (the "Exclude" option); or `nosnippet`/`max-snippet`/`data-nosnippet` (these also limit normal snippets) | Google says the control "isn't used as a ranking or inclusion signal affecting other parts of Search" (Search Console Help). Snippet directives reduce normal snippets too |
| Opt out of Gemini training/grounding | `User-agent: Google-Extended` / `Disallow: /` | None on Search |
| Stay out of ChatGPT search | Disallow `OAI-SearchBot` | — |
| Opt out of OpenAI training but stay in ChatGPT search | Disallow `GPTBot`, allow `OAI-SearchBot` | — |
| Opt out of Claude training but stay in Claude search | Disallow `ClaudeBot`, allow `Claude-SearchBot` (and `Claude-User`) | — |
| Stay out of Perplexity search | Disallow `PerplexityBot` (user-triggered fetches may still occur) | — |

**Blocking training bots and blocking search bots are different decisions.** Many sites unknowingly block search/retrieval bots by copying "block all AI" lists. Any robots.txt change is a production change, so it needs G4. The AI-crawler policy is a **business decision**: present the trade-offs (visibility and citations vs content reuse) and let the client choose. Don't default either way.

Also check the layers beyond robots.txt. CDNs/WAFs (e.g. Cloudflare's AI-bot blocking settings) can block AI crawlers regardless of robots.txt. Ask who manages the CDN, and look for 403s to those user agents in server logs if logs are available.

## 3. Audit procedure

1. **Foundation first.** AI features in Google draw on the regular index. Indexability, snippet eligibility, and content quality issues from the main audit are the first AI-visibility issues too. Don't create separate AIS findings for things already covered by TEC/ONP findings; cross-reference them.
2. **Robots.txt and directives.** List the rules for Googlebot, Google-Extended, Bingbot, OAI-SearchBot, GPTBot, ChatGPT-User, ClaudeBot, Claude-SearchBot, Claude-User, PerplexityBot, and any blanket `User-agent: *` blocks. Check page-level `nosnippet`/`max-snippet`/`data-nosnippet` (via `scripts/site_check.py`, which reports robots meta and X-Robots-Tag). Compare with the client's intended policy. A mismatch is a **Confirmed issue** if it's contrary to the stated intent; otherwise a **Potential issue**, with `dependencies: client decision: AI-crawler policy` (a pending decision is never a bucket; seo-audit-framework.md §7).
3. **CDN/WAF bot settings.** **Missing data** unless the client shares them or logs show blocking.
4. **Search Console.** If available, check the state of the Search generative AI control (Settings → Search generative AI; include, exclude, or inherit), and whether the Generative AI performance report shows data. **[Official, checked 2026-11-24]** The report shows impressions only (by page, country, device, date) for AI Overviews and AI Mode, and was rolled out to all sites by 2026-08-31 (Source: https://support.google.com/webmasters/answer/16984139). **[Third-party/verify]** It may appear only once a site has enough impressions. Clicks from AI features are counted inside the normal Performance report (Web search type) and can't be isolated there.
5. **Bing Webmaster Tools AI Performance**, if the site is verified.
6. **Entity consistency.** Is the business described consistently (name, what it does, where, key facts) across the site, Organization structured data with `sameAs` to official profiles, GBP, and major profiles/directories? Inconsistency confuses both search engines and assistants. **[Hypothesis]**: consistency helps assistants describe the business accurately. It's low-cost and good hygiene regardless.
7. **Content suitability.** Do key pages state clear, specific, verifiable answers (prices or ranges, policies, specs, service areas, credentials) that an assistant could cite? Is there non-commodity content (data, first-hand guides)?
8. **Prompt sampling (indicator only).** See section 5.

## 4. Strategy: what actually helps

Ordered by the strength of evidence:
1. **[Official]** Be indexable and snippet-eligible; fix the technical and on-page issues.
2. **[Official]** Create non-commodity, people-first content with real expertise and first-hand information. Make key facts explicit and consistent.
3. **[Official]** Structured data that matches visible content, for the features Google supports (technical-seo.md). It helps machines understand pages. Google says no special "AI schema" is needed.
4. **[Official/Third-party]** Get indexed on Bing too (Copilot; possibly other assistants). Use IndexNow where supported.
5. **[Hypothesis, widely held]** Brand mentions and presence on the reputable sites, communities, and review platforms that assistants cite help the brand get named. Build them legitimately (off-page-seo.md). Never with spam or fake reviews.
6. **[Business decision]** Set the AI-crawler policy deliberately (section 2).

Do not sell "GEO packages" that promise citations. Nobody controls inclusion in AI answers.

## 5. Measurement, honestly

| Source | What it shows | Label |
|---|---|---|
| GSC Performance report (Web) | Clicks/impressions including AI Overviews and AI Mode, not separable | First-party, aggregated |
| GSC Generative AI performance report (where available) | AI feature impressions by page/country/date/device (impressions only as of 2026-11-24) | First-party; Google may add metrics, re-check at time of use |
| Bing WMT AI Performance | Copilot/Bing AI citations, grounding queries | First-party (Microsoft surfaces only) |
| GA4 referrals | Sessions from assistant domains, e.g. `chatgpt.com`, `perplexity.ai`, `copilot.microsoft.com`, `gemini.google.com`, `claude.ai` (some assistants add `utm_source`, which is observed behaviour that can change) | First-party but undercounted (many AI visits arrive without a referrer) |
| Server logs | Bot fetches by user agent (verify IPs against the published ranges) | First-party, if logs are available |
| Prompt sampling | Whether the brand is mentioned/cited for a fixed set of prompts | **Indicator only.** Answers vary by run, user, location, and model version |

**Prompt sampling method.** Write a fixed set of 10–30 realistic prompts per market and language, covering category, comparison, local, and brand queries. Run each prompt several times per engine, logged-out or in a clean profile, and record the date, engine, model or version if shown, language, location, whether the brand appeared, and which URLs were cited. Report rates ("mentioned in 4 of 12 runs"), never "ranks #1 in ChatGPT". Re-run the same set at the same cadence to compare. Third-party "AI visibility" tools are estimates. Label them so.

## 6. Typical findings

| Example | Prefix | Bucket |
|---|---|---|
| robots.txt blocks `OAI-SearchBot`/`Claude-SearchBot`/`PerplexityBot` though the client wants AI visibility | AIS | Confirmed issue |
| Blanket "block AI bots" list copied from a template; no policy decided | AIS | Potential issue (dependencies: client decision: AI-crawler policy) |
| Key facts (prices, hours, service area) inconsistent across site, GBP, and profiles | AIS/LOC | Confirmed |
| Site not verified in Bing Webmaster Tools; no IndexNow | AIS/TEC | Opportunity |
| Brand not mentioned for any sampled category prompt | AIS | Opportunity (indicator, Low/Medium confidence) |
| No way to see AI-feature data (no GSC access) | ANL | Missing data |

## 7. Myths and risky advice

- "You need llms.txt to appear in AI answers": not for Google (official), and unproven elsewhere.
- "Chunk your content into short passages for AI": Google says this isn't needed.
- "Special AI schema or AI-only pages": not needed, and AI-only cloaked pages risk cloaking violations.
- "Blocking Google-Extended removes you from AI Overviews": no. Google-Extended doesn't control Search features.
- "Blocking GPTBot removes you from ChatGPT search": no. That's `OAI-SearchBot`.
- "Guaranteed AI citations": no one can promise this.
- Fake reviews, mass-generated "best X" listicles naming the client, or planting comments in communities: spam, reputational risk, and against platform rules.
- For Arabic markets, sample prompts in the language variants customers actually use (MSA, dialect, English, mixed). Assistant behaviour differs by language. See arabic-and-multilingual-seo.md.
