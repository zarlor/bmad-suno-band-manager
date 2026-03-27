"""Configure pytest to collect test files with hyphens in names."""
import pytest


def pytest_collect_file(parent, file_path):
    if file_path.suffix == ".py" and file_path.name.startswith("test-"):
        return pytest.Module.from_parent(parent, path=file_path)
