#!/usr/bin/env bash
# ─────────────────────────────────────────────────────────────
#  Regenerate Gemfile.lock, the file that pins exact gem versions.
#
#  The Gemfile allows a range of versions ("jekyll ~> 4.3"). Gemfile.lock records
#  which ones were actually used, so the site can't break from an upstream
#  release nobody here asked for. It is committed.
#
#  Run this only when you deliberately want newer gems, or after editing the
#  Gemfile. Then commit Gemfile.lock on a branch and open a pull request, so the
#  checks prove the new versions build.
#
#  Requires Docker Desktop: https://www.docker.com/products/docker-desktop/
#  Usage:  ./scripts/update-lockfile.sh
# ─────────────────────────────────────────────────────────────
# Website tooling, largely written by AI (Claude) and checked for behaviour
# rather than wording. It describes how the site is built, not how the lab works;
# lab policy lives in _guide/. See accessibility.md, "How this site is made".
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

# The lockfile records which OS/CPU each compiled gem was built for. CI is
# x86_64 Linux, your Mac is arm64; listing only one breaks the other.
# Start clean: an old lockfile carries platforms from whatever container wrote
# it (the retired Alpine image left musl-only builds that fail everywhere else).
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
