---
id: EXP-007
title: Orchestrator Mode 违规的补救路径
keywords: [orchestrator-mode, violation, spec, edit-write, codeagent-wrapper, remediation]
scenario: /spec /do /omo 触发后误用 Edit/Write 直接修改源码
created: 2026-03-18
---

# Orchestrator Mode 违规的补救路径

## Dilemma

`/spec` 触发后应处于 Orchestrator Mode，所有代码修改必须通过 `codeagent-wrapper` 代理执行。但实际操作中直接使用 Edit 工具修改了 5 个源文件（spec-manager.py、SKILL.md、sub-skills、capture-diff.sh、README.md），违反了 CLAUDE.md 的 Execution Mode Switch 规则和 spec 的 Hard Constraint #1。

## Strategy

1. **不盲目回退**：改动方向已确认正确且已完成，回退+重来成本高
2. **委托审查补救**：调用 `codeagent-wrapper --agent spec-reviewer-lite` 审查完整 diff，验证改动质量
3. **修复审查问题**：审查返回 BLOCKING=0, MINOR=2（未使用的 `import io`、`reconfigure` 异常捕获范围窄），立即修复
4. **提交并记录**：修复后正常提交，并记录此经验防止复发
5. **未来纪律**：/spec /do /omo 下所有代码修改必须走 `codeagent-wrapper --agent develop`，无例外

## Reasoning

回退+重来的成本远高于补救验证：改动已经存在、方向正确、逻辑简单。审查代理提供了独立的质量验证视角，等效于 Phase 3 的 code review 环节。关键教训是模式切换的纪律意识——触发 skill 后应立即检查自身处于哪种执行模式。

## Related Files

- `CLAUDE.md` (Execution Mode Switch 规则)
- `skills/spec/SKILL.md:9-10` (Hard Constraint #1: Never write code directly)

## References

- Commit: 2248ee4 fix(spec): fix Windows $HOME path resolution and stdin encoding issues
