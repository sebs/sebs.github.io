#!/usr/bin/env python3
"""One-shot migration: legacy Hexo post HTML -> Jekyll markdown in _posts/.

Each old post is a full Hexo page. The article body lives between the
`<!-- Main Post Content -->` and `<!-- Tags Bottom -->` comments. Code blocks
are Hexo "highlight" line-number tables; we rebuild them as fenced code blocks
(pandoc would otherwise drag the gutter line-numbers into the output). The rest
of the body is handed to pandoc for a faithful HTML->GFM conversion.

Original URLs are preserved verbatim via an explicit `permalink:` so every
existing inbound link and archive reference keeps resolving.

Run once from the repo root:  python3 scripts/extract_posts.py
"""
from __future__ import annotations

import html
import json
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
LEGACY_YEARS = ["2014", "2016", "2017", "2018", "2019"]
OUT = ROOT / "_posts"

TAG_RE = re.compile(r'href="/tags/([^"/]+)/"')
TITLE_RE = re.compile(r'<meta property="og:title" content="([^"]*)"')
FIGURE_RE = re.compile(
    r'<figure class="highlight(?P<cls>[^"]*)">.*?'
    r'<td class="code"><pre>(?P<code>.*?)</pre></td>.*?</figure>',
    re.DOTALL,
)
HEADERLINK_RE = re.compile(r'<a href="#[^"]*" class="headerlink"[^>]*></a>')
TAG_TOKEN_RE = re.compile(r"<[^>]+>")
# Drop target/rel/class attrs on <a> so pandoc emits clean [text](url) markdown
# instead of falling back to raw HTML anchors.
ANCHOR_ATTR_RE = re.compile(r'(<a\s+href="[^"]*")[^>]*(>)')
FIRST_P_RE = re.compile(r"<p>(.*?)</p>", re.DOTALL)
FIGURE_BLOCK_RE = re.compile(r"<figure>.*?</figure>", re.DOTALL)
TITLE_H1_RE = re.compile(r"<h1[^>]*>.*?</h1>", re.DOTALL)
BYLINE_RE = re.compile(r"<p>\s*Sebastian Schürmann\s*•[^<]*</p>", re.DOTALL)


def strip_tags(s: str) -> str:
    return TAG_TOKEN_RE.sub("", s)


def clean_body(body: str) -> str:
    """Drop legacy chrome that the post layout now renders itself or that is
    pure noise: empty cover-image figures (the cover was never set, so only an
    orphan <figcaption> survives), the title repeated as an <h1>, and the
    "Author • Date" byline."""
    body = FIGURE_BLOCK_RE.sub(lambda m: "" if "<img" not in m.group(0) else m.group(0), body)
    body = TITLE_H1_RE.sub("", body, count=1)
    body = BYLINE_RE.sub("", body)
    return body


def make_description(body: str) -> str:
    """A clean meta description from the first prose paragraph of the body."""
    for m in FIRST_P_RE.finditer(body):
        text = re.sub(r"\s+", " ", html.unescape(strip_tags(m.group(1)))).strip()
        if len(text) < 30:
            continue
        if len(text) <= 160:
            return text
        cut = text[:157].rsplit(" ", 1)[0]
        return cut + "…"
    return ""


def figure_to_fence(m: re.Match) -> tuple[str, str]:
    """Return (placeholder_token, fenced_markdown) for one Hexo code figure."""
    cls = m.group("cls").strip()
    lang = cls.split()[0] if cls else ""
    code_html = m.group("code")
    lines = code_html.split("<br>")
    code_lines = [html.unescape(strip_tags(ln)) for ln in lines]
    while code_lines and code_lines[-1].strip() == "":
        code_lines.pop()
    code = "\n".join(code_lines)
    fence = f"```{lang}\n{code}\n```"
    return fence


def extract_body(full: str) -> str:
    start = full.index("<!-- Main Post Content -->") + len("<!-- Main Post Content -->")
    end = full.index("<!-- Tags Bottom -->", start)
    # the body sometimes closes with a trailing comment block before Tags Bottom
    body = full[start:end]
    return body


def convert(path: pathlib.Path) -> dict:
    full = path.read_text(encoding="utf-8")
    rel = path.relative_to(ROOT).parent  # e.g. 2019/01/04/Monorepos-with-Lerna
    parts = rel.parts
    year, month, day = parts[0], parts[1], parts[2]
    dirslug = parts[3]
    permalink = "/" + "/".join(parts) + "/"

    title = html.unescape(TITLE_RE.search(full).group(1)) if TITLE_RE.search(full) else dirslug

    body = clean_body(extract_body(full))
    desc = make_description(body)

    # Tags: first occurrence block is enough; de-dupe preserving order.
    tags: list[str] = []
    for t in TAG_RE.findall(full):
        t = html.unescape(t)
        if t not in tags:
            tags.append(t)

    # Pull code figures out, replace with neutral placeholder paragraphs so
    # pandoc leaves them alone, then splice the fenced blocks back afterwards.
    fences: list[str] = []

    def _stash(m: re.Match) -> str:
        fences.append(figure_to_fence(m))
        return f"<p>CODEFENCEPLACEHOLDER{len(fences) - 1}ENDPLACEHOLDER</p>"

    body = FIGURE_RE.sub(_stash, body)
    body = HEADERLINK_RE.sub("", body)
    body = ANCHOR_ATTR_RE.sub(r"\1\2", body)

    md = subprocess.run(
        ["pandoc", "--from=html", "--to=gfm", "--wrap=none"],
        input=body,
        capture_output=True,
        text=True,
        check=True,
    ).stdout

    for i, fence in enumerate(fences):
        md = md.replace(f"CODEFENCEPLACEHOLDER{i}ENDPLACEHOLDER", fence)

    md = re.sub(r"\n{3,}", "\n\n", md).strip() + "\n"

    fm_slug = re.sub(r"[^a-z0-9]+", "-", dirslug.lower()).strip("-")
    out_name = f"{year}-{month}-{day}-{fm_slug}.md"

    front = [
        "---",
        "layout: post",
        f"title: {json.dumps(title, ensure_ascii=False)}",
        f"date: {year}-{month}-{day}",
        f"permalink: {json.dumps(permalink, ensure_ascii=False)}",
    ]
    if desc:
        front.append(f"description: {json.dumps(desc, ensure_ascii=False)}")
    if tags:
        front.append("tags: [" + ", ".join(tags) + "]")
    front += ["og_type: article", "---", ""]

    (OUT / out_name).write_text("\n".join(front) + md, encoding="utf-8")
    return {"file": out_name, "permalink": permalink, "title": title, "tags": tags}


def main() -> int:
    OUT.mkdir(exist_ok=True)
    posts = []
    for year in LEGACY_YEARS:
        for path in sorted((ROOT / year).rglob("index.html")):
            posts.append(convert(path))
    for p in posts:
        print(f"  {p['file']:<55} -> {p['permalink']}  {p['tags']}")
    print(f"\nWrote {len(posts)} posts to _posts/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
