# do - Feature Development Orchestrator

5-phase feature development workflow orchestrating multiple agents via codeagent-wrapper.

## Installation

```bash
python install.py --module do
```

Installs:
- `~/.claude/skills/do/` - skill files
- hooks auto-merged into `~/.claude/settings.json`

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

| Phase | Name | Goal | Key Actions |
|-------|------|------|-------------|
| 1 | Understand | Gather requirements + map codebase | Parallel code-architect + code-explorer |
| 2 | Clarify | Resolve blocking ambiguities | Conditional - only if blocking questions exist |
| 3 | Design | Plan implementation with task classification | code-architect blueprint + task_type |
| 4 | Implement | Build the feature | develop / frontend-ui-ux-engineer based on task_type |
| 5 | Complete | Finalize and document | code-reviewer summary |

## Task Classification

Phase 3 outputs `task_type` to determine agent selection in Phase 4:
- `backend_only`: invoke only `develop` agent
- `frontend_only`: invoke only `frontend-ui-ux-engineer` agent
- `fullstack`: invoke both agents in parallel
- Missing `task_type`: default to `develop` agent only

## Agents

| Agent | Purpose | Needs --worktree |
|-------|---------|------------------|
| `code-explorer` | Code tracing, architecture mapping | No (read-only) |
| `code-architect` | Design approaches, file planning | No (read-only) |
| `code-reviewer` | Code review, simplification | No (read-only) |
| `develop` | Implement backend code, run tests | **Yes** (if worktree enabled) |
| `frontend-ui-ux-engineer` | Frontend implementation and UI/UX | **Yes** (if worktree enabled) |

To customize agents, create same-named files in `~/.codeagent/agents/` to override.

## Hard Constraints

1. **Never write code directly** - delegate all changes to codeagent-wrapper agents
2. **Phase 2 is conditional** - only if blocking questions exist
3. **Pass complete context forward** - every agent gets the Context Pack
4. **Parallel-first** - run independent tasks via `codeagent-wrapper --parallel`
5. **Update state after each phase** - keep `.claude/do.{task_id}.local.md` current
6. **Respect worktree setting** - if `use_worktree: true`, pass `--worktree` to develop/frontend agents

## Context Pack Template

```text
## Original User Request
<verbatim request>

## Context Pack
- Phase: <1-5 name>
- Decisions: <requirements/constraints/choices>
- Code-explorer output: <paste or "None">
- Code-architect output: <paste or "None">
- Code-reviewer output: <paste or "None">
- Backend (develop) output: <paste or "None">
- Frontend (UI/UX) output: <paste or "None">
- Open questions: <list or "None">

## Current Task
<specific task>

## Acceptance Criteria
<checkable outputs>
```

## Loop State Management

When triggered via `/do <task>`, initializes `.claude/do.{task_id}.local.md` with:
- `active: true`
- `current_phase: 1`
- `max_phases: 5`
- `completion_promise: "<promise>DO_COMPLETE</promise>"`
- `use_worktree: true/false`

After each phase, update frontmatter:
```yaml
current_phase: <next phase number>
phase_name: "<next phase name>"
```

When all 5 phases complete, output:
```
<promise>DO_COMPLETE</promise>
```

To abort early, set `active: false` in the state file.

## Stop Hook

A Stop hook is registered after installation:
1. Creates `.claude/do.{task_id}.local.md` state file
2. Updates `current_phase` after each phase
3. Stop hook checks state, blocks exit if incomplete
4. Outputs `<promise>DO_COMPLETE</promise>` when finished

Manual exit: Set `active` to `false` in the state file.

## Worktree Mode

Use `--worktree` to execute tasks in an isolated git worktree, preventing changes to your main branch:

```bash
codeagent-wrapper --worktree --agent develop "implement feature X" .
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
agent: develop
worktree: true
---CONTENT---
Implement the feature
```

## ~/.codeagent/models.json Configuration

Required when using `agent:` in parallel tasks or `--agent`. Create `~/.codeagent/models.json` to configure agent → backend/model mappings:

```json
{
  "agents": {
    "code-explorer": {
      "backend": "claude",
      "model": "claude-sonnet-4-5-20250929"
    },
    "code-architect": {
      "backend": "claude",
      "model": "claude-sonnet-4-5-20250929"
    },
    "code-reviewer": {
      "backend": "claude",
      "model": "claude-sonnet-4-5-20250929"
    }
  }
}
```

## Uninstall

```bash
python install.py --uninstall --module do
```
