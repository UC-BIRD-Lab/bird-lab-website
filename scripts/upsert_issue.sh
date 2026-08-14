#!/usr/bin/env bash
# Website tooling, largely written by AI (Claude) and checked for behaviour
# rather than wording. It describes how the site is built, not how the lab works;
# lab policy lives in _guide/. See accessibility.md, "How this site is made".
# Open a GitHub issue, or rewrite the existing one instead of adding a duplicate.
# Each scheduled check owns one issue, found by its label.
#
#   scripts/upsert_issue.sh <label> <title> <body-file> [label-description]
#
# Needs the `gh` CLI (on GitHub runners by default) and GH_TOKEN, with
# `issues: write` in the workflow.
set -euo pipefail

LABEL="${1:?usage: upsert_issue.sh <label> <title> <body-file> [description]}"
TITLE="${2:?missing title}"
BODY_FILE="${3:?missing body file}"
DESCRIPTION="${4:-Opened automatically by a scheduled check}"

if [ ! -f "$BODY_FILE" ]; then
  echo "::error::No report at $BODY_FILE, refusing to open an empty issue."
  exit 1
fi

# The label is how we find our own issue again.
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
