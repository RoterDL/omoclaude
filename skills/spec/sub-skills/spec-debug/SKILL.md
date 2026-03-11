---
name: spec-debug
description: Problem diagnosis and fix delegation sub-skill. Diagnoses issues found during spec execution, creates debug documents for traceability, and delegates fixes to codeagent-wrapper --agent do-develop (or do-frontend for UI issues). Does NOT modify confirmed plan.md. Forms feedback loop with spec-test.
allowed-tools: ["Bash", "Read", "Write", "AskUserQuestion", "Glob", "Grep"]
---

# spec-debug - Problem Diagnosis & Fix Delegation

## Core Principles

1. **Do not modify confirmed plan.md**: Create separate debug documents to maintain design traceability
2. **Closed-loop collaboration**: Receive bug report -> diagnose -> fix -> notify for re-verification
3. **User confirmation on diagnosis**: Present diagnosis to user before executing fix

## Collaboration Loop

```
spec-test finds bug
    -> spec-debug receives report
    -> Diagnose -> debug-xxx.md
    -> User confirms diagnosis
    -> Delegate fix to codeagent-wrapper --agent do-develop (or do-frontend)
    -> debug-xxx-fix.md (fix summary)
    -> spec-test re-verifies
```

## Workflow

### Step 1: Collect problem information

From the test report or user report, gather:
- Problem symptoms and reproduction steps
- Expected behavior vs actual behavior
- Related test case ID (if from spec-test)

Read related documents: plan.md, summary.md, test-report.md (if exists).

### Step 2: Search historical experience

Search for related historical solutions:
```
/exp-search <problem keywords>
```

### Step 3: Reproduce and locate

Attempt to reproduce the issue. Use logs, debugging tools to locate the problem code. Confirm boundary conditions.

### Step 4: Root cause analysis

| Type | Description |
|------|-------------|
| Design omission | Boundary case not considered in plan.md |
| Implementation deviation | Implementation inconsistent with plan.md |
| Environment issue | Dependency, configuration, version problem |
| Integration issue | Module interaction problem |

### Step 5: Create debug-xxx.md

**Naming**: `debug-001.md` (numbered by discovery order)

Create in the spec directory:

```yaml
---
title: "Diagnosis: {brief description}"
type: debug
status: draft
severity: high | medium | low
created: {YYYY-MM-DD}
plan: plan.md
tags: [spec, debug]
---
```

**Required content**: Problem symptoms, reproduction steps, root cause analysis, proposed fix, relationship to plan.md.

### Step 6: User confirmation

Present the diagnosis to user via `AskUserQuestion`:
- "Diagnosis confirmed, proceed with fix"
- "Need to revise diagnosis"

### Step 7: Delegate fix

After user confirms diagnosis, delegate the fix.

**Backend fix:**
```bash
codeagent-wrapper --agent do-develop - . <<'EOF'
## Context Pack
- Plan: <paste plan.md content>
- Debug diagnosis: <paste debug-xxx.md content>

## Current Task
Fix the issue described in the debug diagnosis.
- Minimal change scope
- Do not add new features
- Add code comments referencing debug document: "Fix: debug-001.md"

## Acceptance Criteria
Issue fixed. Related tests pass.
EOF
```

**Frontend fix:**
```bash
codeagent-wrapper --agent do-frontend --skills taste-core,taste-output - . <<'EOF'
## Context Pack
- Plan: <paste plan.md content>
- Debug diagnosis: <paste debug-xxx.md content>

## Current Task
Fix the frontend issue described in the debug diagnosis.
- Minimal change scope
- Do not add new features
- Add code comments referencing debug document: "Fix: debug-001.md"

## Acceptance Criteria
Issue fixed. Related tests pass.
EOF
```

Choose agent based on the plan.md `task_type` and the nature of the bug.

### Step 8: Create debug-xxx-fix.md

After fix is applied, write fix summary:

```yaml
---
title: "Fix Summary: {brief description}"
type: debug-fix
status: completed
created: {YYYY-MM-DD}
plan: plan.md
debug: debug-001.md
tags: [spec, debug-fix]
---
```

**Required content**: Files modified, key changes (before/after), verification results.

### Step 9: Trigger re-verification

Inform spec-test to re-run the relevant test cases for the fixed issue.

## Prohibitions

- Do NOT modify confirmed plan.md directly
- Do NOT add new features during bug fix (use a new spec for that)
- Do NOT self-judge if fix is successful; always delegate verification to spec-test

## Common Pitfalls

- Modifying plan.md instead of creating debug documents (breaks traceability)
- Not requesting re-verification after fix (breaks the feedback loop)
- Introducing new features during fix (scope creep)
