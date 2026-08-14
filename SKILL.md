---
name: agent-structure
description: Use at the start of any substantial agentic AI work — a new feature, a multi-step build, a redesign, anything beyond a couple of trivial edits — to work in a structured, algorithmic way instead of an ad-hoc one. Also use when asked what the working methodology is, how an agent should approach a task, or how to keep agentic AI work from drifting.
---

# agent-structure (ASA)

Agent Structure Algorithms — working with an AI agent, structured.

An agent's default, left alone, is the path of least resistance: act a little beyond what was actually asked, let the reasoning behind a decision evaporate once the conversation moves on, declare something done because it compiled. None of this is malicious — it's just what happens without something pushing back.

agent-structure is the discipline of applying specific algorithms at the moments they matter, instead of working ad hoc. Each one is its own skill, with its own trigger and its own procedure — this skill is what ties them together and puts them to use as one working method:

1. **[mandate](mandate/)** — Authority. Before acting: is this what was actually asked, here, in this project, right now, or does it only follow from what was asked?
2. **[readback](readback/)** — Memory. When a decision is made, changed, or reversed: does the reasoning behind it get written down, or does it exist only in a context window that will eventually roll away?
3. **[groundtruth](groundtruth/)** — Truth. Before starting real work, before publishing, before claiming done: is the plan on disk, is the diff clean, was this actually verified against something real?

More get added the same way — a new failure mode earns its own algorithm and a line here, not a rewrite of this file.

## How to use this

At the start of real agentic work, load this skill first. It doesn't replace the other three — each keeps its own `SKILL.md` with the actual step-by-step procedure — it's the orientation that says *these apply here, work this way*. From there, let each individual skill fire on its own trigger as the relevant moment arrives: a scope question invokes mandate, a settled decision invokes readback, a claim of success invokes groundtruth.

Think of it the way "DSA" implies algorithms without spelling them out every time: agent-structure is the name for working this way; the mechanics live one level down, in each skill's own file.

## Related

- [mandate](mandate/) — Authority
- [readback](readback/) — Memory
- [groundtruth](groundtruth/) — Truth
