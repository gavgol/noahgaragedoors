# Noah Garage Doors: 6-Month SEO Article Roadmap

Built 2026-07-22 from live Google Search Console data (28 days ending 2026-07-21).
Governs `TOPIC_QUEUE` in `generate_seo_article.py`. The cloud routine publishes 2 articles
per week (Monday and Thursday) and always takes the FIRST slug in queue order that does not
yet exist as `blog/<slug>.html`. **Queue order is the publishing schedule.** Reordering the
list reorders what goes live.

---

## 1. What the data says

Site totals, 28 days to 2026-07-21: **14 clicks, 2199 impressions, CTR 0.64%, avg position 24.1.**
Prior 28 days had 238 impressions, so impressions grew about 824% while clicks stayed flat.

Where the impressions sit:

| Position band | Share of impressions |
|---|---|
| 1 to 3 | 9.0% |
| 4 to 10 | 5.2% |
| 11 to 20 | 24.4% |
| 21 to 50 | 45.5% |
| 51+ | 16.0% |

Three conclusions drive this roadmap.

**a) The site does not have a content-volume problem, it has a position problem.**
Seventy percent of impressions sit at position 11 or worse. Clicks at position 11 to 25 are
close to zero, which is exactly what the 0.64% CTR shows. Publishing more of the same thing
adds impressions at position 30 and no clicks. The lever is pushing the pages that already sit
at position 10 to 25 up into the top 5, using supporting content that links to them.

**b) There is one very large single asset.**
The query `emergency garage door repair` returns 195 impressions at average position 12.8 with
zero clicks. `emergency garage door repair near me` adds 25 more at 15.8, and
`emergency garage door repair san diego` another 29 at 26.9. The landing page,
`/blog/emergency-garage-door-repair-san-diego.html`, is the strongest page on the site
(292 impressions, position 16.6). Moving that cluster from position 13 to position 4 is worth
more than the entire rest of the queue combined. Tier 1 exists to feed it internal links and
topical depth.

**c) The city posts are not earning their keep.**
There are 12 published city posts, all from the same template, and 29 more were queued. The
homepage outranks them for their own city query:

| Query | Homepage | The city post |
|---|---|---|
| `garage door repair chula vista ca` | 65 impr @ pos 40.7 | 1 impr @ pos 68 |
| `garage doors la mesa ca` | 42 impr @ pos 19.1 | 3 impr @ pos 31.3 |

Google is choosing the homepage and ignoring the templated posts. That is the classic signature
of doorway pages. Adding 29 more would deepen the problem, dilute internal link equity, and put
the site at risk of a thin-content assessment. The queue keeps four cities and parks the rest.

---

## 2. What changed in the queue

- **Before:** 90 items, 71 unpublished.
- **Removed from the live queue:** 38 items, moved to commented `PARKED_*` lists at the bottom
  of `generate_seo_article.py`. Nothing was deleted.
- **Added:** 10 new topics that fill real gaps without competing with an existing page.
- **After:** 43 items in `TOPIC_QUEUE`, all unpublished, no slug collisions, no internal duplicates.
  That is 22 weeks of publishing, from 2026-07-27 through 2026-12-21.

### 2.1 Cut: duplicates an existing service page or a published post (13)

The service pages that already exist as `/<slug>/index.html` are: `emergency-garage-door-repair`,
`garage-door-springs`, `garage-door-openers`, `garage-door-off-track-repair`,
`garage-door-cable-repair`, `garage-door-maintenance`, `new-garage-door`.

| Parked slug | Cannibalizes |
|---|---|
| `garage-door-track-repair-san-diego` | `/garage-door-off-track-repair/` (blog dupe merged in and 301d, 2026-07) |
| `garage-door-opener-installation-san-diego` | `/garage-door-openers/` |
| `new-garage-door-installation-san-diego` | `/new-garage-door/` |
| `garage-door-tune-up-san-diego` | `/garage-door-maintenance/` (blog dupe merged in and 301d, 2026-07) |
| `garage-door-safety-inspection-san-diego` | `/garage-door-maintenance/` |
| `garage-door-maintenance-checklist-san-diego` | the published maintenance post plus `how-often-to-service-garage-door` |
| `glass-garage-door-installation-san-diego` | thin subtopic of `/new-garage-door/` |
| `wood-garage-door-installation-san-diego` | thin subtopic of `/new-garage-door/`, plus `steel-vs-wood-garage-doors` |
| `garage-door-stuck-open-san-diego` | `blog/garage-door-wont-close-san-diego.html` (same user intent) |
| `garage-door-reverses-before-closing` | `blog/garage-door-sensor-problems-san-diego.html` |
| `why-is-my-garage-door-vibrating-or-shaking` | `blog/garage-door-noise-san-diego.html` |
| `how-to-reset-a-garage-door-opener` | `blog/garage-door-remote-not-working.html` plus the kept remote-programming guide |
| `modern-vs-traditional-garage-doors` | `steel-vs-wood-garage-doors` plus `single-vs-double-garage-door` |

The last five were not flagged in the original brief. They were found by comparing every queued
slug against every published `blog/*.html` and every service page directory.

### 2.2 Cut: same topic as another queued item (3)

| Parked slug | Reason |
|---|---|
| `garage-door-bottom-seal-replacement-san-diego` | Identical topic to `garage-door-weather-seal-replacement-san-diego`. Kept the weather-seal version because it is the broader term and covers the bottom seal inside it. |
| `chamberlain-opener-repair-san-diego` | Chamberlain and LiftMaster are the same manufacturer. The copy would be near identical. Kept LiftMaster, the higher-volume brand name. |
| `genie-opener-repair-san-diego` | A third templated brand page repeats the city-page mistake at the brand level. |

### 2.3 Cut: spring topic saturation (2)

Already live: `/garage-door-springs/`,
`blog/how-long-do-garage-door-springs-last.html`, and `blog/signs-of-a-broken-garage-door-spring.html`
(the last one was already published, so it left the queue on its own).

| Parked slug | Reason |
|---|---|
| `garage-door-spring-cost-san-diego` | Competes with both the spring-replacement post and `blog/how-much-does-garage-door-repair-cost-san-diego.html` (151 impr, position 22.7), the site's second-strongest page. Do not put a competitor in front of it. |
| `garage-door-spring-snapped-what-to-do` | Same intent as the published `signs-of-a-broken-garage-door-spring` and the emergency post. |

`torsion-vs-extension-springs` was **kept**. It is genuinely a different query (identification,
not repair) and it is the only spring topic with no existing page.

### 2.4 Cut: negligible demand (2)

`garage-door-lock-repair-san-diego` and `how-to-choose-a-garage-door-color`. Neither has
meaningful search volume or commercial intent for a repair business.

### 2.5 Cut: city bloat (18 of 22)

Kept 4, parked 18.

| Kept city | Why |
|---|---|
| La Jolla | The only unpublished city with proven demand in GSC: `garage doors la jolla ca`, 21 impressions at position 19.1. Already close to the first page. |
| San Marcos | Largest San Diego County city with no page, roughly 95,000 residents. |
| Spring Valley | Roughly 70,000 residents, and it sits between La Mesa and El Cajon, the corridor that already shows query demand. |
| National City | Roughly 56,000 residents, adjacent to Chula Vista, which is the strongest city query the site has (`garage door repair chula vista ca`, 66 impressions). |

The 18 parked cities are mostly small beach towns, backcountry towns, or neighborhoods of the
city of San Diego. Neighborhood pages such as Point Loma, Mira Mesa, Clairemont, Pacific Beach
and Scripps Ranch are the worst of the group because they compete directly with the homepage and
the main San Diego service pages.

**These four are an experiment, not a green light.** Before any parked city is reinstated, the
four kept pages must show they can rank. See section 5.

### 2.6 Added (10)

Each of these fills a gap with no existing page, no overlap, and real commercial or emergency intent.

| New slug | Why it earns a slot |
|---|---|
| `garage-door-opener-battery-backup-california-law` | California requires battery backup on residential openers installed in the state. It is a legally specific, locally unique topic no competitor blog template covers, and it converts into opener replacement work. |
| `garage-door-opener-wifi-app-setup-san-diego` | Supports the published smart-opener post with a how-to that captures a separate query set. |
| `commercial-garage-door-repair-san-diego` | Genuinely distinct commercial intent, higher ticket, and there is no page for it anywhere on the site. |
| `how-to-lubricate-a-garage-door` | High-volume how-to that feeds `/garage-door-maintenance/` without duplicating it. |
| `garage-door-security-tips-san-diego` | Distinct informational cluster, links naturally to openers and locks. |
| `how-to-measure-for-a-new-garage-door` | Supports `/new-garage-door/`, which has 146 impressions but sits at position 47.5. |
| `garage-door-window-replacement-san-diego` | Distinct part service, no existing page. |
| `rv-garage-door-installation-san-diego` | Oversized and RV doors are a high-ticket niche with almost no local competition. |
| `garage-door-installation-permit-san-diego` | Locally specific, high trust value, cannot be templated by a national competitor. |
| `garage-door-repair-for-hoa-and-condos-san-diego` | Repeat-revenue B2B intent. One HOA contract is worth many homeowner jobs. |

---

## 3. Publish schedule

Two per week, Monday and Thursday, starting Monday 2026-07-27.

### Tier 1: emergency and trust cluster (weeks 1 to 4)
Everything here either feeds the emergency page or answers the "who do I trust at 11pm" question.
`garage door company` already sits at position 7.7, so the trust posts are near-term click wins.

| # | Date | Type | Slug |
|---|---|---|---|
| 1 | Mon Jul 27, 2026 | guide | `how-to-manually-open-a-garage-door` |
| 2 | Thu Jul 30, 2026 | guide | `garage-door-opener-wont-work-after-power-outage` |
| 3 | Mon Aug 03, 2026 | guide | `garage-door-opens-a-few-inches-then-stops` |
| 4 | Thu Aug 06, 2026 | guide | `garage-door-opener-humming-wont-move` |
| 5 | Mon Aug 10, 2026 | guide | `how-to-choose-a-garage-door-company-san-diego` |
| 6 | Thu Aug 13, 2026 | guide | `garage-door-repair-scams-to-avoid` |
| 7 | Mon Aug 17, 2026 | guide | `diy-vs-professional-garage-door-repair` |
| 8 | Thu Aug 20, 2026 | city | `garage-door-repair-la-jolla` |

### Tier 2: opener cluster (weeks 5 to 8)
`garage door opener repair` sits at position 13.3 and `/garage-door-openers/` at 38.4. This tier
exists to lift both.

| # | Date | Type | Slug |
|---|---|---|---|
| 9 | Mon Aug 24, 2026 | guide | `garage-door-opener-replacement-cost-san-diego` |
| 10 | Thu Aug 27, 2026 | guide | `how-long-do-garage-door-openers-last` |
| 11 | Mon Aug 31, 2026 | guide | `belt-drive-vs-chain-drive-opener` |
| 12 | Thu Sep 03, 2026 | guide | `garage-door-remote-programming-guide` |
| 13 | Mon Sep 07, 2026 | service | `liftmaster-opener-repair-san-diego` |
| 14 | Thu Sep 10, 2026 | guide | `garage-door-opener-battery-backup-california-law` |
| 15 | Mon Sep 14, 2026 | guide | `garage-door-opener-wifi-app-setup-san-diego` |

### Tier 3: distinct parts and commercial services (weeks 9 to 12)
Hardware services with no existing page, plus the first B2B page.
`garage door cable replacement near me` is already at position 7.6, and rollers are the natural
adjacent part, so this tier also reinforces the cable page.

| # | Date | Type | Slug |
|---|---|---|---|
| 16 | Thu Sep 17, 2026 | service | `garage-door-roller-replacement-san-diego` |
| 17 | Mon Sep 21, 2026 | service | `garage-door-keypad-repair-san-diego` |
| 18 | Thu Sep 24, 2026 | service | `garage-door-weather-seal-replacement-san-diego` |
| 19 | Mon Sep 28, 2026 | service | `garage-door-hinge-replacement-san-diego` |
| 20 | Thu Oct 01, 2026 | service | `commercial-garage-door-repair-san-diego` |
| 21 | Mon Oct 05, 2026 | city | `garage-door-repair-san-marcos` |

### Tier 4: diagnostics and maintenance (weeks 13 to 16)

| # | Date | Type | Slug |
|---|---|---|---|
| 22 | Thu Oct 08, 2026 | guide | `garage-door-off-balance-san-diego` |
| 23 | Mon Oct 12, 2026 | guide | `torsion-vs-extension-springs` |
| 24 | Thu Oct 15, 2026 | guide | `how-to-lubricate-a-garage-door` |
| 25 | Mon Oct 19, 2026 | guide | `how-often-to-service-garage-door` |
| 26 | Thu Oct 22, 2026 | guide | `garage-door-auto-reverse-safety-test` |
| 27 | Mon Oct 26, 2026 | guide | `garage-door-security-tips-san-diego` |
| 28 | Thu Oct 29, 2026 | city | `garage-door-repair-spring-valley` |

### Tier 5: new-door buying cluster (weeks 17 to 22)
`/new-garage-door/` has 146 impressions but sits at position 47.5, the weakest high-impression
page on the site. It needs topical support around it, not more traffic pointed at it.

| # | Date | Type | Slug |
|---|---|---|---|
| 29 | Mon Nov 02, 2026 | guide | `new-garage-door-cost-san-diego` |
| 30 | Thu Nov 05, 2026 | guide | `signs-you-need-a-new-garage-door` |
| 31 | Mon Nov 09, 2026 | guide | `how-to-measure-for-a-new-garage-door` |
| 32 | Thu Nov 12, 2026 | guide | `insulated-vs-non-insulated-garage-doors-san-diego` |
| 33 | Mon Nov 16, 2026 | guide | `best-garage-doors-for-coastal-san-diego` |
| 34 | Thu Nov 19, 2026 | guide | `steel-vs-wood-garage-doors` |
| 35 | Mon Nov 23, 2026 | guide | `single-vs-double-garage-door` |
| 36 | Thu Nov 26, 2026 | guide | `best-garage-door-brands-san-diego` |
| 37 | Mon Nov 30, 2026 | guide | `does-a-new-garage-door-add-home-value` |
| 38 | Thu Dec 03, 2026 | guide | `how-long-does-garage-door-installation-take` |
| 39 | Mon Dec 07, 2026 | city | `garage-door-repair-national-city` |
| 40 | Thu Dec 10, 2026 | service | `garage-door-window-replacement-san-diego` |
| 41 | Mon Dec 14, 2026 | service | `rv-garage-door-installation-san-diego` |
| 42 | Thu Dec 17, 2026 | guide | `garage-door-installation-permit-san-diego` |
| 43 | Mon Dec 21, 2026 | service | `garage-door-repair-for-hoa-and-condos-san-diego` |

Note: slot 36 falls on Thanksgiving, Nov 26. The routine is automated so it does not matter, but
do not expect that post to get early social amplification.

### Weeks 23 to 26 (late Dec 2026 to late Jan 2027): refresh sprint, no new topics

The queue runs out on purpose after 2026-12-21. `get_next_topic()` returns `None` and the routine
stops cleanly, so nothing breaks. That is by design.

Given that 70% of impressions sit at position 11 or worse, the highest-value work in the final
month is not new articles. It is:

1. Rewriting `/new-garage-door/` (146 impressions at position 47.5). The impressions prove
   demand. Position 47 proves the page is not answering the query.
2. Rewriting `/garage-door-off-track-repair/` (76 impressions at position 52.8) and
   `/garage-door-springs/` (83 at 46.7). Same story.
3. Consolidating the 12 underperforming city posts. Either differentiate each one properly with
   genuinely local detail, or merge the weakest into a single service-area page and 301 the rest.
4. Adding internal links from the Tier 1 and Tier 2 posts into
   `/emergency-garage-door-repair/` and `/blog/emergency-garage-door-repair-san-diego.html`.
5. Citations and Google Business Profile work. The 2026-07-08 audit already concluded this is an
   authority gap, not a content gap. Two articles a week does not fix authority. Citations do.

Re-pull GSC before deciding what the next queue looks like.

---

## 4. What success looks like

Do not measure this by article count. Measure it by these, month over month:

| Metric | Now (28d to 2026-07-21) | Target by 2027-01 |
|---|---|---|
| `emergency garage door repair` avg position | 12.8 | top 5 |
| Site CTR | 0.64% | above 2% |
| Share of impressions at position 1 to 10 | 14.2% | above 30% |
| Clicks | 14 | 60+ |

If impressions keep climbing while CTR stays under 1%, stop publishing and go do citations.
That result would mean the content is fine and the domain is not trusted enough to rank it.

---

## 5. Rules for future topics

Apply every one of these before adding anything to `TOPIC_QUEUE`.

1. **No page may compete with an existing service page.** Check `/<slug>/index.html` first. The
   service pages are: `emergency-garage-door-repair`, `garage-door-springs`, `garage-door-openers`,
   `garage-door-off-track-repair`, `garage-door-cable-repair`, `garage-door-maintenance`,
   `new-garage-door`. If a topic is that service, improve the service page instead of writing a post.
2. **Check every published `blog/*.html` before adding.** Different wording is not a different
   topic. "Stuck open" and "won't close" are the same query intent to Google.
3. **One topic, one page.** If two queued titles would answer the same question, keep the broader
   one and park the other.
4. **No new city pages until the format proves itself.** Review the four kept city pages
   (La Jolla, San Marcos, Spring Valley, National City) 90 days after each goes live. Reinstate a
   parked city ONLY if a kept city page ranks in the top 20 for its own `garage door repair <city> ca`
   query AND outranks the homepage for it. If the kept pages fail, remove city pages from the
   strategy and put the effort into the Google Business Profile service area instead.
5. **No brand pages beyond one per manufacturer.** LiftMaster and Chamberlain are the same company.
6. **Prefer topics that support a page already at position 10 to 25.** Those are the pages one push
   away from clicks. A brand new topic at position 40 earns nothing.
7. **Never add a cost page that competes with `blog/how-much-does-garage-door-repair-cost-san-diego.html`.**
   It is the second-strongest page on the site (151 impressions, position 22.7). Cost pages must be
   for a specific distinct item, such as an opener or a new door, never for "repair" generally.
8. **The queue is allowed to run out.** An empty queue is better than filler. When it empties,
   pull fresh GSC data and rebuild from evidence.

### Copy constraints that apply to every generated article

These are enforced in `ARTICLE_PROMPT` inside `generate_seo_article.py`. Do not weaken them.

- **Never** claim the business is licensed, insured, bonded, certified, or background-checked.
  Noah does not hold those credentials yet.
- Say **"manufacturer's warranty"**. Never "lifetime warranty" or "lifetime spring warranty".
  (Fixed 2026-07-22: the prompt previously instructed the generator to write "lifetime spring
  warranty" as a key differentiator. That has been corrected and an explicit rule added.)
- **No em-dashes** anywhere in customer-facing copy. Use commas or periods.
- Canonical contact details: phone (619) 572-4266, email Noahgaragedoors@gmail.com, hours 24/7.
- No street address. This is a service area business covering San Diego County.
