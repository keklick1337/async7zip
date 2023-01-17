#!/usr/bin/env python3

from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='async7zip',
    version='1.0.0',
    author='Vladislav Tislenko',
    author_email='keklick1337@gmail.com',
    packages=find_packages(),
    install_requires=[],
    long_description=long_description,
    long_description_content_type='text/markdown',
)