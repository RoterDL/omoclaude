# research-pro - Academic Research Orchestrator

Multi-agent academic research orchestration for paper reading, content extraction, paper review, literature search, and structured output.

## Installation

```bash
python install.py --module research-pro
```

Installs:

- `~/.claude/skills/research-pro/` - skill files
- agent presets merged into `~/.codeagent/models.json`

## Usage

```
/research-pro <research task>
```

Examples:

```
/research-pro read this PDF paper and produce notes
/research-pro review my draft and include responses to reviewer comments
/research-pro search recent literature on multimodal LLM safety
/research-pro read this paper and also find related work
```

## Routing Signals

| User Intent | Route |
|-------------|-------|
| Read/extract paper content (no evaluation) | `content-extractor` -> confirm -> `format-writer` |
| Review own paper (with/without reviewer comments) | `paper-reviewer` -> confirm -> `format-writer` |
| Search related literature | `literature-scout` -> confirm -> `format-writer` |
| Combined (read + search) | `content-extractor` + `literature-scout` (parallel) -> confirm -> `format-writer` |
| Analysis only (no output file needed) | Stop after analysis agent(s), present results directly |

## Input Source Handling

| Source | How to Handle |
|--------|---------------|
| PDF file path | Pass file path to agent in Context Pack |
| Word file path | Pass file path to agent in Context Pack |
| Zotero MCP | Query Zotero first, pass retrieved content to agent |
| Paper URL/DOI | Pass to `literature-scout` for retrieval |

## User Confirmation Gate

Before invoking `format-writer`, the orchestrator must:

1. Present analysis outputs from prior agent(s) to the user.
2. Ask for explicit confirmation to proceed.
3. Invoke `format-writer` only after user approval.

## Agents

| Agent | Purpose | Backend | Model |
|-------|---------|---------|-------|
| `content-extractor` | Structured paper extraction (no evaluation) | codex | gpt-5.2 |
| `paper-reviewer` | Paper review + reviewer response guidance | codex | gpt-5.2 |
| `literature-scout` | Online literature search with verified links | codex | gpt-5.2 |
| `format-writer` | Generate formatted output documents | gemini | gemini-3-flash-preview |

## Hard Constraints

1. **Never analyze papers yourself**; delegate to specialized agents.
2. **No direct web search for literature**; delegate to `literature-scout`.
3. **Always pass context forward**: original user request + relevant prior outputs.
4. **Use the fewest agents possible** to satisfy the user goal.
5. **Mandatory user confirmation before invoking `format-writer`.**

## Context Pack Template

```text
## Original User Request
<original request>

## Context Pack (include anything relevant; write "None" if absent)
- Content Extractor output: <...>
- Paper Reviewer output: <...>
- Literature Scout output: <...>
- Reviewer Comments: <external reviewer feedback or "None">
- Paper Source: <file path / Zotero query / URL>

## Current Task
<specific task description>

## Acceptance Criteria
<clear completion conditions>
```

## Examples

| Workflow | Minimal Route |
|----------|---------------|
| Read a paper and produce notes | `content-extractor` -> confirm -> `format-writer` |
| Review draft and respond to reviewer comments | `paper-reviewer` -> confirm -> `format-writer` |
| Search recent literature and produce survey output | `literature-scout` -> confirm -> `format-writer` |
| Read target paper and find related work | `content-extractor` + `literature-scout` (parallel) -> confirm -> `format-writer` |

## Configuration

Agent-model mappings in `~/.codeagent/models.json`:

```json
{
  "agents": {
    "content-extractor": {
      "backend": "codex",
      "model": "gpt-5.2",
      "prompt_file": "~/.claude/skills/research-pro/references/content-extractor.md",
      "reasoning": "high"
    },
    "paper-reviewer": {
      "backend": "codex",
      "model": "gpt-5.2",
      "prompt_file": "~/.claude/skills/research-pro/references/paper-reviewer.md",
      "reasoning": "xhigh"
    },
    "literature-scout": {
      "backend": "codex",
      "model": "gpt-5.2",
      "prompt_file": "~/.claude/skills/research-pro/references/literature-scout.md",
      "yolo": true,
      "reasoning": "high"
    },
    "format-writer": {
      "backend": "gemini",
      "model": "gemini-3-flash-preview",
      "prompt_file": "~/.claude/skills/research-pro/references/format-writer.md"
    }
  }
}
```

## Uninstall

```bash
python install.py --uninstall --module research-pro
```
