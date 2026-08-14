---
name: readback
description: Maintain a user-approved, per-project record of architecture and design changes made during AI-assisted work. Use when an architecture direction, implementation design, or consequential decision is settled, changed, rejected, or implemented, and ask the user before creating a record.
---

# Readback

Readback is the history of how a project's architecture and decisions evolved.
It is not the architecture itself, a changelog, or an automatically written
agent diary. The user controls what becomes part of the record.

## Project layout

Create one record in each independent project:

```text
<project>/.readback/
  index.md
  architecture/
  decisions/
```

`index.md` is the short navigational index. `architecture/` records changes to
system shape, boundaries, contracts, plans, or implementation direction.
`decisions/` records consequential choices between alternatives, including
accepted, reversed, or superseded decisions.

Do not create `log.md`, a shared workspace record, or a global record. Route
the record to the project that owns the decision or changed files.

## Canonical project documents

If the project has `docs/architecture/` and `docs/decisions/`, those remain the
canonical architecture and decision documents. Readback records the evolution
around them and links to them; it must not duplicate their full rationale or
silently replace them.

Use this distinction:

- `docs/architecture/`: what the system is or should be.
- `docs/decisions/`: the durable decision and its rationale.
- `.readback/architecture/`: how the architecture changed during the work.
- `.readback/decisions/`: how a consequential decision was reached.

If no project documentation exists, Readback may still create its own record.
For a consequential decision, recommend a project ADR as well; ask before
creating either record.

## Ask before writing

At each material checkpoint, ask once:

> Log this to Readback — architecture update or decision update?

Write only after the user says yes. Do not infer consent, write automatically,
or ask again about the same checkpoint after a no or no response. Do not log
ordinary edits, typos, formatting, or exploratory discussion that produced no
settled change.

On first use for a project, ask what scope the user wants: from now, important
decisions visible in this conversation, earlier project history, or both. Do
not reconstruct hidden conversation history. If earlier history is requested,
label it as a reconstruction rather than a verbatim transcript.

## One new file per update

Never edit an existing architecture or decision entry. Every approved update
gets a new Markdown file in the appropriate folder. The filename must include
a stable sequence, a short title, and the author suffix:

```text
.readback/architecture/0001-console-boundary-codex.md
.readback/decisions/0002-public-private-split-claude.md
.readback/architecture/0003-tool-surface-user.md
```

Use the actual author identity: `codex`, `claude`, `antigravity`, or `user`,
and add a model qualifier only when useful, such as `codex-gpt5` or
`claude-sonnet`. The author suffix is mandatory so another agent can identify
who made the update.

Each file contains:

```markdown
# 0001 — Short title

Date: YYYY-MM-DD HH:MM
Author: Codex (GPT-5)
Type: architecture | decision
Status: proposed | accepted | superseded | rejected
Related: docs/architecture/17-implementation-plan-current.md

## User said
Verbatim user wording, trimmed only with `...`; redact secrets.

## Decided
What was settled, in plain English.

## Agent suggested
What the agent proposed, if relevant.

## Not taken
Alternatives rejected and why, if relevant.

## Executed
What actually changed, or `Not executed`.

## Files
- path/to/file.md
```

Keep records concise and plain-English. `User said` must be verbatim, while
the other sections may summarize. Use relative paths and never include secrets.

## Update the index

After creating an approved update, append one line to `.readback/index.md`.
The index is the only file that may be edited, and only by appending.

```markdown
# Readback — ASRT

Project: ASRT

## Updates
- 2026-08-14 — Console boundary — architecture/0001-console-boundary-codex.md
- 2026-08-15 — Public/private split — decisions/0002-public-private-split-user.md
```

Before proposing or writing an update, read `index.md` and check the relevant
architecture and decision documents. If the same question returns, mention
whether it is a re-decision, reversal, or repeated proposal and whether new
information changed the outcome.

## Moving projects

Keep `.readback/` inside its project. If a project moves, preserve the record
and append its new origin to `index.md`. Never merge two project records
silently.

Keep `.readback/` out of version control by default because it can contain
private user wording and design history. Tracking it is an explicit user
choice.

## Reference

- `FORMAT.md` — portable file and naming contract
- `examples/` — examples of architecture and decision updates
- `references/drift-patterns.md` — recurring ways a request gets misread
- `references/methods.md` — background and rationale
