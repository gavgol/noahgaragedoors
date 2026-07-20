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
    from google import genai
except ImportError:
    print("Install: pip install google-genai")
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
    {"slug": "garage-door-wont-close-san-diego", "title": "Garage Door Won't Close in San Diego? Causes and Fixes", "type": "guide"},
    {"slug": "garage-door-wont-open-san-diego", "title": "Garage Door Won't Open? A San Diego Homeowner's Guide", "type": "guide"},
    {"slug": "garage-door-sensor-problems-san-diego", "title": "Garage Door Sensor Problems: Why Your Door Won't Close", "type": "guide"},
    {"slug": "garage-door-remote-not-working", "title": "Garage Door Remote Not Working? Fixes to Try First", "type": "guide"},
    {"slug": "signs-of-a-broken-garage-door-spring", "title": "7 Signs Your Garage Door Spring Is Broken", "type": "guide"},
    {"slug": "garage-door-opener-replacement-cost-san-diego", "title": "Garage Door Opener Replacement Cost in San Diego (2026)", "type": "guide"},
    {"slug": "new-garage-door-cost-san-diego", "title": "How Much Does a New Garage Door Cost in San Diego? (2026)", "type": "guide"},
    {"slug": "belt-drive-vs-chain-drive-opener", "title": "Belt Drive vs Chain Drive Garage Door Opener: Which Is Best?", "type": "guide"},
    {"slug": "torsion-vs-extension-springs", "title": "Torsion vs Extension Springs: Which Does Your Door Have?", "type": "guide"},
    {"slug": "insulated-vs-non-insulated-garage-doors-san-diego", "title": "Insulated vs Non-Insulated Garage Doors: Worth It in San Diego?", "type": "guide"},
    {"slug": "best-garage-doors-for-coastal-san-diego", "title": "Best Garage Doors for San Diego's Coastal Climate", "type": "guide"},
    {"slug": "how-often-to-service-garage-door", "title": "How Often Should You Service Your Garage Door?", "type": "guide"},
    {"slug": "garage-door-auto-reverse-safety-test", "title": "How to Test Your Garage Door's Auto-Reverse Safety Feature", "type": "guide"},
    {"slug": "how-long-do-garage-door-openers-last", "title": "How Long Do Garage Door Openers Last?", "type": "guide"},
    {"slug": "garage-door-repair-national-city", "title": "Garage Door Repair in National City, CA", "type": "city", "city": "National City"},
    {"slug": "garage-door-repair-coronado", "title": "Garage Door Repair in Coronado, CA", "type": "city", "city": "Coronado"},
    # --- 6-month expansion (added 2026-07-03): more SD-County cities, service pages, and how-to/cost guides ---
    {"slug": "garage-door-repair-san-marcos", "title": "Garage Door Repair in San Marcos, CA", "type": "city", "city": "San Marcos"},
    {"slug": "garage-door-opens-a-few-inches-then-stops", "title": "Garage Door Opens a Few Inches Then Stops: Causes and Fixes", "type": "guide"},
    {"slug": "garage-door-roller-replacement-san-diego", "title": "Garage Door Roller Replacement in San Diego", "type": "service"},
    {"slug": "garage-door-repair-lemon-grove", "title": "Garage Door Repair in Lemon Grove, CA", "type": "city", "city": "Lemon Grove"},
    {"slug": "garage-door-reverses-before-closing", "title": "Garage Door Reverses Before Closing: San Diego Guide", "type": "guide"},
    {"slug": "garage-door-track-repair-san-diego", "title": "Garage Door Track Repair in San Diego", "type": "service"},
    {"slug": "garage-door-repair-spring-valley", "title": "Garage Door Repair in Spring Valley, CA", "type": "city", "city": "Spring Valley"},
    {"slug": "garage-door-stuck-open-san-diego", "title": "Garage Door Stuck Open? San Diego Troubleshooting Guide", "type": "guide"},
    {"slug": "garage-door-weather-seal-replacement-san-diego", "title": "Garage Door Weather Seal Replacement in San Diego", "type": "service"},
    {"slug": "garage-door-repair-imperial-beach", "title": "Garage Door Repair in Imperial Beach, CA", "type": "city", "city": "Imperial Beach"},
    {"slug": "garage-door-opener-humming-wont-move", "title": "Garage Door Opener Hums But Won't Move: What It Means", "type": "guide"},
    {"slug": "garage-door-opener-installation-san-diego", "title": "Garage Door Opener Installation in San Diego", "type": "service"},
    {"slug": "garage-door-repair-solana-beach", "title": "Garage Door Repair in Solana Beach, CA", "type": "city", "city": "Solana Beach"},
    {"slug": "garage-door-off-balance-san-diego", "title": "Is Your Garage Door Off Balance? How to Tell and Fix It", "type": "guide"},
    {"slug": "liftmaster-opener-repair-san-diego", "title": "LiftMaster Garage Door Opener Repair in San Diego", "type": "service"},
    {"slug": "garage-door-repair-del-mar", "title": "Garage Door Repair in Del Mar, CA", "type": "city", "city": "Del Mar"},
    {"slug": "garage-door-spring-cost-san-diego", "title": "How Much Does Garage Door Spring Replacement Cost in San Diego?", "type": "guide"},
    {"slug": "chamberlain-opener-repair-san-diego", "title": "Chamberlain Garage Door Opener Repair in San Diego", "type": "service"},
    {"slug": "garage-door-repair-rancho-bernardo", "title": "Garage Door Repair in Rancho Bernardo, CA", "type": "city", "city": "Rancho Bernardo"},
    {"slug": "garage-door-remote-programming-guide", "title": "How to Program a Garage Door Remote: San Diego Guide", "type": "guide"},
    {"slug": "genie-opener-repair-san-diego", "title": "Genie Garage Door Opener Repair in San Diego", "type": "service"},
    {"slug": "garage-door-repair-la-jolla", "title": "Garage Door Repair in La Jolla, CA", "type": "city", "city": "La Jolla"},
    {"slug": "how-to-choose-a-garage-door-company-san-diego", "title": "How to Choose a Garage Door Repair Company in San Diego", "type": "guide"},
    {"slug": "garage-door-keypad-repair-san-diego", "title": "Garage Door Keypad Repair in San Diego", "type": "service"},
    {"slug": "garage-door-repair-point-loma", "title": "Garage Door Repair in Point Loma, CA", "type": "city", "city": "Point Loma"},
    {"slug": "garage-door-repair-scams-to-avoid", "title": "Garage Door Repair Scams to Avoid in San Diego", "type": "guide"},
    {"slug": "garage-door-bottom-seal-replacement-san-diego", "title": "Garage Door Bottom Seal Replacement in San Diego", "type": "service"},
    {"slug": "garage-door-repair-mira-mesa", "title": "Garage Door Repair in Mira Mesa, CA", "type": "city", "city": "Mira Mesa"},
    {"slug": "single-vs-double-garage-door", "title": "Single vs Double Garage Doors: Which Is Right for You?", "type": "guide"},
    {"slug": "new-garage-door-installation-san-diego", "title": "New Garage Door Installation in San Diego", "type": "service"},
    {"slug": "garage-door-repair-bonita", "title": "Garage Door Repair in Bonita, CA", "type": "city", "city": "Bonita"},
    {"slug": "steel-vs-wood-garage-doors", "title": "Steel vs Wood Garage Doors: A San Diego Buyer's Guide", "type": "guide"},
    {"slug": "garage-door-repair-ramona", "title": "Garage Door Repair in Ramona, CA", "type": "city", "city": "Ramona"},
    {"slug": "does-a-new-garage-door-add-home-value", "title": "Does a New Garage Door Add Home Value in San Diego?", "type": "guide"},
    {"slug": "signs-you-need-a-new-garage-door", "title": "7 Signs You Need a New Garage Door", "type": "guide"},
    {"slug": "diy-vs-professional-garage-door-repair", "title": "DIY vs Professional Garage Door Repair: When to Call a Pro", "type": "guide"},
    {"slug": "garage-door-spring-snapped-what-to-do", "title": "Garage Door Spring Snapped? What to Do Next", "type": "guide"},
    {"slug": "how-long-does-garage-door-installation-take", "title": "How Long Does Garage Door Installation Take?", "type": "guide"},
    {"slug": "best-garage-door-brands-san-diego", "title": "Best Garage Door Brands for San Diego Homes", "type": "guide"},
    {"slug": "garage-door-maintenance-checklist-san-diego", "title": "Garage Door Maintenance Checklist for San Diego Homeowners", "type": "guide"},

    # --- 9-month expansion (added 2026-07-07): more SD neighborhoods/cities, services, how-to guides ---
    {"slug": "garage-door-repair-fallbrook", "title": "Garage Door Repair in Fallbrook, CA", "type": "city", "city": "Fallbrook"},
    {"slug": "how-to-manually-open-a-garage-door", "title": "How to Manually Open a Garage Door: Step-by-Step", "type": "guide"},
    {"slug": "garage-door-hinge-replacement-san-diego", "title": "Garage Door Hinge Replacement in San Diego", "type": "service"},
    {"slug": "garage-door-repair-lakeside", "title": "Garage Door Repair in Lakeside, CA", "type": "city", "city": "Lakeside"},
    {"slug": "how-to-reset-a-garage-door-opener", "title": "How to Reset a Garage Door Opener", "type": "guide"},
    {"slug": "garage-door-tune-up-san-diego", "title": "Garage Door Tune-Up Service in San Diego", "type": "service"},
    {"slug": "garage-door-repair-alpine", "title": "Garage Door Repair in Alpine, CA", "type": "city", "city": "Alpine"},
    {"slug": "garage-door-opener-wont-work-after-power-outage", "title": "Garage Door Opener Won't Work After a Power Outage?", "type": "guide"},
    {"slug": "garage-door-lock-repair-san-diego", "title": "Garage Door Lock Repair in San Diego", "type": "service"},
    {"slug": "garage-door-repair-scripps-ranch", "title": "Garage Door Repair in Scripps Ranch, CA", "type": "city", "city": "Scripps Ranch"},
    {"slug": "why-is-my-garage-door-vibrating-or-shaking", "title": "Why Is My Garage Door Vibrating or Shaking?", "type": "guide"},
    {"slug": "glass-garage-door-installation-san-diego", "title": "Glass Garage Door Installation in San Diego", "type": "service"},
    {"slug": "garage-door-repair-pacific-beach", "title": "Garage Door Repair in Pacific Beach, CA", "type": "city", "city": "Pacific Beach"},
    {"slug": "modern-vs-traditional-garage-doors", "title": "Modern vs Traditional Garage Doors: Which Suits Your Home?", "type": "guide"},
    {"slug": "wood-garage-door-installation-san-diego", "title": "Wood Garage Door Installation in San Diego", "type": "service"},
    {"slug": "garage-door-repair-clairemont", "title": "Garage Door Repair in Clairemont, CA", "type": "city", "city": "Clairemont"},
    {"slug": "how-to-choose-a-garage-door-color", "title": "How to Choose a Garage Door Color for Your San Diego Home", "type": "guide"},
    {"slug": "garage-door-safety-inspection-san-diego", "title": "Garage Door Safety Inspection in San Diego", "type": "service"},
    {"slug": "garage-door-repair-rancho-santa-fe", "title": "Garage Door Repair in Rancho Santa Fe, CA", "type": "city", "city": "Rancho Santa Fe"},
    {"slug": "garage-door-repair-cardiff", "title": "Garage Door Repair in Cardiff, CA", "type": "city", "city": "Cardiff"},

]


ARTICLE_PROMPT = """You are writing a high-quality, locally-focused SEO blog article for Noah Garage Doors, a San Diego-based garage door repair company.

COMPANY INFO:
- Name: Noah Garage Doors
- Phone: (619) 572-4266 (this is the ONLY phone number; never invent another)
- Email: Noahgaragedoors@gmail.com (this is the ONLY email; NEVER write info@noahgaragesd.com or any other address)
- Hours: Open 24/7. We work around the clock, every day. If you mention availability, say "24/7", "round-the-clock", or "same-day". NEVER state limited or specific business hours (e.g. do NOT write "7am to 9pm", "Mon-Fri", or any opening/closing time) — that would contradict the rest of the site.
- Address: NONE. This is a Service Area Business serving all of San Diego County. NEVER print a street address in the article body or schema; refer only to "San Diego, CA" or "San Diego County".
- Key differentiators: Same-day service, lifetime spring warranty, locally owned, upfront honest pricing, experienced technicians
- IMPORTANT: Do NOT claim the business is "licensed", "insured", "bonded", "certified", or "background-checked" — it does not hold those credentials. Never use those words.
- Service area: All of San Diego County

TOPIC: {topic_title}
TYPE: {topic_type}
SLUG: {slug}

CONTENT REQUIREMENTS:
1. Article body: 800-1100 words of genuinely useful content
2. Include at least one price/cost table if relevant (use class="vs-table")
3. Include 3-4 FAQ items using the faq-card divs shown below
4. Include one CTA banner in the middle and one at the end (use cta-banner div)
5. Be specific to San Diego: mention real neighborhoods, local climate factors
6. Direct, authoritative, friendly tone. No marketing fluff.
7. NEVER use em dashes. Use commas, colons, or periods instead.
8. Use service-grid/service-card divs for lists of services when appropriate
9. INTERNAL LINKS: Within the body, naturally link 2-3 relevant phrases to these service pages (use the exact href, descriptive anchor text, NOT "click here"): /garage-door-springs/ , /garage-door-openers/ , /garage-door-off-track-repair/ , /garage-door-cable-repair/ , /garage-door-maintenance/ , /new-garage-door/ , /emergency-garage-door-repair/ . Example: <a href="/garage-door-springs/">broken garage door spring</a>. Only link phrases that genuinely match the service.
10. FAQPage SCHEMA: Fill the FAQPage JSON-LD block in the <head> with the EXACT same questions and answers as the visible faq-card FAQ section. Answers must be PLAIN TEXT (strip all HTML tags, no <a> links). The number of Question entries must equal the number of faq-card items. Escape any double quotes inside the JSON.
11. KEYWORD PLACEMENT: Put the primary keyword near the FRONT of the <title> (aim 50-60 chars), in the H1, and within the first 100 words of the body. Write a unique ~155-char meta description.

Return ONLY the complete HTML document below. Copy the EXACT structure, CSS, nav, and footer. Only change: title, meta description, canonical URL, slug, JSON-LD schema, hero badge text, h1, and article body content.

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="canonical" href="https://www.noahgaragesd.com/blog/{slug}.html">
  <link rel="icon" type="image/webp" href="/logo.webp">
  <title>[WRITE TITLE HERE] | Noah Garage Doors</title>
  <meta name="description" content="[WRITE ~155 CHAR META DESC WITH CITY AND PHONE (619) 572-4266]">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://www.noahgaragesd.com/blog/{slug}.html">
  <meta property="og:title" content="[SAME AS TITLE TAG]">
  <meta property="og:description" content="[SAME AS META DESC]">
  <meta property="og:image" content="https://www.noahgaragesd.com/og-image.jpg">
  <meta property="og:site_name" content="Noah Garage Doors">
  <meta property="article:published_time" content="{date_iso}T00:00:00Z">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="https://www.noahgaragesd.com/og-image.jpg">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "Article",
    "headline": "[ARTICLE H1]",
    "description": "[META DESC]",
    "image": "https://www.noahgaragesd.com/og-image.jpg",
    "author": {{"@type": "Person", "name": "Noah", "url": "https://www.noahgaragesd.com/#about"}},
    "publisher": {{"@type": "Organization", "name": "Noah Garage Doors", "logo": {{"@type": "ImageObject", "url": "https://www.noahgaragesd.com/logo.webp"}}}},
    "datePublished": "{date_iso}",
    "dateModified": "{date_iso}",
    "mainEntityOfPage": {{"@type": "WebPage", "@id": "https://www.noahgaragesd.com/blog/{slug}.html"}}
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {{"@type": "ListItem", "position": 1, "name": "Home", "item": "https://www.noahgaragesd.com/"}},
      {{"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://www.noahgaragesd.com/blog/"}},
      {{"@type": "ListItem", "position": 3, "name": "[ARTICLE TITLE SHORT]"}}
    ]
  }}
  </script>
  <script type="application/ld+json">
  {{
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      {{"@type": "Question", "name": "[FAQ QUESTION 1 - exact text from the FAQ section]", "acceptedAnswer": {{"@type": "Answer", "text": "[FAQ ANSWER 1 as plain text, no HTML]"}}}},
      {{"@type": "Question", "name": "[FAQ QUESTION 2]", "acceptedAnswer": {{"@type": "Answer", "text": "[FAQ ANSWER 2]"}}}},
      {{"@type": "Question", "name": "[FAQ QUESTION 3]", "acceptedAnswer": {{"@type": "Answer", "text": "[FAQ ANSWER 3]"}}}}
    ]
  }}
  </script>
  <style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; }}
    body {{ background: #0a0a0a; color: #e0e0e0; font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; font-size: 17px; line-height: 1.75; -webkit-font-smoothing: antialiased; }}
    .nav {{ background: #0a0a0a; border-bottom: 1px solid rgba(255,255,255,0.06); padding: 16px 0; position: sticky; top: 0; z-index: 100; backdrop-filter: blur(12px); }}
    .nav-inner {{ max-width: 1100px; margin: 0 auto; padding: 0 24px; display: flex; align-items: center; justify-content: space-between; }}
    .nav-brand {{ display: flex; align-items: center; gap: 12px; text-decoration: none; }}
    .nav-brand img {{ width: 40px; height: 40px; border-radius: 50%; object-fit: cover; }}
    .nav-brand-text {{ font-weight: 900; color: #fff; text-transform: uppercase; font-size: 14px; letter-spacing: -0.02em; line-height: 1.1; }}
    .nav-brand-sub {{ display: none; }}
    .nav-phone {{ display: none; align-items: center; gap: 8px; color: #fff; text-decoration: none; font-weight: 600; font-size: 15px; }}
    .nav-phone:hover {{ color: #2563EB; }}
    .nav-cta {{ background: #2563EB; color: #fff; padding: 8px 18px; border-radius: 999px; text-decoration: none; font-weight: 700; font-size: 13px; transition: all 0.2s; white-space: nowrap; }}
    .nav-cta:hover {{ background: #1D4ED8; transform: translateY(-1px); }}
    .nav-right {{ display: flex; align-items: center; gap: 12px; }}
    @media (min-width: 768px) {{ .nav-brand-text {{ font-size: 16px; letter-spacing: 1.5px; }} .nav-brand-sub {{ display: block; font-size: 8px; color: rgba(255,255,255,0.3); letter-spacing: 4px; text-transform: uppercase; font-weight: 500; }} .nav-phone {{ display: flex; color: #fff; }} .nav-cta {{ padding: 10px 22px; font-size: 14px; }} .nav-right {{ gap: 20px; }} }}
    .hero {{ background: linear-gradient(180deg, rgba(37,99,235,0.08) 0%, rgba(10,10,10,0) 60%); padding: 60px 24px 40px; text-align: center; }}
    .hero-badge {{ display: inline-block; background: rgba(37,99,235,0.12); border: 1px solid rgba(37,99,235,0.25); color: #2563EB; padding: 6px 18px; border-radius: 999px; font-size: 12px; font-weight: 600; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 20px; }}
    .article-wrap {{ max-width: 760px; margin: 0 auto; padding: 0 24px 80px; }}
    .article-wrap h1 {{ font-size: clamp(32px, 5vw, 48px); font-weight: 800; color: #ffffff; line-height: 1.15; margin-bottom: 32px; text-align: center; letter-spacing: -0.5px; }}
    .article-wrap h2 {{ font-size: 26px; font-weight: 700; color: #ffffff; margin-top: 48px; margin-bottom: 16px; padding-bottom: 8px; border-bottom: 2px solid rgba(37,99,235,0.3); }}
    .article-wrap h3 {{ font-size: 20px; font-weight: 600; color: #2563EB; margin-top: 32px; margin-bottom: 12px; }}
    .article-wrap p {{ margin-bottom: 18px; color: #c8c8c8; }}
    .article-wrap strong {{ color: #ffffff; font-weight: 600; }}
    .article-wrap a {{ color: #2563EB; text-decoration: none; border-bottom: 1px solid rgba(37,99,235,0.3); transition: border-color 0.2s; }}
    .article-wrap a:hover {{ border-bottom-color: #2563EB; }}
    .article-wrap ul, .article-wrap ol {{ margin: 16px 0 24px 24px; color: #c8c8c8; }}
    .article-wrap li {{ margin-bottom: 10px; padding-left: 4px; }}
    .article-wrap li::marker {{ color: #2563EB; }}
    .faq-card {{ background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 24px 28px; margin-bottom: 16px; }}
    .faq-q {{ color: #fff; font-weight: 600; display: block; margin-bottom: 8px; }}
    .cta-banner {{ background: linear-gradient(135deg, #0f1f4a 0%, #1a2d6e 50%, #0f1f4a 100%); border: 1px solid rgba(37,99,235,0.2); border-radius: 16px; padding: 40px; text-align: center; margin: 48px 0; }}
    .cta-banner h3 {{ color: #fff !important; font-size: 24px; margin-top: 0 !important; margin-bottom: 12px !important; }}
    .cta-banner p {{ color: #a0a0a0; margin-bottom: 24px; }}
    .cta-btn {{ display: inline-block; background: #2563EB; color: #fff !important; padding: 14px 36px; border-radius: 999px; text-decoration: none !important; font-weight: 700; font-size: 16px; border: none !important; transition: all 0.2s; margin: 0 8px; }}
    .cta-btn:hover {{ background: #1D4ED8; transform: translateY(-2px); box-shadow: 0 8px 25px rgba(37,99,235,0.3); }}
    .cta-btn.outline {{ background: transparent; border: 2px solid rgba(255,255,255,0.2) !important; }}
    .cta-btn.outline:hover {{ border-color: #2563EB !important; background: rgba(37,99,235,0.1); }}
    .footer {{ background: #050505; border-top: 1px solid rgba(255,255,255,0.06); padding: 40px 24px; text-align: center; color: #666; font-size: 14px; }}
    .footer a {{ color: #2563EB; text-decoration: none; }}
    .footer-areas {{ color: #555; margin-top: 12px; font-size: 13px; }}
    .sources {{ margin-top: 48px; padding-top: 24px; border-top: 1px solid rgba(255,255,255,0.06); font-size: 14px; color: #666; }}
    .sources a {{ color: #888; font-size: 13px; }}
    .article-hero-img {{ width: 100%; max-height: 420px; object-fit: cover; border-radius: 16px; margin-bottom: 32px; }}
    .service-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin: 24px 0; }}
    .service-card {{ background: rgba(255,255,255,0.03); border: 1px solid rgba(37,99,235,0.15); border-radius: 12px; padding: 20px; }}
    .service-card h4 {{ color: #fff; font-weight: 600; font-size: 15px; margin-bottom: 8px; }}
    .service-card p {{ color: #999; font-size: 14px; margin-bottom: 0; line-height: 1.5; }}
    .vs-table {{ width: 100%; border-collapse: collapse; margin: 24px 0; }}
    .vs-table th {{ background: rgba(37,99,235,0.15); color: #fff; font-weight: 600; padding: 12px 16px; text-align: left; border: 1px solid rgba(37,99,235,0.2); }}
    .vs-table td {{ padding: 12px 16px; border: 1px solid rgba(255,255,255,0.06); color: #c8c8c8; font-size: 15px; }}
    .vs-table tr:nth-child(even) td {{ background: rgba(255,255,255,0.02); }}
    .toc {{ background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 20px 24px; margin-bottom: 32px; }}
    .toc-title {{ color: #fff; font-weight: 700; font-size: 13px; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 10px; }}
    .toc ol {{ margin: 0; padding-left: 20px; color: #c8c8c8; }}
    .toc li {{ margin-bottom: 6px; }}
    .toc a {{ color: #9db8e8; border-bottom: none; }}
    .toc a:hover {{ color: #2563EB; }}
    @media (max-width: 640px) {{ .nav-phone {{ display: none; }} .article-wrap h2 {{ font-size: 22px; }} .cta-banner {{ padding: 28px 20px; }} .cta-btn {{ display: block; margin: 8px 0; }} .service-grid {{ grid-template-columns: 1fr; }} .vs-table {{ font-size: 14px; }} }}
  </style>
</head>
<body>
  <nav class="nav">
    <div class="nav-inner">
      <a href="/" class="nav-brand">
        <img src="/logo.webp" alt="Noah Garage Doors logo" style="height:42px;width:auto;object-fit:contain;border-radius:0;filter:brightness(2.5) drop-shadow(0 0 8px rgba(37,99,235,0.7));">
        <div>
          <div class="nav-brand-text">NOAH GARAGE DOORS</div>
          <div class="nav-brand-sub" style="color:rgba(255,255,255,0.3);font-size:8px;letter-spacing:4px;">Fast. Reliable. Local.</div>
        </div>
      </a>
      <div class="nav-right">
        <a href="tel:6195724266" class="nav-phone">&#9742; (619) 572-4266</a>
        <a href="/#quote" class="nav-cta">Free Estimate</a>
      </div>
    </div>
  </nav>

  <div class="hero">
    <div class="hero-badge">[WRITE BADGE TEXT: e.g. "San Diego County - Same-Day Service"]</div>
  </div>

  <article class="article-wrap">
    <h1>[WRITE H1 TITLE]</h1>
    <div style="display:flex;align-items:center;gap:12px;margin-bottom:28px;color:#888;font-size:14px;justify-content:center;">
      <div style="text-align:center;">
        <strong style="color:#fff;">Noah</strong> &bull; Owner, Noah Garage Doors &bull; San Diego, CA
      </div>
    </div>

    [ARTICLE CONTENT HERE - use h2, h3, p, ul, ol, service-grid, vs-table, cta-banner, faq-card as needed]

    <div style="margin:40px 0;padding:28px 32px;background:rgba(255,255,255,0.04);border-radius:16px;border:1px solid rgba(255,255,255,0.08);">
      <h3 style="font-size:1rem;font-weight:700;color:#fff;margin-bottom:14px;letter-spacing:0.05em;text-transform:uppercase;">Our Garage Door Services in San Diego</h3>
      <ul style="list-style:none;padding:0;margin:0;display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;">
        <li><a href="/garage-door-springs/" style="color:#2563EB;text-decoration:none;font-weight:500;">&rarr; Spring Repair &amp; Replacement</a></li>
        <li><a href="/garage-door-openers/" style="color:#2563EB;text-decoration:none;font-weight:500;">&rarr; Garage Door Opener Repair</a></li>
        <li><a href="/garage-door-off-track-repair/" style="color:#2563EB;text-decoration:none;font-weight:500;">&rarr; Off-Track Door Repair</a></li>
        <li><a href="/garage-door-cable-repair/" style="color:#2563EB;text-decoration:none;font-weight:500;">&rarr; Cable Repair</a></li>
        <li><a href="/garage-door-maintenance/" style="color:#2563EB;text-decoration:none;font-weight:500;">&rarr; Maintenance &amp; Tune-Up</a></li>
        <li><a href="/new-garage-door/" style="color:#2563EB;text-decoration:none;font-weight:500;">&rarr; New Garage Door Installation</a></li>
        <li><a href="/emergency-garage-door-repair/" style="color:#2563EB;text-decoration:none;font-weight:500;">&rarr; 24/7 Emergency Repair</a></li>
      </ul>
    </div>

    <div class="sources">
      <p><strong>About Noah Garage Doors:</strong> Locally owned and operated, serving all of San Diego County. Call or text <a href="tel:6195724266">(619) 572-4266</a> or email <a href="mailto:Noahgaragedoors@gmail.com">Noahgaragedoors@gmail.com</a>.</p>
    </div>
  </article>

  <footer class="footer">
    <p>&copy; 2026 <a href="/">Noah Garage Doors</a>. All rights reserved.</p>
    <p class="footer-areas">Serving San Diego &bull; Chula Vista &bull; Oceanside &bull; Carlsbad &bull; Escondido &bull; El Cajon &bull; Poway &bull; Encinitas &bull; and more</p>
  </footer>
  <script src="/cookie-consent.js?v=2" defer></script>
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
    client = genai.Client(api_key=api_key)
    date_iso = datetime.now().strftime("%Y-%m-%d")
    prompt = ARTICLE_PROMPT.format(
        topic_title=topic["title"],
        topic_type=topic.get("type", "service"),
        slug=topic["slug"],
        date_iso=date_iso,
    )
    response = _generate_with_retry(client, prompt)
    return strip_code_fences(response.text)


# Models tried in order. When the primary is overloaded (503 'high demand'),
# each retry immediately hits a DIFFERENT model instead of hammering the busy one,
# so a spike on one model doesn't fail the run (killed the 2026-06-08 + 06-11 runs).
FALLBACK_MODELS = ["gemini-2.5-flash", "gemini-2.0-flash", "gemini-flash-latest"]


def _generate_with_retry(client, prompt, attempts: int = 6):
    """Call Gemini, rotating across fallback models on transient overloads.
    503/500 UNAVAILABLE is transient (free tier is deprioritized during spikes);
    we rotate model + back off so a temporary spike doesn't fail the whole run."""
    import time
    from google.genai import errors as genai_errors

    delay = 15  # seconds; grows 15 -> 30 -> 60 ... between attempts
    for attempt in range(1, attempts + 1):
        model = FALLBACK_MODELS[(attempt - 1) % len(FALLBACK_MODELS)]
        try:
            return client.models.generate_content(model=model, contents=prompt)
        except genai_errors.ServerError as e:
            # 503/500/overload are transient; rotate model + retry. Other errors re-raise.
            if attempt == attempts:
                raise
            print(f"Gemini transient error on {model} (attempt {attempt}/{attempts}): {e}. "
                  f"Trying next model in {delay}s...")
            time.sleep(delay)
            delay = min(delay * 2, 60)


def strip_code_fences(html: str) -> str:
    """Remove a leading ```html / ``` fence and trailing ``` fence that the model
    sometimes wraps around the document (the Santee article shipped with a visible
    ```html line above <!DOCTYPE>). Returns clean HTML starting at <!DOCTYPE."""
    s = html.strip()
    s = re.sub(r"^```[a-zA-Z]*\s*\n", "", s)  # opening fence
    s = re.sub(r"\n```\s*$", "", s)            # closing fence
    return s.strip() + "\n"


def inject_hero_image(html: str, topic: dict) -> str:
    """If a hero image exists for this article's slug (blog/<slug>.webp), insert it
    after the author byline and use it as the og/twitter/schema social image.

    This makes images automatic: pre-place blog/<slug>.webp (+ optional <slug>.jpg)
    and the published article will include it. No image file -> article unchanged."""
    slug = topic["slug"]
    webp = BLOG_DIR / f"{slug}.webp"
    if not webp.exists():
        return html  # no image staged for this topic; leave article as-is

    alt = f"{topic['title']} by Noah Garage Doors"
    img_tag = (
        f'\n\n    <img class="article-hero-img" src="/blog/{slug}.webp" '
        f'width="1200" height="800" alt="{alt}">'
    )
    # Insert right after the author byline block (copied verbatim from the template).
    pattern = re.compile(r"(Owner, Noah Garage Doors.*?</div>\s*</div>)", re.DOTALL)
    new_html, n = pattern.subn(r"\1" + img_tag.replace("\\", "\\\\"), html, count=1)
    if n == 0:
        print("WARN: byline anchor not found; hero image not inserted")
        return html

    # Use the per-article image for social cards (prefer jpg for compatibility).
    social = f"/blog/{slug}.jpg" if (BLOG_DIR / f"{slug}.jpg").exists() else f"/blog/{slug}.webp"
    new_html = new_html.replace(
        "https://www.noahgaragesd.com/og-image.jpg",
        f"https://www.noahgaragesd.com{social}",
    )
    print(f"Inserted hero image for {slug}")
    return new_html


def inject_toc(html: str) -> str:
    """Insert a jump-link table of contents right after the byline/hero image,
    built deterministically from the article's own <h2> headings (never AI-written,
    so it always matches the real section order). Skipped for short articles."""
    article_match = re.search(r'(<article class="article-wrap">.*?</article>)', html, re.DOTALL)
    if not article_match:
        return html
    article_html = article_match.group(1)

    headings = list(re.finditer(r"<h2>(.*?)</h2>", article_html))
    if len(headings) < 3:
        return html  # not worth a TOC for a short article

    toc_items = []
    new_article_html = article_html
    for i, m in enumerate(headings, start=1):
        heading_text = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        anchor_id = f"s{i}"
        toc_items.append(f'<li><a href="#{anchor_id}">{heading_text}</a></li>')
        new_article_html = new_article_html.replace(m.group(0), f'<h2 id="{anchor_id}">{m.group(1)}</h2>', 1)

    toc_html = (
        '\n    <nav class="toc" aria-label="Table of contents">\n'
        '      <div class="toc-title">In This Guide</div>\n'
        "      <ol>\n        " + "\n        ".join(toc_items) + "\n      </ol>\n    </nav>\n"
    )

    insertion_pattern = re.compile(
        r'(Owner, Noah Garage Doors.*?</div>\s*</div>(?:\s*<img class="article-hero-img"[^>]*>)?)',
        re.DOTALL,
    )
    new_article_html, n = insertion_pattern.subn(lambda mm: mm.group(1) + toc_html, new_article_html, count=1)
    if n == 0:
        return html

    return html.replace(article_html, new_article_html, 1)


_STOPWORDS = {
    "garage", "door", "doors", "san", "diego", "ca", "the", "a", "an", "in", "for",
    "how", "to", "is", "are", "of", "and", "your", "you", "what", "when", "why",
    "does", "do", "vs", "guide", "county", "2026", "best", "which",
}


def _keywords(title: str) -> set:
    words = re.findall(r"[a-zA-Z']+", title.lower())
    return {w for w in words if w not in _STOPWORDS and len(w) > 2}


def inject_related_articles(html: str, topic: dict) -> str:
    """Add a 'Related Guides' box linking to 3-4 other published articles picked by
    keyword overlap with this article's title (falls back to most recent). This is
    the blog-to-blog internal linking every article was previously missing."""
    all_files = sorted(BLOG_DIR.glob("*.html"), key=lambda p: p.stat().st_mtime, reverse=True)
    self_kw = _keywords(topic["title"])
    scored = []
    for idx, f in enumerate(all_files):
        if f.stem in (topic["slug"], "index"):
            continue
        t = next((t for t in TOPIC_QUEUE if t["slug"] == f.stem), None)
        title = t["title"] if t else f.stem.replace("-", " ").title()
        score = len(self_kw & _keywords(title))
        scored.append((score, idx, f.stem, title))
    if not scored:
        return html
    scored.sort(key=lambda c: (-c[0], c[1]))
    picks = scored[:4]

    items = "\n".join(
        f'        <li><a href="/blog/{slug}.html" style="color:#2563EB;text-decoration:none;font-weight:500;">&rarr; {title}</a></li>'
        for _, _, slug, title in picks
    )
    related_html = (
        '\n    <div style="margin:40px 0 0;padding:28px 32px;background:rgba(255,255,255,0.04);border-radius:16px;border:1px solid rgba(255,255,255,0.08);">\n'
        '      <h3 style="font-size:1rem;font-weight:700;color:#fff;margin-bottom:14px;letter-spacing:0.05em;text-transform:uppercase;">Related Guides</h3>\n'
        '      <ul style="list-style:none;padding:0;margin:0;display:grid;gap:10px;">\n'
        f"{items}\n"
        "      </ul>\n    </div>\n"
    )

    # Anchor to the article's closing tag rather than the services box: that box's
    # markup has drifted across template revisions (svc-grid vs inline services list),
    # but every published article has exactly one </article>.
    if "</article>" not in html:
        return html
    return html.replace("</article>", related_html + "  </article>", 1)


def save_article(slug: str, html: str) -> Path:
    output_path = BLOG_DIR / f"{slug}.html"
    output_path.write_text(html, encoding="utf-8")
    return output_path


def update_blog_index(topic: dict, html: str = ""):
    index_path = BLOG_DIR / "index.html"
    if not index_path.exists():
        return

    date_str = datetime.now().strftime("%B %-d, %Y") if sys.platform != "win32" else datetime.now().strftime("%B %d, %Y").replace(" 0", " ")
    tag = topic.get("city", topic.get("type", "Guide").title())
    slug = topic["slug"]

    # Unique card description: pull the article's own meta description (never duplicate).
    desc = ""
    m = re.search(r'<meta name="description" content="([^"]+)"', html or "")
    if m:
        desc = m.group(1).strip()
    if not desc:
        city = topic.get("city")
        desc = (f"Same-day garage door repair for {city} homeowners: springs, openers, cables, and off-track doors. Honest upfront pricing."
                if city else f"{topic['title']}: expert guidance from Noah Garage Doors. Same-day service across San Diego County, honest pricing.")

    # Card image: use per-slug image if it was staged, else a placeholder tile.
    if (BLOG_DIR / f"{slug}.jpg").exists():
        img_html = f'<img src="/blog/{slug}.jpg" alt="{topic["title"]}" class="card-img">'
    elif (BLOG_DIR / f"{slug}.webp").exists():
        img_html = f'<img src="/blog/{slug}.webp" alt="{topic["title"]}" class="card-img">'
    else:
        img_html = '<div class="card-img-placeholder">&#128679;</div>'

    new_card = f"""
      <a href="/blog/{slug}.html" class="blog-card">
        {img_html}
        <div class="card-body">
          <div class="card-tag">{tag}</div>
          <div class="card-title">{topic['title']}</div>
          <div class="card-desc">{desc}</div>
          <div class="card-meta">
            <span class="card-date">{date_str}</span>
            <span class="card-read">Read &rarr;</span>
          </div>
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
    html = inject_hero_image(html, topic)
    html = inject_toc(html)
    html = inject_related_articles(html, topic)
    output_path = save_article(topic["slug"], html)
    update_blog_index(topic, html)

    # Keep sitemap.xml in sync so the new article is always discoverable.
    try:
        import generate_sitemap
        n = generate_sitemap.build()
        print(f"Sitemap regenerated: {n} URLs")
    except Exception as e:
        print(f"WARN: sitemap regeneration failed: {e}")

    print(f"Saved: {output_path}")
    print(f"Preview: http://localhost:3000/blog/{topic['slug']}.html")


if __name__ == "__main__":
    main()
