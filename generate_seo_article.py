#!/usr/bin/env python3
"""
Noah Garage Doors - SEO Article Generator
Generates new blog articles using Google Gemini API (free tier).
Run manually or via GitHub Actions (2x/week).

Usage:
  python generate_seo_article.py --topic "garage door repair poway"
  python generate_seo_article.py --auto   # picks next topic from queue
"""

import os
import sys
import json
import argparse
import re
from datetime import datetime
from pathlib import Path

try:
    import google.generativeai as genai
except ImportError:
    print("Install: pip install google-generativeai")
    sys.exit(1)

BLOG_DIR = Path(__file__).parent / "blog"

# Topic queue — add new topics here. Script picks the next unpublished one.
TOPIC_QUEUE = [
    {"slug": "garage-door-repair-poway", "title": "Garage Door Repair in Poway, CA", "type": "city", "city": "Poway"},
    {"slug": "garage-door-repair-la-mesa", "title": "Garage Door Repair in La Mesa, CA", "type": "city", "city": "La Mesa"},
    {"slug": "garage-door-repair-escondido", "title": "Garage Door Repair in Escondido, CA", "type": "city", "city": "Escondido"},
    {"slug": "garage-door-repair-carlsbad", "title": "Garage Door Repair in Carlsbad, CA", "type": "city", "city": "Carlsbad"},
    {"slug": "garage-door-repair-santee", "title": "Garage Door Repair in Santee, CA", "type": "city", "city": "Santee"},
    {"slug": "garage-door-cable-repair-san-diego", "title": "Garage Door Cable Replacement in San Diego", "type": "service"},
    {"slug": "garage-door-maintenance-san-diego", "title": "Garage Door Maintenance in San Diego: What's Included", "type": "service"},
    {"slug": "garage-door-panel-repair-san-diego", "title": "Garage Door Panel Repair in San Diego", "type": "service"},
    {"slug": "smart-garage-door-opener-san-diego", "title": "Smart Garage Door Opener Installation in San Diego", "type": "service"},
    {"slug": "garage-door-repair-vs-replacement-san-diego", "title": "Garage Door Repair vs Replacement: San Diego Guide", "type": "guide"},
    {"slug": "how-long-do-garage-door-springs-last", "title": "How Long Do Garage Door Springs Last in San Diego?", "type": "guide"},
    {"slug": "garage-door-noise-san-diego", "title": "Why Is My Garage Door So Loud? San Diego Homeowners Guide", "type": "guide"},
    {"slug": "garage-door-repair-encinitas", "title": "Garage Door Repair in Encinitas, CA", "type": "city", "city": "Encinitas"},
    {"slug": "garage-door-repair-vista-ca", "title": "Garage Door Repair in Vista, CA", "type": "city", "city": "Vista"},
]


ARTICLE_PROMPT = """You are writing a high-quality, locally-focused SEO blog article for Noah Garage Doors, a San Diego-based garage door repair company.

COMPANY INFO:
- Name: Noah Garage Doors
- Phone: (619) 572-4266
- Address: 1080 8th Ave, San Diego, CA 92101
- Rating: 5.0 stars, 40 Google reviews
- Key differentiators: Same-day service, lifetime spring warranty, locally owned, licensed & insured
- Service area: All of San Diego County

TOPIC: {topic_title}
TYPE: {topic_type}

Write a complete, detailed HTML article. Requirements:
1. Title tag: "{topic_title} | Noah Garage Doors" (include year 2026 for price guides)
2. Meta description: ~155 characters, includes city name and phone
3. Article body: 700-1000 words of genuinely useful content
4. Include at least one price/cost table if relevant
5. Include 3-4 FAQ items
6. Include one CTA banner in the middle and one at the end
7. Be specific to San Diego — mention neighborhoods, local climate factors, local context
8. Write in a direct, authoritative, friendly tone (not marketing fluff)
9. IMPORTANT: Never use em dashes (—) anywhere. Use periods, commas, colons, or semicolons instead.

Return ONLY the complete HTML document, starting with <!DOCTYPE html>.
Use this exact CSS/nav/footer structure as a template — just change the content:

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="icon" type="image/webp" href="/logo.webp">
  <title>[TITLE]</title>
  <meta name="description" content="[META DESC]">
  <link rel="canonical" href="https://noahgaragedoors.com/blog/[SLUG].html">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <script type="application/ld+json">{{ Article schema }}</script>
  <style>
    [same CSS as other blog articles]
  </style>
</head>
<body>
  [nav, article content, footer]
</body>
</html>
"""


def get_next_topic():
    existing = {f.stem for f in BLOG_DIR.glob("*.html")}
    for topic in TOPIC_QUEUE:
        if topic["slug"] not in existing:
            return topic
    return None


def generate_article(topic: dict, api_key: str) -> str:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")
    prompt = ARTICLE_PROMPT.format(
        topic_title=topic["title"],
        topic_type=topic.get("type", "service"),
    )
    response = model.generate_content(prompt)
    return response.text


def save_article(slug: str, html: str) -> Path:
    output_path = BLOG_DIR / f"{slug}.html"
    output_path.write_text(html, encoding="utf-8")
    return output_path


def update_blog_index(topic: dict):
    index_path = BLOG_DIR / "index.html"
    if not index_path.exists():
        return

    date_str = datetime.now().strftime("%B %-d, %Y") if sys.platform != "win32" else datetime.now().strftime("%B %d, %Y").replace(" 0", " ")
    tag = topic.get("city", topic.get("type", "Guide").title())

    new_card = f"""
      <a href="/blog/{topic['slug']}.html" class="blog-card">
        <div class="card-tag">{tag}</div>
        <div class="card-title">{topic['title']}</div>
        <div class="card-desc">Expert garage door information for San Diego County homeowners. Same-day service, honest pricing.</div>
        <div class="card-meta">
          <span class="card-date">{date_str}</span>
          <span class="card-read">Read &rarr;</span>
        </div>
      </a>"""

    content = index_path.read_text(encoding="utf-8")
    insert_marker = "    </div>\n\n    <div class=\"cta-strip\">"
    if insert_marker in content:
        content = content.replace(insert_marker, f"    {new_card}\n{insert_marker}")
        index_path.write_text(content, encoding="utf-8")
        print(f"Updated blog index: {index_path}")


def main():
    parser = argparse.ArgumentParser(description="Generate SEO article for Noah Garage Doors")
    parser.add_argument("--topic", type=str, help="Topic slug or title to generate")
    parser.add_argument("--auto", action="store_true", help="Auto-pick next topic from queue")
    args = parser.parse_args()

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Error: Set GOOGLE_API_KEY environment variable")
        sys.exit(1)

    if args.auto:
        topic = get_next_topic()
        if not topic:
            print("All topics in queue already generated.")
            sys.exit(0)
    elif args.topic:
        matching = [t for t in TOPIC_QUEUE if args.topic.lower() in t["slug"] or args.topic.lower() in t["title"].lower()]
        if not matching:
            topic = {"slug": re.sub(r"[^a-z0-9]+", "-", args.topic.lower()).strip("-"), "title": args.topic, "type": "guide"}
        else:
            topic = matching[0]
    else:
        parser.print_help()
        sys.exit(1)

    print(f"Generating: {topic['title']}")
    print(f"Slug: {topic['slug']}")

    html = generate_article(topic, api_key)
    output_path = save_article(topic["slug"], html)
    update_blog_index(topic)

    print(f"Saved: {output_path}")
    print(f"Preview: http://localhost:3000/blog/{topic['slug']}.html")


if __name__ == "__main__":
    main()
