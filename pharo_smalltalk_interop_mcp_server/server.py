"""FastMCP server for Pharo Smalltalk evaluation."""

from typing import Any

from fastmcp import Context, FastMCP

from .core import (
    interop_eval,
    interop_export_package,
    interop_get_class_comment,
    interop_get_class_source,
    interop_get_method_source,
    interop_import_package,
    interop_list_classes,
    interop_list_extended_classes,
    interop_list_methods,
    interop_list_packages,
    interop_run_class_test,
    interop_run_package_test,
    interop_search_classes_like,
    interop_search_implementors,
    interop_search_methods_like,
    interop_search_references,
    interop_search_references_to_class,
    interop_search_traits_like,
)

mcp = FastMCP("pharo-smalltalk-interop-mcp-server")


@mcp.tool("eval")
def eval_code(_: Context, code: str) -> dict[str, Any]:
    """
    Evaluate a Pharo Smalltalk expression with PharoSmalltalkInteropServer.

    Args:
        code: The Smalltalk code to evaluate

    Returns:
        API response with success/error and result
    """
    return interop_eval(code)


@mcp.tool("get_class_source")
def get_class_source(_: Context, class_name: str) -> dict[str, Any]:
    """
    Get the source code of a Smalltalk class.

    Args:
        class_name: The name of the class to retrieve source for

    Returns:
        API response with success/error and result
    """
    return interop_get_class_source(class_name)


@mcp.tool("get_method_source")
def get_method_source(_: Context, class_name: str, method_name: str) -> dict[str, Any]:
    """
    Get the source code of a specific method in a class.

    Args:
        class_name: The name of the class containing the method
        method_name: The name of the method to retrieve source for

    Returns:
        API response with success/error and result
    """
    return interop_get_method_source(class_name, method_name)


@mcp.tool("get_class_comment")
def get_class_comment(_: Context, class_name: str) -> dict[str, Any]:
    """
    Get the comment of a Smalltalk class.

    Args:
        class_name: The name of the class to retrieve comment for

    Returns:
        API response with success/error and result
    """
    return interop_get_class_comment(class_name)


@mcp.tool("search_classes_like")
def search_classes_like(_: Context, pattern: str) -> dict[str, Any]:
    """
    Find classes matching a pattern.

    Args:
        pattern: The pattern to search for in class names

    Returns:
        API response with success/error and result
    """
    return interop_search_classes_like(pattern)


@mcp.tool("search_methods_like")
def search_methods_like(_: Context, pattern: str) -> dict[str, Any]:
    """
    Find methods matching a pattern.

    Args:
        pattern: The pattern to search for in method names

    Returns:
        API response with success/error and result
    """
    return interop_search_methods_like(pattern)


@mcp.tool("search_implementors")
def search_implementors(_: Context, selector: str) -> dict[str, Any]:
    """
    Get all implementors of a method selector.

    Args:
        selector: The method selector to find implementors for

    Returns:
        API response with success/error and result
    """
    return interop_search_implementors(selector)


@mcp.tool("search_references")
def search_references(_: Context, selector: str) -> dict[str, Any]:
    """
    Get all references to a method selector.

    Args:
        selector: The method selector to find references for

    Returns:
        API response with success/error and result
    """
    return interop_search_references(selector)


@mcp.tool("list_packages")
def list_packages(_: Context) -> dict[str, Any]:
    """
    Get list of all packages.

    Returns:
        API response with success/error and result
    """
    return interop_list_packages()


@mcp.tool("list_classes")
def list_classes(_: Context, package_name: str) -> dict[str, Any]:
    """
    Get list of classes in a package.

    Args:
        package_name: The name of the package

    Returns:
        API response with success/error and result
    """
    return interop_list_classes(package_name)


@mcp.tool("export_package")
def export_package(_: Context, package_name: str) -> dict[str, Any]:
    """
    Export a package in Tonel format.

    Args:
        package_name: The name of the package to export

    Returns:
        API response with success/error and result
    """
    return interop_export_package(package_name)


@mcp.tool("import_package")
def import_package(_: Context, tonel_content: str) -> dict[str, Any]:
    """
    Import a package from Tonel format.

    Args:
        tonel_content: The package content in Tonel format

    Returns:
        API response with success/error and result
    """
    return interop_import_package(tonel_content)


@mcp.tool("run_package_test")
def run_package_test(_: Context, package_name: str) -> dict[str, Any]:
    """
    Run tests for a package.

    Args:
        package_name: The package name to run tests for

    Returns:
        API response with success/error and result
    """
    return interop_run_package_test(package_name)


@mcp.tool("run_class_test")
def run_class_test(_: Context, class_name: str) -> dict[str, Any]:
    """
    Run tests for a class.

    Args:
        class_name: The class name to run tests for

    Returns:
        API response with success/error and result
    """
    return interop_run_class_test(class_name)


@mcp.tool("list_extended_classes")
def list_extended_classes(_: Context, package_name: str) -> dict[str, Any]:
    """
    Get list of extended classes in a package.

    Args:
        package_name: The name of the package

    Returns:
        API response with success/error and result
    """
    return interop_list_extended_classes(package_name)


@mcp.tool("list_methods")
def list_methods(_: Context, package_name: str) -> dict[str, Any]:
    """
    Get list of methods in a package.

    Args:
        package_name: The name of the package

    Returns:
        API response with success/error and result
    """
    return interop_list_methods(package_name)


@mcp.tool("search_traits_like")
def search_traits_like(_: Context, pattern: str) -> dict[str, Any]:
    """
    Find traits matching a pattern.

    Args:
        pattern: The pattern to search for in trait names

    Returns:
        API response with success/error and result
    """
    return interop_search_traits_like(pattern)


@mcp.tool("search_references_to_class")
def search_references_to_class(_: Context, class_name: str) -> dict[str, Any]:
    """
    Find references to a class.

    Args:
        class_name: The name of the class to find references for

    Returns:
        API response with success/error and result
    """
    return interop_search_references_to_class(class_name)


def main():
    """Main entry point for the server."""
    mcp.run()


if __name__ == "__main__":
    main()
