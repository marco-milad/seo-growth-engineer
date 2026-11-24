# Local SEO

Use this file when discovery shows the business serves customers at a physical location or within a defined service area (see SKILL.md module selection). Purely online businesses skip it; they still keep Organization entity facts consistent. Finding IDs use the `LOC-` prefix. Buckets, confidence, priority, statuses, and gates follow SKILL.md.

## Contents

1. [Safety first: working on live profiles](#1-safety-first-working-on-live-profiles)
2. [How local ranking works (official)](#2-how-local-ranking-works-official)
3. [Eligibility and guidelines](#3-eligibility-and-guidelines)
4. [Google Business Profile audit](#4-google-business-profile-audit)
5. [Reviews and reputation](#5-reviews-and-reputation)
6. [Recent GBP feature changes](#6-recent-gbp-feature-changes)
7. [Local keyword research](#7-local-keyword-research)
8. [Local landing pages vs doorway pages](#8-local-landing-pages-vs-doorway-pages)
9. [Citations and NAP consistency](#9-citations-and-nap-consistency)
10. [LocalBusiness structured data](#10-localbusiness-structured-data)
11. [Multi-location governance](#11-multi-location-governance)
12. [Measurement](#12-measurement)
13. [Market notes: Egypt, Saudi Arabia, Gulf](#13-market-notes-egypt-saudi-arabia-gulf)
14. [Typical findings](#14-typical-findings)

---

## 1. Safety first: working on live profiles

A Business Profile is the business's public identity, and some actions can't be undone (losing ownership, failed re-verification, suspension). The rules below go beyond SKILL.md's gates because the blast radius is large.

- **Read-only by default.** In any logged-in session on a client's Google account, the default is to look and not touch. Every edit, reply, post, photo upload, category change, or hours change needs a G4 proposal approved for *that* change. When the owner makes the change from their own account using your draft, the lighter owner-executed path in SKILL.md applies: the exact draft, where it goes, and a one-line risk.
- **Single listing: check claim status first.** Ask the owner whether the listing appears in their own account (business.google.com / Business Profile Manager). If it doesn't, the owner claims it from the Maps listing ("Own this business?" / claim), and Google chooses the verification method (video verification is common). If someone else already holds it, use the recovery steps in section 11. Steps change, so point to Google Business Profile Help at the time of use. Until the claim status is confirmed, owner statements about the profile are origin "user", Medium confidence.
- **Never** add/remove owners or managers, transfer ownership, request access, start or retry verification, accept "Google updates" suggestions, mark a location closed, or delete a profile without explicit, specific authorization from the user for that exact action. A general "manage the GBP" instruction does not count.
- **Re-take a screenshot before every click.** GBP and Business Profile Manager panels shift after a modal closes, so a click aimed using an older screenshot can land on an edit field or a different button (field observation).
- **Business Profile Manager "Verifications"** can open a bulk-verification wizard. Don't click it while exploring (field observation).
- Prefer **public observation** (Maps and Search as a logged-out user) for audits. Use the account view only for what the public can't see (verification status, managers, Performance data), and only when the user has authorized it.
- **Research browsing never happens in the client-logged-in browser.** Competitor and SERP research uses web fetches or an isolated, logged-out profile (SKILL.md tool protocol).
- Screenshots of the account may show manager emails and other personal data. Store them in `03-audit/evidence/` and redact before anything goes to a client deck.

## 2. How local ranking works (official)

Google says local results are based mainly on **relevance, distance, and prominence** (Source: Google Business Profile Help, Tips to improve your local ranking on Google, https://support.google.com/business/answer/7091, checked 2026-11-24):
- **Relevance**: how well the profile matches the search. Lever: complete, accurate categories, services, products, and description.
- **Distance**: from the searcher's location (or the location named in the query). Not controllable; don't sell tactics that pretend to change it (fake addresses, virtual offices).
- **Prominence**: how well known the business is. Signals include reviews (count and score), links and mentions across the web, and the strength of its organic presence.

Google states you can't pay for better local ranking. Ranking factors beyond these three come from third-party studies (e.g. annual local-search surveys). Label them as third-party opinion, not Google guidance.

Map rankings depend heavily on the searcher's location. Single "rank checks" from one spot are misleading. Use a grid-based local rank tracker if the user has one, or state that rankings vary by location and are being reported at the GBP Performance level instead.

## 3. Eligibility and guidelines

From the Guidelines for representing your business on Google (Source: https://support.google.com/business/answer/3038177, checked 2026-11-24):
- **Eligibility:** the business makes in-person contact with customers during stated hours, at its location or theirs. Online-only businesses aren't eligible.
- **Business name** = the real-world name used consistently on signage, the website, and stationery. Adding keywords, locations, taglines, phone numbers, or hours to the name isn't permitted and can lead to suspension. Keyword-stuffed competitor names can be reported through official channels; never imitate them.
- **Service-area businesses (SABs)** that don't serve customers at their address must hide it and set a service area. Google says that area shouldn't extend beyond roughly two hours' drive from the base. One profile per business with a central location, not one per city served.
- **Address:** a real, staffed location. Virtual offices, PO boxes, and coworking addresses that aren't staffed during business hours aren't allowed.
- **Phone:** a number under the business's direct control, ideally local rather than a call center.
- **Departments/practitioners** (e.g. doctors in a clinic, departments in a hospital or dealership) can have their own profiles under specific rules. Check the current guidelines for the vertical before proposing it.

Any recommendation that edits the name, address, or category can trigger re-verification or a suspension. Flag that risk explicitly in the G4 proposal.

## 4. Google Business Profile audit

Audit **each location separately**, then summarize. Record the source per field (public Maps view vs account view) and the date.

| Area | Check | Typical recommendation |
|---|---|---|
| Existence and duplicates | Search the brand + area on Maps; look for duplicates, unclaimed listings, old addresses, user-created listings | Merge/report duplicates through official channels (G4); claim unclaimed listings via the owner |
| Ownership and access (account view, authorized only) | Who is primary owner; managers; verified status | Owner should be a business-controlled account, not an ex-employee or agency personal account. Changes need owner action plus explicit approval |
| Primary category | Most specific category matching the core business | Change only with evidence (competitor categories, the services the business actually offers). Category changes can trigger re-verification |
| Secondary categories | Relevant, not padded | Add genuinely offered services; remove irrelevant ones |
| Services / products | Filled, specific, with descriptions; products with photos and prices where it fits | Mirror the real service list from discovery; keep in sync with the website |
| Description | ≤ 750 characters, accurate, no URLs or promotional spam | Write from discovery facts only; the user approves the text |
| Hours | Regular, **special hours** (holidays, Ramadan, Eid), more hours (delivery, pickup) | A calendar of special hours for the year |
| Contact | Phone, website URL (with UTM, see section 12), appointment/booking/menu links | Fix broken links and point to the right landing page (location page for multi-location). **No website:** leave the field empty rather than pointing it at an unrelated page. A business's own official social page or ordering/booking page is acceptable if the owner wants it. A website becomes a roadmap *opportunity* when menus, services, booking or trust content can't fit in the profile; it isn't a precondition for local SEO |
| Attributes | Accessibility, payments, amenities, identity attributes where applicable | Fill only true attributes |
| Photos / video | Logo, cover, exterior (helps people find the door), interior, team, products; recency; owner vs customer photos | A photo plan with a real-photo cadence; no stock photos |
| Posts / updates | Recency and usefulness | Optional cadence for offers, events, news; useful but not a ranking lever by itself (third-party view) |
| Reviews | Count, average, recency, response rate and quality, recurring themes | Review request and reply routine (section 5) |
| Maps pin and address | Pin on the actual entrance; address formatted for the local postal format | The owner corrects the pin in the account; for a moved pin, expect possible re-verification |
| Website consistency | NAP and hours match the website location page and schema | One canonical NAP (section 9) |
| Suspension / restrictions | Warnings, "temporarily closed", review restrictions | P0 if the profile is suspended or wrongly marked closed |

**Verification** (official): methods are chosen by Google, not the business. Video verification requires a live, unedited recording from a mobile device of at least 30 seconds, showing the location, proof that the business exists (e.g. permanent signage), and proof of management. Avoid sensitive info and others' faces (Source: Verify your business with a video recording, https://support.google.com/business/answer/14271705, checked 2026-11-24). Brief the owner; never perform verification on their behalf without explicit authorization.

## 5. Reviews and reputation

Policy (Source: Google Business Profile Help, Prohibited & restricted content, https://support.google.com/business/answer/7400114, and Tips to get more reviews, https://support.google.com/business/answer/3474122, checked 2026-11-24):
- **No incentives:** no discounts, gifts, or payment for reviews, or for changing/removing negative ones.
- **No review gating:** don't ask only happy customers, and don't screen customers before sending them to Google. Ask everyone the same way.
- **No fake engagement:** no reviews from staff, family, or bought accounts; no posting from multiple accounts.
- Enforcement can remove reviews and restrict the profile: no new reviews for a period, existing reviews hidden, and a warning shown to customers.

Recommend:
- A consistent request routine (receipt QR code, WhatsApp/SMS after service, staff prompt) sent to every customer. Use the short review link from the profile.
- Reply to reviews, positive and negative, promptly, in the reviewer's language and without personal data. Health and legal businesses must never confirm someone was a patient or client. Replies are public statements, so every reply needs approval. You draft it, and the owner approves it and usually posts it (the owner-executed path; the full G4 proposal only applies if you post it yourself).
- Report only reviews that violate policy (spam, conflict of interest, off-topic, offensive), through official flows. Dislike alone isn't grounds for removal.
- Sentiment themes from reviews feed the content strategy and operations.

Never fabricate review counts or ratings for competitors. Record what you saw publicly, with the date.

## 6. Recent GBP feature changes

Keep recommendations current. As checked 2026-11-24:
- **Chat/messaging and call history** were removed from Business Profiles on **31 July 2024**. Don't recommend enabling GBP chat (Source: Changes to Google Business Profile chat and call history, https://support.google.com/business/answer/14919056, checked 2026-11-24). WhatsApp and phone links remain the practical contact routes.
- **Websites built with Business Profiles** (`business.site`) were shut down in **March 2024**; redirects ended 10 June 2024. Any profile still linking to a business.site URL has a broken website link (Source: Google Business Profile Help, https://support.google.com/business/answer/7178589, checked 2026-11-24). That is a Confirmed finding.
- **Q&A:** the Business Profile Q&A API was discontinued on **3 November 2025**, and Q&A has been replaced on Maps by an AI "Ask" experience (Gemini-generated answers drawn from profile information and reviews), rolling out by country (third-party reporting: Search Engine Roundtable, https://www.seroundtable.com/google-maps-qa-feature-ask-40594.html; Google Maps Help, Ask questions in Google Maps, https://support.google.com/maps/answer/16842041, checked 2026-11-24). Availability per country: verify at time of use. Practical effect: answers come from profile data, the website, and reviews, so complete, accurate profile fields and a website FAQ matter more than seeding Q&A.
- Other features change often (posts types, attributes, product catalogues, booking integrations). Check the live help center before recommending any feature by name.

## 7. Local keyword research

Follow keyword-research.md, plus these local specifics:
- Patterns: `<service> + <area/city>`, `<service> near me` / `قريب مني`, `best <service> in <city>`, Arabic and English variants, dialect forms (arabic-and-multilingual-seo.md), and district names people actually use (which may differ from official names).
- Build a service × area matrix only for areas genuinely served. It drives location pages and GBP services, not doorway pages.
- Search volume for hyper-local terms is often too low for tools to report. Say "below the tool's reporting threshold". Don't write zero, and don't guess.
- GBP Performance "Searches" shows the queries that triggered the profile (account view): first-party local demand evidence.

## 8. Local landing pages vs doorway pages

**Legitimate location page:** one page per real location (or per real service area with genuinely different content). It has the specific address, hours, phone, map, staff/practitioners, services offered *there*, directions and parking, local photos, location-specific reviews or testimonials, and LocalBusiness schema matching the GBP.

**Doorway pages** (spam policy): many near-identical pages that swap the city name to rank for "service + city" without a real local offer. Don't build them. Don't build pages for cities where the business has no presence and no genuine service, either.

Checks:
- Each GBP links to its own location page, not the homepage, when a location page exists.
- Location pages are linked from a crawlable store/branch locator, not only a JS map widget.
- Content uniqueness across location pages. Shared boilerplate is fine; pages that differ only in place names are a finding.

## 9. Citations and NAP consistency

**NAP** = Name, Address, Phone (plus hours and website URL in practice).

1. Establish the **canonical NAP** per location from the owner (discovery). Never pick the "correct" version yourself when sources disagree; ask.
2. Collect NAP from: the website (header/footer, contact, location pages, schema), GBP, Apple Business Connect/Apple Maps, Bing Places, Facebook/Instagram, and the market's main directories and marketplaces (e.g. delivery and booking apps, industry directories). Use public views; log the URL and date.
3. Compare with `scripts/nap_check.py`. It normalizes Arabic letter variants, Arabic-Indic digits, and phone formats (e.g. `+20 10…` vs `010…`), so only real differences are flagged.
   - Input format: `templates/nap-input-template.csv` (`location_id,source,name,address,phone,hours,website`), one row per source per location.
   - Make the first row of each location the owner-confirmed record, with `source` = `Owner master`, and run with `--canonical-source "Owner master"`.
   - Use **one file per language**. The script compares values within a file, so mixing Arabic and English names would create false mismatches.
4. Prioritize fixes: GBP and the website first, then major map platforms, then high-visibility directories. Low-quality directories add nothing; don't do mass submissions. A few accurate, relevant citations beat hundreds of spammy ones.

Arabic/English name consistency: a business can legitimately use an Arabic name and an English name. Pick a consistent pair, use it the same way everywhere, and list both in schema (`name` + `alternateName`). Transliteration drift (e.g. three spellings of the same Arabic name in Latin script) is a common finding.

## 10. LocalBusiness structured data

- Use the most specific `LocalBusiness` subtype (`Dentist`, `MedicalClinic`, `Store`, `Restaurant`…), one per location page, with `name`, `address` (`PostalAddress`), `telephone`, `openingHoursSpecification` (including special hours if maintained), `geo`, `url` (the location page), `image`, and `priceRange` where relevant.
- `parentOrganization` / `branchOf` pattern, or a shared `Organization` `@id` referenced by each location.
- Values must exactly match the canonical NAP and the GBP.
- Don't add self-serving `AggregateRating` from your own testimonials; it isn't eligible (technical-seo.md section 14).
- Validate with the Rich Results Test and the Schema.org validator. QA per seo-implementation-qa.md.

## 11. Multi-location governance

For brands with several branches, the biggest risks are inconsistency and lost control, not optimization details.

- **Location data master:** one sheet or system (`data/locations-master.csv` in the engagement folder; template: `templates/locations-master-template.csv`). Every listing and every page is fed from it. Per location it holds:
  - `location_id`, an internal, stable store identifier that also links the NAP input files. It's never the GBP profile ID; that goes in `gbp_profile_id`, alongside `gbp_profile_url`.
  - Canonical NAP in Arabic and English; hours and special hours; categories; services; the location page URL; verification status.
  - Owner and manager **roles only** (no names, emails or passwords).
  - The last-verified date.
- **Platform listings count as citations.** Medical booking directories, food-delivery apps, real-estate portals, and marketplaces often rank for brand + location queries and show their own NAP, hours, and reviews. Include them in the NAP inventory (`nap_check.py`) and in the location master.
- **Per-location audit with one central strategy.** Run section 4 for each location, using one row per location and the same columns. Summarize patterns (e.g. "9 of 14 profiles lack a website link"). Then give the per-location exceptions.
- **Board of current state:** for audits of many locations, show a screenshot/status row per location before analysis, so the user can see the estate at a glance.
- **Duplicates and unauthorized listings:** listings created by users, former staff, or old agencies. Report them, along with the evidence; resolve them through official flows, with owner approval.
- **Ownership and access structure:** the business owns the organization/account. Agencies and staff get manager access. Remove departed people only with owner approval. Document the structure, not the credentials.
- **Recovering listings held by former staff or old agencies.** This is the owner's own action, never ours. We prepare a guide for each listing; the owner executes.
  1. **Inventory:** list each listing's link, its likely holder, and whether the owner can see it in their own account (Business Profile Manager).
  2. **Ask the holder directly** to add the owner's Google account as Primary owner, then step down. This is the fastest route when the holder is reachable.
  3. **If the holder is unreachable,** the owner uses Google's official "request ownership" flow from the listing. Google notifies the current owner and sets a response window; if there's no response, Google may offer the requester a way to verify. Steps and timings change, so check Google Business Profile Help ("Request ownership of a Business Profile") at the time of use.
  4. **Meanwhile,** don't create new duplicate listings to get around the problem. Duplicates get merged or suspended, and they split reviews.
  5. **Record the outcome** in the location master: roles only, no credentials.
- **Individual practitioners** (doctors, dentists, lawyers): Google has separate guidelines for practitioner profiles versus the practice's profile. Inventory both, check them against Google's current practitioner guidelines, and treat changes as owner decisions.
- **Bulk verification** (typically 10+ locations of the same business) is an owner-level process in Business Profile Manager. Plan it with the owner; never start it casually.
- **New locations:** a launch checklist (create in BPM under the right group, store code, canonical NAP from the master, location page live first, schema, then verification), done one at a time, with a checkpoint after the first.
- **Closures/moves:** mark closed or update the address via the proper flow; redirect the old location page to the nearest location or the locator, never to a 404 with no path forward.

## 12. Measurement

- **GBP Performance** (account view): searches (queries), views on Search vs Maps, calls, website clicks, direction requests, bookings, by location and date range. Export per location monthly. The Business Profile Performance API offers this programmatically, with approved API access (tools-and-integrations.md).
- **UTM on the website link** (illustrative values only, e.g. `?utm_source=google&utm_medium=organic&utm_campaign=gbp-<store-code>`) so GA4 can separate GBP traffic from other organic traffic. Defining or changing the UTM convention is analytics configuration and needs full G4. Applying an already-approved convention to the link is a GBP edit that needs explicit approval: the owner usually makes it, which is the owner-executed path. The full G4 proposal applies if you make it yourself (SKILL.md, Approval gates). Make sure the canonical tag on the landing page strips the parameters.
- Track calls and WhatsApp clicks from location pages as GA4 events (analytics-and-measurement.md).
- Review metrics: count, average, velocity, response rate, and response time per location.
- Local rank: grid tracking if a tool is available; otherwise, don't report rankings.
- Report correlation honestly. GBP metrics move with seasonality and Google interface changes, not only with optimization.

## 13. Market notes: Egypt, Saudi Arabia, Gulf

Labeled by type. Verify at time of use for any specific claim used in client copy.
- **Data:** Google's share of search is ~95–96% in both Egypt and Saudi Arabia (StatCounter, June 2026: Egypt ~96.4%, Saudi Arabia ~95.8%, all platforms), with mobile dominant (Source: https://gs.statcounter.com/search-engine-market-share/all/egypt and https://gs.statcounter.com/search-engine-market-share/all/saudi-arabia, checked 2026-11-24). Google Maps/GBP is the primary local surface.
- **Field observation:** WhatsApp is often the preferred contact channel. Add a WhatsApp link on the website and track clicks. The GBP phone should still be a callable number under the business's control.
- **Field observation:** video verification is frequently the only method offered for new profiles in Egypt. Prepare the owner (signage visible, tools, proof of management) before starting.
- **Field observation:** Arabic vs English business names and transliteration drift across listings are common. Address formats are irregular (landmarks, "beside X"). Use the landmark wording customers use in location page copy, but keep the GBP address in the official format.
- **Field observation:** special hours for Ramadan and Eid matter. Seasonal hour changes left un-updated produce "closed" complaints in reviews.
- In Saudi Arabia and the UAE, national address systems and official business registration details may be expected on the website; check local requirements with the client rather than asserting them.

## 14. Typical findings

Bands below are indicative only. The SKILL.md formula decides P1–P3 from the actual scores, and P0 applies only to SKILL.md's global override conditions.

| Finding | Typical bucket / indicative band |
|---|---|
| Profile suspended / wrongly marked closed | Confirmed, indicative **P1**: escalate to the owner immediately (don't wait for the report), because the listing may be invisible |
| Primary owner is an ex-employee or unknown account | Confirmed, P1 (governance) |
| Website link points to retired business.site or homepage instead of location page | Confirmed, P1–P2 |
| Duplicate listings for the same location | Confirmed, P1–P2 |
| Wrong or generic primary category | Potential until compared with services and competitors; then P1–P2 |
| NAP mismatch between website, schema and GBP | Confirmed, P2 |
| No review request routine; low review velocity vs local competitors | Opportunity, P2 |
| Unanswered negative reviews | Confirmed, P2 |
| Keyword-stuffed business name on own profile | Confirmed, P1 (suspension risk) |
| City pages that only swap place names | Confirmed, P1 (doorway risk) |
| No GBP access granted | Missing data (`ANL-`/`LOC-`), public view only |
