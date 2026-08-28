---
name: node-map
description: Maintains a persistent, append-only knowledge graph of a codebase — one root index plus one node file per project/folder — so future sessions read a compact map instead of re-reading source code. Use this skill whenever an architectural decision is actually implemented (code committed or files changed after a design decision), when the user runs git commit in a mapped workspace, when the user asks to "map", "index", "graph", or "node" a codebase, when starting work in a workspace that already has a nodemap.json, or alongside readback/ground-truth/mandate/commenter as part of an agent-structure workflow. Trigger proactively after any multi-file change lands — don't wait to be asked. Also use when the user wants to know "what connects to what", "what does this file do", or wants a lightweight structural map instead of a full graph tool.
---

# Node Map

A structural memory layer, sibling to **readback** (decision memory), **ground-truth** (verifies claims), **mandate** (scope discipline), and **commenter** (inline documentation). Where readback records *why a decision was made*, node-map records *what the code is and how it connects* — written once per file, updated only when that file actually changes, read cheaply from then on.

## Core principle

**Read once, append, never re-read unless stale.** A file gets a full read exactly once (or again only if its content hash changed since the last map). The output is a short structured note. All future questions about that file are answered from the note. This is the same economy readback applies to decisions — don't re-derive what's already been recorded.

There is deliberately no separate LLM API call in this skill. The model reading this SKILL.md *is* the reader — it already has full understanding of the code in front of it mid-session, so writing the note is nearly free at that point. A second, independent LLM call to summarize the same code (the way some external graph tools do it) would be redundant cost for no extra accuracy. Cheap structural signals (imports, function/class names, git diff scope) come from grep/git, not from a parser or a second model.

## File layout

```
<workspace-root>/
├── .nodemap/
│   ├── nodemap.json          # root index — one line per project/folder, always read first
│   └── nodes/
│       ├── <project-a>.node.json
│       ├── <project-b>.node.json
│       └── ...
```

One `.nodemap/` per workspace root (the folder containing multiple projects), not per project. If the user is inside a single-project repo with no siblings, still create `.nodemap/` at that repo's root and one node file for it.

### `nodemap.json` (root index — keep this tiny, always read in full)

```json
{
  "version": 1,
  "last_updated": "2026-08-27T10:00:00Z",
  "projects": [
    {
      "id": "auth-service",
      "path": "auth-service/",
      "summary": "Login, sessions, token refresh. Talks to billing and users.",
      "connects_to": ["billing-service", "users-service"],
      "node_file": "nodes/auth-service.node.json",
      "last_mapped_commit": "a1b2c3d"
    }
  ]
}
```

### `nodes/<project>.node.json` (per-project detail — read only when that project is relevant)

```json
{
  "project": "auth-service",
  "files": {
    "src/login.py": {
      "purpose": "Password + OAuth login, issues session tokens",
      "exports": ["login_user", "verify_token"],
      "calls_out_to": ["billing.check_subscription", "users.get_profile"],
      "called_by": ["api/routes.py"],
      "source_hash": "sha1:9f8e7d...",
      "last_mapped_commit": "a1b2c3d",
      "mapped_at": "2026-08-27T10:00:00Z",
      "note": "Token refresh rewritten 2026-08-15 to fix race condition — see readback #47"
    }
  },
  "history": [
    {"commit": "a1b2c3d", "at": "2026-08-27T10:00:00Z", "files_updated": ["src/login.py"], "reason": "auto: architectural decision executed"}
  ]
}
```

`history` is append-only — never delete or overwrite past entries, same convention as readback. This is what lets you (or Ground Truth) later ask "did this file's mapped behavior actually match what changed?"

Cross-reference readback: when a file's note relates to a past decision, cite the readback entry id/number rather than repeating the reasoning. Keeps the two systems from duplicating content.

## When to run

**1. After an architectural decision is executed, not just decided.** Mandate and readback typically fire around decisions; node-map fires after the resulting code change actually lands (files written, commit made). Don't map a plan — map what shipped.

**2. On `git commit` in a mapped workspace.** If a git post-commit hook is installed (see below), this triggers automatically. If not, and the user just committed, offer to run it or run it as part of finishing the task.

**3. On explicit request** — "map this", "update the node graph", "what does auth connect to", "index this workspace".

**4. First time in a new workspace** — if no `.nodemap/` exists and the workspace clearly has multiple projects or non-trivial structure, offer to initialize it rather than silently skipping.

## Workflow

### First run in a workspace (bootstrap)

1. Run `scripts/init_nodemap.py <workspace-root>` — creates `.nodemap/nodemap.json` with one entry per top-level project folder (summary left empty) and empty `nodes/*.node.json` for each.
2. For each project, read its files (respecting `.gitignore`; skip generated/vendored dirs) and fill in the node file: purpose, exports, calls_out_to per file. Use judgment on depth — a 3000-line config file gets one summary line, not 3000 lines of notes.
3. Fill in each project's one-line `summary` and `connects_to` in the root index once its node file is done.
4. Record the current git commit hash as `last_mapped_commit`.

This first pass is the expensive one — it's the "read once" cost. Everything after is incremental.

### Incremental update (the common case)

1. Read `.nodemap/nodemap.json`. For the project(s) touched by the current task, get `last_mapped_commit`.
2. Run `scripts/git_changes.py <project-path> <last_mapped_commit>` to get the list of files changed since that commit (falls back to listing all tracked files if there's no prior commit recorded, or if the path isn't a git repo — see script notes).
3. For each changed file: read it, update its entry in the node file (purpose/exports/calls_out_to/source_hash/note). If a file was deleted, remove its entry. If a file's actual behavior contradicts its old note, that's a Ground-Truth-relevant signal — flag it in the note rather than silently overwriting the discrepancy.
4. Append one `history` entry summarizing what changed and why (one line — cite the readback entry if this came from a specific decision).
5. Update the root index: bump `last_mapped_commit`, refresh the project's one-line `summary` only if it materially changed, refresh `connects_to` if new cross-project calls appeared.
6. Do **not** re-read or re-summarize files that didn't change. This is the entire point.

### Answering a question using the map

1. Read `nodemap.json` first — always, it's small.
2. Identify which project(s) the question concerns.
3. Read only that project's `.node.json`.
4. If the note fully answers the question, answer from it — don't open the source file.
5. If the note is insufficient or `source_hash` looks stale relative to what you can see in the repo, say so and read the actual file, then update the note while you're there. Never guess past what the note says.

## Git integration

To make this fire automatically instead of relying on being asked, install a lightweight post-commit hook that just leaves a marker — it does **not** try to generate notes itself (that needs the model), it only flags that a map update is due:

```bash
python scripts/install_git_hook.py <project-path>
```

This writes a `.git/hooks/post-commit` that appends the new commit hash to `.nodemap/.pending-map`. The next time this skill is invoked in that workspace (including proactively, per the trigger above), check for `.nodemap/.pending-map`; if present and non-empty, treat every listed commit as "changes since last map" and run the incremental update workflow, then clear the pending file.

If the user explicitly wants a standalone CLI (not tied to an agent session) that walks git history and writes notes without any model in the loop: be upfront that this can only capture what's mechanically extractable — commit messages, diff stats, changed function/class names via simple grep — not genuine "what does this do and why" understanding. Offer `scripts/git_changes.py` as that building block, but recommend it feed into a Claude session (this skill) rather than trying to fully replace the model, since the whole value of this system over grep or Graphify's tree-sitter approach is the semantic note, not the file list.

## Relationship to Graphify-style tools

This skill is intentionally lighter than a full AST-based knowledge graph (e.g. Graphify): no dependency, no parser, no separate LLM API cost, human-readable JSON you can read directly. Trade-off: cross-file edges (`calls_out_to`) are written by the model's judgment while reading the file, not resolved by a compiler-grade parser, so treat them as "best effort" rather than exhaustive. If a workspace is large enough that this matters (thousands of files, need for exhaustive call-graph accuracy), say so and point to Graphify or an AST tool as the better fit — this skill is for keeping a working map fresh during normal agent-assisted development, not for exhaustive static analysis.

## Notes

- Keep every note terse — a few lines per file. The map's value is being cheap to read; a bloated node file defeats the purpose.
- Never fabricate `calls_out_to` or `exports` — if unsure after reading, omit rather than guess.
- If asked to map a workspace with no git repo, skip the git-hash tracking (`last_mapped_commit`/`source_hash` become content hashes instead — `scripts/git_changes.py` handles this fallback) but keep everything else the same.
