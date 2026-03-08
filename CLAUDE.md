# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**omoclaude** is a multi-agent orchestration system for Claude Code. It provides skills (`/do`, `/omo`, `/research-pro`, `skill:codeagent`) that delegate code editing to external backend CLIs (Codex, Claude, Gemini, OpenCode) via `codeagent-wrapper`, a Go CLI binary that acts as a unified wrapper.

Repository: https://github.com/RoterDL/omoclaude (fork of cexll/myclaude)

## Key Rule: Modify Source Skills, Not Installed Copies

When modifying skills, **always edit files under this project's `skills/` directory**, never the installed copies under `~/.claude/skills/`. The installer copies from here to the user's home.

## Build & Test Commands

### codeagent-wrapper (Go binary)

```bash
cd codeagent-wrapper
make build        # Build binary
make test         # Run tests
make lint         # golangci-lint + staticcheck
make install      # Install to $GOPATH/bin
make clean        # Clean build artifacts
```

Requires Go 1.21+. CI runs Go 1.21/1.22 matrix.

### Installer (Python)

```bash
python install.py                          # Interactive install
python install.py --list-modules           # List available modules
python install.py --module do,omo --force  # Install specific modules
python install.py --update                 # Update installed modules
python install.py --status                 # Show install status
python uninstall.py --module do,omo        # Uninstall modules
```

### Changelog

```bash
make changelog    # Requires git-cliff; updates CHANGELOG.md
```

## Architecture

### Two-Layer Design

1. **Orchestrator (Claude Code)**: Plans, gathers context, routes tasks. Does NOT write code directly when a skill is active.
2. **Executors (codeagent-wrapper)**: External CLI agents that perform actual code edits via `codeagent-wrapper --agent <name>`.

### Core Components

| Component | Location | Language | Purpose |
|-----------|----------|----------|---------|
| Installer | `install.py` | Python | JSON-driven modular installer; reads `config.json`, copies skills/hooks to `~/.claude/`, merges agent configs to `~/.codeagent/models.json` |
| Uninstaller | `uninstall.py` | Python | Reverse of installer |
| codeagent-wrapper | `codeagent-wrapper/` | Go | Unified CLI wrapping Codex/Claude/Gemini/OpenCode backends; handles sessions, worktrees, parallel execution, skill injection |
| Config | `config.json` | JSON | Module definitions: agents, backends, operations, dependencies. Schema: `config.schema.json` |
| Global hooks | `hooks/` | Python | PreToolUse hooks: `pre-bash.py` (dangerous command blocker), `inject-spec.py` (deprecated no-op) |
| npx CLI | `bin/cli.js` | JS | `npx github:RoterDL/omoclaude` entry point |

### Skills (modules)

Each skill lives under `skills/<name>/` with a `SKILL.md` (the prompt loaded by Claude Code) and optional subdirectories:

| Skill | Trigger | Description |
|-------|---------|-------------|
| `do` | `/do` | 5-phase feature development (Understand -> Clarify -> Design -> Implement -> Complete). Orchestrates `code-explorer`, `code-architect`, `do-develop`, `do-frontend`, `do-reviewer`, `do-summarizer`. Has its own hooks (`stop-hook.py`, `verify-loop.py`) and state management (`scripts/task.py`). |
| `omo` | `/omo` | Signal-based routing to agents: `explore`, `librarian`, `oracle`, `develop`, `frontend-ui-ux-engineer`, `document-writer`, `code-reviewer`. Routing-first, not a fixed pipeline. |
| `codeagent` | `skill:codeagent` | Thin wrapper for direct `codeagent-wrapper` invocation |
| `research-pro` | `/research-pro` | Academic paper reading, review, literature search with `content-extractor`, `paper-reviewer`, `literature-scout`, etc. |
| `cr` | (dependency) | Code review checklists; auto-installed as dependency of `do` and `omo` |
| `taste` | (dependency) | Frontend design quality rules; 4 injectable sub-skills (`taste-core`, `taste-output`, `taste-creative`, `taste-redesign`) injected into `do-frontend` via `--skills` |

### Agent Prompt Files

- `skills/do/agents/*.md` - do skill agent prompts
- `skills/omo/references/*.md` - omo skill agent prompts
- `skills/research-pro/references/*.md` - research-pro agent prompts

These are referenced by `config.json` `agents.<name>.prompt_file` and merged into `~/.codeagent/models.json` at install time.

### codeagent-wrapper Internal Structure

```
codeagent-wrapper/
  cmd/codeagent-wrapper/main.go   # Entry point
  internal/
    app/          # CLI command definitions, arg parsing
    backend/      # Backend implementations (codex/claude/gemini/opencode)
    config/       # Config loading, agent resolution (viper)
    executor/     # Single/parallel/worktree task execution, skill injection
    logger/       # Structured logging
    parser/       # JSON stream parser
    utils/        # Common utilities
    worktree/     # Git worktree management
```

### Installation Flow

`install.py` reads `config.json` -> resolves module dependencies -> executes operations (`copy_dir`, `copy_file`, `merge_dir`, `merge_json`, `run_command`) -> merges agent configs into `~/.codeagent/models.json` -> merges hook configs into `~/.claude/settings.json` -> records state to `~/.claude/installed_modules.json`.

### do Skill State Management

`/do` creates task state at `.claude/do-tasks/{task_id}/task.md` with YAML frontmatter tracking phase progression. `scripts/task.py` manages state (update-phase, enable-worktree, set-verify). Stop hook blocks session exit until all 5 phases complete or task is cancelled.

## Commit Convention

`<type>(<scope>): <description>` using conventional commits. `git-cliff` generates changelogs from `cliff.toml` config.

## Cross-Platform Notes

- Windows support: hooks use Python (not bash). `pre-bash.py` has platform-specific dangerous command patterns.
- Paths with CJK characters must be quoted.
- The project uses `python` (not `python3`) as the unified command reference.
