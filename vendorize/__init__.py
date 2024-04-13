import csv
import io
import os
import pathlib
import subprocess
import sys

from . import python_source
from ._vendor import pytoml as toml
from .files import mkdir_p, ensure_file_exists
from .import_rewrite import rewrite_imports_in_module


def vendorize_directory(path):
    config = _read_directory_config(path)

    return vendorize_requirements(config=config, directory_path=path)


def _read_directory_config(path):
    try:
        with open(os.path.join(path, "vendorize.toml")) as fileobj:
            return toml.load(fileobj)
    except FileNotFoundError:
        pass

    try:
        with open(os.path.join(path, "pyproject.toml")) as fileobj:
            pyproject = toml.load(fileobj)
            return pyproject["tool"]["vendorize"]
    except FileNotFoundError:
        raise RuntimeError("Could not find vendorize config")


def vendorize_requirements(config, directory_path):
    target_directory = os.path.join(directory_path, config["target"])
    ensure_file_exists(os.path.join(target_directory, "__init__.py"))
    _download_requirements(
        cwd=directory_path or None,
        requirements=config["packages"],
        target_directory=target_directory,
    )
    top_level_names = _read_top_level_names(target_directory)
    _rewrite_imports(target_directory, top_level_names)


def vendorize_requirement(cwd, requirement, target_directory):
    _download_requirements(cwd=cwd, requirements=[requirement], target_directory=target_directory)
    top_level_names = _read_top_level_names(target_directory)
    _rewrite_imports(target_directory, top_level_names)


def _download_requirements(cwd, requirements, target_directory):
    mkdir_p(target_directory)
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "--no-dependencies", "--target", target_directory] + requirements,
        cwd=cwd)

def _read_top_level_names(target_directory):
    top_level_names = set()

    for name in os.listdir(target_directory):
        if name.endswith(".dist-info"):
            path = os.path.join(target_directory, name)
            top_level_names.update(_read_top_level_names_from_dist_info(path))

        elif name.endswith(".egg-info"):
            path = os.path.join(target_directory, name)
            top_level_names.update(_read_top_level_names_from_egg_info(path))

    return top_level_names


def _read_top_level_names_from_dist_info(dist_info_path):
    path = os.path.join(dist_info_path, "RECORD")

    if not os.path.exists(path):
        return

    py_extension = ".py"

    with open(path, "rt", encoding="utf-8") as fileobj:
        for line in csv.reader(fileobj):
            if len(line) > 0:
                record_path = line[0]
                if record_path.endswith(py_extension):
                    top_part = pathlib.Path(record_path).parts[0]
                    if top_part.endswith(py_extension):
                        yield top_part[:-len(py_extension)]
                    else:
                        yield top_part


def _read_top_level_names_from_egg_info(egg_info_path):
    path = os.path.join(egg_info_path, "top_level.txt")
    if os.path.exists(path):
        with open(path) as top_level_file:
            return list(filter(None, map(lambda line: line.strip(), top_level_file)))


def _rewrite_imports(target_directory, top_level_names):
    for top_level_name in top_level_names:
        module_path = os.path.join(target_directory, top_level_name + ".py")
        if os.path.exists(module_path):
            _rewrite_imports_in_module(module_path, top_level_names, depth=0)

        package_path = os.path.join(target_directory, top_level_name)
        if os.path.exists(package_path):
            _rewrite_imports_in_package(package_path, top_level_names, depth=1)

def _rewrite_imports_in_package(package_path, top_level_names, depth):
    for name in os.listdir(package_path):
        child_path = os.path.join(package_path, name)
        if name.endswith(".py"):
            _rewrite_imports_in_module(child_path, top_level_names, depth=depth)

        if os.path.isdir(child_path):
            _rewrite_imports_in_package(child_path, top_level_names, depth=depth + 1)


def _rewrite_imports_in_module(module_path, top_level_names, depth):
    with io.open(module_path, "rb") as source_file:
        encoding = python_source.find_encoding(source_file)

    with io.open(module_path, "r", encoding=encoding, newline='') as source_file:
        source = source_file.read()

    rewritten_source = rewrite_imports_in_module(source, top_level_names, depth)

    with io.open(module_path, "w", encoding=encoding, newline='') as source_file:
        source_file.write(rewritten_source)

    pyc_path = os.path.splitext(module_path)[0] + ".pyc"
    if os.path.exists(pyc_path):
        os.unlink(pyc_path)
