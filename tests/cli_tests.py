import sys
import os
import shutil
import contextlib
import io

from spur import LocalShell
import tempman

_local = LocalShell()

def test_vendorizing_single_module_with_no_dependencies_grabs_one_module_file():
    with _vendorize_example("isolated-module") as project_path:
        result = _local.run(["python", os.path.join(project_path, "main.py")])
        assert b"('one', 1)" == result.output.strip()

def test_can_vendorize_local_modules_from_relative_paths():
    with _vendorize_example("local-module") as project_path:
        result = _local.run(["python", os.path.join(project_path, "main.py")])
        assert b"hello\n" == result.output

def test_absolute_paths_in_same_distribution_are_rewritten_to_be_relative():
    with _vendorize_example("absolute-import-rewrite") as project_path:
        result = _local.run(["python", os.path.join(project_path, "main.py")])
        assert b"hello\n" == result.output

def test_can_rewrite_indented_absolute_simple_imports():
    with _vendorize_example("indented-absolute-simple-import-rewrite") as project_path:
        result = _local.run(["python", os.path.join(project_path, "main.py")])
        assert b"hello\n" == result.output

def test_can_vendorize_multiple_dependencies():
    with _vendorize_example("multiple-dependencies") as project_path:
        result = _local.run(["python", os.path.join(project_path, "main.py")])
        assert b"hello\nworld\n" == result.output

def test_can_vendorize_multiple_dependencies_that_require_import_rewriting():
    with _vendorize_example("multiple-dependencies-with-rewrite") as project_path:
        result = _local.run(["python", os.path.join(project_path, "main.py")])
        assert b"hello\nworld\n" == result.output

def test_can_vendorize_with_pyproject_toml():
    with _vendorize_example("isolated-module-pyproject") as project_path:
        result = _local.run(["python", os.path.join(project_path, "main.py")])
        assert b"('one', 1)" == result.output.strip()

@contextlib.contextmanager
def _vendorize_example(example_name):
    path = os.path.join(os.path.dirname(__file__), "../examples", example_name)
    _clean_project(path)

    _local.run(
        ["python-vendorize"],
        cwd=path,
        encoding="utf-8",
    )
    yield path


def _clean_project(path):
    vendor_path = os.path.join(path, "_vendor")
    if os.path.exists(vendor_path):
        shutil.rmtree(vendor_path)
