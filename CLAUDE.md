# CLAUDE.md

## Development Rules

1. **TDD First** — Write tests before implementation, even for markdown files. See `tests/unit/test_skill_structure.py` for examples.

2. **Run Tests** — `uv run pytest` before committing.

## Project Structure

```
rhdh-plugin-skill/
├── skills/rhdh-plugin/    # Self-contained skill
│   ├── rhdh_plugin/       # Python CLI package (stdlib only)
│   ├── scripts/           # Entry point (./scripts/rhdh-plugin)
│   ├── workflows/         # Agent workflows
│   └── SKILL.md           # Skill definition
├── tests/                 # pytest test suite (dev only)
└── pyproject.toml         # Dev dependencies (pytest)
```

## CLI

The CLI is stdlib-only and runs with any Python 3.9+:

```bash
./skills/rhdh-plugin/scripts/rhdh-plugin           # Status check
./skills/rhdh-plugin/scripts/rhdh-plugin doctor    # Full environment check
./skills/rhdh-plugin/scripts/rhdh-plugin --json    # Force JSON output
```

Auto-detects output format: **TTY** → human-readable, **Piped** → JSON.

## Key Patterns

- `OutputFormatter` handles JSON/human rendering — commands build data dicts
- Workflows live in `skills/rhdh-plugin/workflows/` — doctor points agents there for setup
- Config discovery: env vars → project config → user config → auto-detection
