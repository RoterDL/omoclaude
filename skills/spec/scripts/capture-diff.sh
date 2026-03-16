#!/bin/bash
# capture-diff.sh — Capture tracked and untracked changes for code review
# Usage: DIFF_OUTPUT=$(bash "$HOME/.claude/skills/spec/scripts/capture-diff.sh")
# Env: DO_WORKTREE_DIR (optional) — if set, operates on the worktree directory

if [ -n "$DO_WORKTREE_DIR" ]; then
  BASE_DIR="$DO_WORKTREE_DIR"
  DIFF_OUTPUT=$(git -C "$DO_WORKTREE_DIR" diff HEAD)
  UNTRACKED=$(git -C "$DO_WORKTREE_DIR" status --porcelain | grep '^??')
else
  BASE_DIR="."
  DIFF_OUTPUT=$(git diff HEAD)
  UNTRACKED=$(git status --porcelain | grep '^??')
fi

if [ -n "$UNTRACKED" ]; then
  NEW_FILES_CONTENT="--- Untracked new files ---"
  while IFS= read -r line; do
    filepath="${line#\?\? }"
    NEW_FILES_CONTENT="$NEW_FILES_CONTENT
--- new file: $filepath ---
$(cat "$BASE_DIR/$filepath")"
  done <<< "$UNTRACKED"
  DIFF_OUTPUT="$DIFF_OUTPUT
$NEW_FILES_CONTENT"
fi

printf '%s\n' "$DIFF_OUTPUT"
