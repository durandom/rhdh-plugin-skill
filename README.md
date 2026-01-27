# RHDH Plugin Skill

A Claude Code skill for managing Red Hat Developer Hub plugins - onboarding, updating, and maintaining plugins in the Extensions Catalog.

## What's Inside

| Category | Count | Description |
|----------|-------|-------------|
| **Commands** | 4 | Slash commands for quick invocation |
| **Skills** | 1 | Router-based skill with 3 workflows |
| **References** | 3 | Domain knowledge for overlay repo, CI, metadata |
| **Templates** | 1 | Workspace file templates |

### Slash Commands

| Command | Description |
|---------|-------------|
| `/onboard-plugin` | Add a new Backstage plugin to Extensions Catalog |
| `/update-plugin` | Bump plugin to newer upstream version |
| `/fix-plugin-build` | Debug and fix CI/publish failures |
| `/plugin-status` | Check plugin health and compatibility |

### Workflows

| Workflow | Description |
|----------|-------------|
| `onboard-plugin` | Full 6-phase process: Discovery → Workspace → PR → Metadata → Verify → Merge |
| `update-plugin` | Version bump with validation |
| `fix-build` | CI debugging with common error patterns |

## Installation

### Option 1: Plugin Marketplace (Recommended)

```bash
# Add the marketplace source
claude plugin marketplace add <org>/rhdh-plugin-skill

# Install the plugin
claude plugin install rhdh-plugin
```

### Option 2: Manual Installation

Copy to your Claude Code configuration:

```bash
# Commands (global, available everywhere)
cp -r commands/* ~/.claude/commands/

# Skills (global, available everywhere)
cp -r skills/* ~/.claude/skills/
```

### Option 3: Git Submodule

Add as a submodule to your project:

```bash
git submodule add <repo-url> rhdh-plugin-skill
```

Then register in your project's `.claude/settings.json`:

```json
{
  "skills": {
    "rhdh-plugin": {
      "path": "rhdh-plugin-skill/skills/rhdh-plugin/SKILL.md"
    }
  }
}
```

## Usage

### Via Slash Commands

```
/onboard-plugin https://github.com/awslabs/backstage-plugins-for-aws
/update-plugin aws-ecs v0.8.0
/fix-plugin-build PR #1234
/plugin-status aws-codebuild
```

### Via Skill Invocation

The skill presents an intake menu:

1. **Onboard a new plugin** — Add upstream plugin to Extensions Catalog
2. **Update plugin version** — Bump to newer upstream commit/tag
3. **Check plugin status** — Verify health and compatibility
4. **Fix build failure** — Debug CI/publish issues

## Structure

```
rhdh-plugin-skill/
├── .claude-plugin/               # Marketplace registration
│   ├── plugin.json               # Plugin manifest
│   └── marketplace.json          # Marketplace metadata
├── commands/                     # Slash command wrappers
│   ├── onboard-plugin.md
│   ├── update-plugin.md
│   ├── fix-plugin-build.md
│   └── plugin-status.md
├── skills/rhdh-plugin/           # Main skill
│   ├── SKILL.md                  # Router + essential principles
│   ├── workflows/                # Step-by-step procedures
│   │   ├── onboard-plugin.md     # Full 6-phase process
│   │   ├── update-plugin.md      # Version bump
│   │   └── fix-build.md          # CI debugging
│   ├── references/               # Domain knowledge
│   │   ├── overlay-repo.md       # Workspace patterns
│   │   ├── ci-feedback.md        # Publish workflow interpretation
│   │   └── metadata-format.md    # Package/Plugin entity specs
│   └── templates/                # Output structures
│       └── workspace-files.md    # source.json, plugins-list.yaml
└── README.md
```

## Related Resources

- [rhdh-plugin-export-overlays](https://github.com/redhat-developer/rhdh-plugin-export-overlays) — Overlay repository for plugin exports
- [rhdh-local](https://github.com/redhat-developer/rhdh-local) — Local testing environment
- [rhdh-dynamic-plugin-factory](https://github.com/redhat-developer/rhdh-dynamic-plugin-factory) — Container for local builds

## License

Apache-2.0
