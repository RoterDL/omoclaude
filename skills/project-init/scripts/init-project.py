#!/usr/bin/env python
"""
Idempotent project initialization script for spec-driven development.

Commands:
  check   - Check project initialization state
  init    - Create spec/ directory structure and memory indexes
"""

import argparse
import os
import sys
from datetime import datetime


# Directory structure to create under spec/
SPEC_DIRS = [
    "spec/01-planning",
    "spec/02-architecture",
    "spec/03-features",
    "spec/04-bugfix",
    "spec/05-testing",
    "spec/06-archived",
    "spec/context/experience",
    "spec/context/knowledge",
]

RULES_DIR = ".claude/rules"


def get_project_root() -> str:
    """Get project root from env or cwd."""
    return os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())


def check_state(project_root: str) -> dict:
    """Check what already exists."""
    state = {
        "spec_dir": os.path.exists(os.path.join(project_root, "spec")),
        "experience_index": os.path.exists(
            os.path.join(project_root, "spec/context/experience/index.md")
        ),
        "knowledge_index": os.path.exists(
            os.path.join(project_root, "spec/context/knowledge/index.md")
        ),
        "rules_dir": os.path.exists(os.path.join(project_root, RULES_DIR)),
        "missing_spec_dirs": [],
    }

    for d in SPEC_DIRS:
        full_path = os.path.join(project_root, d)
        if not os.path.exists(full_path):
            state["missing_spec_dirs"].append(d)

    return state


def create_experience_index(project_root: str) -> bool:
    """Create experience index file."""
    path = os.path.join(project_root, "spec/context/experience/index.md")
    if os.path.exists(path):
        return False

    today = datetime.now().strftime("%Y-%m-%d")
    content = f"""---
title: Experience Index
type: index
updated: {today}
---

# Experience Index

> Use `/exp-search <keywords>` to retrieve related experience.
> This file is maintained by exp-write.

## Index Table

| ID | Title | Keywords | Applicable Scenario | One-line Strategy |
|----|-------|----------|-------------------|------------------|

## Category Index

### Frontend

### Backend

### Architecture Decisions
"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return True


def create_knowledge_index(project_root: str) -> bool:
    """Create knowledge index file."""
    path = os.path.join(project_root, "spec/context/knowledge/index.md")
    if os.path.exists(path):
        return False

    today = datetime.now().strftime("%Y-%m-%d")
    content = f"""---
title: Knowledge Index
type: index
updated: {today}
---

# Knowledge Index

> Use `/exp-search <keywords>` to retrieve related knowledge.
> This file is maintained by exp-write.

## Index Table

| ID | Title | Type | Keywords | One-line Summary |
|----|-------|------|----------|-----------------|

## Category Index

### Project Understanding

### Technical Research

### Code Analysis
"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return True


def cmd_check():
    """Check and report project initialization state."""
    project_root = get_project_root()
    state = check_state(project_root)

    fully_initialized = (
        state["spec_dir"]
        and state["experience_index"]
        and state["knowledge_index"]
        and state["rules_dir"]
        and not state["missing_spec_dirs"]
    )

    if fully_initialized:
        print("STATUS: fully_initialized")
        print("All spec directories, indexes, and rules exist.")
    else:
        print("STATUS: needs_initialization")
        if not state["spec_dir"]:
            print("MISSING: spec/ directory")
        if state["missing_spec_dirs"]:
            for d in state["missing_spec_dirs"]:
                print(f"MISSING: {d}")
        if not state["experience_index"]:
            print("MISSING: spec/context/experience/index.md")
        if not state["knowledge_index"]:
            print("MISSING: spec/context/knowledge/index.md")
        if not state["rules_dir"]:
            print(f"MISSING: {RULES_DIR}")


def cmd_init():
    """Initialize project spec infrastructure (idempotent)."""
    project_root = get_project_root()
    actions = []

    # Create spec directories
    for d in SPEC_DIRS:
        full_path = os.path.join(project_root, d)
        if not os.path.exists(full_path):
            os.makedirs(full_path, exist_ok=True)
            actions.append(f"CREATED: {d}")

    # Create rules directory
    rules_path = os.path.join(project_root, RULES_DIR)
    if not os.path.exists(rules_path):
        os.makedirs(rules_path, exist_ok=True)
        actions.append(f"CREATED: {RULES_DIR}")

    # Create index files
    if create_experience_index(project_root):
        actions.append("CREATED: spec/context/experience/index.md")

    if create_knowledge_index(project_root):
        actions.append("CREATED: spec/context/knowledge/index.md")

    if not actions:
        print("STATUS: no_changes")
        print("All directories and files already exist.")
    else:
        print("STATUS: initialized")
        for action in actions:
            print(action)


def main():
    parser = argparse.ArgumentParser(
        description="Project initialization for spec-driven development"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    subparsers.add_parser("check", help="Check initialization state")
    subparsers.add_parser("init", help="Initialize project (idempotent)")

    args = parser.parse_args()

    if args.command == "check":
        cmd_check()
    elif args.command == "init":
        cmd_init()
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
