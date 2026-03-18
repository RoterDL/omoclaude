---
name: spec-end
description: Spec finalization sub-skill. Triggers experience reflection, archives completed specs, and optionally commits via git. Trigger when all phases (plan, implement, test) are complete.
allowed-tools: ["Bash", "Read", "Write", "AskUserQuestion", "Glob"]
---

# spec-end - Spec Finalization

## Core Principles

1. **Experience capture**: Trigger exp-reflect to capture lessons learned from the full spec cycle
2. **User confirmation**: Always ask before archiving
3. **Clean closure**: Move completed spec to archive, clear current-spec pointer

## Workflow

### Step 1: Verify completion

Read the current spec directory and verify all expected artifacts exist:
- `plan.md` (confirmed)
- `summary.md` (implementation complete)
- `test-report.md` (tests passed)
- `debug-*.md` / `debug-*-fix.md` (if issues were found and fixed)

### Step 2: Experience reflection

Suggest running `/exp-reflect` to analyze the spec lifecycle and extract:
- Dilemma-strategy pairs from problem-solving during implementation
- Knowledge about project architecture discovered during exploration
- Lessons from debugging and testing

The user can choose to run exp-reflect now or skip.

### Step 3: Archive confirmation

Use `AskUserQuestion`:
- "Archive spec to 06-archived/ and optionally commit via git"
- "Keep spec in current location for now"

### Step 4: Archive (if confirmed)

```bash
SPEC_MGR="$(python -c "import os;print(os.path.expanduser('~/.claude/skills/spec/scripts/spec-manager.py'))")" && python "$SPEC_MGR" archive
```

This moves the spec directory to `.spec/06-archived/` and clears the `.current-spec` pointer.

### Step 5: Optional git commit

If user chooses to commit, stage and commit the archived spec and any related changes.

### Step 6: Summary

Report completion:
```
Spec lifecycle complete:
- Plan: plan.md (confirmed)
- Implementation: summary.md
- Tests: test-report.md (passed)
- Experience: [captured / skipped]
- Archive: [archived to 06-archived/ / kept in place]
```

## Common Pitfalls

- Skipping experience reflection (loses valuable lessons)
- Archiving without user confirmation
- Not clearing the .current-spec pointer after archive
