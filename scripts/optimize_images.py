#!/usr/bin/env python3
"""
optimize_images.py: keep committed site images within a sane weight budget, so a
5 MB phone photo dropped into assets/img/ never ships and slows the page (exactly
the "hiking photo is slow to load" / "crop the mobile video" fixes done by hand).

WHAT IT DOES
  Walks assets/img/ and, for any raster image OVER budget, shrinks it in place:
    • resizes anything wider than MAX_WIDTH down to MAX_WIDTH (never enlarges), and
    • recompresses until it fits the size budget (JPEG quality ladder; PNG optimize).
  Images already within budget are left untouched — so it is IDEMPOTENT and never
  re-compresses (and degrades) a file that's already fine.

  Complements apply-images.sh (that macOS `sips` script builds specific assets from
  local originals; this one is a cross-platform safety net that runs in CI on every
  image that lands in the repo).

MODES
  (default)         fix images in place and print what changed.
  --check           don't modify anything; list oversized images and exit 1 if any
                    (used by CI to decide whether to open a "compress images" PR).

SAFE by design: skips SVG/ICO/GIF and any `_raw/` source folder, only ever writes a
file when the result is actually smaller, and preserves PNG transparency.

Run locally:   python scripts/optimize_images.py            # fix in place
               python scripts/optimize_images.py --check    # report only
Requires: Pillow  (pip install Pillow)
"""
from __future__ import annotations
import argparse
import os
import sys

IMG_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "assets", "img")

MAX_WIDTH = 1600          # widest we ever need on the site (hero/lab photos)
JPEG_BUDGET_KB = 300      # a full-width photo should comfortably fit this
PNG_BUDGET_KB = 600       # PNGs are often figures/screenshots; allow a bit more
JPEG_FLOOR_Q = 60         # don't drop JPEG quality below this chasing bytes

RASTER = (".jpg", ".jpeg", ".png")
SKIP_DIRS = {"_raw"}      # source originals live here; don't touch them


def kb(path):
    return os.path.getsize(path) / 1024


def iter_images(root):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            if os.path.splitext(name)[1].lower() in RASTER:
                yield os.path.join(dirpath, name)


def budget_kb(path):
    return JPEG_BUDGET_KB if path.lower().endswith((".jpg", ".jpeg")) else PNG_BUDGET_KB


def is_oversized(path):
    """True if the image is wider than MAX_WIDTH or heavier than its budget."""
    from PIL import Image
    if kb(path) > budget_kb(path):
        return True
    try:
        with Image.open(path) as im:
            return im.width > MAX_WIDTH
    except Exception:
        return False


def optimize(path):
    """Shrink one oversized image in place. Returns (before_kb, after_kb) or None
    if nothing smaller could be produced (so no write happens)."""
    from PIL import Image
    before = kb(path)
    is_jpeg = path.lower().endswith((".jpg", ".jpeg"))
    im = Image.open(path)

    # Resize down to MAX_WIDTH if wider (never up).
    if im.width > MAX_WIDTH:
        im = im.resize((MAX_WIDTH, round(im.height * MAX_WIDTH / im.width)), Image.LANCZOS)

    tmp = path + ".opt"
    if is_jpeg:
        if im.mode in ("RGBA", "LA", "P"):            # flatten transparency onto white
            rgba = im.convert("RGBA")
            bg = Image.new("RGB", rgba.size, (255, 255, 255))
            bg.paste(rgba, mask=rgba.split()[-1])
            im = bg
        else:
            im = im.convert("RGB")
        q = 85
        im.save(tmp, "JPEG", quality=q, optimize=True, progressive=True)
        while kb(tmp) > JPEG_BUDGET_KB and q > JPEG_FLOOR_Q:
            q -= 5
            im.save(tmp, "JPEG", quality=q, optimize=True, progressive=True)
    else:
        # Preserve palette/alpha; optimize losslessly and drop to palette if it has
        # few colours. Resizing (above) is usually where the real savings come from.
        im.save(tmp, "PNG", optimize=True)

    after = kb(tmp)
    if after < before:                                # only replace when we actually win
        os.replace(tmp, path)
        return before, after
    try:                                              # nothing gained → drop the temp
        os.remove(tmp)
    except OSError:
        pass
    return None


def main(argv=None):
    ap = argparse.ArgumentParser(description="Compress oversized site images.")
    ap.add_argument("--check", action="store_true",
                    help="Report oversized images and exit 1 if any; change nothing.")
    ap.add_argument("--dir", default=IMG_ROOT, help="Image root (default assets/img).")
    args = ap.parse_args(argv)

    try:
        import PIL  # noqa: F401
    except ImportError:
        sys.exit("Pillow is required: pip install Pillow")

    if not os.path.isdir(args.dir):
        print("No image directory at %s — nothing to do." % args.dir)
        return 0

    oversized = [p for p in iter_images(args.dir) if is_oversized(p)]

    if args.check:
        if oversized:
            print("Oversized images (> %dpx wide or over budget):" % MAX_WIDTH)
            for p in oversized:
                rel = os.path.relpath(p, os.path.dirname(args.dir))
                print("  • %s  (%d KB)" % (rel, kb(p)))
            print("\nRun `python scripts/optimize_images.py` to compress them.")
            return 1
        print("All images are within budget. ✅")
        return 0

    if not oversized:
        print("All images are within budget. Nothing to compress. ✅")
        return 0

    changed = 0
    for p in oversized:
        rel = os.path.relpath(p, os.path.dirname(args.dir))
        result = optimize(p)
        if result:
            before, after = result
            changed += 1
            print("  ✓ %s  %d KB → %d KB  (-%d%%)"
                  % (rel, before, after, round(100 * (before - after) / before)))
        else:
            print("  – %s  already minimal (left as-is)" % rel)
    print("\nCompressed %d image(s)." % changed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
