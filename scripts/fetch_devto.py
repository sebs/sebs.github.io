#!/usr/bin/env python3
"""Fetch the dev.to writing feed and write it to _data/writing.yml.

Output is JSON (a valid subset of YAML), so Jekyll parses it the same as the
committed seed file. On any failure we leave the existing seed in place, so the
Writing section never disappears from a deploy.
"""
import json
import sys
import urllib.request

USERNAME = "sebs"
URL = f"https://dev.to/api/articles?username={USERNAME}&per_page=12"
OUT = "_data/writing.yml"


def main() -> int:
    try:
        req = urllib.request.Request(URL, headers={"User-Agent": "sebs.github.io build"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            articles = json.load(resp)
    except Exception as exc:  # noqa: BLE001 — never fail the build over the feed
        print(f"dev.to fetch failed, keeping committed seed: {exc}", file=sys.stderr)
        return 0

    posts = [
        {
            "title": a.get("title", ""),
            "url": a.get("url", ""),
            "date": (a.get("published_at") or "")[:10],
            "reactions": a.get("public_reactions_count", 0),
            "comments": a.get("comments_count", 0),
            "tags": a.get("tag_list", []),
        }
        for a in articles
    ]

    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump({"posts": posts}, fh, ensure_ascii=False, indent=2)

    print(f"wrote {len(posts)} posts to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
