# Task 02: Publish Trigger

**Command:** `/publish-overlay-pr <pr-number>`
**Lifecycle:** Onboard
**Persona:** Core Team

---

## Source Context

> "the publish workflow is not automatically triggered on PR creation due to GitHub limitations preventing cycling workflows, meaning a manual step, such as a triage person adding a `/publish` comment, is currently required"
> — David Festal, 00:41:48

> "Marcel Hild will automate adding a `/publish` command"
> — Suggested next steps

---

## Problem

GitHub Actions cannot trigger other workflows from bot-created PRs (to prevent infinite loops). When the automation creates a PR for a workspace update/addition, the `/publish` workflow doesn't run automatically.

**Current workaround:** Someone manually comments `/publish` on the PR.

---

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| PR number | Argument | Yes |
| Repository | Default: `redhat-developer/rhdh-plugin-export-overlays` | Yes |

---

## Workflow

```
1. VALIDATE PR exists and is open
   gh pr view <number> --json state,labels

2. CHECK if publish already running/passed
   gh pr view <number> --json statusCheckRollup
   Look for check named "publish" or similar

3. GUARD against inappropriate PRs
   - Skip if do-not-merge label present
   - Skip if PR is closed/merged

4. COMMENT /publish
   gh pr comment <number> --body "/publish"

5. RETURN workflow link
   Parse response or construct URL
```

---

## Output

```markdown
✓ Triggered publish for PR #1234
  Workflow: https://github.com/redhat-developer/rhdh-plugin-export-overlays/actions/runs/12345

  Next: Watch for smoke tests after publish completes
```

Or if already published:

```markdown
ℹ PR #1234 already has successful publish check
  No action needed
```

---

## Implementation

```bash
#!/bin/bash
PR_NUMBER=$1
REPO="redhat-developer/rhdh-plugin-export-overlays"

# Check PR state
STATE=$(gh pr view "$PR_NUMBER" --repo "$REPO" --json state -q '.state')
if [ "$STATE" != "OPEN" ]; then
  echo "PR #$PR_NUMBER is not open (state: $STATE)"
  exit 1
fi

# Check for do-not-merge label
LABELS=$(gh pr view "$PR_NUMBER" --repo "$REPO" --json labels -q '.labels[].name')
if echo "$LABELS" | grep -q "do-not-merge"; then
  echo "PR #$PR_NUMBER has do-not-merge label, skipping"
  exit 0
fi

# Check existing publish status
PUBLISH_STATUS=$(gh pr view "$PR_NUMBER" --repo "$REPO" --json statusCheckRollup \
  -q '.statusCheckRollup[] | select(.name | contains("publish")) | .conclusion')

if [ "$PUBLISH_STATUS" = "SUCCESS" ]; then
  echo "PR #$PR_NUMBER already has successful publish"
  exit 0
fi

# Trigger publish
gh pr comment "$PR_NUMBER" --repo "$REPO" --body "/publish"
echo "Triggered /publish on PR #$PR_NUMBER"
```

---

## Batch Mode

For triage, support triggering multiple PRs:

```bash
/publish-overlay-prs 1234 1235 1236
```

Or from triage output:

```bash
# Get all PRs needing publish from triage
gh pr list --repo redhat-developer/rhdh-plugin-export-overlays \
  --state open \
  --json number,statusCheckRollup \
  | jq '[.[] | select(.statusCheckRollup | map(.name) | index("publish") | not)] | .[].number'
```

---

## Guards

| Condition | Action |
|-----------|--------|
| PR closed/merged | Skip with message |
| `do-not-merge` label | Skip with message |
| Publish already passed | Skip with message |
| Publish currently running | Skip with message |

---

## Integration with Triage

Task 01 (PR Triage) should include publish status in output:

```markdown
| PR | Plugin | Checks |
|----|--------|--------|
| #1234 | aws-ecs | ⏳ Publish pending |
```

And suggest action:

```markdown
- [ ] Comment `/publish` on PR #1234
```

---

## Open Questions

1. Should we wait for publish to complete and report result?
2. Rate limiting if triggering many PRs at once?
3. Should we auto-trigger for all PRs meeting criteria, or require explicit list?
