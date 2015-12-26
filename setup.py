
#!/usr/bin/env python

import os
import sys
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name='vendorize',
    version='0.1.0',
    description='Vendorize packages from PyPI',
    long_description=read("README.rst"),
    author='Michael Williamson',
    author_email='mike@zwobble.org',
    url='http://github.com/mwilliamson/python-vendorize',
    packages=['vendorize'],
    install_requires=["tempman>=0.1.3,<0.2"],
    keywords="vendor vendorize",
)

