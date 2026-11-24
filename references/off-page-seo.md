# Off-Page SEO

Load this when assessing a site's reputation outside its own pages: backlinks, referring domains, anchor text, competitor link gaps, digital PR, directories, brand mentions, community presence, and risky or toxic links. It also defines which link-building tactics this skill will and will not recommend.

Conventions (finding schema, IDs, buckets, confidence, priority, gates) are in `SKILL.md`. Off-page findings use the `OFF-` prefix.

Contents:
1. Inputs and data reality
2. Policy boundary: legitimate vs risky
3. Audit procedure
4. Competitor link gap
5. Acquisition strategy (legitimate tactics)
6. Toxic links and disavow
7. Typical findings
8. Validation and measurement
9. Pitfalls and myths

---

## 1. Inputs and data reality

No single source sees the whole link graph. Say which source you used, and never mix their numbers.

| Source | What it gives | Limits |
|---|---|---|
| **GSC Links report** | First-party sample of external links, top linking sites, top linked pages, top anchor text | A **sample**, not comprehensive. Grouped by root domain. Doesn't flag nofollow. May include links that no longer exist. Exports are capped (Source: Links report – Search Console Help, https://support.google.com/webmasters/answer/9049606, checked 2026-11-24) |
| **Bing Webmaster Tools** backlinks | A second first-party sample, plus competitor backlink comparison | Bing's index, not Google's |
| **Ahrefs / Semrush / Majestic / Moz** | Large third-party indexes: referring domains, anchors, new/lost, competitor comparisons, authority scores | Estimates from their own crawlers. Authority scores (DR, AS, DA) are **proprietary tool metrics, not Google metrics**. Label them as such |
| **Ahrefs Webmaster Tools (free)** | Ahrefs backlink data for sites the user verifies | Own verified sites only, not competitors; verify current plan terms at time of use |
| **Public search** | Brand mentions, press, directories, community threads | Manual and partial |

If none is available beyond public search, the off-page section becomes **Missing data** for profile metrics. You can still assess brand presence, citations, and opportunities qualitatively. Never estimate referring-domain counts.

## 2. Policy boundary: legitimate vs risky

Google's spam policies define link spam as links intended to manipulate rankings (Source: Spam policies for Google web search, https://developers.google.com/search/docs/essentials/spam-policies, checked 2026-11-24). The skill only recommends tactics a business could describe openly to Google and to its customers.

**Never recommend (policy violations or high risk):**
- Buying or selling links that pass ranking credit. That includes "sponsored posts" without `rel="sponsored"`/`nofollow`, paid placements on link farms, and "guest post packages".
- Private blog networks (PBNs). Excessive link exchanges ("I'll link to you if you link to me" at scale). Automated link-building programs or comment/forum link spam.
- Large-scale article marketing or guest posting campaigns with keyword-rich anchor text.
- Widget, footer, or template links with keyword anchors distributed across many sites.
- **Expired domain abuse:** buying expired domains to exploit their past reputation for unrelated, low-value content (spam policy since March 2024).
- **Site reputation abuse:** placing third-party content on a strong host site mainly to exploit its ranking signals, e.g. coupon or review sections on news sites. Google clarified in Nov 2024 that first-party involvement doesn't excuse it (Source: Updating our site reputation abuse policy, https://developers.google.com/search/blog/2024/11/site-reputation-abuse, checked 2026-11-24). An August 2026 update changed how manual actions under this policy apply to searches in the EEA (Source: Update to the site reputation policy, https://developers.google.com/search/blog/2026/08/update-site-reputation-policy, checked 2026-11-24; read the post for details at time of use).
- Redirecting acquired domains purely to pass link equity unrelated to a genuine business merger.
- Mass, indiscriminate directory submission.

**Allowed, with correct labelling:**
- Paid placements, sponsorships, affiliate links, and advertorials **are fine when qualified** with `rel="sponsored"` (preferred) or `rel="nofollow"`. User-generated links get `rel="ugc"`. Values can be combined (Source: Qualify your outbound links to Google, https://developers.google.com/search/docs/crawling-indexing/qualify-outbound-links, checked 2026-11-24). These buy visibility and referral traffic, not ranking credit. Present them that way.

When a user asks for a risky tactic, explain the specific policy and the realistic downside (a manual action, or the links simply being ignored), and offer the legitimate alternative. Don't lecture beyond that.

## 3. Audit procedure

1. **Baseline the profile** (with the date and source): referring domains, total links, follow/nofollow mix, top linked pages, anchor distribution, new/lost trend over 6–12 months if the tool provides it.
2. **Quality and relevance review.** Sample the top ~50 referring domains, plus a random sample. For each, ask: is it a real site with real readers, relevant to the industry or locality, editorially placed? Classify each as `editorial`, `business-profile/citation`, `partner/supplier`, `community/UGC`, `scraper/auto-generated` (common and harmless), or `manipulative pattern`.
3. **Link targets.** Which pages earn links? Usually the home page only. Note when money pages or key categories have no external links at all. That's an opportunity, not an issue.
4. **Anchor text distribution.** Bucket the anchors as branded, naked URL, generic ("here", "website"), topical/partial, exact-match commercial, or image/empty. Natural profiles are mostly branded/URL/generic. A heavy share of exact-match commercial anchors from unrelated sites is a **Potential** manipulative pattern. Investigate before calling it Confirmed. There is no official "safe" percentage; any ratio you cite is a heuristic.
5. **Broken link equity.** External links pointing to URLs that now 404 or redirect in chains: reclaim them with 301s to the most relevant live page. This is often the highest-ROI off-page task. It needs a G4 gate because redirects are production changes.
6. **Brand mentions.** Search for the brand name (in all spellings and scripts, e.g. Arabic and Latin) excluding the site itself. Find unlinked mentions on reputable sites. Those are reclamation opportunities.
7. **Presence on platforms the audience uses.** Social profiles, marketplaces, industry associations, review platforms, and community forums. Check consistency of name, description, and website link, and coordinate with local-seo.md for NAP.
8. **Manual actions.** Check GSC → Security & Manual Actions. A link-related manual action is **P0**.

## 4. Competitor link gap

Needs a third-party tool (Ahrefs/Semrush "link intersect" or "backlink gap"). Without one, do a qualitative version: find where competitors are mentioned (associations, press, directories, supplier "where to buy" pages) using public search.

Procedure:
1. Choose 3–5 **search competitors**, meaning the sites that actually rank for target clusters. They aren't always the business competitors (see competitor-analysis.md).
2. List the domains linking to two or more competitors but not to the client.
3. Filter for relevance and attainability. Drop scrapers, spam, and sites that only sell links.
4. Classify each target by tactic: directory/association, press/PR, partner/supplier, resource page, event/sponsorship, community.
5. The output is an opportunity list (`OFF-` Opportunities) with a reason per target. Don't produce a raw export dump.

## 5. Acquisition strategy (legitimate tactics)

Match tactics to the business's real assets. Ask what the business actually has: suppliers, partners, awards, data, expertise, events, local ties, customers who'd vouch for it.

| Tactic | Fits | What it needs from the business | Notes |
|---|---|---|---|
| **Supplier / partner / manufacturer pages** | Retailers, distributors, agencies, integrators | Real relationships; ask partners for a "where to buy" or "partners" listing | Highly relevant, low effort |
| **Industry associations, chambers of commerce, professional bodies** | B2B, healthcare, education, local | Membership | Relevance-first |
| **Digital PR** | Brands with news, data, expertise | Real newsworthy assets: original data, surveys, expert commentary, launches, community initiatives | Pitch journalists. Never pay for editorial links without `sponsored` |
| **Linkable assets** | Content-led, SaaS, education, e-commerce with expertise | Tools, calculators, original research, definitive guides, templates | Combine with outreach |
| **Unlinked mention reclamation** | Any brand with press | — | Polite request to add a link |
| **Broken link reclamation (own)** | Sites with history or migrations | — | 301s via G4 |
| **Expert contributions / guest articles** | Professional services, SaaS, B2B | A named expert who writes or approves | A few genuinely expert pieces on relevant publications. Natural or branded anchors. No campaigns at scale with keyword anchors |
| **Local citations & community** | Local businesses | NAP data, local sponsorships, events | See local-seo.md |
| **Relevant directories** | Most, selectively | — | Only directories real customers use, or that are industry/locally authoritative. Quality over count. Never "submit to 500 directories" |
| **Community participation** | Brands with an audience on forums/Reddit/Facebook groups/Quora | Someone who answers helpfully under their real identity | The value is brand discovery and mentions (also seen by AI assistants), not the link. Links in UGC are typically `ugc`/`nofollow` |
| **HARO-style expert sourcing platforms** | Experts | Time to respond | Verify the platform still operates in the market at time of use |

Every outreach email, PR pitch, or post on the business's behalf is a **public action**, so it needs approval (SKILL.md gates). Bulk or automated outreach needs explicit approval of the list, the template, and the volume.

The strategy document states: target page groups, tactic mix, the assets required from the business, cadence it can sustain, owner, and how success is measured (referring domains from relevant sites to target pages; not "DR up by X").

## 6. Toxic links and disavow

Official guidance (Source: Disavow links to your site – Search Console Help, https://support.google.com/webmasters/answer/2648487, checked 2026-11-24):
- Most sites don't need the disavow tool. Google generally decides which links to trust.
- Disavow is appropriate when there's a considerable number of spammy, artificial, or low-quality links **and** they have caused, or are likely to cause, a manual action.
- Try removal first. Used incorrectly, the tool can harm performance. It takes weeks to process.

Rules for this skill:
- "Toxic score" from a third-party tool is **not evidence** of harm. It's a prompt to look. Random spam/scraper links are normal and almost always ignored by Google.
- Recommend a disavow only when there's a link-related manual action, or clear evidence of a past manipulative campaign by the site (e.g. links bought by a previous agency). The bucket is **Needs investigation** until that's established.
- A disavow file is a production change with a delayed and hard-to-measure effect. It requires a G4 proposal (the domains listed, the reasoning per pattern, and a rollback: a re-upload without the entries). Keep a dated copy in `07-changes/`.
- Manual action recovery: clean up → document → disavow what can't be removed → reconsideration request (with approval) describing the actions taken. Reconsideration only applies to manual actions, not algorithmic drops.

## 7. Typical findings

| Example | Prefix | Bucket | Impact | Effort |
|---|---|---|---|---|
| Link-related manual action in GSC | OFF | Confirmed (P0) | 5 | 3–5 |
| Old URLs with external links now 404 after a redesign | OFF/TEC | Confirmed | 3–4 | 2 |
| Money pages have zero external links; all links point to the home page | OFF | Opportunity | 3 | 3–4 |
| Business's suppliers/partners don't list it | OFF | Opportunity | 3 | 2 |
| Unlinked press mentions on reputable outlets | OFF | Opportunity | 2–3 | 1–2 |
| Large share of exact-match anchors from unrelated foreign sites | OFF | Potential / Needs investigation | ? | 2 |
| Brand name inconsistent across profiles | OFF/LOC | Confirmed | 2 | 2 |
| No off-page data source available | OFF | Missing data | — | — |

## 8. Validation and measurement

- Use one tool consistently for trend lines, and record which tool was used. Compare referring domains (relevant, editorial), not raw link counts.
- Track each acquired link in the tracker: URL, date, target, anchor, rel attribute, and whether it is still live.
- Reclaimed 404s: the old URL returns a 301 to a relevant live page (check the status chain); the target page is indexed.
- Expected effects are slow and confounded. Report correlation carefully (reporting-framework.md). Don't attribute ranking changes to individual links.

## 9. Pitfalls and myths

- "DA/DR is a Google metric": no. These are tool estimates.
- "Disavow all toxic links from the tool": usually unnecessary and possibly harmful.
- "Nofollow links are worthless": they can bring traffic, brand discovery, and citations. They just don't pass ranking credit by default. Google treats nofollow as a hint.
- "Social shares are a ranking factor": not directly. Social distribution helps discovery and mentions.
- "More directories = better local SEO": relevance and accuracy beat volume.
- Arabic markets: the press, directories, and communities differ by country (Egypt vs KSA vs UAE). Research them in-market. Brand mentions appear in Arabic, Latin, and transliterated spellings, so search them all. See arabic-and-multilingual-seo.md.
