#!/usr/bin/env python3
"""Uninstaller for myclaude - reads installed_modules.json for precise removal."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

DEFAULT_INSTALL_DIR = "~/.claude"

# Files created by installer itself (not by modules)
INSTALLER_FILES = ["install.log", "installed_modules.json", "installed_modules.json.bak"]
SETTINGS_FILE = "settings.json"
WRAPPER_MODULES = {"do", "omo", "codeagent"}


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Uninstall myclaude")
    parser.add_argument(
        "--install-dir",
        default=DEFAULT_INSTALL_DIR,
        help="Installation directory (defaults to ~/.claude)",
    )
    parser.add_argument(
        "--module",
        help="Comma-separated modules to uninstall (default: all installed)",
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List installed modules and exit",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be removed without actually removing",
    )
    parser.add_argument(
        "--purge",
        action="store_true",
        help="Remove entire install directory (DANGEROUS: removes user files too)",
    )
    parser.add_argument(
        "-y", "--yes",
        action="store_true",
        help="Skip confirmation prompt",
    )
    return parser.parse_args(argv)


def load_installed_modules(install_dir: Path) -> Dict[str, Any]:
    """Load installed_modules.json to know what was installed."""
    status_file = install_dir / "installed_modules.json"
    if not status_file.exists():
        return {}
    try:
        with status_file.open("r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def load_config(install_dir: Path) -> Dict[str, Any]:
    """Try to load config.json from source repo to understand module structure."""
    # Look for config.json in common locations
    candidates = [
        Path(__file__).parent / "config.json",
        install_dir / "config.json",
    ]
    for path in candidates:
        if path.exists():
            try:
                with path.open("r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                continue
    return {}


def get_module_files(module_name: str, config: Dict[str, Any]) -> Set[str]:
    """Extract files/dirs that a module installs based on config.json operations."""
    files: Set[str] = set()
    modules = config.get("modules", {})
    module_cfg = modules.get(module_name, {})

    for op in module_cfg.get("operations", []):
        op_type = op.get("type", "")
        target = op.get("target", "")

        if op_type == "copy_file" and target:
            files.add(target)
        elif op_type == "copy_dir" and target:
            files.add(target)
        elif op_type == "merge_dir":
            # merge_dir merges subdirs like commands/, agents/ into install_dir
            source = op.get("source", "")
            source_path = Path(__file__).parent / source
            if source_path.exists():
                for subdir in source_path.iterdir():
                    if subdir.is_dir():
                        files.add(subdir.name)
    return files


def get_recorded_merge_dir_files(module_status: Dict[str, Any]) -> Set[str]:
    """Read merge_dir output files recorded during install."""
    recorded: Set[str] = set()
    merge_dir_files = module_status.get("merge_dir_files", [])
    if not isinstance(merge_dir_files, list):
        return recorded

    for rel in merge_dir_files:
        rel_str = str(rel).replace("\\", "/").strip()
        if not rel_str:
            continue
        rel_path = Path(rel_str)
        if rel_path.is_absolute() or ".." in rel_path.parts:
            continue
        recorded.add(str(rel_path))

    return recorded


def module_needs_wrapper(module_name: str, config: Dict[str, Any]) -> bool:
    """Whether a module requires codeagent-wrapper."""
    if module_name in WRAPPER_MODULES:
        return True

    module_cfg = config.get("modules", {}).get(module_name, {})
    for op in module_cfg.get("operations", []):
        if op.get("type") != "run_command":
            continue
        cmd = str(op.get("command", ""))
        if "install.sh" in cmd or "install.bat" in cmd:
            return True
    return False


def collect_module_files(
    module_names: Set[str],
    installed_modules: Dict[str, Any],
    config: Dict[str, Any],
) -> Dict[str, Set[str]]:
    """Collect removable file set for each installed module."""
    module_files: Dict[str, Set[str]] = {}
    for name in module_names:
        files = get_module_files(name, config)
        status = installed_modules.get(name, {})
        if isinstance(status, dict):
            files.update(get_recorded_merge_dir_files(status))
        module_files[name] = files
    return module_files


def build_uninstall_file_set(
    selected: List[str],
    installed_modules: Dict[str, Any],
    config: Dict[str, Any],
) -> Tuple[Set[str], Set[str]]:
    """Build file set to remove and shared paths that must be preserved."""
    selected_set = set(selected)
    installed_set = set(installed_modules.keys())
    remaining_set = installed_set - selected_set

    module_files = collect_module_files(selected_set | remaining_set, installed_modules, config)

    protected_by_remaining: Set[str] = set()
    for mod in remaining_set:
        protected_by_remaining.update(module_files.get(mod, set()))

    files_to_remove: Set[str] = set()
    skipped_shared: Set[str] = set()
    for mod in selected_set:
        for rel in module_files.get(mod, set()):
            if rel in protected_by_remaining:
                skipped_shared.add(rel)
                continue
            files_to_remove.add(rel)

    return files_to_remove, skipped_shared


def resolve_install_path(install_dir: Path, item: str) -> Optional[Path]:
    """Resolve an install-relative path safely within install_dir."""
    rel_path = Path(item)
    if rel_path.is_absolute() or ".." in rel_path.parts:
        return None
    path = (install_dir / rel_path).resolve()
    if path == install_dir or install_dir not in path.parents:
        return None
    return path


def prune_empty_parents(path: Path, stop_at: Path) -> None:
    """Remove empty parent dirs up to stop_at (exclusive)."""
    parent = path.parent
    while parent != stop_at and parent.exists():
        try:
            parent.rmdir()
        except OSError:
            break
        parent = parent.parent


def unmerge_agents_from_models(
    module_name: str,
    remaining_modules: Set[str],
    installed_modules: Dict[str, Any],
    config: Dict[str, Any],
) -> bool:
    """Remove module agents from ~/.codeagent/models.json and restore shared ones."""
    prompt_marker_module = "__prompt_file_module__"
    prompt_marker_value = "__prompt_file_module_value__"

    models_path = Path.home() / ".codeagent" / "models.json"
    if not models_path.exists():
        return False

    try:
        with models_path.open("r", encoding="utf-8") as fh:
            models = json.load(fh)
    except (json.JSONDecodeError, OSError):
        return False

    agents = models.get("agents")
    if not isinstance(agents, dict):
        return False

    modified = False

    to_remove = [
        name
        for name, cfg in agents.items()
        if isinstance(cfg, dict) and cfg.get("__module__") == module_name
    ]

    modules_cfg = config.get("modules", {})
    for name in to_remove:
        agents.pop(name, None)
        modified = True
        for other_mod in remaining_modules:
            other_status = installed_modules.get(other_mod, {})
            if isinstance(other_status, dict):
                status = other_status.get("status")
                if status not in (None, "success"):
                    continue
            other_cfg = modules_cfg.get(other_mod, {})
            other_agents = other_cfg.get("agents", {})
            other_agent_cfg = other_agents.get(name)
            if isinstance(other_agent_cfg, dict):
                restored = dict(other_agent_cfg)
                restored["__module__"] = other_mod
                agents[name] = restored
                break

    # Rollback prompt_file backfills applied to user-owned agents.
    for _, cfg in agents.items():
        if not isinstance(cfg, dict):
            continue
        if cfg.get(prompt_marker_module) != module_name:
            continue
        expected = str(cfg.get(prompt_marker_value, "")).strip()
        actual = str(cfg.get("prompt_file", "")).strip()
        if expected and actual == expected:
            cfg.pop("prompt_file", None)
            modified = True
        if prompt_marker_module in cfg or prompt_marker_value in cfg:
            cfg.pop(prompt_marker_module, None)
            cfg.pop(prompt_marker_value, None)
            modified = True

    if not modified:
        return False

    try:
        with models_path.open("w", encoding="utf-8") as fh:
            json.dump(models, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
    except OSError:
        return False

    return True


def unmerge_hooks_from_settings(module_name: str, install_dir: Path) -> bool:
    """Remove hooks belonging to a module from settings.json."""
    settings_path = install_dir / SETTINGS_FILE
    if not settings_path.exists():
        return False

    try:
        with settings_path.open("r", encoding="utf-8") as f:
            settings = json.load(f)
    except (json.JSONDecodeError, OSError):
        return False

    hooks = settings.get("hooks")
    if not isinstance(hooks, dict):
        return False

    modified = False
    for hook_type in list(hooks.keys()):
        entries = hooks.get(hook_type)
        if not isinstance(entries, list):
            continue

        filtered_entries = []
        for entry in entries:
            if isinstance(entry, dict) and entry.get("__module__") == module_name:
                modified = True
                continue
            filtered_entries.append(entry)

        hooks[hook_type] = filtered_entries
        if not filtered_entries:
            del hooks[hook_type]
            modified = True

    if not hooks:
        settings.pop("hooks", None)
        modified = True

    if not modified:
        return False

    try:
        with settings_path.open("w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2, ensure_ascii=False)
            f.write("\n")
    except OSError:
        return False

    return True


def cleanup_shell_config(rc_file: Path, bin_dir: Path) -> bool:
    """Remove PATH export added by installer from shell config."""
    if not rc_file.exists():
        return False

    content = rc_file.read_text(encoding="utf-8")
    original = content

    patterns = [
        r"\n?# Added by myclaude installer\n",
        rf'\nexport PATH="{re.escape(str(bin_dir))}:\$PATH"\n?',
    ]

    for pattern in patterns:
        content = re.sub(pattern, "\n", content)

    content = re.sub(r"\n{3,}$", "\n\n", content)

    if content != original:
        rc_file.write_text(content, encoding="utf-8")
        return True
    return False


def list_installed(install_dir: Path) -> None:
    """List installed modules."""
    status = load_installed_modules(install_dir)
    modules = status.get("modules", {})

    if not modules:
        print("No modules installed (installed_modules.json not found or empty)")
        return

    print(f"Installed modules in {install_dir}:")
    print(f"{'Module':<15} {'Status':<10} {'Installed At'}")
    print("-" * 50)
    for name, info in modules.items():
        st = info.get("status", "unknown")
        ts = info.get("installed_at", "unknown")[:19]
        print(f"{name:<15} {st:<10} {ts}")


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    install_dir = Path(args.install_dir).expanduser().resolve()
    bin_dir = install_dir / "bin"

    if not install_dir.exists():
        print(f"Install directory not found: {install_dir}")
        print("Nothing to uninstall.")
        return 0

    if args.list:
        list_installed(install_dir)
        return 0

    # Load installation status
    status = load_installed_modules(install_dir)
    installed_modules = status.get("modules", {})
    config = load_config(install_dir)

    # Determine which modules to uninstall
    if args.module:
        selected = [m.strip() for m in args.module.split(",") if m.strip()]
        # Validate
        for m in selected:
            if m not in installed_modules:
                print(f"Error: Module '{m}' is not installed")
                print("Use --list to see installed modules")
                return 1
    else:
        selected = list(installed_modules.keys())

    if not selected and not args.purge:
        print("No modules to uninstall.")
        print("Use --list to see installed modules, or --purge to remove everything.")
        return 0

    selected_set = set(selected)
    installed_set = set(installed_modules.keys())
    remaining_modules = installed_set - selected_set
    remove_all_modules = selected_set == installed_set

    # Collect files to remove (protect targets still used by remaining modules)
    files_to_remove, skipped_shared = build_uninstall_file_set(selected, installed_modules, config)

    # Add installer files if removing all modules
    if remove_all_modules:
        files_to_remove.update(INSTALLER_FILES)

    # Wrapper and PATH cleanup decision is based on module dependencies after uninstall
    selected_touches_wrapper = remove_all_modules or any(
        module_needs_wrapper(name, config) for name in selected_set
    )
    wrapper_needed_after = any(module_needs_wrapper(name, config) for name in remaining_modules)
    should_remove_wrapper = selected_touches_wrapper and not wrapper_needed_after
    should_cleanup_shell_path = args.purge or should_remove_wrapper

    files_to_remove.discard("bin")
    files_to_remove.discard("bin/codeagent-wrapper")

    # Show what will be removed
    print(f"Install directory: {install_dir}")
    if args.purge:
        print(f"\n⚠️  PURGE MODE: Will remove ENTIRE directory including user files!")
    else:
        print(f"\nModules to uninstall: {', '.join(selected)}")
        print(f"\nFiles/directories to remove:")
        for f in sorted(files_to_remove):
            path = resolve_install_path(install_dir, f)
            if path is None:
                exists = "⚠ (unsafe path, skipped)"
            else:
                exists = "✓" if path.exists() else "✗ (not found)"
            print(f"  {f} {exists}")
        if should_remove_wrapper:
            wrapper_path = bin_dir / "codeagent-wrapper"
            exists = "✓" if wrapper_path.exists() else "✗ (not found)"
            print(f"  bin/codeagent-wrapper {exists}")
        if skipped_shared:
            print("\nPreserved shared paths (still used by installed modules):")
            for f in sorted(skipped_shared):
                print(f"  {f}")

    # Confirmation
    if not args.yes and not args.dry_run:
        prompt = "\nProceed with uninstallation? [y/N] "
        response = input(prompt).strip().lower()
        if response not in ("y", "yes"):
            print("Aborted.")
            return 0

    if args.dry_run:
        print("\n[Dry run] No files were removed.")
        return 0

    print(f"\nUninstalling...")
    removed: List[str] = []

    if args.purge:
        shutil.rmtree(install_dir)
        print(f"  ✓ Removed {install_dir}")
        removed.append(str(install_dir))
    else:
        # Remove files/dirs in reverse order (files before parent dirs)
        for item in sorted(files_to_remove, key=lambda x: x.count("/"), reverse=True):
            path = resolve_install_path(install_dir, item)
            if path is None:
                print(f"  ⚠ Skipped unsafe path: {item}", file=sys.stderr)
                continue
            if not path.exists():
                continue
            try:
                if path.is_dir():
                    shutil.rmtree(path)
                    print(f"  ✓ Removed {item}/")
                    removed.append(item)
                    prune_empty_parents(path, install_dir)
                else:
                    path.unlink()
                    print(f"  ✓ Removed {item}")
                    removed.append(item)
                    prune_empty_parents(path, install_dir)
            except OSError as e:
                print(f"  ✗ Failed to remove {item}: {e}", file=sys.stderr)

        if should_remove_wrapper:
            wrapper = bin_dir / "codeagent-wrapper"
            if wrapper.exists():
                try:
                    wrapper.unlink()
                    print("  ✓ Removed bin/codeagent-wrapper")
                    removed.append("bin/codeagent-wrapper")
                    prune_empty_parents(wrapper, install_dir)
                except OSError as e:
                    print(f"  ✗ Failed to remove bin/codeagent-wrapper: {e}", file=sys.stderr)

            if bin_dir.exists() and bin_dir.is_dir():
                try:
                    if not any(bin_dir.iterdir()):
                        bin_dir.rmdir()
                        print("  ✓ Removed empty bin/")
                        prune_empty_parents(bin_dir, install_dir)
                except OSError as e:
                    print(f"  ✗ Failed to remove empty bin/: {e}", file=sys.stderr)

        # Remove hooks from settings.json
        for m in selected:
            try:
                if unmerge_hooks_from_settings(m, install_dir):
                    print(f"  ✓ Removed hooks for {m} from settings.json")
            except Exception as e:
                print(f"  ✗ Failed to remove hooks for {m}: {e}", file=sys.stderr)

    # Remove module agents from ~/.codeagent/models.json
    for m in selected:
        try:
            if unmerge_agents_from_models(m, remaining_modules, installed_modules, config):
                print(f"  ✓ Removed agents for {m} from ~/.codeagent/models.json")
        except Exception as e:
            print(f"  ✗ Failed to remove agents for {m}: {e}", file=sys.stderr)

    if not args.purge:
        # Update installed_modules.json
        status_file = install_dir / "installed_modules.json"
        if status_file.exists() and selected_set != installed_set:
            # Partial uninstall: update status file
            for m in selected:
                installed_modules.pop(m, None)
            if installed_modules:
                with status_file.open("w", encoding="utf-8") as f:
                    json.dump({"modules": installed_modules}, f, indent=2)
                    f.write("\n")
                print(f"  ✓ Updated installed_modules.json")
            else:
                status_file.unlink()
                print("  ✓ Removed installed_modules.json")

        # Remove install dir if empty
        if install_dir.exists() and not any(install_dir.iterdir()):
            install_dir.rmdir()
            print(f"  ✓ Removed empty install directory")

    # Clean shell configs
    if should_cleanup_shell_path:
        for rc_name in (".bashrc", ".zshrc", ".profile", ".zprofile"):
            rc_file = Path.home() / rc_name
            if cleanup_shell_config(rc_file, bin_dir):
                print(f"  ✓ Cleaned PATH from {rc_name}")

    print("")
    if removed:
        print(f"✓ Uninstallation complete ({len(removed)} items removed)")
    else:
        print("✓ Nothing to remove")

    if install_dir.exists() and any(install_dir.iterdir()):
        remaining = list(install_dir.iterdir())
        print(f"\nNote: {len(remaining)} items remain in {install_dir}")
        print("These are either user files or from other modules.")
        print("Use --purge to remove everything (DANGEROUS).")

    return 0


if __name__ == "__main__":
    sys.exit(main())
