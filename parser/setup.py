""""""
from setuptools import setup, find_packages

def read_req(path):
    """"""
    with open(path, 'r') as fh:
        array = []
        for line in fh:
            array.append(line)
        return array

setup(
    name='filing13F_searcher',
    version='0.0.1',
    packages=find_packages(),
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
    install_requires=read_req("requirements.txt")
)
