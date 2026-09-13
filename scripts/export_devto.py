#!/usr/bin/env python3
"""Export every dev.to article into the site as Jekyll posts.

Part of moving the writing off dev.to: published articles become
`_posts/YYYY-MM-DD-<slug>.md`, unpublished ones `_drafts/<slug>.md`, in the
same shape as the posts migrated from Hexo (explicit `/YYYY/MM/DD/<slug>/`
permalink, description, tags). Every image — inline and cover — is downloaded
into `assets/posts/<slug>/`, so no post depends on dev.to's CDN afterwards.

    DEVTO_API_KEY=... python3 scripts/export_devto.py

The key comes from the environment only (dev.to -> Settings -> Extensions ->
DEV Community API Keys); it is never written anywhere. Re-running overwrites
the generated posts and skips images that are already on disk. This is a
one-off migration tool, not part of the deploy — scripts/fetch_devto.py is.

What changes on the way in:
  - The front matter dev.to keeps inside `body_markdown` (v1 editor) is
    stripped; its `series` survives into the post's front matter.
  - dev.to Liquid tags (`{% embed %}`, `{% youtube %}`, ...) have no Jekyll
    equivalent and would break the build, so they become plain links. The
    posts are written with `render_with_liquid: false`, so a `{{` or `{%` in a
    code sample renders as text.
  - Boosts (dev.to reposts of someone else's article) are skipped.
"""
import json
import mimetypes
import os
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.request
from datetime import datetime
from pathlib import Path
from urllib.parse import unquote, urlparse

API = "https://dev.to/api/articles/me/all"
POSTS_DIR = Path("_posts")
DRAFTS_DIR = Path("_drafts")
ASSETS_DIR = Path("assets/posts")
USER_AGENT = "sebs.github.io dev.to export"
MAX_SLUG_LEN = 80

IMAGE_MD = re.compile(r'(!\[[^\]]*\]\()(\S+?)((?:\s+"[^"]*")?\))')
IMAGE_HTML = re.compile(r'(<img\b[^>]*?\bsrc=")([^"]+)(")', re.IGNORECASE)
LIQUID_TAG = re.compile(r"\{%\s*(\w+)\s+(.*?)\s*%\}")
LEADING_FRONT_MATTER = re.compile(r"\A\s*---\n(.*?)\n---[ \t]*\n", re.DOTALL)


def request(url, api_key=None):
    headers = {"User-Agent": USER_AGENT}
    if api_key:
        headers["api-key"] = api_key
        headers["Accept"] = "application/vnd.forem.api-v1+json"
    return urllib.request.Request(url, headers=headers)


def fetch_articles(api_key):
    articles, page = [], 1
    while True:
        with urllib.request.urlopen(request(f"{API}?per_page=1000&page={page}", api_key), timeout=60) as resp:
            batch = json.load(resp)
        if not batch:
            return articles
        articles.extend(batch)
        page += 1


def slugify(title):
    for src, dst in (("ä", "ae"), ("ö", "oe"), ("ü", "ue"), ("Ä", "Ae"), ("Ö", "Oe"), ("Ü", "Ue"), ("ß", "ss")):
        title = title.replace(src, dst)
    title = re.sub(r"['’]", "", title)  # "it's" -> "its", not "it-s"
    ascii_title = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_title.lower()).strip("-")
    if len(slug) > MAX_SLUG_LEN:
        slug = slug[:MAX_SLUG_LEN].rsplit("-", 1)[0]
    return slug


def split_front_matter(body):
    """The body without dev.to's embedded front matter, and that block's `series`."""
    match = LEADING_FRONT_MATTER.match(body)
    if not match:
        return body, None
    series = None
    for line in match.group(1).splitlines():
        key, _, value = line.partition(":")
        if key.strip() == "series" and value.strip():
            series = value.strip()
    return body[match.end():].lstrip("\n"), series


def replace_liquid(body):
    def link(match):
        tag, args = match.group(1), match.group(2).split()
        url = next((a for a in args if a.startswith(("http://", "https://"))), None)
        if tag == "youtube" and args:
            url = f"https://www.youtube.com/watch?v={args[0]}"
        if not url:
            print(f"  ! dropped unsupported Liquid tag: {match.group(0)}", file=sys.stderr)
            return ""
        return f"<{url}>"

    return LIQUID_TAG.sub(link, body)


def original_image_url(url):
    """dev.to serves covers through a resizing proxy; fetch the upload behind it."""
    match = re.search(r"\.dev\.to/dynamic/image/[^/]*/(.+)$", url)
    if match:
        inner = unquote(match.group(1))
        if inner.startswith(("http://", "https://")):
            return inner
    return url


def download(url, dest_dir, stem=None):
    """Save `url` under `dest_dir`; returns the file name. Skips existing files."""
    source = original_image_url(url)
    name = Path(unquote(urlparse(source).path)).name
    if stem:
        name = stem + Path(name).suffix
    dest_dir.mkdir(parents=True, exist_ok=True)
    existing = [p for p in dest_dir.iterdir() if p.stem == Path(name).stem] if name else []
    if existing:
        return existing[0].name

    for attempt in range(3):
        try:
            with urllib.request.urlopen(request(source), timeout=60) as resp:
                data = resp.read()
                ctype = resp.headers.get_content_type()
            break
        except urllib.error.URLError:
            if attempt == 2:
                raise
            time.sleep(2 * (attempt + 1))

    if not Path(name).suffix:
        name = (name or "image") + (mimetypes.guess_extension(ctype) or ".png")
    (dest_dir / name).write_bytes(data)
    return name


def localise_images(body, slug):
    asset_dir = ASSETS_DIR / slug
    counter = {"n": 0}

    def swap(match):
        url = match.group(2)
        if not url.startswith(("http://", "https://")):
            return match.group(0)
        counter["n"] += 1
        stem = None if Path(urlparse(url).path).suffix else f"image-{counter['n']}"
        try:
            name = download(url, asset_dir, stem)
        except Exception as exc:  # noqa: BLE001 — keep the remote URL rather than lose the post
            print(f"  ! kept remote image {url}: {exc}", file=sys.stderr)
            return match.group(0)
        return f"{match.group(1)}/{asset_dir.as_posix()}/{name}{match.group(3)}"

    body = IMAGE_MD.sub(swap, body)
    return IMAGE_HTML.sub(swap, body)


def yaml_str(value):
    # JSON string escapes are valid in YAML double-quoted scalars.
    return json.dumps(value or "", ensure_ascii=False)


def render(article, slug, published_at, body, series, cover):
    lines = [
        "---",
        "layout: post",
        f"title: {yaml_str(article['title'])}",
    ]
    if published_at:
        lines.append(f"date: {published_at:%Y-%m-%d %H:%M:%S} +0000")
        lines.append(f'permalink: "/{published_at:%Y/%m/%d}/{slug}/"')
    lines += [
        f"description: {yaml_str((article.get('description') or '').strip())}",
        f"tags: [{', '.join(article.get('tag_list') or [])}]",
        "og_type: article",
    ]
    if cover:
        lines.append(f"image: {yaml_str(cover)}")
    if series:
        lines.append(f"series: {yaml_str(series)}")
    lines += [
        f"devto_url: {yaml_str(article.get('url'))}",
        "render_with_liquid: false",
        "---",
        "",
    ]
    return "\n".join(lines) + body.rstrip() + "\n"


def main():
    api_key = os.environ.get("DEVTO_API_KEY")
    if not api_key:
        print("Set DEVTO_API_KEY (dev.to -> Settings -> Extensions).", file=sys.stderr)
        return 1

    articles = fetch_articles(api_key)
    print(f"fetched {len(articles)} articles")
    written = {"posts": 0, "drafts": 0, "skipped": 0}
    seen = set()

    for article in sorted(articles, key=lambda a: a.get("published_at") or ""):
        if article["title"].strip() == "[Boost]":
            print(f"skip boost: {article['url']}")
            written["skipped"] += 1
            continue

        published_at = None
        if article.get("published") and article.get("published_at"):
            published_at = datetime.fromisoformat(article["published_at"].replace("Z", "+00:00"))

        slug = slugify(article["title"]) or f"post-{article['id']}"
        key = (published_at and published_at.date(), slug)
        if key in seen:
            slug = f"{slug}-{article['id']}"
        seen.add(key)

        print(f"{'post ' if published_at else 'draft'} {slug}")
        body, series = split_front_matter(article.get("body_markdown") or "")
        body = localise_images(replace_liquid(body), slug)

        cover = None
        if article.get("cover_image"):
            try:
                cover = f"/{(ASSETS_DIR / slug).as_posix()}/{download(article['cover_image'], ASSETS_DIR / slug, 'cover')}"
            except Exception as exc:  # noqa: BLE001
                print(f"  ! cover not downloaded: {exc}", file=sys.stderr)

        if published_at:
            POSTS_DIR.mkdir(exist_ok=True)
            path = POSTS_DIR / f"{published_at:%Y-%m-%d}-{slug}.md"
            written["posts"] += 1
        else:
            DRAFTS_DIR.mkdir(exist_ok=True)
            path = DRAFTS_DIR / f"{slug}.md"
            written["drafts"] += 1
        path.write_text(render(article, slug, published_at, body, series, cover), encoding="utf-8")

    print(f"wrote {written['posts']} posts, {written['drafts']} drafts; skipped {written['skipped']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
