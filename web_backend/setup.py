import setuptools

with open('requirements.txt') as f:
    INSTALL_REQUIRES = f.read().splitlines()

setuptools.setup(
    name="filingapi",
    version="0.0.1",
    author="Ed H",
    description="Web backend for filing website",
    url="https://github.com/eharley19/filing13F_searcher",
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    install_requires=INSTALL_REQUIRES
)

