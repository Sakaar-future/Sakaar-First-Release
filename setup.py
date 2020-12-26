from setuptools import Extension, Command, setup
import Sakaar
setup(
    name="Sakaar",
    version=Sakaar.Version,
    description="Coming to future",
    author="No one of us",
    platforms='Posix; MacOS X; Windows',
    zip_safe=False,
    python_requires='>=3.8',
    license="BSD, Public Domain, Apache",
    packages=['Sakaar'],
    install_requires = ['pyCryptoCorex>=1.0.5']
)
