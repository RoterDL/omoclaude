# Skills

This repository currently includes these skills:

- `codeagent`
- `do`
- `omo`
- `research-pro`
- `taste` — Frontend design quality rules (6 injectable sub-skills: plan-phase `taste-creative`, `taste-brutalist`, `taste-minimalist` + implement-phase `taste-core`, `taste-output`, `taste-redesign`)
- `cr` — Automated code review with single-agent and multi-agent modes (also dependency of `do` / `omo`), trigger: `/cr`
- `spec` — Spec-driven development lifecycle with gate-controlled phases (depends on `memory`)
- `memory` — Dual-layer structured memory system: 3 skills (`exp-search`, `exp-reflect`, `exp-write`)
- `project-init` — One-time `.spec/` directory initialization for spec-driven development

## Install with `install.py` (recommended)

List available modules:

```bash
python install.py --list-modules
```

Install interactively:

```bash
python install.py
```

Force overwrite / custom install directory:

```bash
python install.py --install-dir ~/.claude --module do --force
```

Uninstall modules:

```bash
python uninstall.py --module do,omo
```
