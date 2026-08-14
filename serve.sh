#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
#  Preview the BIRD Lab site locally. No Ruby/Jekyll needed on your Mac.
#  Runs Jekyll inside Docker, so none of the native gems
#  (eventmachine, etc.) are compiled against your system.
#
#  Uses the same Ruby version and Gemfile.lock as the GitHub Actions build that
#  publishes the live site, so what you see here is what ships.
#
#  Requires Docker Desktop: https://www.docker.com/products/docker-desktop/
#  Usage:  ./serve.sh      (then open http://localhost:4000)
#  Stop:   Ctrl+C
# ─────────────────────────────────────────────────────────────
# Website tooling, largely written by AI (Claude) and checked for behaviour
# rather than wording. It describes how the site is built, not how the lab works;
# lab policy lives in _guide/. See accessibility.md, "How this site is made".
set -euo pipefail
cd "$(dirname "$0")"

# Must match ruby-version in .github/workflows/*.yml.
RUBY_VERSION="3.3"

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker isn't installed. Get Docker Desktop:"
  echo "  https://www.docker.com/products/docker-desktop/"
  echo "…or preview via a pull request instead (see MAINTENANCE.md)."
  exit 1
fi

if [ ! -f Gemfile.lock ]; then
  echo "Gemfile.lock is missing. Create it once with:"
  echo "  ./scripts/update-lockfile.sh"
  exit 1
fi

# Gemfile.lock records which CPU/OS each compiled gem was built for. Without a
# match Bundler fails cryptically, so check here and say what to run.
case "$(uname -m)" in
  arm64|aarch64) NEEDED_PLATFORM="aarch64-linux" ;;
  *)             NEEDED_PLATFORM="x86_64-linux" ;;
esac

# Anchored match: plain "x86_64-linux" must not match the "x86_64-linux-musl" line.
if ! grep -qE "^  ${NEEDED_PLATFORM}\$" Gemfile.lock; then
  echo "Gemfile.lock doesn't cover this computer (needs ${NEEDED_PLATFORM})."
  echo "It currently covers:"
  sed -n '/^PLATFORMS$/,/^$/p' Gemfile.lock | sed '1d;/^$/d' | sed 's/^/    /'
  echo
  echo "Fix it with:"
  echo "  ./scripts/update-lockfile.sh"
  echo "then commit the updated Gemfile.lock."
  exit 1
fi

# If a previous run was killed without Ctrl+C, its container can linger and
# hold port 4000; remove any leftover one so a restart always works.
docker rm -f birdlab-site >/dev/null 2>&1 || true

echo "Starting Jekyll in Docker: open http://localhost:4000 (Ctrl+C to stop)."
echo "(The first run downloads gems and can take a few minutes. Later runs reuse them.)"

# BUNDLE_FROZEN  stop if Gemfile and Gemfile.lock disagree, rather than
#                previewing different versions than the live site uses.
# birdlab-gems   Docker volume caching installed gems between runs.
# No --platform: ruby:3.3 is multi-arch, so this runs natively on Apple Silicon.
exec docker run --rm -it \
  --name birdlab-site \
  -v "$PWD:/srv/jekyll" \
  -v birdlab-gems:/usr/local/bundle \
  -w /srv/jekyll \
  -e BUNDLE_FROZEN=true \
  -p 4000:4000 \
  "ruby:${RUBY_VERSION}" \
  bash -lc "bundle install --quiet && bundle exec jekyll serve --force_polling --host 0.0.0.0"
