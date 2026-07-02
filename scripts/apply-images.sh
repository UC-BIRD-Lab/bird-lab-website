#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────────────────
#  BIRD Lab — image asset generator (run on a Mac; uses built-in `sips`)
#
#  Generates optimized site images from originals you have locally:
#    • assets/img/lab-photo.jpg   — lab group photo (People page)
#    • assets/img/og-image.jpg    — 1200×630 social-share image
#    • assets/img/people/*.jpg    — square, optimized headshots
#
#  WHY a script you run (not generated for you): the high-res originals and the
#  Notion export live on your Mac, not in this repo. `sips` ships with macOS, so
#  no installs are needed.
#
#  USAGE
#    1) Group photo:
#         bash scripts/apply-images.sh "/path/to/group-photo.jpg"
#       …or let it auto-search the export folder:
#         bash scripts/apply-images.sh
#    2) Headshots: drop originals into  assets/img/people/_raw/  (any name;
#       use the person's name, e.g. "Christina Harvey.jpg") then run this script.
#       Each becomes  assets/img/people/firstname-lastname.jpg.
#
#  AFTER RUNNING
#    • Set  lab_photo: /assets/img/lab-photo.jpg  under  assets:  in _config.yml
#    • For each headshot, add  photo: /assets/img/people/<name>.jpg  in _data/people.yml
#  (og-image.jpg is already wired via `image:` in _config.yml.)
# ─────────────────────────────────────────────────────────────────────────
set -euo pipefail
cd "$(dirname "$0")/.."          # repo root

SRC_DEFAULT="$HOME/Downloads/Private & Shared 5/BIRD Lab"
SRC="${BIRD_SRC:-$SRC_DEFAULT}"

IMG_DIR="assets/img"
PEOPLE_DIR="$IMG_DIR/people"
RAW_HEADSHOTS="$PEOPLE_DIR/_raw"
mkdir -p "$PEOPLE_DIR"

command -v sips >/dev/null 2>&1 || { echo "ERROR: this script needs macOS 'sips'."; exit 1; }

echo "── BIRD Lab image generator ──"
echo "Source export: $SRC"

# ── 1. Lab group photo + OG image ────────────────────────────────────────
GROUP_PHOTO="${1:-}"
if [ -z "$GROUP_PHOTO" ] && [ -d "$SRC" ]; then
  GROUP_PHOTO="$(find "$SRC" -type f \
      \( -iname '*group*' -o -iname '*team*' -o -iname '*lab photo*' -o -iname '*lab-photo*' \) \
      \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' -o -iname '*.heic' \) \
      2>/dev/null | head -1 || true)"
fi

if [ -n "$GROUP_PHOTO" ] && [ -f "$GROUP_PHOTO" ]; then
  echo "Group photo: $GROUP_PHOTO"
  sips -s format jpeg -s formatOptions 82 "$GROUP_PHOTO" \
       --resampleWidth 1600 --out "$IMG_DIR/lab-photo.jpg" >/dev/null
  echo "  → $IMG_DIR/lab-photo.jpg"
  # OG: center-crop to 1200×630 (sips -c is height width)
  cp "$IMG_DIR/lab-photo.jpg" /tmp/bird-og-src.jpg
  sips -s format jpeg -s formatOptions 82 -c 630 1200 /tmp/bird-og-src.jpg \
       --out "$IMG_DIR/og-image.jpg" >/dev/null
  echo "  → $IMG_DIR/og-image.jpg"
  echo "  NEXT: set  lab_photo: /assets/img/lab-photo.jpg  under assets: in _config.yml"
else
  echo "No group photo found automatically."
  echo "  Re-run with an explicit path:  bash scripts/apply-images.sh \"/path/to/group-photo.jpg\""
  if [ ! -f "$IMG_DIR/og-image.jpg" ] && [ -f "$IMG_DIR/facilities/cali.jpg" ]; then
    sips -s format jpeg -s formatOptions 82 -c 630 1200 "$IMG_DIR/facilities/cali.jpg" \
         --out "$IMG_DIR/og-image.jpg" >/dev/null
    echo "  → wrote a temporary $IMG_DIR/og-image.jpg from facilities/cali.jpg (replace later)"
  fi
fi

# ── 2. Headshots ─────────────────────────────────────────────────────────
if [ -d "$RAW_HEADSHOTS" ] && [ -n "$(ls -A "$RAW_HEADSHOTS" 2>/dev/null || true)" ]; then
  echo "Processing headshots in $RAW_HEADSHOTS ..."
  for f in "$RAW_HEADSHOTS"/*; do
    [ -f "$f" ] || continue
    name="$(basename "${f%.*}")"
    slug="$(echo "$name" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-')"
    sips -s format jpeg -s formatOptions 85 "$f" -c 600 600 \
         --out "$PEOPLE_DIR/$slug.jpg" >/dev/null
    echo "  → $PEOPLE_DIR/$slug.jpg   (add  photo: /assets/img/people/$slug.jpg)"
  done
else
  echo "No headshots to process (drop originals in $RAW_HEADSHOTS/ and re-run)."
fi

# ── 3. "Scenes from the lab" storytelling photos ─────────────────────────
#   Drop originals in assets/img/lab/_raw/ named raptor-hall.* / outreach.* /
#   wind-tunnel.* (any extension). They are resized to ~1600px wide, then flip
#   ready: true for each in _data/gallery.yml to show it on the site.
LAB_DIR="$IMG_DIR/lab"
RAW_LAB="$LAB_DIR/_raw"
mkdir -p "$LAB_DIR"
if [ -d "$RAW_LAB" ] && [ -n "$(ls -A "$RAW_LAB" 2>/dev/null || true)" ]; then
  echo "Processing lab scenes in $RAW_LAB ..."
  for f in "$RAW_LAB"/*; do
    [ -f "$f" ] || continue
    base="$(basename "${f%.*}" | tr '[:upper:] ' '[:lower:]-')"
    sips -s format jpeg -s formatOptions 82 "$f" --resampleWidth 1600 \
         --out "$LAB_DIR/$base.jpg" >/dev/null
    echo "  → $LAB_DIR/$base.jpg   (set ready: true for it in _data/gallery.yml)"
  done
else
  echo "No lab scenes to process (drop originals in $RAW_LAB/ and re-run)."
fi

echo "Done. Preview with ./serve.sh"
