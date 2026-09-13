#!/usr/bin/env python3
"""Import the blog of dissident-trainings.de into _posts/.

    python3 scripts/import_dissident_trainings.py

The old site (a Jekyll/GitHub Pages site, 2012-2015) stays online for a while,
so every imported post carries its origin: `original_source` and
`original_url` drive the "Originally published on ..." note in the post
layout, and `canonical_url` points search engines at the original. Once
dissident-trainings.de is taken down, delete the `canonical_url:` lines from
these posts so they become canonical themselves.

Posts that are already on this blog (republished later from the Hexo blog, at
later dates) are detected by title and skipped; links to them, and between
the imported posts, are rewritten to their URLs here. Converting the article
HTML to markdown needs pandoc on the PATH.
"""
import html
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

BASE = "http://dissident-trainings.de"
SOURCE = "Dissident Trainings"
POSTS_DIR = Path("_posts")
ASSETS_DIR = Path("assets/posts")
USER_AGENT = "sebs.github.io blog import"

# Old path -> post already on this blog (same article, republished later).
ALREADY_HERE = {
    "/2014/11/19/Reasons-to-build-a-pairing-station.html": "/2016/11/19/Reasons-to-build-a-pairing-station/",
    "/2014/11/14/codereviews-and-pairprogramming.html": "/2019/04/10/Codereviews-and-Pairprogramming/",
    "/2014/10/29/survive-your-frontend-thoughts.html": "/2014/04/10/Surive-your-Frontend/",
    "/2014/10/06/how-to-pair.html": "/2017/07/23/Ideas-on-Pairprogramming/",
    "/2014/09/17/10-tips-for-the-xp-practice-sit-together.html": "/2017/03/23/10-TIPS-FOR-THE-XP-PRACTICE-SIT-TOGETHER-/",
}

LIST_ENTRY = re.compile(r"<h2>\s*<a href=\"?(/\d{4}/\d{2}/\d{2}/[^\">\s]+)\"?>(.*?)</a>\s*</h2>", re.S)
BODY_END = re.compile(r"</div>\s*<div class=\"(?:col-lg-4|row)\">")
YOUTUBE_FIGURE = re.compile(r"<figure class='BetterTube'[^>]*data-youtube-id='([\w-]+)'.*?</figure>", re.S)


def fetch(url, binary=False):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
    return data if binary else data.decode("utf-8")


def permalink_for(old_path):
    y, m, d, name = re.match(r"/(\d{4})/(\d{2})/(\d{2})/(.+)\.html$", old_path).groups()
    slug = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return f"{y}-{m}-{d}", slug, f"/{y}/{m}/{d}/{slug}/"


def extract_body(page):
    start = page.index("<h1>")
    title = html.unescape(re.search(r"<h1>(.*?)</h1>", page[start:], re.S).group(1)).strip()
    after_lead = page.index("</p>", page.index('class="lead"', start)) + len("</p>")
    end = BODY_END.search(page, after_lead).start()
    return title, page[after_lead:end]


def wayback(url):
    """The newest archived copy of `url`, or None. One polite retry on 429."""
    for attempt in range(2):
        try:
            data = json.loads(fetch(f"https://archive.org/wayback/available?url={urllib.parse.quote(url)}"))
            snap = data.get("archived_snapshots", {}).get("closest")
            if snap and snap.get("available"):
                return re.sub(r"/web/(\d+)/", r"/web/\1id_/", snap["url"])  # raw bytes, no toolbar
            return None
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt == 0:
                time.sleep(30)
                continue
            return None
    return None


def localise_images(body, old_path, slug):
    def swap(match):
        tag, src = match.group(0), html.unescape(match.group(1))
        absolute = urllib.parse.urljoin(BASE + old_path, src)
        name = re.sub(r"[^A-Za-z0-9._-]+", "-", Path(urllib.parse.urlparse(absolute).path).name)
        for candidate in (absolute, wayback(absolute.split("?")[0])):
            if not candidate:
                continue
            try:
                data = fetch(candidate, binary=True)
            except (urllib.error.URLError, TimeoutError):
                continue
            dest = ASSETS_DIR / slug / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            return tag.replace(match.group(1), f"/{dest.as_posix()}")
        print(f"  ! image gone from the original and the archive, dropped: {absolute}", file=sys.stderr)
        return ""

    return re.sub(r"<img[^>]*?\bsrc=[\"']([^\"']+)[\"'][^>]*>", swap, body)


def rewrite_links(body, new_urls):
    def swap(match):
        href = html.unescape(match.group(2))
        on_old_site = re.match(r"https?://(www\.)?dissident-trainings\.de/", href)
        path = urllib.parse.urlparse(href).path if on_old_site else href
        if path in new_urls:
            return f"{match.group(1)}{new_urls[path]}{match.group(3)}"
        if href.startswith("/"):
            return f"{match.group(1)}{BASE}{href}{match.group(3)}"
        return match.group(0)

    return re.sub(r"(<a\b[^>]*?\bhref=[\"'])([^\"']+)([\"'])", swap, body)


def to_markdown(body):
    result = subprocess.run(
        ["pandoc", "--from=html", "--to=gfm-raw_html", "--wrap=none"],
        input=body, capture_output=True, text=True, check=True,
    )
    return result.stdout.strip() + "\n"


def describe(markdown):
    for block in markdown.split("\n\n"):
        text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", block)
        text = re.sub(r"[*_`#>]", "", text).strip()
        if len(text) > 40 and not text.startswith(("-", "|")):
            text = " ".join(text.split())
            return text if len(text) <= 160 else text[:157].rsplit(" ", 1)[0] + "…"
    return ""


def main():
    listing = fetch(f"{BASE}/blog.html")
    entries = list(dict.fromkeys(m.group(1) for m in LIST_ENTRY.finditer(listing)))
    new_urls = dict(ALREADY_HERE)
    for old_path in entries:
        new_urls.setdefault(old_path, permalink_for(old_path)[2])

    imported = 0
    for old_path in entries:
        if old_path in ALREADY_HERE:
            print(f"skip (already here): {old_path}")
            continue
        date, slug, permalink = permalink_for(old_path)
        original_url = BASE + old_path
        title, body = extract_body(fetch(original_url))
        time.sleep(1)

        body = YOUTUBE_FIGURE.sub(
            lambda m: f'<p><a href="https://www.youtube.com/watch?v={m.group(1)}">Watch the video on YouTube</a></p>', body)
        body = localise_images(body, old_path, slug)
        markdown = to_markdown(rewrite_links(body, new_urls))

        front = [
            "---",
            "layout: post",
            f"title: {json.dumps(title, ensure_ascii=False)}",
            f"date: {date}",
            f'permalink: "{permalink}"',
            f"description: {json.dumps(describe(markdown), ensure_ascii=False)}",
            "tags: []",
            "og_type: article",
            f"original_source: {json.dumps(SOURCE)}",
            f'original_url: "{original_url}"',
            f'canonical_url: "{original_url}"',
            "render_with_liquid: false",
            "---",
            "",
        ]
        (POSTS_DIR / f"{date}-{slug}.md").write_text("\n".join(front) + markdown, encoding="utf-8")
        imported += 1
        print(f"post  {date} {slug}")

    print(f"imported {imported} posts, skipped {len(ALREADY_HERE)} already on the blog")


if __name__ == "__main__":
    raise SystemExit(main())
