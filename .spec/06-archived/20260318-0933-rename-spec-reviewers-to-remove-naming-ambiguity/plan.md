---
title: rename spec reviewers to remove naming ambiguity
type: plan
category: 03-features
status: testing
phase: test
created: 2026-03-18
tags: ["spec", "plan"]
use_worktree: false
worktree_dir: 
---




# Plan: Rename spec code review agents to eliminate naming ambiguity

## 1. Overview

### Background
The spec skill has two code review agents with names that do not clearly distinguish review depth:
- `spec-reviewer-lite` — standard-intensity reviewer (Claude Sonnet, BashOutput+git, Priority A+B only)
- `spec-reviewer-deep` — full-intensity reviewer (GPT-5.4/Codex, Glob/Grep/Read only, Priority A+B+C)

The rename clarifies that both agents do code review, but at different depth levels.

### Goals
- Standardize the standard-intensity reviewer on `spec-reviewer-lite` (A+B)
- Standardize the full-intensity reviewer on `spec-reviewer-deep` (A+B+C)
- All references across the codebase are updated consistently
- No functional changes to agent behavior, tooling, or review logic

### Scope
- **Included**: Renaming agent keys in config, renaming reference files, updating all textual references in active source files (SKILL.md, README.md, CLAUDE.md, config.json, agent prompt files)
- **Excluded**: Archived specs under `.spec/06-archived/` (historical records, not active code). No changes to review logic, tool lists, models, or prompt content beyond the name substitution.

## 2. Requirements Analysis

### Functional Requirements
1. **FR-1**: `config.json` standard-intensity reviewer key is `spec-reviewer-lite` with `prompt_file` pointing to `spec-reviewer-lite.md`
2. **FR-2**: `config.json` full-intensity reviewer key is `spec-reviewer-deep` with `prompt_file` pointing to `spec-reviewer-deep.md`
3. **FR-3**: Reference file `skills/spec/references/spec-reviewer-lite.md` has matching `name:` frontmatter
4. **FR-4**: Reference file `skills/spec/references/spec-reviewer-deep.md` has matching `name:` frontmatter
5. **FR-5**: All references in `skills/spec/SKILL.md` updated (lines 13, 14, 235, 236, 324)
6. **FR-6**: All references in `skills/spec/README.md` updated (lines 13, 65, 70, 88, 92)
7. **FR-7**: Cross-reference inside `spec-reviewer-deep.md` line 14 points to `spec-reviewer-lite`

### Non-functional Requirements
- Zero behavioral change to review logic
- Rename is purely cosmetic/organizational

## 3. Design Approach

### Chosen approach: Direct rename with search-and-replace
Rename files, update config keys, and do targeted text substitutions in the 5 affected source files.

### Key design decisions
- **Order of substitution matters**: Replace the longer legacy reviewer identifier first, then the shorter legacy reviewer identifier, to avoid partial matches.
- **Archived specs untouched**: They're historical records and not executed.

## 4. Implementation Steps

### Step 1: Rename reference files
- Rename the standard reviewer prompt file to `skills/spec/references/spec-reviewer-lite.md`
- Rename the deep reviewer prompt file to `skills/spec/references/spec-reviewer-deep.md`

### Step 2: Update frontmatter in renamed files
- `spec-reviewer-lite.md` line 2: update `name:` to `spec-reviewer-lite`
- `spec-reviewer-deep.md` line 2: update `name:` to `spec-reviewer-deep`
- `spec-reviewer-deep.md` line 14: update the parallel reviewer reference to `spec-reviewer-lite`

### Step 3: Update `config.json` agent definitions (4 line edits)

### Step 4: Update `skills/spec/SKILL.md` (5 lines, 7 substitutions)

### Step 5: Update `skills/spec/README.md` (5 lines)

## 5. Task Classification

- **task_type**: `backend_only`
- **review_intensity**: `light`
- ~24 changed lines total, all mechanical text substitution with zero logic changes.

## 6. Risks

| Risk | Mitigation |
|------|------------|
| Partial substitution corrupts a name | Replace longer string first; verify with grep after |
| Missed reference site | Post-change grep to catch stragglers |
| Installed copies become stale | User re-runs install after change |

## 7. Non-goals

- Changing review logic, tools, models, or prompt content
- Updating archived specs under `.spec/06-archived/`
- Adding alias/fallback for old names
