# noahgaragesd.com

Marketing site for Noah Garage Doors, San Diego. Static HTML, deployed to Vercel
production on every push to `main` by `.github/workflows/deploy-production.yml`.

## Publishing a blog article

The article HTML is written directly nowadays; `generate_seo_article.py` is the
old Gemini path and its workflow is disabled. That matters because several
safety steps live inside that generator and no longer run for you. Do these
yourself:

- **Every article needs a hero image.** Stage `blog/<slug>.webp` and reference it
  from the article with `<img class="article-hero-img" ...>` right after the
  author byline, and from its card on `blog/index.html` with
  `<img class="card-img" ...>`. Point `og:image`, `twitter:image` and the
  JSON-LD `image` at it too, instead of leaving the generic `/og-image.jpg`.
  If no suitable photo exists, copy a topically close one from another article
  rather than leaving the card's `card-img-placeholder` div in place: it renders
  as a construction-sign emoji and looks broken. Run
  `python tools/hero_guard.py` before committing; it checks exactly this, and
  `--fix` repairs it.
- **Claims are gated.** `tools/claim_guard.py` blocks the deploy over licensing,
  insurance, bonding, background checks, lifetime warranties, invented ratings
  or review counts, guaranteed arrival windows, and em-dashes. Run it before
  committing rather than finding out from a red deploy.
- **The review count is hardcoded in two places inside `tools/claim_guard.py`**,
  the rule text and its regex. Both move together or the deploy blocks.
- Prices come from the one canonical list in `generate_seo_article.py`. Do not
  invent or recompute them.

## Voice

Written as Noah, first person, to a San Diego homeowner. No em-dashes anywhere
in customer-facing copy (the claim guard enforces this). The canonical contact
details are `(619) 572-4266` and `Noahgaragedoors@gmail.com`, and hours are 24/7.

## Tailwind

`tailwind.css` is inlined into nine pages to stop a flash of unstyled content.
After changing Tailwind classes, rebuild and run `node inline-tailwind.js`.
