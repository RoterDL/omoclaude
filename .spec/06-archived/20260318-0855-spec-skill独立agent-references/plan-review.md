# Plan Review Report

## BLOCKING (1)

**[Implementation Steps]** Step 8 把 config.json 变更写成"mirror do module's backend/model settings"，但 `do-develop` 的注册项还带有 `reasoning` 和 `yolo` 等行为元数据。计划要求新 agent 与 `/do` 版本 functionally equivalent，因此必须明确为"复制完整 agent metadata"。

## MINOR (3)

1. **[Requirements Analysis]** FR-9 声称需要让 spec 模块不依赖 do，但当前 `spec.dependencies` 已经只有 `memory`。建议改成验证项。

2. **[Implementation Steps]** Step 7 漏掉 `skills/spec/README.md` 安装章节中的 spec agents 枚举更新。

3. **[Implementation Steps]** Steps 1-3 没有显式要求更新 prompt 内部的 `name:` 标识和 `/do` 调用描述。

Summary: BLOCKING=1, MINOR=3
