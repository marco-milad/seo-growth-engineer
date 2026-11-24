# Industry Adaptations

The workflow in SKILL.md is the same for every project. What changes by business model is what you ask, which modules get depth, which findings tend to matter most, and which KPIs prove progress. Read the section for this business at Stage 1 (it shapes the discovery questions and module selection) and again at Stage 5 (strategy). Many businesses span two sections (a multi-branch clinic = healthcare + multi-location); combine them.

Labels: **(Official)** = Google documentation, **(Practice)** = common professional practice / field observation, **(Verify)** = check the live documentation at time of use.

## Contents

1. [E-commerce](#1-e-commerce)
2. [Healthcare and other YMYL](#2-healthcare-and-other-ymyl)
3. [SaaS](#3-saas)
4. [Education](#4-education)
5. [Local businesses](#5-local-businesses)
6. [Multi-location brands](#6-multi-location-brands)
7. [Corporate and B2B lead generation](#7-corporate-and-b2b-lead-generation)
8. [Content and media publishers](#8-content-and-media-publishers)
9. [Cross-industry pitfalls](#9-cross-industry-pitfalls)

---

## 1. E-commerce

**Discovery additions**
- Platform (Shopify, WooCommerce, Salla/Zid, custom Next.js…), catalogue size, how often products change, and whether variants have their own URLs.
- Top categories and products by revenue and margin. These define "business relevance" in the priority model.
- Out-of-stock and discontinued policy; seasonal ranges.
- Is a Merchant Center account linked? Product feed source?
- Payment, shipping, and returns facts (they belong in structured data and on-page). Never invent them.
- Whether brands sold are authorized, and whether product copy comes from suppliers (duplicate-content risk).

**Module emphasis:** Technical (faceted navigation, duplication, crawl efficiency on large catalogues, rendering of price/stock), On-page (category pages as the main ranking assets, unique product copy), structured data, Analytics (revenue attribution). Local only if there are stores or pickup points.

**Typical high-impact findings**
- Category pages with no unique copy, weak titles, or targeting the wrong term (category pages usually rank for the head commercial terms, so they're often the biggest lever).
- Faceted URLs crawlable and indexable at scale, creating near-duplicates (technical-seo.md section 15).
- Product copy copied from suppliers or shared across dozens of variants and products.
- Variant URL handling: the same product under several paths, or variants as separate thin pages.
- Out-of-stock products returning 404 or redirecting to the homepage, when they should stay live with availability shown (temporary stock-out) or 301 to the closest replacement or category (permanently discontinued, when there's a real equivalent). Use 404/410 when nothing equivalent exists.
- Structured data mismatches: price, availability, or shipping values that differ from the visible page.

**Structured data (Official)**
- `Product` with `Offer` for product snippets; merchant listing properties (price, availability, shipping details, return policy) for merchant listing experiences (Source: Merchant listing structured data, https://developers.google.com/search/docs/appearance/structured-data/merchant-listing, checked 2026-11-24).
- **Variants:** `ProductGroup` with `hasVariant`, `variesBy`, and `productGroupID`; each variant is a `Product`, ideally with a distinct URL (e.g. `?variant=` or `?color=`) that preselects it (Source: Product variant structured data, https://developers.google.com/search/docs/appearance/structured-data/product-variants, checked 2026-11-24).
- Shipping and return policy can also be set at the Organization level or in Merchant Center (Verify the current recommended placement).
- Review stars only from genuine product reviews collected on the site, never self-serving or imported fakes.

**Merchant Center (Practice + Official):** free listings and Shopping surfaces use the product feed. Feed and on-page data must match. It's often a fast visibility win for e-commerce, but setting it up touches the client's Google accounts, so it needs G4.

**KPIs:** organic revenue and transactions (GA4), organic clicks and impressions for category and product page groups (GSC), indexed product/category coverage, merchant listing impressions (GSC Shopping/merchant reports if available), conversion rate of organic landing pages.

**Pitfalls:** sale/campaign URLs created and deleted every season (link equity lost each time); internal search result pages indexed; pagination with JS-only "load more"; brand-name collisions when the store name is generic; inventing product attributes (materials, origin) to fill copy.

## 2. Healthcare and other YMYL

YMYL ("Your Money or Your Life") topics, such as health, finance, legal, and safety, are where Google's systems put extra weight on reliability. This includes business-adjacent content such as payroll, tax, insurance, HR and labour-law guidance on SaaS or B2B sites. Apply the same evidence bar (named expert reviewer, sources, dates) to those pages, even when the rest of the site isn't YMYL.

**Healthcare listings:** besides each branch's Google profile, inventory practitioner profiles (see local-seo.md section 11) and third-party medical booking/directory platforms. Those often rank for "doctor/clinic + area" queries and carry their own NAP, hours, reviews and booking links. The Search Quality Rater Guidelines describe E-E-A-T (experience, expertise, authoritativeness, trust), with trust as the most important part. E-E-A-T is a framework raters use to evaluate results, not a single ranking factor or a score to optimize (Official: Google, Creating helpful, reliable, people-first content, https://developers.google.com/search/docs/fundamentals/creating-helpful-content, checked 2026-11-24).

**Discovery additions**
- Practitioners: names, specialties, credentials, licences, and which branches they work at.
- Who medically reviews content, and how often. Is there a review date policy?
- Regulatory limits on advertising and claims in the target country (e.g. medical advertising rules from health authorities). Ask the client; don't assert local law.
- Booking flow (phone, WhatsApp, online booking system) and what counts as a conversion.
- Patient privacy constraints for reviews, testimonials, and case photos.

**Module emphasis:** Content trust (CNT), On-page (service and condition pages), Local (branches, practitioner profiles), Technical (booking widget rendering), Analytics (appointment conversion tracking without capturing health data).

**Typical high-impact findings**
- Service and condition pages with no author or reviewer, no credentials, no sources, and no review date.
- Thin or copied medical content, or AI-generated health text that no clinician has reviewed (both a trust and a safety issue).
- Doctor/practitioner pages missing, or not linked from the services they provide.
- Branch pages missing or duplicated; GBP practitioner/department listings unmanaged.
- Claims that cannot be substantiated (guaranteed results, "best doctor").
- Review replies that confirm someone's patient status (privacy risk). Every reply needs explicit approval and careful wording. The owner usually posts it from your draft, which is the owner-executed path. The full G4 proposal applies if you post it yourself (SKILL.md, Approval gates).

**Recommendations (Practice):** an author and medical-reviewer byline linked to practitioner profile pages; a visible "last medically reviewed" date; citations to recognized medical sources; clear separation of informational content from booking CTAs; `Physician`/`MedicalClinic`/`Hospital` subtypes of LocalBusiness where accurate, kept consistent with GBP. Don't chase rich results that don't exist for this vertical (FAQ rich results are no longer shown for any site since May 2026; see technical-seo.md section 14).

**KPIs:** appointment requests (form, call, WhatsApp) from organic and GBP; organic clicks to service pages by branch; GBP calls and direction requests per branch; review rating and velocity per branch.

**Pitfalls:** tracking setups that send health information to analytics (likely conflicts with analytics-provider policies and possible privacy-law exposure: flag it and escalate to the owner and qualified counsel, don't judge legality); copying competitors' medical content; mass "condition + city" pages (doorway risk); promising outcomes in copy.

## 3. SaaS

**Discovery additions**
- Product category, and whether buyers search for it yet (an established category vs a new one).
- ICP (ideal customer profile) and buying committee; self-serve vs sales-led; trial/demo/sign-up as the conversion.
- Competitors and alternatives buyers compare against.
- Integrations, use cases, industries served, and documentation (docs are often the largest indexable asset).
- Markets and languages; pricing page policy.

**Module emphasis:** Content strategy (bottom-of-funnel first), On-page, Technical (JS-heavy marketing sites, docs subdomains, app vs marketing separation), Off-page (digital PR, integration partners, reviews platforms), Analytics (sign-up attribution, assisted conversions).

**Page types that typically matter (Practice):** feature pages, solution/use-case pages, industry pages, integration pages (one per real integration), comparison and "alternative to X" pages (fair and factual), pricing, templates/tools, documentation, and educational content that targets the problems the product solves.

**Typical high-impact findings**
- The marketing site is client-rendered (SPA), so metadata and copy are missing from the initial HTML.
- App routes, login pages, or staging environments are indexable; docs live on a separate subdomain with poor linking to product pages.
- Content targets top-of-funnel vanity topics while no comparison or use-case pages exist.
- Programmatic pages (integrations × use cases × industries) with templated thin content. That's a scaled-content risk (Official spam policy: scaled content abuse, https://developers.google.com/search/docs/essentials/spam-policies, checked 2026-11-24). Programmatic pages are acceptable only when each page has genuinely unique, useful data.
- No tracking of sign-ups/demos by organic landing page.

**KPIs:** organic sign-ups/trials/demo requests, by landing page group; non-brand organic clicks to BOFU pages; branded search growth (a proxy for awareness); docs traffic assisting conversions.

**Pitfalls:** disparaging or inaccurate competitor comparisons (legal risk, and they must be factual and dated); gating all content; publishing at volume with no subject-matter input.

## 4. Education

**Discovery additions**
- Institution type (university, school, training center, online course platform); accreditation and licences.
- Programs and courses, intakes and admission cycles, delivery mode (on campus / online), campuses.
- The decision maker (student, parent, employer) and the language each searches in.
- Conversion: application, inquiry, enrollment, course purchase.

**Module emphasis:** On-page (program/course pages), Content (admissions questions, careers, comparisons), Local (campuses, training centers), Technical (course catalogue structure, faceting by subject/level/location), seasonality-aware Analytics.

**Structured data (Official):** the **Course list** rich result (a carousel; needs at least three courses on a summary page) is still supported. **Course info** markup was phased out in 2025 (Sources: Course list structured data, https://developers.google.com/search/docs/appearance/structured-data/course; Simplifying the search results page, https://developers.google.com/search/blog/2025/06/simplifying-search-results, checked 2026-11-24). Other relevant types: `EducationalOrganization`/`CollegeOrUniversity`, `Event` for open days, `JobPosting` for staff vacancies (not for courses). Verify current support before implementing.

**Typical high-impact findings:** program pages missing fees, duration, entry requirements, intake dates, or accreditation (the facts searchers want); outdated intake dates; one generic page for many programs; PDF-only brochures holding the key information; campus pages missing or not linked to GBP.

**KPIs:** inquiries and applications from organic by program; organic clicks to program pages; seasonality-adjusted comparisons (intake cycles dominate demand; compare year over year).

**Pitfalls:** guarantees about employment or admission outcomes; claiming accreditation the institution doesn't hold; deleting last year's program pages (update them in place to keep their history and links).

## 5. Local businesses

Single-location service businesses: clinics, restaurants, salons, workshops, trades, law offices, shops.

**Discovery additions:** the exact services offered and the area served (storefront vs service-area business), opening hours including seasonal hours, GBP ownership and status, how customers actually contact them (calls, WhatsApp, walk-in), and the main local competitors on Maps.

**No website?** Many small businesses (bakeries, salons, workshops) run on a Maps listing plus social pages and, for food, delivery apps. Run the Focused local path from SKILL.md's module table. Include delivery-app and social listings in the NAP inventory.

**Module emphasis:** Local (dominant; see local-seo.md), On-page (one strong page per core service, plus a contact/location page), Technical at a basic level (small sites need a clean, fast, mobile site, not a deep crawl audit), light Off-page (local citations, associations, local press, suppliers), and Analytics (calls, WhatsApp, direction requests).

**Typical high-impact findings:** an unclaimed, unverified, or duplicated GBP; wrong primary category; the website not linked from the GBP, or the GBP linking to a dead site; NAP mismatches; one "services" page covering everything; no review routine; no call/WhatsApp tracking.

**KPIs:** GBP calls, direction requests, website clicks; organic leads; review count and rating; local pack visibility (only if a grid tracker is available).

**Pitfalls:** overselling technical work to a 10-page site; city pages for areas not served (doorway); keyword-stuffed GBP names copied from competitors (suspension risk).

## 6. Multi-location brands

Combine with the vertical section (retail, healthcare, education…).

**Discovery additions:** number of locations and planned openings/closures; who owns the GBP organization account; existing store codes; whether a store locator exists and how location data is maintained (CMS, spreadsheet, a franchise system); franchise vs corporate ownership (who is allowed to edit what).

**Module emphasis:** Local governance first (local-seo.md section 11: location data master, ownership, duplicates), then location page templates, then per-location optimization. Technical: locator crawlability, location page indexability, consistent LocalBusiness schema. Analytics: centralized reporting with per-location breakdowns.

**Typical high-impact findings:** listings outside the brand's account (user-created, franchisee-created, old agency); inconsistent names and categories across locations; location pages missing or generated as thin duplicates; the locator rendered only by a JS map with no crawlable links; GBPs linking to the homepage; no single source of truth for hours (especially special hours).

**KPIs:** per-location GBP actions and organic leads, aggregated in a central dashboard; profile health score (completeness, accuracy) across the estate; percentage of locations with a verified, correctly owned profile.

**Pitfalls:** mass-editing many profiles at once (one mistake replicates everywhere; work one location first, then checkpoint); bulk verification started without the owner; duplicate location content at scale.

## 7. Corporate and B2B lead generation

**Discovery additions:** services and the industries served; sales cycle length and deal size; what a qualified lead is (and how leads are tracked into the CRM); case studies and proof the client can actually publish; markets and languages (often Arabic + English for Gulf B2B).

**Module emphasis:** On-page and information architecture (service × industry pages), Content (expertise content, case studies, insights), Off-page (digital PR, associations, partners, events, speaking), Technical (often a brochure site with basic issues), Analytics (form, call, and email lead tracking; offline conversion import if CRM data exists).

**Typical high-impact findings:** one "Services" page listing everything with no dedicated page per service; no industry pages; no case studies, or case studies hidden in PDFs; generic stock content with no expertise signals; lead forms not tracked; thin "About" and "Team" pages (trust); the Arabic version missing or a weak translation for Gulf buyers.

**KPIs:** qualified leads from organic (by service line); organic clicks to service and industry pages; branded search growth; assisted conversions; pipeline influenced (only where CRM data is shared).

**Pitfalls:** chasing high-volume informational keywords unrelated to what the firm sells; publishing client names or results without permission; projecting lead numbers.

## 8. Content and media publishers

**Discovery additions:** publishing volume and topics; editorial policies and corrections; author roster; monetization (ads, subscriptions, affiliate); Google News / Discover reliance; paywall model; syndication arrangements.

**Module emphasis:** Technical (crawl efficiency, pagination, archives, Core Web Vitals with ad load, article structured data, paywall markup), Content quality and E-E-A-T (authorship, sourcing, original reporting), Analytics (Discover and News traffic, which GSC reports separately when present).

**Official notes**
- `Article`/`NewsArticle` structured data helps Google understand title, images, dates, and authors (author `name` and `url` to an author page). It's not required for Top stories (Source: Article structured data, https://developers.google.com/search/docs/appearance/structured-data/article, checked 2026-11-24; Verify current wording).
- Google News inclusion is automatic based on content; the Publisher Center manages publication settings. Eligibility follows Google News policies (Verify current policies).
- Paywalled content: use the paywall structured data (`isAccessibleForFree`, `hasPart` with `cssSelector`) so serving full content to Googlebot isn't treated as cloaking.
- **Site reputation abuse:** hosting third-party content (coupons, casino, payday loans, unrelated affiliate sections) to exploit the host site's ranking signals violates spam policy, regardless of first-party involvement (Source: Spam policies, https://developers.google.com/search/docs/essentials/spam-policies; Updating our site reputation abuse policy, https://developers.google.com/search/blog/2024/11/site-reputation-abuse, checked 2026-11-24). Google announced in 2026 that manual actions under this policy apply differently for users in the EEA from 30 August 2026; elsewhere enforcement is unchanged (Source: Update to the Site Reputation Policy, https://developers.google.com/search/blog/2026/08/update-site-reputation-policy, checked 2026-11-24).

**Typical high-impact findings:** no author pages or bylines; thin tag/archive pages indexed at scale; dates that change without real updates ("freshness" manipulation); ad-heavy layouts failing CLS/INP; syndicated copies outranking the original (needs canonical agreements with syndication partners); AI-written articles at scale without editorial review.

**KPIs:** organic and Discover clicks; articles indexed within X hours of publication (from logs/GSC); returning readers; subscription or ad revenue from organic.

**Pitfalls:** rewriting competitor stories without adding reporting; republishing old articles with new dates; sponsored content without `rel="sponsored"` links or disclosure.

## 9. Cross-industry pitfalls

- **Treating every industry the same.** A checklist that recommends GBP to a SaaS company, or crawl-budget work to a 15-page clinic site, signals that the work isn't specific to the project.
- **Recommending retired features** (FAQ/HowTo rich results, the sitelinks search box, Course info, GBP chat, business.site websites). Check technical-seo.md section 14 and local-seo.md section 6.
- **Programmatic or AI-scaled pages** with no unique value, in any industry. Scaled content abuse applies whether the content is produced by AI, humans, or both.
- **Facts not confirmed by the business.** Prices, credentials, materials, policies, service areas: when they're unknown, ask, don't fill the gap with something plausible.
- **Mixing first-party and tool data.** Keep GSC/GA4 numbers apart from Ahrefs/Semrush estimates (SKILL.md evidence standard).
