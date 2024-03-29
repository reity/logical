=======
logical
=======

Callable subclass of the tuple type for representing logical operators/connectives based on their truth tables.

|pypi| |readthedocs| |actions| |coveralls|

.. |pypi| image:: https://badge.fury.io/py/logical.svg
   :target: https://badge.fury.io/py/logical
   :alt: PyPI version and link.

.. |readthedocs| image:: https://readthedocs.org/projects/logical/badge/?version=latest
   :target: https://logical.readthedocs.io/en/latest/?badge=latest
   :alt: Read the Docs documentation status.

.. |actions| image:: https://github.com/reity/logical/workflows/lint-test-cover-docs/badge.svg
   :target: https://github.com/reity/logical/actions/workflows/lint-test-cover-docs.yml
   :alt: GitHub Actions status.

.. |coveralls| image:: https://coveralls.io/repos/github/reity/logical/badge.svg?branch=main
   :target: https://coveralls.io/github/reity/logical?branch=main
   :alt: Coveralls test coverage summary.

Installation and Usage
----------------------
This library is available as a `package on PyPI <https://pypi.org/project/logical>`__::

    python -m pip install logical

The library can be imported in the usual ways::

    import logical
    from logical import *

Examples
^^^^^^^^

.. |logical| replace:: ``logical``
.. _logical: https://logical.readthedocs.io/en/2.0.0/_source/logical.html#logical.logical.logical

.. |tuple| replace:: ``tuple``
.. _tuple: https://docs.python.org/3/library/functions.html#func-tuple

Each instance of the |logical|_ class (derived from the built-in |tuple|_ class) represents a boolean function that accepts ``n`` inputs by specifying its output values across all possible inputs. In other words, an instance represents the *output column* of a `truth table <https://en.wikipedia.org/wiki/Truth_table>`__ for a function (under the assumption that the input vectors to which each output value corresponds are sorted in ascending order). Thus, each instance representing a function that accepts ``n`` inputs must have length ``2**n``.

For example, consider the truth table below for a boolean function *f* that accepts three inputs:

+-----+-----+-----+---------------------+
| *x* | *y* | *z* | *f* (*x*, *y*, *z*) |
+-----+-----+-----+---------------------+
|  0  |  0  |  0  | 1                   |
+-----+-----+-----+---------------------+
|  0  |  0  |  1  | 0                   |
+-----+-----+-----+---------------------+
|  0  |  1  |  0  | 1                   |
+-----+-----+-----+---------------------+
|  0  |  1  |  1  | 0                   |
+-----+-----+-----+---------------------+
|  1  |  0  |  0  | 0                   |
+-----+-----+-----+---------------------+
|  1  |  0  |  1  | 1                   |
+-----+-----+-----+---------------------+
|  1  |  1  |  0  | 1                   |
+-----+-----+-----+---------------------+
|  1  |  1  |  1  | 0                   |
+-----+-----+-----+---------------------+

Notice that the input vectors (*i.e.*, the left-most three column values in each row) are sorted in ascending order from top to bottom. If we always assume this order for input vectors, the entire function *f* can be represented using the right-most column. For the example function *f* defined by the table above, this can be done in the manner illustrated below::

    >>> from logical import *
    >>> f = logical((1, 0, 1, 0, 0, 1, 1, 0)) 

It is then possible to `apply <https://logical.readthedocs.io/en/2.0.0/_source/logical.html#logical.logical.logical.__call__>`__ the instance ``f`` defined above to any three-component input vector::

    >>> f(0, 1, 1)
    0
    >>> f(1, 1, 0)
    1

.. |call| replace:: ``__call__``
.. _call: https://logical.readthedocs.io/en/2.0.0/_source/logical.html#logical.logical.logical.__call__

It is also possible to create a new |logical|_ instance that has a ``function`` attribute corresponding to a `compiled Python function <https://logical.readthedocs.io/en/2.0.0/_source/logical.html#logical.logical.logical.compiled>`__ that has the same behavior as the |call|_ method (at least, on valid inputs). This Python function does not check that inputs are of the correct type and format, but has an execution time that is usually at most half of the execution time of the |call|_ method::

    >>> f = logical((1, 0, 0, 1, 0, 1, 0, 1))
    >>> g = f.compiled()
    >>> g.function(0, 0, 0)
    1
    >>> g.function(1, 1, 0)
    0

Pre-defined instances are provided for all nullary, unary, and binary boolean functions. These are available both as constants and as attributes of the |logical|_ class::

    >>> logical.xor_(1, 0)
    1
    >>> and_(1, 0)
    0

.. |nullary| replace:: ``nullary``
.. _nullary: https://logical.readthedocs.io/en/2.0.0/_source/logical.html#logical.logical.logical.nullary

.. |unary| replace:: ``unary``
.. _unary: https://logical.readthedocs.io/en/2.0.0/_source/logical.html#logical.logical.logical.unary

.. |binary| replace:: ``binary``
.. _binary: https://logical.readthedocs.io/en/2.0.0/_source/logical.html#logical.logical.logical.binary

The constants |nullary|_, |unary|_, and |binary|_ are also defined. Each is a set containing exactly those instances of |logical|_ that represent functions having that arity::

    >>> unary
    {(0, 0), (1, 0), (1, 1), (0, 1)}
    >>> len(binary)
    16

.. |every| replace:: ``every``
.. _every: https://logical.readthedocs.io/en/2.0.0/_source/logical.html#logical.logical.logical.every

For convenience, the constant |every|_ is defined as the union of |nullary|_, |unary|_, and |binary|_.

Development
-----------
All installation and development dependencies are fully specified in ``pyproject.toml``. The ``project.optional-dependencies`` object is used to `specify optional requirements <https://peps.python.org/pep-0621>`__ for various development tasks. This makes it possible to specify additional options (such as ``docs``, ``lint``, and so on) when performing installation using `pip <https://pypi.org/project/pip>`__::

    python -m pip install .[docs,lint]

Documentation
^^^^^^^^^^^^^
The documentation can be generated automatically from the source files using `Sphinx <https://www.sphinx-doc.org>`__::

    python -m pip install .[docs]
    cd docs
    sphinx-apidoc -f -E --templatedir=_templates -o _source .. && make html

Testing and Conventions
^^^^^^^^^^^^^^^^^^^^^^^
All unit tests are executed and their coverage is measured when using `pytest <https://docs.pytest.org>`__ (see the ``pyproject.toml`` file for configuration details)::

    python -m pip install .[test]
    python -m pytest

Alternatively, all unit tests are included in the module itself and can be executed using `doctest <https://docs.python.org/3/library/doctest.html>`__::

    python src/logical/logical.py -v

Style conventions are enforced using `Pylint <https://pylint.pycqa.org>`__::

    python -m pip install .[lint]
    python -m pylint src/logical

Contributions
^^^^^^^^^^^^^
In order to contribute to the source code, open an issue or submit a pull request on the `GitHub page <https://github.com/reity/logical>`__ for this library.

Versioning
^^^^^^^^^^
The version number format for this library and the changes to the library associated with version number increments conform with `Semantic Versioning 2.0.0 <https://semver.org/#semantic-versioning-200>`__.

Publishing
^^^^^^^^^^
This library can be published as a `package on PyPI <https://pypi.org/project/logical>`__ by a package maintainer. First, install the dependencies required for packaging and publishing::

    python -m pip install .[publish]

Ensure that the correct version number appears in ``pyproject.toml``, and that any links in this README document to the Read the Docs documentation of this package (or its dependencies) have appropriate version numbers. Also ensure that the Read the Docs project for this library has an `automation rule <https://docs.readthedocs.io/en/stable/automation-rules.html>`__ that activates and sets as the default all tagged versions. Create and push a tag for this version (replacing ``?.?.?`` with the version number)::

    git tag ?.?.?
    git push origin ?.?.?

Remove any old build/distribution files. Then, package the source into a distribution archive::

    rm -rf build dist src/*.egg-info
    python -m build --sdist --wheel .

Finally, upload the package distribution archive to `PyPI <https://pypi.org>`__::

    python -m twine upload dist/*
