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
    version='0.1.1',
    description=' Get crash signature from Firefox crash trace ',
    long_description=codecs.open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    maintainer='Ben Wu',
    maintainer_email='bwub124@gmail.com',
    url='https://github.com/Ben-Wu/fx-crash-sig',
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points="""
        [console_scripts]
        fx-crash-sig=fx_crash_sig.cmd_get_crash_sig:cmdline
    """,
    classifiers=[
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Programming Language :: Python :: 2 :: Only',
    ]
)
