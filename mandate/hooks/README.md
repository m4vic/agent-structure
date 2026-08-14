# Mandate hook

One rule: escalate to the user when `Write`, `Edit`, or `NotebookEdit` targets a path outside the working directory.

Only one, on purpose. [Auto Mode](https://www.anthropic.com/engineering/claude-code-auto-mode) already hard-blocks `git reset --hard`, `git checkout -- .`, `git clean -fd`, `git stash drop`, `rm -rf`, mass deletions, and teardown commands. Re-implementing that by hand would be worse and would fire constantly. Writing into another project is what it does not catch, because the action is only wrong relative to what was asked.

It escalates (`ask`), never denies. A wrong deny costs as much as a wrong allow.

## Install

Merge the `hooks` key from `settings.snippet.json` into `~/.claude/settings.json` (all projects) or `<project>/.claude/settings.json` (one). If a `hooks` key exists, merge the `PreToolUse` **array** rather than replacing it.

```bash
mkdir -p .claude/hooks
cp mandate-outside-cwd.sh .claude/hooks/
chmod +x .claude/hooks/mandate-outside-cwd.sh
```

The snippet points at `${CLAUDE_PROJECT_DIR}/.claude/hooks/mandate-outside-cwd.sh`. For a user-level install, use an absolute path.

## No dependencies, on purpose

The first version used `jq`, guarded by `command -v jq || exit 0`. `jq` was not installed, so the hook exited 0 on every call — silently allowing everything while looking installed. It passed nothing and said nothing.

That is the worst failure available to a safety check: **inert but plausible.** It now parses the two fields it needs with `grep` and `sed`.

## Test it

```bash
# ASK — another project
echo '{"cwd":"/home/u/proj","tool_input":{"file_path":"/home/u/other/a.py"}}' | ./mandate-outside-cwd.sh

# silent — inside the project
echo '{"cwd":"/home/u/proj","tool_input":{"file_path":"/home/u/proj/src/a.py"}}' | ./mandate-outside-cwd.sh

# ASK — sibling dir sharing a prefix
echo '{"cwd":"/home/u/proj","tool_input":{"file_path":"/home/u/proj2/a.py"}}' | ./mandate-outside-cwd.sh
```

Silence means allow. JSON on stdout means the user gets asked.

Verified on 10 cases: Windows paths with escaped separators, mixed drive-letter case, relative paths, the scratchpad exemption, home-directory installs, the `proj` vs `proj2` prefix trap, `notebook_path`, and calls with no path at all.

**Editing on Windows:** save as UTF-8 **without BOM**, LF endings. A BOM breaks `#!/usr/bin/env bash` in a way that can still appear to work. Re-run the tests after any change — a check that cannot fail loudly has to be tested deliberately.

## Gaps

**Bash reaches outside unchecked.** `cp` or `mv` to another directory is not caught; matching arbitrary shell syntax reliably is not worth the false positives.

**Scope creep is invisible here.** No matcher sees "you redesigned something nobody asked for". That is the skill's job.

**Permission mode wins.** In a mode that auto-approves everything, `ask` may not prompt. This is a floor, not a guarantee.
