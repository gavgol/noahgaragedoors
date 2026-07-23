#!/usr/bin/env python3
"""Block customer-facing claims the business cannot substantiate.

Why this exists as a standalone script: the original guard lived inside
publish-seo-article.yml, so it only ever ran when that one workflow generated an
article. When article publishing moved to a different routine in June 2026 the
guard silently stopped covering anything, and a "lifetime spring warranty" and a
"Background-Checked Technicians" line reached production. This version runs
against the files themselves, so it holds no matter who or what wrote them.

Usage:
    python tools/claim_guard.py            # scan the whole site
    python tools/claim_guard.py --staged   # scan only staged changes
    python tools/claim_guard.py f1 f2      # scan specific files

Exit code 1 on any violation, which is what makes it a gate.

Standing facts this enforces (see also the canonical price list in
generate_seo_article.py):
  - The company holds no contractor licence. Nothing may claim or imply
    licensed / insured / bonded / certified / background-checked.
  - Warranties are the manufacturer's. There is no lifetime warranty.
  - The rating is 4.9 from 44 reviews. No other figure may appear.
  - No invented operational promises (arrival windows, response times).
  - No em-dashes in customer-facing copy.
"""
import argparse
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Each rule: (id, compiled pattern, human explanation, allowed-context pattern)
# A finding is suppressed when the surrounding text matches the allow pattern.
RULES = [
    (
        'licensing',
        r'\b(licensed|licence[ds]?|licensing|insured|bonded'
        r'|background[- ]?check(ed|s)?|certified technician|factory[- ]certified)\b',
        'The company holds no contractor licence. Do not claim or imply licensed, '
        'insured, bonded, certified or background-checked.',
        # "licensed" is fine when the page is telling readers to check for one,
        # or is describing what a licence is.
        r'ask (your|the) contractor|verify (a|the|their) licen|what a licen'
        r'|licen[cs]e (number )?(lookup|search)|cslb',
    ),
    (
        'lifetime-warranty',
        r'lifetime\s+(warrant|guarantee)|(warrant|guarantee)\w*\s+for\s+life',
        'Say "manufacturer\'s warranty". There is no lifetime warranty.',
        None,
    ),
    (
        'rating',
        # Any star rating or review count that is not the real 4.9 / 44.
        r'\b(?!4\.9\b)[0-5]\.\d\s*(?:[-– ]?star|stars|/\s*5|out of 5)'
        r'|\b(?!44\b)\d{1,4}\+?\s+(?:google\s+)?reviews\b',
        'The real figures are 4.9 stars from 44 reviews. Do not use any other number.',
        None,
    ),
    (
        'response-promise',
        r'\b(?:arrive|arrival|respond|response|on ?site|there)\s+(?:in|within|under)\s+'
        r'\d+\s*(?:-|–|to)?\s*\d*\s*(?:minute|min|hour|hr)',
        'No guaranteed arrival windows. Describe response times as typical or '
        'usual, never as a promise.',
        # A hedged description of what usually happens is honest and allowed.
        # A guarantee is not. This is the line: "we typically arrive within 1 to
        # 3 hours" passes, "we guarantee arrival within 60 minutes" does not.
        r'\b(?:typically|usually|often|generally|most|vary|varies|average|'
        r'depending on|in many cases|aim to)\b',
    ),
    (
        'em-dash',
        r'—',
        'No em-dash characters in customer-facing copy.',
        None,
    ),
]

COMPILED = [(rid, re.compile(pat, re.I), why, re.compile(allow, re.I) if allow else None)
            for rid, pat, why, allow in RULES]

SKIP_DIRS = {'.git', 'node_modules', '.github', 'tools', 'backups', 'ADS-OUTPUT'}
SCAN_EXT = {'.html'}

# Machinery, not customer-facing copy. Matching inside these produces noise.
STRIP = [
    re.compile(r'<script\b[^>]*>.*?</script>', re.S | re.I),
    re.compile(r'<style\b[^>]*>.*?</style>', re.S | re.I),
    re.compile(r'<!--.*?-->', re.S),
]


def visible(html):
    """Blank out script/style/comments while preserving offsets, so reported
    line numbers still point at the right line."""
    for pat in STRIP:
        html = pat.sub(lambda m: re.sub(r'[^\n]', ' ', m.group(0)), html)
    return html


def iter_files(explicit):
    if explicit:
        for p in explicit:
            if os.path.splitext(p)[1].lower() in SCAN_EXT and os.path.exists(p):
                yield p
        return
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('_')]
        for f in sorted(files):
            if os.path.splitext(f)[1].lower() in SCAN_EXT:
                yield os.path.join(base, f)


def staged_files():
    out = subprocess.run(
        ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACMR'],
        cwd=ROOT, capture_output=True, text=True, check=True).stdout
    # The extension filter is not optional. Without it this scans the guard's
    # own source, whose rule patterns naturally contain every banned phrase, and
    # reports dozens of violations that do not exist on the site.
    return [os.path.join(ROOT, p) for p in out.split()
            if os.path.splitext(p)[1].lower() in SCAN_EXT]


def scan(path):
    with open(path, encoding='utf-8', errors='replace') as fh:
        raw = fh.read()
    text = visible(raw)
    findings = []
    for rid, pat, why, allow in COMPILED:
        for m in pat.finditer(text):
            ctx = text[max(0, m.start() - 120):m.end() + 120]
            # The allow-context is the ENCLOSING SENTENCE only. A wider window
            # lets a hedge on a neighbouring line excuse a hard guarantee, which
            # is how "we guarantee arrival within 60 minutes" first slipped past.
            sent_start = max(
                (text.rfind(c, 0, m.start()) for c in ('.', '!', '?', '>', '\n')),
                default=-1)
            sent_end = min(
                (p for p in (text.find(c, m.end()) for c in ('.', '!', '?', '<', '\n'))
                 if p != -1), default=len(text))
            sentence = text[sent_start + 1:sent_end]
            if allow and allow.search(sentence):
                continue
            line = text.count('\n', 0, m.start()) + 1
            snippet = ' '.join(re.sub(r'<[^>]+>', ' ', ctx).split())[:120]
            findings.append((rid, line, m.group(0).strip(), why, snippet))
    return findings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('files', nargs='*')
    ap.add_argument('--staged', action='store_true',
                    help='scan only files staged in git')
    args = ap.parse_args()

    targets = staged_files() if args.staged else list(iter_files(args.files))

    total = 0
    for path in targets:
        found = scan(path)
        if not found:
            continue
        try:
            rel = os.path.relpath(path, ROOT).replace(os.sep, '/')
        except ValueError:
            rel = path.replace(os.sep, '/')  # different drive on Windows
        for rid, line, hit, why, snippet in found:
            total += 1
            print(f'{rel}:{line}: [{rid}] {hit!r}')
            print(f'    {why}')
            print(f'    ...{snippet}...')
    files_scanned = len(targets)
    print(f'\nclaim guard: scanned {files_scanned} file(s), {total} violation(s).')
    if total:
        print('Fix the copy, or if a claim has become true, update the rule and the '
              'memory that records it.')
    return 1 if total else 0


if __name__ == '__main__':
    sys.exit(main())
