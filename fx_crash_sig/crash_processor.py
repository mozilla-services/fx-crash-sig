# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function

from siggen.generator import SignatureGenerator

from fx_crash_sig.symbolicate import Symbolicator


class CrashProcessor:
    def __init__(self, max_frames=40,
                 api_url='https://symbols.mozilla.org/symbolicate/v5',
                 verbose=False):
        self.symbolicator = Symbolicator(max_frames, api_url, verbose)
        self.sig_generator = SignatureGenerator()
        self.verbose = verbose

    def get_signature(self, crash_data):
        symbolicated = self.symbolicate(crash_data)
        if symbolicated is None:
            return None
        signature = self.get_signature_from_symbolicated(symbolicated)
        if self.verbose and len(signature['signature']) == 0:
            print('fx-crash-sig: Failed siggen: {}'.format(signature['notes']))
        return signature

    def symbolicate(self, crash_data):
        return self.symbolicator.symbolicate(crash_data)

    def get_signature_from_symbolicated(self, symbolicated):
        return self.sig_generator.generate(symbolicated)
