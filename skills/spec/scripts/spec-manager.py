#!/usr/bin/env python
"""
Spec Lifecycle State Management CLI.

Commands:
  create --category <cat> --title <title>  - Create a new spec directory
  list                                     - List all specs
  status                                   - Show current spec status
  update-phase <phase>                     - Update current spec phase
  archive                                  - Archive current spec to 06-archived/
"""

import argparse
import json
import os
import re
import shutil
import sys
from datetime import datetime

# Directory constants
DIR_SPEC = ".spec"
FILE_CURRENT_SPEC = ".spec/.current-spec"
FILE_PLAN = "plan.md"

CATEGORIES = {
    "planning": "01-planning",
    "architecture": "02-architecture",
    "features": "03-features",
    "bugfix": "04-bugfix",
    "testing": "05-testing",
}

PHASE_NAMES = {
    "intent": "Intent Confirmation",
    "plan": "Design & Planning",
    "implement": "Implementation",
    "test": "Testing",
    "end": "Completed",
}

PHASE_ORDER = ["intent", "plan", "implement", "test", "end"]


def get_project_root() -> str:
    """Get project root from env or cwd."""
    return os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())


def get_current_spec_file(project_root: str) -> str:
    """Get current spec pointer file path."""
    return os.path.join(project_root, FILE_CURRENT_SPEC)


def slugify(title: str) -> str:
    """Convert title to URL-friendly slug."""
    slug = title.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    slug = slug.strip("-")
    return slug[:60] if len(slug) > 60 else slug


def read_plan_frontmatter(plan_path: str) -> dict | None:
    """Read plan.md and parse YAML frontmatter."""
    if not os.path.exists(plan_path):
        return None

    try:
        with open(plan_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return None

    match = re.match(r"^---\n(.*?)\n---\n(.*)$", content, re.DOTALL)
    if not match:
        return None

    frontmatter = {}
    for line in match.group(1).split("\n"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, raw_value = line.split(":", 1)
        key = key.strip()
        raw_value = raw_value.strip()

        if raw_value.startswith("[") and raw_value.endswith("]"):
            try:
                frontmatter[key] = json.loads(raw_value)
            except Exception:
                frontmatter[key] = raw_value
        elif raw_value.startswith('"') and raw_value.endswith('"'):
            frontmatter[key] = raw_value[1:-1]
        elif raw_value.startswith("'") and raw_value.endswith("'"):
            frontmatter[key] = raw_value[1:-1]
        else:
            frontmatter[key] = raw_value

    return frontmatter


def write_plan_md(plan_path: str, frontmatter: dict, body: str) -> bool:
    """Write plan.md with YAML frontmatter + body."""
    try:
        lines = ["---"]
        for key, value in frontmatter.items():
            if isinstance(value, list):
                lines.append(f"{key}: {json.dumps(value, ensure_ascii=False)}")
            elif isinstance(value, str) and (":" in value or "<" in value or ">" in value):
                lines.append(f'{key}: "{value}"')
            elif isinstance(value, str):
                lines.append(f"{key}: {value}")
            else:
                lines.append(f"{key}: {value}")
        lines.append("---")
        lines.append("")
        lines.append(body)

        os.makedirs(os.path.dirname(plan_path), exist_ok=True)
        with open(plan_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return True
    except Exception as e:
        print(f"Error writing plan.md: {e}", file=sys.stderr)
        return False


def create_spec(category: str, title: str) -> dict:
    """Create a new spec directory with initial plan.md."""
    project_root = get_project_root()

    if category not in CATEGORIES:
        print(
            f"Error: Unknown category '{category}'. Valid: {', '.join(CATEGORIES.keys())}",
            file=sys.stderr,
        )
        sys.exit(1)

    cat_dir = CATEGORIES[category]
    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
    slug = slugify(title)
    dir_name = f"{timestamp}-{slug}"

    spec_dir = os.path.join(project_root, DIR_SPEC, cat_dir, dir_name)
    os.makedirs(spec_dir, exist_ok=True)

    # Create initial plan.md with frontmatter
    frontmatter = {
        "title": title,
        "type": "plan",
        "category": cat_dir,
        "status": "draft",
        "phase": "intent",
        "created": datetime.now().strftime("%Y-%m-%d"),
        "tags": ["spec", "plan"],
    }

    body = f"""# {title}

## Overview

(to be filled by spec-planner)

## Requirements

(to be filled by spec-planner)

## Design

(to be filled by spec-planner)

## Implementation Steps

(to be filled by spec-planner)

## Risks and Dependencies

(to be filled by spec-planner)
"""

    plan_path = os.path.join(spec_dir, FILE_PLAN)
    write_plan_md(plan_path, frontmatter, body)

    # Set current spec pointer
    relative_path = os.path.relpath(spec_dir, project_root)
    current_spec_file = get_current_spec_file(project_root)
    os.makedirs(os.path.dirname(current_spec_file), exist_ok=True)
    with open(current_spec_file, "w", encoding="utf-8") as f:
        f.write(relative_path)

    return {
        "spec_dir": spec_dir,
        "relative_path": relative_path,
        "plan_path": plan_path,
        "category": cat_dir,
        "phase": "intent",
    }


def get_current_spec(project_root: str) -> str | None:
    """Read current spec directory path."""
    current_spec_file = get_current_spec_file(project_root)
    if not os.path.exists(current_spec_file):
        return None

    try:
        with open(current_spec_file, "r", encoding="utf-8") as f:
            content = f.read().strip()
            return content if content else None
    except Exception:
        return None


def list_specs() -> list[dict]:
    """List all spec directories across categories."""
    project_root = get_project_root()
    spec_root = os.path.join(project_root, DIR_SPEC)
    current_spec = get_current_spec(project_root)

    if not os.path.exists(spec_root):
        return []

    specs = []
    for cat_dir in sorted(CATEGORIES.values()):
        cat_path = os.path.join(spec_root, cat_dir)
        if not os.path.isdir(cat_path):
            continue

        for entry in sorted(os.listdir(cat_path), reverse=True):
            entry_path = os.path.join(cat_path, entry)
            if not os.path.isdir(entry_path):
                continue

            plan_path = os.path.join(entry_path, FILE_PLAN)
            fm = read_plan_frontmatter(plan_path)

            relative_path = os.path.relpath(entry_path, project_root)
            spec_data = {
                "path": relative_path,
                "name": entry,
                "category": cat_dir,
                "is_current": relative_path == current_spec,
            }

            if fm:
                spec_data["title"] = fm.get("title", entry)
                spec_data["status"] = fm.get("status", "unknown")
                spec_data["phase"] = fm.get("phase", "unknown")
            else:
                spec_data["title"] = entry
                spec_data["status"] = "unknown"
                spec_data["phase"] = "unknown"

            specs.append(spec_data)

    # Also check archived
    archived_path = os.path.join(spec_root, "06-archived")
    if os.path.isdir(archived_path):
        for entry in sorted(os.listdir(archived_path), reverse=True):
            entry_path = os.path.join(archived_path, entry)
            if not os.path.isdir(entry_path):
                continue
            relative_path = os.path.relpath(entry_path, project_root)
            specs.append(
                {
                    "path": relative_path,
                    "name": entry,
                    "category": "06-archived",
                    "is_current": False,
                    "title": entry,
                    "status": "archived",
                    "phase": "end",
                }
            )

    return specs


def get_status() -> dict | None:
    """Get current spec status."""
    project_root = get_project_root()
    current_spec = get_current_spec(project_root)

    if not current_spec:
        return None

    spec_dir = os.path.join(project_root, current_spec)
    plan_path = os.path.join(spec_dir, FILE_PLAN)

    fm = read_plan_frontmatter(plan_path)
    if not fm:
        return {"path": current_spec, "title": os.path.basename(current_spec), "phase": "unknown"}

    return {
        "path": current_spec,
        "title": fm.get("title", os.path.basename(current_spec)),
        "status": fm.get("status", "unknown"),
        "phase": fm.get("phase", "unknown"),
        "phase_name": PHASE_NAMES.get(fm.get("phase", ""), "Unknown"),
        "category": fm.get("category", "unknown"),
        "created": fm.get("created", "unknown"),
    }


def update_phase(phase: str) -> bool:
    """Update current spec phase."""
    if phase not in PHASE_NAMES:
        print(
            f"Error: Unknown phase '{phase}'. Valid: {', '.join(PHASE_NAMES.keys())}",
            file=sys.stderr,
        )
        return False

    project_root = get_project_root()
    current_spec = get_current_spec(project_root)

    if not current_spec:
        print("Error: No active spec.", file=sys.stderr)
        return False

    spec_dir = os.path.join(project_root, current_spec)
    plan_path = os.path.join(spec_dir, FILE_PLAN)

    if not os.path.exists(plan_path):
        print("Error: plan.md not found.", file=sys.stderr)
        return False

    try:
        with open(plan_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        print("Error: Failed to read plan.md.", file=sys.stderr)
        return False

    match = re.match(r"^---\n(.*?)\n---\n(.*)$", content, re.DOTALL)
    if not match:
        print("Error: Invalid plan.md format.", file=sys.stderr)
        return False

    fm_str = match.group(1)
    body = match.group(2)

    # Parse and update frontmatter
    fm = {}
    for line in fm_str.split("\n"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, raw_value = line.split(":", 1)
        fm[key.strip()] = raw_value.strip()

    fm["phase"] = phase
    # Update status based on phase
    status_map = {
        "intent": "draft",
        "plan": "confirmed",
        "implement": "implementing",
        "test": "testing",
        "end": "completed",
    }
    fm["status"] = status_map.get(phase, fm.get("status", "draft"))

    write_plan_md(plan_path, fm, body)
    return True


def archive_spec() -> bool:
    """Archive current spec to 06-archived/."""
    project_root = get_project_root()
    current_spec = get_current_spec(project_root)

    if not current_spec:
        print("Error: No active spec.", file=sys.stderr)
        return False

    source_dir = os.path.join(project_root, current_spec)
    if not os.path.exists(source_dir):
        print(f"Error: Spec directory not found: {source_dir}", file=sys.stderr)
        return False

    archive_dir = os.path.join(project_root, DIR_SPEC, "06-archived")
    os.makedirs(archive_dir, exist_ok=True)

    dest_dir = os.path.join(archive_dir, os.path.basename(source_dir))
    if os.path.exists(dest_dir):
        print(f"Error: Archive destination already exists: {dest_dir}", file=sys.stderr)
        return False

    shutil.move(source_dir, dest_dir)

    # Clear current spec pointer
    current_spec_file = get_current_spec_file(project_root)
    if os.path.exists(current_spec_file):
        os.remove(current_spec_file)

    print(f"Archived to: {os.path.relpath(dest_dir, project_root)}")
    return True


def main():
    parser = argparse.ArgumentParser(description="Spec lifecycle state management")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # create command
    create_parser = subparsers.add_parser("create", help="Create a new spec")
    create_parser.add_argument(
        "--category",
        required=True,
        choices=CATEGORIES.keys(),
        help="Spec category",
    )
    create_parser.add_argument(
        "--title", required=True, nargs="+", help="Spec title"
    )

    # list command
    subparsers.add_parser("list", help="List all specs")

    # status command
    subparsers.add_parser("status", help="Show current spec status")

    # update-phase command
    phase_parser = subparsers.add_parser("update-phase", help="Update current phase")
    phase_parser.add_argument(
        "phase", choices=PHASE_NAMES.keys(), help="Phase name"
    )

    # archive command
    subparsers.add_parser("archive", help="Archive current spec")

    args = parser.parse_args()

    if args.command == "create":
        title = " ".join(args.title)
        result = create_spec(args.category, title)
        print(f"Created spec: {result['relative_path']}")
        print(f"Category: {result['category']}")
        print(f"Phase: {result['phase']} ({PHASE_NAMES[result['phase']]})")
        print(f"Plan: {os.path.relpath(result['plan_path'], get_project_root())}")

    elif args.command == "list":
        specs = list_specs()
        if not specs:
            print("No specs found.")
        else:
            for spec in specs:
                marker = "* " if spec.get("is_current") else "  "
                phase = spec.get("phase", "?")
                status = spec.get("status", "unknown")
                print(f"{marker}[{status}] {phase}: {spec['title']}")
                print(f"    {spec['path']}")

    elif args.command == "status":
        status = get_status()
        if not status:
            print("No active spec.")
        else:
            print(f"Spec: {status['title']}")
            print(f"Status: {status.get('status', 'unknown')}")
            print(f"Phase: {status.get('phase', '?')} ({status.get('phase_name', 'Unknown')})")
            print(f"Category: {status.get('category', 'unknown')}")
            print(f"Path: {status['path']}")

    elif args.command == "update-phase":
        if update_phase(args.phase):
            print(f"Updated to phase: {args.phase} ({PHASE_NAMES[args.phase]})")
        else:
            sys.exit(1)

    elif args.command == "archive":
        if not archive_spec():
            sys.exit(1)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
