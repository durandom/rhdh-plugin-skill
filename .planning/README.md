# Planning: Overlay PR Automation Tasks

Task specifications extracted from 2025-12-17 meeting.

## Task Index

| ID | Task | Lifecycle | Persona | Status |
|----|------|-----------|---------|--------|
| 00 | [Onboard Plugin](00-onboard-plugin.md) | Onboard | Owner | ✅ Prototyped |
| 01 | [PR Triage Command](01-pr-triage.md) | Active | Core | Draft |
| 02 | [Publish Trigger](02-publish-trigger.md) | Onboard | Core | Draft |
| 03 | [Assignment Checker](03-assignment-checker.md) | Onboard | Core | Draft |
| 04 | [Code Owner Enforcement](04-codeowner-check.md) | Onboard | Owner | Draft |
| 05 | [Compatibility Bypass Detector](05-compat-bypass.md) | Active | Core | Draft |
| 06 | [Slack Notification Drafter](06-slack-drafter.md) | Active | Core | Draft |
| 07 | [Plugin Config Setup](07-plugin-config.md) | Onboard | Owner | Draft |
| 08 | [Update Response Assist](08-update-assist.md) | Active | Owner | Draft |

## Priority Order

### Foundation (get this working first)

1. **00-onboard-plugin** — Core workflow, already prototyped
   - Integrate Task 04 (CODEOWNERS) as gate
   - Integrate Task 07 (Plugin Config) for smoke tests

### Then: Active Maintenance Automation

2. **01-pr-triage** — Foundation for all core team tasks
3. **02-publish-trigger** — Quick win, unblocks CI
4. **03-assignment-checker** — Include in triage output
5. **05-compat-bypass** — Add to triage diagnostics
6. **06-slack-drafter** — Needs triage first

### Owner Self-Service

7. **08-update-assist** — Help owners respond to auto-updates

## Dependency Graph

```
00-onboard-plugin (prototyped)
    ├── integrates 04-codeowner-check
    └── integrates 07-plugin-config
           │
           ▼
01-pr-triage (foundation for core team)
    ├── includes 02-publish-trigger
    ├── includes 03-assignment-checker
    ├── includes 05-compat-bypass
    └── feeds into 06-slack-drafter
           │
           ▼
08-update-assist (for plugin owners)
```

## Source Material

- Meeting notes: `docs/resources/2025-12-17-overlay-repo-ai-pr-review-flow/`
- Design overview: `DESIGN.md`
- Existing workflow: `skills/rhdh-plugin/workflows/onboard-plugin.md`
