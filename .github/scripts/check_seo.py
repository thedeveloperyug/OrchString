#!/usr/bin/env python3
"""Validate branding and SEO for the single-page OrchString website."""

from datetime import date
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
CANONICAL = "https://orchstring.com/"
SITEMAP = CANONICAL + "sitemap.xml"
BRAND_TITLE = "OrchString | Enterprise AI Execution"
BRAND_INTRO = "orchstring is an AI-powered, enterprise-oriented execution platform designed to transform business objectives into coordinated, controlled, and verifiable workflows."
VISIBLE_BRAND_INTRO = BRAND_INTRO.replace("orchstring", "OrchString", 1)


class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonicals = []
        self.metadata = {}
        self.in_head = False
        self.captures = []
        self.active = {}

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if tag in {"title", "p", "h1", "h2", "h3", "h4", "h5", "h6"} or (
            tag == "script" and data.get("type") == "application/ld+json"
        ):
            capture = []
            self.captures.append((tag, capture))
            self.active[tag] = capture
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
        self.active.pop(tag, None)
        if tag == "head":
            self.in_head = False

    def handle_data(self, data):
        for capture in self.active.values():
            capture.append(data)


def main():
    errors = []
    parser = SiteParser()
    homepage = (ROOT / "index.html").read_text(encoding="utf-8")
    parser.feed(homepage)

    if parser.canonicals != [CANONICAL]:
        errors.append("index.html needs exactly one canonical pointing to " + CANONICAL)
    if parser.metadata.get("og:url") != CANONICAL:
        errors.append("Open Graph URL must match the canonical URL")
    for key in ("description", "og:description", "twitter:description"):
        if parser.metadata.get(key) != BRAND_INTRO:
            errors.append(key + " must match the official orchstring introduction")
    for key in ("application-name", "og:site_name"):
        if parser.metadata.get(key) != "OrchString":
            errors.append(key + " must use the OrchString display name")
    for key in ("og:title", "twitter:title"):
        if parser.metadata.get(key) != BRAND_TITLE:
            errors.append(key + " must match the homepage title")
    captures = [(tag, "".join(parts)) for tag, parts in parser.captures]
    if [text for tag, text in captures if tag == "title"] != [BRAND_TITLE]:
        errors.append("Homepage title must use the OrchString display name")
    if not any(tag == "h1" and "OrchString" in text for tag, text in captures):
        errors.append("Homepage h1 must include OrchString")
    paragraphs = [text for tag, text in captures if tag == "p"]
    if paragraphs.count(VISIBLE_BRAND_INTRO) < 2:
        errors.append("Official introduction must appear in the hero and introduction sections")
    for tag, text in captures:
        if tag == "script":
            continue
        expected = "orchstring" if tag == "p" and text != VISIBLE_BRAND_INTRO else "OrchString"
        if any(match[0] != expected for match in re.finditer(r"\borchstring\b", text, re.I)):
            errors.append(tag + " must use the " + expected + " spelling")
    schemas = [text for tag, text in captures if tag == "script"]
    try:
        graph = json.loads(schemas[0])["@graph"] if len(schemas) == 1 else []
        if {node["@type"] for node in graph} != {"Organization", "SoftwareApplication", "WebSite", "WebPage"}:
            errors.append("Structured data must describe the organization, application, website and page")
        for node in graph:
            expected_name = BRAND_TITLE if node["@type"] == "WebPage" else "OrchString"
            if node.get("name") != expected_name or node.get("description") != BRAND_INTRO:
                errors.append("Structured data must use the current brand name and introduction")
            if node.get("url") != CANONICAL or not node.get("@id", "").startswith(CANONICAL + "#"):
                errors.append("Structured data URLs must use the canonical domain")
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        errors.append("Invalid structured data: " + str(exc))
    if "github.com/" in homepage:
        errors.append("Public website must not redirect visitors to GitHub repositories")
    if 'id="contact"' not in homepage or 'href="mailto:rishabh@neytraintelligence.com' not in homepage:
        errors.append("Sales contact section and direct email link are required")
    robots_meta = parser.metadata.get("robots", "").lower().replace(" ", "")
    if "noindex" in robots_meta or "nofollow" in robots_meta:
        errors.append("Homepage must not be marked noindex/nofollow")

    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    if "User-agent: *" not in robots or "Allow: /" not in robots:
        errors.append("robots.txt must allow crawlers")
    if "Sitemap: " + SITEMAP not in robots:
        errors.append("robots.txt sitemap must point to the primary .com domain")
    if (ROOT / "CNAME").read_text(encoding="utf-8").strip() != "orchstring.com":
        errors.append("GitHub Pages CNAME must match the canonical domain")

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
    print("Branding and SEO checks passed: casing, metadata, structured data, canonical, indexability, robots, sitemap and CNAME.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
