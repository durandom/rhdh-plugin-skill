---
description: Document session accomplishments and remaining work to .rhdh-plugin/logs/
argument-hint: <descriptive-name>
allowed-tools: Skill(rhdh-plugin), Read, Write, Bash, Glob
---

# Session Log Command

Create a comprehensive session log document that captures work completed and remaining tasks for future resumption.

## Philosophy

Prioritize **comprehensive detail and precision** over brevity. The goal is to enable seamless continuation of work—either by yourself in a future session or by another collaborator—without loss of context.

## Process

### Step 1: Gather Context

Before writing, gather information about this session:

1. **Git changes** — Run `git status` and `git diff --stat` to see what files changed
2. **Recent commits** — Run `git log --oneline -10` if commits were made
3. **CLI state** — Run `$RHDH_PLUGIN` to check current workspace/plugin context
4. **Conversation review** — Review the conversation to identify key decisions and actions

### Step 2: Determine Output Path

**Directory:** `.rhdh-plugin/logs/` (create if missing)
**Filename:** `YYYY-MM-DD-<argument-slug>.md`

Example: `/session-log aws-appsync-onboard` → `.rhdh-plugin/logs/2025-01-29-aws-appsync-onboard.md`

### Step 3: Write the Session Log

Use this template structure:

<session_log_template>

## Session Log: $ARGUMENTS

**Date:** [current date/time]
**Context:** [workspace or plugin being worked on]

## Summary

[1-2 sentence description of the session's primary accomplishment or focus]

## Work Completed

Document all completed work with specific references:

- **Files created/modified:**
  - `path/to/file.ts` — description of change
- **PRs/commits:**
  - PR #123: description
  - Commit abc1234: message
- **Decisions made:**
  - Decision: [what was decided]
  - Rationale: [why]
- **Issues resolved:**
  - Fixed: [specific issue]

## Remaining Work

Actionable next steps with enough context for resumption:

- [ ] **Task description**
  - File: `path/to/file.ts:123`
  - Context: [why this is needed, what blocks it]
  - Acceptance: [how to know it's done]

## Blockers & Open Questions

Items that cannot proceed without external input:

- **Waiting on:** [person/team] for [what]
- **Question:** [unresolved question that needs answer]
- **Dependency:** [external dependency]

## Resumption Context

Critical information for continuing this work:

**Key files:**

- `path/to/important/file.ts` — [what it does, current state]

**Environment state:**

- Build: [passing/failing]
- Tests: [status]
- Branch: [current branch]

**Gotchas:**

- [Things to remember, edge cases discovered, non-obvious behaviors]

**Related resources:**

- JIRA: [ticket URL if applicable]
- PR: [PR URL if applicable]
- Docs: [relevant documentation]
</session_log_template>

### Step 4: Confirm Creation

After writing the file:

1. Display the full path to the created log
2. Show a brief summary of what was captured
