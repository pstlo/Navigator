# Setup for Cython conversion on local machine ( replace the parent directory's "SetupCython.py" file )
from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [Extension("Navigator", ["../../Navigator.py"],)]

setup(
    name='Navigator',
    version='0.4.9',
    author='Mike Pistolesi',
    ext_modules=cythonize(extensions, language_level=3),
    install_requires=['pygame','cryptography','python-dotenv','pypresence','dnspython','pymongo==3.11'])
