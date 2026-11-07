#!/usr/bin/env python3
"""Draw the link-preview card for each page, then check every og:image exists.

Run after `jekyll build`. _plugins/share_cards.rb gives a card to every page
with an `icon:` and lists them in .jekyll-cache/share-cards.json; this script
draws each one as a 1200 x 630 PNG in _site/assets/img/og/: the page's icon in
a ring over the faded BIRD logo. Cards carry no words, since Slack and other
apps print the page title and description beside them, and text that small
can't be read. Everything that matters sits in the centre square, so apps that
crop previews to a square lose nothing.

The cards are drawn fresh on every build and never committed, so changing a
page's icon updates its card by itself.

    python scripts/share_cards.py               # draw cards, then check
    python scripts/share_cards.py --check-only  # only check og:image targets

Needs Pillow. scripts/share-cards/ holds the Noto Emoji font (SIL Open Font
License) and wordmark.png, rendered from assets/img/logo-wordmark.svg. If the
logo changes, re-render it: rsvg-convert -w 1100 assets/img/logo-wordmark.svg
-o scripts/share-cards/wordmark.png
"""
# Site tooling, largely AI-written (Claude), checked for behaviour not wording.
# Lab policy lives in _guide/. See accessibility.md, "How this site is made".
from __future__ import annotations
import argparse
import html
import json
import os
import re
import sys
from urllib.parse import unquote, urlparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS = os.path.join(ROOT, "scripts", "share-cards")
ICON_FONT = os.path.join(ASSETS, "NotoEmoji.ttf")
WORDMARK = os.path.join(ASSETS, "wordmark.png")

# Size and colours. Colours match --c-navy and friends in assets/css/style.css.
W, H = 1200, 630
NAVY = (20, 40, 79)            # --c-navy
NAVY_DEEP = (11, 22, 48)       # edge of the background, as in og-image.png
RING_FILL = (24, 46, 88)
RING_LINE = (70, 98, 146)
WHITE = (255, 255, 255)
WORDMARK_OPACITY = 0.10        # how strongly the BIRD logo shows through
RING_RADIUS = 225
ICON_SIZE = 260


def background():
    """Navy field with the faded BIRD wordmark and the empty ring. Drawn once."""
    from PIL import Image, ImageChops, ImageDraw, ImageFilter
    im = Image.new("RGB", (W, H), NAVY_DEEP)
    glow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(glow).ellipse((W / 2 - 560, -300, W / 2 + 560, H + 260), fill=255)
    im.paste(Image.new("RGB", (W, H), NAVY), (0, 0), glow.filter(ImageFilter.GaussianBlur(170)))

    # The wordmark as a white wash; its pale wing shows a touch brighter than
    # the letters, so the bird stays visible.
    mark = Image.open(WORDMARK).convert("RGBA")
    shade = mark.convert("L").point(lambda v: int(255 * WORDMARK_OPACITY * (0.7 + 0.6 * v / 255)))
    alpha = ImageChops.multiply(mark.getchannel("A"), shade)
    im.paste(Image.new("RGB", mark.size, WHITE), ((W - mark.width) // 2, (H - mark.height) // 2), alpha)

    r, cx, cy = RING_RADIUS, W / 2, H / 2
    ImageDraw.Draw(im).ellipse((cx - r, cy - r, cx + r, cy + r), fill=RING_FILL, outline=RING_LINE, width=5)
    return im


def draw_card(base, icon):
    from PIL import ImageDraw, ImageFont
    im = base.copy()
    font = ImageFont.truetype(ICON_FONT, ICON_SIZE)
    ImageDraw.Draw(im).text((W / 2, H / 2), icon, font=font, fill=WHITE, anchor="mm")
    return im


def draw_all(site_dir, manifest):
    base = background()
    for card in manifest["cards"]:
        out = os.path.join(site_dir, card["path"].lstrip("/"))
        os.makedirs(os.path.dirname(out), exist_ok=True)
        draw_card(base, card["icon"]).save(out, optimize=True)
    print(f"Drew {len(manifest['cards'])} share cards in {os.path.join(site_dir, 'assets', 'img', 'og')}.")


OG_IMAGE = re.compile(r'<meta\s+property="og:image"\s+content="([^"]+)"', re.I)


def check(site_dir, site_url):
    """Every page's og:image must be a file in the built site."""
    base_path = urlparse(site_url).path.rstrip("/")
    host = urlparse(site_url).netloc
    problems, pages = [], 0
    for folder, _, files in os.walk(site_dir):
        for name in files:
            if not name.endswith(".html"):
                continue
            page = os.path.join(folder, name)
            with open(page, encoding="utf-8") as fh:
                found = OG_IMAGE.search(fh.read())
            if not found:
                continue
            pages += 1
            url = urlparse(html.unescape(found.group(1)))
            if url.netloc and url.netloc != host:
                continue  # an outside image; not ours to check
            path = unquote(url.path)
            if base_path and path.startswith(base_path + "/"):
                path = path[len(base_path):]
            if not os.path.isfile(os.path.join(site_dir, path.lstrip("/"))):
                problems.append(f"{os.path.relpath(page, site_dir)} -> {path}")
    if problems:
        print("These pages point their link preview at an image that doesn't exist:")
        print("\n".join(f"  {p}" for p in problems))
        return False
    print(f"Checked {pages} pages: every link-preview image exists.")
    return True


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--site", default=os.path.join(ROOT, "_site"))
    ap.add_argument("--manifest", default=os.path.join(ROOT, ".jekyll-cache", "share-cards.json"))
    ap.add_argument("--check-only", action="store_true")
    args = ap.parse_args()

    if not os.path.isfile(args.manifest):
        sys.exit(f"No {args.manifest}. Run `bundle exec jekyll build` first.")
    with open(args.manifest, encoding="utf-8") as fh:
        manifest = json.load(fh)

    if not args.check_only:
        draw_all(args.site, manifest)
    sys.exit(0 if check(args.site, manifest["site_url"]) else 1)


if __name__ == "__main__":
    main()
