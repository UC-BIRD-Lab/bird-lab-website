#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
#  Regenerate Gemfile.lock — the file that pins EXACT gem versions.
#
#  Why this exists
#  ---------------
#  The Gemfile says things like `gem "jekyll", "~> 4.3"`, which means "any 4.x
#  from 4.3 up". Without a lockfile, every GitHub Actions run re-resolves that
#  to whatever is newest that day, so the live site could break with no change
#  from anyone in the lab. Gemfile.lock freezes the answer, and is committed.
#
#  Run this ONLY when you deliberately want newer gems (or after editing the
#  Gemfile). Then commit the updated Gemfile.lock and open a pull request, so
#  the Site checks workflow proves the new versions still build.
#
#  Requires Docker Desktop: https://www.docker.com/products/docker-desktop/
#  Usage:  ./scripts/update-lockfile.sh
# ─────────────────────────────────────────────────────────────
set -euo pipefail
cd "$(dirname "$0")/.."

# Must match the ruby-version used by .github/workflows/*.yml, or the lockfile
# we produce here won't be the one CI can actually use.
RUBY_VERSION="3.3"

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker isn't installed. Get Docker Desktop:"
  echo "  https://www.docker.com/products/docker-desktop/"
  exit 1
fi

echo "Resolving gems with Ruby ${RUBY_VERSION} (matching CI)…"

# --add-platform matters: the lockfile records which OS/CPU each compiled gem
# was resolved for. CI runs x86_64 Linux; your Mac runs arm64. If the lockfile
# lists only one of them, the other environment fails to install. So we record
# all three the project actually uses.
# Start from scratch. An existing lockfile can carry platforms from whatever
# container last wrote it (the retired Alpine image left musl-only builds behind,
# which then fail on both CI and Apple Silicon).
rm -f Gemfile.lock

docker run --rm \
  -v "$PWD:/app" \
  -w /app \
  "ruby:${RUBY_VERSION}" \
  bash -lc '
    set -e
    bundle lock
    # x86_64-linux  = GitHub Actions runners
    # aarch64-linux = Apple Silicon Macs running ./serve.sh in Docker
    bundle lock --add-platform x86_64-linux aarch64-linux
    # arm64-darwin = native "bundle exec jekyll serve" on a Mac, without Docker.
    # Rarely used here, and not every gem ships a macOS build, so do not let a
    # failure on this one lose the two platforms that actually matter.
    bundle lock --add-platform arm64-darwin \
      || echo "Note: skipped arm64-darwin (native Mac Ruby). Docker preview and CI are unaffected."
  '

echo
echo "Gemfile.lock updated. Locked versions:"
grep -E "^    (jekyll|jekyll-feed|jekyll-seo-tag|jekyll-sitemap|jekyll-last-modified-at) " Gemfile.lock || true
echo
echo "Next: commit Gemfile.lock on a branch and open a pull request so CI can verify the build."
