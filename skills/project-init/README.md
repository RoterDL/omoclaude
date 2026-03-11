# project-init - Project Spec Infrastructure Initialization

One-time project initialization that creates the `.spec/` directory structure, memory indexes, and coding rules templates for spec-driven development.

## Installation

```bash
python install.py --module project-init
```

Installs `~/.claude/skills/project-init/` (skill + scripts + templates).

## Usage

```
/project-init
```

Or say "initialize project" / "set up spec environment" in conversation.

## What It Creates

```
<project>/
  .spec/
    01-planning/
    02-architecture/
    03-features/
    04-bugfix/
    05-testing/
    06-archived/
    context/
      experience/
        index.md          # Experience index (maintained by exp-write)
      knowledge/
        index.md          # Knowledge index (maintained by exp-write)
  .claude/
    rules/
      coding-style.md     # Language-specific coding conventions
      spec-workflow.md     # Spec workflow rules
```

## Workflow

| Step | Action | Gate |
|------|--------|------|
| 1 | Check project state (`init-project.py check`) | Skip if fully initialized |
| 2 | Gather project info (name, stack, type) | AskUserQuestion |
| 3 | Create directories + indexes (`init-project.py init`) | - |
| 4 | Create coding rules templates (if empty) | - |
| 5 | Confirm results | - |

## Idempotency

All operations are idempotent:
- Existing directories are skipped
- Existing index files are never overwritten
- Safe to run multiple times

## Next Steps After Init

- `/spec <task>` - Start a spec-driven development task
- `/do <task>` - Start a feature development workflow
- `/exp-search <keywords>` - Search project memory

## Prerequisites

- Python 3.10+
- Git repository (recommended)

## Platform Compatibility

| Item | Linux/macOS | Windows |
|------|-------------|---------|
| Python scripts | Fully supported | Fully supported |
| `$HOME` path | Bash `$HOME` | PowerShell `$HOME` (auto variable) |
| Directory creation | `os.makedirs` | `os.makedirs` |
| File encoding | UTF-8 | UTF-8 |

Scripts use `os.path.join` and `os.makedirs` throughout -- no platform-specific path handling needed.

## Uninstall

```bash
python uninstall.py --module project-init
```

Note: This only removes the skill files. Project directories created by `init-project.py` in your target project are not affected.
