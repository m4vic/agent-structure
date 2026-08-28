#!/usr/bin/env python3
"""
List files changed since a given commit, so node-map only re-reads what actually changed.

Usage:
    python git_changes.py <project-path> [last-commit-hash]

Behavior:
    - If <project-path> is a git repo and last-commit-hash is given and valid:
        prints files changed between last-commit-hash and HEAD (added/modified/deleted),
        plus the new HEAD hash on the last line as "HEAD:<hash>".
    - If <project-path> is a git repo but no valid last-commit-hash is given:
        prints every tracked file (first-run bootstrap case), plus "HEAD:<hash>".
    - If <project-path> is NOT a git repo:
        prints every file (respecting a .gitignore-like skip list if present) with a
        content hash for each, so the caller can do hash-based staleness checks instead
        of commit-based ones. Prints "HEAD:none" on the last line.

Output format (one per line, until the final HEAD line):
    <status>\t<path>
where status is A (added), M (modified), D (deleted), or ? (no-git content listing).
"""
import subprocess
import sys
import os
import hashlib

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build", ".nodemap"}


def is_git_repo(path):
    return subprocess.run(
        ["git", "-C", path, "rev-parse", "--is-inside-work-tree"],
        capture_output=True, text=True
    ).returncode == 0


def git_head(path):
    r = subprocess.run(["git", "-C", path, "rev-parse", "HEAD"], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def commit_exists(path, commit):
    r = subprocess.run(["git", "-C", path, "cat-file", "-e", commit + "^{commit}"], capture_output=True, text=True)
    return r.returncode == 0


def git_diff_since(path, last_commit):
    r = subprocess.run(
        ["git", "-C", path, "diff", "--name-status", f"{last_commit}..HEAD"],
        capture_output=True, text=True
    )
    lines = []
    for line in r.stdout.strip().splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        status, filepath = parts[0][0], parts[-1]  # collapse R100 etc. to first letter
        lines.append((status, filepath))
    return lines


def git_ls_files(path):
    r = subprocess.run(["git", "-C", path, "ls-files"], capture_output=True, text=True)
    return [("A", f) for f in r.stdout.strip().splitlines() if f.strip()]


def hash_file(fullpath):
    h = hashlib.sha1()
    try:
        with open(fullpath, "rb") as f:
            while chunk := f.read(65536):
                h.update(chunk)
        return "sha1:" + h.hexdigest()[:12]
    except OSError:
        return "sha1:unreadable"


def walk_no_git(path):
    out = []
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith(".")]
        for fname in files:
            full = os.path.join(root, fname)
            rel = os.path.relpath(full, path)
            out.append(("?", rel, hash_file(full)))
    return out


def main():
    if len(sys.argv) < 2:
        print("Usage: git_changes.py <project-path> [last-commit-hash]", file=sys.stderr)
        sys.exit(1)

    path = sys.argv[1]
    last_commit = sys.argv[2] if len(sys.argv) > 2 else None

    if is_git_repo(path):
        head = git_head(path)
        if last_commit and commit_exists(path, last_commit):
            changes = git_diff_since(path, last_commit)
        else:
            changes = git_ls_files(path)
        for status, filepath in changes:
            print(f"{status}\t{filepath}")
        print(f"HEAD:{head}")
    else:
        for status, filepath, filehash in walk_no_git(path):
            print(f"{status}\t{filepath}\t{filehash}")
        print("HEAD:none")


if __name__ == "__main__":
    main()
