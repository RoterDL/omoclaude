# omoclaude

[![Repository](https://img.shields.io/badge/GitHub-RoterDL%2Fomoclaude-black)](https://github.com/RoterDL/omoclaude)

[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Claude Code](https://img.shields.io/badge/Claude-Code-blue)](https://claude.ai/code)
[![Version](https://img.shields.io/badge/Version-6.x-green)](https://github.com/RoterDL/omoclaude)

> AI 驱动的开发自动化，多后端执行架构 (Codex/Claude/Gemini/OpenCode)

## 快速开始

```bash
python install.py
```

本项目仓库：https://github.com/RoterDL/omoclaude  
原始上游项目：https://github.com/cexll/myclaude

## 模块概览

| 模块 | 描述 | 文档 |
|------|------|------|
| [do](skills/do/README.md) | 推荐：5 阶段功能开发 + codeagent 编排 | `/do` 命令 |
| [omo](skills/omo/README.md) | 多智能体编排 + 智能路由 | `/omo` 命令 |
| [codeagent](skills/codeagent/SKILL.md) | 面向实现任务的精简技能，依赖 codeagent-wrapper | `skill:codeagent` 或 `module:codeagent` |
| [research-pro](skills/research-pro/README.md) | 多智能体学术研究编排 | `/research-pro` 命令 |
| [taste](skills/taste/) | 前端设计质量规则 — 规划阶段设计范式 + 实现阶段代码护栏 | `do` 的依赖 |
| [cr](skills/cr/README.md) | 自动代码审查，支持单智能体和多智能体模式 | `/cr` 命令 |
| [spec](skills/spec/README.md) | Spec 驱动开发生命周期，4 阶段门控 | `/spec` 命令 |
| [memory](skills/memory/README.md) | 双层结构化记忆系统（经验/知识） | `/exp-search`、`/exp-reflect`、`/exp-write` |
| [project-init](skills/project-init/README.md) | 一次性项目初始化，创建 `.spec/` 目录结构 | `/project-init` 命令 |

## 可用技能

当前仓库包含以下技能：

| 技能 | 描述 |
|------|------|
| do | 5 阶段功能开发工作流 |
| omo | 多智能体编排工作流 |
| codeagent | 基于 codeagent-wrapper 的实现型技能 |
| research-pro | 多智能体学术研究编排 |
| taste | 前端设计质量规则 — 6 个可注入子技能：规划阶段（`taste-creative`、`taste-brutalist`、`taste-minimalist`）+ 实现阶段（`taste-core`、`taste-output`、`taste-redesign`） |
| cr | 自动代码审查 — 单智能体交互式修复或多智能体对抗式审查 + 自动修复 |
| spec | Spec 驱动开发生命周期：意图确认 -> 设计规划 -> 实现 -> 收尾 |
| memory | 双层结构化记忆 — 3 个技能（`exp-search`、`exp-reflect`、`exp-write`） |
| project-init | 一次性 `.spec/` 目录初始化，含记忆索引和编码规则模板 |

## 安装

```bash
# 交互式安装器（推荐）
python install.py

# 列出可用模块
python install.py --list-modules

# 安装指定模块
python install.py --module do,omo,codeagent

# 指定安装目录 / 强制覆盖
python install.py --install-dir ~/.claude --module do --force

# 更新已安装模块
python install.py --update

# 卸载指定模块
python uninstall.py --module do,omo
```

`--update` 会在目标安装目录（默认 `~/.claude`，优先读取 `installed_modules.json`）检测已安装 modules，并覆盖更新模块文件。

### 模块配置

编辑 `config.json` 启用或禁用模块：

```json
{
  "modules": {
    "do": { "enabled": true },
    "omo": { "enabled": false },
    "cr": { "enabled": true },
    "codeagent": { "enabled": false },
    "research-pro": { "enabled": true },
    "taste": { "enabled": true },
    "spec": { "enabled": true },
    "memory": { "enabled": true },
    "project-init": { "enabled": true }
  }
}
```

## 工作流选择指南

| 场景 | 推荐 |
|------|------|
| 功能开发（默认） | `/do` |
| Bug 调查与修复 | `/omo` |
| 代码审查（分支 / PR / 文件） | `/cr` |
| 论文阅读 / 论文审查 / 文献检索 | `/research-pro` |
| 单轨实现任务 | `skill:codeagent` |
| Spec 驱动的功能开发 | `/spec` |
| 项目初始化（首次设置） | `/project-init` |
| 搜索项目记忆 / 捕获经验 | `/exp-search`、`/exp-reflect` |

## 核心架构

| 角色 | 智能体 | 职责 |
|------|--------|------|
| 编排者 | Claude Code | 规划、上下文收集、验证 |
| 执行者 | codeagent-wrapper | 代码编辑、测试执行（Codex/Claude/Gemini/OpenCode） |

## 后端 CLI 要求

| 后端 | 必需能力 |
|------|----------|
| Codex | `codex e`, `--json`, `-C`, `resume` |
| Claude | `--output-format stream-json`, `-r` |
| Gemini | `-o stream-json`, `-y`, `-r` |
| OpenCode | `opencode`, stdin 模式 |

## 安装后目录结构

```text
~/.claude/
├── bin/codeagent-wrapper
├── CLAUDE.md              (默认安装)
├── skills/
│   ├── do/
│   ├── omo/
│   ├── research-pro/
│   ├── codeagent/
│   ├── cr/
│   ├── spec/
│   ├── project-init/
│   ├── exp-search/
│   ├── exp-reflect/
│   ├── exp-write/
│   ├── taste-core/
│   ├── taste-output/
│   ├── taste-creative/
│   ├── taste-redesign/
│   ├── taste-brutalist/
│   └── taste-minimalist/
├── settings.json          (自动生成，hooks 配置)
└── installed_modules.json (自动生成，记录已装模块)
```

## 文档

- [skills](skills/README.md)
- [codeagent-wrapper](codeagent-wrapper/README.md)
- [插件系统](PLUGIN_README.md)

## 故障排查

**模块未生效：**
```bash
cat ~/.claude/installed_modules.json
python install.py --module do --force
```

**后端 CLI 异常：**
```bash
which codex && codex --version
which claude && claude --version
which gemini && gemini --version
which opencode && opencode --version
```

## 许可证

AGPL-3.0，见 [LICENSE](LICENSE)

### 商业授权

如需商业授权（无需遵守 AGPL 义务），请联系：evanxian9@gmail.com

## 支持

- [GitHub Issues](https://github.com/RoterDL/omoclaude/issues)
