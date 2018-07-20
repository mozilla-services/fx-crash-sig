# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function

import argparse
import sys

import ujson as json

from fx_crash_sig.crash_processor import CrashProcessor

DESCRIPTION = """
Takes raw crash trace and symbolicates it to return the crash signature
"""


def cmdline():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-w', '--windows', action='store_true')
    args = parser.parse_args()

    crash_processor = CrashProcessor(verbose=args.verbose,
                                     windows=args.windows)
    try:
        payload = json.loads(sys.stdin.read())
    except ValueError:
        if args.verbose:
            print('fx-crash-sig: Failed: Invalid input format')
        return

    try:
        signature = crash_processor.get_signature(payload)
        if signature is not None:
            print(json.dumps(signature))
    except Exception as e:
        if args.verbose:
            print('fx-crash-sig: Failed: {}'.format(e.message))
