#!/usr/bin/env python

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import re
from setuptools import setup, find_packages


def read_file(name):
    with open(name) as fp:
        return fp.read().strip()


def get_version():
    fn = os.path.join("fx_crash_sig", "__init__.py")
    vsre = r"""^__version__ = ['"]([^'"]*)['"]"""
    version_file = open(fn, "rt").read()
    return re.search(vsre, version_file, re.M).group(1)


install_requires = [
    "requests>=2.25.0,<3.0.0",
    "ujson>=4.0.0,<5.0.0",

    # NOTE(willkg): We always want to run the latest siggen, so don't pin the
    # version
    "siggen>=1.0.0,<2.0.0",
]

extras_require = {
    "bq": ["google-cloud-bigquery>=2.5.0,<3.0.0"]
}

setup(
    name="fx-crash-sig",
    version=get_version(),
    description="Get crash signature from Firefox crash trace",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/mozilla/fx-crash-sig",
    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
    extras_require=extras_require,
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
