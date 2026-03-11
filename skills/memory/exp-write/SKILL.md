---
name: exp-write
description: Memory persistence skill. Writes major experience to spec/context/experience/ or knowledge to spec/context/knowledge/, updating corresponding indexes. Does not write MEMORY.md. Trigger after exp-reflect confirmation or manual /exp-write type=experience|knowledge.
allowed-tools: ["Read", "Write", "Edit", "Glob"]
---

# exp-write - Memory Persistence

## Overview

Write memories to `spec/context/` directory and update index files. Supports two memory types:

1. **Experience memory** (dilemma-strategy pairs) -> `spec/context/experience/`
2. **Knowledge memory** (project understanding / technical research) -> `spec/context/knowledge/`

**Boundary**:
- Writes to `spec/context/experience/` (experience details + index)
- Writes to `spec/context/knowledge/` (knowledge details + index)
- Does NOT write MEMORY.md (managed by Claude Code Auto Memory)
- Does NOT write `.claude/rules/`

**Note**: This skill only handles experience and knowledge memory writes.
- Procedural memory (SOP) -> use skill-creator
- Tool memory -> edit target skill file directly

## Trigger Scenarios

- After `exp-reflect` user confirmation (automatic)
- Manual: `/exp-write type=experience`
- Manual: `/exp-write type=knowledge`

## Core Files

**Experience memory**:
- **Index**: `spec/context/experience/index.md`
- **Details**: `spec/context/experience/exp-{ID}-{title}.md`

**Knowledge memory**:
- **Index**: `spec/context/knowledge/index.md`
- **Details**: `spec/context/knowledge/know-{ID}-{title}.md`

---

## Execution Flow

```
Write flow:
- [ ] Step 0: Determine memory type
      Get type from invocation parameters (experience or knowledge)
      If unspecified, determine type from content

- [ ] Step 1: Determine memory ID
      Read corresponding index file by type:
      - experience -> read spec/context/experience/index.md, find max EXP-ID
      - knowledge -> read spec/context/knowledge/index.md, find max KNOW-ID
      New ID = max ID + 1
      Format: three digits, e.g. 001, 002, 003

- [ ] Step 2: Generate filename
      Select prefix by type:
      - experience -> exp-{ID}-{english-slug}.md
      - knowledge -> know-{ID}-{english-slug}.md

      Examples:
      - exp-001-websocket-timeout.md
      - know-001-teaching-analyzer-architecture.md

- [ ] Step 3: Write detail file
      Select path and template by type:
      - experience -> spec/context/experience/exp-{ID}-{slug}.md (use experience template)
      - knowledge -> spec/context/knowledge/know-{ID}-{slug}.md (use knowledge template)

- [ ] Step 4: Update index file
      Add new entry to corresponding index table:
      - experience -> spec/context/experience/index.md
      - knowledge -> spec/context/knowledge/index.md

- [ ] Step 5: Confirm completion
      Inform user memory is saved
      Show how to retrieve: /exp-search <keywords>
```

---

## File Formats

### Experience Detail File Template

```markdown
---
id: EXP-{ID}
title: {title}
keywords: [{keyword1}, {keyword2}, {keyword3}]
scenario: {applicable scenario}
created: {YYYY-MM-DD}
---

# {title}

## Dilemma

{describe the problem or challenge encountered}

## Strategy

1. {solution step 1}
2. {solution step 2}
3. {solution step 3}

## Reasoning

{why this strategy works}

## Related Files

- {file path 1}
- {file path 2}

## References

- {related links or documents}
```

### Knowledge Detail File Template

```markdown
---
id: KNOW-{ID}
title: {title}
type: {project understanding / technical research / code analysis}
keywords: [{keyword1}, {keyword2}, {keyword3}]
created: {YYYY-MM-DD}
---

# {title}

## Overview

{brief description of the core content}

## Detailed Content

{organized by type}

### Project understanding structure:
- Project overview
- Core architecture
- Data flow
- Key modules
- Tech stack

### Technical research structure:
- Background
- Solution comparison
- Pros and cons analysis
- Conclusions and recommendations

### Code analysis structure:
- Module responsibilities
- Core implementation
- Design patterns
- Key interfaces

## Related Files

- {file path 1}
- {file path 2}

## References

- {related links or documents}
```

### Experience Index Format (experience/index.md)

```markdown
# Experience Index

> Use `/exp-search <keywords>` to retrieve related experience

## Index Table

| ID | Title | Keywords | Applicable Scenario | One-line Strategy |
|----|-------|----------|-------------------|------------------|
| EXP-001 | WebSocket Connection Timeout | WebSocket, timeout, Nginx, heartbeat | Long-running task connection drop | Three-layer protection: Nginx timeout + heartbeat + reconnect |

## Category Index

### Frontend
- [EXP-001] WebSocket Connection Timeout

### Backend
- (none yet)

### Architecture Decisions
- (none yet)
```

### Knowledge Index Format (knowledge/index.md)

```markdown
# Knowledge Index

> Use `/exp-search <keywords>` to retrieve related knowledge

## Index Table

| ID | Title | Type | Keywords | One-line Summary |
|----|-------|------|----------|-----------------|
| KNOW-001 | TeachingAnalyzer Architecture | project understanding | data flow, architecture | Complete video analysis pipeline |

## Category Index

### Project Understanding
- (none yet)

### Technical Research
- (none yet)

### Code Analysis
- (none yet)
```

---

## Naming Conventions

### Memory IDs

**Experience memory**:
- Format: EXP-{three digits}
- Example: EXP-001, EXP-002, EXP-003
- Incrementally assigned, never reused

**Knowledge memory**:
- Format: KNOW-{three digits}
- Example: KNOW-001, KNOW-002, KNOW-003
- Incrementally assigned, never reused

### Filenames

**Experience memory**:
- Format: `exp-{ID}-{english-slug}.md`
- Slug: lowercase, hyphen-separated, concise
- Examples:
  - `exp-001-websocket-timeout.md`
  - `exp-002-multi-role-page-consistency.md`
  - `exp-006-agentscope-memory-management.md`

**Knowledge memory**:
- Format: `know-{ID}-{english-slug}.md`
- Slug: lowercase, hyphen-separated, concise
- Examples:
  - `know-001-teaching-analyzer-architecture.md`
  - `know-002-agentscope-framework-comparison.md`

---

## Update Mode

When updating existing memory:

```
Update flow:
- [ ] Step 1: Read existing memory file
      By type:
      - experience -> spec/context/experience/exp-{ID}-{slug}.md
      - knowledge -> spec/context/knowledge/know-{ID}-{slug}.md

- [ ] Step 2: Merge new content
      Experience: supplement strategy steps, add related files, update reasoning
      Knowledge: supplement details, update architecture diagrams/data flow, add related files

- [ ] Step 3: Update index (if keywords or scenario changed)
- [ ] Step 4: Confirm completion
```

---

## Output Confirmation

### New Experience

```markdown
Experience saved.

File: spec/context/experience/exp-003-agentscope-memory.md
Index: updated spec/context/experience/index.md

If this experience contains daily coding tips worth cross-session recall,
Auto Memory will handle them automatically.

Retrieve: /exp-search AgentScope
```

### New Knowledge

```markdown
Knowledge saved.

File: spec/context/knowledge/know-001-teaching-analyzer-architecture.md
Index: updated spec/context/knowledge/index.md

Retrieve: /exp-search TeachingAnalyzer
```

---

## Quality Checks

Pre-write automatic checks:

### Experience Memory Checks

| Check item | Requirement |
|-----------|-------------|
| Title | Brief and clear, describes the problem not the solution |
| Keywords | 3-6, covering main concepts |
| Scenario | One sentence describing when to use |
| Dilemma | Clear problem background |
| Strategy | Specific executable steps |
| Reasoning | Explains why it works |

### Knowledge Memory Checks

| Check item | Requirement |
|-----------|-------------|
| Title | Brief and clear, describes the knowledge topic |
| Type | Clearly labeled: project understanding / technical research / code analysis |
| Keywords | 3-6, covering main concepts |
| Overview | Brief description of core content |
| Detailed content | Structured organization, clear hierarchy |
| Related files | List key files involved |

---

## Collaboration with Other Skills

| Scenario | Collaborating Skill |
|----------|-------------------|
| Receive experience draft | <- `/exp-reflect` generates |
| Receive knowledge draft | <- `/exp-reflect` generates |
| Post-write verification | -> `/exp-search` to test retrieval |
