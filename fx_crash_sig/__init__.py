# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pkg_resources
import sys

from siggen import (
    __version__ as siggen_version,
    __releasedate__ as siggen_releasedate
)


SYMBOLS_API = 'https://symbols.mozilla.org/symbolicate/v5'


def get_version_info():
    """Returns version information for debugging."""
    # Figure out fx-crash-sig version using metadata from the install. If it's not
    # installed, then we'll call it "unknown".
    try:
        fx_crash_sig_version = pkg_resources.get_distribution('fx-crash-sig').version
    except (AttributeError, pkg_resources.DistributionNotFound):
        fx_crash_sig_version = 'unknown'

    return {
        'siggen': '{} ({})'.format(siggen_version, siggen_releasedate),
        'python': sys.version.replace('\n', ' '),
        'fx-crash-sig': fx_crash_sig_version
    }
