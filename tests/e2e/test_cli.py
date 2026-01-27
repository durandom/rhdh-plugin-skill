"""End-to-end tests for rhdh-plugin CLI."""


class TestCliStatus:
    """Test CLI status command (no args)."""

    def test_no_args_shows_status(self, cli, isolated_env):
        """Running with no args should show status."""
        # Set SKILL_ROOT to point to our mock repo
        env = {"SKILL_ROOT": str(isolated_env["root"])}
        result = cli(env=env)

        # Should succeed (exit 0)
        assert result.returncode == 0, f"stderr: {result.stderr}"

        # Should show environment header
        assert "RHDH Plugin Environment" in result.stdout

    def test_status_shows_next_steps(self, cli, isolated_env):
        """Status should show next steps."""
        result = cli()

        # Should have next steps section
        assert "Next steps:" in result.stdout

    def test_status_checks_tools(self, cli):
        """Status should check for required tools."""
        result = cli()

        # Should mention tools
        assert "Tools" in result.stdout or "gh CLI" in result.stdout


class TestCliDoctor:
    """Test CLI doctor command."""

    def test_doctor_runs(self, cli):
        """Doctor command should run without error."""
        result = cli("doctor")

        # Should complete (may have issues but shouldn't crash)
        assert result.returncode in [0, 1]
        assert "Environment Check" in result.stdout or "Summary" in result.stdout

    def test_doctor_checks_github(self, cli):
        """Doctor should check GitHub CLI."""
        result = cli("doctor")

        assert "GitHub" in result.stdout or "gh" in result.stdout.lower()

    def test_doctor_shows_summary(self, cli):
        """Doctor should show summary."""
        result = cli("doctor")

        assert "Summary" in result.stdout


class TestCliConfig:
    """Test CLI config commands."""

    def test_config_init_creates_file(self, cli, isolated_env):
        """config init should create config file."""
        result = cli("config", "init")

        assert result.returncode == 0
        assert "Created" in result.stdout or "already exists" in result.stdout

    def test_config_show_displays_config(self, cli, isolated_env):
        """config show should display configuration."""
        # First init
        cli("config", "init")

        result = cli("config", "show")

        assert result.returncode == 0
        assert "Configuration" in result.stdout

    def test_config_set_updates_value(self, cli, isolated_env):
        """config set should update a value."""
        # First init
        cli("config", "init")

        # Set a path (use the mock overlay dir)
        result = cli("config", "set", "overlay", str(isolated_env["overlay_dir"]))

        assert result.returncode == 0
        assert "Set overlay" in result.stdout or "✓" in result.stdout

    def test_config_set_validates_path(self, cli, isolated_env):
        """config set should validate path exists."""
        result = cli("config", "set", "overlay", "/nonexistent/path")

        assert result.returncode != 0
        assert "not exist" in result.stdout or "Error" in result.stdout

    def test_config_set_validates_key(self, cli, isolated_env):
        """config set should validate key name."""
        result = cli("config", "set", "invalid_key", "/tmp")

        assert result.returncode != 0
        assert "Unknown" in result.stdout or "Valid keys" in result.stdout


class TestCliWorkspace:
    """Test CLI workspace commands."""

    def test_workspace_list_works(self, cli, isolated_env):
        """workspace list should show workspaces."""
        # Configure the overlay repo
        cli("config", "init")
        cli("config", "set", "overlay", str(isolated_env["overlay_dir"]))

        result = cli("workspace", "list")

        assert result.returncode == 0
        assert "Plugin Workspaces" in result.stdout or "workspaces" in result.stdout.lower()

    def test_workspace_list_shows_test_plugin(self, cli, isolated_env):
        """workspace list should show our test plugin."""
        # Use env var to override the default discovery
        env = {"RHDH_OVERLAY_REPO": str(isolated_env["overlay_dir"])}

        result = cli("workspace", "list", env=env)

        assert "test-plugin" in result.stdout

    def test_workspace_status_shows_details(self, cli, isolated_env):
        """workspace status should show workspace details."""
        # Use env var to override the default discovery
        env = {"RHDH_OVERLAY_REPO": str(isolated_env["overlay_dir"])}

        result = cli("workspace", "status", "test-plugin", env=env)

        assert result.returncode == 0
        assert "test-plugin" in result.stdout
        assert "source.json" in result.stdout

    def test_workspace_status_unknown_workspace(self, cli, isolated_env):
        """workspace status should error for unknown workspace."""
        cli("config", "set", "overlay", str(isolated_env["overlay_dir"]))

        result = cli("workspace", "status", "nonexistent")

        assert result.returncode != 0
        assert "not found" in result.stdout or "Error" in result.stdout


class TestCliHelp:
    """Test CLI help."""

    def test_help_flag(self, cli):
        """--help should show help."""
        result = cli("--help")

        assert result.returncode == 0
        assert "rhdh-plugin" in result.stdout
        assert "COMMANDS" in result.stdout or "USAGE" in result.stdout

    def test_help_command(self, cli):
        """help command should show help."""
        result = cli("help")

        assert result.returncode == 0
        assert "rhdh-plugin" in result.stdout


class TestCliUnknownCommand:
    """Test CLI handles unknown commands."""

    def test_unknown_command_errors(self, cli):
        """Unknown command should show error."""
        result = cli("unknown_command")

        assert result.returncode != 0
        assert "Unknown" in result.stdout or "--help" in result.stdout


class TestCliEnvironmentVariables:
    """Test CLI respects environment variables."""

    def test_overlay_env_var(self, cli, isolated_env):
        """RHDH_OVERLAY_REPO env var should override config."""
        env = {"RHDH_OVERLAY_REPO": str(isolated_env["overlay_dir"])}

        result = cli("workspace", "list", env=env)

        assert result.returncode == 0
        assert "test-plugin" in result.stdout
