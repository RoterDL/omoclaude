---
title: Experience Index
type: index
updated: 2026-03-17
---

# Experience Index

> Use `/exp-search <keywords>` to retrieve related experience.
> This file is maintained by exp-write.

## Index Table

| ID | Title | Keywords | Applicable Scenario | One-line Strategy |
|----|-------|----------|-------------------|------------------|
| exp-001 | Timing Dependency in Gated Mechanisms | timing, gating, review_intensity | Gating decision depends on downstream value | Separate into two independent mechanisms with distinct timing points |
| exp-002 | Script Extraction Requires allowed-tools Update | allowed-tools, script extraction | Extracting inline code to separate script | Add new script path to allowed-tools frontmatter |
| exp-003 | POSIX vs Bash Shebang Mismatch | shebang, POSIX, bash | Shell scripts with Bash-specific syntax | Use #!/bin/bash when any Bashism is present |
| exp-004 | Local Artifact vs System Persistence Distinction | write-artifact, exp-write, persistence, dual-write | Replacing a persistence tool call with a simpler alternative | Distinguish local artifact save from system-level persistence; use dual-write when both needed |
| exp-005 | Source vs Installed Copy Drift | install, source, copy, drift, spec-manager | Adding new features to skill infrastructure scripts | Use source path directly or re-install before testing new subcommands |

## Category Index

### Frontend

### Backend

### Architecture Decisions
