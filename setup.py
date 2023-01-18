#!/usr/bin/env python3

from setuptools import setup, find_packages

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='async7zip',
    author='Vladislav Tislenko',
    author_email='keklick1337@gmail.com',
    install_requires=[],
    url='https://github.com/keklick1337/async7zip',
    project_urls={
        'Documentation': 'https://github.com/keklick1337/async7zip',
        'Bug Reports':
        'https://github.com/keklick1337/async7zip/issues',
        'Source Code': 'https://github.com/keklick1337/async7zip',
    },
    long_description=long_description,
    long_description_content_type='text/markdown',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    python_requires='>=3.9',
)