"""This is the setup module."""
from setuptools import setup, find_packages

with open('requirements.txt') as f:
    INSTALL_REQUIRES = f.read().splitlines()

setup(
    name="edgar_filing_searcher",
    version="1.1.0",
    description="Web backend for filing website",
    url="https://github.com/secfilingsearcher/filing13F_searcher",
    packages=find_packages(),
    python_requires=">=3.6",
    scripts=["scripts/parser_main"],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
    install_requires=INSTALL_REQUIRES
)
