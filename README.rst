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
