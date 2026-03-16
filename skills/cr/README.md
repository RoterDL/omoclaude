# cr - Automated Code Review

Automated code review and fix for local branches, PRs, commits, and files. Supports single-agent interactive fix and multi-agent adversarial review with auto-fix.

## Installation

```bash
python install.py --module cr
```

Installs `~/.claude/skills/cr/` (skill + references).

Note: `cr` is automatically installed as a dependency of `do` and `omo`.

## Usage

```
/cr [target]
```

Examples:

```
/cr                    # Review current branch changes
/cr #123               # Review PR #123
/cr https://...pull/42 # Review PR by URL
```

## Review Modes

| Mode | Trigger | Description |
|------|---------|-------------|
| PR Review | PR number or URL with `/pull/` | Reviews pull request diffs |
| Local Review (single-agent) | Default, or agent teams unavailable | Single-agent review with interactive fix selection |
| Teams Review (multi-agent) | Agent teams available + user opt-in | Reviewer-verifier adversarial mechanism with auto-fix |

## Teams Review Fix Modes

When multi-agent review is available, the user chooses the auto-fix level:

| Fix Mode | Description |
|----------|-------------|
| `low` | Auto-fix only safest issues (null checks, typos, naming) |
| `low_medium` | Auto-fix most issues, confirm only high-risk ones (Recommended) |
| `full` | Auto-fix everything; only test-baseline issues deferred |

## References

| File | Purpose |
|------|---------|
| `references/local-review.md` | Single-agent local review flow |
| `references/pr-review.md` | PR review flow |
| `references/teams-review.md` | Multi-agent adversarial review flow |
| `references/code-checklist.md` | Code review checklist |
| `references/doc-checklist.md` | Documentation review checklist |
| `references/judgment-matrix.md` | Issue severity judgment matrix |

## Hard Constraints

1. **Never fix code without user confirmation** in single-agent mode
2. **Route by first matching rule** — PR > no teams > uncommitted > main branch > ask
3. **All user-facing text matches user's language**
4. **Interactive dialog tool for all questions** — never output options as plain text

## Dependencies

None (standalone module, but auto-installed as dependency of `do` and `omo`).

## Uninstall

```bash
python uninstall.py --module cr
```
