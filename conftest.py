"""Pytest configuration for custom test output."""

import pytest

# Store failed tests with their docstrings
failed_tests = []


def pytest_itemcollected(item):
    """Use docstring as the test name."""
    if item.obj.__doc__:
        # Store original nodeid for JSON report
        if not hasattr(item, "_original_nodeid"):
            item._original_nodeid = item.nodeid
        # Get the first line of the docstring
        docstring = item.obj.__doc__.strip().split("\n")[0]
        item._nodeid = docstring


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Store failed tests with their docstrings."""
    outcome = yield
    report = outcome.get_result()

    # Store failed tests with full docstring
    if report.when == "call" and report.failed and item.obj.__doc__:
        # Get class name if test is part of a class
        class_name = None
        if hasattr(item, "cls") and item.cls is not None:
            class_name = item.cls.__name__

        # Get file path and line number
        file_path = item.location[0]
        line_number = item.location[1] + 1  # pytest uses 0-based indexing

        failed_tests.append(
            {
                "nodeid": item.nodeid,
                "docstring": item.obj.__doc__.strip(),
                "report": report,
                "file_path": file_path,
                "line_number": line_number,
                "class_name": class_name,
                "function_name": item.name,
            }
        )


def pytest_terminal_summary(terminalreporter):
    """Display detailed docstrings for failed tests."""
    if failed_tests:
        terminalreporter.write_sep("=", "FAILED TEST DESCRIPTIONS", bold=True, red=True)
        for test in failed_tests:
            terminalreporter.write_line("")

            # Build test location info
            location_parts = [f"File: {test['file_path']}:{test['line_number']}"]
            if test["class_name"]:
                location_parts.append(f"Class: {test['class_name']}")
            location_parts.append(f"Function: {test['function_name']}")
            location_info = " | ".join(location_parts)

            terminalreporter.write_sep(
                "-", f"Test: {test['nodeid']}", bold=True, yellow=True
            )
            terminalreporter.write_line(location_info, cyan=True)
            terminalreporter.write_line("")
            terminalreporter.write_line(test["docstring"])
            terminalreporter.write_line("")
