from __future__ import print_function

import sys

import ujson as json
from siggen.generator import SignatureGenerator

from fx_crash_sig.symbolicate import Symbolicator

DESCRIPTION = """
Takes raw crash trace and symbolicates it to return the crash signature
"""


def cmdline():
    symbolicator = Symbolicator()
    generator = SignatureGenerator()
    crash_data = json.loads(sys.stdin.read())

    symbolicated = symbolicator.symbolicate(crash_data)

    signature = generator.generate(symbolicated)

    print(signature)
