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
- UI Debugging: Capture screenshots and inspect UI structure for World morphs, Spec presenters, and Roassal visualizations
- Server Configuration: Retrieve and modify server settings dynamically

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

This server provides 22 MCP tools that map to all [PharoSmalltalkInteropServer](https://github.com/mumez/PharoSmalltalkInteropServer/blob/main/spec/openapi.json) APIs:

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

#### UI Debugging

- **`read_screen`**: UI screen reader for debugging Pharo interfaces with screenshot and structure extraction

#### Server Configuration

- **`get_settings`**: Retrieve current server configuration
- **`apply_settings`**: Modify server configuration dynamically

### read_screen Tool

The `read_screen` tool captures screenshots and extracts UI structure for debugging Pharo UI issues.

**Parameters:**

- `target_type` (string, default: 'world'): UI type to inspect ('world' for morphs, 'spec' for windows, 'roassal' for visualizations)
- `capture_screenshot` (boolean, default: true): Include PNG screenshot in response

**Returns:** UI structure with screenshot and human-readable summary

**Usage Examples:**

```python
# Inspect all morphs in World
read_screen(target_type='world')

# Inspect Spec presenter windows
read_screen(target_type='spec', capture_screenshot=false)

# Inspect Roassal visualizations without screenshot (faster)
read_screen(target_type='roassal', capture_screenshot=false)
```

**Extracted Data Includes:**

*World (morphs):*

- Class name and type identification
- Bounds (x, y, width, height coordinates)
- Visibility state
- Background color
- Owner class
- Submorph count
- Text content (if available)

Example output:

```json
{
  "totalMorphs": 12,
  "displayedMorphCount": 1,
  "morphs": [
    {
      "class": "MenubarMorph",
      "visible": true,
      "bounds": {"x": 0, "y": 0, "width": 976, "height": 18},
      "backgroundColor": "(Color r: 0.883... alpha: 0.8)",
      "owner": "WorldMorph",
      "submorphCount": 8
    }
  ]
}
```

*Spec (presenters):*

- Window title and class name
- Geometry (extent, position)
- Window state (maximized, minimized, resizable)
- Decorations (menu, toolbar, statusbar presence)
- Presenter hierarchy (recursive with max depth of 3 levels)
- Presenter class name, child count, and content properties (label, text, value, etc.)
- Enablement and visibility state

Example output:

```json
{
  "windowCount": 1,
  "presenters": [
    {
      "class": "SpWindowPresenter",
      "title": "Welcome",
      "extent": "(700@550)",
      "hasMenu": false,
      "presenter": {
        "class": "StWelcomeBrowser",
        "childCount": 2,
        "isVisible": true,
        "children": []
      }
    }
  ]
}
```

*Roassal (visualizations):*

- Canvas bounds and visibility state
- Canvas class identification
- Background color and zoom level
- Shape details (color, position, extent, label, text)
- Edge details (source, target, color, label)
- Node and edge counts

Example output:

```json
{
  "canvasCount": 1,
  "canvases": [
    {
      "class": "RSAthensMorph",
      "canvasClass": "RSCanvas",
      "bounds": {"x": 203, "y": 145, "width": 490, "height": 467},
      "backgroundColor": "Color blue",
      "zoomLevel": "1.0",
      "shapeCount": 5,
      "shapes": [
        {
          "class": "RSCircle",
          "color": "(Color r: 1.0 g: 0.0 b: 0.0 alpha: 0.2)",
          "position": "(0.0@0.0)",
          "extent": "(5.0@5.0)"
        }
      ],
      "edgeCount": 0,
      "edges": [],
      "nodeCount": 0
    }
  ]
}
```

### Server Configuration Tools

The `get_settings` and `apply_settings` tools provide dynamic server configuration management.

#### get_settings

Retrieve the current server configuration.

**Parameters:** None

**Returns:** Dictionary containing current server settings

**Usage Example:**

```python
# Get current settings
get_settings()
# Returns: {"stackSize": 100, "customKey": "customValue"}
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

#### apply_settings

Modify server configuration dynamically. Settings take effect immediately during the current session.

**Parameters:**

- `settings` (dict): Dictionary containing settings to modify

**Returns:** Success confirmation message

**Usage Example:**

```python
# Apply new settings
apply_settings(settings={"stackSize": 200, "customKey": "customValue"})
# Returns: "Settings applied successfully"
```

**Common Settings:**

| Setting     | Type    | Default | Description                                   |
| ----------- | ------- | ------- | --------------------------------------------- |
| `stackSize` | integer | 100     | Maximum stack trace depth for error reporting |

**Note:** The server accepts arbitrary key-value pairs beyond documented settings, allowing custom configuration options.

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
- **Comprehensive coverage**: All 22 endpoints and error scenarios are tested
- **Fast execution**: Tests complete in under 1 second
- **Reliable results**: Tests are deterministic and don't depend on external state

Test coverage includes:

- HTTP client functionality (`PharoClient` class)
- All 22 Pharo interop operations
- Error handling (connection errors, HTTP errors, JSON parsing errors)
- MCP server initialization and tool registration
- Integration between core functions and MCP tools
