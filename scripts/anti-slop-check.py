#!/usr/bin/env python3
"""
anti-slop-check.py — Automated AI slop pattern scanner for frontend code.

Scans CSS, SCSS, JSX, TSX, Vue, Svelte, and HTML files for telltale signs
of AI-generated frontend boilerplate ("slop").

Checks are grouped by severity:
  P0 — Must fix (blocks ship)
  P1 — Should fix (polish)
  P2 — Nice to fix (refinement)

Exit code:
  0  No P0 violations
  1  One or more P0 violations

Usage:
  python3 anti-slop-check.py [paths...]
  python3 anti-slop-check.py --profile minimal ./src
  python3 anti-slop-check.py --profile strict ./src --format json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Callable

# ─── File extensions to scan ────────────────────────────────────────────────

SCAN_EXTENSIONS = {".css", ".scss", ".jsx", ".tsx", ".vue", ".svelte", ".html"}

# ─── Directories to skip ────────────────────────────────────────────────────

SKIP_DIRS = {"node_modules", ".git", "dist", "build", "__pycache__", ".next", "out"}

# ─── Profiles ────────────────────────────────────────────────────────────────

PROFILES = {
    "minimal": {"P0"},
    "standard": {"P0", "P1"},
    "strict": {"P0", "P1", "P2"},
}

# ─── Severity constants ─────────────────────────────────────────────────────

P0 = "P0"
P1 = "P1"
P2 = "P2"


# ─── Data structures ─────────────────────────────────────────────────────────


@dataclass
class Violation:
    severity: str
    check_id: int
    check_name: str
    file: str
    line: int
    column: int
    matched: str
    detail: str = ""


@dataclass
class CheckResult:
    check_id: int
    check_name: str
    severity: str
    violations: list[Violation] = field(default_factory=list)


# ─── Helpers ──────────────────────────────────────────────────────────────────


def should_skip(dirpath: str, parts: tuple[str, ...]) -> bool:
    """True if any path component is a skip directory."""
    return any(p in SKIP_DIRS for p in parts)


def collect_files(paths: list[str]) -> list[Path]:
    """Walk directories and return files matching SCAN_EXTENSIONS."""
    files: list[Path] = []
    for target in paths:
        p = Path(target).resolve()
        if p.is_file():
            if p.suffix in SCAN_EXTENSIONS:
                files.append(p)
        elif p.is_dir():
            for dirpath, dirnames, filenames in os.walk(p):
                # Prune skip dirs in-place so os.walk won't descend
                dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
                for fname in filenames:
                    fp = Path(dirpath) / fname
                    if fp.suffix in SCAN_EXTENSIONS:
                        files.append(fp)
    return sorted(files)


def _line_col(source: str, offset: int) -> tuple[int, int]:
    """Return (1-based line, 1-based column) for a string offset."""
    line = source.count("\n", 0, offset) + 1
    col = offset - source.rfind("\n", 0, offset)
    return line, col


def _read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def _iter_lines(source: str):
    """Yield (line_number, line_text) 1-indexed."""
    for i, line in enumerate(source.splitlines(), 1):
        yield i, line


# ─── P0 checks ───────────────────────────────────────────────────────────────

# Default Tailwind indigo / purple hex codes
INDIGO_HEXES = [
    "#6366f1", "#4f46e5", "#4338ca", "#3730a3",
    "#8b5cf6", "#7c3aed", "#a855f7",
]

INDIGO_PATTERN = re.compile(
    r"(?i)(?:^|[\"';,\s(])(" + "|".join(INDIGO_HEXES) + r")(?:[\s\"';,)]|$)",
)

# Two-stop hero gradients — linear-gradient combos
HERO_GRADIENT_PATTERN = re.compile(
    r"linear-gradient\s*\([^)]*\b(?:purple|blue|cyan|indigo|pink|violet|fuchsia)\b[^)]*\)",
    re.IGNORECASE,
)

# Gradient color pairs that are sloppily common
SLOP_GRADIENT_COLORS = {
    frozenset({"purple", "blue"}),
    frozenset({"blue", "cyan"}),
    frozenset({"indigo", "pink"}),
    frozenset({"blue", "indigo"}),
    frozenset({"violet", "pink"}),
    frozenset({"purple", "blue", "cyan"}),
    frozenset({"blue", "purple", "pink"}),
}

# Emoji unicode ranges (common emoji blocks)
EMOJI_PATTERN = re.compile(
    r"[\U0001F300-\U0001F9FF\u2600-\u26FF\u2700-\u27BF\u200D\uFE0F"
    r"\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF"
    r"\U00002702-\U000027B0\U0000FE00-\U0000FE0F"
    r"\U0000200D\U00002764-\U0000FE0F]"
)

# Sans-serif display fonts on headings
HEADING_FONT_PATTERN = re.compile(
    r"(?:h[1-6]|<\s*(?:h[1-6])\b)[^{]*font-family\s*:\s*"
    r"(?:['\"]?)\s*(?:Inter|Roboto|system-ui|Poppins|Outfit|Plus\s+Jakarta)",
    re.IGNORECASE,
)

# Also catch in CSS: heading + font-family near each other (broad heuristic)
CSS_HEADING_FONT = re.compile(
    r"h[1-6][^{]*\{[^}]*font-family\s*:\s*['\"]?(?:Inter|Roboto|system-ui|Poppins|Outfit|Plus Jakarta Sans)",
    re.IGNORECASE | re.DOTALL,
)

# Rounded card with left border
BORDER_LEFT_RADIUS_PATTERN = re.compile(
    r"border-left[^;]*;[^}]*border-radius", re.IGNORECASE | re.DOTALL,
)
RADIUS_BORDER_LEFT_PATTERN = re.compile(
    r"border-radius[^;]*;[^}]*border-left", re.IGNORECASE | re.DOTALL,
)

# Invented metrics
INVENTED_METRICS_PATTERN = re.compile(
    r"\b\d+[xX×]\s*(?:faster|more|better|speed|performance)"
    r"|\b(?:99\.9|99\.99|99\.999)\s*%"
    r"|\b\d+[xX×]\s+more\b",
    re.IGNORECASE,
)

# Filler / placeholder copy
FILLER_COPY_PATTERNS = [
    re.compile(r"lorem\s+ipsum", re.IGNORECASE),
    re.compile(r"\bfeature\s+(?:one|two|three|four|five)\b", re.IGNORECASE),
    re.compile(r"\bplaceholder\s+text\b", re.IGNORECASE),
    re.compile(r"your\s+(?:product|app|business|brand)\s+here", re.IGNORECASE),
    re.compile(r"dummy\s+(?:text|content|data)\b", re.IGNORECASE),
]


def check_p0_indigo_hex(path: Path, source: str) -> list[Violation]:
    """P0-1: Default Tailwind indigo hex codes."""
    vs = []
    for m in INDIGO_PATTERN.finditer(source):
        line, col = _line_col(source, m.start())
        vs.append(Violation(P0, 1, "Default Tailwind Indigo", str(path), line, col, m.group(0).strip()))
    return vs


def check_p0_hero_gradient(path: Path, source: str) -> list[Violation]:
    """P0-2: Two-stop hero gradient (purple→blue etc.)."""
    vs = []
    for m in HERO_GRADIENT_PATTERN.finditer(source):
        text = m.group(0)
        # Extract color words from the match
        words = re.findall(r"(?:purple|blue|cyan|indigo|pink|violet|fuchsia)", text, re.IGNORECASE)
        pair = frozenset(w.lower() for w in words)
        if pair in SLOP_GRADIENT_COLORS:
            line, col = _line_col(source, m.start())
            vs.append(Violation(P0, 2, "Hero Gradient", str(path), line, col, text.strip()))
    return vs


def check_p0_emoji_icons(path: Path, source: str) -> list[Violation]:
    """P0-3: Emoji used as feature icons in class-name contexts."""
    vs = []
    for i, line_text in _iter_lines(source):
        # Look for emoji in likely icon contexts: inside JSX text, alt text, aria-label, title
        icon_contexts = re.finditer(
            r"""(?:aria-label|alt|title|icon)\s*=\s*["'][^"']*(?:[\U0001F300-\U0001F9FF\u2600-\u27BF\u2702-\u27B0])[^"']*["']""",
            line_text,
        )
        for m in icon_contexts:
            vs.append(Violation(P0, 3, "Emoji as Icon", str(path), i, m.start() + 1, m.group(0).strip()))

        # Also catch bare emoji in JSX template content that look like feature icons
        bare_emoji = re.finditer(
            r"(?:^|\s)([\U0001F300-\U0001F9FF\u2600-\u27BF]{1,4})\s*(?:</|<br|\n|$)",
            line_text,
        )
        for m in bare_emoji:
            emoji = m.group(1)
            # Skip if it's in a comment
            stripped = line_text.lstrip()
            if stripped.startswith("//") or stripped.startswith("*") or stripped.startswith("<!--"):
                continue
            vs.append(Violation(P0, 3, "Emoji as Icon", str(path), i, m.start() + 1, emoji))
    return vs


def check_p0_sans_display(path: Path, source: str) -> list[Violation]:
    """P0-4: Sans-serif display text on headings."""
    vs = []
    for m in CSS_HEADING_FONT.finditer(source):
        line, col = _line_col(source, m.start())
        snippet = source[m.start():m.end()][:120]
        vs.append(Violation(P0, 4, "Sans Display Heading", str(path), line, col, snippet))
    return vs


def check_p0_border_left_radius(path: Path, source: str) -> list[Violation]:
    """P0-5: Rounded card with left-border accent."""
    vs = []
    # Check line-by-line with lookahead for multi-line combos
    for m in BORDER_LEFT_RADIUS_PATTERN.finditer(source):
        line, col = _line_col(source, m.start())
        vs.append(Violation(P0, 5, "Border-Left + Radius", str(path), line, col, m.group(0).strip()[:80]))
    for m in RADIUS_BORDER_LEFT_PATTERN.finditer(source):
        line, col = _line_col(source, m.start())
        vs.append(Violation(P0, 5, "Radius + Border-Left", str(path), line, col, m.group(0).strip()[:80]))
    return vs


def check_p0_invented_metrics(path: Path, source: str) -> list[Violation]:
    """P0-6: Invented metrics ("10× faster", "99.9%")."""
    vs = []
    for m in INVENTED_METRICS_PATTERN.finditer(source):
        line, col = _line_col(source, m.start())
        vs.append(Violation(P0, 6, "Invented Metric", str(path), line, col, m.group(0).strip()))
    return vs


def check_p0_filler_copy(path: Path, source: str) -> list[Violation]:
    """P0-7: Filler / placeholder copy."""
    vs = []
    for pat in FILLER_COPY_PATTERNS:
        for m in pat.finditer(source):
            line, col = _line_col(source, m.start())
            vs.append(Violation(P0, 7, "Filler Copy", str(path), line, col, m.group(0).strip()))
    return vs


# ─── P1 checks ───────────────────────────────────────────────────────────────

def check_p1_template_skeleton(path: Path, source: str) -> list[Violation]:
    """P1-8: Template skeleton — standard Hero→Features→Pricing→FAQ→CTA sections."""
    # Heuristic: if a single file contains enough of these section markers, flag it
    lower = source.lower()
    section_keywords = ["hero", "feature", "pricing", "faq", "frequently asked", "call to action", "cta"]
    found = [kw for kw in section_keywords if kw in lower]
    if len(found) >= 4:
        vs = [Violation(
            P1, 8, "Template Skeleton", str(path), 1, 0,
            f"Found {len(found)} skeleton sections: {', '.join(found)}",
        )]
        return vs
    return []


def check_p1_placeholder_cdns(path: Path, source: str) -> list[Violation]:
    """P1-9: External placeholder CDNs (unsplash, placehold.co, etc.)."""
    placeholder_patterns = [
        re.compile(r"unsplash\.com", re.IGNORECASE),
        re.compile(r"placehold\.co", re.IGNORECASE),
        re.compile(r"placekitten\.com", re.IGNORECASE),
        re.compile(r"picsum\.photos", re.IGNORECASE),
    ]
    vs = []
    for pat in placeholder_patterns:
        for m in pat.finditer(source):
            line, col = _line_col(source, m.start())
            vs.append(Violation(P1, 9, "Placeholder CDN", str(path), line, col, m.group(0)))
    return vs


def check_p1_hex_outside_root(path: Path, source: str) -> list[Violation]:
    """P1-10: Hardcoded hex colors outside :root blocks."""
    hex_re = re.compile(r"#[0-9a-fA-F]{3,8}\b")
    vs = []

    # Parse CSS :root blocks to exclude them
    root_ranges = []
    for m in re.finditer(r":root\s*\{([^}]*)\}", source, re.DOTALL):
        root_ranges.append((m.start(), m.end()))

    def in_root(pos: int) -> bool:
        return any(start <= pos <= end for start, end in root_ranges)

    for m in hex_re.finditer(source):
        if in_root(m.start()):
            continue
        # Skip if it's a hex in a Tailwind class (e.g., bg-[#fff])
        # or inside a comment
        before = source[max(0, m.start() - 40):m.start()]
        if "//" in before.split("\n")[-1] or "/*" in before:
            continue
        line, col = _line_col(source, m.start())
        vs.append(Violation(P1, 10, "Hex Outside :root", str(path), line, col, m.group(0)))
    return vs


def check_p1_accent_overuse(path: Path, source: str) -> list[Violation]:
    """P1-11: Overuse of var(--accent)."""
    matches = re.findall(r"var\s*\(\s*--accent\s*\)", source)
    if len(matches) >= 8:
        first = source.find("var(--accent)")
        line, col = _line_col(source, first) if first >= 0 else (1, 0)
        return [Violation(
            P1, 11, "Accent Overuse", str(path), line, col,
            f"var(--accent) used {len(matches)} times",
        )]
    return []


# ─── P2 checks ───────────────────────────────────────────────────────────────

def check_p2_blob_wave_svg(path: Path, source: str) -> list[Violation]:
    """P1-12: Decorative blob/wave SVG patterns."""
    vs = []
    blob_patterns = [
        re.compile(r"<svg[^>]*(?:blob|wave|curve|squiggle|organic)[^>]*>", re.IGNORECASE),
        re.compile(r"d\s*=\s*[\"'][Mm]\s*[\d.]+[\s,]+[\d.]+.*?(?:C\s*[\d.,\s]+){2,}", re.DOTALL),
        re.compile(r"(?:feTurbulence|feDisplacementMap|turbulence)", re.IGNORECASE),
    ]
    for pat in blob_patterns:
        for m in pat.finditer(source):
            line, col = _line_col(source, m.start())
            snippet = m.group(0)[:80]
            vs.append(Violation(P2, 12, "Blob/Wave SVG", str(path), line, col, snippet))
    return vs


def check_p2_symmetric_layout(path: Path, source: str) -> list[Violation]:
    """P1-13: Perfect symmetric layout (heuristic)."""
    # Heuristic: file contains grid/flex with identical gap on both axes,
    # AND symmetric padding patterns, AND no asymmetric positioning
    if not source.strip():
        return []

    symmetry_signals = 0
    lower = source.lower()

    # Equal gap values
    if re.search(r"gap\s*:\s*(\d+(?:px|rem|em))(?:\s+\1\s*;|\s*;)", lower):
        symmetry_signals += 1

    # symmetric grid-template
    if "grid-template-columns" in lower and re.search(
        r"repeat\s*\(\s*(?:auto-fit|auto-fill)\s*,\s*minmax\s*\(\s*\d+(?:px|rem)\s*,\s*1fr\s*\)\s*\)",
        lower,
    ):
        symmetry_signals += 1

    # Very uniform padding
    padding_matches = re.findall(r"padding\s*:\s*(\d+(?:px|rem|em))\s+(\d+(?:px|rem|em))\s+(\d+(?:px|rem|em))\s+(\d+(?:px|rem|em))", lower)
    for p_match in padding_matches:
        if len(set(p_match)) == 1:
            symmetry_signals += 1
            break

    # Same margin auto on both sides
    if re.search(r"margin\s*:\s*(?:\d+\w*\s+)?auto\s+(?:\d+\w*\s+)?auto", lower):
        symmetry_signals += 1

    if symmetry_signals >= 3:
        return [Violation(P2, 13, "Symmetric Layout", str(path), 1, 0, f"{symmetry_signals} symmetry signals detected")]
    return []


# ─── Check registry ──────────────────────────────────────────────────────────

ALL_CHECKS: dict[int, tuple[str, str, Callable]] = {
    1:  ("Default Tailwind Indigo", P0, check_p0_indigo_hex),
    2:  ("Hero Gradient",          P0, check_p0_hero_gradient),
    3:  ("Emoji as Icon",          P0, check_p0_emoji_icons),
    4:  ("Sans Display Heading",   P0, check_p0_sans_display),
    5:  ("Border-Left + Radius",   P0, check_p0_border_left_radius),
    6:  ("Invented Metric",        P0, check_p0_invented_metrics),
    7:  ("Filler Copy",            P0, check_p0_filler_copy),
    8:  ("Template Skeleton",      P1, check_p1_template_skeleton),
    9:  ("Placeholder CDN",        P1, check_p1_placeholder_cdns),
    10: ("Hex Outside :root",      P1, check_p1_hex_outside_root),
    11: ("Accent Overuse",         P1, check_p1_accent_overuse),
    12: ("Blob/Wave SVG",          P2, check_p2_blob_wave_svg),
    13: ("Symmetric Layout",       P2, check_p2_symmetric_layout),
}


# ─── Output formatting ──────────────────────────────────────────────────────


def format_text(results: dict[int, CheckResult], profile: str) -> str:
    """Plain-text report."""
    lines = []
    active = PROFILES[profile]
    total_violations = 0
    p0_count = 0

    for check_id in sorted(results):
        cr = results[check_id]
        if cr.severity not in active:
            continue
        if not cr.violations:
            continue
        total_violations += len(cr.violations)
        p0_count += sum(1 for v in cr.violations if v.severity == P0)

        lines.append(f"\n[{cr.severity}] {cr.check_name} ({len(cr.violations)} violations)")
        lines.append("─" * 60)
        for v in cr.violations[:20]:  # cap per check for readability
            lines.append(f"  {v.file}:{v.line}:{v.column}  {v.matched!r}")
            if v.detail:
                lines.append(f"    └─ {v.detail}")
        if len(cr.violations) > 20:
            lines.append(f"  ... and {len(cr.violations) - 20} more")

    lines.insert(0, f"anti-slop-check  |  profile: {profile}  |  total: {total_violations} violations")
    lines.insert(1, "─" * 60)

    if p0_count == 0:
        lines.append(f"\n✅  No P0 violations. Ship it.")
    else:
        lines.append(f"\n🚨  {p0_count} P0 violation(s) — fix before shipping.")

    return "\n".join(lines)


def format_json(results: dict[int, CheckResult], profile: str) -> str:
    """JSON report."""
    active = PROFILES[profile]
    output = {
        "profile": profile,
        "summary": {"P0": 0, "P1": 0, "P2": 0, "total": 0},
        "checks": [],
    }

    for check_id in sorted(results):
        cr = results[check_id]
        if cr.severity not in active:
            continue
        entry = {
            "id": cr.check_id,
            "name": cr.check_name,
            "severity": cr.severity,
            "count": len(cr.violations),
            "violations": [asdict(v) for v in cr.violations],
        }
        output["checks"].append(entry)
        output["summary"][cr.severity] += len(cr.violations)
        output["summary"]["total"] += len(cr.violations)

    return json.dumps(output, indent=2)


# ─── Main ─────────────────────────────────────────────────────────────────────


def run_checks(
    paths: list[str],
    profile: str = "standard",
    fmt: str = "text",
) -> int:
    """Run anti-slop checks. Returns exit code (0 = no P0)."""
    active = PROFILES[profile]
    files = collect_files(paths)

    if not files:
        print("No matching files found.")
        return 0

    results: dict[int, CheckResult] = {
        cid: CheckResult(check_id=cid, check_name=name, severity=sev)
        for cid, (name, sev, _) in ALL_CHECKS.items()
    }

    for fpath in files:
        source = _read(fpath)
        if not source:
            continue
        for cid, (name, sev, fn) in ALL_CHECKS.items():
            if sev not in active:
                continue
            violations = fn(fpath, source)
            results[cid].violations.extend(violations)

    if fmt == "json":
        print(format_json(results, profile))
    else:
        print(format_text(results, profile))

    p0_total = sum(
        len(cr.violations) for cr in results.values()
        if cr.severity == P0
    )
    return 1 if p0_total > 0 else 0


def main():
    parser = argparse.ArgumentParser(
        description="Anti-AI-slop checker for frontend code.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=["."],
        help="Directories or files to scan (default: current directory)",
    )
    parser.add_argument(
        "--profile", "-p",
        choices=list(PROFILES.keys()),
        default="standard",
        help="Check profile: minimal (P0), standard (P0+P1), strict (P0+P1+P2) [default: standard]",
    )
    parser.add_argument(
        "--format", "-f",
        choices=["text", "json"],
        default="text",
        help="Output format [default: text]",
    )
    args = parser.parse_args()
    exit_code = run_checks(args.paths, args.profile, args.format)
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
