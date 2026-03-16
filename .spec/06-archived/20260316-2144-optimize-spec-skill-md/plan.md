---
title: optimize-spec-skill-md
type: plan
category: 03-features
status: testing
phase: test
created: 2026-03-16
tags: ["spec", "plan"]
use_worktree: false
worktree_dir: 
---




# Plan: Optimize SKILL.md — Redundancy, Logic Fixes, Efficiency

## 1. Overview

### Background
`skills/spec/SKILL.md` was reduced from 693->476 lines in a prior optimization (20260316-1628). That pass focused on worktree variant deduplication and reference table consolidation. The current 476-line file still contains internal redundancies (duplicated templates, inline scripts, repeated worktree mentions), logic gaps (missing artifact saves, missing phase transition), and treats all tasks uniformly regardless of complexity.

### Goals
1. Reduce SKILL.md from ~476 lines to ~370 lines (~22% reduction) by eliminating content redundancy
2. Fix 4 identified logic defects that cause missing artifacts or incorrect phase state
3. Introduce efficiency differentiation so simple tasks complete with fewer agent calls

### Scope
- **In scope**: `skills/spec/SKILL.md` content edits (including frontmatter `allowed-tools`), new `skills/spec/scripts/capture-diff.sh` extraction
- **Out of scope**: Changes to sub-skill files, agent prompt files (spec-planner.md, etc.), spec-manager.py, codeagent-wrapper

## 2. Requirements Analysis

### Functional Requirements
1. **FR-1**: Diff capture logic (current lines 309-334) must be extracted to `scripts/capture-diff.sh` and invoked with a single line in SKILL.md
2. **FR-2**: Plan-reviewer template must appear once; standard and full branches differ only in result-handling logic
3. **FR-3**: Phase 3 Step 2 implementation templates (backend/frontend/fullstack) must be consolidated into a routing table + single parameterized template
4. **FR-4**: Worktree mentions in Phase 3 body text (Steps 0, 4, 5) must be reduced — keep Hard Constraint #5 and Worktree Mode section as authoritative, use brief back-references elsewhere
5. **FR-5**: Tail state commands section (current lines 466-476) must be removed (commands already appear inline in relevant phases)
6. **FR-6**: `test-report.md` save instruction must be added after Phase 3 Step 4
7. **FR-7**: `review-report.md` save instruction must be added in standard intensity code review path
8. **FR-8**: `update-phase implement` call must be added at Phase 3 Step 2 completion
9. **FR-9**: Phase 4 Step 1 experience reflection must be intensity-gated: light = offer skip as default choice
10. **FR-10**: Simple tasks must be fast-tracked via an **orchestrator pre-assessment** mechanism: before Phase 2 Step 2 (explorer), the orchestrator evaluates the task description for triviality signals (single file mentioned, typo-level fix, user says "just do it", obviously narrow scope). If trivial, skip `spec-explorer` and use orchestrator's own lightweight search. This decision is independent of `review_intensity`, which is set later by `spec-planner` in Step 3 and gates Steps 5+.
11. **FR-11**: SKILL.md frontmatter `allowed-tools` must include `Bash(~/.claude/skills/spec/scripts/capture-diff.sh:*)` to permit the extracted script at runtime

### Non-functional Requirements
- **NF-1**: Final line count <= 380 lines (target ~370)
- **NF-2**: No behavioral change for `standard` and `full` intensity tasks (except bug fixes)
- **NF-3**: `capture-diff.sh` must be POSIX-compatible and handle both worktree and non-worktree modes

## 3. Design Approach

### Chosen Approach
Three targeted optimization areas in a single editing pass plus one new script file:

**A. Redundancy reduction** (~95 lines saved):
- Extract diff capture to `scripts/capture-diff.sh` (~24 lines -> 1 invocation line)
- Deduplicate plan-reviewer template (~12 lines saved)
- Parameterize implementation templates with routing table + single template (~35 lines saved)
- Slim worktree references in body text (~13 lines saved)
- Delete tail state commands section (~11 lines saved)

**B. Logic fixes** (net +5 lines):
- Add `test-report.md` save after Phase 3 Step 4 (+1 line)
- Add `review-report.md` save in standard intensity path (+1 line)
- Add `update-phase implement` call (+2 lines)
- Gate Phase 4 reflection on intensity (+1 line)

**C. Efficiency fast-track** (net +6 lines):
- Orchestrator pre-assessment gate before Phase 2 Step 2: orchestrator inspects the original task description for triviality signals and decides whether to skip explorer
- Light intensity gates at Steps 5+ (set by spec-planner in Step 3)

**Net**: -95 + 5 + 6 - 20 (prose trim) = ~104 lines removed -> ~372 lines

### Alternatives Considered
1. **Extract all agent templates to separate files**: Scatters workflow across many files, harder for LLM orchestrator to follow. Rejected.
2. **Separate `light` workflow as distinct section**: Creates divergent flows harder to maintain. Rejected in favor of inline intensity gates.
3. **Use `review_intensity` to gate explorer skip**: Rejected because `review_intensity` is set by `spec-planner` in Step 3, after the explorer decision in Step 2. Timing conflict makes this impossible.

### Key Design Decisions
- **Orchestrator pre-assessment (not review_intensity) gates explorer skip**: The orchestrator makes a quick triviality judgment from the task description *before* Step 2. This is independent of `review_intensity`, which `spec-planner` sets in Step 3 and which gates later phases (Step 5 plan review, Phase 3 code review, Phase 4 reflection). Two separate mechanisms, two separate timing points.
- **Routing table approach for implementation templates**: Table maps `task_type` -> agent, skills, scope label. Single template with placeholders follows.
- **capture-diff.sh as standalone script**: Complex enough (worktree branching, untracked file handling) to warrant extraction. Requires explicit `allowed-tools` frontmatter entry.

## 4. Implementation Steps

### Files touched
| File | Action |
|------|--------|
| `skills/spec/SKILL.md` | Edit (major restructure, including frontmatter) |
| `skills/spec/scripts/capture-diff.sh` | Create new |

### Step 1: Update SKILL.md frontmatter `allowed-tools`
**File**: `skills/spec/SKILL.md` (frontmatter section)
**Change**: Add `"Bash(~/.claude/skills/spec/scripts/capture-diff.sh:*)"` to the `allowed-tools` array alongside existing `spec-manager.py` and `codeagent-wrapper` entries.
**Why**: FR-11 — without this, the extracted `capture-diff.sh` script will be blocked at runtime by the tool permission system.

### Step 2: Create `capture-diff.sh`
**File**: `skills/spec/scripts/capture-diff.sh` (new)
**Change**: Extract SKILL.md lines 309-334 to standalone POSIX script. Script reads `DO_WORKTREE_DIR` env var, outputs combined diff (tracked + untracked) to stdout. `chmod +x`.
**Why**: FR-1.

### Step 3: Deduplicate plan-reviewer template (Phase 2 Step 5)
**File**: `skills/spec/SKILL.md` (current lines 124-168)
**Change**: Show template once after intensity gate, then branch on result handling only. **Before**: ~45 lines -> **After**: ~30 lines.
**Why**: FR-2.

### Step 4: Parameterize Phase 3 Step 2 templates
**File**: `skills/spec/SKILL.md` (current lines 197-283)
**Change**: Replace 3 templates with routing table + single parameterized template + fullstack parallel note. **Before**: ~80 lines -> **After**: ~45 lines.
**Why**: FR-3.

### Step 5: Slim worktree references in Phase 3
**File**: `skills/spec/SKILL.md` (lines 187, 289, 306, 339, 360)
**Change**: Replace verbose reminders with brief parenthetical back-references to Hard Constraint #5 / Worktree Mode section.
**Why**: FR-4.

### Step 6: Delete tail state commands
**File**: `skills/spec/SKILL.md` (lines 466-476)
**Change**: Remove section. Keep agent/sub-skill references (lines 461-465) in compact form.
**Why**: FR-5.

### Step 7: Add `test-report.md` save instruction
**File**: `skills/spec/SKILL.md` (after Phase 3 Step 4, ~line 301)
**Change**: Add "Save spec-tester output as `test-report.md` in the spec directory."
**Why**: FR-6.

### Step 8: Add `review-report.md` save in standard intensity
**File**: `skills/spec/SKILL.md` (after standard intensity review handling, ~line 358)
**Change**: Add "Save review output as `review-report.md`."
**Why**: FR-7.

### Step 9: Add `update-phase implement`
**File**: `skills/spec/SKILL.md` (after Phase 3 Step 2 completion)
**Change**: Insert `update-phase implement` call.
**Why**: FR-8.

### Step 10: Add orchestrator pre-assessment gate in Phase 2
**File**: `skills/spec/SKILL.md` (Phase 2, before Step 2)
**Change**: Add a pre-assessment gate block:
- **Timing**: Before Step 2 (explorer), after Step 1 (context pack).
- **Mechanism**: Orchestrator evaluates the original task description for triviality signals: single file explicitly named, typo/wording-level fix, user signals urgency ("just do it"), obviously narrow scope.
- **If trivial**: Skip `spec-explorer` agent, orchestrator performs own lightweight codebase search (grep/glob), passes streamlined context to `spec-planner` in Step 3.
- **If not trivial**: Proceed to `spec-explorer` as normal.
- **Relationship to `review_intensity`**: This pre-assessment is the orchestrator's own judgment, entirely independent. `spec-planner` sets `review_intensity` in Step 3 afterward, which gates Step 5 (plan review depth), Phase 3 (code review depth), and Phase 4 (reflection skip).
**Why**: FR-10. Resolves timing conflict — explorer skip is decided before `review_intensity` exists.

### Step 11: Gate Phase 4 Step 1 reflection by intensity
**File**: `skills/spec/SKILL.md` (Phase 4 Step 1)
**Change**: Light: default to skip. Standard/full: keep mandatory with "Run now" default.
**Why**: FR-9.

### Step 12: Final prose trimming
**File**: `skills/spec/SKILL.md` (throughout)
**Change**: Tighten all verbose phrasing. Target ~370 total lines.
**Why**: NF-1.

### Build Sequence
Steps 1-2 (frontmatter + script) are prerequisites. Steps 3-12 are independent edits within SKILL.md and can be done in any order, but should be applied in a single editing pass to avoid line-number drift.

## 5. Task Classification
- **task_type**: `backend_only`
- **review_intensity**: `standard`
- **backend_tasks**: All 12 implementation steps (SKILL.md edits + capture-diff.sh creation)
- **frontend_tasks**: None
- **Rationale**: 2 files changed, ~110 estimated changed lines, moderate risk from template restructuring. Fits "standard" — more than 3-file/100-line "light" threshold due to complexity, but well under "full" thresholds.

## 6. Risks and Dependencies

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Parameterized template loses fullstack parallel semantics | Medium | High | Keep explicit `--parallel` example with two task blocks |
| `capture-diff.sh` path not found at runtime | Low | High | Use `$HOME/.claude/skills/spec/scripts/` path; `chmod +x` |
| `capture-diff.sh` blocked by tool permissions | Low | High | Step 1 explicitly adds script to `allowed-tools` frontmatter (FR-11) |
| Orchestrator pre-assessment misjudges task triviality | Low | Medium | Pre-assessment is advisory; spec-planner still runs full analysis in Step 3 and can flag if deeper exploration was needed; orchestrator can always err on "not trivial" |
| Light fast-track skips exploration for tasks that actually need it | Low | Medium | Pre-assessment only skips explorer, not planner; planner can request re-exploration if context is insufficient |
| Prose trimming introduces ambiguity | Low | Medium | Reviewer validates against original behavior |

## 7. Non-goals
- Changing agent prompt files, sub-skill files, spec-manager.py, codeagent-wrapper
- Restructuring the 4-phase lifecycle
- Adding new sub-skills or agents
