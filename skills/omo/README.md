# omo - Multi-Agent Orchestration

OmO is a multi-agent orchestration skill that routes tasks to specialized agents based on risk signals.

## Installation

```bash
python install.py --module omo
```

## Usage

```
/omo <your task>
```

## Agent Hierarchy

| Agent | Role | Backend | Model |
|-------|------|---------|-------|
| `oracle` | Technical advisor | claude | claude-opus-4-6 |
| `librarian` | External research | claude | claude-sonnet-4-6 |
| `explore` | Codebase search | claude | claude-sonnet-4-6 |
| `develop` | Code implementation | codex | gpt-5.3-codex |
| `frontend-ui-ux-engineer` | UI/UX specialist | gemini | gemini-3.1-pro-preview |
| `document-writer` | Documentation | gemini | gemini-3-flash-preview |
| `code-reviewer` | Code review | claude | claude-sonnet-4-6 |

## Routing Signals (Not Fixed Pipeline)

This skill is **routing-first**, not a mandatory conveyor belt.

| Signal | Add Agent |
|--------|----------|
| Code location/behavior unclear | `explore` |
| External library/API usage unclear | `librarian` |
| Risky change (multi-file, public API, security, perf) | `oracle` |
| Implementation required | `develop` / `frontend-ui-ux-engineer` |
| Documentation needed | `document-writer` |
| Post-implementation quality check or user requests review | `code-reviewer` |

### Skipping Heuristics

- Skip `explore` when exact file path + line number is known
- Skip `oracle` when change is local + low-risk (single area, clear fix)
- Skip implementation agents when user only wants analysis

## Common Recipes

| Task | Recipe |
|------|--------|
| Explain code | `explore` |
| Small fix with known location | `develop` directly |
| Bug fix, location unknown | `explore → develop` |
| Cross-cutting refactor | `explore → oracle → develop` |
| External API integration | `explore + librarian → oracle → develop` |
| UI-only change | `explore → frontend-ui-ux-engineer` |
| Docs-only change | `explore → document-writer` |
| Post-implementation review | `code-reviewer` |
| Review + fix | `code-reviewer → develop` |

## Context Pack Template

Every agent invocation includes:

```text
## Original User Request
<original request>

## Context Pack (include anything relevant; write "None" if absent)
- Explore output: <...>
- Librarian output: <...>
- Oracle output: <...>
- Known constraints: <tests to run, time budget, repo conventions>

## Current Task
<specific task description>

## Acceptance Criteria
<clear completion conditions>
```

## Agent Invocation

```bash
codeagent-wrapper --agent <agent_name> - <workdir> <<'EOF'
## Original User Request
...

## Context Pack
...

## Current Task
...

## Acceptance Criteria
...
EOF
```

Timeout: 2 hours.

## Examples

```bash
# Analysis only
/omo how does this function work?
# → explore

# Bug fix with unknown location
/omo fix the authentication bug
# → explore → develop

# Feature with external API
/omo add Stripe payment integration
# → explore + librarian → oracle → develop

# UI change
/omo redesign the dashboard layout
# → explore → frontend-ui-ux-engineer
```

## Configuration

Agent-model mappings in `~/.codeagent/models.json`:

```json
{
  "default_backend": "codex",
  "default_model": "gpt-5.3-codex",
  "agents": {
    "oracle": {
      "backend": "claude",
      "model": "claude-opus-4-6",
      "yolo": true
    },
    "librarian": {
      "backend": "claude",
      "model": "claude-sonnet-4-6",
      "yolo": true
    },
    "explore": {
      "backend": "claude",
      "model": "claude-sonnet-4-6"
    },
    "frontend-ui-ux-engineer": {
      "backend": "gemini",
      "model": "gemini-3.1-pro-preview"
    },
    "document-writer": {
      "backend": "gemini",
      "model": "gemini-3-flash-preview"
    },
    "code-reviewer": {
      "backend": "claude",
      "model": "claude-sonnet-4-6"
    },
    "develop": {
      "backend": "codex",
      "model": "gpt-5.3-codex",
      "yolo": true,
      "reasoning": "xhigh"
    }
  }
}
```

## Hard Constraints

1. **Never write code yourself** - delegate to implementation agents
2. **Always pass context forward** - include original request + prior outputs
3. **No direct grep/glob for non-trivial exploration** - use `explore`
4. **No external docs guessing** - use `librarian`
5. **Use fewest agents possible** - skipping is normal

## Requirements

- codeagent-wrapper with `--agent` support
- Backend CLIs: claude, codex, gemini
