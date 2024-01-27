from setuptools import setup, find_packages

setup(
    name="Rcb4BaseLib",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "pyserial==3.5"
    ]
)
