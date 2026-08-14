# Example — an idea that became five things

What several months of evolution looks like in one record. Seeded from a
project's history as described in conversation, not from real contemporaneous
entries — the point is the shape, not the content.

This is the case the tool exists for: an idea that became five different
things, where no single session contains the reasoning and the context window
that held it is long gone.

---

## The arc, read from `index.md` alone

Reading only the titles, in order, gives the whole story in thirty seconds:

```markdown
Project: ASRT
Origins:
- 2026-03-02 09:15 — ~/ASRT (created)

## Index
- 2026-03-14 11:20 — Attacker becomes a defense
- 2026-04-02 09:40 — Defense becomes a regression harness
- 2026-05-11 16:05 — Attacker returns, this time as an LLM
- 2026-06-19 15:10 — Judge module removed, agent TKI only
```

```
attacker tool
  -> prompt shield / defense
    -> regression tool
      -> LLM attacker + regression
        -> agent TKI only, judge removed
```

Five identities. Each step made sense at the time. By step five the original
goal has inverted — it started as something that attacks and ended as
something that evaluates.

That inversion is invisible from `git log`, invisible from the current
codebase, and invisible from any single conversation. It is only visible from
a record appended to at each turn.

---

## What one entry carries, in `log.md`

```markdown
## 2026-03-14 11:20 — Attacker becomes a defense

**You:** "<what was actually said, verbatim>"

**I suggested:** keeping both in one tool, with a flag to switch modes.

**Decided:** the shield is the product; the attacker becomes its test
harness. The attacker kept producing prompts nothing could score, so the
useful half turned out to be the filter written to evaluate them.

**I did:** src/attack/generator.py, src/shield/filter.py, commit 4a1c9de

**Not taken:** one binary serving both goals — two purposes in one interface
meant neither got a clear contract.

Files: src/attack/generator.py, src/shield/filter.py
```

The `Files:` line is what makes this findable later. Searching `log.md` for
`shield/filter` returns every decision that ever touched it, in order, with
the reasoning in plain English attached.

---

## Why the abandoned steps stay

Entries are never removed, so a step later reversed stays exactly as written.

Six months on, the question is rarely *what is this now* — the code answers
that. It is **why did we leave the previous approach**, and **is that reason
still true**.

The regression tool was dropped for a reason recorded at the time. If that
reason no longer holds, it comes back. Had the entry been tidied away during a
cleanup, the decision would have to be re-derived from nothing.

---

## What a loop looks like at this scale

```markdown
**Loop:** oscillation, 3rd time on whether the judge belongs in-process.
2026-04-02 in-process, 2026-05-11 separated, now in-process again. This time
latency was measured rather than assumed, so the reversal is settled rather
than another swing.
```

Three entries spread across ten weeks. Nobody remembers that pattern
unprompted — the record does.
