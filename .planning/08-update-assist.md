# Task 08: Update Response Assist

**Lifecycle:** Active Maintenance
**Persona:** Plugin Owner

---

## Source Context

> "Once a plugin is in the system, future automatic update PRs are reviewed and merged by the assigned Code Owners"
> — Meeting notes, 00:28:02

> "the original goal of this design was to make it distributed as possible. That means that once plugin is accepted, it's plugin maintainer's job to make sure that everything is in line"
> — Tomas Kral, 00:28:02

---

## Problem

Plugin owners receive auto-generated update PRs but may not know:

- What changed upstream
- What to check before approving
- If smoke tests are configured and passing
- Whether it's safe to merge

---

## Use Case

Plugin owner opens their update PR and wants a quick summary:

```
/explain-update-pr 1234
```

Or integrated into PR comment by automation.

---

## Output

```markdown
## Update Summary for PR #1234

### What Changed
**Workspace:** aws-ecs
**Previous commit:** abc123
**New commit:** def456
**Upstream repo:** awslabs/backstage-plugins-for-aws

**Changelog (upstream):**
- fix: resolve memory leak in polling (#789)
- feat: add support for Fargate tasks (#790)
- chore: update to Backstage 1.42.5 (#791)

### Compatibility
| Check | Status |
|-------|--------|
| Backstage version match | ✅ 1.42.5 (matches overlay) |
| Published artifacts | ✅ Successful |
| Smoke tests | ✅ Passed |

### Merge Readiness
✅ **Ready to merge** — all checks passing, no compatibility issues.

Or:

⚠️ **Action needed:**
- [ ] Smoke test config missing — see Task 07
- [ ] Backstage version mismatch — may need `backstage.json` override
```

---

## Data Sources

| Info | Source |
|------|--------|
| Previous commit | Diff of source.json in PR |
| Upstream changelog | GitHub API: compare commits |
| Compatibility | versions.json + upstream package.json |
| Check status | PR statusCheckRollup |

---

## Implementation

```javascript
async function explainUpdatePR(prNumber) {
  const pr = await getPR(prNumber);

  // Extract commit change from source.json diff
  const { oldCommit, newCommit, upstreamRepo } = extractSourceChange(pr);

  // Get upstream changelog
  const changelog = await getCommitsBetween(upstreamRepo, oldCommit, newCommit);

  // Check compatibility
  const compat = await checkCompatibility(newCommit, overlayVersions);

  // Get check status
  const checks = summarizeChecks(pr.statusCheckRollup);

  // Determine merge readiness
  const ready = checks.publish === 'success'
    && checks.smoke === 'success'
    && compat.status === 'ok';

  return formatSummary({ changelog, compat, checks, ready });
}
```

---

## Upstream Changelog

```bash
# Get commits between two refs
gh api repos/awslabs/backstage-plugins-for-aws/compare/abc123...def456 \
  --jq '.commits[] | "- \(.commit.message | split("\n")[0])"'
```

---

## Integration Options

### Option A: On-demand command

```
/explain-update-pr 1234
```

### Option B: Auto-comment on update PRs

When workspace-update PR is created, automation posts summary comment.

### Option C: Include in triage

Task 01 provides link to generate summary for each PR.

---

## Compatibility Fix Guide

When compatibility issues detected, include fix guidance:

```markdown
### ⚠️ Compatibility Issue Detected

This update targets **Backstage 1.45.0** but overlay targets **1.42.5**.

**Options:**

1. **Wait** — Don't merge until overlay upgrades to 1.45
2. **Override** — Add `backstage.json` to force compatibility:
   ```json
   {
     "version": "1.42.5"
   }
   ```

3. **Patch** — Add patches/ to fix compatibility issues

**Reference:** [Compatibility patching guide](...)

```

---

## Workflow Diagram

```

Plugin Owner receives update PR notification
          ↓
    Runs /explain-update-pr
          ↓
    ┌─────────────────────────────────┐
    │ Summary:                        │
    │ - What changed upstream         │
    │ - Compatibility status          │
    │ - Check status                  │
    │ - Merge readiness               │
    └─────────────────────────────────┘
          ↓
    If ready → Approve & Merge
    If issues → Follow fix guidance

```

---

## Open Questions

1. Auto-comment on all update PRs or on-demand only?
2. How detailed should upstream changelog be?
3. Should we link to upstream PR/commit for context?
