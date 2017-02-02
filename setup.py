#!/usr/bin/env python3

from setuptools import setup

setup(
    packages=['accli'],
    install_requires=['jinja2', 'pyyaml'],
    entry_points={
        'console_scripts': {
            'accli = accli.cli:main'
        }
    }
)
