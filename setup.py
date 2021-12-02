from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read().replace(".. include:: toc.rst\n\n", "")

# The lines below can be parsed by `docs/conf.py`.
name = "logical"
version = "0.3.1"

setup(
    name=name,
    version=version,
    packages=[name,],
    install_requires=[],
    license="MIT",
    url="https://github.com/reity/logical",
    author="Andrei Lapets",
    author_email="a@lapets.io",
    description="Callable subclass of tuple for representing logical "+\
                "operators/connectives based on their truth tables.",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    test_suite="nose.collector",
    tests_require=["nose"],
)
