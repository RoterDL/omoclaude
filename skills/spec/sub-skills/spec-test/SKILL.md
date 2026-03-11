---
name: spec-test
description: Test planning and execution sub-skill. Phase I creates test-plan.md with test cases and acceptance criteria. Phase II executes tests and produces test-report.md. Delegates test execution to codeagent-wrapper --agent spec-tester. Bug fixes delegated to spec-debug, not fixed directly.
allowed-tools: ["Bash", "Read", "Write", "AskUserQuestion", "Glob", "Grep"]
---

# spec-test - Test Planning & Execution

## Core Principles

1. **Two phases, two outputs**: Spec creation phase -> test-plan.md; test execution phase -> test-report.md
2. **Do not fix bugs directly**: When bugs are found, delegate to spec-debug sub-skill, then re-verify after fix
3. **Delegate execution**: Test execution goes through `codeagent-wrapper --agent spec-tester`

## Phase I: Write Test Plan (during spec creation)

### Step 1: Read context

Read from the spec directory:
- `plan.md`: design approach and requirements
- Explore output (if available): existing test patterns and conventions

### Step 2: Create test-plan.md

Write `test-plan.md` in the same directory as plan.md:

```yaml
---
title: Test Plan
type: test-plan
status: draft
created: {YYYY-MM-DD}
plan: plan.md
tags: [spec, test-plan]
---
```

**Required sections**:

```markdown
# Test Plan

## Acceptance Criteria
[Specific, measurable pass/fail criteria]

## Test Cases

| Case ID | Description | Input | Expected Output | Boundary Condition |
|---------|-------------|-------|----------------|-------------------|
| TC-001 | [description] | [input] | [expected] | [boundary] |

## Coverage Requirements
- Code coverage: > 80%
- Functional coverage: [specific requirements]

## Test Environment
[Dependencies, configuration, data preparation]
```

### Step 3: Confirm with user

Use `AskUserQuestion` to confirm the test plan is acceptable.

## Phase II: Execute Tests (after implementation)

### Step 1: Read required documents

- `plan.md`: design approach
- `test-plan.md`: test cases and acceptance criteria
- `summary.md`: implementation details

### Step 2: Delegate test execution

```bash
codeagent-wrapper --agent spec-tester - . <<'EOF'
## Context Pack
- Plan: <paste plan.md content>
- Test Plan: <paste test-plan.md content>
- Summary: <paste summary.md content or "None">

## Current Task
Execute all test cases from test-plan.md.
Run relevant test suites. Report results with pass/fail counts.
Check code coverage if applicable.

## Acceptance Criteria
Complete test report: all test cases executed, results documented, coverage measured.
EOF
```

### Step 3: Handle bug discovery

When tests reveal bugs, do NOT fix directly. Instead:

1. Document the bug in the test report
2. Delegate to spec-debug sub-skill for diagnosis and fix
3. After fix, re-execute the relevant test cases

### Step 4: Record minor adjustments

For non-bug adjustments during testing (parameter tuning, config fixes):
- Record directly in test-report.md under "Modification Record"
- No separate debug document needed

### Step 5: Write test-report.md

Create `test-report.md` in the spec directory:

```yaml
---
title: Test Report
type: test-report
status: draft
created: {YYYY-MM-DD}
plan: plan.md
test-plan: test-plan.md
tags: [spec, test-report]
---
```

**Required sections**:

```markdown
# Test Report

## Test Summary
- Total test cases: X
- Passed: X
- Failed: X (fixed: X)
- Code coverage: X%

## Modification Record

| Type | Description | Related Document |
|------|-------------|-----------------|
| Minor adjustment | [description] | -- |
| Bug fix | [issue summary] | debug-001.md |

## Bugs Found (if any)
- [Bug title] - Fixed / Pending

## Final Result
[Pass / Fail, conclusion]

## Document References
- Design: plan.md
- Test plan: test-plan.md
```

## Common Pitfalls

- Fixing bugs directly instead of delegating to spec-debug (breaks the collaboration loop)
- Acceptance criteria too vague to determine pass/fail
- Forgetting to reference debug documents in test-report.md
