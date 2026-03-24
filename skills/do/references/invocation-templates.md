# Invocation Templates

Reference for `/do` workflow. All templates show the without-worktree form. If worktree is enabled, prefix all Phase 4-5 calls with `DO_WORKTREE_DIR=<path>`.

## Issue Severity Definitions

**Blocking** (require user input): core functionality/correctness impact, security vulnerabilities, architectural conflicts, ambiguous requirements with multiple valid interpretations.

**Minor** (auto-fix without asking): code style, naming, missing docs, non-critical test coverage gaps.

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

## Taste Skill Injection Rules

**Plan phase (Phase 3 — injected into `code-architect` via `--skills`):**
- Default creative/premium UI: `--skills taste-creative`
- Industrial/brutalist style: `--skills taste-creative,taste-brutalist`
- Minimalist/editorial style: `--skills taste-creative,taste-minimalist`
- Backend-only tasks: no `--skills`

**Implement phase (Phase 4 — injected into `do-frontend` via `--skills`):**
- Always: `--skills taste-core,taste-output`
- Existing UI overhaul: append `taste-redesign`
- `do-develop` does not use `--skills`; auto-detect handles tech stack

Design paradigm skills (`taste-creative`, `taste-brutalist`, `taste-minimalist`) are injected in Phase 3 only, not Phase 4.

## Phase 1: Parallel Exploration Template

Invoke with `run_in_background: true`, use `TaskOutput` to retrieve results. `--parallel` defaults to structured summary; avoid `--full-output` unless debugging.

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
End with: Summary: <one sentence>
---TASK---
id: p1_similar_features
agent: code-explorer
workdir: .
---CONTENT---
Find 1-3 similar features, trace end-to-end. Return: key files with line numbers, call flow, extension points.
End with: Summary: <one sentence>
---TASK---
id: p1_architecture
agent: code-explorer
workdir: .
---CONTENT---
Map architecture for relevant subsystem. Return: module map + 5-10 key files.
End with: Summary: <one sentence>
---TASK---
id: p1_conventions
agent: code-explorer
workdir: .
---CONTENT---
Identify testing patterns, conventions, config. Return: test commands + file locations.
End with: Summary: <one sentence>
EOF
```

## Phase 3: Design Invocation Template

Invoke with `run_in_background: true`. For frontend tasks, add `--skills` per Taste Skill Injection Rules above.

```bash
codeagent-wrapper --agent code-architect --skills taste-creative - . <<'EOF'
Design minimal-change implementation:
- Reuse existing abstractions
- Minimize new files
- Follow established patterns from Phase 1 exploration
Output:
- File touch list with specific changes
- Build sequence
- Test plan
- Risks and mitigations
- **Design Specification**: paradigm choice, color palette, typography, layout approach, motion strategy, component patterns
Include a `## Task Classification` section:
- `task_type`: "backend_only" | "frontend_only" | "fullstack"
- `backend_tasks`: list backend implementation tasks (if any)
- `frontend_tasks`: list frontend implementation tasks (if any)
EOF
```

## Phase 4: Implementation Templates

### Single-Domain Template

```bash
# do-develop (backend):
codeagent-wrapper --agent do-develop - . <<'EOF'
Implement with minimal change set following the Phase 3 blueprint.
- Follow Phase 1 patterns
- Add/adjust tests per Phase 3 plan
- Run narrowest relevant tests
After implementation, your code will be reviewed for correctness and simplicity. Write clean, correct code.
EOF

# do-frontend (frontend) — always inject taste-core,taste-output:
codeagent-wrapper --agent do-frontend --skills taste-core,taste-output - . <<'EOF'
Implement with minimal change set following the Phase 3 blueprint.
- Follow Phase 1 patterns
- Add/adjust tests per Phase 3 plan
- Run narrowest relevant tests
After implementation, your code will be reviewed for correctness and simplicity. Write clean, correct code.
EOF
```

### Full-Stack Parallel Template

```bash
codeagent-wrapper --parallel <<'EOF'
---TASK---
id: p4_backend
agent: do-develop
workdir: .
---CONTENT---
Implement backend changes following Phase 3 blueprint.
- Follow Phase 1 patterns
- Add/adjust tests per Phase 3 plan
After implementation, your code will be reviewed. Write clean, correct code.
End with: Summary: <one sentence>
---TASK---
id: p4_frontend
agent: do-frontend
workdir: .
skills: taste-core,taste-output
---CONTENT---
Implement frontend changes following Phase 3 blueprint.
- Follow Phase 1 patterns
- Add/adjust tests per Phase 3 plan
After implementation, your code will be reviewed. Write clean, correct code.
End with: Summary: <one sentence>
EOF
```

### Execution Rules (based on Phase 3 `task_type`)

| task_type | Agent(s) | --skills |
|-----------|----------|----------|
| `backend_only` | `do-develop` only | none |
| `frontend_only` | `do-frontend` only | `taste-core,taste-output` |
| `fullstack` | both in `--parallel` | `do-frontend` gets `taste-core,taste-output` |
| missing | default to `do-develop` | none |

## Phase 4: Review Templates

### Capture Diff

```bash
REVIEW_DIFF=$(cd "${DO_WORKTREE_DIR:-.}" && git diff HEAD~1 --stat && echo "---" && git diff HEAD~1)
```

### Parallel Review Invocation

```bash
codeagent-wrapper --parallel <<'EOF'
---TASK---
id: p4_correctness
agent: do-reviewer
workdir: .
---CONTENT---
Review for correctness, edge cases, failure modes.
Classify each issue as BLOCKING or MINOR.
Implementation diff:
$REVIEW_DIFF
End with: Summary: BLOCKING=<n>, MINOR=<n> — <one sentence>
---TASK---
id: p4_simplicity
agent: do-reviewer
workdir: .
---CONTENT---
Review for KISS: remove bloat, collapse needless abstractions.
Classify each issue as BLOCKING or MINOR.
Implementation diff:
$REVIEW_DIFF
End with: Summary: BLOCKING=<n>, MINOR=<n> — <one sentence>
EOF
```

### Review Result Handling

- **MINOR issues only** -> Auto-fix via `do-develop`/`do-frontend`, no user interaction
- **BLOCKING issues** -> Use AskUserQuestion: "Fix now / Proceed as-is"

## Phase 5: Summarizer Template

```bash
codeagent-wrapper --agent do-summarizer - . <<'EOF'
Write completion summary:
- What was built
- Key decisions/tradeoffs
- Files modified (paths)
- How to verify (commands)
- Follow-ups (optional)
EOF
```
