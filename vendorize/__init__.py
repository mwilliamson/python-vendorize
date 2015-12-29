import os
import subprocess
from ._vendor.six.moves.configparser import RawConfigParser

from .files import mkdir_p, ensure_file_exists


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
    mkdir_p(target_directory)
    subprocess.check_call(["pip", "install", "--no-dependencies", "--target", target_directory, requirement])
