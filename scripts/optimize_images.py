#!/usr/bin/env python3
"""Shrink over-budget images under assets/img/ in place (resize to MAX_WIDTH, recompress).

Idempotent; keeps PNG transparency; skips `_raw/` and ICO. --check only reports
(exit 1 if anything is over) and also covers video, GIF and SVG, which are never
rewritten. Runs in CI; apply-images.sh is the macOS asset builder.

    python scripts/optimize_images.py [--check]     # needs Pillow
"""
# Site tooling, largely AI-written (Claude), checked for behaviour not wording.
# Lab policy lives in _guide/. See accessibility.md, "How this site is made".
from __future__ import annotations
import argparse
import os
import re
import sys

IMG_ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                        "assets", "img")

MAX_WIDTH = 1600          # widest the site needs (hero/lab photos)
HARD_MAX_WIDTH = 2400     # above this, resize even a light file
JPEG_BUDGET_KB = 300
PNG_BUDGET_KB = 600       # figures/screenshots get more room
JPEG_FLOOR_Q = 60         # lowest JPEG quality used

# Video and GIF are reported, never rewritten (needs ffmpeg and judgement).
# Budgets sit just above what the site carries today.
VIDEO_BUDGET_KB = 2560    # bird-glide.mp4 is ~2.4 MB
GIF_BUDGET_KB = 700       # prefer MP4

RASTER = (".jpg", ".jpeg", ".png")
MEDIA = (".mp4", ".webm", ".mov", ".gif")
SKIP_DIRS = {"_raw"}      # source originals

# SVGs can run script; ours are plain icons, so any script is unexpected.
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
    """Video and GIF under roots."""
    for root in roots:
        if not os.path.isdir(root):
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for name in filenames:
                if os.path.splitext(name)[1].lower() in MEDIA:
                    yield os.path.join(dirpath, name)


def check_media(roots, repo_root):
    """Oversized video/GIF, as readable messages."""
    problems = []
    for path in sorted(iter_other_media(roots)):
        ext = os.path.splitext(path)[1].lower()
        limit = GIF_BUDGET_KB if ext == ".gif" else VIDEO_BUDGET_KB
        size = kb(path)
        if size > limit:
            rel = os.path.relpath(path, repo_root)
            problems.append(
                "  • %s  (%d KB, budget %d KB)" % (rel, size, limit)
                + ("\n      The same clip as an MP4 is usually a fraction of the weight."
                   if ext == ".gif" else
                   "\n      Re-encode it smaller, or raise VIDEO_BUDGET_KB deliberately.")
            )
    return problems


def check_svgs(roots, repo_root):
    """SVGs containing scripts or event handlers."""
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
                        + "\n      SVGs here should be plain artwork. Remove the script, "
                          "or re-export it."
                    )
    return problems


def is_oversized(path):
    """Over budget, or past HARD_MAX_WIDTH.

    A file slightly over MAX_WIDTH but within budget is left alone: re-encoding
    can grow it (a 2003px 123 KB PNG became 292 KB at 1600px).
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
    """Shrink one image in place. Returns (before_kb, after_kb), or None if not written."""
    from PIL import Image
    before = kb(path)
    is_jpeg = path.lower().endswith((".jpg", ".jpeg"))
    im = Image.open(path)

    was_too_wide = im.width > MAX_WIDTH
    if was_too_wide:
        im = im.resize((MAX_WIDTH, round(im.height * MAX_WIDTH / im.width)), Image.LANCZOS)

    tmp = path + ".opt"
    if is_jpeg:
        if im.mode in ("RGBA", "LA", "P"):            # flatten onto white
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
        # Lossless; the resize above is where PNG savings come from.
        im.save(tmp, "PNG", optimize=True)

    after = kb(tmp)
    # Also write when only the width changed, or an over-wide file that
    # re-encodes larger stays flagged forever.
    if after < before or was_too_wide:
        os.replace(tmp, path)
        return before, after
    try:
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
        print("No image directory at %s, nothing to do." % args.dir)
        return 0

    oversized = [p for p in iter_images(args.dir) if is_oversized(p)]

    if args.check:
        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Video and SVGs live outside assets/img/ too.
        media_roots = [args.dir, os.path.join(repo_root, "assets", "video")]
        media_problems = check_media(media_roots, repo_root)
        svg_problems = check_svgs([os.path.join(repo_root, "assets")], repo_root)

        if oversized:
            print("Oversized images (> %dpx wide or over budget):" % MAX_WIDTH)
            for p in oversized:
                rel = os.path.relpath(p, os.path.dirname(args.dir))
                print("  • %s  (%d KB)" % (rel, kb(p)))
            print("\nRun `python scripts/optimize_images.py` to compress them.")
            print("Still listed after running that? The compressor has done all it\n"
                  "can (it won't push JPEG quality below %d). Crop it, export it\n"
                  "smaller, or save a photo as JPEG rather than PNG." % JPEG_FLOOR_Q)

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
            # A width-driven resize can grow the file, so show direction.
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
