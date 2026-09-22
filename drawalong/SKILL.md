---
name: drawalong
description: Use when the user wants to understand how a system fits together by drawing it themselves, one piece at a time, in a drawing tool (Excalidraw, draw.io, a whiteboard) while the agent guides. Trigger phrases include "draw it with me", "let's design it in Excalidraw", "one box at a time", "walk me through the architecture so I can draw it", "how does this all connect", or a bare "next" / "done" after the agent has given a drawing piece. Use for flow-shaped systems (things that run in order and pass data between components), not for reading code line by line.
---

# Drawalong

The user draws the system, one piece at a time, in their own drawing tool. The agent is the guide: it investigates the real system first, then dictates the next one to three shapes, with exact text, position and arrows, explains why the piece is shaped that way, and stops. The agent never produces the finished diagram. Drawing it is the exercise.

Reading a finished diagram builds recognition. Placing each box yourself, in the order things actually execute, forces you to decide what connects to what and what travels on each arrow, which builds recall. A whole diagram dumped at once collapses this back into looking at a picture, the same way a whole file dumped at once collapses [[architect]] into normal agentic coding.

## Before piece 1

1. **Investigate the real system, read-only.** Read the code, configs and docs. Verify every claim you are about to have the user draw: grep the call sites, read the imports, run it where possible. A wrong diagram is worse than none, because the user will memorize it. Label what exists today versus what is only proposed. ([[groundtruth]])
2. **Decide the whole sequence privately.** The pieces in execution order, the ownership boundaries, the loops, the failure modes. Announce only a one-line outline ("input, target, tools, recorder, trace, verifier, loop") so the user knows the shape and nothing more.
3. **Give the shape legend once.** Oval is start or end, rectangle is a process or component, cylinder is a store or log, parallelogram is data in flight, diamond is a decision. Every arrow carries a label naming what travels on it. Border style carries ownership: dashed means not ours or external, solid means ours.

## The cycle: one piece per turn

1. **Title:** `Piece N: <what this adds>`.
2. **Drawing instructions, numbered.** For each new shape: the shape type, the exact text inside it, and where it goes relative to what is already on the page. For each arrow: from, to, direction, label. No more than about three new shapes and five arrows per piece.
3. **A small ASCII sketch** of the cumulative picture so far. It is a reference to check against, not something to copy; the user draws in their own tool.
4. **Why it is shaped that way,** two to four short points. Say what the picture cannot show: what breaks if this box were missing, who owns it, and the real file or function it corresponds to, only when that has been verified.
5. **A note to write on the page:** the one-line caveat worth pinning in a corner, such as an invariant or a failure mode.
6. **Close:** "Draw it and say **next**," plus one line naming what the next piece adds. Then stop. Do not deliver the next piece until told.

### A piece, in miniature

> **Piece 3: put a proxy on the wire**
> 1. Delete the two arrows between `SERVICE` and `DATABASE`; move `DATABASE` right.
> 2. In the gap, a small solid rectangle: `PROXY` / `ours`.
> 3. Four arrows: service to proxy `query`, proxy to database `same query`, database to proxy `rows`, proxy to service `same rows`.
> *Why:* the proxy is the only way to see queries from outside; it must never alter them.
> *Write in a corner:* it forwards, it never modifies.
> Draw it and say **next**. Piece 4 is the log the proxy writes to.

## Sequencing rules

- **Follow execution order,** the way data actually flows. Not file order, not alphabetical.
- **Show the "before" and then modify it.** Draw the direct connection first, then cut it and insert the new component. The insertion is the lesson.
- **One system, one canvas.** Do not split it into a separate diagram per flow. Secondary flows branch off shared nodes on the same canvas, or come last as a short second pass if they are genuinely independent.
- **Pick one main direction:** left to right for pipelines, top to bottom for cycles. Loop-back arrows curve around the outside. Leave an arrow dangling on purpose when its destination is not drawn yet, and say so.
- **Ownership first.** Mark external or not-ours boxes dashed from the first piece so the boundary is visible early; add the enclosing boundary boxes near the end.
- **Draw the failure modes,** not just the happy path (an empty log that reads as a pass), and the controls that catch them.

## Handling the user's replies

- **"next" or "done":** deliver the next piece.
- **They describe their drawing or ask "is this right?":** confirm or correct against the real code. If their model differs from the truth, name the exact arrow or box that is wrong and why. If they share a screenshot, read it.
- **They want to change the design:** update the private sequence, tell them what to erase or move, then continue.
- **A question mid-piece:** answer briefly, then resume at the same piece.
- **Dictated or garbled input:** infer the intent; restate it in one line only if it is genuinely ambiguous.

## After the last piece

Recap in one paragraph, then a table mapping each box to its real file or function. Then offer, without doing it unprompted: (a) a line-by-line usage walkthrough mapped to the boxes, showing how a person would actually set the system up and run it, marking what exists today versus what still needs building; (b) a saved copy of the piece sequence in the project's docs.

## What this mode does not do

- Does not dump the whole diagram, or more than one piece at a time.
- Does not create the diagram file or artifact for the user unless explicitly asked.
- Does not draw boxes for things it has not verified exist, and does not present a proposal as if it were built.
- Does not require per-file diagrams. The unit is a piece of one system, not a file.
- Does not write project code. If the user wants to build, hand off to [[mentor]] or [[architect]].

## Relationship to other skills

- [[groundtruth]]: every drawn claim is checked against the real system first, and proposed is labeled apart from existing.
- [[node-map]]: node-map is the agent's persistent structural memory of a codebase; drawalong is the human's structural understanding of it. A finished piece sequence can seed a node-map entry, but neither replaces the other.
- [[mentor]] and [[architect]]: they build code; drawalong builds the mental model that makes the code make sense. The natural order is drawalong first, then build.

## Exit condition

The user can redraw the whole diagram from memory and say, for every arrow, what travels on it.
