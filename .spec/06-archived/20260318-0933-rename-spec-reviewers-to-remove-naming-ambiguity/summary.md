# Summary: Rename spec-reviewer agents

## Changes

| File | Change |
|------|--------|
| `skills/spec/references/spec-reviewer.md` | Renamed to `spec-reviewer-lite.md`, name field updated |
| `skills/spec/references/spec-code-reviewer.md` | Renamed to `spec-reviewer-deep.md`, name field + cross-ref updated |
| `config.json` | Agent keys + prompt_file paths updated (lines 281, 284, 305, 308) |
| `skills/spec/SKILL.md` | 7 substitutions across lines 13, 14, 235, 236, 324 |
| `skills/spec/README.md` | 5 lines updated (agent list, directory tree, table rows) |

## Verification
- `grep -r 'spec-code-reviewer'` on active files: empty (pass)
- `grep -rn 'spec-reviewer'` excluding `-lite`/`-deep` on active files: empty (pass)
- `config.json` JSON syntax valid (pass)
