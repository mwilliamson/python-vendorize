import os
from ConfigParser import RawConfigParser

from .files import mkdir_p, copy, copy_recursive, ensure_file_exists
from . import pypi


def vendorize_requirements(path):
    require_prefix = "require:"
    parser = RawConfigParser()
    parser.read(path)
    target_directory = os.path.join(os.path.dirname(path), parser.get("vendorize", "destination"))
    ensure_file_exists(os.path.join(target_directory, "__init__.py"))
    for section in parser.sections():
        if section.startswith(require_prefix):
            requirement = section[len(require_prefix):]
            vendorize_requirement(
                requirement=requirement,
                target_directory=target_directory)


def vendorize_requirement(requirement, target_directory):
    with pypi.download_requirement_source(requirement) as source:
        mkdir_p(target_directory)
        
        for top_level_name in source.top_level():
            module_path = os.path.join(source.path, top_level_name + ".py")
            if os.path.exists(module_path):
                copy(module_path, target_directory)
            
            package_path = os.path.join(source.path, top_level_name)
            if os.path.exists(package_path):
                target_package_directory = os.path.join(target_directory, top_level_name)
                copy_recursive(package_path, target_package_directory)
