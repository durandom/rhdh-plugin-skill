# Task 06: Slack Notification Drafter

**Lifecycle:** Active Maintenance
**Persona:** Core Team

---

## Source Context

> "there is a big lack of efficient and scoped communication and notification... if the number one tool that you're working with for a lot of folks is GitHub. If this is not working properly, then something is off."
> — Marcel Hild, 00:55:49

> "defining triage based on labels, and drafting Slack messages to ping people for attention if necessary"
> — Meeting notes, 00:53:29

> "GitHub notifications have poor signal/noise ratio"
> — Meeting notes

---

## Problem

GitHub notifications are noisy. People ignore them or miss critical ones. Direct Slack pings are more effective for urgent items.

---

## Workflow

```
1. IDENTIFY stale priority PRs from triage
   - Critical: stale > 2 days
   - Medium: stale > 5 days
   - With assignee who hasn't responded

2. MAP GitHub username to Slack handle
   - Lookup table or LDAP/Rover query

3. DRAFT contextual message
   - PR link
   - Why it's important (label context)
   - Current status (checks, reviews)
   - Specific ask

4. OUTPUT draft messages (human sends)
```

---

## Message Template

```
Hey @{slack_handle} 👋

PR #{number} ({plugin_name} update) needs your attention.

📊 Status:
- Checks: {publish_status} Publish, {smoke_status} Smoke
- Reviews: {review_status}
- Stale: {days} days

🎯 Priority: {priority_reason}

🔗 {pr_url}

Could you take a look when you have a moment?
```

---

## Examples

**Critical - Mandatory workspace update:**

```
Hey @dfestal 👋

PR #1234 (lightspeed update) needs your attention.

📊 Status:
- Checks: ✅ Publish, ✅ Smoke
- Reviews: Awaiting your review
- Stale: 5 days

🎯 Priority: Mandatory workspace — blocking next RHDH release

🔗 https://github.com/redhat-developer/rhdh-plugin-export-overlays/pull/1234

Could you take a look when you have a moment?
```

**Medium - New plugin needs config:**

```
Hey @newcontributor 👋

PR #1235 (your new-plugin addition) needs some updates.

📊 Status:
- Checks: ❌ Smoke (missing config)
- Reviews: Approved, but can't merge

🎯 Action needed: Add plugin configuration to enable smoke tests
See: https://github.com/.../README.md#smoke-test-config

🔗 https://github.com/redhat-developer/rhdh-plugin-export-overlays/pull/1235
```

---

## Handle Mapping

Need a mapping from GitHub username to Slack handle:

```yaml
# slack-handles.yaml
handles:
  dfestal: dfestal
  mhild: mhild
  tkral: tkral
  johndoe: john.doe

# Team fallbacks
teams:
  redhat-developer/rhdh-plugins: "#rhdh-plugins"
  redhat-developer/cope: "#cope-team"
```

Alternative: Query from internal directory (Rover, LDAP).

---

## Implementation

```javascript
function draftSlackMessage(pr, slackHandles) {
  const assignee = pr.assignees[0]?.login;
  const slackHandle = slackHandles[assignee] || assignee;

  const checksStatus = formatChecks(pr.statusCheckRollup);
  const priority = classifyPriority(pr.labels);
  const staleDays = daysSince(pr.updatedAt);

  return `
Hey @${slackHandle} 👋

PR #${pr.number} (${extractPluginName(pr)} update) needs your attention.

📊 Status:
- Checks: ${checksStatus}
- Reviews: ${formatReviews(pr.reviews)}
- Stale: ${staleDays} days

🎯 Priority: ${priority.reason}

🔗 ${pr.url}

Could you take a look when you have a moment?
  `.trim();
}
```

---

## Batch Output

For triage, output all draft messages at once:

```markdown
## Slack Ping Drafts

### Critical PRs (send today)

**To: @dfestal**
```

[message here]

```

**To: @tkral**
```

[message here]

```

### Medium PRs (send if no response in 2 days)

**To: @contributor**
```

[message here]

```
```

---

## Integration with Triage

Task 01 output includes section for Slack drafts:

```markdown
## Suggested Pings

| PR | Owner | Slack | Days Stale |
|----|-------|-------|------------|
| #1234 | @dfestal | @dfestal | 5 |
| #1235 | @johndoe | @john.doe | 3 |

<details>
<summary>Draft messages</summary>

[expandable section with copy-paste messages]

</details>
```

---

## Channels

For team-wide issues or unassigned PRs:

| Situation | Channel |
|-----------|---------|
| No assignee on critical PR | #cope-team |
| Plugin team PR | #rhdh-plugins |
| Release blocker | #rhdh-release |

---

## Open Questions

1. Where to store handle mapping? Repo file, env var, external service?
2. Should messages go to DM or channel?
3. Auto-send via Slack API or just draft for human to send?
4. How to track "already pinged" to avoid spam?
