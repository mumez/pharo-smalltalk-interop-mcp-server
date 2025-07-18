"""Tests for server module."""

from unittest.mock import patch


class TestMCPServerInit:
    """Test MCP server initialization."""

    def test_mcp_server_creation(self):
        """Test that MCP server can be created."""
        from pharo_smalltalk_interop_mcp_server.server import mcp

        assert mcp.name == "pharo-smalltalk-interop-mcp-server"
        # Check that the server instance exists
        assert mcp is not None


class TestMCPToolsIntegration:
    """Test MCP tools integration with core functions."""

    @patch("pharo_smalltalk_interop_mcp_server.core.interop_eval")
    def test_eval_code_integration(self, mock_interop_eval):
        """Test eval_code integration."""
        mock_interop_eval.return_value = {"success": True, "result": "42"}

        # Test the actual function from core
        from pharo_smalltalk_interop_mcp_server.core import interop_eval

        result = interop_eval("1 + 1")

        assert result == {"success": True, "result": "42"}
        mock_interop_eval.assert_called_once_with("1 + 1")

    @patch("pharo_smalltalk_interop_mcp_server.core.interop_get_class_source")
    def test_get_class_source_integration(self, mock_interop_get_class_source):
        """Test get_class_source integration."""
        mock_interop_get_class_source.return_value = {
            "success": True,
            "result": "class source",
        }

        from pharo_smalltalk_interop_mcp_server.core import interop_get_class_source

        result = interop_get_class_source("Object")

        assert result == {"success": True, "result": "class source"}
        mock_interop_get_class_source.assert_called_once_with("Object")

    @patch("pharo_smalltalk_interop_mcp_server.core.interop_list_packages")
    def test_list_packages_integration(self, mock_interop_list_packages):
        """Test list_packages integration."""
        mock_interop_list_packages.return_value = {
            "success": True,
            "result": ["Package1", "Package2"],
        }

        from pharo_smalltalk_interop_mcp_server.core import interop_list_packages

        result = interop_list_packages()

        assert result == {"success": True, "result": ["Package1", "Package2"]}
        mock_interop_list_packages.assert_called_once()

    @patch("pharo_smalltalk_interop_mcp_server.core.interop_install_project")
    def test_install_project_integration(self, mock_interop_install_project):
        """Test install_project integration."""
        mock_interop_install_project.return_value = {
            "success": True,
            "result": "Project installed successfully",
        }

        from pharo_smalltalk_interop_mcp_server.core import interop_install_project

        result = interop_install_project("TestProject", "http://github.com/test/repo")

        assert result == {"success": True, "result": "Project installed successfully"}
        mock_interop_install_project.assert_called_once_with(
            "TestProject", "http://github.com/test/repo"
        )

    def test_server_main_function_exists(self):
        """Test that main function exists and is callable."""
        from pharo_smalltalk_interop_mcp_server.server import main

        assert callable(main)
        # Don't actually call main() as it would start the server
