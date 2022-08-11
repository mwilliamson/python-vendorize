python-vendorize
================

``python-vendorize`` allows pure-Python dependencies to be vendorized:
that is, the Python source of the dependency is copied into your own package.
Best used for small, pure-Python dependencies to avoid version conflicts
when other packages require a different version of the same dependency.

Dependencies you want vendorizing should be specified in ``vendorize.toml``.
``target`` should be a string containing the path where vendorized dependencies should be placed,
relative to the directory that ``vendorize.toml`` is in.
``packages`` should be a list of strings containing the dependencies.
Each of these strings can be anything that ``pip`` would understand,
such as a package name, a package name with version constraints or an URL.
Dependencies can then be vendorized using ``python-vendorize``.

For instance, suppose I want to vendorize ``six`` so it can be used from the package ``hello``.
The directory structure would be something like:

::

    - hello
      - __init__.py
    - setup.py
    - vendorize.toml

``vendorize.toml`` might look something like:

::

    target = "hello/_vendor"
    packages = [
        "six",
    ]

I can then run ``python-vendorize`` in the same directory as ``vendorize.toml``.
The directory structure would then be something like:

::

    - hello
      - _vendor
        - six.dist-info
          - ...
        - __init__.py
        - six.py
      - __init__.py
    - setup.py
    - vendorize.toml

In ``hello/__init__.py``, ``six`` can be imported from ``_vendor``:

.. code:: python

    from ._vendor import six

Packages that are built not with Setuptools (but for example with Poetry) might not have a `top_level.txt` file
in their distribution info. However, vendorize requires this information to rewrite absolute imports. If you encounter
that an absolute import is not rewritten as it should have, set the `top_level_names` option in `vendorize.toml`. These
will be taken into account in addition to any records from `top_level.txt` files.

Installation
~~~~~~~~~~~~

::

    pip install vendorize
