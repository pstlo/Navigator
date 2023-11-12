# Setup for Cython conversion on local machine ( replace the parent directory's "SetupCython.py" file )
from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [Extension("Navigator", ["../../Navigator/Navigator.py"],)]

setup(
    name='Navigator',
    version='0.5.0',
    author='Mike Pistolesi',
    ext_modules=cythonize(extensions, language_level=3),
    install_requires=['pygame','cryptography','python-dotenv','pypresence','dnspython','certifi','pymongo==3.11'])
