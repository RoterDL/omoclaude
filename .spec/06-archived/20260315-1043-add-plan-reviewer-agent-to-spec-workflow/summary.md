# Implementation Summary: Add Plan-Reviewer Agent to Spec Workflow

## Changes Made

### New File
- `skills/spec/references/plan-reviewer.md` — Agent prompt with 7-area review checklist (completeness, spec alignment, task decomposition, file structure, file size, testability, risk assessment). Uses BLOCKING/MINOR output format matching do-reviewer pattern.

### Modified Files
- `config.json` (L275-280) — Added `plan-reviewer` agent to `spec.agents`: `backend=codex`, `model=gpt-5.4`, `reasoning=xhigh`
- `skills/spec/SKILL.md` — Multiple sections updated:
  - Lifecycle diagram (L66-67): Added plan-reviewer and auto-revision loop
  - Hard Constraint #4 (L18): Added plan-reviewer to agent list
  - Hard Constraint #8 (L22): Added plan-reviewer to mandatory pipeline
  - Hard Constraint #9 (L23): New — plan review is mandatory, max 3 auto-revision iterations
  - Phase 2 header (L113): Updated NO SHORTCUTS note to include plan-reviewer
  - Phase 2 Step 5 (L192-219): New — plan review loop with codeagent-wrapper template, BLOCKING handling, max 3 iterations, plan-review.md output
  - Step 5->6 renumber (L221): User confirmation gate
  - Spec Directory Structure (L538): Added `plan-review.md`
  - Agents Used table (L552): Added plan-reviewer row
- `CLAUDE.md` (L86, L116) — Updated agent prompt list and spec lifecycle description

## Design Decisions
- Codex GPT 5.4 with xhigh reasoning for genuine perspective diversity from spec-planner (Opus 4.6)
- Max 3 revision loops to prevent infinite cycles; escalates to user after 3 rounds
- Review saved as `plan-review.md` for audit trail
- Stateless reviewer — no revision history tracking needed
