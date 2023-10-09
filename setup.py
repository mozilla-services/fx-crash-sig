#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from setuptools import setup, find_packages


def read_file(name):
    with open(name) as f:
        return f.read().strip()


VERSION = "1.0.2"

INSTALL_REQUIRES = [
    "requests",
    "siggen",
    "importlib_metadata",
]


setup(
    name="fx-crash-sig",
    version=VERSION,
    description="Get crash signature from Firefox crash ping",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/mozilla/fx-crash-sig",
    packages=find_packages(),
    include_package_data=True,
    install_requires=INSTALL_REQUIRES,
    python_requires=">=3.8",
    entry_points="""
        [console_scripts]
        fx-crash-sig=fx_crash_sig.cmd_get_crash_sig:cmdline
    """,
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Development Status :: 2 - Pre-Alpha",
    ],
)
