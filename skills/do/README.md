# do - Feature Development Orchestrator

5-phase feature development workflow orchestrating multiple agents via codeagent-wrapper.

## Installation

```bash
python install.py --module do
```

Installs:

- `~/.claude/skills/do/` - skill files
- hooks auto-merged into `~/.claude/settings.json`
- agent presets merged into `~/.codeagent/models.json` (for `--agent` / parallel tasks)

## Usage

```
/do <feature description>
```

Examples:

```
/do add user login feature
/do implement order export to CSV
```

## 5-Phase Workflow

| Phase | Name       | Goal                                         | Key Actions                                          |
| ----- | ---------- | -------------------------------------------- | ---------------------------------------------------- |
| 1     | Understand | Gather requirements + map codebase           | Parallel code-architect + code-explorer              |
| 2     | Clarify    | Resolve blocking ambiguities                 | Conditional - only if blocking questions exist       |
| 3     | Design     | Plan implementation with task classification | code-architect blueprint + task_type                 |
| 4     | Implement  | Build the feature                            | do-develop / do-frontend based on task_type          |
| 5     | Complete   | Finalize and document                        | do-summarizer summary                                |

## Task Classification

Phase 3 outputs `task_type` to determine agent selection in Phase 4:

- `backend_only`: invoke only `do-develop` agent
- `frontend_only`: invoke only `do-frontend` agent
- `fullstack`: invoke both agents in parallel
- Missing `task_type`: default to `do-develop` agent only

## Agents

| Agent                       | Purpose                            | Needs DO_WORKTREE_DIR               |
| --------------------------- | ---------------------------------- | ----------------------------------- |
| `code-explorer`           | Code tracing, architecture mapping | No (read-only)                      |
| `code-architect`          | Design approaches, file planning   | No (read-only)                      |
| `do-reviewer`           | Code review, simplification        | **Yes** (if worktree enabled)       |
| `do-summarizer`         | Completion summary (Phase 5)       | **Yes** (if worktree enabled)       |
| `do-develop`              | Implement backend code, run tests  | **Yes** (if worktree enabled) |
| `do-frontend`             | Frontend implementation and UI/UX  | **Yes** (if worktree enabled) |

Prompts are shipped under `~/.claude/skills/do/agents/` and referenced via `agents.<name>.prompt_file` in `~/.codeagent/models.json`.
To customize, edit `~/.codeagent/models.json` (backend/model/prompt_file), or point `prompt_file` to a file under `~/.codeagent/agents/<name>.md`.

## Hard Constraints

1. **Never write code directly** - delegate all changes to codeagent-wrapper agents
2. **Phase 2 is conditional** - only if blocking questions exist
3. **Pass complete context forward** - every agent gets the Context Pack
4. **Parallel-first** - run independent tasks via `codeagent-wrapper --parallel`
5. **Update state after each phase** - use `task.py update-phase <N>`
6. **Respect worktree setting** - if `use_worktree: true`, prefix Phase 4-5 agent calls with `DO_WORKTREE_DIR=<worktree_dir>` (from `task.py enable-worktree` output)

## Context Pack Template

```text
## Original User Request
<verbatim request>

## Context Pack
- Phase: <1-5 name>
- Decisions: <requirements/constraints/choices>
- Code-explorer output: <paste or "None">
- Code-architect output: <paste or "None">
- Do-reviewer output: <paste or "None">
- Backend (do-develop) output: <paste or "None">
- Frontend (UI/UX) output: <paste or "None">
- Open questions: <list or "None">

## Current Task
<specific task>

## Acceptance Criteria
<checkable outputs>
```

## Loop State Management

When triggered via `/do <task>`, initializes `.claude/do-tasks/{task_id}/task.md` with YAML frontmatter:

```yaml
---
id: "<task_id>"
title: "<task description>"
status: "in_progress"
current_phase: 1
phase_name: "Understand"
max_phases: 5
use_worktree: false
verify_commands: []
created_at: "<ISO timestamp>"
completion_promise: "<promise>DO_COMPLETE</promise>"
---

# Requirements

<task description>

## Context

## Progress
```

The current task is tracked in `.claude/do-tasks/.current-task`.

After each phase, update `task.md` frontmatter via:

```bash
python "$HOME/.claude/skills/do/scripts/task.py" update-phase <N>
```

When all 5 phases complete, output:

```
<promise>DO_COMPLETE</promise>
```

To abort early, manually edit `task.md` and set `status: "cancelled"` in the frontmatter.

## Stop Hook

A Stop hook is registered after installation:

1. Creates `.claude/do-tasks/{task_id}/task.md` state file
2. Updates `current_phase` in frontmatter after each phase
3. Stop hook checks state, blocks exit if incomplete
4. Outputs `<promise>DO_COMPLETE</promise>` when finished

Manual exit: Edit `task.md` and set `status: "cancelled"` in the frontmatter.

## Verification Loop (verify_commands)

If `verify_commands` is set in the task's `task.md` frontmatter, a SubagentStop hook will run those
commands when `do-reviewer` attempts to stop, and block completion until they pass.

Configure via `task.py`:

```bash
# Replace verify commands:
python "$HOME/.claude/skills/do/scripts/task.py" set-verify --cmd "pytest -q" --cmd "npm test"

# Append:
python "$HOME/.claude/skills/do/scripts/task.py" set-verify --append --cmd "ruff check ."

# Disable gate:
python "$HOME/.claude/skills/do/scripts/task.py" set-verify --clear
```

When worktree is enabled, commands run in `worktree_dir`; otherwise they run in the project root.

## Worktree Mode

Use a git worktree to isolate changes from your main branch.

**Recommended for `/do`:** enable worktree via `task.py` and use `DO_WORKTREE_DIR` to pin the repo root for all Phase 4-5 agents (implementation + review + summary).

Alternative (standalone): use `codeagent-wrapper --worktree` to create a new isolated worktree.

```bash
codeagent-wrapper --worktree --agent do-develop "implement feature X" .
```

This automatically:

1. Generates a unique task ID (format: `YYYYMMDD-xxxxxx`)
2. Creates a new worktree at `.worktrees/do-{task_id}/`
3. Creates a new branch `do/{task_id}`
4. Executes the task in the isolated worktree

Output includes: `Using worktree: .worktrees/do-{task_id}/ (task_id: {id}, branch: do/{id})`

In parallel mode, add `worktree: true` to task blocks:

```
---TASK---
id: feature_impl
agent: do-develop
worktree: true
---CONTENT---
Implement the feature
```

## ~/.codeagent/models.json Configuration

Required when using `agent:` in parallel tasks or `--agent`. The installer writes module defaults into `~/.codeagent/models.json`; you can edit it to match your environment.

```json
{
  "agents": {
    "code-explorer": {
      "backend": "claude",
      "model": "claude-sonnet-4-6"
    },
    "code-architect": {
      "backend": "claude",
      "model": "claude-opus-4-6"
    },
    "do-reviewer": {
      "backend": "claude",
      "model": "claude-sonnet-4-6",
      "prompt_file": "~/.claude/skills/do/agents/do-reviewer.md"
    },
    "do-summarizer": {
      "backend": "claude",
      "model": "claude-sonnet-4-6",
      "prompt_file": "~/.claude/skills/do/agents/do-summarizer.md"
    },
    "do-develop": {
      "backend": "codex",
      "model": "gpt-5.3-codex",
      "prompt_file": "~/.claude/skills/do/agents/do-develop.md"
    },
    "do-frontend": {
      "backend": "gemini",
      "model": "gemini-3.1-pro-preview",
      "prompt_file": "~/.claude/skills/do/agents/do-frontend.md"
    }
  }
}
```

## Uninstall

```bash
python install.py --uninstall --module do
```
