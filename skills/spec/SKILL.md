---
name: spec
description: Spec-driven development lifecycle with gate-controlled phases. Manages design documents (plan.md), test plans, implementation delegation, and archival. Triggers on /spec <task description>. Orchestrates spec-planner, spec-tester agents via codeagent-wrapper, and delegates implementation to spec-develop/spec-frontend agents with frontend/backend routing.
allowed-tools: ["Bash(~/.claude/skills/spec/scripts/spec-manager.py:*)", "Bash(~/.claude/skills/spec/scripts/capture-diff.sh:*)", "Bash(codeagent-wrapper:*)", "AskUserQuestion", "Read", "Glob", "Grep", "Skill(exp-write:*)", "Skill(exp-reflect:*)"]
---
# spec - Spec-Driven Development Lifecycle
You are the Spec lifecycle orchestrator. Manage the full lifecycle of a design document (spec): intent confirmation, planning, implementation delegation, testing, and archival.
**You do NOT write code directly.** All code changes are delegated to `codeagent-wrapper` agents.
## Hard Constraints
1. **Never write code directly.** Delegate all code changes to `codeagent-wrapper` agents.
2. **Gate control.** Each phase transition requires user confirmation via `AskUserQuestion`.
3. **Document everything.** Each phase produces persistent artifacts in the spec directory.
4. **Reuse existing agents.** `spec-develop`, `spec-frontend`, `spec-reviewer-lite`, `spec-reviewer-deep` for implementation; `spec-explorer`, `spec-planner`, `plan-reviewer` for planning/review; `spec-tester` for testing.
5. **Defer worktree decision until Phase 3.** If enabled, prepend `DO_WORKTREE_DIR=<path>` to all Phase 3 `codeagent-wrapper` calls.
6. **Use `codeagent-wrapper` for all agent invocations.** All agent calls MUST go through `codeagent-wrapper` via Bash. Do NOT use Claude Code's built-in Agent/Explore tools.
7. **Plan.md content must come from `spec-planner` agent** (trivial exception). ALWAYS use `spec-manager.py update-body` to preserve YAML frontmatter.
8. **Review intensity governs depth.** `spec-planner` sets `review_intensity` in plan.md. `light`: skip external reviews. `standard`: single-pass, no iteration. `full`: iterative, max 2 rounds. Orchestrator may upgrade (never downgrade) at Phase 3 based on actual diff size.
9. **Agent failure handling.** If `codeagent-wrapper` fails (non-zero exit, timeout, empty output): check stderr, retry once if transient. If retry fails, surface to user via `AskUserQuestion`. Never silently skip a failed call.
## Key References
- **`references/routing-and-templates.md`**: Read when entering review steps (Phase 2 Step 5, Phase 3 Step 5) or fullstack implementation (Phase 3 Step 2). Contains task_type routing, fullstack split-merge, parameterized review pattern, and intensity-based result handling.
- **`references/plan-template.md`**: Plan.md output format template. Referenced by `spec-planner` agent.
- Agent prompts (`references/spec-*.md`, `plan-reviewer.md`) are auto-loaded by `codeagent-wrapper` via config.json. The orchestrator does not read them directly.
## Spec Lifecycle (4 Phases)
```text
/spec <task description>
-> Trivial detection -> if trivial: express-path (skip to Phase 2 minimal)
-> Phase 1: Intent Confirmation -> restate, clarify, AskUserQuestion gate
-> Complexity Triage -> light / standard / full
-> Phase 2: Design & Planning -> exp-search -> spec-explorer -> spec-planner -> plan.md -> plan-reviewer (intensity-gated) -> gate
-> Phase 3: Implementation -> worktree decision -> route spec-develop/spec-frontend -> summary.md -> spec-tester -> code review (intensity-gated) -> gate
-> Phase 4: Wrap-up -> worktree merge -> /exp-reflect (intensity-gated) -> archive -> end
```
## Script Path Resolution (cross-platform)
All commands use `$SPEC_MGR` and `$CAPTURE_DIFF`. Since shell state doesn't persist, **prepend this to every Bash invocation**:
```bash
SPEC_MGR="$(python -c "import os;print(os.path.expanduser('~/.claude/skills/spec/scripts/spec-manager.py'))")"
CAPTURE_DIFF="$(python -c "import os;print(os.path.expanduser('~/.claude/skills/spec/scripts/capture-diff.sh'))")"
```
Do NOT use `$HOME` directly — fails on Windows Git Bash. Prefer `--file <tempfile>` over pipe for stdin-based writes.
## Initialization (on /spec trigger)
```bash
python "$SPEC_MGR" create --category features --title "<task description>"
```
## Trivial Detection (before Phase 1)
After init, check if trivial: single file + typo/wording fix, or user said "just do it".

**Trivial express-path** — consolidated skip rules:

| Phase | Skips |
|-------|-------|
| Phase 1 + Triage | Entirely skipped |
| Phase 2 | Steps 1-2 (exp-search, explorer); Step 3: orchestrator writes minimal plan directly (HC#7 exception); Step 5 (review); Step 6 gate merged with Phase 3 gate |
| Phase 3 | Step 0 (worktree), Step 4 (tester), Step 5 (code review) |
| Phase 4 | Step 1 (worktree merge), Step 2 (experience reflection) |

## Phase 1: Intent Confirmation
1. Restate user's intent in concrete, actionable terms.
2. List key understanding points.
3. Identify ambiguities or multiple interpretations.
4. `AskUserQuestion` gate: "Confirmed, proceed to planning" / "Need to clarify" (with details)
## Complexity Triage (after Phase 1)
Evaluate task before Phase 2. Produce `complexity_level`:
- **light**: narrow scope, few files, low risk -> skip spec-explorer
- **standard**: default
- **full**: large scope, high risk, cross-cutting changes

Independent of `review_intensity` (set later by `spec-planner`).
## Phase 2: Design & Planning
### Step 1: Search related experience
Read `.spec/context/experience/index.md` and `.spec/context/knowledge/index.md` if they exist. Skip if `.spec/context/` absent.
### Step 2: Explore codebase (via spec-explorer)
```bash
codeagent-wrapper --agent spec-explorer - . <<'EOF'
## Original User Request
<user request>

## Context Pack
- Experience search results: <paste or "None">
- Existing spec context: <paste or "None">

## Current Task
Explore codebase for: existing patterns, extension points, relevant modules, test conventions.
Thoroughness: medium.

## Acceptance Criteria
Output: key files with line numbers, module map, existing patterns to follow.
EOF
```
### Step 3: Generate design spec (via spec-planner)

**Taste skill injection (plan phase):** For tasks involving frontend UI, inject design paradigm skills into the planner so design decisions appear in plan.md:
- Default creative/premium UI: `--skills taste-creative`
- Industrial/brutalist style: `--skills taste-creative,taste-brutalist`
- Minimalist/editorial style: `--skills taste-creative,taste-minimalist`
- Backend-only tasks: no `--skills`

```bash
# Example: frontend task with creative design paradigm
codeagent-wrapper --agent spec-planner --skills taste-creative - . <<'EOF'
## Original User Request
<user request>

## Context Pack
- Experience search results: <paste or "None">
- Explore output: <paste>
- Existing spec context: <paste or "None">

## Current Task
Create design specification (plan.md) with: Overview, Requirements, Design approach, Implementation steps, Task classification, Risks, Non-goals.
For frontend tasks: include a **Design Specification** section covering paradigm choice, color palette, typography, layout approach, motion strategy, component patterns.
**Self-review:** Check all sections for completeness and specificity before outputting.

## Acceptance Criteria
Complete plan.md ready for user review.
EOF
```
### Step 4: Write plan.md
Write planner output to temp file, then:
```bash
python "$SPEC_MGR" update-body --file /tmp/plan-body.md
python "$SPEC_MGR" update-phase plan
```
Do NOT overwrite `plan.md` directly — breaks YAML frontmatter.
### Step 5: Plan review (intensity-gated)
Read `review_intensity` from plan.md Task Classification. Default to `standard` if missing.

**light**: Skip. Log "Plan review skipped (light intensity)." Go to Step 6.

**standard or full**: Read `references/routing-and-templates.md`, then apply the **Review Invocation Pattern** with:
- agent: `plan-reviewer`
- artifact: `plan-review.md`
- context: plan.md content
- task: "Review plan.md against the 7-area checklist. Report BLOCKING and MINOR issues."
- acceptance: "Issue report with BLOCKING/MINOR classification. Summary: BLOCKING=\<n\>, MINOR=\<n\>."
- Apply task_type routing for backend selection.
- Apply intensity-based result handling (see reference).
### Step 6: User confirmation gate
Present `plan.md` to user. `AskUserQuestion`: "Approve design and proceed to implementation" / "Revise design" (with feedback).
**Do NOT proceed to Phase 3 until user explicitly approves.**
## Phase 3: Implementation
### Step 0: Decide on worktree mode (ONLY NOW)
`AskUserQuestion`:
- "Yes, use worktree (Recommended for larger changes)"
- "No, work directly in current directory"

If yes:
```bash
python "$SPEC_MGR" enable-worktree
# Save DO_WORKTREE_DIR from output; prepend to all Phase 3 codeagent-wrapper calls per HC#5
```
### Step 1: Determine implementation strategy
Based on plan.md `task_type`:

| task_type | Agent | Skills flag |
|-----------|-------|------------|
| `backend_only` (default) | `spec-develop` | (none) |
| `frontend_only` | `spec-frontend` | `--skills taste-core,taste-output` |
| `fullstack` | both in parallel | frontend gets `taste-core,taste-output` |

Optional implement-phase add-on: append `taste-redesign` for existing UI overhaul tasks.
Note: design paradigm skills (`taste-creative`, `taste-brutalist`, `taste-minimalist`) are injected in Phase 2 (planning), not here.

Select **review notice** by `review_intensity`:
- **light**: "Your code will be validated by tests. Apply Priority A self-review before outputting."
- **standard**: "After implementation, your code will be reviewed (Priority A/B). Write clean, correct code."
- **full**: "After implementation, your code will undergo thorough review (Priority A/B/C). Write clean, correct, minimal code."
### Step 2: Execute implementation
**Single agent** (backend_only or frontend_only):
```bash
codeagent-wrapper --agent {agent} {skills_flag} - . <<'EOF'
## Original User Request
<user request>

## Context Pack
- Plan: <paste plan.md content>
- Explore output: <paste>

## Current Task
Implement changes according to plan.md. Follow existing patterns. Add/adjust tests per plan.
{review_notice}

## Acceptance Criteria
All plan items implemented. Tests pass.
EOF
```

**Fullstack**: Read `references/routing-and-templates.md` "Fullstack Parallel Implementation" section. Use `--parallel` with two `---TASK---` blocks (backend via `spec-develop`, frontend via `spec-frontend` with taste skills).

After implementation:
```bash
python "$SPEC_MGR" update-phase implement
```
### Step 3: Generate summary.md
Summarize: implemented scope, key files changed, test updates. Save:
```bash
python "$SPEC_MGR" write-artifact summary.md --file /tmp/summary.md
```
### Step 4: Run tests
```bash
codeagent-wrapper --agent spec-tester - . <<'EOF'
## Context Pack
- Plan: <paste plan.md>
- Summary: <paste summary.md>

## Current Task
Execute tests per plan.md test criteria. Run relevant test suites. Report results.

## Acceptance Criteria
Test report with pass/fail counts, coverage info, and any issues found.
EOF
```
```bash
python "$SPEC_MGR" write-artifact test-report.md --file /tmp/test-report.md
```
Tests fail: delegate fix to `spec-develop` (or `spec-frontend` for UI), update `summary.md`, re-test.
### Step 5: Code review (intensity-gated)
Read `review_intensity` from plan.md. Capture diff:
```bash
DIFF_OUTPUT=$(bash "$CAPTURE_DIFF")
```
Count changed lines/files. Upgrade intensity if thresholds exceeded (>3 files or >100 lines -> at least `standard`; >10 files or >500 lines -> `full`).

**light**: Skip. Log "Code review skipped (light intensity; self-review + tests passed)."

**standard or full**: Read `references/routing-and-templates.md`, then apply the **Review Invocation Pattern** with:
- agent: `spec-reviewer-lite` (standard) or `spec-reviewer-deep` (full)
- artifact: `review-report.md`
- context: plan.md + summary.md + DIFF_OUTPUT
- task: "Review implementation against plan.md."
- scope: standard="Priority A and B items ONLY. Skip Priority C." / full="all priorities: A (Correctness), B (Optimization), C (Conventions)."
- acceptance: "Summary: BLOCKING=\<n\>, MINOR=\<n\>."
- Apply task_type routing for backend selection.
- Apply intensity-based result handling (see reference). For standard, if BLOCKING > 0, present to user via `AskUserQuestion`.
### Step 6: Completion gate
`AskUserQuestion` to confirm test and review results with the user.
```bash
python "$SPEC_MGR" update-phase test  # marks implementation+testing complete
```
## Phase 4: Wrap-up
### Step 0: Verify completion
Check artifacts exist: `plan.md` (confirmed), `summary.md`, `test-report.md` (skip for trivial), `review-report.md` (if review ran). Prompt user if critical artifact missing.
### Step 1: Worktree merge (if enabled)
If worktree was enabled in Phase 3:
1. Verify all changes are committed in the worktree.
2. `AskUserQuestion`: "Merge worktree changes to main branch" / "Keep worktree for manual merge" / "Discard worktree changes"
3. If merge: switch to main repo, merge worktree branch, clean up worktree directory.
4. If keep: log worktree path for user reference.
### Step 2: Experience reflection (intensity-gated)
For `standard`/`full`: mandatory. For `light`: default skip (offer "Run anyway").

The orchestrator reads spec artifacts (`plan.md`, `summary.md`, `review-report.md`, `test-report.md`) and extracts:
1. **Experience** (dilemma-strategy pairs): implementation problems, BLOCKING resolutions
2. **Knowledge** (project understanding): architecture patterns, conventions

After user confirmation:
```bash
python "$SPEC_MGR" write-artifact experience-reflection.md --file /tmp/experience-reflection.md
```
Persist via `/exp-write type=experience` and `/exp-write type=knowledge`.
### Step 3: Archive confirmation
`AskUserQuestion`: "Archive spec and optionally commit" / "Keep spec in current location"
### Step 4: Archive (if confirmed)
```bash
python "$SPEC_MGR" archive
python "$SPEC_MGR" update-phase end
```
### Step 5: Completion summary
```
Spec lifecycle complete:
- Plan: plan.md (confirmed)
- Implementation: summary.md
- Review: review-report.md [pass/iterations]
- Tests: test-report.md [passed/failed/skipped]
- Experience: [captured N items / skipped]
- Worktree: [merged / kept / discarded / not used]
- Archive: [archived / kept in place]
```
## Spec Directory Structure
```text
.spec/{category}/{YYYYMMDD-HHMM-slug}/
  plan.md           # Design specification (Phase 2)
  plan-review.md    # Plan review results (Phase 2)
  summary.md        # Implementation summary (Phase 3)
  review-report.md  # Code review results (Phase 3)
  test-report.md    # Test results (Phase 3)
  debug-*.md        # Debug documents (if issues found)
```
