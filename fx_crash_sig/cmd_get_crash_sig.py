# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function

import argparse
import sys

import ujson as json

from fx_crash_sig import get_version_info
from fx_crash_sig.crash_processor import CrashProcessor


DESCRIPTION = """
Takes raw crash trace and symbolicates it to return the crash signature
"""


def cmdline():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("-w", "--windows", action="store_true")
    parser.add_argument("--version", action="store_true")
    args = parser.parse_args()

    if args.version:
        version_info = get_version_info()
        for key in sorted(version_info):
            print("{}: {}".format(key, version_info[key]))
        return

    crash_processor = CrashProcessor(verbose=args.verbose, windows=args.windows)

    if sys.stdin.isatty():
        print("fx-crash-sig: Failed: pass crash trace using stdin", file=sys.stderr)
        sys.exit(1)

    try:
        payload = json.loads(sys.stdin.read())
    except ValueError:
        print("fx-crash-sig: Failed: Invalid input format", file=sys.stderr)
        sys.exit(1)

    try:
        siggen_result = crash_processor.get_signature(payload)
    except Exception as exc:
        print(f"fx-crash-sig: Failed with exception: {exc}", file=sys.stderr)
        sys.exit(1)

    if siggen_result is not None:
        data = {
            "signature": siggen_result.signature,
            "notes": siggen_result.notes,
            "extra": siggen_result.extra,
        }
        print(json.dumps(data, indent=2))
