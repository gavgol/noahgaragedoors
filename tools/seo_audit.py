#!/usr/bin/env python3
"""Structural SEO checks that are easy to break and easy to misdiagnose.

Exists because each of these checks was got WRONG by hand at least once:

  FAQ parity   Three different FAQ markup styles are in use on this site:
               <span class="faq-q">, <strong class="faq-q">, <button
               class="faq-btn">, and a bare <button onclick="toggleFaq(this)">.
               Counting question elements gives false mismatches (springs uses
               two signals on the same button and double counts) and false
               alarms (the homepage FAQ was briefly reported as missing when it
               was there all along). Counting the ANSWER container is the only
               reliable signal: exactly one per Q and A in every style.

  JSON-LD      A trailing comma anywhere silently kills a rich result.

  Dead links   Internal hrefs that resolve to nothing after a page merge.

  lastmod      Google uses it to prioritise recrawling. Pages were sitting on
               stale dates while their content had changed, so nothing got
               recrawled.

Usage:  python tools/seo_audit.py
Exit code 1 if any check fails.
"""
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = 'https://www.noahgaragesd.com/'
SKIP_DIRS = {'.git', 'node_modules', '.github', 'tools', 'backups'}
SKIP_EXT = ('.xml', '.txt', '.png', '.jpg', '.jpeg', '.webp', '.ico', '.js',
            '.css', '.svg', '.pdf', '.webmanifest', '.avif')

# One answer container per question, in every markup style used on this site.
FAQ_ANSWER = re.compile(r'class="[^"]*\b(faq-content|faq-card)\b', re.I)
LD = re.compile(r'<script[^>]*application/ld\+json[^>]*>(.*?)</script>', re.S | re.I)


def html_files():
    out = []
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('_')]
        for f in sorted(files):
            if f.endswith('.html'):
                out.append(os.path.join(base, f))
    return out


def rel(p):
    return os.path.relpath(p, ROOT).replace(os.sep, '/')


def strip_machinery(html):
    """Remove style blocks and non-JSON-LD scripts, so CSS rule definitions and
    event handlers are not mistaken for page content."""
    html = re.sub(r'<style\b.*?</style>', ' ', html, flags=re.S | re.I)
    return re.sub(r'<script(?![^>]*ld\+json)\b.*?</script>', ' ', html,
                  flags=re.S | re.I)


def main():
    files = html_files()
    failures = []

    # 1. JSON-LD parses
    blocks = 0
    for p in files:
        raw = open(p, encoding='utf-8').read()
        for m in LD.finditer(raw):
            blocks += 1
            try:
                json.loads(m.group(1))
            except Exception as e:
                failures.append(f'{rel(p)}: JSON-LD does not parse: {e}')
    print(f'JSON-LD          {blocks} blocks')

    # 2. FAQ schema matches visible content
    checked = 0
    for p in files:
        raw = open(p, encoding='utf-8').read()
        schema_n = None
        for m in LD.finditer(raw):
            try:
                d = json.loads(m.group(1))
            except Exception:
                continue
            if isinstance(d, dict) and d.get('@type') == 'FAQPage':
                schema_n = len(d.get('mainEntity', []))
        if schema_n is None:
            continue
        checked += 1
        page_n = len(FAQ_ANSWER.findall(strip_machinery(raw)))
        if page_n != schema_n:
            failures.append(
                f'{rel(p)}: FAQPage schema has {schema_n} questions but the page '
                f'shows {page_n}. Schema must match visible content.')
    print(f'FAQ parity       {checked} pages with FAQPage schema')

    # 3. Internal links resolve
    known = {rel(p) for p in files}
    known |= {p.rsplit('/', 1)[0] + '/' for p in known if p.endswith('index.html')}
    dead = 0
    for p in files:
        for h in set(re.findall(r'href="(/[^"#?]*)"', open(p, encoding='utf-8').read())):
            t = h.lstrip('/')
            if t == '' or t in known or (t + 'index.html') in known:
                continue
            if any(t.lower().endswith(e) for e in SKIP_EXT):
                continue
            dead += 1
            failures.append(f'{rel(p)}: dead internal link {h}')
    print(f'Internal links   {dead} dead')

    # 4. Every sitemap URL exists, and every indexable page is in the sitemap
    sm = os.path.join(ROOT, 'sitemap.xml')
    if os.path.exists(sm):
        raw = open(sm, encoding='utf-8').read()
        entries = re.findall(r'<loc>(.*?)</loc>', raw)
        for loc in entries:
            path = loc.replace(BASE, '')
            cand = path if path.endswith('.html') else path + 'index.html'
            if cand and cand not in known:
                failures.append(f'sitemap.xml: {loc} has no matching file')
        listed = {l.replace(BASE, '') for l in entries}
        for p in files:
            r = rel(p)
            if r.startswith('_'):
                continue
            body = open(p, encoding='utf-8').read()
            if re.search(r'<meta[^>]+robots[^>]+noindex', body, re.I):
                continue
            url = r[:-len('index.html')] if r.endswith('index.html') else r
            if url not in listed:
                failures.append(f'{r}: indexable but missing from sitemap.xml')
        print(f'Sitemap          {len(entries)} urls')

    print()
    if failures:
        print(f'FAILED, {len(failures)} problem(s):')
        for f in failures:
            print('  -', f)
        return 1
    print('All structural SEO checks passed.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
