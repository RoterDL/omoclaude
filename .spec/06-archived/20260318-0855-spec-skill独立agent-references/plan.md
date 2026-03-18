---
title: spec skill独立agent references
type: plan
category: 03-features
status: testing
phase: test
created: 2026-03-18
tags: ["spec", "plan"]
use_worktree: false
worktree_dir: 
---




# Plan: Make spec skill's agents fully self-contained

## 1. Overview

### Background
The `/spec` skill currently depends on the `/do` module for three agent reference files: `do-develop`, `do-frontend`, and `do-reviewer`. This creates a coupling where changes to `/do` agents can unintentionally break `/spec` behavior, and installing `/spec` without `/do` is impossible. Experience exp-005 specifically warns about source vs installed copy drift — the same risk applies here when two modules share agent definitions.

### Goals
- Create three new spec-owned agent reference files: `spec-develop.md`, `spec-frontend.md`, `spec-reviewer.md` in `skills/spec/references/`
- Update all `/spec` files to reference the new agents instead of `do-develop`/`do-frontend`/`do-reviewer`
- Register the new agents in `config.json` under the `spec` module
- Remove the `/do` module dependency from `/spec`

### Scope
- **Included**: Creating new agent files, updating all references in spec SKILL.md, spec README.md, spec-debug SKILL.md, spec-code-reviewer.md, config.json
- **Excluded**: Modifying `/do` module agents, changing agent behavior/capabilities (clone-and-adapt only), CLAUDE.md changes

## 2. Requirements Analysis

### Functional Requirements
1. **FR-1**: `spec-develop.md` exists at `skills/spec/references/` with content adapted from `do-develop.md`
2. **FR-2**: `spec-frontend.md` exists at `skills/spec/references/` with content adapted from `do-frontend.md`
3. **FR-3**: `spec-reviewer.md` exists at `skills/spec/references/` with content adapted from `do-reviewer.md`
4. **FR-4**: `skills/spec/SKILL.md` references `spec-develop`, `spec-frontend`, `spec-reviewer` everywhere
5. **FR-5**: `skills/spec/README.md` references the new agents and removes "depends on do module" language
6. **FR-6**: `skills/spec/sub-skills/spec-debug/SKILL.md` references `spec-develop` and `spec-frontend`
7. **FR-7**: `skills/spec/references/spec-code-reviewer.md` references `spec-reviewer` instead of `do-reviewer`
8. **FR-8**: `config.json` spec module has three new agent entries
9. **FR-9**: `config.json` spec module `dependencies` does not require `do`

### Non-functional Requirements
- Agent content must follow existing naming conventions (`spec-<role>.md`)
- New agents must be functionally equivalent to their `/do` counterparts
- All `/spec` references to `/do` agents must be eliminated (grep-verifiable)

## 3. Design Approach

### Chosen Approach: Clone-and-adapt
Clone each `/do` agent file into `skills/spec/references/`, then adapt orchestrator references from `/do` to `/spec`.

### Alternatives Considered
1. **Symlinks/includes**: Rejected — doesn't solve the coupling problem
2. **Shared common base with overrides**: Rejected — over-engineering for 3 small files
3. **Keep dependency, just document it**: Rejected — doesn't achieve self-containment

## 4. Implementation Steps

### Step 1-3: Create new agent files (parallel)
- `spec-develop.md`: Clone from `do-develop.md`, adapt to `/spec` orchestrator
- `spec-frontend.md`: Clone from `do-frontend.md`, adapt to `/spec` orchestrator
- `spec-reviewer.md`: Clone from `do-reviewer.md`, adapt to `/spec` orchestrator

### Step 4: Update `skills/spec/SKILL.md`
- 9+ substitution sites: lines 3,13,14,25,169-172,197,226,235,324

### Step 5: Update `skills/spec/references/spec-code-reviewer.md`
- Line 14: `do-reviewer` → `spec-reviewer`

### Step 6: Update `skills/spec/sub-skills/spec-debug/SKILL.md`
- Lines 3,22,90,108: `do-develop`/`do-frontend` → `spec-develop`/`spec-frontend`

### Step 7: Update `skills/spec/README.md`
- Lines 44-45,54,85-86,111: agent references and dependency info

### Step 8: Update `config.json`
- Add 3 new agent entries under spec module (mirror do module's backend/model settings)

## 5. Task Classification

- **task_type**: `backend_only`
- **review_intensity**: `standard`
- **Rationale**: 8 files (3 new + 5 edited), ~400 changed lines, text substitutions and file cloning, no architectural risk

## 6. Risks and Dependencies

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Missed reference to do-* agents | Medium | Medium | Post-implementation grep across `skills/spec/` |
| Config.json syntax error | Low | High | Validate JSON after edit |
| Agent behavior divergence | Low | Low | Exact clone with only name changes |

## 7. Non-goals
- Not changing agent behavior (functional clones only)
- Not removing /do agents (they remain for /do module)
- Not updating root READMEs or CLAUDE.md
- Not optimizing cloned agent content
