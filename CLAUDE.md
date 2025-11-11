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
- **UI Debugging**: Capture screenshots and inspect UI structure for World morphs, Spec presenters, and Roassal visualizations

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
   - Enhanced error handling supporting detailed error information from PharoSmalltalkInteropServer
   - 22 core operations mapped to Pharo API endpoints

1. **`server.py`** - MCP server layer

   - Built on FastMCP framework
   - Decorates core functions with MCP tool registration
   - Exposes 22 MCP tools covering code evaluation, introspection, search, packages, project installation, testing, UI debugging, and server configuration

### Tool Categories

- **Code Evaluation**: `eval` - Execute Smalltalk expressions
- **Code Introspection**: `get_class_source`, `get_method_source`, `get_class_comment`
- **Search & Discovery**: `search_classes_like`, `search_methods_like`, `search_traits_like`, `search_implementors`, `search_references`, `search_references_to_class`
- **Package Management**: `export_package`, `import_package`, `list_packages`, `list_classes`, `list_extended_classes`, `list_methods`
- **Project Installation**: `install_project` - Install projects using Metacello
- **Test Execution**: `run_package_test`, `run_class_test`
- **UI Debugging**: `read_screen` - Capture screenshots and extract UI structure
- **Server Configuration**: `get_settings`, `apply_settings` - Retrieve and modify server configuration

### Key Patterns

- **Singleton HTTP Client**: Global `PharoClient` instance with connection reuse
- **Error Handling**: Structured JSON responses with success/error fields, automatic handling of both simple and detailed error formats
- **Type Safety**: Full type hints throughout codebase
- **Separation of Concerns**: Core logic separate from MCP decorators

## Enhanced Error Handling

The MCP server supports enhanced error information from PharoSmalltalkInteropServer v2.0.0+, providing detailed debugging information while maintaining backward compatibility.

### Error Response Formats

**Simple Error Format** (Legacy compatibility):

```json
{
  "success": false,
  "error": "Class not found: NonExistentClass"
}
```

**Enhanced Error Format** (New detailed format):

```json
{
  "success": false,
  "error": {
    "description": "ZeroDivide: division by zero",
    "stack_trace": "SmallInteger>>/ (SmallInteger.class:123)\nUndefinedObject>>DoIt (DoIt.class:1)\nCompiler>>evaluate:in: (Compiler.class:456)",
    "receiver": {
      "class": "SmallInteger",
      "self": "1",
      "variables": {"value": 1}
    }
  }
}
```

### Usage

MCP tools return error responses directly from the Pharo server. Enhanced errors include:

- **`description`**: Error message
- **`stack_trace`**: Complete stack trace (string)
- **`receiver`**: Object that received the failing message with class, self representation, and instance variables

### Compatibility

- **PharoSmalltalkInteropServer v1.x**: Simple string error messages (backward compatible)
- **PharoSmalltalkInteropServer v2.0.0+**: Enhanced error objects with stack traces and receiver information

The Pharo server uses Python-compatible naming conventions (`stack_trace`, `variables`). No code changes are required when upgrading the Pharo server.

## UI Debugging

The `read_screen` tool provides comprehensive UI inspection capabilities for debugging Pharo interfaces. It captures screenshots and extracts complete UI structure information.

### Supported UI Types

- **`world`**: World morphs (default) - Inspect the Pharo world and all visible morphs
- **`spec`**: Spec windows - Inspect Spec presenters and their hierarchical structure
- **`roassal`**: Roassal visualizations - Inspect Roassal canvas elements and shapes

### Parameters

- **`target_type`**: UI type to inspect (default: `"world"`)
- **`capture_screenshot`**: Include PNG screenshot in response (default: `true`)

### Response Format

```json
{
  "success": true,
  "result": {
    "screenshot": "/tmp/pharo_screenshot_20250105_123456.png",
    "target_type": "world",
    "structure": {
      "morphs": [...],
      "count": 42,
      "details": "..."
    },
    "summary": "World contains 42 morphs including..."
  }
}
```

### Usage Example

```python
# Capture world morphs with screenshot
result = read_screen(target_type="world", capture_screenshot=True)

# Inspect Spec windows without screenshot
result = read_screen(target_type="spec", capture_screenshot=False)

# Inspect Roassal visualizations
result = read_screen(target_type="roassal", capture_screenshot=True)
```

### Screenshot Storage

Screenshots are saved to `/tmp/` with timestamped filenames: `pharo_screenshot_YYYYMMDD_HHMMSS.png`

## Server Configuration

The `get_settings` and `apply_settings` tools provide dynamic server configuration management.

### get_settings

Retrieve the current server configuration:

```python
# Get current settings
result = interop_get_settings()
# Returns: {"success": True, "result": {"stackSize": 100, "customKey": "customValue"}}
```

**Response Format:**

```json
{
  "success": true,
  "result": {
    "stackSize": 100,
    "customKey": "customValue"
  }
}
```

### apply_settings

Modify server configuration dynamically. Settings are passed as a dictionary and wrapped in a `settings` object:

```python
# Apply new settings
settings = {"stackSize": 200, "customKey": "customValue"}
result = interop_apply_settings(settings)
# Returns: {"success": True, "result": "Settings applied successfully"}
```

**Request Format (sent to Pharo server):**

```json
{
  "settings": {
    "stackSize": 200,
    "customKey": "customValue"
  }
}
```

**Response Format:**

```json
{
  "success": true,
  "result": "Settings applied successfully"
}
```

### Common Settings

| Setting     | Type    | Default | Description                                   |
| ----------- | ------- | ------- | --------------------------------------------- |
| `stackSize` | integer | 100     | Maximum stack trace depth for error reporting |

**Note:** The server accepts arbitrary key-value pairs beyond documented settings, allowing custom configuration options.

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
- Enhanced error handling passes through detailed error information from Pharo server
- Comprehensive test suite with mock-based testing to avoid requiring a live Pharo instance
- Tests cover all 22 endpoints and error scenarios
