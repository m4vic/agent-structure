---
name: agent-structure
description: Use at the start of substantial agentic AI work, including multi-step builds, redesigns, and new features, to apply structured skills for authority, memory, verification, and code-documentation clarity.
---

# agent-structure (ASA)

Agent Structure Algorithms is a personal, practical set of skills for working with AI coding agents in a structured way. Use it while creating tools and systems with Codex, Claude Code, Antigravity, or another compatible agent.

An agent's default, left alone, is the path of least resistance: act a little beyond what was actually asked, let the reasoning behind a decision disappear once the conversation moves on, declare something done because it compiled, or add code comments that merely repeat the code. ASA applies a focused skill at each of those moments.

1. **[mandate](mandate/)** - Authority. Before acting: is this what was actually asked, here, in this project, right now, or does it only follow from what was asked?
2. **[readback](readback/)** - Memory. When a decision is made, changed, or reversed: is the reasoning written down for future work?
3. **[groundtruth](groundtruth/)** - Truth. Before starting real work, before publishing, and before claiming done: is the plan on disk, is the diff clean, and was this actually verified?
4. **[commenter](commenter/)** - Clarity. When code needs documentation: does it explain what a future reader cannot infer from the code, at the detail level they need?

## How to use this

At the start of real agentic work, load this skill first. It does not replace the individual skills; each keeps its own `SKILL.md` with the detailed procedure. This is the orientation that says: these apply here, work this way.

Let each skill fire on its own trigger:

- A scope or authority question invokes `mandate`.
- A settled or changed decision invokes `readback`.
- A substantial build, publish action, or completion claim invokes `groundtruth`.
- A request to add, improve, or review code comments invokes `commenter`.

More skills can be added in the same way: a recurring failure mode earns a focused algorithm with a clear trigger and exit condition.

## Related

- [mandate](mandate/) - Authority
- [readback](readback/) - Memory
- [groundtruth](groundtruth/) - Truth
- [commenter](commenter/) - Clarity
