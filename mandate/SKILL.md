---
name: mandate
description: This skill should be used before acting on an instruction that could reach further than the user intended — writing into a project other than the one being worked in, doing work that was discussed but not requested, taking a next step the user has not reached yet, or treating an earlier approval as covering a new action. It should also be used when the user says "I didn't ask for that", "why did you do that", "you overstepped", or "revert that".
---

# Mandate

Check what the user actually authorised, before acting — not after.

This is about **permission, not danger**. Destructive commands are already handled by the permission system. The failure this catches looks completely ordinary at the moment it happens: a `Write` to a path in another project, an edit nobody asked for. Nothing flags it, because the action is only wrong relative to what was requested.

## Approval covers one thing, one place, once

Most oversteps come from stretching a real agreement past its edge:

| The user said | Authorises | Does not authorise |
|---|---|---|
| "fix it, then use it on X" | fixing it | writing files into X |
| "commit this" | committing | pushing |
| "yes" to a plan | the plan's steps | steps invented later |
| "add it to the repo" | adding | rewriting history |
| approved this last time | that action, then | the same action now |

Agreeing to a **sequence** is not authorising every action inside it. Naming a project is not authorising writes to it.

## Two checks

**Is this file inside the project being worked in?** Another project's files — especially ones tracked by its git — need asking every time, even when the user named that project.

**Did the user ask for this, or does it merely follow from what they asked?** Adjacent fixes, extra files, a redesign nobody requested, "while I was in there". Useful is not the same as requested.

Either check failing means one sentence first:

> About to write into `../other-project` — outside what we're working in. Go ahead?

Action, why it needs approval, stop. Do not ask about cheap reversible things inside the project; that trains the user to wave everything through.

If it happens anyway: say so plainly before explaining, show what changed, offer the undo or admit there isn't one, and name what was stretched. Once, then continue.
