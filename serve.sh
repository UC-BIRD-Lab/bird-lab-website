#!/usr/bin/env bash
# Preview the site locally in Docker, with the same Ruby and Gemfile.lock as CI.
# Needs Docker Desktop. Usage: ./serve.sh, then open http://localhost:4000; Ctrl+C stops.
# Site tooling, largely AI-written (Claude), checked for behaviour not wording.
# Lab policy lives in _guide/. See accessibility.md, "How this site is made".
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

# Bundler fails cryptically if Gemfile.lock lacks this platform.
case "$(uname -m)" in
  arm64|aarch64) NEEDED_PLATFORM="aarch64-linux" ;;
  *)             NEEDED_PLATFORM="x86_64-linux" ;;
esac

# Anchored so "x86_64-linux" does not match "x86_64-linux-musl".
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

# A run killed without Ctrl+C can leave a container holding port 4000.
docker rm -f birdlab-site >/dev/null 2>&1 || true

echo "Starting Jekyll in Docker: open http://localhost:4000 (Ctrl+C to stop)."
echo "(The first run downloads gems and can take a few minutes. Later runs reuse them.)"

# BUNDLE_FROZEN: fail if Gemfile and Gemfile.lock disagree. birdlab-gems: gem
# cache volume. No --platform: ruby:3.3 is multi-arch.
exec docker run --rm -it \
  --name birdlab-site \
  -v "$PWD:/srv/jekyll" \
  -v birdlab-gems:/usr/local/bundle \
  -w /srv/jekyll \
  -e BUNDLE_FROZEN=true \
  -p 4000:4000 \
  "ruby:${RUBY_VERSION}" \
  bash -lc "bundle install --quiet && bundle exec jekyll serve --force_polling --host 0.0.0.0"
