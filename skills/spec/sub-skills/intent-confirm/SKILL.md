---
name: intent-confirm
description: Intent confirmation sub-skill. Standardizes user intent confirmation before task execution. Auto-triggers for abstract requirements, design decisions, multi-step tasks, or large-impact changes. Skips for simple tasks, detailed specs, queries, and single-file operations.
allowed-tools: ["AskUserQuestion"]
---

# Intent Confirmation

## Core Principle

**Confirm before execute** - Before executing any non-trivial task, restate user intent and get confirmation.

## Confirmation Flow

```
User states requirement
    |
Judge if confirmation needed (see trigger conditions)
    |
+-- Needs confirmation -------------------------+
|  1. Restate user intent                        |
|  2. List key understanding points              |
|  3. Ask "Is this what you mean?"               |
|  4. Wait for user confirmation                 |
|     +-- Confirmed -> start execution           |
|     +-- Needs correction -> re-understand      |
+------------------------------------------------+
    |
+-- No confirmation needed ---------------------+
|  Execute task directly                         |
+------------------------------------------------+
```

## Trigger Conditions

### Needs Confirmation

| Scenario | Description | Example |
|----------|-------------|---------|
| Abstract requirement | Vague or high-level description | "Optimize this feature" |
| Design decision | Architecture changes or design choices | "Refactor the auth module" |
| Ambiguous expression | Multiple valid interpretations | "Update the docs" (which docs? what update?) |
| Large impact scope | Task affects many areas | "Unify error handling across project" |
| Hidden assumptions | Execution requires assumptions | "Add a new feature" (what feature?) |
| Multi-step task | Complex task with multiple phases | "Implement user registration flow" |

### Skip Confirmation

| Scenario | Description | Example |
|----------|-------------|---------|
| Clear simple task | Task is unambiguous and simple | "Run tests", "Commit code" |
| Detailed spec provided | User gave detailed specification | "Follow plan.md to implement" |
| Information query | Pure information lookup | "What does this function do?" |
| Single-file operation | Simple operation on a specific file | "Fix the typo at login.js line 42" |
| User explicit skip | User indicates no confirmation needed | "Just do it, skip confirmation" |

## Confirmation Templates

### Standard Template

```
I understand you want to:
- [understanding point 1]
- [understanding point 2]
- [understanding point 3 (if applicable)]

Is this correct?
```

### Multiple Interpretations Template

```
I understand your requirement, but there are several possible approaches:

**Interpretation A**:
- [describe interpretation A]

**Interpretation B**:
- [describe interpretation B]

Which approach do you prefer? Or do you have something else in mind?
```

### Needs More Info Template

```
I understand you want to:
- [understanding point 1]
- [understanding point 2]

Before starting, I need to confirm:
1. [question 1]?
2. [question 2]?

Is this correct?
```

## Post-confirmation Behavior

### User Confirms

Proceed immediately to execution. If complex, plan steps first.

### User Corrects

Re-read the correction, restate updated understanding, confirm again. Do NOT start execution on unconfirmed understanding.

### User Supplements

Incorporate additional info, update understanding, re-confirm.

## Quality Standards

### Good confirmation
- Accurately captures user's core intent
- Uses specific, actionable language
- Proactively identifies ambiguity points
- Asks relevant clarifying questions

### Poor confirmation
- Simply repeats user's words (no interpretation)
- Misses key information
- Over-confirms simple tasks (wastes time)
- Confirmation is too verbose
