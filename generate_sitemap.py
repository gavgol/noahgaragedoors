#!/usr/bin/env python3
"""
Noah Garage Doors - sitemap generator.

Scans all public HTML pages and writes sitemap.xml with a real <lastmod> taken
from each file's last git commit date (falls back to today). Run manually or
automatically at the end of generate_seo_article.py so the sitemap never goes
stale (it used to miss newly auto-published articles).

Usage: python generate_sitemap.py
"""

import subprocess
from datetime import date
from pathlib import Path

BASE = "https://www.noahgaragesd.com"
ROOT = Path(__file__).parent

# Files/dirs that must never appear in the sitemap (internal/working assets).
EXCLUDE_NAMES = {"index_standalone.html"}
EXCLUDE_PREFIXES = ("social-post", "ad-creative", "garage_source", "sevan")
EXCLUDE_DIRS = {"node_modules", "NOAHGRAGEBEFOREAFTER", ".git"}


def url_for(rel: Path) -> str:
    """Map a repo-relative html path to its canonical URL."""
    parts = rel.as_posix()
    if parts == "index.html":
        return f"{BASE}/"
    if parts.endswith("/index.html"):
        return f"{BASE}/{parts[:-len('index.html')]}"  # foo/index.html -> /foo/
    return f"{BASE}/{parts}"


def priority_freq(rel: Path):
    p = rel.as_posix()
    if p == "index.html":
        return "1.0", "weekly"
    if "/" not in p:               # root-level standalone (privacy-policy, etc.)
        return "0.3", "yearly"
    if p.endswith("/index.html"):  # service / city landing pages
        return "0.9", "monthly"
    if p.startswith("blog/"):      # articles + blog index
        return ("0.6", "weekly") if p == "blog/index.html" else ("0.7", "monthly")
    return "0.5", "monthly"


def git_lastmod(rel: Path) -> str:
    try:
        out = subprocess.run(
            ["git", "log", "-1", "--format=%cs", "--", rel.as_posix()],
            cwd=ROOT, capture_output=True, text=True, timeout=20,
        ).stdout.strip()
        return out or date.today().isoformat()
    except Exception:
        return date.today().isoformat()


def collect():
    pages = []
    for path in sorted(ROOT.rglob("*.html")):
        rel = path.relative_to(ROOT)
        if any(part in EXCLUDE_DIRS for part in rel.parts):
            continue
        if rel.name in EXCLUDE_NAMES or rel.name.startswith(EXCLUDE_PREFIXES):
            continue
        pages.append(rel)
    return pages


def build():
    rows = []
    for rel in collect():
        prio, freq = priority_freq(rel)
        rows.append(
            f"  <url>\n"
            f"    <loc>{url_for(rel)}</loc>\n"
            f"    <lastmod>{git_lastmod(rel)}</lastmod>\n"
            f"    <changefreq>{freq}</changefreq>\n"
            f"    <priority>{prio}</priority>\n"
            f"  </url>"
        )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(rows)
        + "\n</urlset>\n"
    )
    (ROOT / "sitemap.xml").write_text(xml, encoding="utf-8")
    return len(rows)


if __name__ == "__main__":
    n = build()
    print(f"sitemap.xml written with {n} URLs")
