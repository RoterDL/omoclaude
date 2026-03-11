---
name: exp-reflect
description: Experience reflection skill. Analyzes conversation to extract memories and routes by type - dilemma-strategy pairs to experience/, project understanding to knowledge/. Supports weight-based routing (major -> exp-write, lightweight -> Auto Memory). Trigger on /exp-reflect, after task completion, or after solving difficult problems.
allowed-tools: ["Read", "Glob", "Grep"]
---

# exp-reflect - Experience Reflection

## Overview

Analyze current conversation, extract memories worth persisting, and route them by type to appropriate storage layers.

**Memory type recognition**:
- **Dilemma-strategy pairs** (experience memory) -> route by weight (major -> exp-write to `.spec/context/experience/`, lightweight -> Auto Memory)
- **Project understanding** (knowledge memory) -> exp-write to `.spec/context/knowledge/` (architecture, data flow, module analysis)
- **Technical research** (knowledge memory) -> exp-write to `.spec/context/knowledge/` (framework comparison, selection analysis)
- **Procedural memory** (SOP) -> create `sop-xxx` skill via skill-creator
- **Tool memory** -> update skill's follow-up actions section

## Trigger Scenarios

- After task completion (suggestive, not mandatory)
- After solving a difficult problem
- User explicitly invokes: `/exp-reflect`
- User invokes with hints: `/exp-reflect record data flow`, `/exp-reflect record architecture`

## Core Principle

**Analyze content first, then determine memory type**

Not everything is worth recording. Decision tree:

| Ask yourself | Yes | No |
|-------------|------|------|
| Is this a dilemma -> solution experience? | **Experience memory** | Next question |
| Is this project understanding (architecture/data flow/module analysis)? | **Knowledge memory** | Next question |
| Is this technical research (framework comparison/selection analysis)? | **Knowledge memory** | Next question |
| Is this a reusable multi-step process (>5 steps)? | **Procedural memory (SOP)** | Next question |
| Is this a fixed follow-up action after a skill executes? | **Tool memory** | Not worth recording |

---

## Execution Flow

```
Reflection flow:
- [ ] Step 1: Trace conversation
      Review all operations in this conversation
      Identify key decision points and turning points
      Note user hints (e.g. "record data flow", "record architecture")

- [ ] Step 2: Identify memories worth persisting
      Analyze and classify:

      | Content characteristic | Memory type | Storage location |
      |----------------------|-------------|------------------|
      | What problem was solved? Why this approach? | Experience | .spec/context/experience/ |
      | Project architecture, data flow, module analysis? | Knowledge | .spec/context/knowledge/ |
      | Technical research, framework comparison? | Knowledge | .spec/context/knowledge/ |
      | Multi-step operations completed (>5 steps)? Reusable? | Procedural | sop-xxx skill |
      | Fixed follow-up action after a skill? | Tool memory | Skill follow-up section |

- [ ] Step 2.5: Memory weight judgment

      For experience memory (dilemma-strategy pairs):
      | Dimension | Major experience -> exp-write | Lightweight -> Auto Memory |
      |-----------|-------------------------------|----------------------------|
      | Complexity | Multi-component coordination, non-obvious solution | Single-point trick, simple debugging |
      | Correlation | Needs structured record linked to spec/code files | Independent, no context needed |
      | Shareability | Team/project level sharing needed | Personal coding habits |
      | Persistence | Long-term architectural decisions, design patterns | Temporary debugging tricks |

      For knowledge memory (project understanding / technical research):
      - All knowledge memory goes through exp-write to knowledge/
      - No weight distinction needed; project understanding is inherently structured

      Routing result:
      - Major experience -> continue to exp-write flow (write to .spec/context/experience/)
      - Lightweight experience -> suggest Auto Memory handles it (see lightweight guidance)
      - Knowledge memory -> continue to exp-write flow (write to .spec/context/knowledge/)

- [ ] Step 3: Check existing memories (prevent duplicates)
      Based on type identified in step 2, check corresponding location:
      - Experience -> read .spec/context/experience/index.md
      - Knowledge -> read .spec/context/knowledge/index.md
      - Procedural -> list .claude/skills/ sop-* directories
      - Tool memory -> read target skill's follow-up section

- [ ] Step 4: Present analysis results to user
      Group by memory type

- [ ] Step 5: Execute writes after user confirmation
      - Major experience -> invoke /exp-write type=experience
      - Knowledge -> invoke /exp-write type=knowledge
      - Procedural memory -> create SOP skill
      - Tool memory -> edit target skill file directly
```

---

## Reflection Draft Format

```markdown
Reflection results:

== Experience Memory (dilemma-strategy pairs) ==

Title: [brief problem description]
Weight: MAJOR (recommend exp-write) / LIGHTWEIGHT (recommend Auto Memory)
Rationale: [multi-component coordination / needs spec linkage / team sharing / ...]
Keywords: [keyword1], [keyword2], [keyword3]
Applicable scenario: [when this experience is useful]

Dilemma: [describe the problem or challenge encountered]
Strategy:
1. [solution step 1]
2. [solution step 2]
Reasoning: [why this strategy works]

-> MAJOR: after confirmation, invoke /exp-write type=experience
-> LIGHTWEIGHT: Auto Memory will handle this automatically

== Knowledge Memory (project understanding / technical research) ==

Title: [knowledge topic]
Type: project understanding / technical research / code analysis
Keywords: [keyword1], [keyword2], [keyword3]

Content summary:
[brief description of the core content]

Detailed content:
[organized by type]

-> After confirmation, invoke /exp-write type=knowledge

== Procedural Memory (SOP) ==

SOP name: sop-xxx-[name]
Trigger scenario: [when to use this SOP]
Main steps:
1. [step 1]
2. [step 2]
...

-> After confirmation, create SOP skill

== Tool Memory (skill follow-up actions) ==

Target skill: [skill name]
New follow-up actions:
1. [action 1]
2. [action 2]

-> After confirmation, edit skill file directly

Execute these memory operations?
```

---

## Memory Quality Standards

### Worth persisting

| Memory type | Worth-persisting characteristics |
|------------|--------------------------------|
| **Experience** | Solves recurring problem, non-obvious solution, multi-component coordination, lessons learned |
| **Knowledge** | Project architecture understanding, data flow analysis, technical research results, framework comparison |
| **Procedural** | Multi-step process (>5 steps), reusable, clear trigger conditions and verification methods |
| **Tool** | Fixed follow-up action after a skill executes, forms workflow chain |

### Not worth persisting

| Characteristic | Example |
|---------------|---------|
| Common sense | "Variable names should be meaningful" |
| One-off operations | "Fixed a typo" |
| Project-specific temporary workaround | "Temporarily commented out a line" |
| Already documented | Content covered by official framework docs |

---

## Duplicate Detection Rules

```
Q1: Is the core problem in the dilemma description the same?
Q2: Is the main approach in the strategy the same?
Q3: Is the applicable scenario the same?

If Q1 and Q2 both yes -> treat as duplicate
If Q1 yes but Q2 no -> possibly different solution to same problem, ask user
If Q1 no -> not duplicate, can add
```

### Duplicate Handling

```markdown
Found similar experience:

Existing [EXP-001]: WebSocket Connection Timeout
- Dilemma: Long-running task causes connection drop
- Strategy: Three-layer protection (Nginx timeout + heartbeat + reconnect)

This experience is highly similar to existing one.

Options:
1. Do not record (existing experience is sufficient)
2. Update existing experience (supplement with new content)
3. Add new experience (scenario is genuinely different)
```

---

## Auto-trigger Signals

Agent should proactively suggest reflection in these scenarios (suggestive, not mandatory):

| Signal | Suggested prompt |
|--------|-----------------|
| Solved a difficult problem | "The solution to this problem might be worth recording. Want to reflect?" |
| Made an architectural decision | "This decision and its rationale could help in the future. Want to persist it?" |
| User says "always do it this way" | "Got it, let me extract this experience for future reference." |
| Task completed | "Task complete. Any major experience worth structured recording? Daily small experiences will be handled by Auto Memory." |

---

## Lightweight Experience Guidance

When step 2.5 determines lightweight experience, skip exp-write and suggest:

```markdown
This experience is lightweight. Recommend letting Auto Memory handle it:

Experience: [one-line description]

Auto Memory will automatically remember daily experiences like this.
If you believe this is important enough for structured recording, let me know and I will use the exp-write flow.
```

---

## Collaboration with Other Skills

| Scenario | Collaborating Skill |
|----------|-------------------|
| Write experience memory | -> `/exp-write type=experience` |
| Write knowledge memory | -> `/exp-write type=knowledge` |
| Check for duplicates | -> read `.spec/context/experience/index.md` and `.spec/context/knowledge/index.md` |
| Update existing memory | -> `/exp-write` update mode |
