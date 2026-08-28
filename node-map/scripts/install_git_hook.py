#!/usr/bin/env python3
"""
Install a post-commit hook that marks a node-map update as pending after each commit.
The hook does NOT generate notes itself (that needs the model) — it only appends the
new commit hash to .nodemap/.pending-map so the next agent session knows work is due.

Usage:
    python install_git_hook.py <project-path>
"""
import os
import sys
import stat

HOOK_TEMPLATE = """#!/bin/sh
# Installed by node-map skill: flags that a map update is due. Does not call any model.
mkdir -p "$(git rev-parse --show-toplevel)/.nodemap"
git rev-parse HEAD >> "$(git rev-parse --show-toplevel)/.nodemap/.pending-map"
"""


def main():
    if len(sys.argv) < 2:
        print("Usage: install_git_hook.py <project-path>", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    git_dir = os.path.join(path, ".git")
    if not os.path.isdir(git_dir):
        print(f"{path} is not a git repo root (no .git/ found). Run this from the repo root.", file=sys.stderr)
        sys.exit(1)

    hooks_dir = os.path.join(git_dir, "hooks")
    os.makedirs(hooks_dir, exist_ok=True)
    hook_path = os.path.join(hooks_dir, "post-commit")

    if os.path.exists(hook_path):
        with open(hook_path) as f:
            existing = f.read()
        if "node-map skill" in existing:
            print("Hook already installed.")
            return
        # append rather than clobber an existing hook
        with open(hook_path, "a") as f:
            f.write("\n" + HOOK_TEMPLATE)
    else:
        with open(hook_path, "w") as f:
            f.write(HOOK_TEMPLATE)

    st = os.stat(hook_path)
    os.chmod(hook_path, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    print(f"Installed post-commit hook at {hook_path}")


if __name__ == "__main__":
    main()
