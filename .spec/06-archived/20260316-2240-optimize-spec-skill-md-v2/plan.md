---
title: optimize spec skill md v2
type: plan
category: 03-features
status: testing
phase: test
created: 2026-03-16
tags: ["spec", "plan"]
use_worktree: false
worktree_dir: 
---




# Plan: Optimize spec/SKILL.md v2 (343 → ≤320 lines) + write-artifact

## 1. Overview

### Background
The spec SKILL.md was previously optimized from 476 to 343 lines (v1). Orchestrator analysis identified 11 additional items across four categories: redundancy (-25-30 lines), logic fixes (3 functional defects), efficiency improvements (2 items), and minor issues (2 items).

### Goals
- Reduce SKILL.md from 343 lines to ≤320 lines (net ~-29 lines after additions)
- Fix 3 functional defects where instructions reference unavailable tools
- Add express-path for trivial/light tasks to reduce unnecessary gates
- Unify skip conditions and pre-assessment into single triage
- Add `write-artifact` subcommand to `spec-manager.py` to handle ALL spec artifact writes

### Scope
- **In scope**: All 11 items applied to `skills/spec/SKILL.md`; `write-artifact` added to `skills/spec/scripts/spec-manager.py`
- **Out of scope**: Agent prompt files, sub-skill files, README sync

## 2. Requirements Analysis

### Functional Requirements
1. **FR-1**: Standalone Worktree Mode section (L18-29) removed; Phase 3 Step 0 is sole worktree reference.
2. **FR-2**: Phase 3 Step 5 code review templates merged into single parameterized template.
3. **FR-3**: Hard Constraints #6 and #7 each compressed to 2 sentences.
4. **FR-4**: Phase 2 Step 3 Review/Self-review notices merged into 2 lines.
5. **FR-5**: `spec-manager.py` gains `write-artifact` subcommand for ALL spec artifact writes.
6. **FR-6**: Phase 4 Step 1 `/exp-write` replaced with `write-artifact` + orchestrator extraction.
7. **FR-7**: Phase 2 Step 1 exp-search uses explicit Read instructions; dead comment removed.
8. **FR-8**: Express-path for trivial tasks with specific step skip/keep table.
9. **FR-9**: Phase 1 skip + Phase 2 pre-assessment unified into Complexity Triage (trivial/light/standard/full).
10. **FR-10**: Phase 3 Step 6 `update-phase test` gets inline comment.
11. **FR-11**: Additional References cleaned of unused mentions.

### Non-functional Requirements
- NF-1: Net SKILL.md line count ≤ 320 (target ~314).
- NF-2: No behavioral regression for standard/full intensity tasks.
- NF-3: All existing `spec-manager.py` subcommands unchanged.

### Constraints
- `write-artifact`: minimal, writes to current spec dir only.
- Express-path shortcuts within phases, not around them.
- Per exp-001: `complexity_level` (orchestrator, pre-planning) and `review_intensity` (planner, post-planning) are separate.
- Per exp-002: `allowed-tools` glob `spec-manager.py:*` already covers `write-artifact`.

## 3. Design Approach

### Chosen Approach
Incremental in-place edits to SKILL.md + targeted `write-artifact` addition to `spec-manager.py`.

### Alternatives Rejected
1. Full rewrite of SKILL.md: high regression risk.
2. Express-path as sub-skill: unnecessary indirection.
3. Use Write tool directly: too permissive for orchestrator.

### write-artifact Interface Contract

```
Usage: spec-manager.py write-artifact <filename> [--file <path>]
       echo "content" | spec-manager.py write-artifact <filename>
```

**Parameters:**
- `filename` (positional, required): Target filename within current spec dir (e.g. `summary.md`).
- `--file <path>` (optional): Read content from file instead of stdin.

**Validation:** filename must not contain `/` or `..`; must end with `.md`; content must be non-empty. Active spec must exist.

**Behavior:** Overwrites silently if file exists. No frontmatter injection. Success: prints `Wrote: <path>`, exit 0. Failure: stderr error, exit 1.

**Unified artifact writes:** Replaces all spec artifact saves: `plan-review.md`, `summary.md`, `test-report.md`, `review-report.md`, experience reflection output.

### Express-path Decision Table

| Phase | Step | standard/full | light | trivial |
|-------|------|--------------|-------|---------|
| 1 | Intent Confirmation | Full flow | Full flow | **SKIP** |
| 2.1 | exp-search | Run | Run | **SKIP** |
| 2.2 | spec-explorer | Run | **SKIP** (orchestrator Read/Grep) | **SKIP** |
| 2.3 | spec-planner | Run (codeagent-wrapper) | Run (codeagent-wrapper) | **SKIP** (orchestrator writes minimal plan) |
| 2.4 | Write plan.md | Run | Run | Run (via update-body) |
| 2.5 | plan-reviewer | intensity-gated | **SKIP** | **SKIP** |
| 2.6 | User gate | Run | Run | **MERGE** with Phase 3 Step 6 |
| 3.0 | Worktree decision | Ask user | Ask user | **SKIP** (no worktree) |
| 3.1-2 | Implementation | Run | Run | Run (codeagent-wrapper) |
| 3.3 | summary.md | Run | Run | Run |
| 3.4 | spec-tester | Run | Run | **SKIP** |
| 3.5 | Code review | intensity-gated | **SKIP** | **SKIP** |
| 3.6 | User gate | Run | Run | Run (merged from Phase 2) |
| 4.1 | exp-reflect | intensity-gated | default skip | **SKIP** |
| 4.2-4 | Archive flow | Run | Run | Run |

**Key:** trivial HC#7 exception: orchestrator writes minimal plan directly. Implementation still delegated to codeagent-wrapper.

## 4. Implementation Steps

### Step 1: Add `write-artifact` to spec-manager.py (+30 lines)
**File**: `skills/spec/scripts/spec-manager.py`
1. Add `write_artifact(filename: str, content_file: str | None) -> bool` after `update_body()` (~L514): validate filename (no `/`, `..`; must `.md`), read from file/stdin, reject empty, write to spec dir, print path.
2. Add subparser after archive: `write-artifact <filename> [--file]`.
3. Add elif in dispatch: call `write_artifact()`.

### Step 2: Delete Worktree Mode section (-12 lines)
**File**: `skills/spec/SKILL.md` L18-29. Delete all 12 lines.

### Step 3: Compress HC#6 and HC#7 (-4 lines)
**File**: `skills/spec/SKILL.md` L15-16. Remove "Common failure modes to avoid: ..." clauses from both.

### Step 4: Unify triage (net -3 lines)
**File**: `skills/spec/SKILL.md`. Remove L52 skip conditions + L55 pre-assessment (~11 lines). Add 8-line Complexity Triage block between Phase 1 and Phase 2.

### Step 5: Clean exp-search (-2 lines)
**File**: `skills/spec/SKILL.md` L56-60. Replace bash comment with 2-line Read instructions.

### Step 6: Merge review notices (-2 lines)
**File**: `skills/spec/SKILL.md` L100-103. Merge 4 lines into 2.

### Step 7: Add express-path conditionals (+5 lines)
**File**: `skills/spec/SKILL.md`. Add 1-line conditional at Phase 2/3/4 headers + 2-line note after triage block.

### Step 8: Parameterize code review templates (-12 lines)
**File**: `skills/spec/SKILL.md` L237-279. Replace 2 templates with routing + 1 parameterized template.

### Step 9: Replace /exp-write + unify artifact writes (-2 lines)
**File**: `skills/spec/SKILL.md`. Replace exp-write calls with write-artifact. Update all artifact save sites (plan-review.md, summary.md, test-report.md, review-report.md) to use write-artifact.

### Step 10: Add inline comment to update-phase test (+0)
**File**: `skills/spec/SKILL.md` L283. Append comment.

### Step 11: Clean Additional References (-2 lines)
**File**: `skills/spec/SKILL.md` L340-343. Remove unused code-architect/spec-debug.

### Step 12: Verify allowed-tools (+0)
**File**: `skills/spec/SKILL.md` L4. Confirm glob `spec-manager.py:*` covers write-artifact.

### Line Count Reconciliation
| Step | Delta | | Step | Delta |
|------|-------|-|------|-------|
| 2 | -12 | | 7 | +5 |
| 3 | -4 | | 9 | -2 |
| 4 | -3 | | 10 | +0 |
| 5 | -2 | | 11 | -2 |
| 6 | -2 | | 12 | +0 |
| 8 | -12 | | **Total** | **-34+5 = -29** |

**Projected: 343 - 29 = ~314 lines** (≤320 target satisfied)

### Build Sequence
Step 1 first (spec-manager.py, independent). Then SKILL.md bottom-up: 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 12.

## 5. Task Classification
- **task_type**: `backend_only`
- **review_intensity**: `standard`
- Rationale: 2 files, ~60 lines net delta, many interrelated edits with moderate regression risk.

## 6. Risks and Dependencies

| Risk | Impact | Mitigation |
|------|--------|------------|
| Express-path misjudgment | Medium | review_intensity can upgrade; user has final gate |
| Parameterized template errors | Low | Single source of truth |
| write-artifact path traversal | Medium | Filename validation: reject `/`, `..`, non-`.md` |
| Worktree section discoverability | Low | Phase 3 Step 0 canonical; HC#5 references it |
| Triage/intensity conflation | Medium | Per exp-001: separate mechanisms, separate timing |
| spec-manager.py regression | Medium | Manual verification (see below) |

### NF-3 Manual Verification
```bash
python spec-manager.py --help                                    # write-artifact in list
python spec-manager.py status                                    # no crash
python spec-manager.py list                                      # no crash
echo "test" | python spec-manager.py write-artifact test.md      # success
echo "bad" | python spec-manager.py write-artifact ../escape.md  # error, exit 1
echo "bad" | python spec-manager.py write-artifact sub/dir.md    # error, exit 1
echo "" | python spec-manager.py write-artifact empty.md         # error, exit 1
```

## 7. Non-goals
- Restructuring the 4-phase model
- Changes to agent prompts, sub-skills, README, capture-diff.sh
- Adding automated tests to spec-manager.py
