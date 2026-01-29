# Task 03: Assignment Checker

**Lifecycle:** Onboard / Active
**Persona:** Core Team

---

## Source Context

> "Concerns were raised about the number of requested reviewers, with Tomas Kral stating that assigning to a team is not ideal, as too many reviewers dilute responsibility. Tomas Kral suggested assigning to one or two individuals instead."
> — Meeting notes, 00:36:35

> "if it's everyone's responsibility, it's no one's responsibility. I think that's the big problem here."
> — Tomas Kral

> "assignment happens when someone starts the review, either through an OpenShift CI bot when they use LGTM or approve, or inferred by GitHub when they submit a review comment"
> — Meeting notes, 00:37:51

---

## Problem

PRs get review requests sent to teams (e.g., `@redhat-developer/rhdh-plugins`), but team assignments dilute responsibility. Nobody feels personally accountable.

**Desired state:** Each PR has 1-2 individual assignees.

---

## Logic

```
FOR each open PR:
  1. GET requested reviewers (individuals and teams)
  2. GET assignees

  IF no assignees AND no individual reviewers:
    → FLAG: "No individual assigned"
    → SUGGEST: Look up CODEOWNERS for this workspace

  IF only team reviewers (no individuals):
    → FLAG: "Only team assigned, responsibility diluted"
    → SUGGEST: Pick specific person from team

  IF assignee exists:
    → OK (responsibility clear)
```

---

## CODEOWNERS Lookup

When suggesting an assignee, check the CODEOWNERS file:

```bash
# Get CODEOWNERS content
gh api repos/redhat-developer/rhdh-plugin-export-overlays/contents/CODEOWNERS \
  --jq '.content' | base64 -d
```

Parse for workspace path:

```
# Example CODEOWNERS
workspaces/aws-ecs/    @johndoe @janedoe
workspaces/lightspeed/ @redhat-developer/rhdh-lightspeed
```

---

## Inputs

| Input | Source |
|-------|--------|
| PR list | From Task 01 triage or direct query |
| CODEOWNERS | GitHub API |

---

## Output (integrated into triage)

```markdown
### Assignment Issues

| PR | Plugin | Reviewers | Assignees | Suggested |
|----|--------|-----------|-----------|-----------|
| #1234 | aws-ecs | @team (team only) | (none) | @johndoe (from CODEOWNERS) |
| #1235 | lightspeed | (none) | (none) | @lightspeed-owner |

### PRs with Clear Ownership
| PR | Plugin | Assignee |
|----|--------|----------|
| #1236 | todo | @todoowner |
```

---

## Implementation

```javascript
async function checkAssignment(pr, codeowners) {
  const reviewers = pr.reviewRequests || [];
  const assignees = pr.assignees || [];

  const individualReviewers = reviewers.filter(r => !r.isTeam);
  const teamReviewers = reviewers.filter(r => r.isTeam);

  // Extract workspace name from PR files
  const workspace = extractWorkspace(pr.files);
  const suggestedOwners = codeowners[workspace] || [];

  if (assignees.length === 0 && individualReviewers.length === 0) {
    return {
      status: 'no-owner',
      message: 'No individual assigned',
      suggested: suggestedOwners[0] || 'unknown'
    };
  }

  if (assignees.length === 0 && teamReviewers.length > 0 && individualReviewers.length === 0) {
    return {
      status: 'team-only',
      message: `Only team assigned: ${teamReviewers.map(t => t.name).join(', ')}`,
      suggested: suggestedOwners[0] || 'pick from team'
    };
  }

  return {
    status: 'ok',
    owner: assignees[0] || individualReviewers[0]
  };
}
```

---

## GitHub CLI

```bash
# Get PR with reviewer info
gh pr view 1234 --repo redhat-developer/rhdh-plugin-export-overlays \
  --json assignees,reviewRequests,files

# Assign someone
gh pr edit 1234 --repo redhat-developer/rhdh-plugin-export-overlays \
  --add-assignee johndoe
```

---

## Integration

This check is part of Task 01 (PR Triage) output, not a standalone command. But could offer:

```
/assign-overlay-pr 1234 @johndoe
```

As a quick action.

---

## Open Questions

1. Should we auto-assign from CODEOWNERS, or just suggest?
2. How to handle PRs for new workspaces (no CODEOWNERS entry yet)?
3. Should Core Team members be fallback assignees?
