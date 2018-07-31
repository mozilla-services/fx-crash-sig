# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function

import json
from siggen.generator import SignatureGenerator

from fx_crash_sig.symbolicate import Symbolicator


class CrashProcessor:
    def __init__(self, max_frames=40,
                 api_url='https://symbols.mozilla.org/symbolicate/v5',
                 verbose=False,
                 windows=False):
        self.symbolicator = Symbolicator(max_frames, api_url, verbose)
        self.sig_generator = SignatureGenerator()
        self.verbose = verbose
        self.windows = windows

    def get_signature(self, payload):
        symbolicated = self.symbolicate(payload)
        signature = self.get_signature_from_symbolicated(symbolicated)
        if self.verbose and len(signature['signature']) == 0:
            print('fx-crash-sig: Failed siggen: {}'.format(signature['notes']))
        return signature

    def symbolicate(self, payload):
        crash_data = payload.get('stackTraces', None)
        if crash_data is None or len(crash_data) == 0:
            symbolicated = {}
        elif 'ipc_channel_error' in payload:
            # ipc_channel_error will always overwrite the crash signature so
            # we don't need to symbolicate to get the signature
            symbolicated = {}
        else:
            symbolicated = self.symbolicator.symbolicate(crash_data)

        metadata = payload['metadata']

        meta_fields = {
            'ipc_channel_error': 'ipc_channel_error',
            'MozCrashReason': 'moz_crash_reason',
            'OOMAllocationSize': 'oom_allocation_size',
            'AsyncShutdownTimeout': 'async_shutdown_timeout'
        }

        symbolicated['os'] = 'Windows NT' if self.windows else 'Not Windows'
        for k in meta_fields.keys():
            if k in metadata:
                symbolicated[meta_fields[k]] = metadata[k]

        # async_shutdown_timeout should be json string not dict
        if 'async_shutdown_timeout' in metadata:
            try:
                metadata['async_shutdown_timeout'] = (
                    json.dumps(metadata['async_shutdown_timeout']))
            except TypeError:
                metadata.pop('async_shutdown_timeout')

        return symbolicated

    def get_signature_from_symbolicated(self, symbolicated):
        return self.sig_generator.generate(symbolicated)
