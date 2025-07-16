"""Core functions for Pharo MCP server without FastMCP decorators."""

import json
import os
from typing import Any

import httpx


class PharoInteropError(Exception):
    """Custom exception for Pharo interop errors."""

    pass


class PharoClient:
    """HTTP client for communicating with PharoSmalltalkInteropServer."""

    def __init__(self, host: str = "localhost", port: int | None = None):
        if port is None:
            port = int(os.getenv("PHARO_SIS_PORT", "8086"))
        self.base_url = f"http://{host}:{port}"
        self.client = httpx.Client(timeout=30.0)

    def _make_request(
        self, method: str, endpoint: str, data: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """Make HTTP request to Pharo server."""
        url = f"{self.base_url}{endpoint}"
        try:
            if method.upper() == "GET":
                response = self.client.get(url, params=data)
            else:
                response = self.client.post(url, json=data)

            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            return {"success": False, "error": f"Connection error: {e}"}
        except httpx.HTTPStatusError as e:
            return {
                "success": False,
                "error": f"HTTP error {e.response.status_code}: {e.response.text}",
            }
        except json.JSONDecodeError as e:
            return {"success": False, "error": f"Invalid JSON response: {e}"}

    def evaluate(self, code: str) -> dict[str, Any]:
        """Evaluate Smalltalk expression."""
        data = {"code": code}
        return self._make_request("POST", "/eval", data)

    def get_class_source(self, class_name: str) -> dict[str, Any]:
        """Get source code of a class."""
        data = {"class_name": class_name}
        return self._make_request("GET", "/get-class-source", data)

    def get_method_source(self, class_name: str, method_name: str) -> dict[str, Any]:
        """Get source code of a method."""
        data = {"class_name": class_name, "method_name": method_name}
        return self._make_request("GET", "/get-method-source", data)

    def search_classes_like(self, class_name_query: str) -> dict[str, Any]:
        """Find classes matching pattern."""
        data = {"class_name_query": class_name_query}
        return self._make_request("GET", "/search-classes-like", data)

    def search_methods_like(self, method_name_query: str) -> dict[str, Any]:
        """Find methods matching pattern."""
        data = {"method_name_query": method_name_query}
        return self._make_request("GET", "/search-methods-like", data)

    def search_implementors(self, selector: str) -> dict[str, Any]:
        """Get implementors of a selector."""
        data = {"method_name": selector}
        return self._make_request("GET", "/search-implementors", data)

    def search_references(self, program_symbol: str) -> dict[str, Any]:
        """Get references to a selector."""
        data = {"program_symbol": program_symbol}
        return self._make_request("GET", "/search-references", data)

    def export_package(self, package_name: str, path: str = "/tmp") -> dict[str, Any]:
        """Export package in Tonel format."""
        data = {"package_name": package_name, "path": path}
        return self._make_request("GET", "/export-package", data)

    def import_package(self, package_name: str, path: str = "/tmp") -> dict[str, Any]:
        """Import package from Tonel format."""
        data = {"package_name": package_name, "path": path}
        return self._make_request("GET", "/import-package", data)

    def run_package_test(self, package_name: str) -> dict[str, Any]:
        """Run tests for a package."""
        data = {"package_name": package_name}
        return self._make_request("GET", "/run-package-test", data)

    def run_class_test(self, class_name: str) -> dict[str, Any]:
        """Run tests for a class."""
        data = {"class_name": class_name}
        return self._make_request("GET", "/run-class-test", data)

    def list_packages(self) -> dict[str, Any]:
        """List all packages."""
        return self._make_request("GET", "/list-packages")

    def list_classes(self, package_name: str) -> dict[str, Any]:
        """List classes in a package."""
        data = {"package_name": package_name}
        return self._make_request("GET", "/list-classes", data)

    def get_class_comment(self, class_name: str) -> dict[str, Any]:
        """Get comment of a class."""
        data = {"class_name": class_name}
        return self._make_request("GET", "/get-class-comment", data)

    def list_extended_classes(self, package_name: str) -> dict[str, Any]:
        """List extended classes in a package."""
        data = {"package_name": package_name}
        return self._make_request("GET", "/list-extended-classes", data)

    def list_methods(self, package_name: str) -> dict[str, Any]:
        """List methods in a package."""
        data = {"package_name": package_name}
        return self._make_request("GET", "/list-methods", data)

    def search_traits_like(self, pattern: str) -> dict[str, Any]:
        """Find traits matching pattern."""
        data = {"trait_name_query": pattern}
        return self._make_request("GET", "/search-traits-like", data)

    def search_references_to_class(self, class_name: str) -> dict[str, Any]:
        """Find references to a class."""
        data = {"class_name": class_name}
        return self._make_request("GET", "/search-references-to-class", data)

    def close(self):
        """Close the HTTP client."""
        self.client.close()


# Global client instance
_pharo_client = None


def get_pharo_client() -> PharoClient:
    """Get or create global Pharo client instance."""
    global _pharo_client
    if _pharo_client is None:
        _pharo_client = PharoClient()
    return _pharo_client


def interop_eval(code: str) -> dict[str, Any]:
    """
    Evaluate a Pharo Smalltalk expression with PharoSmalltalkInteropServer.

    Args:
        code: The Smalltalk code to evaluate

    Returns:
        API response with success/error and result
    """
    client = get_pharo_client()
    return client.evaluate(code)


def interop_get_class_source(class_name: str) -> dict[str, Any]:
    """Get source code of a class."""
    client = get_pharo_client()
    return client.get_class_source(class_name)


def interop_get_method_source(class_name: str, method_name: str) -> dict[str, Any]:
    """Get source code of a method."""
    client = get_pharo_client()
    return client.get_method_source(class_name, method_name)


def interop_search_classes_like(class_name_query: str) -> dict[str, Any]:
    """Find classes matching pattern."""
    client = get_pharo_client()
    return client.search_classes_like(class_name_query)


def interop_search_methods_like(method_name_query: str) -> dict[str, Any]:
    """Find methods matching pattern."""
    client = get_pharo_client()
    return client.search_methods_like(method_name_query)


def interop_search_implementors(selector: str) -> dict[str, Any]:
    """Get implementors of a selector."""
    client = get_pharo_client()
    return client.search_implementors(selector)


def interop_search_references(program_symbol: str) -> dict[str, Any]:
    """Get references to a selector."""
    client = get_pharo_client()
    return client.search_references(program_symbol)


def interop_export_package(package_name: str, path: str = "/tmp") -> dict[str, Any]:
    """Export package in Tonel format."""
    client = get_pharo_client()
    return client.export_package(package_name, path)


def interop_import_package(package_name: str, path: str = "/tmp") -> dict[str, Any]:
    """Import package from specified path."""
    client = get_pharo_client()
    return client.import_package(package_name, path)


def interop_run_package_test(package_name: str) -> dict[str, Any]:
    """Run tests for a package."""
    client = get_pharo_client()
    return client.run_package_test(package_name)


def interop_run_class_test(class_name: str) -> dict[str, Any]:
    """Run tests for a class."""
    client = get_pharo_client()
    return client.run_class_test(class_name)


def interop_list_packages() -> dict[str, Any]:
    """List all packages."""
    client = get_pharo_client()
    return client.list_packages()


def interop_list_classes(package_name: str) -> dict[str, Any]:
    """List classes in a package."""
    client = get_pharo_client()
    return client.list_classes(package_name)


def interop_get_class_comment(class_name: str) -> dict[str, Any]:
    """Get comment of a class."""
    client = get_pharo_client()
    return client.get_class_comment(class_name)


def interop_list_extended_classes(package_name: str) -> dict[str, Any]:
    """List extended classes in a package."""
    client = get_pharo_client()
    return client.list_extended_classes(package_name)


def interop_list_methods(package_name: str) -> dict[str, Any]:
    """List methods in a package."""
    client = get_pharo_client()
    return client.list_methods(package_name)


def interop_search_traits_like(pattern: str) -> dict[str, Any]:
    """Find traits matching pattern."""
    client = get_pharo_client()
    return client.search_traits_like(pattern)


def interop_search_references_to_class(class_name: str) -> dict[str, Any]:
    """Find references to a class."""
    client = get_pharo_client()
    return client.search_references_to_class(class_name)
