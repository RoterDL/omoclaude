---
name: project-init
description: One-time project initialization for spec-driven development. Creates .spec/ directory structure, memory indexes, and coding rules templates. Trigger on /project-init, when user says "initialize project" / "set up spec environment", or when a project has no .spec/ directory.
allowed-tools: ["Bash(~/.claude/skills/project-init/scripts/init-project.py:*)", "AskUserQuestion", "Read", "Glob"]
---

# project-init - Project Spec Infrastructure Initialization

## Core Principles

1. **Idempotent**: All operations check before create; skip if exists, never overwrite existing content
2. **Complete**: Build the full project skeleton in one run; user needs no manual supplement
3. **One-time**: Execute once per project lifecycle; subsequent development uses `/spec` or `/do`

## Workflow

### Step 1: Check Project State

Run the initialization script to check and create the directory structure:

```bash
python "$HOME/.claude/skills/project-init/scripts/init-project.py" check
```

If .spec/ and .claude/rules/ both exist, inform user that initialization is unnecessary. Suggest using `/spec` to start a development task.

If partially exists, only supplement missing parts.

### Step 2: Gather Project Information

Use `AskUserQuestion` to collect project info (for coding rules context):

```
Project initialization:

1. Project name
2. One-line description
3. Main tech stack (e.g. Python/FastAPI, TypeScript/React)
4. Project type (e.g. web app, CLI tool, library)
```

### Step 3: Run Initialization

```bash
python "$HOME/.claude/skills/project-init/scripts/init-project.py" init
```

This creates:
- `.spec/` directory with 6 category subdirectories + context/
- `.spec/context/experience/index.md` (experience index)
- `.spec/context/knowledge/index.md` (knowledge index)
- `.claude/rules/` directory (if not exists)

### Step 4: Create Coding Rules (if .claude/rules/ is empty)

Based on the project info from Step 2, create minimal coding rules:

Create `.claude/rules/coding-style.md`:
```markdown
# Coding Style

- Naming: {camelCase / snake_case based on language}
- Functions: short, single responsibility
- File length: recommended max 300 lines
- Comments: comment critical logic, not obvious code
```

Create `.claude/rules/spec-workflow.md`:
```markdown
# Spec Workflow Rules

- Implementation requires a confirmed plan.md first
- Do not add features not defined in the spec
- Wait for user confirmation at each key gate
- Use /exp-reflect to capture experience after completion
```

### Step 5: Confirm Results

Present initialization summary:

```
Project spec environment initialized:

- .spec/ directory structure (6 categories + context)
- .spec/context/experience/index.md (experience index)
- .spec/context/knowledge/index.md (knowledge index)
- .claude/rules/ (coding rules templates)

Next steps:
- /spec <task> - Start a spec-driven development task
- /do <task> - Start a feature development workflow
- /exp-search <keywords> - Search project memory
```

## Directory Structure Created

```
<project>/
  .spec/
    01-planning/
    02-architecture/
    03-features/
    04-bugfix/
    05-testing/
    06-archived/
    context/
      experience/
        index.md
      knowledge/
        index.md
  .claude/
    rules/
      coding-style.md
      spec-workflow.md
```

## Common Pitfalls

- Overwriting existing CLAUDE.md with template (check first, skip or merge)
- Overwriting existing .claude/rules/ content (check first)
- Recreating existing .spec/ structure (check first)
- Starting development immediately after init without gathering requirements
