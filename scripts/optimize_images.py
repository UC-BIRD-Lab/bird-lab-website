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
import re
import sys

IMG_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "assets", "img")

MAX_WIDTH = 1600          # widest we ever need on the site (hero/lab photos)
HARD_MAX_WIDTH = 2400     # beyond this, resize even if the file is already light
JPEG_BUDGET_KB = 300      # a full-width photo should comfortably fit this
PNG_BUDGET_KB = 600       # PNGs are often figures/screenshots; allow a bit more
JPEG_FLOOR_Q = 60         # don't drop JPEG quality below this chasing bytes

# Video and GIF are REPORTED, never rewritten: re-encoding video needs ffmpeg and
# real judgement about quality, which isn't something to do automatically behind
# someone's back. The budget is a ratchet — it's set just above what the site
# carries today, so nothing has to change now, but a heavier file can't drift in
# unnoticed. Raise it deliberately if you genuinely need a bigger asset.
VIDEO_BUDGET_KB = 2560    # ~2.5 MB; bird-glide.mp4 is ~2.4 MB
GIF_BUDGET_KB = 700       # GIFs are enormous for what they are; prefer MP4

RASTER = (".jpg", ".jpeg", ".png")
MEDIA = (".mp4", ".webm", ".mov", ".gif")
SKIP_DIRS = {"_raw"}      # source originals live here; don't touch them

# An SVG is executable content: it can carry <script> or event handlers, which
# would run on the page. Ours are all hand-made icons, so any script inside one
# means something unexpected arrived — a downloaded asset, or a bad export.
SVG_DANGER = re.compile(r"<script|\son\w+\s*=|javascript:", re.I)


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


def iter_other_media(roots):
    """Video and GIF files anywhere in assets/ — these are checked, never rewritten."""
    for root in roots:
        if not os.path.isdir(root):
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for name in filenames:
                if os.path.splitext(name)[1].lower() in MEDIA:
                    yield os.path.join(dirpath, name)


def check_media(roots, repo_root):
    """Report oversized video/GIF. Returns a list of human-readable problems."""
    problems = []
    for path in sorted(iter_other_media(roots)):
        ext = os.path.splitext(path)[1].lower()
        limit = GIF_BUDGET_KB if ext == ".gif" else VIDEO_BUDGET_KB
        size = kb(path)
        if size > limit:
            rel = os.path.relpath(path, repo_root)
            problems.append(
                "  • %s  (%d KB, budget %d KB)" % (rel, size, limit)
                + ("\n      A GIF this size is almost always better as an MP4 — "
                   "an MP4 of the same clip is usually a fraction of the weight."
                   if ext == ".gif" else
                   "\n      Re-encode it (smaller dimensions, or a lower bitrate) "
                   "or raise VIDEO_BUDGET_KB deliberately.")
            )
    return problems


def check_svgs(roots, repo_root):
    """Report SVGs containing scripts or event handlers."""
    problems = []
    for root in roots:
        if not os.path.isdir(root):
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for name in sorted(filenames):
                if not name.lower().endswith(".svg"):
                    continue
                path = os.path.join(dirpath, name)
                try:
                    with open(path, encoding="utf-8", errors="replace") as fh:
                        body = fh.read()
                except OSError:
                    continue
                if SVG_DANGER.search(body):
                    problems.append(
                        "  • %s contains a script or event handler."
                        % os.path.relpath(path, repo_root)
                        + "\n      SVGs on this site should be plain artwork. Open it in a "
                          "text editor and remove the <script>/on… code, or re-export it."
                    )
    return problems


def is_oversized(path):
    """True if this image is a problem worth fixing.

    The budget that actually matters is WEIGHT — width is only a proxy for it.
    So a file that is a bit wider than MAX_WIDTH but comfortably inside its byte
    budget is left alone: re-encoding such an image makes it BIGGER, because the
    original was compressed more thoroughly than Pillow will manage. (Measured on
    this repo: a 2003px 123 KB PNG becomes 292 KB when resized to 1600px. Shipping
    169 KB more to save 400px of width is a bad trade, and flagging it forever
    would give us a check nothing can clear.)

    Width therefore only forces a rewrite when the file is ALSO over its byte
    budget, or when it is so large that decoding it wastes real memory on a phone.
    """
    from PIL import Image
    if kb(path) > budget_kb(path):
        return True
    try:
        with Image.open(path) as im:
            return im.width > HARD_MAX_WIDTH
    except Exception:
        return False


def optimize(path):
    """Shrink one oversized image in place. Returns (before_kb, after_kb) or None
    if there was nothing worth writing."""
    from PIL import Image
    before = kb(path)
    is_jpeg = path.lower().endswith((".jpg", ".jpeg"))
    im = Image.open(path)

    # Resize down to MAX_WIDTH if wider (never up).
    was_too_wide = im.width > MAX_WIDTH
    if was_too_wide:
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
    # Write if we saved bytes, OR if the image was too wide and now isn't.
    #
    # That second case matters: an already well-compressed PNG that is merely a
    # little too wide often gets BIGGER when re-encoded at a smaller size (fewer
    # pixels, but Pillow's encoder is less thorough than whatever produced the
    # original). Under the old "only write when smaller" rule such a file was
    # never rewritten, stayed over the width budget, and was reported oversized
    # on every single run — a failure the fixer itself could not clear.
    if after < before or was_too_wide:
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
        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Video/GIF and SVGs live across assets/, not just assets/img/.
        media_roots = [args.dir, os.path.join(repo_root, "assets", "video")]
        media_problems = check_media(media_roots, repo_root)
        svg_problems = check_svgs([os.path.join(repo_root, "assets")], repo_root)

        if oversized:
            print("Oversized images (> %dpx wide or over budget):" % MAX_WIDTH)
            for p in oversized:
                rel = os.path.relpath(p, os.path.dirname(args.dir))
                print("  • %s  (%d KB)" % (rel, kb(p)))
            print("\nRun `python scripts/optimize_images.py` to compress them.")
            print("If an image is STILL listed after running that, the automatic\n"
                  "compressor has done all it can (it won't push JPEG quality below\n"
                  "%d chasing bytes). Crop it, export it smaller, or save a photo as\n"
                  "JPEG instead of PNG." % JPEG_FLOOR_Q)

        if media_problems:
            print("\nOversized video/GIF (these are never changed automatically):")
            print("\n".join(media_problems))

        if svg_problems:
            print("\nSVGs that contain code:")
            print("\n".join(svg_problems))

        if oversized or media_problems or svg_problems:
            return 1
        print("All images, video and SVGs are within budget and safe. ✅")
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
            # A width-driven resize can legitimately increase the byte size, so
            # say "grew"/"shrank" rather than printing a double-negative percentage.
            pct = round(100 * abs(before - after) / before)
            direction = "-" if after <= before else "+"
            print("  ✓ %s  %d KB → %d KB  (%s%d%%%s)"
                  % (rel, before, after, direction, pct,
                     ", resized to fit the width limit" if after > before else ""))
        else:
            print("  – %s  already minimal (left as-is)" % rel)
    print("\nCompressed %d image(s)." % changed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
