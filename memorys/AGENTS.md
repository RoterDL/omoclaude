## 1. Core Principles

### 1.1 Research First (Mandatory)

The following actions must be performed before modifying any code:

* **Retrieve Related Code**: Use `mcp__augment-context-engine__codebase-retrieval`, LSP, Grep, or Glob.
* **Identify Reuse Opportunities**: Find existing similar functions; prioritize reuse over rewriting.
* **Trace Call Chains**: Analyze the scope of impact via references search (Grep / codebase-retrieval).

### 1.2 Three Questions Before Modification

1. Is this a real issue or an imaginary one? (**Reject over-engineering**)
2. Is there existing code available for reuse? (**Prioritize reuse**)
3. What call relationships will this break? (**Protect the dependency chain**)

### 1.3 Red-Line Principles

* **Prohibit** copy-pasting duplicate code.
* **Prohibit** breaking existing functionality.
* **Prohibit** compromising on incorrect solutions.
* **Prohibit** blind execution without critical thinking.
* **Critical paths** must include error handling.

### 1.4 Knowledge Acquisition (Mandatory)

When encountering unfamiliar knowledge, you must search the web—guessing is strictly forbidden:

#### Web Search (Priority Order)

1. **Grok Search** (preferred): `mcp__grok-search__web_search`
   - Supports deep search + source tracing via `mcp__grok-search__get_sources`
2. **Exa Search** (fallback): `mcp__exa__web_search_exa`
3. **WebSearch** (last resort): Built-in `WebSearch`

#### Grok Model Selection (Mandatory)

**Timing**: Before every `web_search` or `web_fetch` call
**Action**: Call `mcp__grok-search__switch_model` to select the appropriate model. Default: `grok-4.1-thinking`

| Task Type | Model | Trigger |
| --- | --- | --- |
| Quick lookup | `grok-4.1-fast` | Simple questions, single facts |
| Deep research | `grok-4.1-thinking` | Analysis, comparison, complex problems |

#### URL Content Fetching (Priority Order)

1. **Grok Fetch** (preferred): `mcp__grok-search__web_fetch`
2. **Exa Crawl** (fallback): `mcp__exa__crawling_exa`
3. **WebFetch** (last resort): Built-in `WebFetch`

#### Library Documentation

* `mcp__context7__resolve-library-id` → `mcp__context7__query-docs`

#### Open Source Projects

* `mcp__deepwiki__ask_question`

---

## 2. Task Grading

| Level | Criteria | Handling Method |
| --- | --- | --- |
| **Simple** | Single file, clear requirements, < 20 lines of change | Execute directly |
| **Medium** | 2–5 files, requires research | Briefly explain the plan → Execute |
| **Complex** | Architectural changes, multi-module, high uncertainty | Follow Full Planning Process (see 2.1) |

### 2.1 Complex Task Workflow

1. **RESEARCH**: Investigate the code without proposing suggestions yet.
2. **PLAN**: List the proposed solutions and wait for user confirmation.
3. **EXECUTE**: Execute strictly according to the plan.
4. **REVIEW**: Perform a self-check upon completion.

> **Trigger**: Automatically enabled when the user inputs "Enter X Mode" or when a task meets the "Complex" criteria.

### 2.2 Deep Thinking for Complex Problems

* **Trigger Scenarios**: Multi-step reasoning, architectural design, difficult debugging, or solution comparison.
* **Mandatory Tool**: `mcp__sequential-thinking__sequentialthinking`.

---

## 3. Git Standards

* **No Spontaneous Commits/Pushes**: Unless explicitly requested by the user.
* **Commit Format**: `<type>(<scope>): <description>`.
* **No Signatures**: Do not add "Claude" or "codex" attribution markers (e.g., "Generated with Claude Code") to commits.
* **Pre-commit Check**: Run `git diff` to confirm the scope of changes.
* **No Force Push**: Prohibit `--force` pushes to `main`/`master`.

---

## 4. Security Checks

* Prohibit hardcoding keys, passwords, or tokens.
* Prohibit committing sensitive files such as `.env` or `credentials`.
* User input must be validated at system boundaries.

---

## 5. Code Style

* **KISS**: Keep It Simple, Stupid. Avoid complexity where simplicity suffices.
* **DRY**: Zero tolerance for duplication; reuse is mandatory.
* **Protect Call Chains**: When modifying function signatures, update all call sites simultaneously.

### 5.1 Post-Completion Cleanup

* Delete temporary files, commented-out obsolete code, unused imports, and debug logs.

---

## 6. Interaction Standards

### 6.1 When to Ask the User

* When multiple reasonable solutions exist.
* When requirements are unclear or ambiguous.
* When the scope of changes exceeds expectations.
* When potential risks are discovered.

### 6.2 When to Execute Directly

* Requirements are clear and the solution is unique.
* Small-scale modifications (< 20 lines).
* The user has already confirmed similar operations.

### 6.3 Dare to Say "No"

* Point out issues directly when found; do not compromise on flawed solutions.

---

## 7. Environment & Output

### 7.1 Windows / PowerShell Specifics

* PowerShell does not support `&&`; use `;` to separate commands.
* Paths containing Chinese characters must be wrapped in quotes.

### 7.2 Output Settings

* **Language**: Chinese responses.
* **Style**: **Disable emojis**; prohibit truncated output.

## 8. Encoding Rules

* Pay attention to Chinese encoding when writing script files.