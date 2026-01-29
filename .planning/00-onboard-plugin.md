# Task 00: Onboard Plugin to Extensions Catalog

**Command:** `/onboard-plugin <upstream-url>`
**Lifecycle:** Onboard
**Persona:** Plugin Owner
**Status:** ✅ Prototyped — see `skills/rhdh-plugin/workflows/onboard-plugin.md`

---

## Source Context

> "So effectively we could we should probably add that as a gate for first merge."
> — David Festal, on requiring CODEOWNERS entry, 00:27:05

> "if a new plugin is added by someone who is not a Code Owner, one of the root Code Owners (RJH cope, gash, and Tomas Kral) must approve it"
> — Tomas Kral, 00:26:04

> "the original goal of this design was to make it distributed as possible. That means that once plugin is accepted, it's plugin maintainer's job"
> — Tomas Kral, 00:28:02

---

## Existing Implementation

**Location:** `skills/rhdh-plugin/workflows/onboard-plugin.md`

### 6 Phases

| Phase | Name | Status | Notes |
|-------|------|--------|-------|
| 1 | Discovery & Evaluation | ✅ Working | License, health, version checks |
| 2 | Workspace Creation | ✅ Working | source.json, plugins-list.yaml |
| 3 | PR & Build | ✅ Working | /publish trigger, CI feedback |
| 4 | Plugin Metadata | ⚠️ Needs work | Integration with smoke tests |
| 5 | Verification | ✅ Working | rhdh-local testing |
| 6 | PR Approval & Merge | ⚠️ Needs work | Gating enforcement |

---

## Gaps Identified from Meeting

### Gap 1: CODEOWNERS Enforcement (Phase 2/6)

**Current:** Phase 2.6 says "Add CODEOWNERS Entry" but it's not enforced.

**From meeting:**
> "when you are adding new plugin or new workspace then you add yourself as a code owner into this file... that's maybe something that we should check automatically"
> — Tomas Kral, 00:27:05

**Fix:** Integrate Task 04 (CODEOWNERS Check) into Phase 6 as a gate.

```
Phase 6.0 (new): Verify CODEOWNERS
- [ ] Check CODEOWNERS file modified in PR
- [ ] Verify entry exists for new workspace
- [ ] If missing → block merge, comment with template
```

---

### Gap 2: Smoke Test Configuration (Phase 4)

**Current:** Phase 4 creates metadata but doesn't emphasize smoke test config.

**From meeting:**
> "the test workflow checks that both the back end and front end of the dynamic plugins are correctly loaded using configuration defined in the package-level catalog entities"
> — David Festal, 00:22:02

**Fix:** Integrate Task 07 (Plugin Config Setup) into Phase 4.

```
Phase 4.2 (enhanced): Smoke Test Configuration
- [ ] Add appConfigExamples to Package metadata
- [ ] Verify smoke test runs after /publish
- [ ] If smoke test fails → check config, see references/ci-feedback.md
```

---

### Gap 3: Gating Review Process (Phase 6)

**Current:** Phase 6 says "request from cope team" but doesn't explain the gating.

**From meeting:**
> "one of the root Code Owners (RJH cope, gash, and Tomas Kral) must approve it"

**Root code owners:** `@redhat-developer/rhdh-cope`, `@gashcrumb`, `@tkral`

**Fix:** Add explicit gating step.

```
Phase 6.1 (enhanced): Gating Review
- [ ] If first PR from contributor → requires root code owner approval
- [ ] Root owners: @redhat-developer/rhdh-cope, @gashcrumb, @tkral
- [ ] They verify: License OK, upstream active, CODEOWNERS added
```

---

### Gap 4: Productization File Guidance

**Current:** Not covered in workflow.

**From meeting:**
> "these files are related to RHDH productization and are typically not needed for a new community plugin to be added to the overlay"
> — David Festal, 00:46:53

**Clarification to add:**

```
## Note: Productization Files

The following files are NOT needed for initial onboarding:
- rhdh-supported-packages.txt (GA plugins)
- rhdh-techpreview-packages.txt (TP plugins)
- community-packages.txt (dev preview)

These are managed by the product team AFTER onboarding.
Your plugin can be in the overlay and work without being in these files.
```

---

## Integration with Other Tasks

| Task | Integration Point | How |
|------|-------------------|-----|
| 02: Publish Trigger | Phase 3.3 | Already covered — /publish comment |
| 04: CODEOWNERS Check | Phase 2.6 / 6.0 | Add verification step |
| 07: Plugin Config | Phase 4 | Add smoke test config guidance |

---

## Workflow Diagram

```
        ┌─────────────────────────────────────────────────────────┐
        │  ONBOARD PLUGIN WORKFLOW                                │
        └─────────────────────────────────────────────────────────┘
                                    │
        ┌───────────────────────────┴───────────────────────────┐
        ▼                                                       ▼
   PHASE 1: Discovery                                    [Plugin Owner]
   • License check                                        does this
   • Upstream health
   • Backstage version
        │
        ▼
   PHASE 2: Workspace Creation
   • source.json
   • plugins-list.yaml
   • CODEOWNERS entry  ◀─── Task 04 enforcement
        │
        ▼
   PHASE 3: PR & Build
   • Open PR
   • /publish comment  ◀─── Task 02 (can be automated)
   • Watch CI feedback
        │
        ▼
   PHASE 4: Metadata
   • Package entities
   • Plugin entity
   • Smoke test config  ◀─── Task 07 guidance
        │
        ▼
   PHASE 5: Verification
   • rhdh-local testing
   • Document results
        │
        ▼
   PHASE 6: Approval & Merge
   • Root owner gate   ◀─── [Core Team] reviews
   • CODEOWNERS check  ◀─── Task 04 enforcement
   • Merge
        │
        ▼
   ✅ Plugin onboarded
   Future updates handled by code owner
```

---

## Proposed Enhancements

### Priority 1: Add CODEOWNERS Gate

In `workflows/onboard-plugin.md`, enhance Phase 2.6 and add Phase 6.0:

```markdown
### 2.6 Add CODEOWNERS Entry (Required)

⚠️ **This is a merge requirement** — PRs adding new workspaces without CODEOWNERS will be blocked.

\`\`\`bash
# Add your entry
echo "/workspaces/<workspace-name>/ @<your-github-username>" >> CODEOWNERS
\`\`\`

Verify with:
\`\`\`bash
grep "<workspace-name>" CODEOWNERS
\`\`\`
```

### Priority 2: Enhance Smoke Test Guidance

In Phase 4, add explicit smoke test requirements:

```markdown
### 4.1.1 Smoke Test Configuration

Your metadata files MUST include `appConfigExamples` for smoke tests to work.

**Without this:**
- Smoke tests will skip your plugin
- Auto-merge won't be possible
- Updates will require manual review

**Example:**
\`\`\`yaml
spec:
  appConfigExamples:
    - title: Basic Configuration
      content: |
        app:
          extensions:
            - package: "@scope/plugin-name"
              pluginId: your-plugin-id
\`\`\`
```

### Priority 3: Clarify Gating

In Phase 6, be explicit about who approves:

```markdown
### 6.1 Request Review

**For first-time contributors:**
Your PR requires approval from a root code owner:
- @redhat-developer/rhdh-cope
- @gashcrumb
- @tkral

They will verify:
- [ ] License is compatible
- [ ] Upstream is active and maintained
- [ ] CODEOWNERS entry added for your workspace
```

---

## Success Criteria

Onboarding is complete when:

- [x] Workspace exists with source.json + plugins-list.yaml
- [x] /publish succeeds with OCI images
- [x] Metadata files with appConfigExamples (smoke test ready)
- [ ] **CODEOWNERS entry exists** ← enforce this
- [x] Plugin tested locally
- [x] PR merged

After merge:

- Plugin owner receives auto-generated update PRs
- Plugin owner can approve/merge updates for their workspace
- Core team only involved for exceptional issues

---

## Open Questions

1. Should we auto-check CODEOWNERS via GitHub Action or just document?
2. Should Phase 4 (metadata) be required before first merge, or can it be follow-up?
3. How to handle PRs from bots/automation that add new workspaces?
