---
id: EXP-004
title: Local Artifact vs System Persistence Distinction
keywords: [write-artifact, exp-write, persistence, memory index, dual-write]
scenario: Replacing a persistence tool call with a simpler alternative
created: 2026-03-16
---

# Local Artifact vs System Persistence Distinction

## Dilemma

When optimizing SKILL.md, replaced `/exp-write type=experience` and `/exp-write type=knowledge` calls with `spec-manager.py write-artifact experience-reflection.md`. This unified the write mechanism but silently broke project memory persistence: `write-artifact` only saves a file in the local spec directory, while `/exp-write` persists to `.spec/context/experience/index.md` and `.spec/context/knowledge/index.md` — the indexed memory that future `exp-search` queries read from.

## Strategy

1. Distinguish two write semantics: "local artifact save" (spec directory, for spec lifecycle tracking) vs "system-level persistence" (indexed memory, for cross-spec retrieval).
2. When both are needed, use dual-write: `write-artifact` for the local copy + `/exp-write` for indexed persistence.
3. Never assume a simpler write mechanism is equivalent unless you verify the downstream consumers (in this case, `exp-search` reads from the index, not from spec directories).

## Reasoning

The two write targets serve different purposes with different lifecycles. Spec artifacts are archived with the spec and may be hard to find later. Indexed memory is designed for retrieval across all future specs. Collapsing them into one loses the retrieval guarantee.

## Related Files

- skills/spec/SKILL.md (Phase 4 Step 1)
- .spec/context/experience/index.md
- .spec/context/knowledge/index.md

## References

- Code review BLOCKING finding in optimize-spec-skill-md-v2
