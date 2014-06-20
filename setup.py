#!/usr/bin/env python
# encoding: utf-8

from setuptools import setup, find_packages
import glob


setup(
    name="andromap",
    version="0.1",
    packages=find_packages(),
    scripts=glob.glob('scripts/*.py'),

    install_requires=['numpy',
                      'matplotlib',
                      'astropy',
                      'pil',
                      'aplpy',
                      'pymongo',
                      'shapely'],

    package_data={'': ['*.txt', '*.rst']},

    # metadata for upload to PyPI
    author="Jonathan Sick",
    author_email="jonathansick@mac.com",
    description="Package for making maps of the ANDROIDS survey footprint",
    license="BSD",
    keywords="astronomy",
    url="https://github.com/jonathansick/andromap",
)
