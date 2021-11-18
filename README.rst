=======
logical
=======

Callable subclass of tuple for representing logical operators/connectives based on their truth tables.

|pypi| |travis| |coveralls|

.. |pypi| image:: https://badge.fury.io/py/logical.svg
   :target: https://badge.fury.io/py/logical
   :alt: PyPI version and link.

.. |travis| image:: https://travis-ci.com/reity/logical.svg?branch=master
    :target: https://travis-ci.com/reity/logical

.. |coveralls| image:: https://coveralls.io/repos/github/reity/logical/badge.svg?branch=master
   :target: https://coveralls.io/github/reity/logical?branch=master

Package Installation and Usage
------------------------------
The package is available on PyPI::

    python -m pip install logical

The library can be imported in the usual ways::

    import logical
    from logical import *

Each instance of the ``logical`` class (derived from the ``tuple`` class) represents a boolean function that accepts ``n`` inputs by specifying its output values across all possible inputs. In other words, an instance represents the *output column* of a truth table for a function (under the assumption that the input vectors to which each output value corresponds are sorted in ascending order). Thus, each instance representing a function that accepts ``n`` inputs must have length ``2**n``.

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

It is then possible to apply the instance ``f`` defined above to any three-component input vector::

    >>> f(0, 1, 1)
    0
    >>> f(1, 1, 0)
    1

Pre-defined instances are provided for all unary and binary boolean functions. These are available both as constants and as attributes of the ``logical`` class::

    >>> logical.xor_(1, 0)
    1
    >>> and_(1, 0)
    0

The constants ``unary`` and ``binary`` are also defined. Each is a set containing exactly those instances of ``logical`` that represent functions having that arity.

    >>> unary
    {(0, 0), (1, 0), (1, 1), (0, 1)}
    >>> len(binary)
    16

Documentation
-------------
.. include:: toc.rst

The documentation can be generated automatically from the source files using `Sphinx <https://www.sphinx-doc.org/>`_::

    cd docs
    python -m pip install -r requirements.txt
    sphinx-apidoc -f -E --templatedir=_templates -o _source .. ../setup.py && make html

Testing and Conventions
-----------------------
All unit tests are executed and their coverage is measured when using `nose <https://nose.readthedocs.io/>`_ (see ``setup.cfg`` for configution details)::

    nosetests

Alternatively, all unit tests are included in the module itself and can be executed using `doctest <https://docs.python.org/3/library/doctest.html>`_::

    python logical/logical.py -v

Style conventions are enforced using `Pylint <https://www.pylint.org/>`_::

    pylint logical

Contributions
-------------
In order to contribute to the source code, open an issue or submit a pull request on the GitHub page for this library.

Versioning
----------
The version number format for this library and the changes to the library associated with version number increments conform with `Semantic Versioning 2.0.0 <https://semver.org/#semantic-versioning-200>`_.
