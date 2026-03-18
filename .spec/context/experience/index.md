---
title: Experience Index
type: index
updated: 2026-03-18
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
| exp-006 | Windows $HOME 解析与管道编码双重陷阱 | windows, $HOME, expanduser, stdin, encoding, surrogate, pipe, cross-platform | SKILL.md 中引用脚本路径或通过管道传递内容时 | 用 os.path.expanduser 替代 $HOME；添加 _read_stdin_safe()；优先 --file 代替 pipe |
| exp-007 | Orchestrator Mode 违规的补救路径 | orchestrator-mode, violation, spec, edit-write, codeagent-wrapper, remediation | /spec /do /omo 触发后误用 Edit/Write 直接修改源码 | 不回退正确改动，委托 reviewer 代理审查 diff 补救验证 |

## Category Index

### Frontend

### Backend

### Architecture Decisions
- [EXP-006] Windows $HOME 解析与管道编码双重陷阱
- [EXP-007] Orchestrator Mode 违规的补救路径
