# Summary: Review Backend Routing by task_type

## Implemented Scope
在 `skills/spec/SKILL.md` 中为计划审核（Phase 2 Step 5）和代码审核（Phase 3 Step 5）增加了 task_type 路由逻辑。

## Changes
- **skills/spec/SKILL.md** (+141/-6 lines)
  - Phase 2 Step 5 (L124-213): standard/full 强度下 plan-reviewer 根据 task_type 路由 --backend (frontend→claude, backend→codex, fullstack→双审合并)
  - Phase 3 Step 5 (L303-400): standard/full 强度下 spec-reviewer-lite/deep 根据 task_type 路由 --backend，fullstack 双审合并到 review-report.md

## Key Design Decisions
- 路由表放在 light skip 之后、standard/full 调用之前，逻辑清晰
- fullstack 双审结果通过 temp 文件合并后统一保存为单个 artifact
- full 强度的迭代重审也使用 routed calls
