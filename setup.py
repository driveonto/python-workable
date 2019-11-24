import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "python-workable",
    version = "0.0.6",
    author = "Yiannis Inglessis",
    author_email = "negtheone@gmail.com",
    description = ("Python API library for the Workable platform."),
    license = "MIT",
    keywords = "workable api",
    url = "http://packages.python.org/python-workable",
    py_modules=['workable'],
    long_description=read('README'),
    install_requires = ['requests >= 2.11.1'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: MIT License",
    ],
)
