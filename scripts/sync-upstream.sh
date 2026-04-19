#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SOURCE_REPO="${HERMES_SOURCE_REPO:-/Users/liyifan/hermes-agent}"
SYNC_FILE="$REPO_ROOT/.last-sync"
SUMMARY_FILE="$REPO_ROOT/scripts/changes-summary.md"

if [ ! -d "$SOURCE_REPO/.git" ]; then
  echo "ERROR: Source repo not found at $SOURCE_REPO"
  echo "Set HERMES_SOURCE_REPO to the hermes-agent repo path"
  exit 1
fi

cd "$SOURCE_REPO"

echo "Fetching latest from upstream..."
git fetch origin main

SYNC_FROM=$(cat "$SYNC_FILE" 2>/dev/null || git log -1 --format=%H HEAD)
SYNC_TO=$(git rev-parse origin/main)

if [ "$SYNC_FROM" = "$SYNC_TO" ]; then
  echo "Already up to date (both at $SYNC_FROM)"
  echo "# No changes since last sync" > "$SUMMARY_FILE"
  exit 0
fi

echo "Generating change summary: ${SYNC_FROM:0:8}..${SYNC_TO:0:8}"

cat > "$SUMMARY_FILE" <<EOF
# Changes since last sync

From: ${SYNC_FROM:0:12}
To:   ${SYNC_TO:0:12}
Date: $(date -u +%Y-%m-%dT%H:%M:%SZ)

## Commits

$(git log --format="- **%s** (%h)" "$SYNC_FROM..$SYNC_TO")

## Changed files

\`\`\`
$(git diff --stat "$SYNC_FROM..$SYNC_TO")
\`\`\`

## Full diff (for reference)

$(git diff "$SYNC_FROM..$SYNC_TO" -- . ':!.lock' ':!uv.lock' | head -3000)

[DIFF TRUNCATED - full diff has $(git diff --stat "$SYNC_FROM..$SYNC_TO" | tail -1) lines]
EOF

echo "$SYNC_TO" > "$SYNC_FILE"
echo ""
echo "Summary written to $SUMMARY_FILE"
echo "Last sync updated to ${SYNC_TO:0:12}"
