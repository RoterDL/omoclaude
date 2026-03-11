# memory - Dual-Layer Structured Memory System

Cross-workflow structured memory for experience (dilemma-strategy pairs) and knowledge (project understanding, technical research). Independent of spec/do/omo -- usable from any workflow.

## Installation

```bash
python install.py --module memory
```

Installs three skills:
- `~/.claude/skills/exp-search/` - Memory retrieval
- `~/.claude/skills/exp-reflect/` - Conversation analysis + classification
- `~/.claude/skills/exp-write/` - Memory persistence

## Skills

| Skill | Trigger | Purpose | Tools |
|-------|---------|---------|-------|
| `exp-search` | `/exp-search <keywords>` | Read-only retrieval across 5 memory layers | Read, Glob, Grep |
| `exp-reflect` | `/exp-reflect` | Analyze conversation, extract + classify memories | Read, Glob, Grep |
| `exp-write` | `/exp-write type=experience\|knowledge` | Write memories to `.spec/context/` | Read, Write, Edit, Glob |

## Five-Layer Memory Search (exp-search)

| Layer | Location | Content |
|-------|----------|---------|
| 1. Experience | `.spec/context/experience/exp-*.md` | Dilemma-strategy pairs |
| 2. Knowledge | `.spec/context/knowledge/know-*.md` | Project understanding, technical research |
| 3. SOP | `.claude/skills/sop-*/SKILL.md` | Reusable multi-step workflows |
| 4. Tool Memory | Skill SKILL.md follow-up sections | Post-skill actions |
| 5. Auto Memory | `~/.claude/projects/*/memory/*.md` | Claude native memory (read-only) |

## Memory Weight Routing (exp-reflect)

exp-reflect classifies memories by weight to decide storage:

| Dimension | Major -> exp-write | Lightweight -> Auto Memory |
|-----------|-------------------|---------------------------|
| Complexity | Multi-component coordination | Single-point trick |
| Correlation | Needs structured record | Independent, no context |
| Shareability | Team-level | Personal habit |
| Persistence | Long-term architectural decision | Temporary debug trick |

## File Naming Conventions

- Experience: `exp-{ID}-{english-slug}.md` (e.g., `exp-001-websocket-timeout.md`)
- Knowledge: `know-{ID}-{english-slug}.md` (e.g., `know-001-project-architecture.md`)
- IDs: Three-digit, incrementally assigned (EXP-001, KNOW-001)

## Usage Examples

```bash
# Search for related experience before a task
/exp-search WebSocket timeout

# Reflect after solving a problem
/exp-reflect

# Reflect with hints
/exp-reflect record data flow

# Write experience directly
/exp-write type=experience

# Write knowledge directly
/exp-write type=knowledge
```

## Storage Layout

```
<project>/
  .spec/
    context/
      experience/
        index.md                              # Experience index table
        exp-001-websocket-timeout.md          # Experience detail
        exp-002-multi-role-consistency.md
      knowledge/
        index.md                              # Knowledge index table
        know-001-teaching-analyzer-arch.md    # Knowledge detail
```

Requires `.spec/context/` directory -- created by `/project-init` or manually.

## Dependencies

- None (memory is independent of spec/do/omo)
- Optional: `project-init` module to create `.spec/context/` directory structure

## Prerequisites

- Python 3.10+ (for type hint syntax)

## Platform Compatibility

| Item | Linux/macOS | Windows |
|------|-------------|---------|
| exp-search | Fully supported (read-only) | Fully supported (read-only) |
| exp-reflect | Fully supported (read-only) | Fully supported (read-only) |
| exp-write | Fully supported | Fully supported |
| `$HOME` path | Bash `$HOME` | PowerShell `$HOME` (auto variable) |
| File encoding | UTF-8 | UTF-8 |

All three skills use only Read/Write/Edit/Glob/Grep tools -- no shell commands or subprocess calls. Fully cross-platform.

## Collaboration

| From | To | Scenario |
|------|----|----------|
| Any workflow | `exp-search` | Before complex tasks, search for related experience |
| Any workflow | `exp-reflect` | After task completion, capture lessons learned |
| `exp-reflect` | `exp-write` | Write confirmed memories to .spec/context/ |
| `exp-write` | `exp-search` | Verify newly written memories are retrievable |
| `spec` Phase 2 | `exp-search` | Search experience during design planning |
| `spec` Phase 4 | `exp-reflect` | Capture experience during spec wrap-up |

## Uninstall

```bash
python uninstall.py --module memory
```

Note: This only removes the skill files. Memory data in your project's `.spec/context/` is not affected.
