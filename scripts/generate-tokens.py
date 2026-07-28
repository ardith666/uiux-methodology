#!/usr/bin/env python3
"""Generate CSS design tokens from JSON config.

Usage:
    python3 generate-tokens.py --config tokens.json -o tokens.css
"""

import argparse
import json
import sys
from pathlib import Path


def flatten_tokens(obj, prefix=''):
    """Flatten nested token object into CSS variable pairs."""
    tokens = {}
    for key, value in obj.items():
        full_key = f'{prefix}{key}' if prefix else key
        if isinstance(value, dict):
            tokens.update(flatten_tokens(value, f'{full_key}-'))
        else:
            tokens[full_key] = value
    return tokens


def generate_css(tokens):
    """Generate CSS from flat token dict."""
    lines = [':root {']
    for key, value in sorted(tokens.items()):
        css_var = f'--{key}'
        lines.append(f'  {css_var}: {value};')
    lines.append('}')
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Generate CSS tokens from JSON')
    parser.add_argument('--config', '-c', required=True, help='JSON token config')
    parser.add_argument('-o', '--output', help='Output CSS file')
    args = parser.parse_args()

    config_path = Path(args.config)
    if not config_path.exists():
        print(f"Config not found: {config_path}", file=sys.stderr)
        sys.exit(1)

    with open(config_path, 'r') as f:
        config = json.load(f)

    tokens = {}
    for key, value in config.items():
        if isinstance(value, dict):
            tokens.update(flatten_tokens(value, f'{key}-'))
        else:
            tokens[key] = value

    css = generate_css(tokens)

    if args.output:
        Path(args.output).write_text(css, encoding='utf-8')
        print(f"Written: {args.output}", file=sys.stderr)
    else:
        print(css)


if __name__ == '__main__':
    main()
