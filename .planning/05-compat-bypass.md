# Task 05: Compatibility Bypass Detector

**Lifecycle:** Active Maintenance
**Persona:** Core Team

---

## Source Context

> "David Festal raised a concern about people manually updating commits in `source.json` to target a newer backstage version than the overlay repository currently supports, thereby bypassing compatibility checks"
> — Meeting notes, 00:14:21

> "this practice is usually unnecessary because automation already attempts to discover new commits, and if one is not discovered, it is often due to incompatibility"
> — David Festal, 00:16:12

> "we end up having in the overlay plugins or workspaces which targets a backstage version which is not compatible with the underlying backstage version"
> — David Festal

---

## Problem

Contributors manually update `source.json` to point to a newer commit that targets a higher Backstage version than the overlay supports. This:

1. Bypasses automated compatibility discovery
2. May introduce incompatible plugins
3. Creates "time bombs" for release branches

**Why automation didn't pick it up:** Usually because the new commit targets an incompatible Backstage version.

---

## Detection Logic

```
1. GET current overlay target Backstage version
   From versions.json in overlay repo

2. FOR each PR modifying source.json:
   a. EXTRACT commit hash from source.json change
   b. FETCH that commit's package.json from upstream
   c. FIND backstage dependency version
   d. COMPARE to overlay target

3. IF upstream backstage > overlay target:
   → FLAG: "Compatibility bypass detected"
   → EXPLAIN: "This commit targets Backstage X.Y but overlay targets X.Z"
```

---

## Key Files

| File | Purpose |
|------|---------|
| `versions.json` | Overlay's target Backstage version |
| `workspaces/<name>/source.json` | Commit hash pointing to upstream |
| `workspaces/<name>/backstage.json` | Optional version override |

---

## versions.json Structure

```json
{
  "backstage": "1.42.5",
  "rhdh": "1.8"
}
```

---

## source.json Structure

```json
{
  "type": "github",
  "owner": "backstage",
  "repo": "community-plugins",
  "commit": "abc123def456"
}
```

---

## Implementation

```javascript
async function checkCompatBypass(pr, overlayVersions) {
  const targetBackstage = overlayVersions.backstage; // e.g., "1.42.5"

  // Get source.json changes from PR
  const sourceChanges = pr.files.filter(f => f.path.endsWith('source.json'));

  for (const file of sourceChanges) {
    const newContent = await getFileFromPR(pr.number, file.path);
    const source = JSON.parse(newContent);

    // Fetch upstream package.json at that commit
    const upstreamPkg = await fetchUpstreamPackage(source);
    const upstreamBackstage = extractBackstageVersion(upstreamPkg);

    if (semver.gt(upstreamBackstage, targetBackstage)) {
      return {
        status: 'bypass',
        workspace: extractWorkspace(file.path),
        upstreamVersion: upstreamBackstage,
        overlayTarget: targetBackstage,
        message: `Commit targets Backstage ${upstreamBackstage} but overlay targets ${targetBackstage}`
      };
    }
  }

  return { status: 'ok' };
}
```

---

## Fetch Upstream Version

```bash
# For community-plugins
COMMIT="abc123"
WORKSPACE="todo"

# Get package.json from upstream at specific commit
gh api repos/backstage/community-plugins/contents/workspaces/$WORKSPACE/package.json?ref=$COMMIT \
  --jq '.content' | base64 -d | jq '.dependencies["@backstage/core-plugin-api"]'
```

---

## Output (in triage)

```markdown
### ⚠️ Compatibility Warnings

| PR | Workspace | Issue |
|----|-----------|-------|
| #1234 | todo | Targets Backstage 1.45.0 but overlay is 1.42.5 |

**Why this matters:**
- Automation didn't discover this commit because it's incompatible
- May break when we cut a release branch
- Consider: Is there a `backstage.json` override? Is this intentional?
```

---

## Valid Exceptions

Sometimes bypassing is intentional:

| Scenario | How to Detect | Action |
|----------|---------------|--------|
| `backstage.json` override present | Check for file | Note but don't block |
| Explicit compatibility note in PR | PR body contains explanation | Reduce severity |
| Patch to fix compatibility | PR includes patches/ changes | Reduce severity |

---

## Integration with Triage

This check runs as part of Task 01 diagnostics:

```
FOR each PR in triage:
  IF modifies source.json:
    RUN compatibility check
    ADD warning to triage output if bypass detected
```

---

## Comment Template

When flagging:

```markdown
### ⚠️ Potential Compatibility Bypass

This PR updates `source.json` to commit `{commit}` which targets **Backstage {upstream_version}**.

The overlay repository currently targets **Backstage {overlay_version}**.

**Why this might be a problem:**
- Automated discovery didn't pick this commit (likely due to version mismatch)
- This plugin may not work correctly with the current RHDH release

**If intentional:**
- Add a `backstage.json` override file
- Or add patches to fix compatibility
- Please note in PR description why this is safe

---
*Automated compatibility check*
```

---

## Open Questions

1. Should we check the actual plugin's Backstage deps or the monorepo root?
2. How to handle plugins with `backstage.json` override already?
3. Block merge or just warn?
