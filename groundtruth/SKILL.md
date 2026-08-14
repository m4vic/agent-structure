---
name: groundtruth
description: Use before starting any non-trivial build (write the plan to a persistent file, not just a chat reply); before pushing commits, opening a PR, or making a repository public (scan for leaked keys, tokens, absolute paths, and internal hostnames first); and before declaring something done, fixed, working, or ready (verify against a real run or real data, not test-green optimism alone). Three routes, one skill — build-plan, publish-check, reality-check.
---

# groundtruth

An agent's default gravity pulls toward three shortcuts: keep the plan in the chat instead of on disk, push before checking what's actually in the diff, and declare success because the tests are green instead of because it was actually run against something real. None of these are dishonesty — they're the path of least resistance, taken by every model, every time, unless something pushes back.

groundtruth is the counter-pressure, at the three moments it matters most: **before building, before publishing, before claiming done.**

## Route 1 — build-plan

**Trigger:** about to start implementation work of real size — a new feature, a redesign, a multi-file change, anything more than a couple of edits — regardless of which other skill or method produced the plan.

**Rule:** the plan lands in a file in the project's working folder before code changes start — `IMPLEMENTATION_PLAN.md`, or whatever the project already calls its plan doc. Never leave a plan only in the chat transcript. A plan that exists only as scrollback is invisible to the next session, the next agent, and any tool (Codex, another Claude Code session, a teammate) that picks up the work later.

This does not replace a real planning method — if `socratic` or another design-review skill is available, use it to actually derive the plan. groundtruth's job is narrower and comes after: whatever plan gets produced, by whatever method, **it gets written to disk**, and it gets updated as the plan changes, not written once and abandoned while the real plan drifts in conversation.

**Check before starting work:**
- Does a plan file already exist for this piece of work? If yes, read it before proposing changes — don't re-derive from scratch.
- If a plan just got settled in conversation, is it on disk yet? If not, write it before touching code.
- If the plan changes mid-build, does the file still say the old thing? Update it — a stale plan file is worse than none, because it's trusted.

## Route 2 — publish-check

**Trigger:** about to `git push` (especially to a new remote, or for the first time), open a PR, or make a repository public — or the user says "push this," "open source this," "make this public."

**Rule:** before the push or publish action, check what's actually about to leave the machine. Do not assume "I didn't add anything secret" is the same as "nothing secret is in this diff" — dependency lockfiles, `.env` copies, debug output, and absolute paths get committed by accident constantly.

**Check:**
- **Secrets and keys** — API keys, tokens, private keys, connection strings, passwords, in the diff or the files about to be added. Grep for vendor key shapes (`sk-`, `AKIA`, `ghp_`, etc.) and generic patterns (`_KEY\s*=`, `_TOKEN\s*=`, `_SECRET\s*=`) in what's staged or about to be committed — not just files the agent itself wrote.
- **Paths and hosts** — absolute paths containing a username (`C:\Users\<name>\...`, `/home/<name>/...`), internal hostnames, private IP ranges, anything that identifies the machine or network unnecessarily.
- **`.gitignore` coverage** — does it actually exclude `.env`, credentials files, `.venv`/`node_modules`, local databases, and any runtime-generated secrets directory the project uses?
- **History, not just the diff** — if this is the *first* public push of a repo that's had private history, a secret removed in a later commit can still be recovered from an earlier one. Check history before the first public push, not just the files being added now.

**On a finding:** stop and report it plainly — file, what was found, why it matters — before the push happens. Do not silently strip it and push anyway, and do not silently rewrite history to remove it (that's a `mandate`-territory action: rewriting history needs explicit approval, every time). Report, then let the user decide.

## Route 3 — reality-check

**Trigger:** about to say something works, is fixed, is ready, or is done — based on unit tests passing, a successful build, or the model's own reasoning about correctness, with no execution against anything real.

**Rule:** before the claim, verify against something real — an actual run, actual output, an actual target or real data — not the fact that tests are green or the code compiles. If real verification genuinely isn't possible (no environment, no way to run it, no real data available), **say that explicitly** rather than letting a claim of correctness stand in for it.

This is not hypothetical: a recon tool passed every unit test and still returned an unrelated company's domains for a real scan — the bug was invisible until it ran against a real target. Green tests measure that the code does what the tests expect, not that the tests expect the right thing.

**Check before claiming success:**
- Was this actually run, or only reasoned about?
- If it was run, was it run against something *real* — a real target, real data, a real environment — or only against a fixture built to make it pass?
- If it can't be verified right now, does the response say so, or does it imply verification that didn't happen?

## Why one skill, three routes

All three routes are the same failure, at three different moments: the agent defaults to the version of events that requires the least friction — keep the plan in chat, push without checking, claim success without running it. Each route is a specific point where that default gets overridden with an explicit check. They're bundled together because they're the same discipline applied at different times, not three unrelated features.

## Related

- [mandate](../mandate/SKILL.md) — checks *authority*: did the user actually ask for this action, here, now. groundtruth checks *truth*: is the plan written down, is the diff clean, is the claim actually verified.
- [readback](../readback/SKILL.md) — records decisions after they're made. groundtruth's build-plan route is about the plan *before* work starts; readback is the history of how it changed.
- [agent-structure](../SKILL.md) — the orientation skill that ties mandate, readback, and groundtruth together as one working method; load it first at the start of real work.
