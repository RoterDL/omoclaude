---
title: {task title}
type: plan
category: {category directory, e.g. 03-features}
status: draft
phase: intent
created: {YYYY-MM-DD}
tags: [spec, plan]
---

# {task title}

## Overview

### Background
{Why this task exists. What problem does it solve?}

### Goals
{What does success look like? Be specific and measurable.}

### Scope
{What is included in this spec. What is explicitly excluded.}

## Requirements Analysis

### Functional Requirements
1. {FR-001: Testable requirement description}
2. {FR-002: Testable requirement description}

### Non-functional Requirements
- Performance: {specific targets}
- Security: {specific concerns}
- Compatibility: {backward compatibility requirements}

### Constraints and Assumptions
- {Constraint or assumption 1}
- {Constraint or assumption 2}

## Design Approach

### Chosen Approach
{Description of the selected design approach with rationale}

### Alternatives Considered
1. **{Alternative A}**: {description}. Rejected because: {reason}.
2. **{Alternative B}**: {description}. Rejected because: {reason}.

### Key Design Decisions
- {Decision 1}: {rationale}
- {Decision 2}: {rationale}

## Implementation Steps

| # | File | Change | Depends On |
|---|------|--------|------------|
| 1 | {file path} | {what to modify and why} | - |
| 2 | {file path} | {what to modify and why} | Step 1 |

## Task Classification

- **task_type**: {backend_only | frontend_only | fullstack}
- **backend_tasks**: {list of backend tasks, or "N/A"}
- **frontend_tasks**: {list of frontend tasks, or "N/A"}
- **Rationale**: {why this classification}

## Risks and Dependencies

| Risk | Impact | Mitigation |
|------|--------|------------|
| {risk description} | {high/medium/low} | {mitigation strategy} |

### External Dependencies
- {dependency 1}
- {dependency 2}

## Non-goals

- {What this spec explicitly does NOT cover}
- {Features deferred to future work}
