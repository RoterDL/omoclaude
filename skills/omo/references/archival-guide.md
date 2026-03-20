# Archival Guide

Read this file at task wrap-up. Contains trigger conditions, archival flow, and cross-session recovery.

## Task Wrap-up (Optional)

After the task's core work is complete, Sisyphus evaluates whether to archive the session's outputs.

### Trigger Conditions

Archive when **any** of these hold:
- Task involved 2+ agents
- An implementation agent (develop, frontend-ui-ux-engineer) was invoked
- User explicitly asks to save/archive

**Do not trigger** for single-agent explore queries or trivial fixes.

### Wrap-up Flow

1. Use `AskUserQuestion` with three options:
   - **"归档并总结经验"** — write analysis.md, then invoke `/exp-reflect`
   - **"仅归档"** — write analysis.md only
   - **"结束"** — skip archival entirely

2. If archiving, write a temporary file `/tmp/omo-analysis.md` with this template:

```markdown
# <Task Title>

## Task Description
<Original user request>

## Analysis Summary
<Key findings from explore/librarian, condensed>

## Implementation Summary
<What was changed, files touched — skip if analysis-only>

## Key Decisions
<Important choices made and rationale>

## Agents Used
<Agent sequence with brief per-agent contribution>

## Follow-up Items
<Remaining work, known issues, or suggested next steps>
```

3. Save via omo-manager:

```bash
OMO_MGR="$(python -c "import os;print(os.path.expanduser('~/.claude/skills/omo/scripts/omo-manager.py'))")"
python "$OMO_MGR" save --title "<title>" --agents "<agent1,agent2>" --task-type "<analysis|development|mixed>" --file /tmp/omo-analysis.md
```

4. If user chose "归档并总结经验", invoke `/exp-reflect` after save completes.

### Cross-Session Recovery

To resume from a previous analysis:
1. `python "$OMO_MGR" list` to list saved analyses
2. Read the target `analysis.md`
3. Include its content in the Context Pack when routing subsequent agents
