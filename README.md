# agent-structure (ASA)

**Agent Structure Algorithms** is my personal, daily-use collection of focused skills for creating tools and systems with Codex, Claude Code, Antigravity, or another compatible coding agent.

It gives an agent practical structure at the moments that matter: before acting, when a decision is settled, before calling work complete, and when documenting code for future readers. Start by loading `agent-structure`, then let its focused skills apply when their triggers occur. Try an individual skill when you need it, or use the whole family as a working method.

| Skill | Catches | One-line rule |
|---|---|---|
| **[mandate](mandate/)** - Authority | doing more than was asked | approval covers one thing, one place, once |
| **[readback](readback/)** - Memory | losing why a decision was made | record approved reasoning for later work |
| **[groundtruth](groundtruth/)** - Truth | declaring success without checking | plan on disk, diff checked, claim verified |
| **[commenter](commenter/)** - Clarity | code that hides important context | explain what a reader cannot infer from the code |
| **[node-map](node-map/)** - Structure | re-reading unchanged code every session | one node per file, updated only when the file changes |
| **[mentor](mentor/)** - Recall | the agent quietly doing the coding for you | the user writes every line; the agent explains, assigns, and reviews only |
| **[architect](architect/)** - Assembly | approving a diff you never actually read | the agent hands over one chunk at a time in chat; the user merges it in by hand |

Each skill is an algorithm, not a loose guideline: it has a clear trigger, a focused procedure, and an exit condition. The detailed steps live in each skill's `SKILL.md`; this README is the index.

## Why separate skills, not one big one

Each skill owns a different moment and a different question:

- **mandate** fires before an action: "Did the user actually ask for this, here, now?"
- **readback** fires after a decision: "Will the reasoning behind this still exist in the next session?"
- **groundtruth** fires before a substantial build, publication, or completion claim: "Is the plan written down and has the result been checked against reality?"
- **commenter** fires when code is documented: "Does this explain the intent, contract, and non-obvious behavior at the right detail level?"
- **node-map** fires after a change lands: "Is the structural map of what connects to what still accurate, without re-reading everything?"
- **mentor** fires when the user is deliberately relearning to code by hand: "Am I about to write code the user asked to write themselves?"
- **architect** fires when the user wants to assemble the codebase from agent-provided pieces: "Is this chunk small enough, and explained enough, for the user to place it themselves?"

`mentor` and `architect` are mutually exclusive per chunk of work — pick the one matching how the user wants to build right now, or switch between them mid-session as the difficulty of a given piece warrants. They are independent by design. Install or use the skills you need, but load `agent-structure` when you want the shared working method.

## How they interact in practice

1. `groundtruth` puts a plan in `IMPLEMENTATION_PLAN.md` before a substantial build starts.
2. Work happens. When a design decision is settled, changed, or rejected, `readback` asks whether to preserve the reasoning.
3. If a possible next step reaches beyond what the user requested, `mandate` checks authority before acting.
4. When code needs documentation, `commenter` adds meaningful comments at beginner, intermediate, or advanced detail levels.
5. Before work is called complete, `groundtruth` requires real verification instead of a claim based only on reasoning or passing tests.

The skills do not need direct coordination. Each protects one recurring failure mode, and together they keep long-running agent work deliberate, understandable, and verifiable.

## Use it

Use the normal skill location for your agent, such as `~/.codex/skills/<name>` for Codex or the equivalent skill directory for another compatible tool. The skills use the Agent Skills `SKILL.md` format.
