#!/usr/bin/env python3
"""Check canonical pages, visible content, discovery files and structured data."""

from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse
import json
import re
import struct
import sys
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[2]
BASE = 'https://orchstring.com/'
BRAND_TITLE = 'OrchString | Enterprise AI Execution Platform'
BRAND_INTRO = 'orchstring is an AI-powered, enterprise-oriented execution platform designed to transform business objectives into coordinated, controlled, and verifiable workflows.'
VISIBLE_BRAND_INTRO = BRAND_INTRO.replace('orchstring', 'OrchString', 1)
HOMEPAGE_DESCRIPTION = 'orchstring is an enterprise AI execution platform designed to coordinate business operations, people, apps and workflows from objectives to verified outcomes.'


def normalized(text):
    return ' '.join(text.split())


class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonicals = []
        self.metadata = {}
        self.captures = []
        self.active = {}
        self.ids = []
        self.links = []
        self.assets = []
        self.icons = []
        self.faqs = []
        self.current_faq = None

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if data.get('id'):
            self.ids.append(data['id'])
        if tag == 'br':
            for capture in self.active.values():
                capture.append(' ')
        if tag in {'title', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6'} or (
            tag == 'script' and data.get('type') == 'application/ld+json'
        ):
            capture = []
            self.captures.append((tag, capture))
            self.active[tag] = capture
        if tag == 'article' and 'faq-answer' in data.get('class', '').split():
            self.current_faq = {}
        if tag == 'link' and data.get('rel') == 'icon':
            self.icons.append(data.get('href', ''))
        if tag == 'link' and data.get('rel') == 'canonical':
            self.canonicals.append(data.get('href', ''))
        if tag == 'meta':
            key = (data.get('name') or data.get('property') or '').lower()
            self.metadata[key] = data.get('content', '')
        if tag in {'a', 'use'} and data.get('href'):
            self.links.append(data['href'])
        if tag in {'img', 'script'} and data.get('src'):
            self.assets.append(data['src'])
        if tag == 'link' and data.get('rel') in {'stylesheet', 'icon', 'apple-touch-icon'}:
            self.assets.append(data.get('href', ''))

    def handle_endtag(self, tag):
        if self.current_faq is not None and tag in {'h2', 'p'}:
            self.current_faq[tag] = normalized(''.join(self.active.get(tag, [])))
        self.active.pop(tag, None)
        if tag == 'article' and self.current_faq is not None:
            self.faqs.append(self.current_faq)
            self.current_faq = None

    def handle_data(self, data):
        for capture in self.active.values():
            capture.append(data)

    def texts(self, tag):
        return [normalized(''.join(parts)) for name, parts in self.captures if name == tag]


def canonical_for(path):
    relative = path.relative_to(ROOT).as_posix()
    return BASE + (relative[:-len('index.html')] if relative != 'index.html' else '')


def main():
    errors = []
    pages = {}
    titles, descriptions = set(), set()
    for path in sorted(ROOT.rglob('index.html')):
        if any(part.startswith('.') for part in path.relative_to(ROOT).parts):
            continue
        parser = SiteParser()
        parser.feed(path.read_text(encoding='utf-8'))
        url = canonical_for(path)
        pages[url] = (path, parser)

    def fail(url, message):
        errors.append(url + ': ' + message)

    for url, (path, parser) in pages.items():
        title = parser.texts('title')
        description = parser.metadata.get('description', '')
        h1 = parser.texts('h1')
        if parser.icons != ['/assets/orchstring-o.svg']:
            fail(url, 'must use only the blue O SVG favicon')
        if parser.canonicals != [url]:
            fail(url, 'needs exactly one self-referencing canonical')
        if len(title) != 1 or not title[0] or title[0] in titles:
            fail(url, 'needs one unique, non-empty title')
        else:
            titles.add(title[0])
        if not description or description in descriptions:
            fail(url, 'needs a unique, non-empty description')
        descriptions.add(description)
        if len(h1) != 1 or not h1[0]:
            fail(url, 'needs exactly one descriptive h1')
        if parser.metadata.get('og:url') != url:
            fail(url, 'Open Graph URL must match canonical')
        for key in ('og:title', 'twitter:title'):
            if parser.metadata.get(key) != (title[0] if title else ''):
                fail(url, key + ' must match title')
        for key in ('og:description', 'twitter:description'):
            if parser.metadata.get(key) != description:
                fail(url, key + ' must match description')
        for key in ('og:image', 'twitter:image'):
            if parser.metadata.get(key) != BASE + 'assets/orchstring-social.png':
                fail(url, key + ' must use the published social preview')
        if not parser.metadata.get('og:image:alt') or not parser.metadata.get('twitter:image:alt'):
            fail(url, 'social preview needs descriptive alt text')
        robots = parser.metadata.get('robots', '').lower().replace(' ', '')
        if not robots or any(rule in robots for rule in ('noindex', 'nofollow', 'nosnippet')):
            fail(url, 'page must be indexable and snippet-eligible')
        if len(parser.ids) != len(set(parser.ids)):
            fail(url, 'duplicate element IDs')
        for text in parser.texts('p'):
            expected = 'OrchString' if text == VISIBLE_BRAND_INTRO else 'orchstring'
            text = text.replace('OrchString Console', '')
            if any(match[0] != expected for match in re.finditer(r'\borchstring\b', text, re.I)):
                fail(url, 'paragraph brand casing must match the display rules')
        try:
            scripts = parser.texts('script')
            if len(scripts) != 1:
                raise ValueError('needs one structured-data graph')
            graph = json.loads(scripts[0])['@graph']
            nodes = {node['@id']: node for node in graph}
            if len(nodes) != len(graph):
                raise ValueError('duplicate structured-data IDs')
            webpage = nodes[url + '#webpage']
            if webpage['url'] != url or webpage['name'] != title[0] or webpage['description'] != description:
                raise ValueError('page schema must match visible page metadata')
            if webpage.get('dateModified'):
                if date.fromisoformat(webpage['dateModified']) > date.today():
                    raise ValueError('modification date is in the future')
            if url == BASE:
                for kind, fragment in [('Organization', 'organization'), ('SoftwareApplication', 'orchstring'), ('WebSite', 'website')]:
                    node = nodes[BASE + '#' + fragment]
                    if node['@type'] != kind or node['name'] != 'OrchString' or node['url'] != BASE:
                        raise ValueError('brand entities must use the canonical brand identity')
                if title != [BRAND_TITLE] or description != HOMEPAGE_DESCRIPTION:
                    raise ValueError('homepage metadata must match brand positioning')
                if parser.texts('p').count(VISIBLE_BRAND_INTRO) < 2:
                    raise ValueError('visible introductions must match the official introduction')
            else:
                crumb = nodes[url + '#breadcrumb']['itemListElement']
                if crumb[0]['item'] != BASE or crumb[-1]['item'] != url:
                    raise ValueError('breadcrumb must connect home to the current page')
                if webpage['@type'] == 'FAQPage':
                    schema_faqs = [{'h2': normalized(item['name']), 'p': normalized(item['acceptedAnswer']['text'])} for item in webpage['mainEntity']]
                    if not parser.faqs or schema_faqs != parser.faqs:
                        raise ValueError('FAQ schema must exactly match visible questions and answers')
                else:
                    article = nodes[url + '#article']
                    if article['headline'] != h1[0] or article['description'] != description:
                        raise ValueError('article schema must match the visible article')
                    if article['mainEntityOfPage']['@id'] != url + '#webpage':
                        raise ValueError('article must reference its own canonical page')
        except (json.JSONDecodeError, KeyError, IndexError, TypeError, ValueError) as exc:
            fail(url, 'invalid structured data: ' + str(exc))

        for reference in parser.links + parser.assets:
            target = urlparse(urljoin(url, reference))
            if target.netloc != 'orchstring.com' or target.scheme not in {'http', 'https'}:
                continue
            target_url = BASE + target.path.lstrip('/')
            if target_url in pages:
                if target.fragment and unquote(target.fragment) not in pages[target_url][1].ids:
                    fail(url, 'broken internal fragment: ' + reference)
            else:
                resource = ROOT / unquote(target.path).lstrip('/')
                if not resource.is_file():
                    fail(url, 'missing local page or asset: ' + reference)

    robots = (ROOT / 'robots.txt').read_text(encoding='utf-8')
    if 'User-agent: *' not in robots or 'Allow: /' not in robots or 'Sitemap: ' + BASE + 'sitemap.xml' not in robots:
        errors.append('robots.txt must allow crawling and list the canonical sitemap')
    if (ROOT / 'CNAME').read_text(encoding='utf-8').strip() != 'orchstring.com':
        errors.append('CNAME must match the canonical host')
    try:
        namespace = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        sitemap = ET.parse(ROOT / 'sitemap.xml').getroot()
        entries = sitemap.findall('s:url', namespace)
        locations = [node.findtext('s:loc', '', namespace) for node in entries]
        if len(locations) != len(set(locations)) or set(locations) != set(pages):
            errors.append('sitemap must list every canonical page exactly once, without fragments')
        for node in entries:
            modified = node.findtext('s:lastmod', '', namespace)
            if not modified or date.fromisoformat(modified) > date.today():
                errors.append('sitemap lastmod must be a real, non-future ISO date')
    except (ET.ParseError, ValueError) as exc:
        errors.append('invalid sitemap: ' + str(exc))
    summary = (ROOT / 'llms.txt').read_text(encoding='utf-8')
    if any(url not in summary for url in pages):
        errors.append('llms.txt must reference all canonical pages')
    preview = (ROOT / 'assets/orchstring-social.png').read_bytes()
    if preview[:8] != b'\x89PNG\r\n\x1a\n' or struct.unpack('>II', preview[16:24]) != (1200, 630):
        errors.append('social preview must be a 1200 by 630 PNG')
    if errors:
        for error in errors:
            print('SEO ERROR:', error, file=sys.stderr)
        return 1
    print(f'SEO checks passed for {len(pages)} pages: metadata, brand casing, structured data, visible FAQ parity, local links, sitemap, robots, llms.txt and social preview.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
