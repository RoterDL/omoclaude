---
name: exp-search
description: Experience retrieval skill. Searches project memory across five layers (experience, knowledge, SOP, tool memory, auto memory) by keywords. Trigger on /exp-search <keywords>, before complex tasks, or when searching for historical solutions.
allowed-tools: ["Read", "Glob", "Grep"]
---

# exp-search - Experience Retrieval

## Overview

Fast retrieval across multi-layer project memory. Load relevant knowledge at the right moment to avoid repeating past mistakes.

**Five-layer search scope**:
1. **Experience memory**: Dilemma-strategy pairs in `spec/context/experience/exp-*.md`
2. **Knowledge memory**: Project understanding, technical research in `spec/context/knowledge/know-*.md`
3. **Procedural memory (SOP)**: Workflows in `.claude/skills/sop-*/SKILL.md`
4. **Tool memory**: Follow-up actions at the end of each skill's SKILL.md
5. **Auto Memory (read-only)**: Cross-session memory in `~/.claude/projects/*/memory/*.md`

**Boundary**: exp-search is **read-only** across all memory sources. It never writes files.

## Trigger Scenarios

- Before starting a complex task, retrieve related experience
- When encountering errors, search for historical solutions
- When looking for project understanding documents (architecture, data flow)
- User explicitly invokes: `/exp-search <keywords>`

## Core Files

- **Experience index**: `spec/context/experience/index.md`
- **Knowledge index**: `spec/context/knowledge/index.md`
- **Experience details**: `spec/context/experience/exp-{ID}-{title}.md`
- **Knowledge details**: `spec/context/knowledge/know-{ID}-{title}.md`
- **SOP Skills**: `.claude/skills/sop-*/SKILL.md`
- **Auto Memory**: `~/.claude/projects/*/memory/*.md` (read-only)

---

## Execution Flow

```
Retrieval flow:
- [ ] Step 1: Read memory indexes
      1. Read spec/context/experience/index.md (experience memory)
      2. Read spec/context/knowledge/index.md (knowledge memory)
      3. Read MEMORY.md (read-only, supplementary source)
      4. Scan ~/.claude/projects/*/memory/*.md file name list (read-only)

- [ ] Step 2: Keyword matching
      Search indexes for matching entries.
      Match fields: title, keywords, applicable scenario / trigger scenario

      Match scope:
      - Experience table (EXP-xxx)
      - Knowledge table (KNOW-xxx)
      - Procedural memory table (sop-xxx)
      - Tool memory table (skill follow-up actions)
      - MEMORY.md summary lines (read-only)
      - Auto Memory .md file contents (read-only)

- [ ] Step 3: Display matched results
      Group results by memory type

- [ ] Step 4: Load details (optional)
      - Experience memory: read spec/context/experience/exp-xxx-{title}.md
      - Knowledge memory: read spec/context/knowledge/know-xxx-{title}.md
      - Procedural memory: suggest user invoke the corresponding SOP skill
      - Tool memory: read the follow-up actions section of the relevant skill
```

---

## Search Syntax

| Usage | Example | Description |
|-------|---------|-------------|
| Single keyword | `/exp-search WebSocket` | Search for experience containing WebSocket |
| Multiple keywords | `/exp-search WebSocket timeout` | Search for experience containing both words |
| Scenario description | `/exp-search long-running task connection drop` | Match by scenario description |

---

## Output Format

### Matched Results List

```markdown
Search results for "<keywords>":

== Experience Memory (dilemma-strategy pairs) ==

[EXP-003] AgentScope Hook State Management
Keywords: AgentScope, Hook, state
Strategy: Detect new messages via msg.id, reset state while preserving progress

== Knowledge Memory (project understanding / technical research) ==

[KNOW-001] TeachingAnalyzer Data Flow and Architecture
Keywords: data flow, architecture, MainAnalyzer
Summary: Complete video analysis pipeline from ASR to result upload

== Procedural Memory (SOP) ==

[sop-001] Docker Deployment Flow
Trigger: After project code update, deploy to server
Invoke: Use the SOP skill directly

== Tool Memory (skill follow-up actions) ==

[spec-end] Follow-up actions
Summary: Create summary.md -> review -> archive

== Auto Memory (cross-session, read-only) ==

[MEMORY.md] One-line summary...
[debugging.md] Related content snippet...

To view details, provide a memory ID or SOP name.
```

---

## No Match Handling

```markdown
No results found for "<keywords>".

Suggestions:
1. Try more general keywords
2. Check keyword spelling
3. Check Auto Memory for related records (MEMORY.md is loaded every session)
4. This may be a new problem; after solving it, use /exp-reflect to capture experience
```

---

## Auto-trigger Suggestions

In these scenarios, the agent should proactively suggest using exp-search:

| Scenario | Suggested prompt |
|----------|-----------------|
| Starting a complex task | "Before starting, let me search for related experience..." |
| Encountering an error | "This error might have a historical solution, let me search..." |
| User describes a problem | "Let me check if there's prior experience with similar issues..." |

---

## Collaboration with Other Skills

| Scenario | Collaborating Skill |
|----------|-------------------|
| No results found, problem solved | -> `/exp-reflect` to capture new experience or knowledge |
| Need to add new experience | -> `/exp-write type=experience` to write experience |
| Need to add new knowledge | -> `/exp-write type=knowledge` to write knowledge |
