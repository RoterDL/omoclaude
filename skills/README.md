# Skills

This repository currently includes only these skills:

- `codeagent`
- `do`
- `omo`

## Install with `install.py` (recommended)

List available modules:

```bash
python3 install.py --list-modules
```

Install interactively:

```bash
python3 install.py
```

Force overwrite / custom install directory:

```bash
python3 install.py --install-dir ~/.claude --module do --force
```

Uninstall modules:

```bash
python3 uninstall.py --module do,omo
```
