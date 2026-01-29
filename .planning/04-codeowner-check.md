# Task 04: Code Owner Enforcement

**Lifecycle:** Onboard
**Persona:** Plugin Owner

---

## Source Context

> "Tomas Kral confirmed that if a new plugin is added by someone who is not a Code Owner, one of the root Code Owners must approve it, suggesting that the initial PR should also require the person to add themself as a Code Owner for that plugin's file"
> — Meeting notes, 00:26:04

> "David Festal agreed that this self-assignment to the Code Owners file should be a gate for the first merge"
> — Meeting notes, 00:27:05

> "Once a plugin is in the system, future automatic update PRs are reviewed and merged by the assigned Code Owners"
> — Meeting notes, 00:28:02

---

## Problem

New plugins get merged without the contributor adding themselves to CODEOWNERS. Result:

- Future update PRs have no clear owner
- Falls back to root code owners (COPE team)
- Bottleneck on core team

---

## Rule

**For any PR adding a new workspace:**
The PR MUST modify `CODEOWNERS` to add an entry for that workspace.

---

## Detection Logic

```
1. CHECK if PR has workspace-addition label
   OR files include new workspaces/<name>/ directory

2. CHECK if CODEOWNERS file is modified in PR
   gh pr diff <number> --name-only | grep CODEOWNERS

3. IF new workspace AND no CODEOWNERS change:
   → FLAG: "Missing CODEOWNERS entry"
   → COMMENT with template
```

---

## CODEOWNERS Template

```
# In CODEOWNERS file, add:
workspaces/<your-plugin-name>/    @your-github-username
```

Example entry:

```
workspaces/aws-ecs/    @johndoe @janedoe
```

---

## Implementation

```bash
#!/bin/bash
PR_NUMBER=$1
REPO="redhat-developer/rhdh-plugin-export-overlays"

# Get files changed
FILES=$(gh pr diff "$PR_NUMBER" --repo "$REPO" --name-only)

# Check for new workspace
NEW_WORKSPACES=$(echo "$FILES" | grep -E '^workspaces/[^/]+/' | cut -d/ -f2 | sort -u)

if [ -z "$NEW_WORKSPACES" ]; then
  echo "No new workspaces in PR"
  exit 0
fi

# Check if CODEOWNERS modified
if echo "$FILES" | grep -q "CODEOWNERS"; then
  echo "✓ CODEOWNERS modified"

  # Verify each new workspace has entry
  CODEOWNERS_DIFF=$(gh pr diff "$PR_NUMBER" --repo "$REPO" -- CODEOWNERS)
  for ws in $NEW_WORKSPACES; do
    if echo "$CODEOWNERS_DIFF" | grep -q "workspaces/$ws/"; then
      echo "  ✓ Entry for $ws found"
    else
      echo "  ⚠ No entry for $ws"
    fi
  done
else
  echo "⚠ CODEOWNERS not modified"
  echo ""
  echo "New workspaces detected: $NEW_WORKSPACES"
  echo ""
  echo "Please add to CODEOWNERS:"
  for ws in $NEW_WORKSPACES; do
    echo "  workspaces/$ws/    @your-username"
  done
fi
```

---

## Comment Template

When flagging a PR:

```markdown
### ⚠️ Missing CODEOWNERS Entry

This PR adds a new workspace but doesn't update the `CODEOWNERS` file.

**Why this matters:** Without a CODEOWNERS entry, future update PRs for this plugin will require approval from root code owners, creating a bottleneck.

**Please add to `CODEOWNERS`:**

```

workspaces/{workspace-name}/    @{your-github-username}

```

This ensures you'll be notified and can approve future updates to your plugin.

---
*Automated check from overlay PR triage*
```

---

## Integration Points

### With Onboard Workflow

The existing `onboard-plugin` workflow (Phase 5: Verify) should include this check.

### With Triage

Task 01 should flag `workspace-addition` PRs missing CODEOWNERS:

```markdown
| PR | Plugin | Issue |
|----|--------|-------|
| #1234 | new-plugin | ⚠️ Missing CODEOWNERS |
```

---

## Edge Cases

| Scenario | Handling |
|----------|----------|
| PR from bot (automation) | Still flag — someone should add owner |
| Multiple workspaces in one PR | Check each workspace has entry |
| Existing workspace (not new) | Skip check — already has owner |
| CODEOWNERS entry points to team | Warn but allow — individual preferred |

---

## Open Questions

1. Should this block merge (via GitHub Actions), or just warn?
2. Should we auto-comment on PRs, or include in triage report only?
3. What if contributor adds team instead of individual?
