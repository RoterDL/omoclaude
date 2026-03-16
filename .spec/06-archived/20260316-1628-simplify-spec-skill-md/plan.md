---
title: simplify-spec-skill-md
type: plan
category: 03-features
status: testing
phase: test
created: 2026-03-16
tags: ["spec", "plan"]
use_worktree: false
worktree_dir: 
---



# Plan: Simplify SKILL.md

## 1. Overview

### Background
`skills/spec/SKILL.md` has grown to ~693 lines. Much of the bulk comes from duplicated worktree/non-worktree code block variants, repeated warning callouts, and reference tables that duplicate information already in README.md and config.json. The file is the primary instruction set for the spec orchestrator agent -- it must remain precise, but redundancy makes it harder to parse and maintain.

### Goals
- Reduce SKILL.md from ~693 lines by ~40% (target ~415 lines)
- Preserve all behavioral semantics: 4-phase lifecycle, 9 hard constraints, gate control, agent invocation protocol (4-section contract for most agents; 3-section for spec-tester), review/revision loops, worktree support
- Improve readability and maintainability

### Scope
- **In scope**: SKILL.md content restructuring only
- **Out of scope**: Sub-skill files, agent reference files, config.json, spec-manager.py, README files

## 2. Requirements Analysis

### Functional Requirements (MUST preserve)
1. FR-1: 4-phase lifecycle (Intent, Design, Implementation, Wrap-up)
2. FR-2: 9 hard constraints (all semantic content)
3. FR-3: Gate control -- every phase transition requires AskUserQuestion confirmation
4. FR-4: Agent invocation templates -- most agents use a 4-section contract (Original User Request / Context Pack / Current Task / Acceptance Criteria); spec-tester uses a 3-section contract (Context Pack / Current Task / Acceptance Criteria, no "Original User Request")
5. FR-5: Review/revision loop logic (plan-reviewer max 3 iterations, code review max 3 iterations)
6. FR-6: Worktree support -- DO_WORKTREE_DIR prefix convention for Phase 3 agents
7. FR-7: Task-type routing table (backend_only / frontend_only / fullstack)
8. FR-8: Diff capture logic for code review (tracked + untracked files)
9. FR-9: Combined dual-review result handling (max of Claude/Codex BLOCKING counts)

### Non-Functional Requirements
1. NFR-1: Agent must still follow all steps without ambiguity after simplification
2. NFR-2: No behavioral regression -- same agent, same inputs should produce same phase transitions

### Immutable Elements (MUST NOT change)
- Frontmatter (lines 1-5): name, description, allowed-tools
- Agent names: spec-explorer, spec-planner, plan-reviewer, do-develop, do-frontend, do-reviewer, spec-code-reviewer, spec-tester, code-architect
- spec-manager.py command syntax: create, update-body, update-phase, enable-worktree, archive, status, list
- codeagent-wrapper invocation syntax: --agent, --skills, --parallel, ---TASK---/---CONTENT--- delimiters

### Simplification Targets (CAN change)
- Duplicated worktree/non-worktree code blocks (~200 lines of duplication)
- Repeated "Review notice" text (8 occurrences, identical)
- Repeated IMPORTANT callouts that restate Hard Constraints
- "Common Violations" section (restates constraints #6, #7, #8)
- Informational tables: Agents Used, Sub-skills, State Management
- Lifecycle ASCII diagram (can be compressed)

## 3. Design Approach

### Strategy A: Worktree Note + Single Template (RECOMMENDED)
Add a single worktree note at the top of Phase 3, before any templates:

> **Worktree mode:** If worktree mode is enabled, prepend `DO_WORKTREE_DIR=<worktree_dir>` to all Phase 3 `codeagent-wrapper` invocations below (`do-develop`, `do-frontend`, `do-reviewer`, `spec-code-reviewer`, `spec-tester`). The orchestrator adds this prefix at call time.

Then show only ONE template per agent call, written in its non-worktree form (no prefix). The orchestrator prepends `DO_WORKTREE_DIR=<worktree_dir>` at call time when worktree mode is active. This eliminates ~200 lines of duplication without introducing any symbolic substitution — the templates remain directly executable Bash.

**Important**: This worktree deduplication applies to `codeagent-wrapper` invocation templates only. The diff capture script (Step 4, lines 437-462) already handles both worktree and non-worktree cases in a single conditional block (`if [ -n "$DO_WORKTREE_DIR" ]`) and is NOT duplicated — it is kept as-is.

**Why not $W shorthand**: A symbolic prefix like `$W` would turn directly executable Bash templates into convention-dependent text that requires interpretation. Showing the plain template + a one-time "prepend if worktree" note is both simpler and directly executable.

### Strategy B: Reusable Agent Call Template Section (REJECTED)
**Rejection rationale**: The 4-section contract is only ~8 lines per occurrence, variable parts differ per call. Indirection without line savings.

### Decision: Strategy A

### Review Notice Handling
The "Review notice" text appears 8 times across Phase 3 implementation templates (backend-only, frontend-only, fullstack backend task, fullstack frontend task — each in the now-removed worktree/non-worktree duplicates). After collapsing worktree duplicates, 4 occurrences remain. These MUST be kept literally inline in each template because agents receive heredoc content literally — extracting to a "constant" would change the agent input contract. The ~4 lines of duplication across 4 templates is acceptable for correctness.

### Additional Consolidations
1. Merge "Common Violations" into Hard Constraints as sub-bullets
2. Remove IMPORTANT callouts in Phase 2 that restate Hard Constraints #6-#8
3. Collapse Agents Used / Sub-skills / State Management into compact reference (retain brief mention of `spec-debug` and `spec-end` sub-skills for discoverability)
4. Compress lifecycle diagram

## 4. Implementation Steps

All changes to single file: skills/spec/SKILL.md

### Step 1: Add worktree note to Phase 3 top
- Lines: 231-248 (Phase 3 header area)
- Add a single worktree-mode note before Step 1, explaining that the orchestrator prepends `DO_WORKTREE_DIR=<worktree_dir>` to all Phase 3 `codeagent-wrapper` invocations when worktree is active
- This note applies to `codeagent-wrapper` calls only — it does NOT apply to the diff capture script (which already has its own conditional block)
- Keep the Worktree Mode section (lines 32-51) for enable-worktree instructions, but remove redundant sentences about which agents need the prefix (now covered by the Phase 3 note)
- Target Worktree Mode section: ~12 lines (from ~20). Savings: ~8 lines

### Step 2: Merge Common Violations into Hard Constraints
- Lines: 25-31 merged into 13-24
- Add violation examples as sub-bullets under constraints #6, #7, #8. Delete Common Violations H3.
- Savings: ~3 lines

### Step 3: Remove redundant IMPORTANT callouts in Phase 2
- Lines: 112-113, 125-126, 147-148, 190-191, 193-194
- Delete NO SHORTCUTS banner and 4 IMPORTANT blocks. Keep one reminder: "All steps are mandatory per Hard Constraints #6-#9."
- Savings: ~15 lines

### Step 4: Collapse worktree-duplicated code blocks (LARGEST SAVINGS)
- Phase 3 Step 2 (264-427), Step 4 (437-542), Step 5 (569-597)
- **Diff capture conditional block (lines 437-462) is kept as-is.** This block uses `if [ -n "$DO_WORKTREE_DIR" ]` to branch between worktree (`git -C "$DO_WORKTREE_DIR"`) and non-worktree (`git`) commands. It is a single conditional script, NOT a duplicated template, and must be preserved unchanged.
- **Only the `codeagent-wrapper --parallel` call after the diff capture (lines 464-542) is deduplicated** — remove the worktree variant and keep the non-worktree form. The Phase 3 worktree note (Step 1 above) tells the orchestrator to prepend `DO_WORKTREE_DIR=<worktree_dir>` at call time.
- For implementation templates (Step 2) and test template (Step 5), keep only ONE template per agent call in non-worktree form (directly executable Bash). The Phase 3 worktree note covers the prefix.
- Keep all 4 "Review notice" texts literally inline in their respective templates (backend-only, frontend-only, fullstack-backend, fullstack-frontend) — do NOT extract or reference
  - Backend-only: 35->18 lines
  - Frontend-only: 36->18 lines
  - Fullstack: 90->45 lines
  - Code review (codeagent-wrapper calls only): 106->70 lines (diff capture block ~26 lines preserved, dual-review call deduplicated)
  - Tests: 29->14 lines
- Savings: ~125 lines

### Step 5: Compress lifecycle diagram
- Lines: 53-86. Replace with compact 4-line version.
- Savings: ~27 lines

### Step 6: Consolidate reference tables
- Lines: 650-693. Remove Agents Used table, compress State Management section.
- Sub-skills table: remove full table, but retain a one-line mention of `spec-debug` (issue diagnosis) and `spec-end` (archival/experience capture) so users know these sub-skills exist even though they aren't invoked in the main lifecycle flow.
- Savings: ~30 lines

### Step 7: Compress Spec Directory Structure
- Lines: 636-648. Remove blank-line padding.
- Savings: ~3 lines

### Build Sequence
1. Step 1 (worktree note at Phase 3 top)
2. Steps 2, 3 (independent consolidations)
3. Step 4 (worktree collapse, depends on Step 1)
4. Steps 5, 6, 7 (reference cleanup)

## 5. Task Classification
- task_type: backend_only

## 6. Risks and Dependencies

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Agent omits DO_WORKTREE_DIR in worktree mode | Low | High | Phase 3 note is explicit; Worktree Mode section has concrete example; Hard Constraint #5 reinforces |
| Removing IMPORTANT callouts causes constraint violations | Low | Medium | Hard Constraints preserved at top; one-liner reminder at Phase 2 |
| Removing Agents Used table causes wrong agent selection | Very Low | Low | Routing table in Phase 3 Step 1 already specifies agents per task_type |
| Over-compression loses review loop nuance | Low | High | Do NOT simplify review loop logic; only collapse worktree duplication |
| Review notice extracted instead of kept inline | N/A (prevented) | High | Plan explicitly requires literal inline text in all 4 templates |
| Diff capture conditional block altered or split | N/A (prevented) | High | Plan explicitly requires the `if [ -n "$DO_WORKTREE_DIR" ]` block to be kept as-is |

## 7. Non-goals
- Changing sub-skill files, agent reference files, config.json, spec-manager.py, codeagent-wrapper, README files
- Altering the 4-phase lifecycle semantics
- Adding new features or phases

## 8. Estimated Line Counts

| Section | Current | Target | Savings |
|---------|---------|--------|---------|
| Frontmatter + intro | 12 | 12 | 0 |
| Hard Constraints | 22 | 19 | 3 |
| Worktree Mode | 20 | 12 | 8 |
| Lifecycle Diagram | 33 | 6 | 27 |
| Initialization | 8 | 8 | 0 |
| Phase 1 | 12 | 12 | 0 |
| Phase 2 | 118 | 103 | 15 |
| Phase 3 | 376 | 215 | 161 |
| Phase 4 | 24 | 24 | 0 |
| Spec Directory Structure | 13 | 10 | 3 |
| Reference tables | 44 | 14 | 30 |
| **TOTAL** | **~693** | **~435** | **~258** |

> **Note**: The estimated total of ~435 represents a ~37% reduction. The priority is preserving correctness (literal inline review notices, complete diff capture conditional block kept as-is) over hitting an exact line count. The diff capture block contributes ~26 lines that cannot be compressed.

## 9. Verification Checklist

After implementing all steps, the implementer MUST confirm every item below is present in the simplified SKILL.md. Check each box only after verifying against the file.

### Phase 1: Intent Confirmation
- [ ] Restate-confirm-clarify flow with AskUserQuestion
- [ ] Skip conditions listed (detailed spec, single-file fix, explicit "just do it")

### Phase 2: Design & Planning
- [ ] Step 1: exp-search for related experience
- [ ] Step 2: `codeagent-wrapper --agent spec-explorer` template with 4-section contract
- [ ] Step 3: `codeagent-wrapper --agent spec-planner` template with 4-section contract
- [ ] Step 4: `spec-manager.py update-body` for writing plan.md (NOT Write/cp)
- [ ] Step 5: `codeagent-wrapper --agent plan-reviewer` template with 4-section contract
- [ ] Plan review loop: BLOCKING>0 → re-invoke spec-planner (max 3 iterations)
- [ ] Plan review loop: iteration>=3 → save review, AskUserQuestion for guidance
- [ ] Save plan-review.md artifact
- [ ] Step 6: AskUserQuestion gate before Phase 3

### Phase 3: Implementation
- [ ] Step 0: Worktree decision via AskUserQuestion + `enable-worktree` command
- [ ] Worktree note: "prepend DO_WORKTREE_DIR=<worktree_dir> to all Phase 3 codeagent-wrapper calls"
- [ ] Step 1: Task-type routing table (backend_only / frontend_only / fullstack)
- [ ] Step 2 backend-only template: `do-develop` with 4-section contract + literal review notice
- [ ] Step 2 frontend-only template: `do-frontend --skills taste-core,taste-output` with 4-section contract + literal review notice
- [ ] Step 2 fullstack template: `--parallel` with both tasks, each with 4-section contract + literal review notice
- [ ] Optional taste-creative / taste-redesign add-on mentioned
- [ ] Step 3: summary.md generation
- [ ] Step 4: Diff capture conditional block preserved as-is (uses `if [ -n "$DO_WORKTREE_DIR" ]` to branch between worktree/non-worktree git commands)
- [ ] Step 4: Diff capture covers tracked via `git diff HEAD` + untracked via `git status --porcelain`
- [ ] Step 4: Dual review via `--parallel` with `do-reviewer` + `spec-code-reviewer` templates
- [ ] Combined assessment: `BLOCKING = max(claude, codex)`, `MINOR = max(claude, codex)`
- [ ] Code review loop: BLOCKING>0 → fix via do-develop/do-frontend, re-review (max 3 iterations)
- [ ] Code review loop: iteration>=3 → save report, AskUserQuestion for guidance
- [ ] Save review-report.md artifact with Claude/Codex/Combined sections
- [ ] Step 5: `codeagent-wrapper --agent spec-tester` template with 3-section contract (Context Pack / Current Task / Acceptance Criteria — no "Original User Request")
- [ ] Step 6: Test result handling (pass → Phase 4, fail → fix + re-test)
- [ ] `update-phase test` command
- [ ] AskUserQuestion gate after review & tests

### Phase 4: Wrap-up
- [ ] Step 1: Suggest `/exp-reflect`
- [ ] Step 2: AskUserQuestion for archive confirmation
- [ ] Step 3: `spec-manager.py archive` command
- [ ] `update-phase end` command

### Hard Constraints & Structure
- [ ] All 9 hard constraints present with full semantic content
- [ ] Common Violations content merged into constraints (not lost)
- [ ] Frontmatter unchanged (lines 1-5: name, description, allowed-tools)
- [ ] Spec Directory Structure with all artifact files listed
- [ ] Sub-skills `spec-debug` and `spec-end` mentioned
- [ ] `spec-manager.py` commands: create, update-body, update-phase, enable-worktree, archive, status, list
- [ ] `code-architect` agent name preserved in immutable elements

### Line Count
- [ ] Final line count is within target range (~415-435 lines, ~37-40% reduction from ~693)

## 10. File Touch List

| File | Action |
|------|--------|
| skills/spec/SKILL.md | Edit (major restructure, 7 steps) |
