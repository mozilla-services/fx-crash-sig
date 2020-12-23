# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json
import sys

from siggen.generator import SignatureGenerator

from fx_crash_sig import SYMBOLS_API
from fx_crash_sig.symbolicate import Symbolicator


class CrashProcessor:
    def __init__(
        self, max_frames=40, api_url=SYMBOLS_API, verbose=False, windows=False
    ):
        self.symbolicator = Symbolicator(max_frames, api_url, verbose)
        self.sig_generator = SignatureGenerator()
        self.verbose = verbose
        self.windows = windows

    def get_signature(self, payload):
        symbolicated = self.symbolicate(payload)
        result = self.get_signature_from_symbolicated(symbolicated)
        if self.verbose and len(result.signature) == 0:
            print(
                "fx-crash-sig: Failed siggen: {}".format(result.notes), file=sys.stderr
            )
        return result

    def get_signatures_multi(self, opaque_ids, payloads):
        crash_data = [payload.get("stack_traces", None) for payload in payloads]
        symbolicated = self.symbolicator.symbolicate_multi(crash_data)

        if symbolicated is None:
            # One or more of the crashes errored out, let's do them individually
            # and log the opaque_ids entries for the ones that error out.
            symbolicated = []
            for (opaque_id, crash_datum) in zip(opaque_ids, crash_data):
                symbolicated_datum = self.symbolicator.symbolicate(crash_datum)
                if self.verbose and symbolicated_datum == {}:
                    print(
                        "fx-crash-sig: Failed symbolicating id: {}".format(opaque_id),
                        file=sys.stderr,
                    )
                symbolicated.append(symbolicated_datum)

        sigs = []
        for (payload, sym) in zip(payloads, symbolicated):
            sym = self._postprocess_symbolicated(payload, sym)
            sigs.append(self.get_signature_from_symbolicated(sym))
        return sigs

    def symbolicate(self, payload):
        crash_data = payload.get("stack_traces", None)
        if crash_data is None or len(crash_data) == 0:
            symbolicated = {}
        elif "ipc_channel_error" in payload:
            # ipc_channel_error will always overwrite the crash signature so
            # we don't need to symbolicate to get the signature
            symbolicated = {}
        else:
            symbolicated = self.symbolicator.symbolicate(crash_data)

        return self._postprocess_symbolicated(payload, symbolicated)

    def _postprocess_symbolicated(self, payload, symbolicated):
        metadata = payload.get("metadata") or {}
        meta_fields = {
            "ipc_channel_error": "ipc_channel_error",
            "MozCrashReason": "moz_crash_reason",
            "OOMAllocationSize": "oom_allocation_size",
            "AsyncShutdownTimeout": "async_shutdown_timeout",
        }

        symbolicated["os"] = "Windows NT" if self.windows else "Not Windows"
        for k in meta_fields.keys():
            if k in metadata:
                symbolicated[meta_fields[k]] = metadata[k]

        # async_shutdown_timeout should be json string not dict
        if "async_shutdown_timeout" in metadata:
            try:
                metadata["async_shutdown_timeout"] = json.dumps(
                    metadata["async_shutdown_timeout"]
                )
            except TypeError:
                metadata.pop("async_shutdown_timeout")

        return symbolicated

    def get_signature_from_symbolicated(self, symbolicated):
        return self.sig_generator.generate(symbolicated)
