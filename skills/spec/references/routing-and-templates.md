# Routing & Templates Reference

Read this file when entering review steps (Phase 2 Step 5, Phase 3 Step 5) or fullstack implementation (Phase 3 Step 2).

## Task_type → Backend Routing

Read `task_type` from plan.md Task Classification. Route:

| task_type | --backend flag |
|-----------|----------------|
| `backend_only` (or missing) | `--backend codex` |
| `frontend_only` | `--backend claude` |
| `fullstack` | run both, then merge (see Fullstack Split-Merge) |

## Fullstack Split-Merge Pattern

For fullstack task_type, run the agent twice with scope constraints, then merge results.

```bash
# 1. Frontend pass
codeagent-wrapper --agent <agent> --backend claude - . <<'EOF' > /tmp/<artifact>-frontend.md
## Original User Request
<request>

## Context Pack
<context items>

## Current Task
<task description>
**Scope: frontend aspects only.**

## Acceptance Criteria
<criteria>
EOF
```

```bash
# 2. Backend pass
codeagent-wrapper --agent <agent> --backend codex - . <<'EOF' > /tmp/<artifact>-backend.md
## Original User Request
<request>

## Context Pack
<context items>

## Current Task
<task description>
**Scope: backend aspects only.**

## Acceptance Criteria
<criteria>
EOF
```

```bash
# 3. Merge
{
  printf '## Frontend Review\n\n'
  cat /tmp/<artifact>-frontend.md
  printf '\n## Backend Review\n\n'
  cat /tmp/<artifact>-backend.md
} > /tmp/<artifact>.md
```

## Review Invocation Pattern

Parameterized pattern for plan review (Phase 2 Step 5) and code review (Phase 3 Step 5).

**Parameters** (set by the calling step):

| Param | Phase 2 (Plan review) | Phase 3 (Code review) |
|-------|----------------------|----------------------|
| agent | `plan-reviewer` | `spec-reviewer-lite` (standard) or `spec-reviewer-deep` (full) |
| artifact | `plan-review.md` | `review-report.md` |
| context | plan.md content | plan.md + summary.md + diff |
| task | Review against 7-area checklist | Review implementation against plan |
| scope | (none) | standard: "Priority A/B only. Skip C." / full: "all priorities A/B/C" |

**Steps:**

1. Apply task_type routing (table above) to determine backend(s).

2. **Single backend** (backend_only or frontend_only):
```bash
codeagent-wrapper --agent <agent> --backend <routed_backend> - . <<'EOF'
## Original User Request
<request>

## Context Pack
<context items>

## Current Task
<task description>
<scope constraint if applicable>

## Acceptance Criteria
<criteria, typically: "Issue report with BLOCKING/MINOR classification. Summary: BLOCKING=<n>, MINOR=<n>.">
EOF
```

3. **Fullstack**: Apply Fullstack Split-Merge Pattern above. Append scope constraint ("frontend aspects only" / "backend aspects only") to each pass's Current Task.

4. Save result:
```bash
python "$SPEC_MGR" write-artifact <artifact> --file /tmp/<artifact>.md
```

## Intensity-Based Result Handling

After review completes, handle by `review_intensity`:

- **standard**: Proceed to next gate regardless of BLOCKING count (user decides at gate). For code review: if BLOCKING > 0, present to user via `AskUserQuestion` for guidance before proceeding.
- **full**: Initialize revision counter at 0.
  - BLOCKING=0: proceed.
  - BLOCKING>0 and iteration < 2: re-invoke the producing agent with reviewer feedback appended to Context Pack, re-write artifact, re-run review.
  - BLOCKING>0 and iteration >= 2: present to user via `AskUserQuestion` for guidance.

## Fullstack Parallel Implementation

For Phase 3 Step 2, when `task_type` is `fullstack`:

```bash
codeagent-wrapper --parallel - . <<'EOF'
---TASK---
agent: spec-develop

## Original User Request
<request>

## Context Pack
- Plan: <plan.md content>
- Explore output: <paste>

## Current Task
Implement backend changes according to plan.md. Follow existing patterns. Add/adjust tests per plan.
{review_notice}

## Acceptance Criteria
All backend plan items implemented. Tests pass.
Summary: <one sentence>
---TASK---
agent: spec-frontend
skills: taste-core,taste-output

## Original User Request
<request>

## Context Pack
- Plan: <plan.md content>
- Explore output: <paste>

## Current Task
Implement frontend changes according to plan.md. Follow existing patterns. Add/adjust tests per plan.
{review_notice}

## Acceptance Criteria
All frontend plan items implemented. Tests pass.
Summary: <one sentence>
EOF
```
