# Task 07: Plugin Config Setup Guide

**Lifecycle:** Onboard
**Persona:** Plugin Owner

---

## Source Context

> "the test workflow checks that both the back end and front end of the dynamic plugins are correctly loaded using configuration defined in the package-level catalog entities within each workspace's metadata"
> — David Festal, 00:22:02

> "Marcel Hild will try to automate opening a PR for configuration updates so the cope team or plugins team can help with the configuration and make the process more automated"
> — Suggested next steps

---

## Problem

Smoke tests require catalog entity configuration in `metadata/`. New contributors don't know:

- What files are needed
- What format to use
- Where to find examples

Result: Plugins merge without config → smoke tests can't run → can't auto-merge updates.

---

## Required Files

```
workspaces/<plugin>/
└── metadata/
    ├── <plugin-name>-frontend.yaml   # For frontend plugins
    └── <plugin-name>-backend.yaml    # For backend plugins
```

Each file is a Backstage catalog entity with plugin configuration.

---

## Template: Frontend Plugin

```yaml
apiVersion: extensions.backstage.io/v1alpha1
kind: Package
metadata:
  name: {plugin-name}-frontend
  title: {Plugin Title}
  description: {Brief description}
spec:
  type: frontend-plugin
  lifecycle: production
  owner: {your-team}
  packageName: "@{scope}/{plugin-name}"
  dynamicArtifact:
    registry: ghcr.io
    organization: redhat-developer
    repository: rhdh-plugin-export-overlays
  appConfigExamples:
    - title: Basic Configuration
      content: |
        # Example app-config.yaml snippet
        app:
          extensions:
            - package: "@{scope}/{plugin-name}"
              pluginId: {plugin-id}
```

---

## Template: Backend Plugin

```yaml
apiVersion: extensions.backstage.io/v1alpha1
kind: Package
metadata:
  name: {plugin-name}-backend
  title: {Plugin Title} Backend
  description: Backend service for {plugin}
spec:
  type: backend-plugin
  lifecycle: production
  owner: {your-team}
  packageName: "@{scope}/{plugin-name}-backend"
  dynamicArtifact:
    registry: ghcr.io
    organization: redhat-developer
    repository: rhdh-plugin-export-overlays
  appConfigExamples:
    - title: Basic Configuration
      content: |
        backend:
          plugins:
            - package: "@{scope}/{plugin-name}-backend"
              disabled: false
```

---

## Workflow

```
1. DETECT new workspace merged without metadata/
   OR metadata/ without appConfigExamples

2. GENERATE template files based on plugins-list.yaml
   - Parse which plugins are exported (frontend/backend)
   - Create metadata YAML for each

3. OUTPUT
   - Option A: Open PR with generated files
   - Option B: Provide templates for contributor to fill
```

---

## Detection

```bash
# Find workspaces without metadata
for ws in workspaces/*/; do
  if [ ! -d "$ws/metadata" ]; then
    echo "Missing metadata: $ws"
  fi
done

# Find metadata without appConfigExamples
grep -L "appConfigExamples" workspaces/*/metadata/*.yaml 2>/dev/null
```

---

## Implementation

```javascript
async function generatePluginConfig(workspace) {
  // Read plugins-list.yaml
  const pluginsList = await readYaml(`workspaces/${workspace}/plugins-list.yaml`);

  const configs = [];

  for (const plugin of pluginsList.plugins) {
    const isBackend = plugin.name.includes('-backend');
    const template = isBackend ? backendTemplate : frontendTemplate;

    const config = template
      .replace(/{plugin-name}/g, plugin.name)
      .replace(/{scope}/g, plugin.scope || 'backstage')
      .replace(/{plugin-id}/g, plugin.pluginId || plugin.name);

    configs.push({
      filename: `${plugin.name}.yaml`,
      content: config
    });
  }

  return configs;
}
```

---

## Comment Template (for PRs missing config)

```markdown
### ℹ️ Plugin Configuration Needed

Your plugin has been added to the overlay, but smoke tests need configuration to run.

**Please add metadata files:**

Create `workspaces/{workspace}/metadata/` with YAML files for each plugin.

Example for a frontend plugin:
```yaml
[template here]
```

**Reference:**

- [Full documentation](https://github.com/redhat-developer/rhdh-plugin-export-overlays/blob/main/catalog-entities/marketplace/README.md)
- [Example: aws-codebuild](https://github.com/redhat-developer/rhdh-plugin-export-overlays/tree/main/workspaces/aws-codebuild/metadata)

**Why this matters:**

- Enables automated smoke tests
- Allows auto-merge when all checks pass
- Provides configuration examples for users

---
*Automated configuration check*

```

---

## Integration with Onboard Workflow

The existing `onboard-plugin` workflow Phase 4 (Metadata) should:

1. Generate initial templates
2. Guide contributor to fill in specifics
3. Validate required fields

---

## Open Questions

1. Should we auto-generate and open PR, or just provide templates?
2. How to handle plugins with complex configuration?
3. Where to document optional vs required config fields?
