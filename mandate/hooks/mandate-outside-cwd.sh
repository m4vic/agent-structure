#!/usr/bin/env bash
# Mandate: ask before writing outside the current working directory.
#
# Fires on Write/Edit/NotebookEdit. Escalates to the user when the target path
# is not inside cwd. Never denies - a wrong deny costs as much as a wrong allow.
#
# No dependencies. Parses the two fields it needs with sed rather than jq,
# because a hook that silently no-ops when a tool is missing is worse than no
# hook at all: it looks installed and enforces nothing.

set -uo pipefail

INPUT=$(cat)

# Extract a top-level or tool_input string field without a JSON parser.
# Handles the escaped backslashes Windows paths arrive with.
field() {
  printf '%s' "$INPUT" \
    | tr -d '\n' \
    | grep -o "\"$1\"[[:space:]]*:[[:space:]]*\"[^\"]*\"" \
    | head -n1 \
    | sed -e "s/^\"$1\"[[:space:]]*:[[:space:]]*\"//" -e 's/"$//'
}

CWD=$(field 'cwd')
TARGET=$(field 'file_path')
[ -z "$TARGET" ] && TARGET=$(field 'notebook_path')

[ -z "$TARGET" ] && exit 0
[ -z "$CWD" ] && exit 0

# Normalise: unescape \\, unify separators, strip trailing slash, lowercase.
norm() {
  printf '%s' "$1" \
    | sed -e 's/\\\\/\\/g' \
    | tr '\\' '/' \
    | sed -e 's#//*#/#g' -e 's#/$##' \
    | tr '[:upper:]' '[:lower:]'
}

N_CWD=$(norm "$CWD")
N_TARGET=$(norm "$TARGET")

# Relative paths resolve inside cwd.
case "$N_TARGET" in
  /*|[a-z]:/*) ;;
  *) exit 0 ;;
esac

# Inside cwd. The trailing slash matters: without it /proj matches /proj2.
case "$N_TARGET" in
  "$N_CWD"/*|"$N_CWD") exit 0 ;;
esac

# Scratchpad and temp dirs are expected workspaces, not oversteps.
case "$N_TARGET" in
  */appdata/local/temp/*|/tmp/*|/var/folders/*) exit 0 ;;
esac

# Escape for embedding in JSON.
esc() { printf '%s' "$1" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g'; }

printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":"Mandate: writes outside the working directory. Target is %s, working directory is %s. Creating or modifying files in another project was not necessarily what was asked for - confirm before proceeding."}}\n' \
  "$(esc "$TARGET")" "$(esc "$CWD")"
