# Readback

> Current design: Readback is a user-approved, per-project record with
> `.readback/index.md`, `.readback/architecture/`, and `.readback/decisions/`.
> Every update is a new author-suffixed Markdown file. There is no automatic
> `log.md` append. See `SKILL.md` for the active contract; older examples below
> are historical.

**A map of how your ideas changed.**

Not documentation. Not a changelog. A running record of what you decided, what the agent suggested, what you chose instead, and why it changed — appended as you work, in plain English.

The name is from aviation, where a pilot repeats a clearance back so a misunderstanding is caught before it is acted on.

## The problem

You work with an agent for weeks. The idea moves — an attacker tool becomes a defense, becomes a regression harness, becomes something else again. Every step made sense at the time.

Then you look back and cannot reconstruct any of it. The context window that held the reasoning is gone, and a long one is unreadable even before it's compacted. `git log` shows what changed, never why you changed your mind. The decision to abandon the previous approach — the one you now need to re-evaluate — exists nowhere.

## What it does

One `.readback/` directory per project. The agent appends to it as you work. You never write in it.

```text
<project>/.readback/
  index.md    identity, move history, one line per entry — always read
  log.md      the entries — never read whole
```

**One per project, never global.** A project is anything that could be moved somewhere else on its own; a folder holding several projects is a workspace and gets no record:

```text
rootfolder/                      workspace — no record
  folderB/
    .readback/             its own history
  folderB/
    .readback/             its own history, separate
```

Talk about promptshields and it appends there. Talk about promptxploit and it appends there. They never merge, and either can be moved out without losing its past.

```markdown
## 2026-08-03 17:55 — Cut to one append-only file

**You:** "we have to... just append it. Nothing else in the format. Same format
should be managed by all agent tools... just smooth and not much more."

**I suggested:** optional verification fields for ideas that reached code, and
two entry types — a light one and a heavy one.

**Decided:** one entry type, no optional fields. Every optional field is a
choice to make before writing, and that is what kills the habit.

**I did:** cut SKILL.md from 12.5KB to 4.6KB. Removed the status taxonomy,
match values, and the three-file layout.

Files: readback/SKILL.md, readback/FORMAT.md
```

**You** and **I** stay separate, so you can see what you asked for next to what actually got built. `**I did:** Not executed` covers a decision that hasn't been acted on yet. An optional `**Not taken:**` keeps the approaches that lost.

## It catches loops

The same decision made twice. An idea you passed over without comment, which quietly died and resurfaced a month later. A settled question reopened because nobody remembered settling it. This is invisible from inside a conversation and expensive over months.

Before proposing anything, and again before appending, the agent checks the index. When a question has come up before, the entry says so:

```markdown
**Loop:** re-decided, 2nd time — see 2026-08-03 17:55. Same question, same
outcome, nothing new either time. The pull toward splitting comes back
whenever the file starts to look long.
```

Five kinds: `re-decided`, `reversed`, `oscillation`, `ignored`, `re-derived`.

The line that carries the meaning is **whether anything actually changed**. A reversal with new information is learning; a reversal with nothing new is a loop. They look identical in the file unless the entry says which — so it always says which, including when the answer is "nothing changed."

## Four rules

**Append only.** Entries are never edited, reordered, summarized, or deleted — not even wrong ones. When something changes, the next entry says so. An idea that was right in March and wrong in July is only visible if both entries survive untouched. The index at the top is the single exception.

**Decisions only.** Talking is not deciding. Exploring options and thinking out loud produce no entry — the file waits until something is settled, then records how it was settled. This is what keeps it short enough to read.

**Plain English, no code.** If an entry needs code to make sense, it's written wrong. You should be able to read the file in six months without the conversation around it.

**Your words, verbatim.** Quotes are not cleaned up or condensed. A paraphrase replaces what you meant with what the agent understood, which is the exact thing this file exists to catch.

## The index

`index.md` carries one line per entry. Reading only the titles, in order, gives the whole arc of an idea in about thirty seconds:

```markdown
## Index
- 2026-03-14 11:20 — Attacker tool becomes a defense
- 2026-04-02 09:40 — Defense becomes a regression harness
- 2026-06-19 15:10 — Judge module removed, agent TKI only
```

That is the view that makes a long history usable. Past ~300 entries `log.md` rolls by year into `.readback/YYYY.md` — entries move whole, never summarized, and `index.md` is never split.

## Moving projects

`index.md` carries a `Project:` name and an append-only `Origins:` list of every path the project has lived at. Identity travels with the record, not with the path — two records naming the same `Project:` are the same lineage no matter where either ended up.

Move a project and its `.readback/` goes with it. Pull files in from another project and the record gets a *pointer* to their prior history rather than a copy, because a pointer stays true as the source keeps changing. Split a project and both halves name the shared parent.

What it will not do is hunt the filesystem for a record you lost. Inside a repo `git log --follow` traces a moved file; across drives, only you know — so it records the move when you mention it.

## Same format in every tool

Claude Code, Codex, Antigravity — same file, same format, no per-tool sections. [`FORMAT.md`](FORMAT.md) is a portable one-page spec you can drop into any of them, and the file's own header is self-describing enough that a model can continue it correctly without the skill loaded.

## Install

```bash
# Claude Code
git clone https://github.com/<you>/readback ~/.claude/skills/readback

# Codex
git clone https://github.com/<you>/readback ~/.codex/skills/readback
```

Then just work. The skill triggers on decisions and corrections. `/readback` or `$readback` to invoke it directly.

## Reading it back

Read `index.md` in full — it stays short. Never read `log.md` whole, it only grows. Search it instead:

```bash
grep -n "queue"       .readback/log.md    # everything about a topic
grep -n "src/jobs.ts" .readback/log.md    # history of one file
tail -40              .readback/log.md    # what happened recently
```

On Windows PowerShell, `Select-String -Path .readback/log.md -Pattern "queue"`.

Because every entry carries its `Files:` line, searching for a path returns every decision that ever touched it, in order, with the reasoning attached.

## Related

- [mandate](../mandate/) — authority: did the user actually ask for this, here, now
- [groundtruth](../groundtruth/) — truth: is the plan on disk, is the diff clean, is the claim verified
- [agent-structure](../) — mandate, readback, and groundtruth as one family: Authority, Memory, Truth

## Reference

- [`FORMAT.md`](FORMAT.md) — the portable spec and file skeletons
- [`.readback/`](.readback/) — this project's own record, kept by the skill itself
- [`examples/long-arc.md`](examples/long-arc.md) — what months of drift looks like
- [`references/drift-patterns.md`](references/drift-patterns.md) — recurring ways a request gets misread
- [`references/methods.md`](references/methods.md) — what this borrows from, and what it deliberately refused

## License

MIT
