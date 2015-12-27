import subprocess
import os
import sys
import contextlib

import tempman
import distlib.locators

from .setuptools_build import SETUPTOOLS_SHIM
from .files import download_tarball


def download_requirement_source(requirement):
    distribution = distlib.locators.locate(requirement)
    return _download_distribution_source(distribution)


@contextlib.contextmanager
def _download_distribution_source(distribution):
    with tempman.create_temp_dir() as temp_directory:
        download_tarball(distribution.source_url, temp_directory.path)
        path = os.path.join(temp_directory.path, "{0}-{1}".format(distribution.name, distribution.version))
        yield SourceDistribution(path=path, package_name=distribution.name)


class SourceDistribution(object):
    def __init__(self, path, package_name):
        self.path = path
        self._egg_info = _egg_info(source_directory=path, package_name=package_name)
    
    def top_level(self):
        return self._egg_info.top_level()


def _egg_info(source_directory, package_name):
    script = SETUPTOOLS_SHIM % os.path.join(source_directory, "setup.py")
    subprocess.check_call(
        [sys.executable, "-c", script, "egg_info"],
        cwd=source_directory)
    
    return EggInfo(os.path.join(source_directory, package_name + ".egg-info"))


class EggInfo(object):
    def __init__(self, path):
        self._path = path
    
    def top_level(self):
        with open(os.path.join(self._path, "top_level.txt")) as top_level_fileobj:
            return filter(None, map(str.strip, top_level_fileobj))
