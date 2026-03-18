---
id: EXP-006
title: Windows 平台 SKILL.md 命令模板的 $HOME 解析与管道编码双重陷阱
keywords: [windows, $HOME, expanduser, stdin, encoding, surrogate, pipe, cross-platform]
scenario: SKILL.md 中引用脚本路径或通过管道传递内容时
created: 2026-03-18
---

# Windows 平台 SKILL.md 命令模板的 $HOME 解析与管道编码双重陷阱

## Dilemma

Windows Git Bash 下 `$HOME` 解析为 `C:\Program Files\Git\` 而非用户主目录（`C:\Users\<username>`），导致 `python "$HOME/.claude/skills/spec/scripts/spec-manager.py"` 找不到脚本文件。同时，stdin 管道使用系统 code page（如 cp936）传输中文内容，Python `sys.stdin.read()` 产生 surrogate 字符（如 `\udcae`），在 `write_plan_md` 写回 UTF-8 时抛出 `surrogates not allowed` 错误。

## Strategy

1. **路径解析**：用 `python -c "import os;print(os.path.expanduser('~/<path>'))"` 替代 `$HOME`，在 SKILL.md 中定义 `$SPEC_MGR` 变量模式，每次 Bash 调用内联解析
2. **编码处理**：在 `spec-manager.py` 中添加 `_read_stdin_safe()` 函数，Windows 下强制 `sys.stdin.reconfigure(encoding='utf-8', errors='replace')`，回退到 `sys.stdin.buffer.read().decode('utf-8', errors='replace')`
3. **模板优化**：SKILL.md 中所有 `echo '...' | python ... write-artifact` 管道模式改为 `--file` 模式
4. **全面替换**：所有 SKILL.md/sub-skills/README/capture-diff.sh 中的 `$HOME` 引用统一替换

## Reasoning

Python `os.path.expanduser('~')` 在 Windows 上读取 `USERPROFILE` 环境变量，绕过 Git Bash 的 `HOME` 环境变量错误解析。`--file` 模式直接读取文件（`open(path, encoding='utf-8')`），完全避免管道编码链条中的 code page 转换问题。

## Related Files

- `skills/spec/scripts/spec-manager.py:25-43` (_read_stdin_safe 函数)
- `skills/spec/SKILL.md:28-35` (Script Path Resolution 段)
- `skills/spec/sub-skills/spec-end/SKILL.md:43`
- `skills/spec/scripts/capture-diff.sh:3-4`
- `skills/spec/README.md:126-145` (Platform Compatibility 表)

## References

- Commit: 2248ee4 fix(spec): fix Windows $HOME path resolution and stdin encoding issues
