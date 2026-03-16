# know-001: spec-manager.py Phase Values and State Machine

## Type
Project Understanding

## Content
`spec-manager.py` supports 5 phase values for `update-phase`:
- `intent` → status: `draft`
- `plan` → status: `confirmed`
- `implement` → status: `implementing`
- `test` → status: `testing`
- `end` → status: `completed`

No ordering enforcement — any valid key is accepted regardless of current phase. Located at `skills/spec/scripts/spec-manager.py` lines 37-45 (PHASE_NAMES) and 439-475 (update_phase).

Prior to optimization, SKILL.md only called 3 of 5 values (plan/test/end), skipping `implement`. Now all 5 are used.

## Keywords
spec-manager, phase, state machine, update-phase
