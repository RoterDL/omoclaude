# Skills

This repository currently includes these skills:

- `codeagent`
- `do`
- `omo`
- `research-pro`
- `taste` — Frontend design quality rules (4 injectable sub-skills: `taste-core`, `taste-output`, `taste-creative`, `taste-redesign`)
- `cr` — Code review checklists (dependency of `do` / `omo`)

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
