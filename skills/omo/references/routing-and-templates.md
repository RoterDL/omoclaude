# Routing and Templates

Read this file when routing agents. Contains signal table, recipes, invocation format, and examples.

## Routing Signals (No Fixed Pipeline)

This skill is **routing-first**, not a mandatory `explore → oracle → develop` conveyor belt.

| Signal | Add this agent |
|--------|----------------|
| Code location/behavior unclear | `explore` |
| External library/API usage unclear | `librarian` |
| Risky change: multi-file/module, public API, data format/config, concurrency, security/perf, or unclear tradeoffs | `oracle` |
| Implementation required | `develop` (or `frontend-ui-ux-engineer` / `document-writer`) |
| Post-implementation quality check requested, or implementation touched multiple files / public API | `code-reviewer` |

## Skipping Heuristics (Prefer Explicit Risk Signals)

- Skip `explore` when the user already provided exact file path + line number, or you already have it from context.
- Skip `oracle` when the change is **local + low-risk** (single area, clear fix, no tradeoffs). Line count is a weak signal; risk is the real gate.
- Skip `code-reviewer` when the change is trivial (single-line fix, comment-only, config tweak) and the user did not request review.
- Skip implementation agents when the user only wants analysis/answers (stop after `explore`/`librarian`).

## Common Recipes (Examples, Not Rules)

- Explain code: `explore`
- Small localized fix with exact location: **confirm** → `develop`
- Bug fix, location unknown: `explore` → **confirm** → `develop`
- Cross-cutting refactor / high risk: `explore → oracle` → **confirm** → `develop` (optionally `oracle` again for review)
- External API integration: `explore` + `librarian` (can run in parallel) → `oracle` (if risk) → **confirm** → implementation agent
- UI-only change: `explore` → **confirm** → `frontend-ui-ux-engineer` (split logic to `develop` if needed)
- Docs-only change: `explore` → **confirm** → `document-writer`
- Post-implementation review: `code-reviewer` (after `develop` / `frontend-ui-ux-engineer`)
- Review + fix: `code-reviewer` → **confirm** → `develop` (fix reported issues)
- Resume from saved analysis: Read `.spec/07-analysis/<dir>/analysis.md` → build Context Pack → route agents

## Agent Invocation Format

```bash
codeagent-wrapper --agent <agent_name> - <workdir> <<'EOF'
## Original User Request
<original request>

## Context Pack (include only what's available)
<List only the context items that exist. Omit agents that weren't invoked.>
- <Agent> output: <paste>
- Known constraints: <tests, time budget, conventions>

## Current Task
<specific task description>

## Acceptance Criteria
<clear completion conditions>
EOF
```

Execute in shell tool, timeout 2h.

## Agent Selection

| Agent | When to Use |
|-------|---------------|
| `explore` | Need to locate code position or understand code structure |
| `oracle` | Risky changes, tradeoffs, unclear requirements, or after failed attempts |
| `develop` | Backend/logic code implementation |
| `frontend-ui-ux-engineer` | UI/styling/frontend component implementation |
| `document-writer` | Documentation writing and editing: README, API docs, architecture docs, user guides, changelogs, config references |
| `librarian` | Need to lookup external library docs or OSS examples |
| `code-reviewer` | Post-implementation review, or user explicitly requests code review |

## Examples (Routing by Task)

<example>
User: /omo fix this type error at src/foo.ts:123

Sisyphus executes:

**Single step: develop** (location known; low-risk change)
```bash
codeagent-wrapper --agent develop - /path/to/project <<'EOF'
## Original User Request
fix this type error at src/foo.ts:123

## Context Pack
None

## Current Task
Fix the type error at src/foo.ts:123 with the minimal targeted change.

## Acceptance Criteria
Typecheck passes; no unrelated refactors.
EOF
```
</example>

<example>
User: /omo analyze this bug and fix it (location unknown)

Sisyphus executes:

**Step 1: explore**
```bash
codeagent-wrapper --agent explore - /path/to/project <<'EOF'
## Original User Request
analyze this bug and fix it

## Context Pack
None

## Current Task
Locate bug position, analyze root cause, collect relevant code context (thoroughness: medium).

## Acceptance Criteria
Output: problem file path, line numbers, root cause analysis, relevant code snippets.
EOF
```

**Step 2: User Confirmation Gate**

Present explore findings to user:
- Root cause analysis
- Proposed fix approach
- Files to be changed

Use `AskUserQuestion`:
- "Approve and proceed with fix"
- "Revise approach"

**Step 3: develop** (after user approval, use explore output as input)
```bash
codeagent-wrapper --agent develop - /path/to/project <<'EOF'
## Original User Request
analyze this bug and fix it

## Context Pack
- Explore output: [paste complete explore output]

## Current Task
Implement the minimal fix; run the narrowest relevant tests.

## Acceptance Criteria
Fix is implemented; tests pass; no regressions introduced.
EOF
```

Note: If explore shows a multi-file or high-risk change, consult `oracle` before `develop`.
</example>

<example>
User: /omo add feature X using library Y (need internal context + external docs)

Sisyphus executes:

**Step 1a: explore** (internal codebase)
```bash
codeagent-wrapper --agent explore - /path/to/project <<'EOF'
## Original User Request
add feature X using library Y

## Context Pack
None

## Current Task
Find where feature X should hook in; identify existing patterns and extension points.

## Acceptance Criteria
Output: file paths/lines for hook points; current flow summary; constraints/edge cases.
EOF
```

**Step 1b: librarian** (external docs/usage) — can run in parallel with explore
```bash
codeagent-wrapper --agent librarian - /path/to/project <<'EOF'
## Original User Request
add feature X using library Y

## Context Pack
None

## Current Task
Find library Y's recommended API usage for feature X; provide evidence/links.

## Acceptance Criteria
Output: minimal usage pattern; API pitfalls; version constraints; links to authoritative sources.
EOF
```

**Step 2: oracle** (optional but recommended if multi-file/risky)
```bash
codeagent-wrapper --agent oracle - /path/to/project <<'EOF'
## Original User Request
add feature X using library Y

## Context Pack
- Explore output: [paste explore output]
- Librarian output: [paste librarian output]

## Current Task
Propose the minimal implementation plan and file touch list; call out risks.

## Acceptance Criteria
Output: concrete plan; files to change; risk/edge cases; effort estimate.
EOF
```

**Step 3: User Confirmation Gate**

Present collected findings to user:
- Problem analysis (from explore)
- Library/API findings (from librarian)
- Implementation plan and risk assessment (from oracle, if used)
- Files to be changed and approach

Use `AskUserQuestion`:
- "Approve and proceed with implementation"
- "Revise approach"

**Step 4: develop** (after user approval, implement)
```bash
codeagent-wrapper --agent develop - /path/to/project <<'EOF'
## Original User Request
add feature X using library Y

## Context Pack
- Explore output: [paste explore output]
- Librarian output: [paste librarian output]
- Oracle output: [paste oracle output, or "None" if skipped]

## Current Task
Implement feature X using the established internal patterns and library Y guidance.

## Acceptance Criteria
Feature works end-to-end; tests pass; no unrelated refactors.
EOF
```
</example>

<example>
User: /omo how does this function work?

Sisyphus executes:

**Only explore needed** (analysis task, no code changes)
```bash
codeagent-wrapper --agent explore - /path/to/project <<'EOF'
## Original User Request
how does this function work?

## Context Pack
None

## Current Task
Analyze function implementation and call chain

## Acceptance Criteria
Output: function signature, core logic, call relationship diagram
EOF
```
</example>

## Anti-Examples

<anti_example>
User: /omo fix this type error

Wrong approach:
- Always run `explore → oracle → develop` mechanically
- Use grep to find files yourself
- Modify code yourself
- Invoke develop without passing context

Correct approach:
- Route based on signals: if location is known and low-risk, invoke `develop` directly
- Otherwise invoke `explore` to locate the problem (or to confirm scope), then delegate implementation
- Invoke the implementation agent with a complete Context Pack
</anti_example>

## Forbidden Behaviors

- **FORBIDDEN** to write code yourself (must delegate to implementation agent)
- **FORBIDDEN** to invoke an agent without the original request and relevant Context Pack
- **FORBIDDEN** to skip agents and use grep/glob for complex analysis
- **FORBIDDEN** to treat `explore → oracle → develop` as a mandatory workflow
