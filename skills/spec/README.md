# spec - Spec-Driven Development Lifecycle

Manages design document lifecycle with 4 gate-controlled phases: Intent -> Plan -> Implement -> End.

## Installation

```bash
python install.py --module spec
```

Installs:
- `~/.claude/skills/spec/` - skill files, scripts, references
- `spec-explorer`, `spec-planner`, `plan-reviewer`, `spec-reviewer-deep`, `spec-tester`, `spec-develop`, `spec-frontend`, and `spec-reviewer-lite` agent presets merged into `~/.codeagent/models.json`
- Automatically installs `memory` dependency

## Usage

```
/spec <task description>
```

Examples:
```
/spec add user authentication with JWT
/spec refactor database connection pooling
/spec implement dashboard analytics page
```

## 4-Phase Lifecycle

| Phase | Name | Gate | Artifacts |
|-------|------|------|-----------|
| 1 | Intent Confirmation | User confirms requirements | - |
| 2 | Design & Planning | User confirms design | `plan.md`, `test-plan.md` |
| 3 | Implementation | User confirms tests pass | `summary.md`, `test-report.md` |
| 4 | Wrap-up | User confirms archive | Archived to `06-archived/` |

## Task Classification (Phase 3 Routing)

`plan.md` includes `task_type` to determine implementation agents:

| task_type | Agent(s) | Skills Injection |
|-----------|----------|-----------------|
| `backend_only` | `spec-develop` | (none) |
| `frontend_only` | `spec-frontend` | `taste-core`, `taste-output` |
| `fullstack` | both in parallel | frontend gets taste skills |

## Relationship to /do and /omo

- `/spec` = document lifecycle management (cross-session, persistent design docs)
- `/do` = code execution orchestration (session-scoped, 5-phase workflow)
- `/omo` = signal-based agent routing (session-scoped, minimal agent set)

Spec does NOT nest into `/do` or `/omo`. Implementation is always delegated directly to `codeagent-wrapper` agents (`spec-develop`, `spec-frontend`, `explore`, etc.).

## Directory Structure

```
spec/
  SKILL.md                         # Main skill prompt
  README.md                        # This file
  references/
    spec-explorer.md               # spec-explorer agent prompt
    plan-reviewer.md               # plan-reviewer agent prompt
    spec-reviewer-deep.md          # spec-reviewer-deep agent prompt
    spec-planner.md                # spec-planner agent prompt
    spec-tester.md                 # spec-tester agent prompt
    spec-develop.md                # spec-develop agent prompt
    spec-frontend.md               # spec-frontend agent prompt
    spec-reviewer-lite.md          # spec-reviewer-lite agent prompt
    plan-template.md               # plan.md template
  scripts/
    spec-manager.py                # Spec lifecycle CLI
```

## Agents

| Agent | Source Module | Purpose |
|-------|-------------|---------|
| `spec-develop` | spec | Backend implementation |
| `spec-frontend` | spec | Frontend implementation (with taste skills) |
| `spec-reviewer-lite` | spec | Code review (standard intensity) |
| `spec-explorer` | spec | Self-contained codebase analysis for spec planning |
| `spec-planner` | spec | Design specification authoring |
| `plan-reviewer` | spec | Automated plan.md review before user confirmation |
| `spec-reviewer-deep` | spec | Post-implementation code review (deep intensity, Codex-based) |
| `spec-tester` | spec | Test execution and reporting |

## State Management

```bash
# Resolve script path (cross-platform, required on Windows)
SPEC_MGR="$(python -c "import os;print(os.path.expanduser('~/.claude/skills/spec/scripts/spec-manager.py'))")"

# Check current spec status
python "$SPEC_MGR" status

# List all specs
python "$SPEC_MGR" list

# Archive current spec
python "$SPEC_MGR" archive
```

State tracked via `.spec/.current-spec` pointer file.

## Dependencies

- `memory` module (for exp-search/exp-reflect integration)
- `taste` skills (`taste-core`, `taste-output`) injected into frontend tasks

## Prerequisites

- Python 3.10+
- codeagent-wrapper with `--agent` support
- Backend CLIs: claude, codex, gemini (depending on agent configuration)

## Platform Compatibility

| Item | Linux/macOS | Windows |
|------|-------------|---------|
| `spec-manager.py` | Fully supported | Fully supported |
| Script path | `$HOME` or `expanduser` | `expanduser` only (see note) |
| Heredoc `<<'EOF'` | Bash native | Not supported in PowerShell (see note) |
| codeagent-wrapper | Fully supported | Fully supported |
| stdin pipe encoding | UTF-8 | Use `--file` flag (see note) |

**Windows path note**: `$HOME` resolves incorrectly in Windows Git Bash (may point to Git installation directory instead of user home). Always use Python's `os.path.expanduser` to resolve the script path:
```bash
SPEC_MGR="$(python -c "import os;print(os.path.expanduser('~/.claude/skills/spec/scripts/spec-manager.py'))")"
```

**Windows encoding note**: Piping content via stdin (`echo '...' | python spec-manager.py update-body`) can corrupt UTF-8 encoding on Windows due to code page mismatches. Use the `--file` flag instead:
```bash
python "$SPEC_MGR" update-body --file /tmp/plan-body.md
python "$SPEC_MGR" write-artifact summary.md --file /tmp/summary.md
```

**Windows heredoc note**: SKILL.md examples use Bash heredoc syntax (`<<'EOF'`) to pipe multi-line input to `codeagent-wrapper`. On Windows (PowerShell), Claude Code will adapt to platform-appropriate syntax (here-strings or temp files).

## Uninstall

```bash
python uninstall.py --module spec
```
