# groundtruth

**The counter-pressure to an agent's default optimism.**

Left alone, an agent takes the path of least resistance at three specific moments: it keeps a plan in the chat instead of writing it down, it pushes a commit without checking what's actually in it, and it declares something done because the tests are green rather than because it ran against something real. None of these are dishonesty — they're just what happens by default, every time, unless something pushes back.

groundtruth is that push-back, bundled as one skill with three routes.

## The three routes

**build-plan** — before starting real implementation work, the plan goes into a file (`IMPLEMENTATION_PLAN.md` or equivalent) in the project, not just the chat transcript. A plan that only exists as scrollback is invisible to the next session, the next agent, or a teammate picking up the work.

**publish-check** — before a push, a PR, or making a repo public, scan what's actually about to leave the machine: leaked keys and tokens, absolute paths with a username, internal hostnames, `.gitignore` gaps, and — on a first public push — history, not just the current diff. Report findings; never silently strip or rewrite.

**reality-check** — before claiming something works, fixed, or is ready, verify it against something real: an actual run, real data, a real target. Green tests prove the code does what the tests expect, not that the tests expect the right thing.

## Why one skill

All three are the same failure at different moments — the agent taking the cheaper version of events instead of the true one. They're bundled because they're one discipline, not three unrelated features.

## Origin

Built after a live session where a recon tool passed every unit test and still returned an unrelated company's domains on a real scan — the bug was invisible until someone insisted on running it against reality instead of trusting green tests. That instinct — "know the problem better than the idea, and check it against reality before you believe it" — is what this skill exists to make automatic.

## Install

```bash
git clone https://github.com/<you>/groundtruth ~/.claude/skills/groundtruth
```

## Related

- [mandate](https://github.com/<you>/mandate) — authority: did the user actually ask for this, here, now.
- [readback](https://github.com/<you>/readback) — memory: what was decided, and why it changed.
- [agent-structure](../) — mandate, readback, and groundtruth as one family: Authority, Memory, Truth.

groundtruth checks truth (is the plan real, is the diff clean, is the claim verified); mandate checks permission; readback keeps the record. Different failure modes, same family.

## License

MIT
