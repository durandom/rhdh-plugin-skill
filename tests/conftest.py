"""Shared pytest fixtures for rhdh-plugin-skill tests."""

import os
import subprocess
from pathlib import Path

import pytest

# Path to the skill root
SKILL_ROOT = Path(__file__).parent.parent
SCRIPTS_DIR = SKILL_ROOT / "scripts"
SKILLS_DIR = SKILL_ROOT / "skills" / "rhdh-plugin"


@pytest.fixture
def skill_root():
    """Return the skill root path."""
    return SKILL_ROOT


@pytest.fixture
def scripts_dir():
    """Return the scripts directory path."""
    return SCRIPTS_DIR


@pytest.fixture
def skills_dir():
    """Return the skills/rhdh-plugin directory path."""
    return SKILLS_DIR


@pytest.fixture
def isolated_env(tmp_path):
    """Create an isolated environment with temp directories.

    Sets up:
    - Temporary config directory (~/.config/rhdh-plugin-skill/)
    - Isolated working directory
    """
    # Create temp config dir
    config_dir = tmp_path / ".config" / "rhdh-plugin-skill"
    config_dir.mkdir(parents=True)

    # Create a mock repo structure
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()

    # Create mock overlay repo
    overlay_dir = repo_dir / "rhdh-plugin-export-overlays"
    overlay_dir.mkdir()
    (overlay_dir / "versions.json").write_text('{"backstage": "1.45.0"}')
    (overlay_dir / "workspaces").mkdir()

    # Create a sample workspace
    sample_workspace = overlay_dir / "workspaces" / "test-plugin"
    sample_workspace.mkdir()
    (sample_workspace / "source.json").write_text('''{
  "repo": "https://github.com/example/test-plugin",
  "repo-ref": "abc123",
  "repo-flat": false,
  "repo-backstage-version": "1.43.0"
}''')
    (sample_workspace / "plugins-list.yaml").write_text("- plugins/test/frontend:\n")

    # Initialize as git repo
    subprocess.run(["git", "init"], cwd=overlay_dir, capture_output=True)
    subprocess.run(["git", "add", "."], cwd=overlay_dir, capture_output=True)
    subprocess.run(
        ["git", "commit", "-m", "init"],
        cwd=overlay_dir,
        capture_output=True,
        env={**os.environ, "GIT_AUTHOR_NAME": "test", "GIT_AUTHOR_EMAIL": "test@test.com",
             "GIT_COMMITTER_NAME": "test", "GIT_COMMITTER_EMAIL": "test@test.com"}
    )

    # Create mock rhdh-local
    local_dir = repo_dir / "rhdh-local"
    local_dir.mkdir()
    (local_dir / "compose.yaml").write_text("services:\n  rhdh:\n    image: rhdh\n")

    old_cwd = os.getcwd()
    os.chdir(tmp_path)

    # Set HOME to temp dir so config goes there
    old_home = os.environ.get("HOME")
    os.environ["HOME"] = str(tmp_path)

    yield {
        "root": tmp_path,
        "config_dir": config_dir,
        "repo_dir": repo_dir,
        "overlay_dir": overlay_dir,
        "local_dir": local_dir,
    }

    os.chdir(old_cwd)
    if old_home:
        os.environ["HOME"] = old_home


def run_cli(*args, cwd=None, env=None):
    """Run the rhdh-plugin CLI and return result.

    Args:
        *args: CLI arguments
        cwd: Working directory
        env: Environment variables (merged with current env)

    Returns:
        subprocess.CompletedProcess with stdout, stderr, returncode
    """
    script_path = SCRIPTS_DIR / "rhdh-plugin"

    run_env = os.environ.copy()
    if env:
        run_env.update(env)

    result = subprocess.run(
        [str(script_path), *args],
        capture_output=True,
        text=True,
        cwd=cwd,
        env=run_env,
    )
    return result


@pytest.fixture
def cli():
    """Fixture providing the run_cli function."""
    return run_cli
