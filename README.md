[中文](README_CN.md) [English](README.md)

# omoclaude

[![Repository](https://img.shields.io/badge/GitHub-RoterDL%2Fomoclaude-black)](https://github.com/RoterDL/omoclaude)
[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL_v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)
[![Claude Code](https://img.shields.io/badge/Claude-Code-blue)](https://claude.ai/code)
[![Version](https://img.shields.io/badge/Version-6.x-green)](https://github.com/RoterDL/omoclaude)

> AI-powered development automation with multi-backend execution (Codex/Claude/Gemini/OpenCode)

## Quick Start

```bash
python3 install.py
```

Project repository: https://github.com/RoterDL/omoclaude  
Original upstream project: https://github.com/cexll/myclaude

## Modules Overview

| Module | Description | Documentation |
|--------|-------------|---------------|
| [do](skills/do/README.md) | **Recommended** - 5-phase feature development with codeagent orchestration | `/do` command |
| [omo](skills/omo/README.md) | Multi-agent orchestration with intelligent routing | `/omo` command |
| [codeagent](skills/codeagent/SKILL.md) | Focused implementation skill using codeagent-wrapper | `skill:codeagent` or `module:codeagent` |

## Available Skills

Installable skills in this repository:

| Skill | Description |
|-------|-------------|
| do | 5-phase feature development workflow |
| omo | Multi-agent orchestration workflow |
| codeagent | Focused implementation with codeagent-wrapper |

## Installation

```bash
# Interactive installer (recommended)
python3 install.py

# List available modules
python3 install.py --list-modules

# Install selected modules
python3 install.py --module do,omo,codeagent

# Custom install directory / overwrite
python3 install.py --install-dir ~/.claude --module do --force

# Update installed modules
python3 install.py --update

# Uninstall selected modules
python3 uninstall.py --module do,omo
```

`--update` detects already installed modules in the target install dir (defaults to `~/.claude`, via `installed_modules.json` when present) and updates module files.

### Module Configuration

Edit `config.json` to enable/disable modules:

```json
{
  "modules": {
    "do": { "enabled": true },
    "omo": { "enabled": false },
    "codeagent": { "enabled": false }
  }
}
```

## Workflow Selection Guide

| Scenario | Recommended |
|----------|-------------|
| Feature development (default) | `/do` |
| Bug investigation + fix | `/omo` |
| Focused single-track implementation | `skill:codeagent` |

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
│   └── codeagent/
├── settings.json          (auto-generated, hooks config)
└── installed_modules.json (auto-generated, tracks modules)
```

## Documentation

- [skills](skills/README.md)
- [codeagent-wrapper](codeagent-wrapper/README.md)
- [Plugin System](PLUGIN_README.md)

## Troubleshooting

**Module not loading:**
```bash
cat ~/.claude/installed_modules.json
python3 install.py --module do --force
```

**Backend CLI errors:**
```bash
which codex && codex --version
which claude && claude --version
which gemini && gemini --version
which opencode && opencode --version
```

## License

AGPL-3.0 - see [LICENSE](LICENSE)

### Commercial Licensing

For commercial use without AGPL obligations, contact: evanxian9@gmail.com

## Support

- [GitHub Issues](https://github.com/RoterDL/omoclaude/issues)
