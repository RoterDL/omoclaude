---
title: Add worktree support to spec skill
type: plan
category: 03-features
status: completed
phase: end
task_type: backend_only
created: 2026-03-11
tags: ["spec", "plan"]
---




# Add worktree support to spec skill

## Overview

`skills/spec` 的 Phase 3（Implementation）目前所有 agent 调用都直接在当前工作目录执行，没有 git worktree 隔离。`skills/do` 已经有完善的 worktree 支持（延迟到 Phase 4 决策、`enable-worktree` 命令、`DO_WORKTREE_DIR` 环境变量传递）。本任务将同样的能力引入 spec skill。

## Requirements

1. `spec-manager.py` 新增 `enable-worktree` 命令，创建 git worktree 并更新 plan.md frontmatter
2. `spec-manager.py` 的 `create_spec` 在 plan.md frontmatter 中预置 `use_worktree`/`worktree_dir` 字段
3. `SKILL.md` Phase 3 前增加 worktree 决策步骤
4. `SKILL.md` Phase 3 所有 agent 调用示例包含 worktree/非 worktree 两种写法
5. `status` 命令输出 worktree 信息

## Non-goals

- 不修改 codeagent-wrapper（已支持 `DO_WORKTREE_DIR`）
- 不修改 do skill
- Phase 1-2 不涉及 worktree（只读阶段）

## Design

### 1. spec-manager.py 修改

#### 1.1 新增 `create_worktree()` 函数

复用 do/task.py 的模式，但使用 `spec-` 前缀：

```python
def create_worktree(project_root: str, spec_name: str) -> str:
    """Create a git worktree for the spec. Returns worktree directory path."""
    git_root = subprocess.run(
        ["git", "-C", project_root, "rev-parse", "--show-toplevel"],
        capture_output=True, text=True
    ).stdout.strip()

    worktree_dir = os.path.join(git_root, ".worktrees", f"spec-{spec_name}")
    branch_name = f"spec/{spec_name}"

    subprocess.run(
        ["git", "-C", git_root, "worktree", "add", "-b", branch_name, worktree_dir],
        capture_output=True, text=True, check=True
    )
    return worktree_dir
```

- 路径：`.worktrees/spec-{YYYYMMDD-HHMM-slug}`
- 分支：`spec/{YYYYMMDD-HHMM-slug}`

#### 1.2 新增 `enable_worktree()` 函数

```python
def enable_worktree() -> bool:
    # 读取当前 spec
    # 若已启用 worktree，输出已有路径
    # 否则调用 create_worktree()
    # 更新 plan.md frontmatter：use_worktree=true, worktree_dir=<path>
    # 输出 export DO_WORKTREE_DIR=<path>
```

#### 1.3 修改 `create_spec()`

在 plan.md frontmatter 中添加：
```yaml
use_worktree: false
worktree_dir: ""
```

#### 1.4 修改 `get_status()`

输出增加 worktree 信息行。

#### 1.5 新增 CLI 子命令 `enable-worktree`

在 `main()` 的 argparse 中注册。

### 2. SKILL.md 修改

#### 2.1 增加 `## Worktree Mode` 章节

位置：在 "Hard Constraints" 之后。说明：
- worktree 决策延迟到 Phase 3（Implementation）
- Phase 1-2 只读，不需要 worktree
- 启用后所有写操作 agent 调用需要 `DO_WORKTREE_DIR` 前缀

#### 2.2 Hard Constraints 增加第 5 条

"Defer worktree decision until Phase 3. If enabled, prefix agent calls with `DO_WORKTREE_DIR=<path>`."

#### 2.3 Phase 3 Step 1 前插入 worktree 决策步骤

新增 "Step 0: Decide on worktree mode"：
- AskUserQuestion 询问是否使用 worktree
- 若是，调用 `spec-manager.py enable-worktree`
- 保存 DO_WORKTREE_DIR 值

#### 2.4 Phase 3 所有 agent 调用示例改为双模式

每个 agent 调用提供 "with worktree" 和 "without worktree" 两种示例。

#### 2.5 Agents 表增加 "Needs worktree" 列

标记哪些 agent 需要 worktree（do-develop, do-frontend, spec-tester），哪些不需要（explore, spec-planner, code-architect）。

#### 2.6 allowed-tools 更新

确保 `Bash(~/.claude/skills/spec/scripts/spec-manager.py:*)` 已覆盖（已有）。

## Implementation Steps (File Touch List)

| # | File | Changes |
|---|------|---------|
| 1 | `skills/spec/scripts/spec-manager.py` | +`import subprocess`, +`create_worktree()`, +`enable_worktree()`, modify `create_spec()` frontmatter, modify `get_status()`, +`enable-worktree` CLI subcommand |
| 2 | `skills/spec/SKILL.md` | +Worktree Mode section, +Hard Constraint #5, +Phase 3 worktree decision step, update agent call examples, +Agents table worktree column |

## Risks and Dependencies

1. **分支名过长**：spec_name 包含日期和 slug（如 `20260311-2117-add-worktree-support-to-spec-skill`），分支名为 `spec/20260311-2117-add-worktree-support-to-spec-skill`，git 可接受但较长。可接受，不需截断。
2. **codeagent-wrapper 兼容性**：`DO_WORKTREE_DIR` 已在 executor.go:982 被支持，无风险。
3. **无 worktree 清理**：与 do skill 一致，不自动清理 worktree，由用户手动管理。可后续增加。
