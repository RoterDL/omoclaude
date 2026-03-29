[中文](README_CN.md) [English](README.md)

# omoclaude

[![Repository](https://img.shields.io/badge/GitHub-RoterDL%2Fomoclaude-black)](https://github.com/RoterDL/omoclaude)
[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Claude Code](https://img.shields.io/badge/Claude-Code-blue)](https://claude.ai/code)
[![Version](https://img.shields.io/badge/Version-6.x-green)](https://github.com/RoterDL/omoclaude)

> AI-powered development automation with multi-backend execution (Codex/Claude/Gemini/OpenCode)

## Quick Start

```bash
python install.py
```

Project repository: https://github.com/RoterDL/omoclaude  
Original upstream project: https://github.com/stellarlinkco/myclaude

## Modules Overview

| Module | Description | Documentation |
|--------|-------------|---------------|
| [do](skills/do/README.md) | **Recommended** - 5-phase feature development with codeagent orchestration | `/do` command |
| [omo](skills/omo/README.md) | Multi-agent orchestration with intelligent routing and quick-first exploration | `/omo` command |
| [codeagent](skills/codeagent/SKILL.md) | Focused implementation skill using codeagent-wrapper | `skill:codeagent` or `module:codeagent` |
| [research-pro](skills/research-pro/README.md) | Multi-agent academic research orchestration | `/research-pro` command |
| [taste](skills/taste/) | Frontend design quality rules — plan-phase paradigms + implement-phase guardrails | Dependency of `do` |
| [cr](skills/cr/README.md) | Automated code review with single-agent and multi-agent modes | `/cr` command |
| [spec](skills/spec/README.md) | Spec-driven development lifecycle with gate-controlled phases | `/spec` command |
| [memory](skills/memory/README.md) | Dual-layer structured memory system (experience/knowledge) | `/exp-search`, `/exp-reflect`, `/exp-write` |
| [project-init](skills/project-init/README.md) | One-time project initialization for `.spec/` directory structure | `/project-init` command |

## Available Skills

Installable skills in this repository:

| Skill | Description |
|-------|-------------|
| do | 5-phase feature development workflow |
| omo | Multi-agent orchestration workflow |
| codeagent | Focused implementation with codeagent-wrapper |
| research-pro | Multi-agent academic research orchestration |
| taste | Frontend design quality rules — 6 injectable sub-skills: plan-phase (`taste-creative`, `taste-brutalist`, `taste-minimalist`) + implement-phase (`taste-core`, `taste-output`, `taste-redesign`) |
| cr | Automated code review — single-agent interactive fix or multi-agent adversarial review with auto-fix |
| spec | Spec-driven development lifecycle: Intent -> Plan -> Implement -> End |
| memory | Dual-layer structured memory — 3 skills (`exp-search`, `exp-reflect`, `exp-write`) |
| project-init | One-time `.spec/` directory initialization with memory indexes and coding rules |

## Installation

```bash
# Interactive installer (recommended)
python install.py

# List available modules
python install.py --list-modules

# Install selected modules
python install.py --module do,omo,codeagent

# Custom install directory / overwrite
python install.py --install-dir ~/.claude --module do --force

# Update installed modules
python install.py --update

# Uninstall selected modules
python uninstall.py --module do,omo
```

`--update` detects already installed modules in the target install dir (defaults to `~/.claude`, via `installed_modules.json` when present) and updates module files.

### Module Configuration

Edit `config.json` to enable/disable modules:

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

## Workflow Selection Guide

| Scenario | Recommended |
|----------|-------------|
| Feature development (default) | `/do` |
| Bug investigation + fix | `/omo` |
| Code review (branch / PR / files) | `/cr` |
| Academic paper reading / review / literature search | `/research-pro` |
| Focused single-track implementation | `skill:codeagent` |
| Spec-driven feature development | `/spec` |
| Project initialization (first-time setup) | `/project-init` |
| Search project memory / capture experience | `/exp-search`, `/exp-reflect` |

## Core Architecture

| Role | Agent | Responsibility |
|------|-------|----------------|
| **Orchestrator** | Claude Code | Planning, context gathering, verification |
| **Executor** | codeagent-wrapper | Code editing, test execution (Codex/Claude/Gemini/OpenCode) |

## Backend CLI Requirements

| Backend | Required Features |
|---------|-------------------|
| Codex | `codex e`, `--json`, `-C`, `resume` |
| Claude | `--output-format stream-json`, `-r` |
| Gemini | `-o stream-json`, `-y`, `-r` |
| OpenCode | `opencode`, stdin mode |

## Directory Structure After Installation

```text
~/.claude/
├── bin/codeagent-wrapper
├── CLAUDE.md              (installed by default)
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
├── settings.json          (auto-generated, hooks config)
└── installed_modules.json (auto-generated, tracks modules)
```

## Documentation

- [skills](skills/README.md)
- [codeagent-wrapper](codeagent-wrapper/README.md)

## Troubleshooting

**Module not loading:**
```bash
cat ~/.claude/installed_modules.json
python install.py --module do --force
```

**Backend CLI errors:**
```bash
which codex && codex --version
which claude && claude --version
which gemini && gemini --version
which opencode && opencode --version
```

## Acknowledgments

The skills in this project are primarily inspired by the following repositories:

- [stellarlinkco/myclaude](https://github.com/stellarlinkco/myclaude)
- [HHU3637kr/skills](https://github.com/HHU3637kr/skills)
- [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill)

## License

AGPL-3.0 - see [LICENSE](LICENSE)

## Support

- [GitHub Issues](https://github.com/RoterDL/omoclaude/issues)
