# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

from __future__ import print_function

import ujson as json

from fx_crash_sig import sample_traces
from fx_crash_sig.crash_processor import CrashProcessor


def wrap_in_payload(crash_data):
    return {
        'metadata': {},
        'stackTraces': crash_data
    }


if __name__ == '__main__':
    crash_processor = CrashProcessor(verbose=True)

    trace_dict = wrap_in_payload(json.loads(sample_traces.string_trace2))

    symbolicated = crash_processor.symbolicate(trace_dict)

    print(symbolicated)

    if symbolicated is not None:
        signature = crash_processor.get_signature_from_symbolicated(symbolicated)
        print(signature)

    signatures = [crash_processor.get_signature(wrap_in_payload(crash))
                  for crash in [
                      sample_traces.trace1,
                      sample_traces.trace2,
                  ]]

    signatures = [sig['signature'] for sig in signatures if sig is not None]

    print(signatures)
