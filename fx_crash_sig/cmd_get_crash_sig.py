# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import argparse
import json
import sys

from fx_crash_sig import get_version_info
from fx_crash_sig.crash_processor import CrashProcessor


DESCRIPTION = """
Takes raw crash trace and symbolicates it to return the crash signature
"""


def cmdline():
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument("--version", action="store_true")
    args = parser.parse_args()

    if args.version:
        version_info = get_version_info()
        for key, val in sorted(version_info.items()):
            print(f"{key}: {val}")
        return

    if sys.stdin.isatty():
        print("fx-crash-sig: Failed: pass crash trace using stdin", file=sys.stderr)
        sys.exit(1)

    crash_processor = CrashProcessor(verbose=args.verbose)
    try:
        payload = json.loads(sys.stdin.read())
    except ValueError:
        if args.verbose:
            print("fx-crash-sig: Failed: Invalid input format", file=sys.stderr)
        sys.exit(1)

    result = crash_processor.get_signature(payload)
    if result is not None:
        print(f"signature: {result.signature}")
        print(f"notes:     ({len(result.notes)})")
        for note in result.notes:
            print(f"           * {note}")
