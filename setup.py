#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from setuptools import setup, find_packages


def read_file(name):
    with open(name) as f:
        return f.read().strip()


install_requires = [
    'requests',
    'siggen',
    'ujson',
]

setup(
    name='fx-crash-sig',
    version='0.1.11',
    description=' Get crash signature from Firefox crash trace ',
    long_description=read_file('README.md'),
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
        'Development Status :: 2 - Pre-Alpha',
    ]
)
