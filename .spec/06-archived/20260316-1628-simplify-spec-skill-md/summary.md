# Implementation Summary: Simplify SKILL.md

## Scope
Single file: `skills/spec/SKILL.md` — reduced from 693 to 416 lines (40% reduction).

## Changes Implemented (7 Steps)

### Step 1: Worktree note at Phase 3 top
- Added unified worktree mode note at line 163 replacing per-template duplication
- Trimmed Worktree Mode section from ~20 to ~14 lines

### Step 2: Common Violations merged into Hard Constraints
- Violation examples now appear as inline text within constraints #6, #7, #8 (lines 15-17)
- Deleted separate "Common Violations" subsection

### Step 3: Removed redundant Phase 2 callouts
- Deleted "NO SHORTCUTS" banner and 4 IMPORTANT blocks
- Replaced with single reminder: "All steps below are mandatory per Hard Constraints #6-#9." (line 57)

### Step 4: Collapsed worktree-duplicated code blocks (largest savings)
- All Phase 3 templates now show only non-worktree form (directly executable Bash)
- Diff capture conditional block (`if [ -n "$DO_WORKTREE_DIR" ]`) preserved as-is (lines 260-286)
- 4 "Review notice" texts kept literally inline (lines 186, 204, 227, 248)

### Step 5: Compressed lifecycle diagram
- Replaced ~33-line ASCII diagram with 4-line compact text version (lines 34-40)

### Step 6: Consolidated reference tables
- Removed Agents Used table (9-row table)
- Removed Sub-skills table (5-row table)
- Compressed into "Additional References" section (lines 401-416)
- spec-debug and spec-end mentioned with brief descriptions (lines 404-405)
- code-architect mentioned (line 403)
- All spec-manager.py commands preserved (lines 407-416)

### Step 7: Compressed Spec Directory Structure
- Removed padding, kept all artifact file listings (lines 389-400)

## Key Files
- `skills/spec/SKILL.md:1-416` — simplified file

## Preserved Behavior
- 4-phase lifecycle with all gates
- 9 Hard Constraints (semantics preserved, violations merged in)
- All agent invocation templates with correct section contracts
- spec-tester 3-section contract (no "Original User Request")
- Plan review loop (max 3 iterations)
- Code review loop (max 3 iterations)
- Diff capture conditional block unchanged
- Worktree support via Phase 3 note
