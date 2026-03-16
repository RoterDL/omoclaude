# exp-001: Timing Dependency in Gated Mechanisms

## Dilemma
Plan proposed skipping `spec-explorer` based on `review_intensity`, but that value is set by `spec-planner` which runs AFTER the explorer step. Timing conflict makes the gate impossible.

## Strategy
Separate into two independent mechanisms with distinct timing points:
1. **Orchestrator pre-assessment** (before Step 2): orchestrator's own judgment from task description
2. **review_intensity gating** (after Step 3): spec-planner's classification, gates later phases

## Applicable Scenario
Any workflow where a gating decision depends on a value produced by a downstream step.

## Keywords
timing, gating, review_intensity, spec-explorer, pre-assessment
