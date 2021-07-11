
#!/usr/bin/env python

import os
import sys
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='vendorize',
    version='0.2.2',
    description='Vendorize packages from PyPI',
    long_description=read("README.rst"),
    author='Michael Williamson',
    author_email='mike@zwobble.org',
    url='http://github.com/mwilliamson/python-vendorize',
    packages=find_packages(exclude=["tests", "tests.*", "examples", "examples.*"]),
    entry_points={
        "console_scripts": [
            "python-vendorize=vendorize.cli:main"
        ]
    },
    keywords="vendor vendorize",
    license="BSD-2-Clause",
)

