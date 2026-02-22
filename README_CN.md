# Claude Code 多智能体工作流系统

[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Claude Code](https://img.shields.io/badge/Claude-Code-blue)](https://claude.ai/code)
[![Version](https://img.shields.io/badge/Version-6.x-green)](https://github.com/cexll/myclaude)

> AI 驱动的开发自动化 - 多后端执行架构 (Codex/Claude/Gemini/OpenCode)

## 快速开始

```bash
npx github:cexll/myclaude
```

## 模块概览

| 模块 | 描述 | 文档 |
|------|------|------|
| [do](skills/do/README.md) | **推荐** - 5 阶段功能开发 + codeagent 编排 | `/do` 命令 |
| [omo](skills/omo/README.md) | 多智能体编排 + 智能路由 | `/omo` 命令 |
| claudekit | ClaudeKit：do 技能 + 全局钩子（pre-bash、inject-spec、log-prompt）| 组合模块 |

## 核心架构

| 角色 | 智能体 | 职责 |
|------|-------|------|
| **编排者** | Claude Code | 规划、上下文收集、验证 |
| **执行者** | codeagent-wrapper | 代码编辑、测试执行（Codex/Claude/Gemini/OpenCode 后端）|

## 工作流详解

### do 工作流（推荐）

5 阶段功能开发，通过 codeagent-wrapper 编排多个智能体。**大多数功能开发任务的首选工作流。**

```bash
/do "添加用户登录功能"
```

**5 阶段：**
| 阶段 | 名称 | 目标 |
|------|------|------|
| 1 | Understand | 并行探索理解需求和映射代码库 |
| 2 | Clarify | 解决阻塞性歧义（条件触发）|
| 3 | Design | 产出最小变更实现方案 |
| 4 | Implement + Review | 构建功能并审查 |
| 5 | Complete | 记录构建结果 |

**智能体：**
- `code-explorer` - 代码追踪、架构映射
- `code-architect` - 设计方案、文件规划
- `code-reviewer` - 代码审查、简化建议
- `develop` - 实现代码、运行测试

---

### OmO 多智能体编排器

基于风险信号智能路由任务到专业智能体。

```bash
/omo "分析并修复这个认证 bug"
```

**智能体层级：**
| 智能体 | 角色 | 后端 |
|-------|------|------|
| `oracle` | 技术顾问 | Claude |
| `librarian` | 外部研究 | Claude |
| `explore` | 代码库搜索 | OpenCode |
| `develop` | 代码实现 | Codex |
| `frontend-ui-ux-engineer` | UI/UX 专家 | Gemini |
| `document-writer` | 文档撰写 | Gemini |

**常用配方：**
- 解释代码：`explore`
- 位置已知的小修复：直接 `develop`
- Bug 修复（位置未知）：`explore → develop`
- 跨模块重构：`explore → oracle → develop`

---

## 工作流选择指南

| 场景 | 推荐 |
|------|------|
| 功能开发（默认） | `/do` |
| Bug 调查 + 修复 | `/omo` |

## 安装

```bash
# 交互式安装器（推荐）
npx github:cexll/myclaude

# 列出可安装项（module:* / skill:* / codeagent-wrapper）
npx github:cexll/myclaude --list

# 检测已安装 modules 并从 GitHub 更新
npx github:cexll/myclaude --update

# 指定安装目录 / 强制覆盖
npx github:cexll/myclaude --install-dir ~/.claude --force
```

`--update` 会在目标安装目录（默认 `~/.claude`，优先读取 `installed_modules.json`）检测已安装 modules，并从 GitHub 拉取最新发布版本覆盖更新。

### 模块配置

编辑 `config.json` 启用/禁用模块：

```json
{
  "modules": {
    "omo": { "enabled": false },
    "do": { "enabled": true },
    "claudekit": { "enabled": false }
  }
}
```

## 后端 CLI 要求

| 后端 | 必需功能 |
|------|----------|
| Codex | `codex e`, `--json`, `-C`, `resume` |
| Claude | `--output-format stream-json`, `-r` |
| Gemini | `-o stream-json`, `-y`, `-r` |
| OpenCode | `opencode`, stdin 模式 |

## 故障排查

**Codex wrapper 未找到：**
```bash
# 选择：codeagent-wrapper
npx github:cexll/myclaude
```

**模块未加载：**
```bash
cat ~/.claude/installed_modules.json
npx github:cexll/myclaude --force
```

## FAQ

| 问题 | 解决方案 |
|------|----------|
| "Unknown event format" | 日志显示问题，可忽略 |
| Gemini 无法读取 .gitignore 文件 | 从 .gitignore 移除或使用其他后端 |
| Codex 权限拒绝 | 在 ~/.codex/config.yaml 设置 `approval_policy = "never"` |

更多问题请访问 [GitHub Issues](https://github.com/cexll/myclaude/issues)。

## 许可证

AGPL-3.0 - 查看 [LICENSE](LICENSE)

### 商业授权

如需商业授权（无需遵守 AGPL 义务），请联系：evanxian9@gmail.com

## 支持

- [GitHub Issues](https://github.com/cexll/myclaude/issues)
