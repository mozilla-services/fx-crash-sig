# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import sys

from siggen import __version__ as siggen_version, __releasedate__ as siggen_releasedate


# yyyymmdd
__releasedate__ = ""
# x.y.z or x.y.z.dev0 -- semver
__version__ = "0.1.11"


# Symbolication API
SYMBOLS_API = "https://symbols.mozilla.org/symbolicate/v5"


def get_version_info():
    """Returns version information of fx-crash-sig and dependencies for debugging."""
    return {
        "siggen": "{} ({})".format(siggen_version, siggen_releasedate),
        "python": sys.version.replace("\n", " "),
        "fx-crash-sig": "{} ({})".format(__version__, __releasedate__ or "dev"),
    }
