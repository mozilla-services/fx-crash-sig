#!/usr/bin/env python

import codecs

from setuptools import setup, find_packages

install_requires = [
    'requests',
    'siggen',
    'ujson',
]

setup(
    name='fx-crash-sig',
    version=0.1,
    description=' Get crash signature from Firefox crash trace ',
    long_description=codecs.open('README.md', encoding='utf-8').read(),
    maintainer='Ben Wu',
    maintainer_email='benjaminwu124@gmail.com',
    url='https://github.com/Ben-Wu/fx-crash-sig',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points="""
        [console_scripts]
        fx-crash-sig=fx_crash_sig.cmd_get_crash_sig:cmdline
    """
)
