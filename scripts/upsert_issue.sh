#!/usr/bin/env bash
# Open a GitHub issue, or rewrite the open one with the same label.
#   scripts/upsert_issue.sh <label> <title> <body-file> [label-description]
# Needs `gh`, GH_TOKEN and `issues: write` in the workflow.
# Site tooling, largely AI-written (Claude), checked for behaviour not wording.
# Lab policy lives in _guide/. See accessibility.md, "How this site is made".
set -euo pipefail

LABEL="${1:?usage: upsert_issue.sh <label> <title> <body-file> [description]}"
TITLE="${2:?missing title}"
BODY_FILE="${3:?missing body file}"
DESCRIPTION="${4:-Opened automatically by a scheduled check}"

if [ ! -f "$BODY_FILE" ]; then
  echo "::error::No report at $BODY_FILE, refusing to open an empty issue."
  exit 1
fi

gh label create "$LABEL" --description "$DESCRIPTION" --color "D93F0B" 2>/dev/null || true

NUMBER="$(gh issue list --label "$LABEL" --state open \
            --json number --jq '.[0].number // empty')"

if [ -n "$NUMBER" ]; then
  gh issue edit "$NUMBER" --title "$TITLE" --body-file "$BODY_FILE"
  gh issue comment "$NUMBER" --body \
    "Re-checked $(date -u '+%-d %B %Y'). The description above has been replaced with the latest results."
  echo "Updated existing issue #$NUMBER."
else
  gh issue create --title "$TITLE" --label "$LABEL" --body-file "$BODY_FILE"
  echo "Opened a new issue."
fi
