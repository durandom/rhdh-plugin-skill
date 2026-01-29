# RHDH Plugin Skill

A Claude Code skill for managing Red Hat Developer Hub plugins — onboarding, updating, and triaging plugins in the Extensions Catalog.

## Installation

### From Local Checkout (Development)

```bash
claude plugin marketplace add ~/src/rhdh/store-manager/rhdh-plugin-skill
claude plugin install --scope project rhdh-plugin
```

### From Published Plugin

```bash
claude plugin marketplace add durandom/rhdh-plugin-skill
claude plugin install --scope project rhdh-plugin
```

> **Note:** Always install in project scope. The skill references repository-specific paths.

## Setup

After installation, run the skill to check environment:

```bash
/rhdh-plugin
```

If `needs_setup: true`, follow the setup instructions to configure required repositories.

## Usage

### Slash Commands

| Command | Description |
|---------|-------------|
| `/onboard-plugin` | Add a new plugin to Extensions Catalog |
| `/update-plugin` | Bump plugin to newer upstream version |
| `/fix-plugin-build` | Debug CI/publish failures |
| `/plugin-status` | Check plugin health |
| `/triage-overlay-prs` | Prioritize open PRs (Core Team) |
| `/analyze-overlay-pr` | Analyze specific PR (Core Team) |

### CLI

```bash
rhdh-plugin                          # Status / orientation
rhdh-plugin setup submodule add --all  # Set up repos as submodules
rhdh-plugin workspace list           # List plugin workspaces
rhdh-plugin doctor                   # Full environment check
```

## License

Apache-2.0
