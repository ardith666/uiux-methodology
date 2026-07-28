#!/usr/bin/env python3
"""Extract brand context from brand-guidelines.md for prompt injection.

Usage:
    python3 inject-brand-context.py [--json] [--brand-file PATH]
"""

import argparse
import json
import re
import sys
from pathlib import Path


def parse_brand_file(filepath):
    """Parse brand-guidelines.md into structured context."""
    if not filepath.exists():
        return None

    content = filepath.read_text(encoding='utf-8')
    context = {
        'brand_name': '',
        'colors': {},
        'typography': {},
        'voice': {},
        'messaging': {},
    }

    # Extract brand name from first heading
    name_match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
    if name_match:
        context['brand_name'] = name_match.group(1).strip()

    # Extract colors
    color_section = re.search(r'## Colors?\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
    if color_section:
        colors = {}
        for line in color_section.group(1).split('\n'):
            match = re.match(r'[-*]\s*\*?\*?(\w[\w\s]*?)\*?\*?\s*[:=]\s*`?([#A-Fa-f0-9]+|[\w\s]+)`?', line)
            if match:
                colors[match.group(1).strip().lower()] = match.group(2).strip()
        context['colors'] = colors

    # Extract typography
    type_section = re.search(r'## Typography\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
    if type_section:
        typography = {}
        for line in type_section.group(1).split('\n'):
            heading_match = re.search(r'[Hh]eading[s]?\s*[:=]\s*`?([^`\n]+)`?', line)
            if heading_match:
                typography['heading'] = heading_match.group(1).strip()
            body_match = re.search(r'[Bb]ody\s*[:=]\s*`?([^`\n]+)`?', line)
            if body_match:
                typography['body'] = body_match.group(1).strip()
        context['typography'] = typography

    # Extract voice/tone
    voice_section = re.search(r'## Voice\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL | re.IGNORECASE)
    if voice_section:
        voice_lines = [l.strip().lstrip('-* ') for l in voice_section.group(1).split('\n') if l.strip()]
        context['voice'] = {'tone': voice_lines[:5]}

    return context


def main():
    parser = argparse.ArgumentParser(description='Extract brand context')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--brand-file', default='docs/brand-guidelines.md',
                        help='Path to brand guidelines file')
    args = parser.parse_args()

    brand_path = Path(args.brand_file)
    context = parse_brand_file(brand_path)

    if context is None:
        print(f"Brand file not found: {brand_path}", file=sys.stderr)
        print("Create docs/brand-guidelines.md with your brand guidelines.", file=sys.stderr)
        sys.exit(1)

    if args.json:
        print(json.dumps(context, indent=2))
    else:
        print(f"Brand: {context['brand_name']}")
        if context['colors']:
            print("\nColors:")
            for name, value in context['colors'].items():
                print(f"  {name}: {value}")
        if context['typography']:
            print(f"\nTypography: {context['typography'].get('heading', 'N/A')} / {context['typography'].get('body', 'N/A')}")
        if context['voice']:
            print(f"\nVoice: {', '.join(context['voice'].get('tone', []))}")


if __name__ == '__main__':
    main()
