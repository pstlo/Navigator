# Setup for Cython conversion from github action
from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [Extension("Navigator", ["Navigator.py"],)]

setup(
    name='Navigator',
    version='0.4.9',
    author='Mike Pistolesi',
    ext_modules=cythonize(extensions, language_level=3),
    install_requires=['pygame','cryptography','python-dotenv','pypresence','dnspython','certifi','pymongo==3.11'])
