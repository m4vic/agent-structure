# Mandate

**Check what the user actually authorised, before acting.**

Not a safety tool. Claude Code's [Auto Mode](https://www.anthropic.com/engineering/claude-code-auto-mode) already blocks `git reset --hard`, `git clean`, `rm -rf`, and infrastructure teardown. This covers the failure those miss entirely: an action that is **completely ordinary in itself** and wrong only relative to what was asked for.

A `Write` to a path in another project trips nothing. The command is fine. The authority is not.

## Approval covers one thing, one place, once

| The user said | Authorises | Does not authorise |
|---|---|---|
| "fix it, then use it on X" | fixing it | writing files into X |
| "commit this" | committing | pushing |
| "yes" to a plan | the plan's steps | steps invented later |
| "add it to the repo" | adding | rewriting history |
| approved this last time | that action, then | the same action now |

Agreeing to a **sequence** is not authorising every action inside it. Naming a project is not authorising writes to it.

## Two layers

**The skill** ([`SKILL.md`](SKILL.md), **515 tokens**) covers what no matcher can see: whether the request actually extends this far. It is deliberately small because it fires often.

**One hook** ([`hooks/`](hooks/)) covers the mechanical half — `Write`/`Edit`/`NotebookEdit` landing outside the working directory, escalated to the user.

Only one hook, on purpose. Auto Mode has the destructive-command list; duplicating it by hand would be worse and would fire constantly.

> *Skills are things you want the agent to know how to do. Hooks are things you want to happen no matter what the agent does.*

## Install

```bash
git clone https://github.com/<you>/mandate ~/.claude/skills/mandate
```

Hook: merge `hooks/settings.snippet.json` into `settings.json`, then

```bash
mkdir -p .claude/hooks
cp hooks/mandate-outside-cwd.sh .claude/hooks/
chmod +x .claude/hooks/mandate-outside-cwd.sh
```

The hook escalates to the user; it never denies. A hook that blocks legitimate work gets uninstalled within a day.

## Built from three real failures

In one session an agent pushed a private decision log to a public repo, created files in an unrelated project, and edited that project's tracked `.gitignore` — reporting each afterward. All three were `Write`/`Edit`/`Bash` calls that looked entirely normal.

Two engineering notes from building it:

**The first hook was inert.** It used `jq` with `command -v jq || exit 0` as a safety net. `jq` was not installed, so it exited 0 on every call — allowing everything while appearing installed. A safety check that silently passes is worse than none. It now has no dependencies and a 10-case test suite.

**Then a BOM broke the shebang.** Editing the script from PowerShell wrote a UTF-8 byte-order mark, so `#!/usr/bin/env bash` stopped resolving. It happened to keep working via bash's fallback. If you edit the script on Windows, save it as UTF-8 without BOM and LF, then re-run the tests in [`hooks/README.md`](hooks/README.md).

## Related

- [socratic](https://github.com/m4vic/socratic) — design review before building
- readback — recording what was decided, after
- groundtruth — the plan is on disk, the diff is clean, the claim is verified
- [agent-structure](../) — mandate, readback, and groundtruth as one family: Authority, Memory, Truth

## License

MIT
