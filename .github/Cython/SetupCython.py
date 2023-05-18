# Setup for Cython conversion
from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [Extension("Navigator", ["Navigator.py"],)]

setup(
    name='Navigator',
    version='0.4.8',
    author='Mike Pistolesi',
    ext_modules=cythonize(extensions, language_level=3),
    install_requires=['pygame', 'cryptography', 'python-dotenv', 'pypresence'])
