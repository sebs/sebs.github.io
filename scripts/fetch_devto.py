#!/usr/bin/env python3
"""Fetch the dev.to writing feed (RSS) and write it to _data/writing.yml.

Source: https://dev.to/feed/sebs — the canonical dev.to RSS feed for the user.
Output is JSON (a valid subset of YAML), so Jekyll parses it the same as the
committed seed file. On any failure we leave the existing seed in place, so the
Writing section never disappears from a deploy.

The homepage shows the most recent few (the template limits the list); we keep a
slightly larger set here as a buffer.
"""
import json
import sys
import urllib.request
import xml.etree.ElementTree as ET
from email.utils import parsedate_to_datetime

FEED_URL = "https://dev.to/feed/sebs"
OUT = "_data/writing.yml"
MAX_POSTS = 12


def _date(pubdate: str) -> str:
    """RFC-822 pubDate -> ISO yyyy-mm-dd (empty string if unparseable)."""
    if not pubdate:
        return ""
    try:
        return parsedate_to_datetime(pubdate).date().isoformat()
    except (TypeError, ValueError):
        return ""


def main() -> int:
    try:
        req = urllib.request.Request(FEED_URL, headers={"User-Agent": "sebs.github.io build"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            root = ET.fromstring(resp.read())
    except Exception as exc:  # noqa: BLE001 — never fail the build over the feed
        print(f"dev.to RSS fetch failed, keeping committed seed: {exc}", file=sys.stderr)
        return 0

    posts = []
    for item in root.iterfind(".//item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        if not title or not link:
            continue
        posts.append(
            {
                "title": title,
                "url": link,
                "date": _date(item.findtext("pubDate") or ""),
                "tags": [c.text.strip() for c in item.findall("category") if c.text],
            }
        )
        if len(posts) >= MAX_POSTS:
            break

    if not posts:
        print("dev.to RSS had no items, keeping committed seed", file=sys.stderr)
        return 0

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump({"posts": posts}, fh, ensure_ascii=False, indent=2)

    print(f"wrote {len(posts)} posts to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
