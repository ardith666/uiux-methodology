#!/usr/bin/env python3
"""Validate that code uses design tokens instead of hardcoded values.

Usage:
    python3 validate-tokens.py --dir src/
"""

import argparse
import re
import sys
from pathlib import Path

HARDCODED_HEX = re.compile(r'(?<!\w)#[0-9A-Fa-f]{3,8}(?!\w)')
HARDCODED_RGB = re.compile(r'rgba?\(\s*\d+\s*,\s*\d+\s*,\s*\d+')
SKIP_PATTERNS = [
    re.compile(r'node_modules/'),
    re.compile(r'\.min\.css'),
    re.compile(r'design-tokens\.css'),
]


def scan_file(filepath):
    """Scan a file for hardcoded color values."""
    issues = []
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception:
        return issues

    for i, line in enumerate(content.split('\n'), 1):
        stripped = line.strip()
        if stripped.startswith('//') or stripped.startswith('*') or stripped.startswith('/*'):
            continue

        for match in HARDCODED_HEX.finditer(line):
            hex_val = match.group()
            # Skip common patterns
            if hex_val in ('#fff', '#FFF', '#ffffff', '#FFFFFF', '#000', '#000000'):
                continue
            issues.append({'file': str(filepath), 'line': i, 'value': hex_val})

        for match in HARDCODED_RGB.finditer(line):
            issues.append({'file': str(filepath), 'line': i, 'value': match.group()})

    return issues


def main():
    parser = argparse.ArgumentParser(description='Validate token usage in code')
    parser.add_argument('--dir', '-d', required=True, help='Directory to scan')
    parser.add_argument('--ext', default='.css,.scss,.tsx,.jsx,.vue,.svelte',
                        help='File extensions to scan')
    args = parser.parse_args()

    scan_dir = Path(args.dir)
    if not scan_dir.exists():
        print(f"Directory not found: {scan_dir}", file=sys.stderr)
        sys.exit(1)

    extensions = set(args.ext.split(','))
    all_issues = []

    for ext in extensions:
        for filepath in scan_dir.rglob(f'*{ext}'):
            if any(skip.search(str(filepath)) for skip in SKIP_PATTERNS):
                continue
            issues = scan_file(filepath)
            all_issues.extend(issues)

    if all_issues:
        print(f"Found {len(all_issues)} hardcoded values:\n")
        for issue in all_issues:
            print(f"  {issue['file']}:{issue['line']} — {issue['value']}")
        sys.exit(1)
    else:
        print("No hardcoded values found. All good!")
        sys.exit(0)


if __name__ == '__main__':
    main()
