#!/usr/bin/env python3
"""Shrink post images and cut social-card images.

    python3 scripts/optimize_images.py        # needs Pillow with WebP support

Run it after adding a post with images; it is idempotent.

1. Every PNG/JPEG under assets/posts/ is scaled to at most MAX_WIDTH pixels
   wide and re-encoded as WebP. The WebP replaces the original only when it is
   smaller, and every reference in _posts/ and _drafts/ is rewritten to match.
   GIFs are left alone (animation), as are files already small enough.
2. A post whose front-matter `image:` is a local cover gets og.jpg next to it:
   the cover centre-cropped to 1200×630, the size the page head announces for
   og:image. `image:` then points at og.jpg and the full-size cover is removed
   — nothing on the site shows covers except as social cards.
"""
import re
import sys
from pathlib import Path

from PIL import Image, ImageOps

ASSETS = Path("assets/posts")
TEXT_DIRS = [Path("_posts"), Path("_drafts")]
MAX_WIDTH = 1600
WEBP_QUALITY = 82
OG_SIZE = (1200, 630)
OG_NAME = "og.jpg"
SMALL_ENOUGH = 150_000  # bytes; below this a narrow image is not worth re-encoding


def markdown_files():
    return [p for d in TEXT_DIRS if d.is_dir() for p in sorted(d.glob("*.md"))]


def rewrite_references(old, new):
    old_url, new_url = f"/{old.as_posix()}", f"/{new.as_posix()}"
    for path in markdown_files():
        text = path.read_text(encoding="utf-8")
        if old_url in text:
            path.write_text(text.replace(old_url, new_url), encoding="utf-8")


def open_image(path):
    image = ImageOps.exif_transpose(Image.open(path))
    if image.mode not in ("RGB", "RGBA"):
        image = image.convert("RGBA" if "transparency" in image.info or image.mode in ("LA", "P") else "RGB")
    return image


def make_og_images():
    made = 0
    for post in markdown_files():
        text = post.read_text(encoding="utf-8")
        match = re.search(r'^image: "?/(assets/posts/[^"\n]+)"?$', text, re.M)
        if not match:
            continue
        cover = Path(match.group(1))
        if cover.name == OG_NAME or not cover.exists():
            continue
        og = cover.with_name(OG_NAME)
        card = ImageOps.fit(open_image(cover).convert("RGB"), OG_SIZE, Image.LANCZOS, centering=(0.5, 0.5))
        card.save(og, "JPEG", quality=85, optimize=True, progressive=True)
        post.write_text(text.replace(match.group(0), f'image: "/{og.as_posix()}"'), encoding="utf-8")
        if not any(f"/{cover.as_posix()}" in p.read_text(encoding="utf-8") for p in markdown_files()):
            cover.unlink()
        made += 1
        print(f"og     {og}")
    return made


def shrink_images():
    saved = 0
    for path in sorted(ASSETS.rglob("*")):
        if path.suffix.lower() not in (".png", ".jpg", ".jpeg", ".webp") or path.name == OG_NAME:
            continue
        before = path.stat().st_size
        image = open_image(path)
        if image.width <= MAX_WIDTH and (before <= SMALL_ENOUGH or path.suffix.lower() == ".webp"):
            continue
        if image.width > MAX_WIDTH:
            image = image.resize((MAX_WIDTH, round(image.height * MAX_WIDTH / image.width)), Image.LANCZOS)
        target = path.with_suffix(".webp")
        tmp = target.with_name(target.stem + ".tmp.webp")
        image.save(tmp, "WEBP", quality=WEBP_QUALITY, method=6)
        after = tmp.stat().st_size
        if after >= before and path.suffix.lower() != ".webp" and image.width == Image.open(path).width:
            tmp.unlink()  # the original is already the better file
            continue
        tmp.replace(target)
        if target != path:
            path.unlink()
            rewrite_references(path, target)
        saved += before - after
        print(f"webp   {path} {before // 1024}KB -> {target.name} {after // 1024}KB")
    return saved


def main():
    if not ASSETS.is_dir():
        print("run from the repository root", file=sys.stderr)
        return 1
    cards = make_og_images()
    saved = shrink_images()
    print(f"{cards} social cards cut, {saved / 1_048_576:.1f} MB saved on post images")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
