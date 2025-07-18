"""Integration tests for Pharo Smalltalk Interop MCP Server.

These tests communicate with a live PharoSmalltalkInteropServer instance
running on port 8086. They are designed to be version-agnostic and test
the actual functionality of the MCP server.
"""

import glob
import tempfile

import pytest

from pharo_smalltalk_interop_mcp_server.core import PharoClient


class TestPharoIntegration:
    """Integration tests that communicate with live Pharo server."""

    @pytest.fixture(autouse=True)
    def setup_client(self):
        """Setup PharoClient for integration tests."""
        self.client = PharoClient()

        # Test server connectivity first
        try:
            response = self.client.evaluate("1 + 1")
            if not response.get("success", False):
                pytest.skip("Pharo server not available or not responding correctly")
        except Exception as e:
            pytest.skip(f"Cannot connect to Pharo server: {e}")

        yield

        # Cleanup
        self.client.close()

    def test_server_connectivity(self):
        """Test basic server connectivity."""
        response = self.client.evaluate("1 + 1")
        assert response["success"] is True
        assert "result" in response

    def test_eval_basic_arithmetics(self):
        """Test basic arithmetic operations."""
        test_cases = [
            ("1 + 1", "2"),
            ("2 * 3", "6"),
            ("10 / 2", "5"),
            ("5 - 3", "2"),
        ]

        for code, expected in test_cases:
            response = self.client.evaluate(code)
            assert response["success"] is True
            assert str(expected) in str(response["result"])

    def test_eval_string_operations(self):
        """Test string operations."""
        response = self.client.evaluate("'Hello' , ' World'")
        assert response["success"] is True
        assert "Hello World" in str(response["result"])

    def test_eval_large_string_operations(self):
        """Test evaluation with large strings."""
        # Create a moderately large string
        large_string = "a" * 1000
        code = f"'{large_string}' size"

        response = self.client.evaluate(code)
        assert response["success"] is True
        assert "1000" in str(response["result"])

    def test_list_packages(self):
        """Test listing packages."""
        response = self.client.list_packages()
        assert response["success"] is True
        assert "result" in response
        assert isinstance(response["result"], list)
        assert len(response["result"]) > 0
        # Check that the SIS-related packages are present
        packages = response["result"]
        assert "Sis-Core" in packages
        assert "Sis-Tests" in packages
        assert "Sis-Tests-Dummy" in packages

    def test_search_classes_like(self):
        """Test searching for classes like 'SisFixture'."""
        response = self.client.search_classes_like("SisFixture")
        assert response["success"] is True
        assert "result" in response
        assert isinstance(response["result"], list)
        # Should find SisFixtureClassForTest
        assert "SisFixtureClassForTest" in response["result"]

    def test_search_traits_like(self):
        """Test searching for traits like 'SisFixtureTrait'."""
        response = self.client.search_traits_like("SisFixtureTrait")
        assert response["success"] is True
        assert "result" in response
        assert isinstance(response["result"], list)
        # Should find SisFixtureTraitForTest
        assert "SisFixtureTraitForTest" in response["result"]

    def test_get_class_source(self):
        """Test getting SisFixtureClassForTest class source."""
        response = self.client.get_class_source("SisFixtureClassForTest")
        assert response["success"] is True
        assert "result" in response
        source = response["result"]
        # Check that source contains expected elements
        assert "SisFixtureClassForTest" in source
        assert "testMethodAaa" in source
        assert "instVarA" in source
        assert "instVarB" in source

    def test_get_class_comment(self):
        """Test getting SisFixtureClassForTest class comment."""
        response = self.client.get_class_comment("SisFixtureClassForTest")
        assert response["success"] is True
        assert "result" in response
        comment = response["result"]
        # Check the specific comment content
        assert comment == "SisFixtureClassForTest is a fixture class for SIS testing"

    def test_get_method_source(self):
        """Test getting SisFixtureClassForTest>>testMethodBbb method source."""
        response = self.client.get_method_source(
            "SisFixtureClassForTest", "testMethodBbb"
        )
        assert response["success"] is True
        assert "result" in response
        source = response["result"]
        # Check that method source contains expected elements
        assert "testMethodBbb" in source
        assert "TestSymbolBBB" in source

    def test_list_classes(self):
        """Test listing classes in Sis-Tests package."""
        response = self.client.list_classes("Sis-Tests")
        assert response["success"] is True
        assert "result" in response
        assert isinstance(response["result"], list)
        classes = response["result"]
        # Should include test classes
        assert "SisTest" in classes
        assert "SisFixtureClassForTest" in classes

    def test_list_methods(self):
        """Test listing methods in Sis-Tests package."""
        response = self.client.list_methods("Sis-Tests")
        assert response["success"] is True
        assert "result" in response
        assert isinstance(response["result"], list)
        methods = response["result"]
        # Should include specific test methods
        assert "SisTest>>#testEval" in methods
        assert "SisFixtureClassForTest>>#testMethodBbb" in methods

    def test_search_methods_like(self):
        """Test searching for methods like 'testMethodAa'."""
        response = self.client.search_methods_like("testMethodAa")
        assert response["success"] is True
        assert "result" in response
        assert isinstance(response["result"], list)
        methods = response["result"]
        # Should find both testMethodAaa and testMethodAab
        assert "testMethodAaa" in methods
        assert "testMethodAab" in methods

    def test_search_implementors(self):
        """Test searching for implementors of 'testMethodAaa'."""
        response = self.client.search_implementors("testMethodAaa")
        assert response["success"] is True
        assert "result" in response
        assert isinstance(response["result"], list)
        implementors = response["result"]
        # Should find exactly one implementor
        assert len(implementors) == 1
        assert implementors[0]["class"] == "SisFixtureClassForTest"
        assert implementors[0]["method"] == "testMethodAaa"

    def test_search_references(self):
        """Test searching for references to 'TestSymbolBBB'."""
        response = self.client.search_references("TestSymbolBBB")
        assert response["success"] is True
        assert "result" in response
        assert isinstance(response["result"], list)
        references = response["result"]
        # Should find reference in testMethodBbb
        assert len(references) == 1
        assert references[0]["class"] == "SisFixtureClassForTest"
        assert references[0]["method"] == "testMethodBbb"

    def test_search_references_to(self):
        """Test searching for references to SisTest class."""
        response = self.client.search_references_to_class("SisTest")
        assert response["success"] is True
        assert "result" in response
        assert isinstance(response["result"], list)
        references = response["result"]
        # Should find reference in SisFixtureClassForTest>>#testMethodAaa
        assert len(references) == 1
        assert references[0]["package"] == "Sis-Tests"
        assert references[0]["class"] == "SisFixtureClassForTest"
        assert references[0]["method"] == "testMethodAaa"

    def test_run_class(self):
        """Test running SisDummyTest class tests."""
        response = self.client.run_class_test("SisDummyTest")
        assert response["success"] is True
        assert "result" in response
        result = response["result"]
        # Should run 2 tests, both passing
        assert "2 ran, 2 passed, " in result

    def test_run_package(self):
        """Test running Sis-Tests-Dummy package tests."""
        response = self.client.run_package_test("Sis-Tests-Dummy")
        assert response["success"] is True
        assert "result" in response
        result = response["result"]
        # Should run 3 tests total (2 from SisDummyTest + 1 from SisDummyTest2)
        assert "3 ran, 3 passed, " in result

    def test_eval_specific_operation(self):
        """Test evaluation of specific operation from SIS tests."""
        response = self.client.evaluate("5 rem: 3")
        assert response["success"] is True
        assert "result" in response
        # Should return 2 (remainder of 5 divided by 3)
        assert response["result"] == 2

    def test_export_package(self):
        """Test export and import of Sis-Tests-Dummy package."""
        # Use a temporary directory for export
        with tempfile.TemporaryDirectory() as tmpdir:
            export_response = self.client.export_package("Sis-Tests-Dummy", tmpdir)
            assert export_response["success"] is True
            assert "result" in export_response
            result = export_response["result"]
            assert result.startswith("Sis-Tests-Dummy exported to: ")
            # Check the *.st file really exists (search recursively)
            st_files = glob.glob(f"{tmpdir}/**/*.st", recursive=True)
            assert (
                len(st_files) > 0
            ), f"No .st file found in {tmpdir} or its subdirectories after export"
        # Temporary directory is deleted automatically after the with block

    def test_list_extended_classes(self):
        """Test listing extended classes in System-Object Events package."""
        response = self.client.list_extended_classes("System-Object Events")
        assert response["success"] is True
        assert "result" in response
        assert isinstance(response["result"], list)
        extended_classes = response["result"]
        # Should include Object as extended class
        assert "Object" in extended_classes

    def test_comprehensive_package_analysis(self):
        """Test comprehensive analysis of SIS packages."""
        # Test that we can analyze the complete structure
        packages = ["Sis-Core", "Sis-Tests", "Sis-Tests-Dummy"]

        for package in packages:
            # Each package should exist
            pkg_response = self.client.list_packages()
            assert pkg_response["success"] is True
            assert package in pkg_response["result"]

            # Each package should have classes
            classes_response = self.client.list_classes(package)
            assert classes_response["success"] is True
            assert len(classes_response["result"]) > 0

            # Each package should have methods
            methods_response = self.client.list_methods(package)
            assert methods_response["success"] is True
            assert len(methods_response["result"]) > 0

    def test_error_handling_with_nonexistent_sis_elements(self):
        """Test error handling with non-existent SIS elements."""
        # Test with non-existent class
        response = self.client.get_class_source("NonExistentSisClass")
        assert response["success"] is False
        assert "error" in response

        # Test with non-existent method
        response = self.client.get_method_source(
            "SisFixtureClassForTest", "nonExistentMethod"
        )
        assert response["success"] is False
        assert "error" in response

        # Test with non-existent package
        response = self.client.list_classes("NonExistentSisPackage")
        assert response["success"] is False
        assert "error" in response

    def test_search_precision_with_sis_elements(self):
        """Test search precision using SIS elements."""
        # Test precise class search
        response = self.client.search_classes_like("SisFixtureClassForTest")
        assert response["success"] is True
        assert "SisFixtureClassForTest" in response["result"]

        # Test partial class search
        response = self.client.search_classes_like("SisFixture")
        assert response["success"] is True
        assert "SisFixtureClassForTest" in response["result"]

        # Test precise method search
        response = self.client.search_methods_like("testMethodAaa")
        assert response["success"] is True
        assert "testMethodAaa" in response["result"]

        # Test partial method search
        response = self.client.search_methods_like("testMethod")
        assert response["success"] is True
        assert "testMethodAaa" in response["result"]
        assert "testMethodAab" in response["result"]
        assert "testMethodBbb" in response["result"]

    def test_cross_package_references(self):
        """Test cross-package references using SIS elements."""
        # SisFixtureClassForTest>>#testMethodAaa references SisTest class
        # This tests that references work across the same package
        response = self.client.search_references_to_class("SisTest")
        assert response["success"] is True
        references = response["result"]

        # Find the reference from SisFixtureClassForTest
        sis_reference = None
        for ref in references:
            if (
                ref["class"] == "SisFixtureClassForTest"
                and ref["method"] == "testMethodAaa"
            ):
                sis_reference = ref
                break

        assert sis_reference is not None
        assert sis_reference["package"] == "Sis-Tests"

    def test_trait_functionality(self):
        """Test trait-related functionality using SIS elements."""
        # Test that SisFixtureTraitForTest is found
        response = self.client.search_traits_like("SisFixtureTraitForTest")
        assert response["success"] is True
        assert "SisFixtureTraitForTest" in response["result"]

        # Test partial trait search
        response = self.client.search_traits_like("SisFixture")
        assert response["success"] is True
        assert "SisFixtureTraitForTest" in response["result"]

    def test_method_search_with_exact_matches(self):
        """Test method search with exact matches from SIS codebase."""
        # Test finding methods with exact patterns
        test_methods = ["testMethodAaa", "testMethodAab", "testMethodBbb"]

        for method in test_methods:
            response = self.client.search_methods_like(method)
            assert response["success"] is True
            assert method in response["result"]

    def test_symbol_reference_tracking(self):
        """Test tracking of symbol references using SIS test data."""
        # TestSymbolBBB is referenced in SisFixtureClassForTest>>#testMethodBbb
        response = self.client.search_references("TestSymbolBBB")
        assert response["success"] is True
        references = response["result"]

        # Should find exactly one reference
        assert len(references) == 1
        ref = references[0]
        assert ref["class"] == "SisFixtureClassForTest"
        assert ref["method"] == "testMethodBbb"

    def test_test_execution_reliability(self):
        """Test that SIS dummy tests execute reliably."""
        # Test individual test classes
        test_classes = ["SisDummyTest", "SisDummyTest2"]

        for test_class in test_classes:
            response = self.client.run_class_test(test_class)
            assert response["success"] is True
            result = response["result"]
            # Tests should pass
            assert "passed" in result
            assert "failed" not in result or "0 failed" in result

    def test_package_completeness(self):
        """Test that SIS packages are complete and accessible."""
        # Test that we can access all expected SIS elements

        # Check Sis-Core package
        response = self.client.list_classes("Sis-Core")
        assert response["success"] is True

        # Check Sis-Tests package has expected classes
        response = self.client.list_classes("Sis-Tests")
        assert response["success"] is True
        classes = response["result"]
        expected_classes = ["SisTest", "SisFixtureClassForTest"]
        for cls in expected_classes:
            assert cls in classes

        # Check Sis-Tests-Dummy package has expected classes
        response = self.client.list_classes("Sis-Tests-Dummy")
        assert response["success"] is True
        classes = response["result"]
        expected_classes = ["SisDummyTest", "SisDummyTest2"]
        for cls in expected_classes:
            assert cls in classes
