#!/usr/bin/env python
"""
OmO Analysis Archival CLI.

Commands:
  save --title <title> [--agents <a,b>] [--tags <t1,t2>] [--task-type <type>] --file <path>
  list [--limit N]
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime


# Directory for analysis archives
DIR_ANALYSIS = ".spec/07-analysis"


def _read_stdin_safe() -> str:
    """Read stdin with robust encoding for Windows pipe compatibility."""
    if sys.platform == "win32":
        try:
            sys.stdin.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError):
            pass
        try:
            return sys.stdin.read()
        except UnicodeDecodeError:
            raw = sys.stdin.buffer.read()
            return raw.decode("utf-8", errors="replace")
    return sys.stdin.read()


def slugify(title: str) -> str:
    """Convert title to URL-friendly slug."""
    slug = title.lower().strip()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    slug = slug.strip("-")
    return slug[:60] if len(slug) > 60 else slug


def get_project_root() -> str:
    """Get project root from env or cwd."""
    return os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())


def read_frontmatter(filepath: str) -> dict | None:
    """Parse YAML frontmatter from a markdown file."""
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception:
        return None

    match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
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


def write_analysis_md(filepath: str, frontmatter: dict, body: str) -> bool:
    """Write analysis.md with YAML frontmatter + body."""
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

        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        return True
    except Exception as e:
        print(f"Error writing analysis.md: {e}", file=sys.stderr)
        return False


def cmd_save(args):
    """Save an analysis archive."""
    project_root = get_project_root()
    title = " ".join(args.title)

    # Read body from file
    try:
        with open(args.file, "r", encoding="utf-8") as f:
            body = f.read()
    except Exception as e:
        print(f"Error reading file: {e}", file=sys.stderr)
        sys.exit(1)

    if not body.strip():
        print("Error: Empty body content.", file=sys.stderr)
        sys.exit(1)

    # Build directory
    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
    slug = slugify(title)
    dir_name = f"{timestamp}-{slug}"
    analysis_dir = os.path.join(project_root, DIR_ANALYSIS, dir_name)

    # Build frontmatter
    frontmatter = {
        "title": title,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "task_type": args.task_type or "mixed",
    }
    if args.agents:
        frontmatter["agents_used"] = [a.strip() for a in args.agents.split(",")]
    if args.tags:
        frontmatter["tags"] = [t.strip() for t in args.tags.split(",")]

    filepath = os.path.join(analysis_dir, "analysis.md")
    if write_analysis_md(filepath, frontmatter, body):
        rel = os.path.relpath(filepath, project_root)
        print(f"Saved: {rel}")
    else:
        sys.exit(1)


def cmd_list(args):
    """List saved analyses."""
    project_root = get_project_root()
    analysis_root = os.path.join(project_root, DIR_ANALYSIS)

    if not os.path.isdir(analysis_root):
        print("No analyses found.")
        return

    entries = []
    for entry in sorted(os.listdir(analysis_root), reverse=True):
        entry_path = os.path.join(analysis_root, entry)
        if not os.path.isdir(entry_path):
            continue
        analysis_file = os.path.join(entry_path, "analysis.md")
        fm = read_frontmatter(analysis_file)
        entries.append({
            "dir": entry,
            "title": fm.get("title", entry) if fm else entry,
            "created": fm.get("created", "unknown") if fm else "unknown",
            "task_type": fm.get("task_type", "unknown") if fm else "unknown",
            "agents": fm.get("agents_used", []) if fm else [],
        })

    limit = args.limit or len(entries)
    for item in entries[:limit]:
        agents_str = ", ".join(item["agents"]) if item["agents"] else "-"
        print(f"[{item['task_type']}] {item['title']}")
        print(f"  {item['dir']}  agents: {agents_str}")


def main():
    parser = argparse.ArgumentParser(description="OmO analysis archival")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # save command
    save_parser = subparsers.add_parser("save", help="Save an analysis")
    save_parser.add_argument("--title", required=True, nargs="+", help="Analysis title")
    save_parser.add_argument("--agents", default=None, help="Comma-separated agent names")
    save_parser.add_argument("--tags", default=None, help="Comma-separated tags")
    save_parser.add_argument(
        "--task-type",
        default="mixed",
        choices=["analysis", "development", "mixed"],
        help="Task type (default: mixed)",
    )
    save_parser.add_argument("--file", required=True, help="Path to analysis body file")

    # list command
    list_parser = subparsers.add_parser("list", help="List saved analyses")
    list_parser.add_argument("--limit", type=int, default=None, help="Max entries to show")

    args = parser.parse_args()

    if args.command == "save":
        cmd_save(args)
    elif args.command == "list":
        cmd_list(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
