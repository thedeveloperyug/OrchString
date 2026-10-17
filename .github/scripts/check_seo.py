#!/usr/bin/env python3
"""Validate SEO signals for the single-page Neytra website before deployment."""

from datetime import date
from html.parser import HTMLParser
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
CANONICAL = "https://neytraintelligence.com/"
SITEMAP = CANONICAL + "sitemap.xml"
BRAND_INTRO = "The Neytra Intelligence Platform (NIP) is an AI-powered, enterprise-oriented execution platform designed to transform business objectives into coordinated, controlled, and verifiable workflows."


class HeadParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonicals = []
        self.metadata = {}
        self.in_head = False

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag == "head":
            self.in_head = True
        if not self.in_head:
            return
        if tag == "link" and data.get("rel", "").lower() == "canonical":
            self.canonicals.append(data.get("href", ""))
        if tag == "meta":
            name = (data.get("name") or data.get("property") or "").lower()
            self.metadata[name] = data.get("content", "")

    def handle_endtag(self, tag):
        if tag == "head":
            self.in_head = False


def main():
    errors = []
    parser = HeadParser()
    parser.feed((ROOT / "index.html").read_text(encoding="utf-8"))

    if parser.canonicals != [CANONICAL]:
        errors.append("index.html needs exactly one canonical pointing to " + CANONICAL)
    if parser.metadata.get("og:url") != CANONICAL:
        errors.append("Open Graph URL must match the canonical URL")
    if parser.metadata.get("description") != BRAND_INTRO:
        errors.append("Homepage meta description must match the official NIP introduction")
    homepage = (ROOT / "index.html").read_text(encoding="utf-8")
    if "NEYTRA" in homepage:
        errors.append("Use Neytra title case, not all-caps NEYTRA")
    if homepage.count(BRAND_INTRO) < 2:
        errors.append("Official NIP introduction must appear in visible homepage content")
    robots_meta = parser.metadata.get("robots", "").lower().replace(" ", "")
    if "noindex" in robots_meta or "nofollow" in robots_meta:
        errors.append("Homepage must not be marked noindex/nofollow")

    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    if "User-agent: *" not in robots or "Allow: /" not in robots:
        errors.append("robots.txt must allow crawlers")
    if "Sitemap: " + SITEMAP not in robots:
        errors.append("robots.txt sitemap must point to the primary .com domain")

    try:
        sitemap = ET.parse(ROOT / "sitemap.xml").getroot()
        namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        urls = sitemap.findall("s:url", namespace)
        locations = [(u.findtext("s:loc", default="", namespaces=namespace)).strip()
                     for u in urls]
        if locations != [CANONICAL]:
            errors.append("Sitemap must list only the primary canonical homepage")
        for url in urls:
            modified = url.findtext("s:lastmod", default="", namespaces=namespace).strip()
            if modified:
                try:
                    if date.fromisoformat(modified) > date.today():
                        errors.append("Sitemap lastmod is in the future")
                except ValueError:
                    errors.append("Sitemap lastmod must be an ISO date")
    except ET.ParseError as exc:
        errors.append("Invalid sitemap XML: " + str(exc))

    if errors:
        for error in errors:
            print("SEO ERROR:", error, file=sys.stderr)
        return 1
    print("SEO checks passed: canonical, indexability, Open Graph, robots and sitemap.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
