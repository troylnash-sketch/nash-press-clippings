#!/usr/bin/env python3
"""Extract all troynash.com URLs from specified web pages."""

import re
import urllib.request
import ssl
import sys

# Disable SSL verification for simplicity
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

pages = [
    # nashdg.com
    "https://nashdg.com/about-us",
    "https://nashdg.com/dr-troy-nash",
    "https://nashdg.com/impact",
    "https://nashdg.com/in-the-news",
    "https://nashdg.com/stakeholder-engagement",
    # agiaffinity.com
    "https://agiaffinity.com/",
    "https://agiaffinity.com/news",
    "https://agiaffinity.com/our-story",
    # tngcf.org
    "https://tngcf.org/our-story",
    "https://tngcf.org/press-media",
]

all_urls = set()
page_results = {}

for page_url in pages:
    try:
        req = urllib.request.Request(page_url, headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
        })
        resp = urllib.request.urlopen(req, context=ctx, timeout=15)
        html = resp.read().decode("utf-8", errors="replace")

        # Find all href values containing troynash.com
        found = re.findall(r'href=["\']([^"\']*troynash\.com[^"\']*)["\']', html)
        unique = sorted(set(found))
        page_results[page_url] = unique
        all_urls.update(unique)

        print(f"PAGE: {page_url}")
        print(f"  Found: {len(unique)} unique troynash.com URLs")
        for u in unique:
            print(f"  - {u}")
        print()
    except Exception as e:
        print(f"PAGE: {page_url}")
        print(f"  ERROR: {e}")
        page_results[page_url] = []
        print()

print("=" * 80)
print(f"COMPLETE DEDUPLICATED LIST: {len(all_urls)} unique troynash.com URLs")
print("=" * 80)
for u in sorted(all_urls):
    print(u)
