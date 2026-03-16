# know-003: SKILL.md Prompt Optimization Boundaries

## Type
Architecture Decisions

## Content
When optimizing SKILL.md prompts for line count:

**Safe to parameterize**: Agent invocation templates that differ only in agent name, skills flag, and scope label. Use a routing table + single template with placeholders.

**Safe to deduplicate**: Identical code blocks that appear in different intensity branches (e.g., plan-reviewer template). Show block once, branch only on result handling.

**Safe to extract**: Complex inline bash (>15 lines) like diff capture scripts. Extract to standalone script, invoke with single line.

**NOT safe to merge**: `--parallel` fullstack templates — their `---TASK---`/`---CONTENT---` format is structurally distinct. Describe in prose instead of full template.

**NOT safe to remove**: Sub-skill references in Additional References — they provide discoverability for edge-case workflows (spec-debug for diagnosis loops).

## Keywords
SKILL.md, optimization, prompt engineering, template, parameterization
