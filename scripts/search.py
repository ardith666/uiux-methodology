#!/usr/bin/env python3
"""BM25 search engine for UI/UX design intelligence.

Searches across multiple domains: product types, UI styles, color palettes,
font pairings, landing patterns, UX guidelines, charts, GSAP presets.
Generates comprehensive design systems with reasoning.

Usage:
    python3 search.py "beauty spa wellness" --design-system -p "Project Name"
    python3 search.py "glassmorphism" --domain style
    python3 search.py "entertainment vibrant" --domain color --json
"""

import argparse
import csv
import json
import math
import os
import re
import sys
from pathlib import Path

# --- Config ---
K1 = 1.5
B = 0.75

STOP_WORDS = {
    'a', 'an', 'the', 'is', 'it', 'in', 'on', 'at', 'to', 'for', 'of',
    'and', 'or', 'but', 'not', 'with', 'as', 'by', 'from', 'that', 'this',
    'be', 'are', 'was', 'were', 'been', 'being', 'have', 'has', 'had',
    'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may',
    'might', 'can', 'shall', 'i', 'you', 'he', 'she', 'we', 'they',
    'my', 'your', 'his', 'her', 'our', 'their', 'what', 'which', 'who',
    'how', 'when', 'where', 'why', 'all', 'each', 'every', 'both',
    'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor',
    'too', 'very', 'just', 'about', 'above', 'after', 'again', 'also',
}

DATA_DIR = Path(__file__).resolve().parent.parent / 'data'


# --- Tokenization ---
def tokenize(text):
    if not text:
        return []
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s\-]', ' ', text)
    tokens = text.split()
    return [t for t in tokens if t and t not in STOP_WORDS and len(t) > 1]


# --- CSV Loading ---
def load_domain(domain):
    filepath = DATA_DIR / f'{domain}.csv'
    if not filepath.exists():
        return []
    rows = []
    with open(filepath, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def get_all_domains():
    return [
        'product-types', 'ui-styles', 'color-palettes', 'font-pairings',
        'landing-patterns', 'ux-guidelines', 'chart-types', 'gsap-presets',
    ]


# --- BM25 Search ---
def bm25_search(query_tokens, documents, field_weights=None):
    """Rank documents using BM25 scoring.

    Args:
        query_tokens: List of search tokens
        documents: List of dicts to search
        field_weights: Dict of field_name -> weight multiplier
    """
    if not query_tokens or not documents:
        return []

    if field_weights is None:
        field_weights = {}

    # Build corpus: combine all text fields per document
    doc_texts = []
    for doc in documents:
        parts = []
        for key, val in doc.items():
            if not key or key.startswith('_'):
                continue
            weight = field_weights.get(key, 1.0)
            text = str(val) if val else ''
            parts.extend([text] * max(1, int(weight * 10)))
        doc_texts.append(' '.join(parts))

    # Tokenize all docs
    doc_tokens_list = [tokenize(text) for text in doc_texts]
    n = len(documents)

    if n == 0:
        return []

    # Average doc length
    avg_dl = sum(len(dt) for dt in doc_tokens_list) / n if n else 1

    # Document frequency for each query term
    df = {}
    for token in query_tokens:
        df[token] = sum(1 for dt in doc_tokens_list if token in dt)

    # Score each document
    scores = []
    for i, doc in enumerate(documents):
        score = 0.0
        doc_len = len(doc_tokens_list[i])
        dl_norm = 1 - B + B * (doc_len / avg_dl) if avg_dl > 0 else 1

        for token in query_tokens:
            if token not in df:
                continue
            tf = doc_tokens_list[i].count(token)
            if tf == 0:
                continue

            idf = math.log((n - df[token] + 0.5) / (df[token] + 0.5) + 1)
            tf_norm = (tf * (K1 + 1)) / (tf + K1 * dl_norm)
            score += idf * tf_norm

        scores.append((score, i))

    scores.sort(reverse=True, key=lambda x: x[0])
    return [(documents[i], score) for score, i in scores if score > 0]


# --- Domain Search ---
DOMAIN_MAP = {
    'product': 'product-types',
    'product-types': 'product-types',
    'style': 'ui-styles',
    'ui-styles': 'ui-styles',
    'color': 'color-palettes',
    'color-palettes': 'color-palettes',
    'typography': 'font-pairings',
    'font': 'font-pairings',
    'font-pairings': 'font-pairings',
    'landing': 'landing-patterns',
    'landing-patterns': 'landing-patterns',
    'ux': 'ux-guidelines',
    'ux-guidelines': 'ux-guidelines',
    'chart': 'chart-types',
    'chart-types': 'chart-types',
    'gsap': 'gsap-presets',
    'animation': 'gsap-presets',
    'icons': 'ui-styles',
}


def search_domain(query, domain_name, max_results=5):
    """Search a single domain, return top results."""
    csv_domain = DOMAIN_MAP.get(domain_name, domain_name)
    docs = load_domain(csv_domain)
    if not docs:
        return []

    tokens = tokenize(query)
    results = bm25_search(tokens, docs)
    return results[:max_results]


def search_all(query, max_results=3):
    """Search all domains, return grouped results."""
    tokens = tokenize(query)
    results = {}
    for domain in get_all_domains():
        docs = load_domain(domain)
        if docs:
            hits = bm25_search(tokens, docs)
            results[domain] = hits[:max_results]
    return results


# --- Design System Generator ---
def generate_design_system(query, project_name=None, variance=5, motion=5, density=5):
    """Generate a complete design system from query.

    Searches product types, styles, colors, typography, landing patterns,
    and UX guidelines. Returns unified recommendations.
    """
    tokens = tokenize(query)

    # Search multiple domains
    product_results = bm25_search(tokens, load_domain('product-types'))
    style_results = bm25_search(tokens, load_domain('ui-styles'))
    color_results = bm25_search(tokens, load_domain('color-palettes'))
    type_results = bm25_search(tokens, load_domain('font-pairings'))
    landing_results = bm25_search(tokens, load_domain('landing-patterns'))
    ux_results = bm25_search(tokens, load_domain('ux-guidelines'))

    # Extract top recommendations
    product = product_results[0][0] if product_results else {}
    style = style_results[0][0] if style_results else {}
    color = color_results[0][0] if color_results else {}
    font = type_results[0][0] if type_results else {}
    landing = landing_results[0][0] if landing_results else {}

    # Apply design dials
    if variance <= 3:
        style_bias = 'minimal, centered, clean'
    elif variance >= 8:
        style_bias = 'bold, asymmetric, brutalist'
    else:
        style_bias = 'balanced, modern'

    if motion <= 3:
        motion_bias = 'subtle micro-interactions, 150ms'
    elif motion >= 8:
        motion_bias = 'complex choreography, GSAP ScrollTrigger, Flip'
    else:
        motion_bias = 'standard scroll/stagger, 200-300ms'

    if density <= 3:
        spacing_scale = '24-96px (spacious)'
    elif density >= 8:
        spacing_scale = '8-32px (dense/dashboard)'
    else:
        spacing_scale = '16-64px (standard)'

    # Collect anti-patterns
    anti_patterns = set()
    if product.get('anti_patterns'):
        anti_patterns.update(product['anti_patterns'].split(';'))
    if style.get('anti_patterns'):
        anti_patterns.update(style['anti_patterns'].split(';'))

    # Collect effects
    effects = set()
    if style.get('key_effects'):
        effects.update(style['key_effects'].split(';'))

    # UX guidelines (top 5)
    ux_top = [r[0] for r in ux_results[:5]]

    # Build output
    ds = {
        'project': project_name or 'Untitled',
        'query': query,
        'pattern': product.get('recommended_pattern', 'Hero-Centric'),
        'pattern_description': landing.get('description', ''),
        'sections': landing.get('sections', ''),
        'style': style.get('name', 'Minimalism'),
        'style_description': style.get('description', ''),
        'style_bias': style_bias,
        'best_for': style.get('best_for', ''),
        'colors': {
            'primary': color.get('primary', '#2563EB'),
            'secondary': color.get('secondary', '#7C3AED'),
            'accent': color.get('accent', '#F59E0B'),
            'background': color.get('background', '#FFFFFF'),
            'text': color.get('text', '#1F2937'),
            'mood': color.get('mood', ''),
        },
        'typography': {
            'heading': font.get('heading_font', 'Inter'),
            'body': font.get('body_font', 'Inter'),
            'mood': font.get('mood', ''),
            'google_fonts_url': font.get('google_fonts_url', ''),
        },
        'effects': list(effects),
        'anti_patterns': list(anti_patterns),
        'motion': motion_bias,
        'spacing': spacing_scale,
        'ux_guidelines': [
            {'title': g.get('title', ''), 'description': g.get('description', '')}
            for g in ux_top
        ],
    }

    # Persist if requested
    return ds


def format_ascii(ds):
    """Format design system as ASCII table."""
    lines = []
    sep = '+' + '-' * 68 + '+'

    lines.append(sep)
    lines.append(f"| TARGET: {ds['project']}" + ' ' * (59 - len(ds['project'])) + '|')
    lines.append(sep)
    lines.append(f"| PATTERN: {ds['pattern']}" + ' ' * (58 - len(ds['pattern'])) + '|')
    if ds.get('sections'):
        sections = ds['sections'][:57]
        lines.append(f"| Sections: {sections}" + ' ' * (57 - len(sections)) + '|')
    lines.append(sep)
    lines.append(f"| STYLE: {ds['style']}" + ' ' * (61 - len(ds['style'])) + '|')
    if ds.get('best_for'):
        bf = ds['best_for'][:57]
        lines.append(f"| Best For: {bf}" + ' ' * (57 - len(bf)) + '|')
    lines.append(f"| Variance Bias: {ds['style_bias']}" + ' ' * max(0, 53 - len(ds['style_bias'])) + '|')
    lines.append(sep)

    c = ds['colors']
    lines.append(f"| COLORS:")
    lines.append(f"| Primary: {c['primary']}" + ' ' * max(0, 58 - len(c['primary'])) + '|')
    lines.append(f"| Secondary: {c['secondary']}" + ' ' * max(0, 56 - len(c['secondary'])) + '|')
    lines.append(f"| Accent: {c['accent']}" + ' ' * max(0, 59 - len(c['accent'])) + '|')
    lines.append(f"| Background: {c['background']}" + ' ' * max(0, 55 - len(c['background'])) + '|')
    lines.append(f"| Text: {c['text']}" + ' ' * max(0, 61 - len(c['text'])) + '|')
    if c.get('mood'):
        mood = c['mood'][:57]
        lines.append(f"| Mood: {mood}" + ' ' * max(0, 57 - len(mood)) + '|')
    lines.append(sep)

    t = ds['typography']
    lines.append(f"| TYPOGRAPHY: {t['heading']} / {t['body']}" + ' ' * max(0, 43 - len(t['heading']) - len(t['body'])) + '|')
    if t.get('mood'):
        tm = t['mood'][:57]
        lines.append(f"| Mood: {tm}" + ' ' * max(0, 57 - len(tm)) + '|')
    if t.get('google_fonts_url'):
        url = t['google_fonts_url'][:57]
        lines.append(f"| Google Fonts: {url}" + ' ' * max(0, 54 - len(url)) + '|')
    lines.append(sep)

    if ds['effects']:
        lines.append(f"| KEY EFFECTS: {', '.join(ds['effects'][:5])}" + ' ' * max(0, 54 - len(', '.join(ds['effects'][:5]))) + '|')
    lines.append(f"| MOTION: {ds['motion']}" + ' ' * max(0, 59 - len(ds['motion'])) + '|')
    lines.append(f"| SPACING: {ds['spacing']}" + ' ' * max(0, 59 - len(ds['spacing'])) + '|')
    lines.append(sep)

    if ds['anti_patterns']:
        lines.append(f"| AVOID:")
        for ap in ds['anti_patterns'][:6]:
            ap_clean = ap.strip()[:57]
            lines.append(f"| - {ap_clean}" + ' ' * max(0, 58 - len(ap_clean)) + '|')
        lines.append(sep)

    if ds.get('ux_guidelines'):
        lines.append(f"| UX GUIDELINES (top 5):")
        for g in ds['ux_guidelines'][:5]:
            title = g['title'][:56]
            lines.append(f"| [{title}]" + ' ' * max(0, 57 - len(title)) + '|')
        lines.append(sep)

    return '\n'.join(lines)


def format_markdown(ds):
    """Format design system as Markdown."""
    lines = []
    lines.append(f"# Design System: {ds['project']}")
    lines.append(f"\n**Query:** {ds['query']}\n")

    lines.append(f"## Pattern: {ds['pattern']}")
    if ds.get('sections'):
        lines.append(f"**Sections:** {ds['sections']}")
    lines.append('')

    lines.append(f"## Style: {ds['style']}")
    if ds.get('style_description'):
        lines.append(f"{ds['style_description']}")
    if ds.get('best_for'):
        lines.append(f"**Best For:** {ds['best_for']}")
    lines.append(f"**Variance Bias:** {ds['style_bias']}")
    lines.append('')

    lines.append("## Colors")
    c = ds['colors']
    lines.append(f"- Primary: `{c['primary']}`")
    lines.append(f"- Secondary: `{c['secondary']}`")
    lines.append(f"- Accent: `{c['accent']}`")
    lines.append(f"- Background: `{c['background']}`")
    lines.append(f"- Text: `{c['text']}`")
    if c.get('mood'):
        lines.append(f"- Mood: {c['mood']}")
    lines.append('')

    lines.append("## Typography")
    t = ds['typography']
    lines.append(f"- Heading: **{t['heading']}**")
    lines.append(f"- Body: **{t['body']}**")
    if t.get('mood'):
        lines.append(f"- Mood: {t['mood']}")
    if t.get('google_fonts_url'):
        lines.append(f"- [Google Fonts]({t['google_fonts_url']})")
    lines.append('')

    if ds['effects']:
        lines.append("## Key Effects")
        for e in ds['effects']:
            lines.append(f"- {e.strip()}")
        lines.append('')

    lines.append(f"## Motion: {ds['motion']}")
    lines.append(f"## Spacing: {ds['spacing']}")
    lines.append('')

    if ds['anti_patterns']:
        lines.append("## Anti-Patterns to Avoid")
        for ap in ds['anti_patterns']:
            lines.append(f"- ❌ {ap.strip()}")
        lines.append('')

    if ds.get('ux_guidelines'):
        lines.append("## UX Guidelines")
        for g in ds['ux_guidelines']:
            lines.append(f"### {g['title']}")
            lines.append(f"{g['description']}")
            lines.append('')

    return '\n'.join(lines)


def persist_design_system(ds, output_dir, page=None, force=False):
    """Save design system to files."""
    slug = re.sub(r'[^a-z0-9]+', '-', ds['project'].lower()).strip('-')
    base = Path(output_dir) / 'design-system' / slug
    master_path = base / 'MASTER.md'

    if master_path.exists() and not force:
        print(f"Master already exists: {master_path}", file=sys.stderr)
        print("Use --force to overwrite.", file=sys.stderr)
        return str(master_path)

    base.mkdir(parents=True, exist_ok=True)
    (base / 'pages').mkdir(exist_ok=True)

    content = format_markdown(ds)
    master_path.write_text(content, encoding='utf-8')
    print(f"Saved: {master_path}", file=sys.stderr)

    if page:
        page_slug = re.sub(r'[^a-z0-9]+', '-', page.lower()).strip('-')
        page_path = base / 'pages' / f'{page_slug}.md'
        page_path.write_text(content, encoding='utf-8')
        print(f"Saved page: {page_path}", file=sys.stderr)

    return str(master_path)


# --- Main ---
def main():
    parser = argparse.ArgumentParser(description='UI/UX Design Intelligence Search')
    parser.add_argument('query', help='Search query')
    parser.add_argument('--domain', '-d', help='Search specific domain')
    parser.add_argument('--design-system', action='store_true',
                        help='Generate complete design system')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--format', '-f', choices=['ascii', 'markdown'],
                        default='ascii', help='Output format')
    parser.add_argument('-n', type=int, default=5, help='Max results per domain')
    parser.add_argument('--variance', type=int, default=5, choices=range(1, 11),
                        metavar='1-10', help='Style variance dial')
    parser.add_argument('--motion', type=int, default=5, choices=range(1, 11),
                        metavar='1-10', help='Motion complexity dial')
    parser.add_argument('--density', type=int, default=5, choices=range(1, 11),
                        metavar='1-10', help='Layout density dial')
    parser.add_argument('-p', '--project', help='Project name')
    parser.add_argument('--persist', action='store_true',
                        help='Save design system to file')
    parser.add_argument('--output-dir', default='.',
                        help='Output directory for persistence')
    parser.add_argument('--page', help='Page name for page-specific override')
    parser.add_argument('--force', action='store_true',
                        help='Overwrite existing files')

    args = parser.parse_args()

    if args.design_system:
        ds = generate_design_system(
            args.query, args.project,
            args.variance, args.motion, args.density
        )

        if args.persist:
            persist_design_system(ds, args.output_dir, args.page, args.force)

        if args.json:
            print(json.dumps(ds, indent=2))
        elif args.format == 'markdown':
            print(format_markdown(ds))
        else:
            print(format_ascii(ds))

    else:
        if args.domain:
            results = search_domain(args.query, args.domain, args.n)
            if args.json:
                output = [{'rank': i+1, 'score': round(score, 3), **doc}
                          for i, (doc, score) in enumerate(results)]
                print(json.dumps(output, indent=2))
            else:
                if not results:
                    print(f"No results for '{args.query}' in domain '{args.domain}'")
                for i, (doc, score) in enumerate(results):
                    name = doc.get('name', doc.get('title', 'Unknown'))
                    print(f"  {i+1}. [{score:.2f}] {name}")
                    desc = doc.get('description', doc.get('best_for', ''))
                    if desc:
                        print(f"     {desc[:80]}")
        else:
            results = search_all(args.query, args.n)
            if args.json:
                output = {}
                for domain, hits in results.items():
                    output[domain] = [
                        {'rank': i+1, 'score': round(s, 3), **d}
                        for i, (d, s) in enumerate(hits)
                    ]
                print(json.dumps(output, indent=2))
            else:
                for domain, hits in results.items():
                    if hits:
                        print(f"\n--- {domain} ---")
                        for i, (doc, score) in enumerate(hits):
                            name = doc.get('name', doc.get('title', 'Unknown'))
                            print(f"  {i+1}. [{score:.2f}] {name}")


if __name__ == '__main__':
    main()
