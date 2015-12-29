python-vendorize
================

``python-vendorize`` allows pure-Python dependencies to be vendorized:
that is, the Python source of the dependency is copied into your own package.
Best used for small, pure-Python dependencies to avoid version conflicts
when other packages require a different version of the same dependency.

Dependencies you want vendorizing should be specified in ``vendorize.ini``.
In the ``vendorize`` section, the ``target`` option describes where vendorized dependencies should be placed.
Each dependency should have its own section named ``require:${REQUIREMENT}``.
``$REQUIREMENT`` can be anything that ``pip`` would understand,
such as a package name, a package name with version constraints or an URL.
Dependencies can then be vendorized using ``python-vendorize``.

For instance, suppose I want to vendorize ``six`` so it can be used from the package ``hello``.
The directory structure would be something like:

::

    - hello
      - __init__.py
    - setup.py
    - vendorize.ini

``vendorize.ini`` might look something like:

::

    [vendorize]
    target=hello/_vendor
    [require:six]

I can then run ``python-vendorize`` in the same directory as ``vendorize.ini``.
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
    - vendorize.ini

In ``hello/__init__.py``, ``six`` can be imported from ``_vendor``:

.. code:: python

    from ._vendor import six

Installation
~~~~~~~~~~~~

::

    pip install vendorize
