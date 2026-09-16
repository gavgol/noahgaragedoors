#!/usr/bin/env python3
"""Make sure no blog article ever ships without a hero image.

Why this exists as a standalone script, and not as a function inside
generate_seo_article.py: that generator already has a fallback-hero pool and an
inject_hero_image() step that cannot fail open. It stopped protecting anything
the moment article publishing moved off the Gemini workflow (now
"disabled_manually") to a routine that writes the article HTML directly. The
safety net was still in the repo, still correct, and never called.

The result reached production twice in September 2026: the Wi-Fi setup guide and
the California battery-backup guide both went live with no hero image and a
construction-sign placeholder on their blog index card, and stayed that way for
a week because nothing looks at published files.

So this runs against the files themselves, like tools/claim_guard.py, and holds
no matter who or what wrote them.

Usage:
    python tools/hero_guard.py          # report, exit 1 if anything is missing
    python tools/hero_guard.py --fix    # repair in place, exit 0 if all repaired

Two things are checked per article:
  1. the article page carries at least one content image (the logo does not
     count), and
  2. its card on blog/index.html shows a real image, not the placeholder div.

Note that city and cost pages carry a hero with a different class than the
generated guides, so the check looks for any content image rather than for one
specific class.
"""
import argparse
import hashlib
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLOG = os.path.join(ROOT, "blog")
INDEX = os.path.join(BLOG, "index.html")

# Branded interior job photos. Deliberately the same pool as
# FALLBACK_HERO_IMAGES in generate_seo_article.py: a fallback that differs
# between the generator and the guard is two answers to one question.
FALLBACK_HEROES = [
    "/blog/images/guide-default-1.jpg",
    "/blog/images/guide-default-2.jpg",
    "/blog/images/guide-default-3.jpg",
    "/blog/images/guide-default-4.jpg",
]

PLACEHOLDER = '<div class="card-img-placeholder">&#128679;</div>'

# Site furniture that is present on every page and proves nothing about whether
# the article itself is illustrated.
CHROME_IMAGES = ("/logo.webp", "/favicon", "/og-image.jpg")

IMG_SRC = re.compile(r'<img\b[^>]*\bsrc="([^"]+)"', re.IGNORECASE)
# The byline is copied verbatim into every generated article, so it is a stable
# insertion point. Falls back to the opening <article> tag if it ever moves.
BYLINE = re.compile(r"(Owner, Noah Garage Doors.*?</div>\s*</div>)", re.DOTALL)
ARTICLE_OPEN = re.compile(r'(<article class="article-wrap">)')
TITLE = re.compile(r"<title>(.*?)</title>", re.DOTALL | re.IGNORECASE)


def articles():
    for name in sorted(os.listdir(BLOG)):
        if name.endswith(".html") and name != "index.html":
            yield name[: -len(".html")], os.path.join(BLOG, name)


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text)


def has_content_image(html):
    for src in IMG_SRC.findall(html):
        if not src.startswith(CHROME_IMAGES):
            return True
    return False


def hero_for(slug):
    """Per-slug image if one is staged, else a deterministic pick from the
    branded pool. md5 rather than hash() so the same article keeps the same
    fallback across runs and across machines."""
    for ext in ("webp", "jpg"):
        if os.path.exists(os.path.join(BLOG, f"{slug}.{ext}")):
            return f"/blog/{slug}.{ext}"
    pool = [p for p in FALLBACK_HEROES if os.path.exists(os.path.join(ROOT, p.lstrip("/")))]
    if not pool:
        return None
    return pool[int(hashlib.md5(slug.encode()).hexdigest(), 16) % len(pool)]


def page_title(html, slug):
    match = TITLE.search(html)
    if not match:
        return slug.replace("-", " ").title()
    # Titles are "Topic | Noah Garage Doors" - keep the topic half.
    return re.sub(r"\s*\|.*$", "", match.group(1)).strip()


def fix_article(path, slug, html):
    hero = hero_for(slug)
    if not hero:
        return None, "no image available (per-slug file missing and fallback pool empty)"
    alt = f"{page_title(html, slug)} by Noah Garage Doors"
    tag = f'\n\n    <img class="article-hero-img" src="{hero}" width="1200" height="800" alt="{alt}">'

    fixed, count = BYLINE.subn(lambda m: m.group(1) + tag, html, count=1)
    if count == 0:
        fixed, count = ARTICLE_OPEN.subn(lambda m: m.group(1) + tag, html, count=1)
    if count == 0:
        return None, "no insertion point (neither the byline nor <article class=\"article-wrap\">)"

    # The social card should show the article's own image, not the generic one.
    fixed = fixed.replace(
        "https://www.noahgaragesd.com/og-image.jpg",
        f"https://www.noahgaragesd.com{hero}",
    )
    return fixed, hero


def fix_cards(index_html):
    """Replace every placeholder card with the real image for that slug."""
    fixed = index_html
    repaired = []
    while True:
        at = fixed.find(PLACEHOLDER)
        if at == -1:
            break
        opening = fixed.rfind('<a href="/blog/', 0, at)
        slug_match = re.match(r'<a href="/blog/([^"]+)\.html"', fixed[opening:])
        if opening == -1 or not slug_match:
            # Leave it rather than guess: an orphan placeholder is reported, not
            # silently rewritten to point at some other article's photo.
            break
        slug = slug_match.group(1)
        hero = hero_for(slug)
        if not hero:
            break
        article = os.path.join(BLOG, f"{slug}.html")
        title = page_title(read(article), slug) if os.path.exists(article) else slug
        fixed = (
            fixed[:at]
            + f'<img class="card-img" src="{hero}" alt="{title}">'
            + fixed[at + len(PLACEHOLDER):]
        )
        repaired.append((slug, hero))
    return fixed, repaired


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fix", action="store_true", help="repair in place")
    args = parser.parse_args()

    missing_articles = []
    for slug, path in articles():
        html = read(path)
        if has_content_image(html):
            continue
        if not args.fix:
            missing_articles.append((slug, "no hero image"))
            continue
        fixed, result = fix_article(path, slug, html)
        if fixed is None:
            missing_articles.append((slug, result))
            continue
        write(path, fixed)
        print(f"FIXED  {slug}: hero image {result}")

    index_html = read(INDEX)
    if args.fix:
        fixed_index, repaired = fix_cards(index_html)
        for slug, hero in repaired:
            print(f"FIXED  blog/index.html card for {slug}: {hero}")
        if fixed_index != index_html:
            write(INDEX, fixed_index)
            index_html = fixed_index
    orphan_cards = index_html.count(PLACEHOLDER)

    if missing_articles or orphan_cards:
        print("\nHero image guard FAILED:", file=sys.stderr)
        for slug, why in missing_articles:
            print(f"  blog/{slug}.html - {why}", file=sys.stderr)
        if orphan_cards:
            print(
                f"  blog/index.html - {orphan_cards} card(s) still showing the placeholder",
                file=sys.stderr,
            )
        if not args.fix:
            print("\nRun: python tools/hero_guard.py --fix", file=sys.stderr)
        return 1

    print("Hero image guard passed: every article is illustrated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
