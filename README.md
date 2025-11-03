# pharo-smalltalk-interop-mcp-server

[![CI](https://github.com/mumez/pharo-smalltalk-interop-mcp-server/actions/workflows/ci.yml/badge.svg)](https://github.com/mumez/pharo-smalltalk-interop-mcp-server/actions/workflows/ci.yml)

A local MCP server to communicate local Pharo Smalltalk image.
It supports:

- Code Evaluation: Execute Smalltalk expressions and return results
- Code Introspection: Retrieve source code, comments, and metadata for classes and methods
- Search & Discovery: Find classes, traits, methods, references, and implementors
- Package Management: Export and import packages in Tonel format
- Project Installation: Install projects using Metacello
- Test Execution: Run test suites at package or class level

## Prerequisites

- Python 3.10 or later
- [uv](https://docs.astral.sh/uv/) package manager
- Pharo with [PharoSmalltalkInteropServer](https://github.com/mumez/PharoSmalltalkInteropServer) installed

## Installation

### Quick Start (using uvx)

The easiest way to run the server without cloning the repository:

```bash
uvx --from git+https://github.com/mumez/pharo-smalltalk-interop-mcp-server.git pharo-smalltalk-interop-mcp-server
```

### Development Installation

To set up for development:

1. Clone the repository:

```bash
git clone https://github.com/mumez/pharo-smalltalk-interop-mcp-server.git
```

2. Install dependencies using uv:

```bash
cd pharo-smalltalk-interop-mcp-server
uv sync --dev
```

## Usage

### Running the MCP Server

**Using uvx (no installation required):**

```bash
uvx --from git+https://github.com/mumez/pharo-smalltalk-interop-mcp-server.git pharo-smalltalk-interop-mcp-server
```

**Using uv (after cloning the repository):**

```bash
uv run pharo-smalltalk-interop-mcp-server
```

#### Environment Variables

You can configure the server using environment variables:

- **`PHARO_SIS_PORT`**: Port number for PharoSmalltalkInteropServer (default: 8086)

Examples:

**Using uvx:**
```bash
PHARO_SIS_PORT=8086 uvx --from git+https://github.com/mumez/pharo-smalltalk-interop-mcp-server.git pharo-smalltalk-interop-mcp-server
```

**Using uv:**
```bash
PHARO_SIS_PORT=9999 uv run pharo-smalltalk-interop-mcp-server
```

### Cursor MCP settings

**Using uvx (recommended):**
```json:mcp.json
{
  "mcpServers": {
    "smalltalk-interop": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/mumez/pharo-smalltalk-interop-mcp-server.git",
        "pharo-smalltalk-interop-mcp-server"
      ],
      "env": {
        "PHARO_SIS_PORT": "8086"
      }
    }
  }
}
```

**Using uv (after cloning):**
```json:mcp.json
{
  "mcpServers": {
    "smalltalk-interop": {
      "command": "uv",
      "args": [
        "--directory",
        "/your-path/to/pharo-smalltalk-interop-mcp-server",
        "run",
        "pharo-smalltalk-interop-mcp-server"
      ],
      "env": {
        "PHARO_SIS_PORT": "8086"
      }
    }
  }
}
```

Note: The `env` section is optional and can be used to set environment variables for the MCP server.

### Claude Code Configuration

**Using uvx (recommended):**
```bash
claude mcp add -s user smalltalk-interop -- uvx --from git+https://github.com/mumez/pharo-smalltalk-interop-mcp-server.git pharo-smalltalk-interop-mcp-server
```

**Using uv (after cloning):**
```bash
claude mcp add -s user smalltalk-interop -- uv --directory /path/to/pharo-smalltalk-interop-mcp-server run pharo-smalltalk-interop-mcp-server
```

### MCP Tools Available

This server provides 19 MCP tools that map to all [PharoSmalltalkInteropServer](https://github.com/mumez/PharoSmalltalkInteropServer/blob/main/spec/openapi.json) APIs:

#### Code Evaluation

- **`eval`**: Execute Smalltalk expressions and return results

#### Code Introspection

- **`get_class_source`**: Retrieve source code of a class
- **`get_method_source`**: Retrieve source code of a specific method
- **`get_class_comment`**: Retrieve comment/documentation of a class

#### Search & Discovery

- **`search_classes_like`**: Find classes matching a pattern
- **`search_methods_like`**: Find methods matching a pattern
- **`search_traits_like`**: Find traits matching a pattern
- **`search_implementors`**: Find all implementors of a method selector
- **`search_references`**: Find all references to a method selector
- **`search_references_to_class`**: Find all references to a class

#### Package Management

- **`list_packages`**: List all packages in the image
- **`list_classes`**: List classes in a specific package
- **`list_extended_classes`**: List extended classes in a package
- **`list_methods`**: List methods in a package
- **`export_package`**: Export a package in Tonel format
- **`import_package`**: Import a package from specified path

#### Project Installation

- **`install_project`**: Install a project using Metacello with optional load groups

#### Test Execution

- **`run_package_test`**: Run test suites for a package
- **`run_class_test`**: Run test suites for a specific class

## Development

### Running Tests

The project includes comprehensive unit tests with mock-based testing to avoid requiring a live Pharo instance:

```bash
# Run all tests
uv run pytest

# Run tests with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_core.py -v
```

### Code Quality

```bash
# Run linting
uv run ruff check

# Run formatting
uv run ruff format

# Run all pre-commit hooks
uv run pre-commit run --all-files
```

### Project Structure

```
pharo-smalltalk-interop-mcp-server/
├── pharo_smalltalk_interop_mcp_server/
│   ├── __init__.py
│   ├── core.py          # HTTP client and core functions
│   └── server.py        # FastMCP server with tool definitions
├── tests/
│   ├── __init__.py
│   ├── test_core.py     # Tests for core HTTP client functionality
│   └── test_server.py   # Tests for MCP server integration
├── pyproject.toml       # Project configuration
├── pytest.ini          # Test configuration
└── README.md
```

### Testing Strategy

The test suite uses mock-based testing to ensure:

- **No external dependencies**: Tests run without requiring a live Pharo instance
- **Comprehensive coverage**: All 19 endpoints and error scenarios are tested
- **Fast execution**: Tests complete in under 1 second
- **Reliable results**: Tests are deterministic and don't depend on external state

Test coverage includes:

- HTTP client functionality (`PharoClient` class)
- All 19 Pharo interop operations
- Error handling (connection errors, HTTP errors, JSON parsing errors)
- MCP server initialization and tool registration
- Integration between core functions and MCP tools
