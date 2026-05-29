# Reviews / Ratings Backup & Restore Guide

**Status (2026-05-30):** Noah Garage Doors has **0 reviews** so far. The site is being
submitted to Google Business; once a real Google Business profile exists and real reviews
are collected, restore the rating claims below with the **real numbers**.

⚠️ Do NOT restore fake/placeholder numbers. Google penalizes fake `aggregateRating` schema
and it is deceptive advertising. Only restore once you have verifiable reviews.

The full testimonials **section** is already preserved in-place inside `index.html` as an
HTML comment marked `<!-- REVIEWS-SECTION hidden until real reviews added ... -->`
(plus the nav links `<!-- REVIEWS-NAV-DESKTOP ... -->` and `<!-- REVIEWS-NAV-MOBILE ... -->`).
The items below are the rating CLAIMS that were also removed from the live pages.

---

## 1. JSON-LD `aggregateRating` (index.html, inside LocalBusiness schema)

Removed block (was between `openingHoursSpecification` and `priceRange`):

```json
      "aggregateRating": {
        "@type": "AggregateRating",
        "ratingValue": "5.0",
        "reviewCount": "40"
      },
```

**Restore:** paste back after the `openingHoursSpecification` object, with REAL
`ratingValue` and `reviewCount` from your Google Business profile.

## 2. Trust band (index.html ~line 679)

Original:
```html
<span class="flex items-center gap-1.5"><i data-lucide="star" class="w-4 h-4 text-yellow-400 fill-yellow-400 shrink-0"></i><span class="text-white font-bold">5.0</span><span class="text-white/40 font-normal">· 40 Google Reviews</span></span>
<span class="text-white/20 hidden sm:block">|</span>
```

## 3. Quote sidebar (index.html ~line 1965)

Original:
```html
<span class="text-white font-semibold">5.0 · 40 Google reviews</span>
```

## 4. Hero badge (index.html ~line 661)

Original:
```html
<i data-lucide="star" class="w-4 h-4 text-yellow-400 fill-yellow-400"></i> 5-Star Rated
```

## 5. Gallery stats bar (gallery/index.html ~line 154-155)

Original:
```html
<div class="font-display" style="font-size:2rem;font-weight:900;color:#60a5fa;">5★</div>
<div style="...">Average Rating</div>
```

## 6. Sub-page "5-Star Rated" trust chips

Pages: `garage-door-maintenance/index.html`, `garage-door-springs/index.html`,
`garage-door-openers/index.html` each had a `5-Star Rated` chip with a star icon.

## 7. Sub-page nav "Reviews" links

Most sub-pages link to `/#reviews`. That anchor target is currently hidden on the homepage.
When the reviews section is restored, these links will work again automatically.

---

### Restore checklist (when real reviews exist)
- [ ] Un-comment `REVIEWS-SECTION`, `REVIEWS-NAV-DESKTOP`, `REVIEWS-NAV-MOBILE` in index.html
- [ ] Replace placeholder testimonials in that section with REAL reviews
- [ ] Add back `aggregateRating` (item 1) with real numbers
- [ ] Restore trust-band + sidebar review counts (items 2, 3) with real numbers
- [ ] Restore hero / gallery / sub-page rating chips (items 4, 5, 6) if desired
