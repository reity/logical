from setuptools import setup

with open("README.rst", "r") as fh:
    long_description = fh.read()

setup(
    name="logical",
    version="0.1.1",
    packages=["logical",],
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
