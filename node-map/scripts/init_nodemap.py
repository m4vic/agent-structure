#!/usr/bin/env python3
"""
Bootstrap .nodemap/ for a workspace root: one nodemap.json listing each top-level
project folder, and an empty node file per project for the model to fill in.

Usage:
    python init_nodemap.py <workspace-root>

This does NOT read or summarize any code — it only scaffolds the files. The skill
(the model reading SKILL.md) is responsible for filling in summaries, exports, and
calls_out_to by actually reading each project's files, since that step needs
understanding, not just file listing.
"""
import json
import os
import sys
import subprocess
from datetime import datetime, timezone

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build", ".nodemap"}


def git_head(path):
    r = subprocess.run(["git", "-C", path, "rev-parse", "HEAD"], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def find_projects(root):
    """Top-level folders under root that look like projects (skip dotfiles/hidden/skip-list)."""
    projects = []
    for entry in sorted(os.listdir(root)):
        full = os.path.join(root, entry)
        if not os.path.isdir(full):
            continue
        if entry in SKIP_DIRS or entry.startswith("."):
            continue
        projects.append(entry)
    return projects


def main():
    if len(sys.argv) < 2:
        print("Usage: init_nodemap.py <workspace-root>", file=sys.stderr)
        sys.exit(1)

    root = os.path.abspath(sys.argv[1])
    nodemap_dir = os.path.join(root, ".nodemap")
    nodes_dir = os.path.join(nodemap_dir, "nodes")
    os.makedirs(nodes_dir, exist_ok=True)

    nodemap_path = os.path.join(nodemap_dir, "nodemap.json")
    if os.path.exists(nodemap_path):
        print(f"Already exists: {nodemap_path} — not overwriting. Delete it first if you want a clean rebuild.")
        sys.exit(0)

    projects = find_projects(root)
    if not projects:
        # single-project repo case: treat root itself as the one project
        projects = [os.path.basename(root.rstrip("/")) or "root"]
        project_paths = {projects[0]: "."}
    else:
        project_paths = {p: p + "/" for p in projects}

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    nodemap = {"version": 1, "last_updated": now, "projects": []}

    for proj in projects:
        proj_path = os.path.join(root, project_paths[proj]) if project_paths[proj] != "." else root
        head = git_head(proj_path) or git_head(root)
        node_file_rel = f"nodes/{proj}.node.json"
        nodemap["projects"].append({
            "id": proj,
            "path": project_paths[proj],
            "summary": "",  # to be filled in by the model after reading the project
            "connects_to": [],
            "node_file": node_file_rel,
            "last_mapped_commit": None
        })
        node_file_full = os.path.join(nodemap_dir, node_file_rel)
        if not os.path.exists(node_file_full):
            with open(node_file_full, "w") as f:
                json.dump({"project": proj, "files": {}, "history": []}, f, indent=2)

    with open(nodemap_path, "w") as f:
        json.dump(nodemap, f, indent=2)

    print(f"Initialized {nodemap_path} with {len(projects)} project(s): {', '.join(projects)}")
    print("Next: read each project's files and fill in summaries/exports/calls_out_to per SKILL.md.")


if __name__ == "__main__":
    main()
