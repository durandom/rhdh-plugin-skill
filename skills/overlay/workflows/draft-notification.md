# Workflow: Draft Slack Notifications

Generate Slack messages for stale or blocked PRs that need human attention.

<required_reading>
**Read these reference files NOW:**

1. `../../rhdh/references/slack-notification.md` — Templates, channels, handle mapping
2. `references/label-priority.md` — PR classification by labels
</required_reading>

<prerequisites>
| Requirement | Details |
|-------------|---------|
| **Input** | Triage report or list of PRs needing attention |
| **Access** | Read access to overlay repo |
| **Tools** | `gh` CLI authenticated |
</prerequisites>

<process>

## Phase 1: Identify PRs Needing Pings

Run after triage, or use these filters directly:

```bash
REPO="redhat-developer/rhdh-plugin-export-overlays"

# Critical PRs stale > 2 days
gh pr list --repo $REPO --state open \
  --label mandatory-workspace --label workspace-update \
  --json number,title,updatedAt,assignees,author \
  --jq '.[] | select((now - (.updatedAt | fromdateiso8601)) / 86400 > 2)'

# Medium PRs stale > 5 days
gh pr list --repo $REPO --state open \
  --label mandatory-workspace --label workspace-addition \
  --json number,title,updatedAt,assignees,author \
  --jq '.[] | select((now - (.updatedAt | fromdateiso8601)) / 86400 > 5)'
```

---

## Phase 2: Gather PR Details

For each PR needing a ping:

```bash
PR_NUMBER=1234

gh pr view $PR_NUMBER --repo $REPO \
  --json number,title,url,updatedAt,labels,assignees,author,reviewRequests,statusCheckRollup
```

Extract:

- **Plugin name** from title (usually `<plugin>: <action>`)
- **Action** from labels (`workspace-update` or `workspace-addition`)
- **Assignee** from `assignees[0].login` or `author.login` as fallback
- **Check status** from `statusCheckRollup`
- **Staleness** = days since `updatedAt`

---

## Phase 3: Map to Slack Handles

Check handle mapping (if configured):

```bash
# If using .rhdh/slack-handles.yaml
cat .rhdh/slack-handles.yaml | grep <github_username>
```

**Fallback:** Use GitHub username as Slack handle (often matches).

---

## Phase 4: Generate Draft Messages

Using template from `slack-notification.md`, generate messages.

### Output Format

```markdown
## Slack Ping Drafts
Generated: {date}

### Critical PRs (send today)

**To: @{slack_handle}** (PR #{number})

```

Hey @{slack_handle}

PR #{number} ({plugin_name} update) needs your attention.

Status:

- Checks: {publish} Publish, {smoke} Smoke
- Reviews: {review_status}
- Stale: {days} days

Priority: Mandatory workspace update — blocking RHDH release

{pr_url}

Could you take a look when you have a moment?

```

---

### Medium PRs (send if no response in 2 days)

**To: @{slack_handle}** (PR #{number})

```

[message]

```

---

### Channel Pings (unassigned critical)

**To: #cope-team**

```

[message]

```
```

---

## Phase 5: Review and Send

1. **Review each draft** — adjust tone/details as needed
2. **Copy to Slack** — paste into appropriate DM or channel
3. **Log the ping** to avoid duplicates:

```bash
$RHDH log add "Pinged @{handle} on PR #{number} ({plugin})" --tag slack --tag triage
```

</process>

<integration_with_triage>

## Using with Triage Workflow

After running `workflows/triage-prs.md`, the report includes a "Suggested Actions" section.

For each row with action "Ping @user":

1. Use PR number to gather details (Phase 2)
2. Generate draft (Phase 4)
3. Add to batch output

### Batch Example

```markdown
## Triage Session: 2025-01-15
## Slack Drafts

| PR | Owner | Slack | Days Stale | Status |
|----|-------|-------|------------|--------|
| #1234 | @dfestal | @dfestal | 5 | Awaiting review |
| #1235 | @johndoe | @john.doe | 3 | Checks failing |

<details>
<summary>Draft messages (click to expand)</summary>

### @dfestal — PR #1234

```

[message]

```

### @john.doe — PR #1235

```

[message]

```

</details>
```

</integration_with_triage>

<tracking>

## Activity Logging

```bash
# Log ping session
$RHDH log add "Drafted Slack pings for {N} stale PRs" --tag slack --tag triage

# Log individual pings (after sending)
$RHDH log add "Pinged @dfestal on PR #1234 (lightspeed)" --tag slack --tag pr-1234

# Search past pings to avoid duplicates
$RHDH log search "slack" | grep "#1234"
```

</tracking>

<success_criteria>
Notification drafting is complete when:

- [ ] All stale priority PRs have draft messages
- [ ] Handles mapped (or flagged as unknown)
- [ ] Messages reviewed for accuracy
- [ ] Drafts ready for human to copy/send
- [ ] Session logged for tracking
</success_criteria>
