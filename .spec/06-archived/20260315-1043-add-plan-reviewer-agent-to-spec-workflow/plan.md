---
title: add-plan-reviewer-agent-to-spec-workflow
type: plan
category: 03-features
status: testing
phase: test
created: 2026-03-15
tags: ["spec", "plan"]
use_worktree: false
worktree_dir: 
---



# Add Plan-Reviewer Agent to Spec Workflow

## Overview

### Background
The spec skill's Phase 2 currently goes: spec-explorer -> spec-planner -> write plan.md -> user gate. There is no automated quality check on the plan before the user sees it. Phase 3 already has an automated review loop (do-reviewer checks code, BLOCKING issues trigger auto-fix), but Phase 2 lacks the equivalent for design documents. This means spec-planner output with incomplete tasks, missing steps, scope creep, or oversized files goes straight to the user, wasting a gate cycle if the user catches issues and requests revision.

### Goals
- Insert a plan-reviewer agent (Codex GPT 5.4) between plan.md generation and the user confirmation gate in Phase 2
- Implement a BLOCKING auto-revision loop: if plan-reviewer finds BLOCKING issues, auto-feed feedback to spec-planner, re-generate plan.md, re-review -- loop until BLOCKING=0
- Use a review checklist derived from the superpowers plan-document-reviewer-prompt.md (completeness, spec alignment, task decomposition, file structure, file size, task syntax, chunk size)
- Produce the same output format as do-reviewer: `Summary: BLOCKING=<n>, MINOR=<n> -- <sentence>`

### Scope
**In scope:**
- New agent prompt file: `skills/spec/references/plan-reviewer.md`
- Config entry in `config.json` under `spec.agents`
- Phase 2 flow update in `SKILL.md` (new Step 5 between current Step 4 and Step 5)
- Updates to SKILL.md lifecycle diagram, Hard Constraints, and Agents Used table
- Updates to CLAUDE.md agent references

**Out of scope:**
- Changes to Phase 3 do-reviewer workflow
- Changes to spec-planner prompt (it already generates the right sections)
- New scripts or Python tooling (uses existing codeagent-wrapper)
- Changes to spec-manager.py

## Requirements Analysis

### Functional Requirements
1. **FR-001**: plan-reviewer agent receives plan.md content + original user request and produces a structured review with BLOCKING/MINOR classifications
2. **FR-002**: Review covers 7 checklist areas: completeness, spec alignment, task decomposition, file structure, file size, task syntax, chunk size
3. **FR-003**: Output ends with `Summary: BLOCKING=<n>, MINOR=<n> -- <sentence>` (same format as do-reviewer)
4. **FR-004**: When BLOCKING>0, the spec orchestrator auto-invokes spec-planner with the reviewer feedback appended, then re-reviews -- no user intervention required
5. **FR-005**: When BLOCKING=0, the flow proceeds to the user confirmation gate (formerly Step 5, now Step 6)
6. **FR-006**: MINOR issues are reported but do not block progression
7. **FR-007**: A maximum loop count (3 iterations) prevents infinite revision cycles; if still BLOCKING after 3 rounds, escalate to user

### Non-functional Requirements
- **Latency**: Each review round adds one codeagent-wrapper call (~30-60s). Acceptable given Phase 2 is not latency-critical.
- **Cost**: Uses Codex GPT 5.4 with `xhigh` reasoning. Bounded by max loop count.
- **Consistency**: Output format must exactly match do-reviewer pattern for orchestrator parsing.

### Constraints and Assumptions
- codeagent-wrapper already supports `--agent plan-reviewer` once config.json is updated and installed
- plan-reviewer does not need worktree access (Phase 2 is read-only)
- The spec orchestrator (SKILL.md) handles the loop logic -- plan-reviewer itself is stateless

## Design Approach

### Chosen Approach
Mirror the Phase 3 do-reviewer pattern for Phase 2:

```
Step 4: Write plan.md (existing)
Step 5: Plan review loop (NEW)
  5a. Invoke plan-reviewer with plan.md + user request
  5b. Parse BLOCKING count from summary line
  5c. If BLOCKING>0 and iteration<3:
      - Re-invoke spec-planner with original context + reviewer feedback
      - Re-write plan.md via update-body
      - Go to 5a
  5d. If BLOCKING>0 and iteration>=3:
      - Present review to user, ask for guidance
  5e. If BLOCKING=0:
      - Save review as plan-review.md in spec directory
      - Proceed to Step 6 (user gate)
Step 6: User confirmation gate (renumbered from Step 5)
```

### Alternatives Considered
1. **User-only review (status quo)**: Rejected -- wastes user gate cycles on issues an LLM can catch
2. **Non-blocking advisory review**: Rejected -- if issues are fixable, auto-fixing saves time
3. **Same model (Opus 4.6) as reviewer**: Rejected -- different model provides genuine perspective diversity

### Key Design Decisions
- **Codex GPT 5.4 backend with xhigh reasoning**: Matches do-develop pattern
- **Max 3 loop iterations**: Prevents runaway loops
- **Stateless reviewer**: Sees only current plan.md + original request + checklist
- **Save review output as plan-review.md**: Audit trail in spec directory

## Implementation Steps

| # | File | Change | Depends On |
|---|------|--------|------------|
| 1 | `skills/spec/references/plan-reviewer.md` | **CREATE**: Agent prompt with 7-area review checklist, input/output format, BLOCKING/MINOR criteria | - |
| 2 | `config.json` | **EDIT** (L264-281): Add `plan-reviewer` to `spec.agents` with codex/gpt-5.4/xhigh | Step 1 |
| 3 | `skills/spec/SKILL.md` Phase 2 section | **EDIT** (L172-194): Insert Step 5 (plan review loop) between Step 4 and old Step 5. Include codeagent-wrapper template, BLOCKING parse, revision loop (max 3), plan-review.md save | Step 1 |
| 4 | `skills/spec/SKILL.md` Phase 2 header | **EDIT** (L110): Update NO SHORTCUTS note to include plan-reviewer in mandatory pipeline | Step 3 |
| 5 | `skills/spec/SKILL.md` lifecycle diagram | **EDIT** (L60-66): Add plan-reviewer line and auto-revision loop | Step 3 |
| 6 | `skills/spec/SKILL.md` Hard Constraints | **EDIT** (L13-22): Add constraint about plan-reviewer being mandatory | Step 3 |
| 7 | `skills/spec/SKILL.md` Agents Used table | **EDIT** (L514-522): Add plan-reviewer row | Step 3 |
| 8 | `CLAUDE.md` agent references | **EDIT**: Update spec agent list and lifecycle description | Step 3 |

## Task Classification
- **task_type**: backend_only
- **backend_tasks**: All 8 steps (agent prompt, config, workflow docs)
- **frontend_tasks**: N/A

## Risks and Dependencies

| Risk | Impact | Mitigation |
|------|--------|------------|
| Infinite revision loop | Medium | Hard cap at 3 iterations with user escalation |
| plan-reviewer too strict | Medium | Careful BLOCKING criteria -- only genuinely broken plans |
| Codex API latency spike | Low | codeagent-wrapper handles retries; bounded by max iterations |
| Prompt format mismatch | Medium | plan-reviewer explicitly references plan-template.md sections |

## Non-goals
- Modifying spec-planner prompt or plan-template.md
- Adding plan-reviewer to Phase 3
- Building revision history / diff tracking
- Making review checklist user-configurable
- Changing user confirmation gate behavior
