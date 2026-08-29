---
name: architect
description: Use when the user wants to build hands-on but by assembling code themselves rather than writing it from a blank file — they want the agent to hand over one function or concept at a time in chat, with explanation, which they then type or paste into the project and merge on their own. Trigger phrases include "give it to me in chunks", "paste it myself", "dump it in chat, I'll merge it", "walk me through it piece by piece", or a stated preference to stay in control of what lands in the file without writing every line from scratch.
---

# Architect

The user assembles the codebase by hand from pieces the agent hands over — the agent never touches the project's files directly. Code is delivered in the chat, one function or concept at a time, and the user is the one who transcribes or pastes it into the real file and merges it with what's already there.

This sits between full from-scratch writing ([[mentor]]) and normal agentic coding. The user isn't deriving syntax from nothing, but they are still reading, understanding, and physically placing every piece — the act of merging is what keeps them the architect of the resulting file, not a bystander approving a diff they didn't read.

## Cycle

1. **Name the chunk.** State what single function, class, or concept comes next, and how it fits into the file as it currently stands (what calls it, what it needs to return, where it belongs).
2. **Deliver the chunk in the chat as text** — a fenced code block the user will copy themselves — never via the Edit or Write tool. The agent does not touch the user's project files in this mode, full stop.
3. **Explain the chunk alongside it**: what each part does, why it's shaped that way, what it depends on, and anything non-obvious about how it fits the surrounding code the user already has.
4. **Stop and wait** for the user to confirm they've merged it in. Do not deliver the next chunk unprompted.
5. **After they confirm**, ask to see the current state of the file (or have them paste it back) and check the merge: right location, no leftover duplicate code, references line up with what actually exists elsewhere in the file.
6. **Report plainly** what this chunk added, what it calls, what calls it, and what's still missing before the file/module is complete.

## Chunk size

Default to the smallest coherent unit — one function, one class, one conditional block — not a whole file at once. A whole file dumped at once collapses this back into normal agentic coding, since the user has no natural pause point to actually read before pasting.

## What this mode does not do

- Does not use Edit/Write on the user's in-progress files — the user is the only one who touches those files in this mode.
- Does not silently expand scope past the named chunk ("while I was at it, also...").
- Does not skip the explanation to save time — the explanation is the point, not overhead around the code.
- Does not move to the next chunk before the current one is confirmed merged.

## Relationship to mentor

Both modes exist to keep the user in command of a codebase instead of trusting an agent's diff sight-unseen. [[mentor]] is stricter: no code changes hands at all, the user derives it. Architect is for when the user wants to move faster than from-scratch recall but still refuses to let code land in their files without personally placing it. Pick per session, or switch mid-session if the user says a chunk is "too much to derive from scratch" — that's a legitimate signal to drop from mentor into architect for that one piece, not a failure.
