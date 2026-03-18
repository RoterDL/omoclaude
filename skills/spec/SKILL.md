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
4. **Reuse existing agents.** Reuse existing agents where possible: `spec-develop`, `spec-frontend`, `spec-reviewer`, `spec-code-reviewer` for implementation; `spec-explorer`, `spec-planner`, `plan-reviewer` for planning and review; `spec-tester` for testing.
5. **Defer worktree decision until Phase 3.** Only ask about worktree mode right before implementation. If enabled, prefix Phase 3 agent calls that operate in the worktree (`spec-develop`, `spec-frontend`, `spec-reviewer`, `spec-code-reviewer`, `spec-tester`) with `DO_WORKTREE_DIR=<path>`.
6. **Use `codeagent-wrapper` for all agent invocations.** All agent calls in Phase 2 and Phase 3 MUST go through `codeagent-wrapper` via Bash. Do NOT substitute Claude Code's built-in Agent/Explore tools.
7. **Plan.md content must come from `spec-planner` agent** (exception: trivial complexity). ALWAYS use `spec-manager.py update-body` to preserve YAML frontmatter.
8. **Review intensity governs review depth.** `spec-planner` sets `review_intensity` in plan.md Task Classification. Phase 2 plan review and Phase 3 code review depth scale with this setting. At `light`, external reviews are skipped (planner/implementer self-review + tests suffice). At `standard`, single-pass reviews with no iteration. At `full`, iterative reviews with max 2 rounds. The orchestrator may upgrade (never downgrade) intensity at Phase 3 based on actual diff size.
## Spec Lifecycle (4 Phases)
```text
/spec <task description>
-> Trivial detection -> if trivial: express-path (skip to Phase 2 minimal)
-> Phase 1: Intent Confirmation -> restate, clarify, AskUserQuestion gate
-> Complexity Triage -> light / standard / full
-> Phase 2: Design & Planning -> exp-search -> spec-explorer -> spec-planner -> plan.md -> plan-reviewer (intensity-gated) -> gate
-> Phase 3: Implementation -> worktree decision -> route spec-develop/spec-frontend -> summary.md -> spec-tester -> code review (intensity-gated) -> gate
-> Phase 4: Wrap-up -> /exp-reflect (intensity-gated) -> archive -> update-phase end
```
## Initialization (on /spec trigger)
When triggered via `/spec <task>`:
```bash
python "$HOME/.claude/skills/spec/scripts/spec-manager.py" create --category features --title "<task description>"
```
This creates a spec directory under `.spec/03-features/` (or appropriate category) with a `.current-spec` pointer.
## Trivial Detection (before Phase 1)
After initialization, check if the task is trivial before entering Phase 1:
- **trivial**: single file named + typo/wording fix or user said "just do it" -> express-path

If not trivial, proceed to Phase 1.

**Trivial express-path**: Skip Phase 1 and Complexity Triage. Phase 2: skip Steps 1-2, orchestrator writes minimal plan at Step 3 (HC#7 exception), skip Step 5, merge Step 6 gate with Phase 3 Step 6. Phase 3: skip Step 0/4/5. Phase 4: skip Step 1.
## Phase 1: Intent Confirmation
Use the intent-confirm sub-skill logic:
1. Restate user's intent in concrete, actionable terms.
2. List key understanding points.
3. Identify ambiguities or multiple interpretations.
4. Use `AskUserQuestion` to confirm:
   - "Confirmed, proceed to planning"
   - "Need to clarify" (with details)
## Complexity Triage (after Phase 1)
Evaluate task before Phase 2. Produce `complexity_level` (non-trivial tasks only):
- **light**: narrow scope, few files, low risk -> skip spec-explorer
- **standard**: default
- **full**: large scope, high risk, cross-cutting changes
This is orchestrator judgment, independent of `review_intensity` (set later by `spec-planner`).
## Phase 2: Design & Planning
**If trivial**: Skip Steps 1-2; at Step 3, orchestrator writes minimal plan directly via `update-body`; skip Step 5; merge Step 6 with Phase 3 gate.
Steps 1-4 and Step 6 are mandatory per Hard Constraints #6-#8. Step 5 (plan review) depth is governed by Hard Constraint #8 (`review_intensity`).
### Step 1: Search related experience
Read `.spec/context/experience/index.md` and `.spec/context/knowledge/index.md` if they exist. Skip if `.spec/context/` absent.
### Step 2: Explore codebase (via spec-explorer agent)
Use `codeagent-wrapper --agent spec-explorer` via Bash. Do NOT replace it with the built-in Explore/Agent tool.
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
### Step 3: Generate design spec (via spec-planner agent)
Delegate `plan.md` content generation to `codeagent-wrapper --agent spec-planner`; do not author it yourself.
```bash
codeagent-wrapper --agent spec-planner - . <<'EOF'
## Original User Request
<user request>

## Context Pack
- Experience search results: <paste or "None">
- Explore output: <paste>
- Existing spec context: <paste or "None">

## Current Task
Create a design specification (plan.md) including:
1. Overview (background, goals, scope)
2. Requirements analysis
3. Design approach (with alternatives considered)
4. Implementation steps (file touch list)
5. Task classification
6. Risks and dependencies
7. Non-goals
**Review & self-review:** Plan will be reviewed by plan-reviewer (7-area checklist); BLOCKING issues trigger revision. Self-check all sections for completeness and specificity before outputting.
Output the full plan.md content.
## Acceptance Criteria
Complete plan.md ready for user review.
EOF
```
### Step 4: Write plan.md
Pipe the `spec-planner` output through `update-body` to preserve frontmatter, then advance phase:
```bash
echo '<spec-planner output>' | python "$HOME/.claude/skills/spec/scripts/spec-manager.py" update-body
# Or from a file:
python "$HOME/.claude/skills/spec/scripts/spec-manager.py" update-body --file /tmp/plan-body.md

python "$HOME/.claude/skills/spec/scripts/spec-manager.py" update-phase plan
```
Do NOT overwrite `plan.md` directly via Write/cp; direct overwrites break the YAML frontmatter.
### Step 5: Plan review (intensity-gated)
Read plan.md Task Classification to get `review_intensity`. If missing, default to `standard`.
**light intensity**: Skip plan-reviewer. Log "Plan review skipped (light intensity)." Proceed to Step 6.
**standard or full intensity**: Invoke plan-reviewer:
```bash
codeagent-wrapper --agent plan-reviewer - . <<'EOF'
## Original User Request
<user request>

## Context Pack
- Plan: <paste plan.md content>

## Current Task
Review plan.md against the 7-area checklist. Report BLOCKING and MINOR issues.

## Acceptance Criteria
Issue report with BLOCKING/MINOR classification. Summary line: BLOCKING=<n>, MINOR=<n>.
EOF
```
**Result handling by intensity:**
- Save via:
```bash
echo '<plan-reviewer output>' | python "$HOME/.claude/skills/spec/scripts/spec-manager.py" write-artifact plan-review.md
```
- **standard**: Proceed to Step 6 regardless of BLOCKING count (user decides at gate).
- **full**: Initialize revision counter at 0.
  - **BLOCKING=0**: proceed to Step 6.
  - **BLOCKING>0 and iteration < 2**: re-invoke `spec-planner` with reviewer feedback appended to Context Pack, re-write `plan.md` via `update-body`, re-review.
  - **BLOCKING>0 and iteration >= 2**: present to user via `AskUserQuestion` for guidance.
### Step 6: User confirmation gate
Present `plan.md` to the user. Use `AskUserQuestion`:
- "Approve design and proceed to implementation"
- "Revise design" (with feedback)
**Do NOT proceed to Phase 3 until user explicitly approves.**
## Phase 3: Implementation
**If trivial**: Skip Step 0 (no worktree), Step 4 (spec-tester), Step 5 (code review).
### Step 0: Decide on worktree mode (ONLY NOW)
Use `AskUserQuestion` to ask:
```text
Develop in a separate worktree? (Isolates changes from main branch)
- Yes (Recommended for larger changes)
- No (Work directly in current directory)
```
If user chooses worktree:
```bash
python "$HOME/.claude/skills/spec/scripts/spec-manager.py" enable-worktree
# Save the DO_WORKTREE_DIR from output
```
If worktree mode is enabled, prepend `DO_WORKTREE_DIR=<worktree_dir>` to all Phase 3 `codeagent-wrapper` invocations below (per Hard Constraint #5).
### Step 1: Determine implementation strategy
Based on `plan.md` `task_type` classification:
| task_type | Agent | Skills flag | Scope label |
|-----------|-------|------------|-------------|
| `backend_only` | `spec-develop` | (none) | (omit) |
| `frontend_only` | `spec-frontend` | `--skills taste-core,taste-output` | "frontend" |
| `fullstack` | both in parallel | frontend gets taste skills | "backend"/"frontend" |
- Missing `task_type`: default to `spec-develop`.
- **Optional**: append `taste-creative` for creative/premium UI; `taste-redesign` for UI overhaul.
Select **Review notice** based on `review_intensity`:
- **light**: `**Review notice:** Your code will be validated by tests. Apply Priority A self-review before outputting.`
- **standard**: `**Review notice:** After implementation, your code will be reviewed (Priority A/B). Write clean, correct code.`
- **full**: `**Review notice:** After implementation, your code will undergo thorough review (Priority A/B/C). Write clean, correct, minimal code.`
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
Implement {scope_label} changes according to plan.md. Follow existing patterns. Add/adjust tests per plan.
{review_notice}

## Acceptance Criteria
All plan items implemented. Tests pass.
EOF
```
**Fullstack (parallel)**: Use `codeagent-wrapper --parallel` with two `---TASK---` blocks following the same template structure. Backend task uses `spec-develop`, frontend task uses `spec-frontend` with `skills: taste-core,taste-output`. Each task's Acceptance Criteria should end with `Summary: <one sentence>`.
After implementation completes:
```bash
python "$HOME/.claude/skills/spec/scripts/spec-manager.py" update-phase implement
```
### Step 3: Generate summary.md
Summarize: implemented scope, key files changed, test updates. Save via:
```bash
echo '<summary content>' | python "$HOME/.claude/skills/spec/scripts/spec-manager.py" write-artifact summary.md
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
echo '<spec-tester output>' | python "$HOME/.claude/skills/spec/scripts/spec-manager.py" write-artifact test-report.md
```
**Handle test results:**
- All tests pass: proceed to Step 5.
- Tests fail: delegate fix to `spec-develop` (or `spec-frontend` for UI issues), update `summary.md` to reflect fixes, then re-test.
### Step 5: Code review (intensity-gated)
Read `review_intensity` from plan.md. Capture diff:
```bash
DIFF_OUTPUT=$(bash "$HOME/.claude/skills/spec/scripts/capture-diff.sh")
```
Count changed lines and files. If actual counts exceed the next tier's thresholds (>3 files or >100 lines -> at least `standard`; >10 files or >500 lines -> `full`), upgrade intensity.
**light intensity**: Skip code review. Log "Code review skipped (light intensity; self-review + tests passed)." Proceed to Step 6.
**standard or full intensity**: Select reviewer and scope:
- **standard**: agent=`spec-reviewer`, scope="Priority A and B items ONLY. Skip Priority C (Conventions)."
- **full**: agent=`spec-code-reviewer`, scope="all priorities: A (Correctness), B (Optimization), C (Conventions)."
```bash
codeagent-wrapper --agent {reviewer_agent} - . <<'EOF'
## Original User Request
<user request>

## Context Pack
- Plan: <paste plan.md>
- Summary: <paste summary.md>
- Diff: <paste DIFF_OUTPUT>

## Current Task
Review implementation against plan.md.
**Scope: Review {scope_line}.**

## Acceptance Criteria
Summary: BLOCKING=<n>, MINOR=<n>.
EOF
```
```bash
echo '<review output>' | python "$HOME/.claude/skills/spec/scripts/spec-manager.py" write-artifact review-report.md
```
**Result handling:**
- **standard**: If BLOCKING > 0, present to user via `AskUserQuestion` for guidance. Proceed to Step 6.
- **full**: Initialize `review_iteration=0`. BLOCKING=0 -> proceed. BLOCKING>0 and iteration<2 -> delegate fixes, re-capture diff, re-review. BLOCKING>0 and iteration>=2 -> present to user.
### Step 6: Completion gate
Use `AskUserQuestion` to confirm test and review results with the user.
```bash
python "$HOME/.claude/skills/spec/scripts/spec-manager.py" update-phase test  # marks implementation+testing complete
```
## Phase 4: Wrap-up
**If trivial**: Skip Step 1 (experience reflection).
### Step 0: Verify completion
Read the spec directory and verify expected artifacts exist:
- `plan.md` (confirmed)
- `summary.md` (implementation complete)
- `test-report.md` (tests passed; skipped for trivial express-path)
- `review-report.md` (if review was run)
If any critical artifact is missing, prompt the user to confirm whether to continue.
### Step 1: Experience reflection (intensity-gated)
For `standard` and `full` intensity, this step is **mandatory**. For `light` intensity, default to skip (offer "Run anyway" as secondary choice).
The orchestrator reads spec artifacts (`plan.md`, `summary.md`, `review-report.md`, `test-report.md`) and extracts reusable lessons:
1. **Experience (dilemma-strategy pairs)**: implementation problems and resolutions, BLOCKING issues and fix strategies
2. **Knowledge (project understanding)**: architecture patterns, code conventions
Present findings to user via `AskUserQuestion`. After confirmation:
1. Save local artifact:
```bash
echo '<reflection content>' | python "$HOME/.claude/skills/spec/scripts/spec-manager.py" write-artifact experience-reflection.md
```
2. Persist to project memory indexes via Skill tool:
   - Call `/exp-write type=experience` for dilemma-strategy pairs
   - Call `/exp-write type=knowledge` for project understanding
Use `AskUserQuestion`:
- For standard/full: "Run experience extraction now" (recommended) / "Skip"
- For light: "Skip experience extraction (light task)" (recommended) / "Run anyway"
### Step 2: Archive confirmation
Use `AskUserQuestion`:
- "Archive spec and optionally commit"
- "Keep spec in current location"
### Step 3: Archive (if confirmed)
```bash
python "$HOME/.claude/skills/spec/scripts/spec-manager.py" archive
```
This moves the spec directory to `.spec/06-archived/`.
```bash
python "$HOME/.claude/skills/spec/scripts/spec-manager.py" update-phase end
```
### Step 4: Completion summary
```
Spec lifecycle complete:
- Plan: plan.md (confirmed)
- Implementation: summary.md
- Review: review-report.md [pass/iterations]
- Tests: test-report.md [passed/failed/skipped for trivial]
- Experience: [captured N items / skipped (reason)]
- Archive: [archived to 06-archived/ / kept in place]
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
## Additional References
- Related agents: `spec-explorer`, `spec-planner`, `plan-reviewer`, `spec-develop`, `spec-frontend`, `spec-reviewer`, `spec-code-reviewer`, `spec-tester`.
