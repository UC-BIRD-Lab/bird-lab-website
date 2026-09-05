#!/usr/bin/env bash
# Regenerate Gemfile.lock (committed; pins exact gem versions).
# Run after editing the Gemfile or to take newer gems, then open a pull request
# so CI proves the build. Needs Docker Desktop.
# Usage: ./scripts/update-lockfile.sh
# Site tooling, largely AI-written (Claude), checked for behaviour not wording.
# Lab policy lives in _guide/. See accessibility.md, "How this site is made".
set -euo pipefail
cd "$(dirname "$0")/.."

# Must match ruby-version in .github/workflows/*.yml.
RUBY_VERSION="3.3"

if ! command -v docker >/dev/null 2>&1; then
  echo "Docker isn't installed. Get Docker Desktop:"
  echo "  https://www.docker.com/products/docker-desktop/"
  exit 1
fi

echo "Resolving gems with Ruby ${RUBY_VERSION} (matching CI)…"

# Start clean: an old lockfile keeps stale platforms (the retired Alpine image
# left musl-only builds that fail elsewhere).
rm -f Gemfile.lock

docker run --rm \
  -v "$PWD:/app" \
  -w /app \
  "ruby:${RUBY_VERSION}" \
  bash -lc '
    set -e
    bundle lock
    # x86_64-linux = CI runners; aarch64-linux = Apple Silicon in Docker
    bundle lock --add-platform x86_64-linux aarch64-linux
    # arm64-darwin = native Mac Ruby, rarely used; not every gem ships it, so
    # a failure here must not lose the two above.
    bundle lock --add-platform arm64-darwin \
      || echo "Note: skipped arm64-darwin (native Mac Ruby). Docker preview and CI are unaffected."
  '

echo
echo "Gemfile.lock updated. Locked versions:"
grep -E "^    (jekyll|jekyll-feed|jekyll-seo-tag|jekyll-sitemap|jekyll-last-modified-at) " Gemfile.lock || true
echo
echo "Next: commit Gemfile.lock on a branch and open a pull request so CI can verify the build."
