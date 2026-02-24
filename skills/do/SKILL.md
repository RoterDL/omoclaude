---
name: do
description: This skill should be used for structured feature development with codebase understanding. Triggers on /do command. Provides a 5-phase workflow (Understand, Clarify, Design, Implement, Complete) using codeagent-wrapper to orchestrate code-explorer, code-architect, code-reviewer, develop, and frontend-ui-ux-engineer agents in parallel.
allowed-tools: ["Bash(~/.claude/skills/do/scripts/setup-do.py:*)", "Bash(~/.claude/skills/do/scripts/task.py:*)"]
---

# do - Feature Development Orchestrator

An orchestrator for systematic feature development. Invoke agents via `codeagent-wrapper`, never write code directly.

## Loop Initialization (REQUIRED)

When triggered via `/do <task>`, initialize the task directory immediately without asking about worktree:

Check the `Platform:` field in the environment info to determine the correct command:
- **Windows (Platform: win32):** use `python` and `$HOME` for home directory
- **Linux/macOS:** use `python3` and `$HOME` for home directory

```bash
# Windows:
python "$HOME/.claude/skills/do/scripts/setup-do.py" "<task description>"
# Linux/macOS:
python3 "$HOME/.claude/skills/do/scripts/setup-do.py" "<task description>"
```

This creates a task directory under `.claude/do-tasks/` with:
- `task.md`: Single file containing YAML frontmatter (metadata) + Markdown body (requirements/context)

**Worktree decision is deferred until Phase 4 (Implement).** Phases 1-3 are read-only and do not require worktree isolation.

## Task Directory Management

Use `task.py` to manage task state (use `python` on Windows, `python3` on Linux/macOS):

```bash
# Update phase (Linux/macOS)
python3 "$HOME/.claude/skills/do/scripts/task.py" update-phase 2

# Check status
python3 "$HOME/.claude/skills/do/scripts/task.py" status

# List all tasks
python3 "$HOME/.claude/skills/do/scripts/task.py" list
```

## Worktree Mode

The worktree is created **only when needed** (right before Phase 4: Implement). If the user chooses worktree mode:

1. Enable worktree for the current task (creates worktree without resetting task context):
   ```bash
   # Windows:
   python "$HOME/.claude/skills/do/scripts/task.py" enable-worktree
   # Linux/macOS:
   python3 "$HOME/.claude/skills/do/scripts/task.py" enable-worktree
   ```

2. Use the `DO_WORKTREE_DIR` environment variable from the output to direct `codeagent-wrapper` develop agent into the worktree:

```bash
# Prefix all develop/frontend calls with DO_WORKTREE_DIR:
DO_WORKTREE_DIR=<worktree_dir> codeagent-wrapper --agent develop - . <<'EOF'
...
EOF
```

Read-only agents (code-explorer, code-architect, code-reviewer) do NOT need `DO_WORKTREE_DIR`.

## Hard Constraints

1. **Never write code directly.** Delegate all code changes to `codeagent-wrapper` agents.
2. **Pass complete context forward.** Every agent invocation includes the Context Pack.
3. **Parallel-first.** Run independent tasks via `codeagent-wrapper --parallel`.
4. **Update phase after each phase.** Use `task.py update-phase <N>`.
5. **Expect long-running `codeagent-wrapper` calls.** High-reasoning modes can take a long time; stay in the orchestrator role and wait for agents to complete.
6. **Timeouts are not an escape hatch.** If a `codeagent-wrapper` invocation times out/errors, retry (split/narrow the task if needed); never switch to direct implementation.
7. **Defer worktree decision until Phase 4.** Only ask about worktree mode right before implementation. If enabled, prefix develop/frontend agent calls with `DO_WORKTREE_DIR=<path>`. Never pass `--worktree` after initialization.

## Agents

| Agent | Purpose | Needs worktree |
|-------|---------|------------------|
| `code-explorer` | Trace code, map architecture, find patterns | No (read-only) |
| `code-architect` | Design approaches, file plans, build sequences | No (read-only) |
| `code-reviewer` | Review for bugs, simplicity, conventions | No (read-only) |
| `develop` | Implement backend code, run tests | **Yes** — use `DO_WORKTREE_DIR` env prefix |
| `frontend-ui-ux-engineer` | Frontend implementation and UI/UX interactions | **Yes** — use `DO_WORKTREE_DIR` env prefix |

## Issue Severity Definitions

**Blocking issues** (require user input):
- Impacts core functionality or correctness
- Security vulnerabilities
- Architectural conflicts with existing patterns
- Ambiguous requirements with multiple valid interpretations

**Minor issues** (auto-fix without asking):
- Code style inconsistencies
- Naming improvements
- Missing documentation
- Non-critical test coverage gaps

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

## 5-Phase Workflow

### Phase 1: Understand (Parallel, No Interaction)

**Goal:** Understand requirements and map codebase simultaneously.

**Actions:** Run `code-architect` and 2-3 `code-explorer` tasks in parallel.

```bash
codeagent-wrapper --parallel <<'EOF'
---TASK---
id: p1_requirements
agent: code-architect
workdir: .
---CONTENT---
Analyze requirements completeness (score 1-10):
1. Extract explicit requirements, constraints, acceptance criteria
2. Identify blocking questions (issues that prevent implementation)
3. Identify minor clarifications (nice-to-have but can proceed without)

Output format:
- Completeness score: X/10
- Requirements: [list]
- Non-goals: [list]
- Blocking questions: [list, if any]

---TASK---
id: p1_similar_features
agent: code-explorer
workdir: .
---CONTENT---
Find 1-3 similar features, trace end-to-end. Return: key files with line numbers, call flow, extension points.

---TASK---
id: p1_architecture
agent: code-explorer
workdir: .
---CONTENT---
Map architecture for relevant subsystem. Return: module map + 5-10 key files.

---TASK---
id: p1_conventions
agent: code-explorer
workdir: .
---CONTENT---
Identify testing patterns, conventions, config. Return: test commands + file locations.
EOF
```

### Phase 2: Clarify (Conditional)

**Goal:** Resolve blocking ambiguities only.

**Actions:**
1. Review `p1_requirements` output for blocking questions
2. **IF blocking questions exist** → Use AskUserQuestion
3. **IF no blocking questions (completeness >= 8)** → Skip to Phase 3

### Phase 3: Design (User Confirmation Required)

**Goal:** Produce minimal-change implementation plan with task classification.

```bash
codeagent-wrapper --agent code-architect - . <<'EOF'
Design minimal-change implementation:
- Reuse existing abstractions
- Minimize new files
- Follow established patterns from Phase 1 exploration

Output:
- File touch list with specific changes
- Build sequence
- Test plan
- Risks and mitigations

Include a `## Task Classification` section:
- `task_type`: "backend_only" | "frontend_only" | "fullstack"
- `backend_tasks`: list backend implementation tasks (if any)
- `frontend_tasks`: list frontend implementation tasks (if any)
EOF
```

**After code-architect completes, present the design to the user for confirmation:**

1. Display the full design output from code-architect, including:
   - File touch list with specific changes
   - Build sequence
   - Test plan
   - Risks and mitigations
   - Task classification
2. Use `AskUserQuestion` to get explicit approval:
   - "Approve design and proceed to implementation" — continue to Phase 4
   - "Revise design" — adjust based on user feedback and re-run code-architect
3. **Do NOT enter Phase 4 until the user explicitly approves the design.**

### Phase 4: Implement + Review

**Goal:** Build feature and review in one phase, using task classification from Phase 3.

**Step 1: Decide on worktree mode (ONLY NOW)**

Use AskUserQuestion to ask:

```
Develop in a separate worktree? (Isolates changes from main branch)
- Yes (Recommended for larger changes)
- No (Work directly in current directory)
```

If user chooses worktree:
```bash
# Windows:
python "$HOME/.claude/skills/do/scripts/task.py" enable-worktree
# Linux/macOS:
python3 "$HOME/.claude/skills/do/scripts/task.py" enable-worktree
# Save the DO_WORKTREE_DIR from output
```

**Step 2: Invoke implementation agent(s)**

**Execution Rules (based on Phase 3 `task_type`):**
- `backend_only`: invoke only `develop` agent
- `frontend_only`: invoke only `frontend-ui-ux-engineer` agent
- `fullstack`: invoke both agents in parallel
- Missing `task_type`: default to `develop` agent only

For full-stack projects, split into backend/frontend tasks with per-task `skills:` injection. Use `--parallel` when tasks can be split; use single agent when the change is small or single-domain.

**Single-domain example** (prefix with `DO_WORKTREE_DIR` if worktree enabled):

```bash
# With worktree:
DO_WORKTREE_DIR=<worktree_dir> codeagent-wrapper --agent develop - . <<'EOF'
Implement with minimal change set following the Phase 3 blueprint.
- Follow Phase 1 patterns
- Add/adjust tests per Phase 3 plan
- Run narrowest relevant tests
EOF

# Without worktree:
codeagent-wrapper --agent develop - . <<'EOF'
Implement with minimal change set following the Phase 3 blueprint.
- Follow Phase 1 patterns
- Add/adjust tests per Phase 3 plan
- Run narrowest relevant tests
EOF
```

**Full-stack parallel example** (adapt task IDs, skills, and content based on Phase 3 design):

```bash
# With worktree:
DO_WORKTREE_DIR=<worktree_dir> codeagent-wrapper --parallel <<'EOF'
---TASK---
id: p4_backend
agent: develop
workdir: .
---CONTENT---
Implement backend changes following Phase 3 blueprint.
- Follow Phase 1 patterns
- Add/adjust tests per Phase 3 plan

---TASK---
id: p4_frontend
agent: frontend-ui-ux-engineer
workdir: .
---CONTENT---
Implement frontend changes following Phase 3 blueprint.
- Follow Phase 1 patterns
- Add/adjust tests per Phase 3 plan
EOF

# Without worktree: remove DO_WORKTREE_DIR prefix
```

Note: Choose which skills to inject based on Phase 3 design output. Only inject skills relevant to each task's domain.

**Step 3: Review**

Run parallel reviews:

```bash
codeagent-wrapper --parallel <<'EOF'
---TASK---
id: p4_correctness
agent: code-reviewer
workdir: .
---CONTENT---
Review for correctness, edge cases, failure modes.
Classify each issue as BLOCKING or MINOR.

---TASK---
id: p4_simplicity
agent: code-reviewer
workdir: .
---CONTENT---
Review for KISS: remove bloat, collapse needless abstractions.
Classify each issue as BLOCKING or MINOR.
EOF
```

**Step 4: Handle review results**

- **MINOR issues only** → Auto-fix via `develop`/`frontend-ui-ux-engineer` (with `DO_WORKTREE_DIR` if enabled), no user interaction
- **BLOCKING issues** → Use AskUserQuestion: "Fix now / Proceed as-is"

### Phase 5: Complete (No Interaction)

**Goal:** Document what was built.

```bash
codeagent-wrapper --agent code-reviewer - . <<'EOF'
Write completion summary:
- What was built
- Key decisions/tradeoffs
- Files modified (paths)
- How to verify (commands)
- Follow-ups (optional)
EOF
```

Output the completion signal:
```
<promise>DO_COMPLETE</promise>
```
