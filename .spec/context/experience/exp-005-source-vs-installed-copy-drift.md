---
id: EXP-005
title: Source vs Installed Copy Drift
keywords: [install, source, copy, drift, spec-manager, stale]
scenario: Adding new features to skill infrastructure scripts
created: 2026-03-16
---

# Source vs Installed Copy Drift

## Dilemma

Added `write-artifact` subcommand to `skills/spec/scripts/spec-manager.py` in the source repo. When the orchestrator called `$HOME/.claude/skills/spec/scripts/spec-manager.py write-artifact`, it failed because the installed copy at `~/.claude/skills/` was stale — it didn't have the new subcommand.

## Strategy

1. After modifying skill infrastructure scripts in the source repo, use the source path directly for testing (e.g., `python skills/spec/scripts/spec-manager.py` instead of `$HOME/.claude/skills/spec/scripts/spec-manager.py`).
2. Alternatively, re-run `install.py` to sync the installed copy before testing.
3. Always verify which copy is being executed when a "command not found" or "invalid choice" error occurs on a newly added feature.

## Reasoning

The omoclaude project has a two-location architecture: source in the repo, installed copies in `~/.claude/skills/`. The installer (`install.py`) copies from source to installed location. During development, the source is modified first, but the runtime environment may still reference the installed copy. This drift is expected but must be accounted for.

## Related Files

- skills/spec/scripts/spec-manager.py (source)
- ~/.claude/skills/spec/scripts/spec-manager.py (installed copy)
- install.py (syncs source to installed)

## References

- Runtime error during optimize-spec-skill-md-v2 implementation
