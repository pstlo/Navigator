# Setup for Cython conversion on local machine ( replace the parent directory's "SetupCython.py" file )
from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [Extension("Navigator", ["../../Navigator/Navigator.py"]), 
        Extension("Settings",["../../Navigator/Settings.py"]),
        Extension("Game",["../../Navigator/Game.py"]),
        Extension("Assets",["../../Navigator/Assets.py"]),
        Extension("Event",["../../Navigator/Event.py"]),
        Extension("Explosion",["../../Navigator/Explosion.py"]),
        Extension("Gamepad",["../../Navigator/Gamepad.py"]),
        Extension("Lasers",["../../Navigator/Lasers.py"]),
        Extension("Menu",["../../Navigator/Menu.py"]),
        Extension("Obstacles",["../../Navigator/Obstacles.py"]),
        Extension("Player",["../../Navigator/Player.py"]),
        Extension("Point",["../../Navigator/Point.py"]),
        Extension("Presence",["../../Navigator/Presence.py"]),
        Extension("Unlocks",["../../Navigator/Unlocks.py"])
    ]
    

setup(
    name='Navigator',
    version='0.5.1',
    author='Mike Pistolesi',
    ext_modules=cythonize(extensions, language_level=3),
    install_requires=['pygame','cryptography','python-dotenv','pypresence','dnspython','certifi','pymongo==3.11'])
