import io
import os
import subprocess

from . import python_source
from ._vendor import pytoml as toml
from .files import mkdir_p, ensure_file_exists
from .import_rewrite import rewrite_imports_in_module


def vendorize_requirements(path):
    with open(path) as fileobj:
        config = toml.load(fileobj)
    target_directory = os.path.join(os.path.dirname(path), config["target"])
    ensure_file_exists(os.path.join(target_directory, "__init__.py"))
    for requirement in config["packages"]:
        vendorize_requirement(
            cwd=os.path.dirname(path) or None,
            requirement=requirement,
            target_directory=target_directory,
        )


def vendorize_requirement(cwd, requirement, target_directory):
    mkdir_p(target_directory)
    subprocess.check_call(
        ["pip", "install", "--no-dependencies", "--target", target_directory, requirement],
        cwd=cwd)
    top_level_names = _read_top_level_names(target_directory)
    _rewrite_imports(target_directory, top_level_names)

def _read_top_level_names(target_directory):
    for name in os.listdir(target_directory):
        if name.endswith(".egg-info") or name.endswith(".dist-info"):
            path = os.path.join(target_directory, name, "top_level.txt")
            if os.path.exists(path):
                with open(path) as top_level_file:
                    return list(filter(None, map(lambda line: line.strip(), top_level_file)))
    
    raise Exception("Could not find top_level.txt")
            
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
