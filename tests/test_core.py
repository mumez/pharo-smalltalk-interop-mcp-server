"""Tests for core module."""

import json
from unittest.mock import Mock, patch

import httpx

from pharo_smalltalk_interop_mcp_server.core import (
    PharoClient,
    get_pharo_client,
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


class TestPharoClient:
    """Test PharoClient class."""

    def test_init(self):
        """Test PharoClient initialization."""
        client = PharoClient()
        assert client.base_url == "http://localhost:8086"
        assert client.client.timeout.connect == 30.0

    def test_init_with_custom_host_port(self):
        """Test PharoClient initialization with custom host and port."""
        client = PharoClient(host="example.com", port=9999)
        assert client.base_url == "http://example.com:9999"

    @patch.dict("os.environ", {"PHARO_SIS_PORT": "8081"})
    def test_init_with_environment_variable(self):
        """Test PharoClient initialization with environment variable."""
        client = PharoClient()
        assert client.base_url == "http://localhost:8081"

    @patch.dict("os.environ", {"PHARO_SIS_PORT": "8081"})
    def test_init_explicit_port_overrides_env(self):
        """Test that explicit port parameter overrides environment variable."""
        client = PharoClient(port=9999)
        assert client.base_url == "http://localhost:9999"

    @patch.dict("os.environ", {}, clear=True)
    def test_init_default_port_when_no_env(self):
        """Test default port is used when no environment variable is set."""
        client = PharoClient()
        assert client.base_url == "http://localhost:8086"

    @patch("pharo_smalltalk_interop_mcp_server.core.httpx.Client")
    def test_make_request_get_success(self, mock_client_class):
        """Test successful GET request."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.json.return_value = {"success": True, "result": "test"}
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = PharoClient()
        result = client._make_request("GET", "/test", {"param": "value"})

        assert result == {"success": True, "result": "test"}
        mock_client.get.assert_called_once_with(
            "http://localhost:8086/test", params={"param": "value"}
        )
        mock_response.raise_for_status.assert_called_once()

    @patch("pharo_smalltalk_interop_mcp_server.core.httpx.Client")
    def test_make_request_post_success(self, mock_client_class):
        """Test successful POST request."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.json.return_value = {"success": True, "result": "test"}
        mock_client.post.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = PharoClient()
        result = client._make_request("POST", "/test", {"data": "value"})

        assert result == {"success": True, "result": "test"}
        mock_client.post.assert_called_once_with(
            "http://localhost:8086/test", json={"data": "value"}
        )
        mock_response.raise_for_status.assert_called_once()

    @patch("pharo_smalltalk_interop_mcp_server.core.httpx.Client")
    def test_make_request_connection_error(self, mock_client_class):
        """Test connection error handling."""
        mock_client = Mock()
        mock_client.get.side_effect = httpx.RequestError("Connection failed")
        mock_client_class.return_value = mock_client

        client = PharoClient()
        result = client._make_request("GET", "/test")

        assert result == {
            "success": False,
            "error": "Connection error: Connection failed",
        }

    @patch("pharo_smalltalk_interop_mcp_server.core.httpx.Client")
    def test_make_request_http_error(self, mock_client_class):
        """Test HTTP error handling."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.text = "Server Error"
        mock_client.get.side_effect = httpx.HTTPStatusError(
            "Server Error", request=Mock(), response=mock_response
        )
        mock_client_class.return_value = mock_client

        client = PharoClient()
        result = client._make_request("GET", "/test")

        assert result == {"success": False, "error": "HTTP error 500: Server Error"}

    @patch("pharo_smalltalk_interop_mcp_server.core.httpx.Client")
    def test_make_request_json_decode_error(self, mock_client_class):
        """Test JSON decode error handling."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.json.side_effect = json.JSONDecodeError("Invalid JSON", "", 0)
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = PharoClient()
        result = client._make_request("GET", "/test")

        assert result["success"] is False
        assert "Invalid JSON response" in result["error"]

    @patch("pharo_smalltalk_interop_mcp_server.core.httpx.Client")
    def test_evaluate(self, mock_client_class):
        """Test evaluate method."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.json.return_value = {"success": True, "result": "42"}
        mock_client.post.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = PharoClient()
        result = client.evaluate("1 + 1")

        assert result == {"success": True, "result": "42"}
        mock_client.post.assert_called_once_with(
            "http://localhost:8086/eval", json={"code": "1 + 1"}
        )

    @patch("pharo_smalltalk_interop_mcp_server.core.httpx.Client")
    def test_get_class_source(self, mock_client_class):
        """Test get_class_source method."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.json.return_value = {"success": True, "result": "class source"}
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = PharoClient()
        result = client.get_class_source("Object")

        assert result == {"success": True, "result": "class source"}
        mock_client.get.assert_called_once_with(
            "http://localhost:8086/get-class-source", params={"class_name": "Object"}
        )

    @patch("pharo_smalltalk_interop_mcp_server.core.httpx.Client")
    def test_get_method_source(self, mock_client_class):
        """Test get_method_source method."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.json.return_value = {"success": True, "result": "method source"}
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = PharoClient()
        result = client.get_method_source("Object", "hash")

        assert result == {"success": True, "result": "method source"}
        mock_client.get.assert_called_once_with(
            "http://localhost:8086/get-method-source",
            params={"class_name": "Object", "method_name": "hash"},
        )

    @patch("pharo_smalltalk_interop_mcp_server.core.httpx.Client")
    def test_search_classes_like(self, mock_client_class):
        """Test search_classes_like method."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "result": ["String", "Symbol"],
        }
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = PharoClient()
        result = client.search_classes_like("Str*")

        assert result == {"success": True, "result": ["String", "Symbol"]}
        mock_client.get.assert_called_once_with(
            "http://localhost:8086/search-classes-like",
            params={"class_name_query": "Str*"},
        )

    @patch("pharo_smalltalk_interop_mcp_server.core.httpx.Client")
    def test_search_methods_like(self, mock_client_class):
        """Test search_methods_like method."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.json.return_value = {"success": True, "result": ["add:", "at:"]}
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = PharoClient()
        result = client.search_methods_like("a*:")

        assert result == {"success": True, "result": ["add:", "at:"]}
        mock_client.get.assert_called_once_with(
            "http://localhost:8086/search-methods-like",
            params={"method_name_query": "a*:"},
        )

    @patch("pharo_smalltalk_interop_mcp_server.core.httpx.Client")
    def test_search_implementors(self, mock_client_class):
        """Test search_implementors method."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "result": ["Object", "ProtoObject"],
        }
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = PharoClient()
        result = client.search_implementors("hash")

        assert result == {"success": True, "result": ["Object", "ProtoObject"]}
        mock_client.get.assert_called_once_with(
            "http://localhost:8086/search-implementors", params={"method_name": "hash"}
        )

    @patch("pharo_smalltalk_interop_mcp_server.core.httpx.Client")
    def test_search_references(self, mock_client_class):
        """Test search_references method."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "result": ["Class1", "Class2"],
        }
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = PharoClient()
        result = client.search_references("hash")

        assert result == {"success": True, "result": ["Class1", "Class2"]}
        mock_client.get.assert_called_once_with(
            "http://localhost:8086/search-references", params={"program_symbol": "hash"}
        )

    @patch("pharo_smalltalk_interop_mcp_server.core.httpx.Client")
    def test_export_package(self, mock_client_class):
        """Test export_package method."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.json.return_value = {"success": True, "result": "tonel content"}
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = PharoClient()
        result = client.export_package("MyPackage")

        assert result == {"success": True, "result": "tonel content"}
        mock_client.get.assert_called_once_with(
            "http://localhost:8086/export-package",
            params={"package_name": "MyPackage", "path": "/tmp"},
        )

    @patch("pharo_smalltalk_interop_mcp_server.core.httpx.Client")
    def test_import_package(self, mock_client_class):
        """Test import_package method."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.json.return_value = {"success": True, "result": "imported"}
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = PharoClient()
        result = client.import_package("tonel content")

        assert result == {"success": True, "result": "imported"}
        mock_client.get.assert_called_once_with(
            "http://localhost:8086/import-package", params={"tonel": "tonel content"}
        )

    @patch("pharo_smalltalk_interop_mcp_server.core.httpx.Client")
    def test_run_package_test(self, mock_client_class):
        """Test run_package_test method."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.json.return_value = {"success": True, "result": "test results"}
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = PharoClient()
        result = client.run_package_test("MyPackage")

        assert result == {"success": True, "result": "test results"}
        mock_client.get.assert_called_once_with(
            "http://localhost:8086/run-package-test",
            params={"package_name": "MyPackage"},
        )

    @patch("pharo_smalltalk_interop_mcp_server.core.httpx.Client")
    def test_run_class_test(self, mock_client_class):
        """Test run_class_test method."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.json.return_value = {"success": True, "result": "test results"}
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = PharoClient()
        result = client.run_class_test("MyClass")

        assert result == {"success": True, "result": "test results"}
        mock_client.get.assert_called_once_with(
            "http://localhost:8086/run-class-test", params={"class_name": "MyClass"}
        )

    @patch("pharo_smalltalk_interop_mcp_server.core.httpx.Client")
    def test_list_packages(self, mock_client_class):
        """Test list_packages method."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "result": ["Package1", "Package2"],
        }
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = PharoClient()
        result = client.list_packages()

        assert result == {"success": True, "result": ["Package1", "Package2"]}
        mock_client.get.assert_called_once_with(
            "http://localhost:8086/list-packages", params=None
        )

    @patch("pharo_smalltalk_interop_mcp_server.core.httpx.Client")
    def test_list_classes(self, mock_client_class):
        """Test list_classes method."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "result": ["Class1", "Class2"],
        }
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = PharoClient()
        result = client.list_classes("MyPackage")

        assert result == {"success": True, "result": ["Class1", "Class2"]}
        mock_client.get.assert_called_once_with(
            "http://localhost:8086/list-classes", params={"package_name": "MyPackage"}
        )

    @patch("pharo_smalltalk_interop_mcp_server.core.httpx.Client")
    def test_get_class_comment(self, mock_client_class):
        """Test get_class_comment method."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.json.return_value = {"success": True, "result": "class comment"}
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = PharoClient()
        result = client.get_class_comment("Object")

        assert result == {"success": True, "result": "class comment"}
        mock_client.get.assert_called_once_with(
            "http://localhost:8086/get-class-comment", params={"class_name": "Object"}
        )

    @patch("pharo_smalltalk_interop_mcp_server.core.httpx.Client")
    def test_list_extended_classes(self, mock_client_class):
        """Test list_extended_classes method."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "result": ["ExtClass1", "ExtClass2"],
        }
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = PharoClient()
        result = client.list_extended_classes("MyPackage")

        assert result == {"success": True, "result": ["ExtClass1", "ExtClass2"]}
        mock_client.get.assert_called_once_with(
            "http://localhost:8086/list-extended-classes",
            params={"package_name": "MyPackage"},
        )

    @patch("pharo_smalltalk_interop_mcp_server.core.httpx.Client")
    def test_list_methods(self, mock_client_class):
        """Test list_methods method."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "result": ["method1", "method2"],
        }
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = PharoClient()
        result = client.list_methods("MyPackage")

        assert result == {"success": True, "result": ["method1", "method2"]}
        mock_client.get.assert_called_once_with(
            "http://localhost:8086/list-methods", params={"package_name": "MyPackage"}
        )

    @patch("pharo_smalltalk_interop_mcp_server.core.httpx.Client")
    def test_search_traits_like(self, mock_client_class):
        """Test search_traits_like method."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "result": ["Trait1", "Trait2"],
        }
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = PharoClient()
        result = client.search_traits_like("T*")

        assert result == {"success": True, "result": ["Trait1", "Trait2"]}
        mock_client.get.assert_called_once_with(
            "http://localhost:8086/search-traits-like",
            params={"trait_name_query": "T*"},
        )

    @patch("pharo_smalltalk_interop_mcp_server.core.httpx.Client")
    def test_search_references_to_class(self, mock_client_class):
        """Test search_references_to_class method."""
        mock_client = Mock()
        mock_response = Mock()
        mock_response.json.return_value = {
            "success": True,
            "result": ["Class1", "Class2"],
        }
        mock_client.get.return_value = mock_response
        mock_client_class.return_value = mock_client

        client = PharoClient()
        result = client.search_references_to_class("Object")

        assert result == {"success": True, "result": ["Class1", "Class2"]}
        mock_client.get.assert_called_once_with(
            "http://localhost:8086/search-references-to-class",
            params={"class_name": "Object"},
        )

    @patch("pharo_smalltalk_interop_mcp_server.core.httpx.Client")
    def test_close(self, mock_client_class):
        """Test close method."""
        mock_client = Mock()
        mock_client_class.return_value = mock_client

        client = PharoClient()
        client.close()

        mock_client.close.assert_called_once()


class TestGlobalClientFunctions:
    """Test global client functions."""

    @patch("pharo_smalltalk_interop_mcp_server.core._pharo_client", None)
    @patch("pharo_smalltalk_interop_mcp_server.core.PharoClient")
    def test_get_pharo_client_creates_new_instance(self, mock_pharo_client_class):
        """Test get_pharo_client creates new instance when none exists."""
        mock_client = Mock()
        mock_pharo_client_class.return_value = mock_client

        result = get_pharo_client()

        assert result == mock_client
        mock_pharo_client_class.assert_called_once()

    @patch("pharo_smalltalk_interop_mcp_server.core._pharo_client")
    def test_get_pharo_client_returns_existing_instance(self, mock_existing_client):
        """Test get_pharo_client returns existing instance."""
        result = get_pharo_client()

        assert result == mock_existing_client


class TestInteropFunctions:
    """Test interop wrapper functions."""

    @patch("pharo_smalltalk_interop_mcp_server.core.get_pharo_client")
    def test_interop_eval(self, mock_get_client):
        """Test interop_eval function."""
        mock_client = Mock()
        mock_client.evaluate.return_value = {"success": True, "result": "42"}
        mock_get_client.return_value = mock_client

        result = interop_eval("1 + 1")

        assert result == {"success": True, "result": "42"}
        mock_client.evaluate.assert_called_once_with("1 + 1")

    @patch("pharo_smalltalk_interop_mcp_server.core.get_pharo_client")
    def test_interop_get_class_source(self, mock_get_client):
        """Test interop_get_class_source function."""
        mock_client = Mock()
        mock_client.get_class_source.return_value = {
            "success": True,
            "result": "source",
        }
        mock_get_client.return_value = mock_client

        result = interop_get_class_source("Object")

        assert result == {"success": True, "result": "source"}
        mock_client.get_class_source.assert_called_once_with("Object")

    @patch("pharo_smalltalk_interop_mcp_server.core.get_pharo_client")
    def test_interop_get_method_source(self, mock_get_client):
        """Test interop_get_method_source function."""
        mock_client = Mock()
        mock_client.get_method_source.return_value = {
            "success": True,
            "result": "source",
        }
        mock_get_client.return_value = mock_client

        result = interop_get_method_source("Object", "hash")

        assert result == {"success": True, "result": "source"}
        mock_client.get_method_source.assert_called_once_with("Object", "hash")

    @patch("pharo_smalltalk_interop_mcp_server.core.get_pharo_client")
    def test_interop_search_classes_like(self, mock_get_client):
        """Test interop_search_classes_like function."""
        mock_client = Mock()
        mock_client.search_classes_like.return_value = {
            "success": True,
            "result": ["String"],
        }
        mock_get_client.return_value = mock_client

        result = interop_search_classes_like("Str*")

        assert result == {"success": True, "result": ["String"]}
        mock_client.search_classes_like.assert_called_once_with("Str*")

    @patch("pharo_smalltalk_interop_mcp_server.core.get_pharo_client")
    def test_interop_search_methods_like(self, mock_get_client):
        """Test interop_search_methods_like function."""
        mock_client = Mock()
        mock_client.search_methods_like.return_value = {
            "success": True,
            "result": ["add:"],
        }
        mock_get_client.return_value = mock_client

        result = interop_search_methods_like("a*:")

        assert result == {"success": True, "result": ["add:"]}
        mock_client.search_methods_like.assert_called_once_with("a*:")

    @patch("pharo_smalltalk_interop_mcp_server.core.get_pharo_client")
    def test_interop_search_implementors(self, mock_get_client):
        """Test interop_search_implementors function."""
        mock_client = Mock()
        mock_client.search_implementors.return_value = {
            "success": True,
            "result": ["Object"],
        }
        mock_get_client.return_value = mock_client

        result = interop_search_implementors("hash")

        assert result == {"success": True, "result": ["Object"]}
        mock_client.search_implementors.assert_called_once_with("hash")

    @patch("pharo_smalltalk_interop_mcp_server.core.get_pharo_client")
    def test_interop_search_references(self, mock_get_client):
        """Test interop_search_references function."""
        mock_client = Mock()
        mock_client.search_references.return_value = {
            "success": True,
            "result": ["Class1"],
        }
        mock_get_client.return_value = mock_client

        result = interop_search_references("hash")

        assert result == {"success": True, "result": ["Class1"]}
        mock_client.search_references.assert_called_once_with("hash")

    @patch("pharo_smalltalk_interop_mcp_server.core.get_pharo_client")
    def test_interop_export_package(self, mock_get_client):
        """Test interop_export_package function."""
        mock_client = Mock()
        mock_client.export_package.return_value = {"success": True, "result": "tonel"}
        mock_get_client.return_value = mock_client

        result = interop_export_package("MyPackage")

        assert result == {"success": True, "result": "tonel"}
        mock_client.export_package.assert_called_once_with("MyPackage", "/tmp")

    @patch("pharo_smalltalk_interop_mcp_server.core.get_pharo_client")
    def test_interop_import_package(self, mock_get_client):
        """Test interop_import_package function."""
        mock_client = Mock()
        mock_client.import_package.return_value = {
            "success": True,
            "result": "imported",
        }
        mock_get_client.return_value = mock_client

        result = interop_import_package("tonel content")

        assert result == {"success": True, "result": "imported"}
        mock_client.import_package.assert_called_once_with("tonel content")

    @patch("pharo_smalltalk_interop_mcp_server.core.get_pharo_client")
    def test_interop_run_package_test(self, mock_get_client):
        """Test interop_run_package_test function."""
        mock_client = Mock()
        mock_client.run_package_test.return_value = {
            "success": True,
            "result": "test results",
        }
        mock_get_client.return_value = mock_client

        result = interop_run_package_test("MyPackage")

        assert result == {"success": True, "result": "test results"}
        mock_client.run_package_test.assert_called_once_with("MyPackage")

    @patch("pharo_smalltalk_interop_mcp_server.core.get_pharo_client")
    def test_interop_run_class_test(self, mock_get_client):
        """Test interop_run_class_test function."""
        mock_client = Mock()
        mock_client.run_class_test.return_value = {
            "success": True,
            "result": "test results",
        }
        mock_get_client.return_value = mock_client

        result = interop_run_class_test("MyClass")

        assert result == {"success": True, "result": "test results"}
        mock_client.run_class_test.assert_called_once_with("MyClass")

    @patch("pharo_smalltalk_interop_mcp_server.core.get_pharo_client")
    def test_interop_list_packages(self, mock_get_client):
        """Test interop_list_packages function."""
        mock_client = Mock()
        mock_client.list_packages.return_value = {
            "success": True,
            "result": ["Package1"],
        }
        mock_get_client.return_value = mock_client

        result = interop_list_packages()

        assert result == {"success": True, "result": ["Package1"]}
        mock_client.list_packages.assert_called_once()

    @patch("pharo_smalltalk_interop_mcp_server.core.get_pharo_client")
    def test_interop_list_classes(self, mock_get_client):
        """Test interop_list_classes function."""
        mock_client = Mock()
        mock_client.list_classes.return_value = {"success": True, "result": ["Class1"]}
        mock_get_client.return_value = mock_client

        result = interop_list_classes("MyPackage")

        assert result == {"success": True, "result": ["Class1"]}
        mock_client.list_classes.assert_called_once_with("MyPackage")

    @patch("pharo_smalltalk_interop_mcp_server.core.get_pharo_client")
    def test_interop_get_class_comment(self, mock_get_client):
        """Test interop_get_class_comment function."""
        mock_client = Mock()
        mock_client.get_class_comment.return_value = {
            "success": True,
            "result": "comment",
        }
        mock_get_client.return_value = mock_client

        result = interop_get_class_comment("Object")

        assert result == {"success": True, "result": "comment"}
        mock_client.get_class_comment.assert_called_once_with("Object")

    @patch("pharo_smalltalk_interop_mcp_server.core.get_pharo_client")
    def test_interop_list_extended_classes(self, mock_get_client):
        """Test interop_list_extended_classes function."""
        mock_client = Mock()
        mock_client.list_extended_classes.return_value = {
            "success": True,
            "result": ["ExtClass1"],
        }
        mock_get_client.return_value = mock_client

        result = interop_list_extended_classes("MyPackage")

        assert result == {"success": True, "result": ["ExtClass1"]}
        mock_client.list_extended_classes.assert_called_once_with("MyPackage")

    @patch("pharo_smalltalk_interop_mcp_server.core.get_pharo_client")
    def test_interop_list_methods(self, mock_get_client):
        """Test interop_list_methods function."""
        mock_client = Mock()
        mock_client.list_methods.return_value = {"success": True, "result": ["method1"]}
        mock_get_client.return_value = mock_client

        result = interop_list_methods("MyPackage")

        assert result == {"success": True, "result": ["method1"]}
        mock_client.list_methods.assert_called_once_with("MyPackage")

    @patch("pharo_smalltalk_interop_mcp_server.core.get_pharo_client")
    def test_interop_search_traits_like(self, mock_get_client):
        """Test interop_search_traits_like function."""
        mock_client = Mock()
        mock_client.search_traits_like.return_value = {
            "success": True,
            "result": ["Trait1"],
        }
        mock_get_client.return_value = mock_client

        result = interop_search_traits_like("T*")

        assert result == {"success": True, "result": ["Trait1"]}
        mock_client.search_traits_like.assert_called_once_with("T*")

    @patch("pharo_smalltalk_interop_mcp_server.core.get_pharo_client")
    def test_interop_search_references_to_class(self, mock_get_client):
        """Test interop_search_references_to_class function."""
        mock_client = Mock()
        mock_client.search_references_to_class.return_value = {
            "success": True,
            "result": ["Class1"],
        }
        mock_get_client.return_value = mock_client

        result = interop_search_references_to_class("Object")

        assert result == {"success": True, "result": ["Class1"]}
        mock_client.search_references_to_class.assert_called_once_with("Object")
