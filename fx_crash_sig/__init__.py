# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# NOTE(willkg): we're using the backfill library until we can drop support for
# Python 3.7.
from importlib_metadata import (
    version as importlib_version,
    PackageNotFoundError,
)
import sys

from siggen import __version__ as siggen_version


# Default symbolication API URL
SYMBOLICATION_API = "https://symbolication.services.mozilla.com/symbolicate/v5"

try:
    __version__ = importlib_version("fx-crash-sig")
except PackageNotFoundError:
    __version__ = "unknown"


def get_version_info():
    """Returns version information for debugging."""
    return {
        "siggen": f"{siggen_version}",
        "python": sys.version.replace("\n", " "),
        "fx-crash-sig": __version__,
    }
