from __future__ import print_function

import sys

import ujson as json

from fx_crash_sig.crash_processor import CrashProcessor

DESCRIPTION = """
Takes raw crash trace and symbolicates it to return the crash signature
"""


def cmdline():
    crash_processor = CrashProcessor()
    crash_data = json.loads(sys.stdin.read())

    signature = crash_processor.get_signature(crash_data)

    print(signature)
