# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import json

from siggen.generator import SignatureGenerator

from fx_crash_sig import SYMBOLICATION_API
from fx_crash_sig.symbolicate import Symbolicator


class CrashProcessor:
    def __init__(self, max_frames=40, api_url=SYMBOLICATION_API, verbose=False):
        self.symbolicator = Symbolicator(max_frames, api_url, verbose)
        self.sig_generator = SignatureGenerator()
        self.verbose = verbose

    def get_signature(self, crash_ping):
        """Takes a crash_ping, symbolicates it, generates signature, returns result

        :args dict crash_ping: a crash ping

        :returns: signature result

        """
        symbolicated = self.symbolicate(crash_ping)
        signature_result = self.get_signature_from_symbolicated(symbolicated)
        if self.verbose and len(signature_result.signature) == 0:
            print(f'fx-crash-sig: Failed siggen: {signature_result.notes}')
        return signature_result

    def symbolicate(self, crash_ping):
        # These are the parts of the crash ping we use:
        #
        # - normalized_os
        # - payload:
        #   - crash_data
        #   - metadata:
        #     - async_shutdown_timeout
        #     - ipc_channel_error
        #     - oom_allocation_size
        #     - moz_crash_reason
        #   - stack_traces:
        #     - crash_info:
        #       - crashing_thread
        #     - modules[]
        #       - debug_file
        #       - debug_id
        #       - filename
        #       - base_addr
        #     - threads[]
        #       - frames[]
        #          - ip
        #          - module_index
        #          - trust
        normalized_os = crash_ping.get("normalized_os") or ""
        payload = crash_ping["payload"]

        if isinstance(payload, str):
            # If payload is a string, it's probably a JSON-encoded string
            # straight from telemetry.crash. Try to decode it and if that
            # fails, let the exception bubble up because there's nothing we can
            # do with this crash report
            payload = json.loads(payload)

        metadata = payload.get("metadata", {})
        stack_traces = payload["stack_traces"]

        if stack_traces is None or len(stack_traces) == 0:
            symbolicated = {}
        elif metadata.get("ipc_channel_error"):
            # ipc_channel_error will always overwrite the crash signature so
            # we don't need to symbolicate to get the signature
            symbolicated = {}
        else:
            symbolicated = self.symbolicator.symbolicate(stack_traces)

        metadata_fields = [
            "async_shutdown_timeout",
            "oom_allocation_size",
            "moz_crash_reason",
            "ipc_channel_error"
        ]

        symbolicated["os"] = (
            "Windows NT" if normalized_os.startswith("Windows") else ""
        )
        for field_name in metadata_fields:
            if metadata.get(field_name):
                symbolicated[field_name] = metadata[field_name]

        # async_shutdown_timeout should be json string not dict, so we need to
        # encode it
        if metadata.get("async_shutdown_timeout"):
            try:
                metadata["async_shutdown_timeout"] = json.dumps(
                    metadata["async_shutdown_timeout"]
                )
            except TypeError:
                metadata.pop("async_shutdown_timeout")

        return symbolicated

    def get_signature_from_symbolicated(self, symbolicated):
        """Takes output of symbolicate() and returns a signature result

        :args dict symbolicated: the result of .symbolicate()

        :returns: a signature result

        """
        return self.sig_generator.generate(symbolicated)
