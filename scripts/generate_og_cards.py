#!/usr/bin/env python3
"""Render a social card for every post that has no `image:` of its own.

    python3 scripts/generate_og_cards.py      # needs rsvg-convert on PATH

Without this, those posts fall back to the site card (assets/og/og-default.png),
which is a big "Sebastian Schürmann" — every shared article link then previews
like the homepage. Each card carries the post's title, date and topics in the
same Carbon Gray 100 / IBM Plex look as og-default.svg; the author's name
stays, but as a small kicker instead of the headline.

Cards are written to assets/og/posts/<slug>.svg and rasterized to .png. Both
are build artifacts (git-ignored), regenerated in CI before the Jekyll build.
_includes/head.html points a post's og:image at its card only when the PNG
exists, so a failed rasterization degrades to the site card, not a 404.

Standard library only: the front matter is read with a few regexes instead of
PyYAML, which the CI runner does not guarantee.
"""
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path
from xml.sax.saxutils import escape

POSTS = Path("_posts")
TOPICS = Path("_data/topics.yml")
OUT = Path("assets/og/posts")

# Title area: from the text column (x=112) to just inside the right gutter.
TITLE_WIDTH = 960
MAX_LINES = 3
# (font size, line height) tried largest first; the first that fits wins.
TITLE_SIZES = [(80, 88), (68, 76), (58, 66), (50, 58)]

FILENAME = re.compile(r"^(\d{4})-(\d{2})-(\d{2})-(.+)\.md$")


def front_matter(text):
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return match.group(1) if match else ""


def scalar(fm, key):
    match = re.search(rf"^{key}:\s*(.*)$", fm, re.M)
    if not match:
        return None
    value = match.group(1).strip()
    if len(value) >= 2 and value[0] == value[-1] == '"':
        return re.sub(r'\\(["\\])', r"\1", value[1:-1])
    if len(value) >= 2 and value[0] == value[-1] == "'":
        return value[1:-1].replace("''", "'")
    return value


def tag_list(fm):
    match = re.search(r"^tags:\s*\[(.*)\]\s*$", fm, re.M)
    if not match:
        return []
    return [t.strip().strip("'\"") for t in match.group(1).split(",") if t.strip()]


def topic_names():
    names, current = {}, None
    for line in TOPICS.read_text(encoding="utf-8").splitlines():
        top = re.match(r"^([a-z0-9-]+):\s*$", line)
        if top:
            current = top.group(1)
            continue
        name = re.match(r"^\s+name:\s*(.+)$", line)
        if name and current:
            names[current] = name.group(1).strip().strip("'\"")
    return names


def char_width(ch):
    """Rough advance width of IBM Plex Sans Light, in em. Errs wide."""
    if ch == " ":
        return 0.25
    if ch in "iljI.,:;'!|()[]`\"":
        return 0.28
    if ch in "frt-/":
        return 0.36
    if ch in "mwMW@":
        return 0.86
    if ch.isupper() or ch.isdigit():
        return 0.64
    return 0.53


def text_width(text, size):
    return sum(char_width(c) for c in text) * size


def wrap(title, size):
    lines, line = [], ""
    for word in title.split():
        candidate = f"{line} {word}".strip()
        if line and text_width(candidate, size) > TITLE_WIDTH:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines


def layout(title):
    for size, leading in TITLE_SIZES:
        lines = wrap(title, size)
        if len(lines) <= MAX_LINES and all(text_width(l, size) <= TITLE_WIDTH for l in lines):
            return size, leading, lines
    # Nothing fits: smallest size, cut to MAX_LINES with an ellipsis.
    size, leading = TITLE_SIZES[-1]
    lines = wrap(title, size)
    if len(lines) > MAX_LINES:
        lines = lines[:MAX_LINES]
        lines[-1] = lines[-1].rstrip(" .,:;") + " …"
    return size, leading, lines


def card(title, day, topics):
    size, leading, lines = layout(title)
    # Centre the title block in the band between the rules at y=120 and y=500.
    block = size + leading * (len(lines) - 1)
    first_baseline = 120 + (380 - block) // 2 + round(size * 0.78)
    bar_top = first_baseline - round(size * 0.78) - 8
    bar_height = block + 16
    tspans = "\n    ".join(
        f'<text x="112" y="{first_baseline + i * leading}">{escape(l)}</text>'
        for i, l in enumerate(lines)
    )
    kicker = f"SEBASTIAN SCHÜRMANN — {day.strftime('%d %b %Y').upper()}"
    topic_line = " · ".join(topics[:3])
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
  <rect width="1200" height="630" fill="#161616"/>
  <g stroke="#393939" stroke-width="1">
    <line x1="80" y1="0" x2="80" y2="630"/>
    <line x1="0" y1="120" x2="1200" y2="120"/>
    <line x1="0" y1="500" x2="1200" y2="500"/>
    <line x1="1120" y1="0" x2="1120" y2="630"/>
  </g>
  <rect x="77" y="{bar_top}" width="6" height="{bar_height}" fill="#4589ff"/>
  <g font-family="'IBM Plex Mono', 'DejaVu Sans Mono', monospace" font-size="22" letter-spacing="4">
    <text x="112" y="72" fill="#8d8d8d">{escape(kicker)}</text>
  </g>
  <g font-family="'IBM Plex Sans', 'DejaVu Sans', system-ui, sans-serif" fill="#f4f4f4" font-size="{size}" font-weight="300" letter-spacing="-1">
    {tspans}
  </g>
  <g font-family="'IBM Plex Sans', 'DejaVu Sans', system-ui, sans-serif" font-size="28">
    <text x="112" y="570" fill="#4589ff">{escape(topic_line)}</text>
  </g>
</svg>
"""


def main():
    rsvg = shutil.which("rsvg-convert")
    if not rsvg:
        sys.exit("rsvg-convert not found (brew install librsvg / apt install librsvg2-bin)")
    names = topic_names()
    OUT.mkdir(parents=True, exist_ok=True)
    made = 0
    for path in sorted(POSTS.glob("*.md")):
        match = FILENAME.match(path.name)
        if not match:
            continue
        fm = front_matter(path.read_text(encoding="utf-8"))
        if scalar(fm, "image"):
            continue
        y, m, d, slug = match.groups()
        title = scalar(fm, "title") or slug.replace("-", " ")
        topics = [names.get(t, t) for t in tag_list(fm)]
        svg = OUT / f"{slug}.svg"
        svg.write_text(card(title, date(int(y), int(m), int(d)), topics), encoding="utf-8")
        subprocess.run([rsvg, "-w", "1200", "-h", "630", str(svg), "-o", str(svg.with_suffix(".png"))], check=True)
        made += 1
    print(f"{made} cards in {OUT}/")


if __name__ == "__main__":
    main()
