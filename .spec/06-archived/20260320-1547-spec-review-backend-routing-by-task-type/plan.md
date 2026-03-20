---
title: spec-review-backend-routing-by-task-type
type: plan
category: 03-features
status: testing
phase: test
created: 2026-03-20
tags: ["spec", "plan"]
use_worktree: false
worktree_dir: 
---




# Review Backend Routing by task_type

## Overview

在 `skills/spec/SKILL.md` 的审核环节（计划审核 Phase 2 Step 5 + 代码审核 Phase 3 Step 5），standard 强度下增加 `task_type` 路由逻辑：前端任务走 `--backend claude`，后端任务走 `--backend codex`，fullstack 分别审。

## Requirements

1. Phase 2 Step 5（计划审核，standard 强度）：根据 `task_type` 添加 `--backend` 参数
2. Phase 3 Step 5（代码审核，standard 强度）：根据 `task_type` 添加 `--backend` 参数
3. 路由规则：
   - `frontend_only` → `--backend claude`
   - `backend_only` → `--backend codex`
   - `fullstack` → 分别调用两次，各带对应 `--backend`
4. light/full 强度不受影响
5. 具体模型由 config.json agent 定义控制，SKILL.md 只指定 `--backend`

## Design

### Phase 2 Step 5 变更

在 `standard or full intensity` 分支中，standard 子分支内加入 task_type 判断：
- 读取 plan.md 的 `task_type`
- 单类型：`codeagent-wrapper --agent plan-reviewer --backend {backend} ...`
- fullstack：两次调用，分别 `--backend claude`（前端范围）和 `--backend codex`（后端范围），prompt 中注明审核范围

### Phase 3 Step 5 变更

在 standard 强度分支中加入 task_type 判断：
- 单类型：`codeagent-wrapper --agent spec-reviewer-lite --backend {backend} ...`
- fullstack：两次调用，分别带对应 `--backend`，prompt 中注明审核范围（frontend/backend scope）

### full 强度处理

full 强度使用 `spec-reviewer-deep`，不在本次变更范围内。保持原有逻辑不变。

## Implementation Steps

| # | File | Change |
|---|------|--------|
| 1 | `skills/spec/SKILL.md` | Phase 2 Step 5: standard 分支增加 task_type 路由 |
| 2 | `skills/spec/SKILL.md` | Phase 3 Step 5: standard 分支增加 task_type 路由 |

## Task Classification

- task_type: backend_only
- review_intensity: light
- estimated_scope: ~40 lines changed in 1 file

## Risks

- fullstack 双审核增加 agent 调用次数，但仅在 standard+fullstack 组合时触发

## Non-goals

- 不修改 config.json 中的 agent backend/model 配置
- 不修改 light/full 强度的审核逻辑
- 不修改 `spec-reviewer-deep` 的路由
