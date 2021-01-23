""" setuptools-based setup module. """

from setuptools import setup, find_packages

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

setup(
    name="app",
    version="0.1",
    description="Science Vocabulary Study webapp",
    url="https://github.com/L4LabUA/scivocab",
    packages = find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
    ],
    keywords="speech analysis",
    zip_safe=False,
    install_requires=[
        "wheel",
        "flask",
        "xlrd",
        "numpy==1.18.0",
        "pandas",
        "openpyxl",
        "Flask-WTF",
        "Flask-SQLAlchemy",
        "flask-migrate",
        "flask-login",
    ],
    python_requires=">=3.6",
)

