---
name: spec-plan
description: Design planning sub-skill for spec lifecycle. Creates plan.md design documents by coordinating explore and spec-planner agents. Delegates to codeagent-wrapper for codebase analysis and design authoring. Trigger during Phase 2 of /spec workflow.
allowed-tools: ["Bash", "Read", "Write", "AskUserQuestion", "Glob", "Grep"]
---

# spec-plan - Design & Planning Phase

## Core Rules

### User Confirmation (mandatory)

After plan.md is created, **must** use `AskUserQuestion` to wait for user confirmation before proceeding.

### Category Directories

| Directory | Purpose | Use Case |
|-----------|---------|----------|
| `01-planning` | PRD, process design, project planning | New project, feature planning |
| `02-architecture` | Architecture, data models, service design | Architecture design |
| `03-features` | Feature implementation, API, integration | New feature development |
| `04-bugfix` | Bug fixes, refactoring plans | Bug fix, code refactor |
| `05-testing` | Test plans, test reports | Test preparation |
| `06-archived` | Completed specs (auto-moved) | Archived by spec-end |

**Directory naming**: `YYYYMMDD-HHMM-slug` (slug is English, lowercase, hyphen-separated)

**Path examples**:
```
spec/03-features/20260311-0900-user-auth/plan.md
spec/04-bugfix/20260311-1400-memory-leak-fix/plan.md
```

## Workflow

| Step | Action | Key Point |
|------|--------|-----------|
| 1 | Search related experience | Read spec/context/experience/index.md, spec/context/knowledge/index.md |
| 2 | Explore codebase via codeagent-wrapper | Identify patterns, extension points, constraints |
| 3 | Determine category and directory name | Based on task type; use YYYYMMDD-HHMM-slug format |
| 4 | Create spec directory | `mkdir -p "spec/{category}/{dirname}"` |
| 5 | Invoke spec-planner agent | Generate plan.md content via codeagent-wrapper |
| 6 | Write plan.md | Save to spec directory with frontmatter |
| 7 | Wait for user confirmation | **Must** use AskUserQuestion |

### plan.md Content Requirements

**Required sections**:
1. Overview (background, goals, scope)
2. Requirements analysis
3. Design approach (with alternatives considered)
4. Implementation steps (file touch list with specific changes)
5. Task classification (`task_type`: backend_only / frontend_only / fullstack, with task lists per domain)
6. Risks and dependencies
7. Non-goals

### plan.md Frontmatter

```yaml
---
title: {task title}
type: plan
category: {category directory}
status: draft | confirmed | implementing | testing | completed | archived
phase: intent | plan | implement | test | end
created: {YYYY-MM-DD}
tags: [spec, plan]
---
```

## Prohibitions

- Do NOT start coding before spec confirmation
- Do NOT create directories directly under spec/ (must use category subdirectory)
- Do NOT skip user confirmation step
- Do NOT include test plan in plan.md (test planning is handled by spec-test)

## Recommendations

- Read experience/knowledge indexes for prior art
- Explore codebase before designing
- Keep plan focused on the minimal change set
- Reference existing patterns from codebase exploration
