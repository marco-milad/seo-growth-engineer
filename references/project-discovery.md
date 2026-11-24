# Stage 1: Project Discovery and Business Understanding

Discovery exists because SEO advice is only as good as its fit to the business. "Add more blog posts" is useless to a clinic whose patients book by phone from Google Maps. "Build backlinks" is premature for a store whose product pages return `noindex`. The goal of Stage 1 is a short, confirmed picture of the business, its goals, and its site, so that every later finding can be judged by "does this matter to *them*?".

Output: `01-discovery.md` (from `templates/project-discovery-template.md`). Exit: **G1**, where the user confirms the summary.

## Contents

1. Principles
2. Infer before you ask
3. The conversation: how to run it
4. Question bank by tier
5. Variants by business model
6. Arabic phrasing for key questions
7. Module selection reasoning
8. Recording answers
9. G1 confirmation summary
10. Common discovery mistakes

## 1. Principles

- **Business first, website second.** Ask what the business sells and how it makes money before asking about the CMS.
- **One essential question at a time.** Ask the question whose answer changes what you do next, and offer a recommended default so the user can answer with a single word. Batch only trivial facts the user can answer together (e.g. "website URL and the main country you sell in?").
- **Never ask what you can find out.** The codebase, the live site, and existing files answer many questions. Asking them anyway wastes the user's time and signals you haven't looked.
- **Unknown is a valid answer.** "I don't know our conversion rate" gets recorded as unknown and becomes a Missing-data item later. It never stalls discovery.
- **Discovery is progressive.** Tier 1 must be known before the audit. Tier 2 can be collected during the audit. Tier 3 is collected when it becomes relevant. Don't front-load all of it.
- **Confirm, don't assume.** Anything you inferred is presented back as "I see X; is that right?", not silently written down as fact.

## 2. Infer before you ask

Spend a few minutes looking before the first question. Record what you found and where (file path or URL), with the date.

### If you are inside the website's codebase

| Look at | Tells you |
|---|---|
| `package.json`, `composer.json`, `Gemfile`, `requirements.txt`, lockfiles | Framework and version (Next.js, Nuxt, Astro, Remix, Angular, Laravel, WordPress theme, Shopify theme…) |
| Next.js: `app/` vs `pages/`, `generateMetadata`, `metadata` exports, `next.config.*`, `middleware.*` | Rendering mode, metadata approach, redirects/rewrites, i18n routing |
| `robots.ts/txt`, `sitemap.ts/xml`, `public/` | Current crawl directives and sitemap generation |
| i18n config (`next-intl`, `i18next`, `[locale]` segments, `dir="rtl"`) | Languages, URL strategy for locales, RTL handling |
| JSON-LD components, `schema` folders | Existing structured data |
| Analytics snippets (gtag, GTM container ID, consent banner) | Whether GA4/GTM is installed (presence only; it isn't proof that tracking works) |
| Routes/folders (`/products`, `/services`, `/blog`, `/locations`) | Page types and site architecture |
| `.env.example` (never `.env` contents) | Which third-party services are expected (names only) |
| README, docs, previous reports in the repo | Business context, previous SEO work |

### If you only have the URL (public look, polite, a handful of requests)

- Homepage: what the business sells, languages offered, phone/WhatsApp/address in the footer (local signal), primary CTA (call, book, buy, sign up).
- `robots.txt` and the sitemap(s): page types, approximate size, platform hints (`/wp-sitemap.xml`, `/sitemap_products_1.xml` for Shopify).
- Response headers and HTML generator meta: platform and CDN.
- One page of each type: product/service/article/location templates.
- `scripts/site_check.py` on a small sample gives status, metadata, canonical, hreflang, and schema in one pass. Raw HTML only: note that JavaScript-rendered content won't appear.

### Existing artifacts

Check the working directory and `seo-engagement/` for previous discovery docs, exports (GSC/GA4/Ahrefs CSVs), audits, and briefs. A previous `PROJECT_STATE.md` means resume, not restart.

Then open the conversation with what you found: "I looked at the site first: Next.js App Router, Arabic and English under `/ar` and `/en`, about 300 URLs in the sitemap, mostly products, and a phone number and Cairo address in the footer. A few questions to fill the gaps."

## 3. The conversation: how to run it

1. **State what you already know** (from section 2), briefly.
2. **Settle the operating mode** in the first two turns (SKILL.md "Start of every engagement", steps 5–6). If the request already names it, confirm it in one line. Otherwise, the first turn's one decision question is either the mode or the single fact the mode recommendation depends on (e.g. "do you have access to the site's code or CMS?").
3. **Ask the most decision-relevant missing Tier 1 question**, with a default. Typically the primary business goal / conversion, or the target market. Quick factual items (country, online-only vs storefront) may ride along on the same turn if they take one line to answer.
4. **Continue Tier 1 one question at a time** until it's covered. Skip anything already answered.
5. **Move to Stage 2** (access and data). Tier 2 questions get asked alongside the audit, when they become relevant ("you have two branches in Giza; do both have Google Business Profiles?").
6. **Write `01-discovery.md` and present the G1 summary.**

Good question shape: *"What's the single action you most want visitors from Google to take: call, WhatsApp, book online, or buy on the site? My guess from the homepage is WhatsApp."*

Bad question shape: a 25-item questionnaire, or an open-ended "tell me about your business" with no anchor.

When the user gives a lot of information at once (e.g. pastes a brief), extract it into the template, then ask only about the gaps.

## 4. Question bank by tier

Use these as a menu, not a script. Skip anything inferred or already answered.

### Tier 1: must know before the audit

| # | Question | Why it matters | Default if unknown |
|---|---|---|---|
| T1.1 | Business name and website URL(s), including other domains or subdomains (shop., blog., old domains) | Scope of the audit; duplicate hosts; migrations | — (required) |
| T1.2 | What do you sell, and to whom? (products/services; B2C/B2B) | Search intent, page types, schema | Inferred from site, confirm |
| T1.3 | What is the main conversion? (purchase, lead form, call, WhatsApp, booking, sign-up, store visit) | Defines Business relevance in prioritization and the KPI tree | Inferred from the primary CTA |
| T1.4 | Which countries/cities do you target, and in which languages? | Local module, hreflang, keyword research market and language | Country of the address/phone + site languages |
| T1.5 | Do customers visit a physical location, or do you serve a defined area? How many locations? | Turns the Local module on/off; multi-location governance | No → Local skipped (confirm) |
| T1.6 | Top 2–3 business goals for the next 6–12 months (e.g. grow online sales of category X, more bookings in branch Y, enter Saudi market) | Strategy focus; which pages matter | "More qualified organic leads/sales"; ask for specifics |
| T1.7 | Operating mode (Audit Only / Strategy & Planning / Execution) | Which stages run; whether G4 changes will happen | Recommend based on the request |
| T1.8 | Known problems or events: traffic drop, migration/redesign, domain change, manual action, hacking, "Google doesn't show us" | P0 candidates; audit focus; timeline annotations | None known |
| T1.9 | Which of these tools do you have, and can you export from them, connect them, or give a team member access? (GSC, GA4, GBP, Ahrefs/Semrush, CMS, repo) | Stage 2 planning (details in tools-and-integrations.md) | Assume none until verified |

### Tier 2: should know before strategy (collect during Stages 2–4)

| # | Question | Why |
|---|---|---|
| T2.1 | Who are your main competitors: in the market, and the ones you see on Google for your key searches? (They may differ) | Competitor analysis; business vs search competitors |
| T2.2 | Who is the customer: personas, what they search for, objections, how they decide | Keyword intent; content strategy |
| T2.3 | Which products/services/categories matter most (margin, strategic priority, stock) | Business relevance scores; keyword-to-page mapping |
| T2.4 | Platform and who controls it: CMS, developer/agency, hosting, deployment process, staging environment | Effort estimates; owner roles; G4 feasibility |
| T2.5 | Previous SEO work: agencies, reports, link building done (and how), disavow file, content programs | Risk (toxic links), avoid repeating failed work |
| T2.6 | Baseline numbers, if the business tracks them: monthly leads/sales, share from organic, average order value, lead value | Business impact estimates (the user's numbers only) |
| T2.7 | Content capacity: who can write or approve content, in which language, how often; subject-matter experts (essential for YMYL) | Realistic content roadmap |
| T2.8 | Seasonality and campaigns (Ramadan, Eid, back to school, White Friday, summer travel) | Period comparisons; content timing |
| T2.9 | Brand assets for off-page: partners, suppliers, associations, press, events, original data | Legitimate link opportunities |
| T2.10 | Constraints: budget class, deadlines, legal/regulatory limits (medical claims, financial promotions), brand rules, words never to use | Feasibility; compliance |

### Tier 3: nice to have (ask when relevant)

- Revenue/lead value per category (for ROI framing). Only if the user offers it; never estimate it for them.
- Customer support FAQs, sales call notes, and on-site search logs: excellent keyword and content sources.
- Offline marketing and brand campaigns that cause branded search spikes.
- Internal stakeholders and approval chain for content and code (who signs off on G4).
- Plans for new markets, products, or a redesign in the next year (migration risk; architecture decisions).
- Reporting preferences: frequency, format, language, audience (owner, marketing manager, board).

## 5. Variants by business model

Swap or add these questions depending on the model. See industry-adaptations.md for how the audit changes.

| Model | Ask additionally |
|---|---|
| E-commerce | Catalogue size and growth; variants (size/colour) and how they're URL'd; out-of-stock and discontinued handling; filters/facets; marketplaces also sold on (Amazon, Noon, Jumia); feeds/Merchant Center; payment and shipping facts (they feed schema and copy) |
| Healthcare | Practitioners and their credentials; who medically reviews content; branches and their services; booking flow; regulatory limits on claims and advertising; insurance accepted |
| SaaS | ICP and buying committee; free trial vs demo; integrations and competitors used in comparisons; docs/help centre location (subdomain?); product-led vs sales-led |
| Education | Programs/courses, intakes and deadlines, accreditation, campuses, admissions funnel, languages of instruction |
| Local service business | Service area (cities/districts), whether customers visit, call or get visited; emergency/after-hours; GBP status and who owns it; review volume and handling |
| Multi-location | Number of locations, which are open/opening/closed; who owns location data (HQ vs branch); per-location phone numbers and pages; GBP account structure and ownership |
| Corporate / B2B | Service lines and industries served; lead qualification; case studies; sales cycle; regional offices |
| Content / media | Monetization (ads, subscriptions, affiliate); editorial team and policies; publishing volume; Google News / Discover reliance |

## 6. Arabic phrasing for key questions

When the user writes in Arabic, ask in Arabic and keep SEO terms in English. Match their dialect register: Egyptian colloquial if they write that way, otherwise Modern Standard Arabic.

- **Main conversion (T1.3):**
  "إيه أهم حاجة عايز الزائر اللي جاي من جوجل يعملها؟ يشتري من الموقع، يكلمك واتساب، يحجز، ولا يزور الفرع؟ من الصفحة الرئيسية شكلها واتساب، صح؟"
  (MSA: "ما الإجراء الأهم الذي تريد أن يقوم به الزائر القادم من جوجل: الشراء، التواصل عبر واتساب، الحجز، أم زيارة الفرع؟")
- **Target market and language (T1.4):**
  "بتستهدف أنهي دول أو مدن؟ والعملاء بيدوروا بالعربي ولا بالإنجليزي ولا الاتنين؟"
- **Operating mode (T1.7):**
  "تحب نبدأ بـ Audit بس (تقرير بالمشاكل والأولويات من غير أي تعديل)، ولا Audit + Strategy و Roadmap، ولا كمان ننفذ التعديلات بنفسنا بعد موافقتك على كل تعديل؟ أنا أنصح نبدأ بـ Audit + Strategy."
- **Known problems (T1.8):**
  "حصل قبل كده أي حاجة ممكن تكون أثرت على ظهوركم في جوجل؟ زي نقل الموقع لدومين جديد، Redesign، نزول مفاجئ في الزيارات، أو رسالة من Google Search Console؟"
- **Physical locations (T1.5):**
  "العملاء بيزوروكم في فرع؟ كام فرع، وكل فرع ليه Google Business Profile؟"

## 7. Module selection reasoning

Apply the "Module selection" table in SKILL.md to the discovery facts and write the reasoning down. For each of the five domains plus the two lenses, record one line:

```text
Local SEO: IN SCOPE. Two branches customers visit (Nasr City, Sheikh Zayed); calls and WhatsApp are the main conversions.
Arabic/multilingual lens: IN SCOPE. Site in AR (default) + EN; customers search in both; hreflang needed.
AI-search lens: LIGHT. Informational queries in this niche show AI Overviews (to verify in Stage 3); no dedicated work until basics are fixed.
Off-page: IN SCOPE, depth medium. New domain, likely few referring domains (to verify).
```

Depth matters as much as in/out. Scale the audit to the site: a 15-page brochure site doesn't get a crawl-budget review, and a 200k-URL catalogue doesn't get page-by-page title rewrites.

Re-open module selection whenever new facts change it (e.g. the user mentions a showroom halfway through the audit).

## 8. Recording answers

Copy `templates/project-discovery-template.md` to `seo-engagement/<slug>/01-discovery.md` and fill it as you go:

- Mark each fact with its **origin**: `user` (stated), `inferred` (with the file/URL), or `unknown`.
- Inferred facts are listed as "to confirm" until the user confirms them at G1.
- Quote the user's own wording for goals and constraints. Don't paraphrase them into marketing language.
- Numbers come only from the user or verified data, with a date. Never fill a baseline with an estimate.
- Record the operating mode and module selection with reasoning.
- Update `PROJECT_STATE.md`: stage = 1, open questions, blockers.

## 9. G1 confirmation summary

Present a short summary the user can confirm in one reply, in the user's language. Keep it under about 15 lines:

```text
Here's my understanding — please correct anything wrong:

Business: [name], [what they sell] to [whom], in [markets]; site in [languages].
Main conversion: [conversion]. Secondary: [x].
Goals (6–12 months): 1) … 2) …
Site: [platform/framework], ~[N] URLs (sitemap, [date]), page types: […].
Known issues: […] / none reported.
Mode: [Audit Only | Strategy & Planning | Execution].
Modules: On-page ✓, Technical ✓ (JS rendering focus), Local ✓ (2 branches), Off-page ✓, Analytics ✓; Arabic lens ✓; AI-search: light.
Still unknown (won't block the audit): [competitors list, baseline revenue…].

Next: Stage 2, checking which data we can actually access (GSC, GA4, GBP…).
Shall I proceed?
```

G1 passes on an explicit confirmation. Record the date in `PROJECT_STATE.md`. If the user corrects something, update `01-discovery.md` first, then continue.

## 10. Common discovery mistakes

- Asking for the platform, languages, or page types when the site or repo already shows them.
- Treating the business's market competitors as their search competitors without checking.
- Turning Local on for a purely online store because it has a registered office address customers never visit. Or turning it off for a service-area business that has no storefront but serves defined cities.
- Writing guessed numbers ("about 5,000 visits a month") into the baseline.
- Skipping known-problem questions. A forgotten migration from last year explains half the audit.
- Starting the audit before the operating mode is clear, then making changes the user didn't expect.
