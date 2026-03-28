---
name: do
description: This skill should be used for structured feature development with codebase understanding. Triggers on /do command. Provides a 5-phase workflow (Understand, Clarify, Design, Implement, Complete) using codeagent-wrapper to orchestrate code-explorer, code-architect, do-reviewer, do-develop, and do-frontend agents in parallel.
allowed-tools: ["Bash(~/.claude/skills/do/scripts/setup-do.py:*)", "Bash(~/.claude/skills/do/scripts/task.py:*)", "Skill(exp-reflect:*)"]
---

# do - Feature Development Orchestrator

An orchestrator for systematic feature development. Invoke agents via `codeagent-wrapper`, never write code directly.

## Key References

- **`references/invocation-templates.md`**: Read when entering Phase 1, 3, 4, or 5. Contains Context Pack template, issue severity definitions, taste skill injection rules, and all agent invocation templates.

## Loop Initialization (REQUIRED)

When triggered via `/do <task>`, initialize the task directory immediately without asking about worktree:

Use `$SETUP_DO` (see Script Path Resolution below):

```bash
python "$SETUP_DO" "<task description>"
```

This creates a task directory under `.claude/do-tasks/` with:
- `task.md`: Single file containing YAML frontmatter (metadata) + Markdown body (requirements/context)

**Worktree decision is deferred until Phase 4 (Implement).** Phases 1-3 are read-only and do not require worktree isolation.

## Script Path Resolution (cross-platform)

All commands use `$TASK_MGR` and `$SETUP_DO`. Since shell state doesn't persist, **prepend this to every Bash invocation that uses these scripts**:

```bash
TASK_MGR="$(python -c "import os;print(os.path.expanduser('~/.claude/skills/do/scripts/task.py'))")"
SETUP_DO="$(python -c "import os;print(os.path.expanduser('~/.claude/skills/do/scripts/setup-do.py'))")"
```

Do NOT use `$HOME` directly -- fails on Windows Git Bash. Prefer `--file <tempfile>` over pipe for stdin-based writes.

## Task Directory Management

Use `task.py` to manage task state:

```bash
# Update phase
python "$TASK_MGR" update-phase 2

# Check status
python "$TASK_MGR" status

# List all tasks
python "$TASK_MGR" list
```

## Worktree Mode

The worktree is created **only when needed** (right before Phase 4: Implement). If the user chooses worktree mode:

1. Enable worktree: `python "$TASK_MGR" enable-worktree`
2. Use the `DO_WORKTREE_DIR` from output to prefix all Phase 4-5 agent calls that depend on repo state.

Phases 1-3 are read-only and do not require `DO_WORKTREE_DIR`. See `references/invocation-templates.md` "Worktree Prefix Rule" for details.

## Trivial Detection (before Phase 1)

After init, check if trivial: single file + typo/wording fix, clear scope, or user said "just do it".

**Trivial express-path** -- skip rules:

| Phase | Action |
|-------|--------|
| Phase 1 (Understand) | Skip parallel exploration |
| Phase 2 (Clarify) | Skip |
| Phase 3 (Design) | Skip architect; orchestrator states the change directly to user |
| Phase 4 (Implement) | Execute `do-develop`/`do-frontend` only (skip worktree question, skip review) |
| Phase 5 (Complete) | Skip summarizer and experience reflection; orchestrator outputs brief summary |

Context Pack is not used for trivial tasks; pass the user request directly as the agent prompt.

Flow: init -> confirm change with user via AskUserQuestion -> implement -> `<promise>DO_COMPLETE</promise>`

## Pre-Task Experience Check (before Phase 1)

**Trigger**: Task is non-trivial (would proceed to Phase 1 parallel exploration).
**Skip**: Trivial express-path tasks, no `.spec/context/` directory.

Read index files directly (no agent needed):
1. Read `.spec/context/experience/index.md` (if exists) -- scan for matching dilemma-strategy pairs
2. Read `.spec/context/knowledge/index.md` (if exists) -- scan for relevant project knowledge
3. If matches found, include as context in Phase 1 agent prompts (Context Pack)

This is a lightweight read-only step. If no `.spec/context/` directory exists, skip silently.

## Hard Constraints

1. **Never write code directly.** Delegate all code changes to `codeagent-wrapper` agents.
2. **Pass complete context forward.** Every agent invocation includes the Context Pack (see `references/invocation-templates.md`).
3. **Parallel-first.** Run independent tasks via `codeagent-wrapper --parallel`.
4. **Update phase after each phase.** Use `task.py update-phase <N>`.
5. **Expect long-running `codeagent-wrapper` calls.** For calls that may exceed the Bash tool timeout, invoke with `run_in_background: true` and fetch via `TaskOutput`.
6. **Agent failure handling.** If `codeagent-wrapper` fails: check stderr, retry once if transient. If retry fails, surface error to user via `AskUserQuestion`. Never silently skip a failed agent call; never switch to direct implementation.
7. **Defer worktree decision until Phase 4.** Only ask about worktree mode right before implementation.

## Task Cancellation

When the user requests to cancel or abort the current task:

1. Run: `python "$TASK_MGR" cancel`
2. Confirm to the user that the task has been cancelled
3. Do NOT continue to subsequent phases

## Agents

| Agent | Purpose | Needs worktree |
|-------|---------|----------------|
| `code-explorer` | Trace code, map architecture, find patterns | No |
| `code-architect` | Design approaches, file plans, build sequences | No |
| `do-reviewer` | Review for bugs, simplicity, conventions | Yes (if enabled) |
| `do-summarizer` | Completion summary (Phase 5) | Yes (if enabled) |
| `do-develop` | Implement backend code, run tests | Yes |
| `do-frontend` | Frontend implementation and UI/UX interactions | Yes |

## 5-Phase Workflow

### Phase 1: Understand (Parallel, No Interaction)

**Goal:** Understand requirements and map codebase simultaneously.

Read `references/invocation-templates.md` "Phase 1: Parallel Exploration Template". Run `code-architect` + 2-3 `code-explorer` tasks in parallel using `run_in_background: true`. Use `TaskOutput` to retrieve results.

### Phase 2: Clarify (Conditional)

**Goal:** Resolve blocking ambiguities only.

1. Review `p1_requirements` output for blocking questions
2. IF completeness >= 8 AND blocking questions list is empty -> Skip to Phase 3
3. OTHERWISE -> Use AskUserQuestion to resolve blocking questions, then proceed

### Phase 3: Design (User Confirmation Required)

**Goal:** Produce minimal-change implementation plan with task classification.

Read `references/invocation-templates.md` "Taste Skill Injection Rules" (plan phase) and "Phase 3: Design Invocation Template". Invoke `code-architect` with `run_in_background: true`; for frontend tasks, inject the appropriate taste skill via `--skills`.

**After code-architect completes, present the design to the user for confirmation:**

1. Display the full design output including: file touch list, build sequence, test plan, risks, task classification
2. Use `AskUserQuestion` to get explicit approval:
   - "Approve design and proceed to implementation" -> continue to Phase 4
   - "Revise design" -> adjust based on feedback and re-run code-architect
3. **Do NOT enter Phase 4 until the user explicitly approves the design.**

### Phase 4: Implement + Review

**Goal:** Build feature and review in one phase.

Read `references/invocation-templates.md` for all Phase 4 templates before proceeding.

**Step 1: Decide on worktree mode (ONLY NOW)**

Use AskUserQuestion: "Develop in a separate worktree? (Yes / No)"

If yes: `python "$TASK_MGR" enable-worktree` and save `DO_WORKTREE_DIR` from output. All subsequent agent calls in Phase 4-5 must be prefixed with `DO_WORKTREE_DIR=<path>`.

**Step 2: Invoke implementation agent(s)**

Route based on Phase 3 `task_type` (see `references/invocation-templates.md` "Implementation Templates"):

| task_type | Agent(s) | --skills |
|-----------|----------|----------|
| `frontend_only` | `do-frontend` | `taste-core,taste-output` |
| `backend_only` | `do-develop` | none |
| `fullstack` | both via `--parallel` | `do-frontend` gets `taste-core,taste-output` |

**If `task_type` is missing from architect output:** infer from the file touch list — if all files are frontend (.html, .css, .scss, .js, .jsx, .ts, .tsx, .vue, .svelte), use `do-frontend`; mixed → `--parallel`; otherwise `do-develop`. **Never default to `do-develop` for tasks touching only frontend files.**

**Step 3: Configure verification commands (Recommended)**

```bash
python "$TASK_MGR" set-verify --cmd "<command>" --cmd "<command2>"
```

Use `--append` to add commands; `--clear` to disable the gate.

**Step 4: Review**

Capture diff and run parallel reviews -- see `references/invocation-templates.md` "Phase 4: Review Templates".

**Step 5: Handle review results**

- **MINOR issues only** -> Auto-fix via `do-develop`/`do-frontend`, no user interaction
- **BLOCKING issues** -> Use AskUserQuestion: "Fix now / Proceed as-is"

### Phase 5: Complete (No Interaction)

**Goal:** Document what was built.

Read `references/invocation-templates.md` "Phase 5: Summarizer Template". Invoke `do-summarizer` (with `DO_WORKTREE_DIR` prefix if worktree enabled).

**Auto Experience Reflection:**

After summarizer completes, automatically invoke experience reflection. No user prompt needed.

**Trigger** (any one):
- Task involved 3+ phases (non-trivial)
- Implementation touched 3+ files
- Review found BLOCKING issues that were resolved

**Skip**: Trivial express-path, single-file changes, no `.spec/context/` directory.

When triggered, invoke:
```
Skill(exp-reflect)
```

Then output the completion signal:
```
<promise>DO_COMPLETE</promise>
```
