# agent-structure


**A**gent **S**tructure **A**lgorithms - a set of skills for making your agentic AI work algorithmically structured.


Working with an AI agent for real, over weeks, fails in ways a permission system and a green test suite don't catch. Not because the agent is malicious — because its defaults trend toward the cheaper version of events: do a bit more than was asked, forget why an earlier decision was made, declare something done because it compiled. Each skill in this family exists to catch one of those defaults, at the exact moment it happens. New failure modes get their own skill and a new row below, same as any other library grows.

| Skill | Catches | One-line rule |
|---|---|---|
| **[mandate](mandate/)** — Authority | doing more than was asked | approval covers one thing, one place, once |
| **[readback](readback/)** — Memory | losing why a decision was made | append-only record, written only when the user says yes |
| **[groundtruth](groundtruth/)** — Truth | declaring success without checking | plan on disk, diff checked, claim verified |

Each row is an algorithm, not a loose guideline — a fixed trigger, a fixed procedure, a fixed exit condition. The steps live in each skill's own `SKILL.md`; this table is the index, not a copy of them.

## Why separate skills, not one big one

Each covers a different moment and a different question:

- **mandate** fires *before* an action — "did the user actually ask for this, here, now?"
- **readback** fires *after* a decision — "is the reasoning behind this written down anywhere?"
- **groundtruth** fires at build, publish, and done — "is the plan on disk, is the diff clean, was this actually checked?"

They're independent on purpose. A project can install any subset — none of them depends on another being present. They're documented together because they share a root cause, not a codebase: an agent's default is the path of least resistance, and each skill is a specific, narrow push back against one version of that default.

## Install

Each is its own skill, installed the normal way:

```bash
git clone https://github.com/<you>/mandate     ~/.claude/skills/mandate
git clone https://github.com/<you>/readback    ~/.claude/skills/readback
git clone https://github.com/<you>/groundtruth ~/.claude/skills/groundtruth
```

Same layout for Codex (`~/.codex/skills/<name>`) or any tool that reads the Agent Skills format — the `name`/`description` frontmatter contract is identical across tools; only the install path differs.

## How they interact in practice

A typical build touches several of these without any explicit hand-off:

1. **groundtruth (build-plan)** — before real work starts, the plan lands in `IMPLEMENTATION_PLAN.md`, not just chat.
2. Work happens. A decision gets made, reversed, or an approach gets rejected —
3. **readback** asks: *"log this?"* On yes, it's appended, verbatim, with which agent wrote it.
4. Partway through, a next step outside what was actually asked comes up (touch another project, push, rewrite history) —
5. **mandate** stops and asks first: one sentence, what it needs, why.
6. Work looks finished —
7. **groundtruth (reality-check)** asks whether this was actually run against something real before the claim is made, and **groundtruth (publish-check)** scans the diff before it goes anywhere public.

None of them talk to each other directly. Each just owns its one moment, and between them, most of the ordinary ways an agent quietly goes wrong have something watching.


## License


MIT 
