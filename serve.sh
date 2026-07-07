#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
#  Preview the BIRD Lab site locally — no Ruby/Jekyll on your Mac.
#  Runs Jekyll inside Docker, so none of the native gems
#  (eventmachine, etc.) are compiled against your system.
#
#  Requires Docker Desktop: https://www.docker.com/products/docker-desktop/
#  Usage:  ./serve.sh      (then open http://localhost:4000)
#  Stop:   Ctrl+C
# ─────────────────────────────────────────────────────────────
set -e
cd "$(dirname "$0")"

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker isn't installed. Get Docker Desktop:"
  echo "  https://www.docker.com/products/docker-desktop/"
  echo "…or preview via GitHub Pages instead (see DEPLOYMENT.md)."
  exit 1
fi

# If a previous run was killed without Ctrl+C, its container can linger and
# hold port 4000; remove any leftover one so a restart always works.
docker rm -f birdlab-site >/dev/null 2>&1 || true

echo "Starting Jekyll in Docker: open http://localhost:4000 (Ctrl+C to stop)."
echo "(The first start after a Docker restart can take a few minutes before any output appears.)"
exec docker run --rm -it \
  --name birdlab-site \
  --platform linux/amd64 \
  -v "$PWD:/srv/jekyll" \
  -p 4000:4000 \
  jekyll/jekyll:4.2.2 \
  jekyll serve --force_polling --host 0.0.0.0
