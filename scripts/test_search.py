#!/usr/bin/env python3
"""Self-check for uiux-methodology search engine. Run: python3 scripts/test_search.py"""
import csv
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from search import (AVAILABLE_STACKS, detect_domain, search_domain,
                    search_stack, generate_design_system, tokenize)

DATA = Path(__file__).resolve().parent.parent / 'data'
failures = []

def check(label, cond):
    if not cond:
        failures.append(label)
        print(f'FAIL: {label}')
    else:
        print(f'ok:   {label}')

# 1. Synonym normalization
check('synonym dark-mode -> dark', 'dark' in tokenize('dark-mode glassmorphism'))
check('synonym e-commerce -> ecommerce', 'ecommerce' in tokenize('e-commerce landing'))
check('synonym a11y -> accessibility', 'accessibility' in tokenize('a11y contrast'))

# 2. Auto domain detection
check('detect style', detect_domain('glassmorphism dark ui') == 'style')
check('detect framer', detect_domain('framer motion stagger') == 'framer')
check('detect chart', detect_domain('trend over time chart') == 'chart')
check('detect fonts', detect_domain('find monospace font') == 'fonts')
check('detect fallback style', detect_domain('zzz qqq') == 'style')

# 3. Domain search returns ranked results
for domain, q in [('style', 'glassmorphism dark'), ('icons', 'navigation menu'),
                  ('fonts', 'monospace technical'), ('ux', 'accessibility contrast'),
                  ('gsap', 'scroll reveal'), ('framer', 'hero stagger')]:
    res = search_domain(q, domain, 3)
    check(f'search {domain} has results', len(res) > 0)
    if res:
        check(f'search {domain} sorted desc', res[0][1] >= res[-1][1])

# 4. Stack search
check('stacks available', 'react' in AVAILABLE_STACKS)
res = search_stack('layout state', 'react', 3)
check('stack react results', len(res) > 0)
check('stack react fields', all(r[0].get('code_good') for r in res))

# 5. Design system generator (all dials)
for motion in (1, 5, 10):
    ds = generate_design_system('fintech dashboard', 'Test', 5, motion, 5)
    check(f'design system motion={motion}', 'motion' in ds and ds['motion'])

# 6. Data integrity: every csv parses, no empty required cols
required = {'name': ['ui-styles.csv', 'color-palettes.csv', 'chart-types.csv',
                     'gsap-presets.csv', 'icons.csv', 'ui-reasoning.csv',
                     'app-interface.csv', 'google-fonts.csv',
                     'framer-motion-presets.csv'],
            'heading_font': ['font-pairings.csv']}
for col, files in required.items():
    for f in files:
        rows = list(csv.DictReader(open(DATA / f, encoding='utf-8')))
        check(f'{f} rows + {col} filled',
              len(rows) > 0 and all(r.get(col, '').strip() for r in rows))

# 7. Every stack file parses with expected columns
for s in AVAILABLE_STACKS:
    rows = list(csv.DictReader(open(DATA / 'stacks' / f'{s}.csv', encoding='utf-8')))
    check(f'stack {s} parses', len(rows) > 0)

print()
if failures:
    print(f'{len(failures)} FAILURES')
    sys.exit(1)
print('ALL CHECKS PASSED')
