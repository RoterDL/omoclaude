---
title: spec-explorer agent prompt and config registration
type: plan
category: 03-features
status: completed
phase: end
created: 2026-03-12
tags: ["spec", "plan"]
use_worktree: false
worktree_dir: 
---




# Plan: Spec-Explorer Agent — Prompt and Config Registration

## 1. Overview

### Background
`spec` 模块当前借用 `omo` 模块的 `explore` agent 做 Phase 2 代码探索。这造成隐式跨模块依赖——`spec` 声明 `dependencies: ["memory"]`，但实际需要 `omo` 已安装才能使用 `explore` agent。同时 `omo/explore` 偏向搜索（并行搜索策略、intent analysis tags），而 `do/code-explorer` 的深度架构分析（4步分析、Summary footer、YAML frontmatter）更适合 spec 规划场景。

### Goals
1. 创建自包含的 `spec-explorer` agent，融合两个 agent 的优势
2. 在 `config.json` 的 `modules.spec.agents` 下注册
3. 更新 `SKILL.md` 中所有 `explore` 引用为 `spec-explorer`
4. 消除 spec 对 omo 的隐式依赖

### Scope
- **In scope**: 新 agent prompt 文件、config 注册、SKILL.md 更新
- **Out of scope**: 不改动 omo/explore.md、do/code-explorer.md 或其他模块

## 2. Requirements Analysis

### Functional Requirements
| ID | Requirement |
|----|-------------|
| FR1 | `spec-explorer.md` 位于 `skills/spec/references/spec-explorer.md` |
| FR2 | config.json 注册：backend=claude, model=claude-sonnet-4-6 |
| FR3 | SKILL.md 中所有 `explore` agent 引用替换为 `spec-explorer` |
| FR4 | prompt 融合 code-explorer 的 4 步分析 + explore 的输入契约 |
| FR5 | 包含 `Summary:` footer（兼容 --parallel） |
| FR6 | 包含 YAML frontmatter |
| FR7 | 包含 Sisyphus 输入契约 |
| FR8 | 只读 agent，禁止写文件/生成代码 |
| FR9 | 叙事分析为主，末尾附精简文件列表摘要 |

### Constraints
- claude-sonnet-4-6 / claude backend
- 无需并行搜索策略
- prompt 位于 `skills/spec/references/`

## 3. Design Approach

### Prompt 结构

```
---
name: spec-explorer
description: ...
tools: Glob, Grep, Read, Bash
model: sonnet
---

# Spec-Explorer — Codebase Analysis for Spec Planning

## Input Contract (from explore.md)
## Repo Root & Rules Discovery (from code-explorer.md)
## Core Mission (adapted for spec context)
## Analysis Approach (code-explorer 4-step)
  1. Feature Discovery
  2. Code Flow Tracing
  3. Architecture Analysis
  4. Implementation Details
## Output Format
  - Narrative analysis body
  - File list summary (markdown, not XML)
  - Summary: one-liner footer
## Constraints (merged, deduplicated)
## Tool Restrictions (merged)
## Thoroughness Levels (from explore.md)
```

### Key Design Decisions
- **不用 `<analysis>` intent tags**：spec 工作流已通过输入契约提供明确意图
- **不用 `<results>` XML 标签**：改用 markdown 文件列表，更可读
- **保留 thoroughness levels**：便于 spec 工作流按需调节探索深度
- **保留 `Summary:` footer**：兼容 `--parallel` 模式

### Alternatives Considered
1. 直接 fork explore.md → 缺少 code-explorer 的分析深度
2. 直接 fork code-explorer.md → 缺少输入契约和结构化输出
3. 使用 symlink → 不解决质量差距和自包含问题

## 4. Implementation Steps

### Step 1: 创建 `skills/spec/references/spec-explorer.md` (NEW)
YAML frontmatter + 输入契约 + 4步分析 + 输出格式 + 约束

### Step 2: 更新 `config.json` — 添加 spec-explorer agent
在 `modules.spec.agents` 下添加：
```json
"spec-explorer": {
  "backend": "claude",
  "model": "claude-sonnet-4-6",
  "prompt_file": "~/.claude/skills/spec/references/spec-explorer.md"
}
```

### Step 3: 更新 `skills/spec/SKILL.md` — 替换 explore 为 spec-explorer
8 处引用需更新：
- Line 18: agent 列表
- Line 22: codeagent-wrapper 命令
- Line 28: 跳过探索警告
- Line 29: 内置 Agent 警告
- Line 49: worktree 示例
- Line 63: 生命周期图
- Lines 122-136: Phase 2 Step 2 完整代码块
- Line 512: Agents Used 表格

### Build Sequence
1 → 2 → 3（逻辑顺序：创建 prompt → 注册 → 接线）

## 5. Task Classification
- **task_type**: `backend_only`
- 全部为 markdown/JSON 配置文件变更

## 6. Risks

| Risk | Impact | Mitigation |
|------|--------|------------|
| prompt 合并后过于冗长 | Low | 主动去重，code-explorer 已很精简 |
| 进行中的 spec 引用旧 explore | Low | omo 的 explore 不变，仅新 spec 使用 spec-explorer |
| codeagent-wrapper 找不到 agent | Medium | 验证 config.json 注册与 agent 解析逻辑一致 |

## 7. Non-goals
- 不修改 omo/explore.md 或 do/code-explorer.md
- 不在 spec 以外的模块添加 spec-explorer
- 不改变 spec 生命周期阶段或门控逻辑
- 不更新 README（如需，另开任务）
