"""This file sets up pytest to be run as a Github Action"""
from setuptools import setup, find_packages

def read_req(path):
    """Returns dependencies from requirements.txt"""
    with open(path, 'r') as file_handle:
        array = []
        for line in file_handle:
            array.append(line)
        return array

setup(
    name='filing13F_searcher',
    version='0.0.1',
    packages=find_packages('filingparser'),
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
    install_requires=read_req("requirements.txt")
)
