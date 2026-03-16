# Experience Reflection: optimize-spec-skill-md-v2

## Experience (dilemma-strategy pairs)

### E1: Local artifact vs system persistence distinction
- **Dilemma**: Replacing `/exp-write` with `write-artifact` unified the write mechanism but lost project memory index persistence.
- **Strategy**: When replacing tool calls, distinguish between "local artifact save" (spec directory) and "system-level persistence" (indexed memory). These are different operations with different semantics. Use dual-write when both are needed.
- **Keywords**: write-artifact, exp-write, persistence, memory index, dual-write

### E2: Source vs installed copy drift
- **Dilemma**: Modified spec-manager.py in the source repo but the installed copy at $HOME/.claude/skills/ was stale, causing write-artifact to fail.
- **Strategy**: After modifying spec infrastructure scripts, either use the source path directly or re-install. Always verify the execution path matches the modified file.
- **Keywords**: install, source, copy, drift, spec-manager

## Knowledge (project understanding)

### K1: allowed-tools supports Skill tool scoping
- The `Skill(exp-write:*)` syntax in SKILL.md frontmatter `allowed-tools` can precisely authorize specific skill invocations without opening all Skill access.
- **Keywords**: allowed-tools, Skill, frontmatter, authorization
