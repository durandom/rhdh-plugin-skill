# Task 01: PR Triage Command

**Command:** `/triage-overlay-prs`
**Lifecycle:** Active Maintenance
**Persona:** Core Team

---

## Source Context

> "the core problem is actually working down the backlog of PRs and also a communication problem. So prioritizing PR. So it's not just seeing I have 90 PRs that are up for review, but I also need to prioritize which ones are the most important one to focus at."
> — Marcel Hild, 00:00:00

> "all the PRs do not have the same meaning and criticality especially all the automatically created PRs... the real list of PRs that we should critically focus on is the workspace update PRs on mandatory workspaces"
> — David Festal, 00:03:59

> "if you search for mandatory workspace yes and then update workspace... even from this we would also remove the do not merge for example because we have the do not merge labels for people like in the orchestrator they use mainly the PRs just to generate create some OCI artifacts for tests"
> — David Festal, 00:06:05

---

## Priority Classification

From meeting discussion:

```
CRITICAL:  mandatory-workspace + workspace-update
           → Updates to plugins in RHDH catalog

MEDIUM:    mandatory-workspace + workspace-addition
           → New plugins targeting RHDH catalog

LOW:       workspace-addition (without mandatory)
           → Community plugins, not in catalog

SKIP:      do-not-merge
           → OCI artifact generation only (orchestrator use case)
```

---

## Inputs

| Input | Source | Required |
|-------|--------|----------|
| Repository | `redhat-developer/rhdh-plugin-export-overlays` | Yes |
| PR state | `open` | Yes |
| Labels | GitHub API | Yes |
| Assignees | GitHub API | Yes |
| Last activity | GitHub API | Yes |

---

## Workflow

```
1. FETCH open PRs
   gh pr list --repo redhat-developer/rhdh-plugin-export-overlays \
     --state open --json number,title,labels,assignees,updatedAt,author

2. CLASSIFY each PR by priority
   - Check labels for mandatory-workspace, workspace-update, workspace-addition, do-not-merge
   - Calculate days since last activity

3. ASSESS each PR for issues
   - Missing assignee?
   - Assigned to team only (not individual)?
   - Publish check pending?
   - Stale (>X days based on priority)?

4. OUTPUT actionable report
   - Group by priority tier
   - Include suggested actions
   - Flag blocking issues
```

---

## Output Format

```markdown
## Overlay PR Triage Report
Generated: {timestamp}

### 🔴 Critical — Mandatory Workspace Updates
| PR | Plugin | Days | Assignee | Checks | Action |
|----|--------|------|----------|--------|--------|
| #1234 | aws-ecs | 3 | @user | ✓ Publish ✓ Smoke | Ready to merge |
| #1235 | lightspeed | 7 | (none) | ⏳ Publish | Assign reviewer, trigger /publish |

### 🟡 Medium — Mandatory Workspace Additions
...

### 🟢 Low — Community Additions
...

### ⚫ Skipped — Do Not Merge
| PR | Plugin | Reason |
|----|--------|--------|
| #1240 | orchestrator-test | OCI artifact only |

---

## Suggested Actions
- [ ] Assign @someone to PR #1235 (lightspeed update, 7 days stale)
- [ ] Comment `/publish` on PR #1236
- [ ] Ping @owner — PR #1237 blocking release
```

---

## Implementation Notes

### GitHub CLI Commands

```bash
# Fetch PRs with labels
gh pr list --repo redhat-developer/rhdh-plugin-export-overlays \
  --state open \
  --json number,title,labels,assignees,updatedAt,author,reviews,statusCheckRollup

# Filter by label
gh pr list --label mandatory-workspace --label workspace-update

# Get PR details
gh pr view 1234 --repo redhat-developer/rhdh-plugin-export-overlays --json statusCheckRollup
```

### Label Detection

```javascript
const labels = pr.labels.map(l => l.name);
const isMandatory = labels.includes('mandatory-workspace');
const isUpdate = labels.includes('workspace-update');
const isAddition = labels.includes('workspace-addition');
const isDoNotMerge = labels.includes('do-not-merge');

let priority;
if (isDoNotMerge) priority = 'skip';
else if (isMandatory && isUpdate) priority = 'critical';
else if (isMandatory && isAddition) priority = 'medium';
else if (isAddition) priority = 'low';
else priority = 'unknown';
```

### Staleness Thresholds

| Priority | Warn After | Alert After |
|----------|------------|-------------|
| Critical | 2 days | 5 days |
| Medium | 5 days | 10 days |
| Low | 14 days | 30 days |

---

## Dependencies

- Task 02 (Publish Trigger) — suggest `/publish` action
- Task 03 (Assignment Checker) — include assignment status
- Task 05 (Compat Bypass) — flag compatibility warnings

---

## Open Questions

1. Should we cache PR data locally to avoid rate limits on repeated runs?
2. What's the threshold for "stale" by priority tier?
3. Should output be markdown file, GitHub issue, or console only?
