# .readback format

> Current contract: use `index.md`, `architecture/`, and `decisions/` under
> `.readback/`. Every user-approved update is a new Markdown file with an
> author suffix (`-codex.md`, `-claude.md`, `-antigravity.md`, or `-user.md`).
> There is no `log.md` and no automatic append. The older material below is
> historical reference and is superseded by `SKILL.md`.

A portable one-page spec. Drop it into any agent tool — Claude Code, Codex,
Antigravity — or paste it into a chat. It is the whole contract.

---

## Layout

One `.readback/` directory per project, at that project's root:

```text
<project>/.readback/
  index.md       identity, move history, one line per entry — always read
  log.md         every entry — never read whole, search it
  decisions/     rare — one file per genuinely consequential decision
    0001-title.md
```

`decisions/` appears only once a decision earns its own file — see below.

**A project is anything that could be moved somewhere else on its own.** A
folder holding several projects is a workspace and gets no record of its own:

```text
ASRT/                      workspace — no record
  promptshields/
    .readback/             its own history
  promptxploit/
    .readback/             its own history, separate
```

Never global. Never shared. Records are never merged across projects.

## Ask, don't infer

At a checkpoint — a new idea, an architecture/design decision made or
reversed, a plan drafted or implemented, an approach rejected, a
misunderstanding corrected, files changed by a decision — **ask the user**
before writing:

> Log this to readback — new idea / architecture change / plan drafted or
> implemented?

Write only on yes. No response or a no means nothing is logged, and the
moment is not asked about again. Never ask about typos or mechanical edits.

## Resolve scope first

Inspect the current workspace before creating a record. If it is one project,
use that project root. If it holds several independent projects, create no
parent record and route by changed-file ownership. If nothing changed or the
structure is unclear, ask which project the decision concerns. An explicit user
statement that a workspace is one project is authoritative.

**Add `.readback/` to `.gitignore` when creating it.** The record quotes the
user verbatim and names decisions and dead ends they did not choose to
publish. Tracking it is an explicit opt-in for private repos or teams that
want the shared history — and when tracked, the whole directory is
publishable text: redacted, home-relative paths only, read through before the
repo goes public.

## Rules

**Append only.** Entries are never edited, reordered, summarized, or deleted.
When something changes, add a new entry saying so. `index.md` is the only
exception: it gains one line per entry, and an `Origins:` line on a move.

**Ask before logging, not after.** See "Ask, don't infer" above — this
replaces silently deciding what counts as a decision.

**Read `index.md` before proposing and before asking to log.** If the
question has come up before, say so in a `**Loop:**` line.

**Route by ownership.** Write to the project owning the changed files. If
nothing changed, the project the decision is about. A decision spanning two
projects gets the full entry in one and a one-line pointer in the other —
never the same entry twice.

## Conversation checkpoint

At the first material interaction for a project in a session, resolve the
capture range before writing any entry:

1. Start from now.
2. Important decisions in this visible conversation.
3. Earlier project history before this record existed.
4. Both earlier history and this visible conversation.

For 2, append one clearly labelled checkpoint in `log.md`. For 3, create the
`Before this record began` reconstruction block before any normal entry. For 4,
create the reconstruction first, then append the checkpoint. Use only visible
conversation, user recollection, and repository evidence. Never invent quotes,
timestamps, decisions, or access to hidden chat history from another tool.

Do not create a normal checkpoint until the range is resolved. Treat "everything
so far" or "the project journey" as option 4. If a normal entry was created
first by mistake, append a `Record correction` entry. Never insert, move,
rewrite, or delete existing history.

## Entry

```markdown
## YYYY-MM-DD HH:MM — Short title

**Agent:** Claude Code (Sonnet 5)

**You:** "the user's exact words, verbatim"

**I suggested:** what the agent proposed, if the user went a different way.

**Decided:** what was settled, in plain English.

**I did:** what was actually executed, or `Not executed`.

**Not taken:** approaches considered and rejected, with the reason.

**Loop:** this came up before — which kind, which entry, what changed since.

Files: path/to/one.ts, path/to/two.md
```

| Field | Required | Rule |
|---|---|---|
| Heading | yes | Date **and** time, plus a short title |
| `**Agent:**` | yes | Which tool and model wrote this entry — e.g. `Claude Code (Sonnet 5)`, `Codex`, `Antigravity (Gemini 3)` — so a later reader can see who made which call, without splitting the file by author |
| `**You:**` | yes | Verbatim. Trim with `...`, never rewrite. Redact secrets as `[redacted]`; rewrite absolute paths containing a username to a home-relative form |
| `**Decided:**` | yes | What was settled, plain English |
| `**I did:**` | yes | What was executed. `Not executed` if the decision stands but no work happened |
| `Files:` | yes | Paths only, no diffs. `Files: none` if nothing changed |
| `**I suggested:**` | when true | The agent proposed something else. Record both |
| `**Not taken:**` | when true | Rejected approaches and why |
| `**Loop:**` | when true | This question recurred — see below |

For a conversation checkpoint, write `**You:** Not a verbatim transcript; visible
conversation checkpoint approved by the user.` Do not turn reconstructed text
into a quote.

Plain English throughout. **No code.** Two to five sentences per field; more
when a decision genuinely warrants it.

## If the project already has its own record

Check for an existing ADR folder, `docs/decisions/`, architecture docs, or a
CHANGELOG before writing. If this decision already has one:

- `**Decided:**` states the outcome in one sentence and stops — do not
  re-narrate reasoning or evidence the source document already holds.
- `Files:` links the source. The link is the detail; don't compress a 50-line
  ADR into a paragraph.
- Only add texture the source is missing: the back-and-forth, a rejected
  alternative it doesn't mention, a loop it doesn't record.

## Rare: a decision earns its own file

Almost everything stays in `log.md`. Give one its own file in `decisions/`
only when it is consequential (changes a boundary, contract, format, or
dependency), contested (real alternatives were weighed), and likely to be
cited by number later — and the project doesn't already have an ADR for it.
A project with a decision file per one-paragraph call has miscalibrated this.

A `log.md` entry is small on purpose: two to five sentences a field, cheap
because it fires often. A `decisions/` file has no such limit — write it at
the length the reasoning actually needs.

Files are `.readback/decisions/NNNN-short-title.md`, sequential, never
reused or renumbered. Same fields as a log entry, under a title heading:

```markdown
# 0004 — Short title

Date: YYYY-MM-DD
Status: accepted | superseded
Supersedes: —

**Agent:** Claude Code (Sonnet 5)
**You:** "verbatim"
**I suggested:** if the user went another way.
**Decided:** what was settled.
**I did:** what was executed, or `Not executed`.
**Not taken:** rejected approaches and why.
**Loop:** if this recurred.

Files: path/one.ts
```

Index lines for a decision file point at it: `2026-08-04 — Title →
decisions/0004-title.md`. To promote a routine log entry later, add a new
decision file and append `Promoted: see decisions/000N-title.md` to the
original log entry — never move or delete it. Decision files are append-only
like everything else: a correction is a new superseding file or a dated
addendum at the bottom, never an edit to existing text.

## Loops

The same decision made twice, a proposal ignored and resurfacing, a settled
question reopened. Name the kind, the prior entry, and **whether anything
actually changed**:

```markdown
**Loop:** re-decided, 2nd time — see 2026-08-03 17:55. Same outcome both
times, nothing new. The pull toward splitting returns whenever the file
looks long.
```

| Kind | |
|---|---|
| `re-decided` | Same question, same answer, twice |
| `reversed` | Decided A, now B — legitimate only if something changed |
| `oscillation` | A, then B, then A again |
| `ignored` | Proposed, passed over, resurfaced later |
| `re-derived` | Worked out a second time because it was never recorded |

A reversal with new information is learning; a reversal with nothing new is a
loop. They look identical unless the entry says which — so always state what
changed, or state plainly that nothing did.

Only what was written down can be detected. Find them by searching `log.md`
for `Loop:`.

## Moving and inheriting

`Project:` is a stable name, not a path — two records with the same `Project:`
are the same lineage no matter where either has moved. `Origins:` is
append-only: add a line when a move is observed, never rewrite the list.

- **Project moved** — the record travels inside it. Append an `Origins:` line.
- **Files arrived from another project** — append an entry pointing at their
  prior history. Never copy it; a pointer stays true, a copy goes stale.
- **Project split** — each new record names the shared parent in `Origins:`.
  Do not divide the old history; both descend from all of it.
- **Two records, same `Project:`** — neither is authoritative. Show the user
  both. Never merge silently.

Nothing here discovers a lost record by itself. Within a repo,
`git log --follow` traces a moved file; across drives, only the user knows.

## Growth

Past ~300 entries, roll `log.md` by year into `.readback/YYYY.md`. Move entries
whole, never summarize. `index.md` is never split.

## Portability

The skill contract — `name` and `description` frontmatter — is identical in
Claude Code, Codex, Copilot, and Cline. Only the install path and invocation
prefix differ. Keep the record free of tool-specific and shell-specific
assumptions: say "search the file", not `grep`.

---

## Skeletons for a new project

`.readback/index.md`:

```markdown
# Readback — <project>

How the ideas in this project changed, in order. Append only — entries are
never edited or removed, including wrong ones. Logged only when the user says
yes at a checkpoint, never inferred.

Project: <stable name, not a path>
Origins:
- YYYY-MM-DD HH:MM — <path> (created)

Entries are in `log.md`. Format: `## date time — title`, then **Agent:**
(tool + model), **You:** (verbatim), optional **I suggested:**, then
**Decided:**, **I did:**, optional **Not taken:** and **Loop:**, then
`Files:`. Plain English, no code.

## Index
```

`.readback/log.md`:

```markdown
# Readback log — <project>

Append only. Newest at the bottom. See `index.md` for the format and index.

---
```

The skeletons are deliberately self-describing: any tool opening them can
continue correctly without this spec.
