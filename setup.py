#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from setuptools import setup, find_packages


def read_file(name):
    with open(name) as f:
        return f.read().strip()


install_requires = [
    "requests",
    "siggen>=1.0.0,<2.0.0",
    "ujson",
]

setup(
    name="fx-crash-sig",
    version="0.1.12",
    description="Get crash signature from Firefox crash ping",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/mozilla/fx-crash-sig",
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    entry_points="""
        [console_scripts]
        fx-crash-sig=fx_crash_sig.cmd_get_crash_sig:cmdline
    """,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Development Status :: 2 - Pre-Alpha",
    ]
)
