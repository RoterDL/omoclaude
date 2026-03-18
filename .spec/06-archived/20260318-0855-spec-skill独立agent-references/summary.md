# Implementation Summary

## Scope
Made spec skill's agents fully self-contained by creating its own reference files for implementation, frontend, and review agents.

## New Files Created (3)
- `skills/spec/references/spec-develop.md` — Cloned from `do-develop.md`, adapted orchestrator references to `/spec`
- `skills/spec/references/spec-frontend.md` — Cloned from `do-frontend.md`, adapted orchestrator references to `/spec`
- `skills/spec/references/spec-reviewer.md` — Cloned from `do-reviewer.md`, adapted name and orchestrator references to `/spec`

## Files Modified (5)
- `skills/spec/SKILL.md` — 11 substitution sites: `do-develop`->`spec-develop`, `do-frontend`->`spec-frontend`, `do-reviewer`->`spec-reviewer`
- `skills/spec/references/spec-code-reviewer.md` — Line 14: `do-reviewer`->`spec-reviewer`
- `skills/spec/sub-skills/spec-debug/SKILL.md` — 4 substitution sites in description, workflow, and bash snippets
- `skills/spec/README.md` — Updated agent table, installation list, directory structure, removed `do` module dependency
- `config.json` — Added 3 new agent entries under spec module (spec-develop, spec-frontend, spec-reviewer)

## Verification
- `grep -r "do-develop|do-frontend|do-reviewer" skills/spec/` = 0 matches
- `python -m json.tool config.json` = valid JSON
- All 3 new files exist in `skills/spec/references/`
