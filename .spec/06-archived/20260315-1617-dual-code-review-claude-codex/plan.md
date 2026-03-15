---
title: dual-code-review-claude-codex
type: plan
category: 03-features
status: testing
phase: test
created: 2026-03-15
tags: ["spec", "plan"]
use_worktree: false
worktree_dir: 
---




# Dual Code Review (Claude + Codex) for Phase 3

## 1. Overview

### Background

Phase 3 Step 4 of `skills/spec/SKILL.md` currently uses a single reviewer (`do-reviewer`, claude-sonnet-4-6) to review implementation output from `do-develop` (codex gpt-5.4). While this is already cross-model (codex writes, claude reviews), a single reviewer has inherent blind spots — any one model's training distribution creates systematic gaps in what it catches versus misses.

Phase 2 already demonstrates a successful dual-review pattern: `spec-planner` (claude-opus) produces plan.md, then `plan-reviewer` (codex gpt-5.4, reasoning=xhigh) reviews it. This cross-model, cross-perspective approach catches issues that same-model review would miss. Phase 3 lacks this same rigor.

Additionally, Phase 3's review-fix loop currently has no iteration cap (`BLOCKING>0: delegate fixes then re-run do-reviewer`), unlike Phase 2 which caps at 3 iterations. Two reviewers without a cap could create unbounded loops if they alternate disagreements.

### Goals

1. Add a second, independent code reviewer using a different model backend (codex) to Phase 3 Step 4
2. Run both reviewers in parallel for zero additional wall-clock time
3. Merge their findings into a unified BLOCKING/MINOR report
4. Add an iteration cap to the review-fix loop (matching Phase 2's max 3 iterations)

### Scope

**In scope:**
- New codex-backed code reviewer agent prompt file
- `config.json` agent registration for the new reviewer
- `skills/spec/SKILL.md` Phase 3 Step 4 rewrite (dual parallel review + merge + iteration cap)
- Agent table update in SKILL.md

**Out of scope:**
- Phase 2 review process (already has dual-perspective review)
- `/do` workflow's standalone review step
- `/omo` workflow's code-reviewer
- Modifications to `do-reviewer.md` itself
- Changes to `codeagent-wrapper` parallel executor (it already supports what we need)

## 2. Requirements Analysis

### Functional Requirements

1. **FR-1**: A new agent `spec-code-reviewer` must exist, backed by codex (gpt-5.4), that can review code changes against a plan without running `git diff` itself
2. **FR-2**: Phase 3 Step 4 must invoke both `do-reviewer` and `spec-code-reviewer` in parallel using `codeagent-wrapper --parallel`. Both reviewers must cover the full changeset (tracked diff + untracked new files), each through its own mechanism: `do-reviewer` determines scope independently via git commands (BashOutput), while `spec-code-reviewer` receives pre-captured diff and untracked file contents via the Context Pack
3. **FR-3**: The orchestrator (Claude, executing SKILL.md) must merge the two reviewers' `Summary: BLOCKING=<n>, MINOR=<n>` lines into a combined assessment using the `max()` strategy
4. **FR-4**: If either reviewer reports BLOCKING > 0, the fix-and-re-review loop triggers
5. **FR-5**: The review-fix loop must cap at 3 iterations (matching Phase 2 precedent); on iteration >= 3 with remaining BLOCKINGs, escalate to user via `AskUserQuestion`
6. **FR-6**: Both reviewers' full outputs must be saved together in `review-report.md`
7. **FR-7**: The diff capture step must include both tracked changes (`git diff HEAD`) and untracked new files (`git status --porcelain` + file contents) to ensure complete review scope

### Non-Functional Requirements

1. **NFR-1**: No additional wall-clock time — parallel execution keeps latency equivalent to single-reviewer
2. **NFR-2**: Token cost increase is bounded — codex reviewer uses `reasoning: "high"` (not xhigh) and reads diff from prompt (no exploratory tool calls)
3. **NFR-3**: The new agent prompt reuses the same `cr` checklists (`code-checklist.md`, `judgment-matrix.md`) for consistent evaluation criteria

### Constraints and Assumptions

- Codex agents cannot execute `BashOutput` / shell commands — the git diff must be captured by the orchestrator and passed in the prompt's Context Pack
- `codeagent-wrapper --parallel` already supports `dependencies` field, topological sort, and per-task KeyOutput extraction — no executor changes needed
- The `Summary: BLOCKING=<n>, MINOR=<n>` output format is stable and parseable by the orchestrator
- Both reviewers must operate in the same `DO_WORKTREE_DIR` as all other Phase 3 agents — the existing env-var prefix pattern (not the parallel config's `worktree: true` field) is the correct mechanism

## 3. Design Approach

### Options Considered

**Option A: Parallel dual review (both run simultaneously, merge results)**
- Both reviewers receive the same diff and plan.md independently
- Orchestrator merges BLOCKING/MINOR counts
- Pro: Independent analysis = genuinely diverse perspectives; no time penalty via parallel execution
- Con: Requires merge logic in SKILL.md instructions; slight increase in total token cost

**Option B: Sequential dual review (claude first, codex second with claude's findings)**
- `do-reviewer` runs first, then `spec-code-reviewer` runs with claude's findings as additional context
- Pro: Codex can focus on what claude missed; potentially fewer duplicate findings
- Con: 2x wall-clock time; codex review is biased by claude's findings (anchoring effect), defeating the purpose of independent perspectives

**Option C: Conditional dual review (only invoke second reviewer for complex/high-risk specs)**
- Only trigger codex reviewer when plan.md has certain markers (e.g., `task_type: fullstack`, high estimated complexity)
- Pro: Cost-efficient for simple changes
- Con: Hard to define "complex" objectively; simple-looking changes can have subtle bugs that benefit most from a second pair of eyes

### Chosen Approach: Option A (Parallel Dual Review)

**Rationale from first principles:**

The value of code review comes from independent analysis with diverse cognitive biases. Option B's sequential approach introduces anchoring bias — the second reviewer's attention is drawn to areas the first already flagged, reducing the chance of catching genuinely novel issues. Option C's conditional approach is a false economy — the marginal cost of a second parallel reviewer is low (bounded token cost, zero wall-clock penalty), but the marginal benefit is highest precisely on the "simple" changes where a single reviewer's confidence is high but wrong.

Option A preserves full independence. Both reviewers see the same inputs, apply the same checklists, but bring different model-level reasoning biases. The parallel executor already handles this pattern — Phase 2's `spec-planner` + `plan-reviewer` proves the infrastructure works.

### Key Design Decisions

1. **Worktree binding**: Both reviewers run under the same `DO_WORKTREE_DIR` environment variable prefix, consistent with how `do-develop`, `do-frontend`, `do-reviewer`, and `spec-tester` already operate in SKILL.md. The `DO_WORKTREE_DIR` is set on the `codeagent-wrapper` command line (not via a `worktree: true` field in parallel task config). This ensures both reviewers operate in the context of the same worktree where implementation ran — `do-reviewer` accesses files and git state directly via BashOutput, while `spec-code-reviewer` works with the pre-captured diff from this same worktree delivered via its Context Pack.

2. **Scope coverage via complementary mechanisms**: The two reviewers cover the full changeset through different mechanisms rather than consuming a single shared paste. `do-reviewer` determines its review scope independently via git commands (BashOutput) — it runs `git diff`, checks `git status` for untracked files, and reads them directly, naturally covering the complete changeset. `spec-code-reviewer` (codex) cannot run shell commands, so the orchestrator pre-captures the diff and untracked file contents and delivers them via the Context Pack. Both approaches cover the same complete changeset — the guarantee comes from each mechanism independently being able to cover all tracked changes and untracked new files. The orchestrator also includes the diff in `do-reviewer`'s Context Pack as supplementary input, but `do-reviewer` is free to verify or augment this via its own git access.

3. **Merge strategy — `max()` rule**: The combined BLOCKING count is `max(claude_blocking, codex_blocking)`. The combined MINOR count is `max(claude_minor, codex_minor)`. This is simple, consistent, and avoids both over-counting (sum would double-count overlapping findings) and under-counting (min would discard one reviewer's signal). Both reports are saved in full — no attempt to deduplicate individual findings, as duplicates across reviewers increase confidence that an issue is real. The loop triggers when `max(claude_blocking, codex_blocking) > 0`.

4. **Iteration cap**: 3 iterations, matching Phase 2's established pattern. Counter tracks review-fix cycles, not individual reviewer invocations.

## 4. Implementation Steps

### Step 1: Create `spec-code-reviewer.md` agent prompt

**File**: `skills/spec/references/spec-code-reviewer.md` (new file)

**What**: A codex-compatible code reviewer prompt, adapted from `do-reviewer.md` (`skills/do/agents/do-reviewer.md`) with these key differences:
- **Tools**: `Glob, Grep, Read` only (no BashOutput — matching `plan-reviewer` tool set)
- **No worktree logic**: Diff comes pre-captured in the prompt, not via git commands
- **Diff source**: Step 1 reads diff from `## Context Pack` instead of running `git diff`
- **Same output format**: `[file:line] [A/B/C] [risk] — description` + `Summary: BLOCKING=<n>, MINOR=<n>`
- **Same checklist references**: `code-checklist.md`, `doc-checklist.md`, `judgment-matrix.md`
- **Same constraints**: Read-only, no code generation, evidence-required, quality over quantity

**Model**: The prompt file frontmatter should specify `model: gpt-5.4` and omit BashOutput from tools.

**Why**: Codex needs a dedicated prompt because it cannot run git commands; the diff must come from the orchestrator. Reusing `do-reviewer.md` directly would cause failures when codex tries to execute `git diff` via BashOutput.

**Complexity**: Low — mostly adaptation of existing `do-reviewer.md` text with `plan-reviewer.md` as the model for codex-compatible tool constraints.

### Step 2: Register `spec-code-reviewer` in `config.json`

**File**: `config.json` — inside `modules.spec.agents` block (after `plan-reviewer` at line 280)

**What**: Add new agent entry:
```json
"spec-code-reviewer": {
  "backend": "codex",
  "model": "gpt-5.4",
  "prompt_file": "~/.claude/skills/spec/references/spec-code-reviewer.md",
  "reasoning": "high"
}
```

**Why**: `codeagent-wrapper` resolves agent backends from `config.json`. Without this entry, `--agent spec-code-reviewer` will fail at resolution time.

**Design note**: `reasoning: "high"` (not `xhigh`) — code review is judgment-heavy but doesn't need the deepest reasoning that plan architecture review (`plan-reviewer`) requires. This keeps token cost proportional to the task.

**Complexity**: Trivial — 5 lines of JSON.

### Step 3: Rewrite SKILL.md Phase 3 Step 4

**File**: `skills/spec/SKILL.md` lines 425-465

**What**: Replace the current single-reviewer Step 4 with a dual-review flow:

**3a. Diff capture** (new, before reviewer invocation):

Capture both tracked changes and untracked new files to provide complete review scope. This mirrors what `do-reviewer` already does internally (it checks for `??` files when there's no diff), but is needed explicitly because `spec-code-reviewer` (codex) cannot run git commands.

```bash
# Capture diff for both reviewers — must include both tracked and untracked changes
# Set BASE_DIR for file reads: worktree root if in worktree mode, else current directory
if [ -n "$DO_WORKTREE_DIR" ]; then
  BASE_DIR="$DO_WORKTREE_DIR"
  DIFF_OUTPUT=$(git -C "$DO_WORKTREE_DIR" diff HEAD)
  UNTRACKED=$(git -C "$DO_WORKTREE_DIR" status --porcelain | grep '^??')
else
  BASE_DIR="."
  DIFF_OUTPUT=$(git diff HEAD)
  UNTRACKED=$(git status --porcelain | grep '^??')
fi

# If there are untracked new files, read their contents and append to DIFF_OUTPUT
# so both reviewers can see newly created files that aren't yet staged
if [ -n "$UNTRACKED" ]; then
  NEW_FILES_CONTENT="--- Untracked new files ---"
  while IFS= read -r line; do
    filepath="${line#\?\? }"
    NEW_FILES_CONTENT="$NEW_FILES_CONTENT
--- new file: $filepath ---
$(cat "$BASE_DIR/$filepath")"
  done <<< "$UNTRACKED"
  DIFF_OUTPUT="$DIFF_OUTPUT
$NEW_FILES_CONTENT"
fi
```

**3b. Parallel dual review invocation**:

Both reviewers are invoked via `DO_WORKTREE_DIR` env-var prefix on the `codeagent-wrapper` command — the same pattern used by `do-develop`, `do-frontend`, `do-reviewer`, and `spec-tester` throughout Phase 3. Each task uses `workdir: .` in the parallel config (the `DO_WORKTREE_DIR` env-var handles the actual directory routing).

```bash
# With worktree:
DO_WORKTREE_DIR=<worktree_dir> codeagent-wrapper --parallel <<'EOF'
---TASK---
id: review_claude
agent: do-reviewer
workdir: .
---CONTENT---
## Original User Request
<user request>

## Context Pack
- Plan: <paste plan.md>
- Summary: <paste summary.md>
- Diff: <paste DIFF_OUTPUT>

## Current Task
Review implementation against plan.md. Focus on correctness (Priority A), then optimization and conventions (B/C).

## Acceptance Criteria
Issue report with BLOCKING/MINOR classification. Summary line: BLOCKING=<n>, MINOR=<n>.
---TASK---
id: review_codex
agent: spec-code-reviewer
workdir: .
---CONTENT---
## Original User Request
<user request>

## Context Pack
- Plan: <paste plan.md>
- Summary: <paste summary.md>
- Diff: <paste DIFF_OUTPUT>

## Current Task
Review implementation against plan.md. Focus on correctness (Priority A), then optimization and conventions (B/C).

## Acceptance Criteria
Issue report with BLOCKING/MINOR classification. Summary line: BLOCKING=<n>, MINOR=<n>.
EOF

# Without worktree:
codeagent-wrapper --parallel <<'EOF'
---TASK---
id: review_claude
agent: do-reviewer
workdir: .
---CONTENT---
## Original User Request
<user request>

## Context Pack
- Plan: <paste plan.md>
- Summary: <paste summary.md>
- Diff: <paste DIFF_OUTPUT>

## Current Task
Review implementation against plan.md. Focus on correctness (Priority A), then optimization and conventions (B/C).

## Acceptance Criteria
Issue report with BLOCKING/MINOR classification. Summary line: BLOCKING=<n>, MINOR=<n>.
---TASK---
id: review_codex
agent: spec-code-reviewer
workdir: .
---CONTENT---
## Original User Request
<user request>

## Context Pack
- Plan: <paste plan.md>
- Summary: <paste summary.md>
- Diff: <paste DIFF_OUTPUT>

## Current Task
Review implementation against plan.md. Focus on correctness (Priority A), then optimization and conventions (B/C).

## Acceptance Criteria
Issue report with BLOCKING/MINOR classification. Summary line: BLOCKING=<n>, MINOR=<n>.
EOF
```

**3c. Merge logic** (new, after parallel execution):

Parse both `Summary:` lines from the parallel output. Compute the combined assessment using the `max()` rule:
- `BLOCKING = max(claude_blocking, codex_blocking)`
- `MINOR = max(claude_minor, codex_minor)`

The effective decision:
- **max BLOCKING = 0**: proceed to Step 5 (tests)
- **max BLOCKING > 0 and iteration < 3**: present both reports' BLOCKING findings as a single fix list, delegate fixes to `do-develop` (or `do-frontend` for UI issues), increment iteration counter, re-run diff capture + both reviewers
- **max BLOCKING > 0 and iteration >= 3**: save combined report as `review-report.md`, present to user via `AskUserQuestion` with the unresolved BLOCKING findings, and ask for guidance

**3d. Iteration cap** (new):
Initialize `review_iteration=0` before entering the review loop. Increment after each fix-and-re-review cycle. This matches Phase 2's pattern at SKILL.md line 216-217.

**3e. Save output**:
Write combined output from both reviewers to `review-report.md` in the spec directory, with clear section headers:
```
# Code Review Report

## Claude Review (do-reviewer)
<full output from review_claude>

## Codex Review (spec-code-reviewer)
<full output from review_codex>

## Combined Summary
BLOCKING=max(claude_blocking, codex_blocking), MINOR=max(claude_minor, codex_minor)
Iteration: <n>/3
```

**Complexity**: Medium — the SKILL.md text needs careful rewriting to maintain clarity while adding parallel invocation, merge logic, and iteration cap.

### Step 4: Update SKILL.md Agent Table and References

**File**: `skills/spec/SKILL.md`

**What**: Update all locations that reference the reviewer agent list or single-reviewer flow:

1. **Agent table** (lines 548-559): Add row for `spec-code-reviewer` after the `do-reviewer` row:

```
| `spec-code-reviewer` | Code review — codex cross-check (cr checklists) | 3 | **Yes** — use `DO_WORKTREE_DIR` |
```

2. **Principle 5** (line 19): Include `spec-code-reviewer` in the worktree agent list:

```
5. **Defer worktree decision until Phase 3.** ... prefix Phase 3 agent calls that operate in the worktree (`do-develop`, `do-frontend`, `do-reviewer`, `spec-code-reviewer`, `spec-tester`) with `DO_WORKTREE_DIR=<path>`.
```

3. **Worktree agent list** (line 51): Add `spec-code-reviewer` to the list of agents that run inside the worktree.

4. **Phase 3 summary** (line 77): Update "Code review via do-reviewer" to "Code review via do-reviewer + spec-code-reviewer (parallel dual review)" to reflect the new dual-review flow.

**Why**: All four locations reference the reviewer setup. Updating only the agent table and principle 5 would leave stale references to single-reviewer flow at lines 51 and 77, creating inconsistency in the SKILL.md documentation.

**Complexity**: Low — 1 line addition + 3 line edits across the file.

### Build Sequence

```
Step 1 (agent prompt)  ─┐
                         ├──> Step 3 (SKILL.md rewrite) ──> Step 4 (agent table)
Step 2 (config.json)   ─┘
```

Steps 1 and 2 are independent and can be done in parallel. Step 3 depends on both (references the agent name and assumes config registration). Step 4 is a trivial addition done alongside Step 3.

## 5. Task Classification

- **task_type**: `backend_only`
- **backend_tasks**:
  1. Create `spec-code-reviewer.md` agent prompt
  2. Add `spec-code-reviewer` entry to `config.json`
  3. Rewrite SKILL.md Phase 3 Step 4 with parallel dual review, merge logic, and iteration cap
  4. Update SKILL.md agent table, principle 5, worktree agent list (line 51), and Phase 3 summary (line 77)
- **frontend_tasks**: None

**Rationale**: This change is entirely to orchestration configuration — agent prompts (markdown), JSON config, and skill instructions (markdown). No frontend code, no application logic, no compiled binaries are involved.

## 6. Risks and Dependencies

### Technical Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Token cost increase from dual review | Certain | Low | Codex reviewer uses `reasoning: "high"` (not xhigh); diff is bounded by actual change size; parallel execution means no wall-clock penalty |
| Reviewer disagreement loops (one says BLOCKING, other says clean after fix, fix introduces new issue for the other) | Low | Medium | 3-iteration cap with user escalation prevents unbounded loops; in practice, genuine BLOCKING issues are objective (bugs, security) not subjective |
| Codex reviewer has less context than do-reviewer (no git exec, no worktree access) | Certain | Low | Diff is explicitly provided in prompt including untracked new files; codex can still read source files via Glob/Grep/Read for surrounding context; `plan-reviewer` operates under identical tool constraints successfully |
| Large diffs exceed codex context window | Low | Medium | Spec-driven changes are scoped by plan.md; if diff is extremely large, orchestrator can note truncation; this is an existing risk for single-reviewer too |
| SKILL.md instructions become harder to follow for the orchestrator | Low | Low | Follow Phase 2's established pattern for iteration cap and escalation; keep parallel config format consistent with existing examples |
| Untracked files missed by diff capture | Low | Medium | Mitigated by explicitly capturing `git status --porcelain` output and reading new file contents into the diff payload (Step 3a) |

### External Dependencies

- **`codeagent-wrapper --parallel`**: Already supports the required parallel task format with `id`, `agent`, `dependencies`, and `---CONTENT---` separators — no changes needed
- **`cr` checklists** (`code-checklist.md`, `judgment-matrix.md`): Already backend-agnostic plain text — readable by both Claude and Codex without modification
- **Codex API availability**: Same dependency as existing `do-develop` and `plan-reviewer` agents; no new external service introduced

### Backward Compatibility

- No breaking changes — the new parallel review is a strict superset of the old single review
- `do-reviewer` itself is completely unchanged; it continues to work identically in `/do`, `/omo`, and standalone contexts
- The iteration cap is a new constraint on Phase 3 that currently has no cap — this is strictly safer behavior (prevents infinite loops)
- If `spec-code-reviewer` fails to resolve (e.g., config not installed), `codeagent-wrapper` will error explicitly — no silent degradation

## 7. Non-goals

1. **Not changing Phase 2 review** — Phase 2 already has its own dual-perspective pattern (`spec-planner` on claude-opus produces, `plan-reviewer` on codex reviews)
2. **Not modifying `do-reviewer.md`** — The existing Claude reviewer prompt is stable and well-tested; we add a second reviewer alongside it, not replace it
3. **Not adding dual review to `/do` or `/omo` workflows** — Those workflows have their own review patterns and lifecycle; this change is scoped to `/spec` Phase 3 only
4. **Not building automated deduplication** — If both reviewers flag the same file:line, both findings appear in the combined report; duplicate findings across independent reviewers are a signal of high confidence, not noise to be removed. The `max()` merge rule handles the summary counts without needing finding-level dedup.
5. **Not adding configurable reviewer count** — Two reviewers (one per model backend) is the design point; making it N-configurable adds complexity for a problem that doesn't exist
6. **Not modifying `codeagent-wrapper` code** — The parallel executor already has all required capabilities; this is a pure configuration/instruction change

## 8. Acceptance Scenarios

The following scenarios verify the key paths of the dual-review flow:

### Scenario A: Worktree mode, both reviewers pass
1. Phase 3 enables worktree; `DO_WORKTREE_DIR` is set
2. Implementation completes; diff capture runs `git -C "$DO_WORKTREE_DIR" diff HEAD` + `git -C "$DO_WORKTREE_DIR" status --porcelain`
3. Both reviewers invoked via `DO_WORKTREE_DIR=<path> codeagent-wrapper --parallel`
4. Both return `BLOCKING=0`; `max(0, 0) = 0`
5. Proceed to Step 5 (tests)

### Scenario B: No worktree, both reviewers pass
1. Phase 3 skips worktree; `DO_WORKTREE_DIR` is unset
2. Diff capture runs `git diff HEAD` + `git status --porcelain` in current directory
3. Both reviewers invoked via `codeagent-wrapper --parallel` (no env prefix)
4. Both return `BLOCKING=0`; proceed to tests

### Scenario C: One reviewer finds BLOCKING, iteration < 3
1. `review_claude` returns `BLOCKING=2, MINOR=1`; `review_codex` returns `BLOCKING=0, MINOR=3`
2. Combined: `BLOCKING=max(2,0)=2, MINOR=max(1,3)=3`
3. BLOCKING > 0 and iteration (0) < 3: delegate fixes, increment to iteration=1
4. Re-capture diff, re-run both reviewers
5. Both return `BLOCKING=0`: proceed to tests

### Scenario D: Iteration cap reached (iteration >= 3), escalate to user
1. After 3 fix-and-re-review cycles, at least one reviewer still reports `BLOCKING > 0`
2. Combined report saved as `review-report.md`
3. `AskUserQuestion` presents unresolved BLOCKING findings and asks for guidance
4. User decides: force-proceed, manually fix, or abort

### Scenario E: Untracked new files in review scope
1. Implementation creates new files that aren't yet staged (`git status --porcelain` shows `??` entries)
2. Diff capture reads these files' contents and appends under `--- Untracked new files ---`
3. Both reviewers see the new file contents in the Diff section of their Context Pack
4. Reviewers can flag issues in new files (matching `do-reviewer`'s existing behavior for untracked files)
