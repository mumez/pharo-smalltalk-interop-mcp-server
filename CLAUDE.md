# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python-based MCP (Model Context Protocol) server designed to communicate with local Pharo Smalltalk images. The server provides an interface for:

- **Code Evaluation**: Execute Smalltalk expressions and return results
- **Code Introspection**: Retrieve source code, comments, and metadata for classes and methods
- **Search & Discovery**: Find classes, traits, methods, references, and implementors
- **Package Management**: Export and import packages in Tonel format
- **Project Installation**: Install projects using Metacello
- **Test Execution**: Run test suites at package or class level

## Development Setup

This project uses `uv` as the Python package manager. Prerequisites:

- Python 3.10 or later
- [uv](https://docs.astral.sh/uv/) package manager
- Pharo with [PharoSmalltalkInteropServer](https://github.com/mumez/PharoSmalltalkInteropServer) installed

### Environment Variables

You can configure the server using environment variables:

- **`PHARO_SIS_PORT`**: Port number for PharoSmalltalkInteropServer (default: 8086)

### Common Commands

```bash
# Install dependencies
uv sync --dev

# Run the MCP server
uv run pharo-smalltalk-interop-mcp-server

# Run the MCP server with custom port
PHARO_SIS_PORT=8081 uv run pharo-smalltalk-interop-mcp-server

# Run tests
uv run pytest

# Run tests with verbose output
uv run pytest -v

# Run linting and formatting
uv run ruff check
uv run ruff format

# Format markdown files
uv run mdformat .

# Run pre-commit hooks
uv run pre-commit run --all-files
```

## Architecture Overview

The codebase follows a layered architecture with clean separation of concerns:

### Core Components

1. **`core.py`** - HTTP client layer

   - `PharoClient` class handles all HTTP communication with PharoSmalltalkInteropServer
   - Connects to `localhost:8086` by default
   - Comprehensive error handling for connection, HTTP, and JSON parsing errors
   - 17 core operations mapped to Pharo API endpoints

1. **`server.py`** - MCP server layer

   - Built on FastMCP framework
   - Decorates core functions with MCP tool registration
   - Exposes 19 MCP tools covering code evaluation, introspection, search, packages, project installation, and testing

### Tool Categories

- **Code Evaluation**: `eval` - Execute Smalltalk expressions
- **Code Introspection**: `get_class_source`, `get_method_source`, `get_class_comment`
- **Search & Discovery**: `search_classes_like`, `search_methods_like`, `search_traits_like`, `search_implementors`, `search_references`, `search_references_to_class`
- **Package Management**: `export_package`, `import_package`, `list_packages`, `list_classes`, `list_extended_classes`, `list_methods`
- **Project Installation**: `install_project` - Install projects using Metacello
- **Test Execution**: `run_package_test`, `run_class_test`

### Key Patterns

- **Singleton HTTP Client**: Global `PharoClient` instance with connection reuse
- **Error Handling**: Structured JSON responses with success/error fields
- **Type Safety**: Full type hints throughout codebase
- **Separation of Concerns**: Core logic separate from MCP decorators

## MCP Integration

The server is designed to be configured in Cursor's mcp.json:

```json
{
  "mcpServers": {
    "pharo-smalltalk-interop-mcp-server": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/pharo-smalltalk-interop-mcp-server",
        "run",
        "pharo-smalltalk-interop-mcp-server"
      ],
      "env": {
        "PHARO_SIS_PORT": "8081"
      }
    }
  }
}
```

Note: The `env` section is optional and can be used to set environment variables for the MCP server.

## Development Notes

- Implementation follows MCP server patterns with FastMCP decorators
- Communication with Pharo uses HTTP to PharoSmalltalkInteropServer (port 8086)
- All operations return structured JSON with success/error status
- Comprehensive test suite with mock-based testing to avoid requiring a live Pharo instance
- Tests cover all 19 endpoints and error scenarios
