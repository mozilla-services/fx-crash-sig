from __future__ import print_function

import ujson as json

from fx_crash_sig import sample_traces
from fx_crash_sig.crash_processor import CrashProcessor

if __name__ == '__main__':
    crash_processor = CrashProcessor()

    trace_dict = json.loads(sample_traces.string_trace1)

    symbolicated = crash_processor.symbolicate(trace_dict)

    print(symbolicated)

    signature = crash_processor.get_signature(symbolicated)

    print(signature)

    signatures = [crash_processor.process_crash_trace(crash)['signature']
                  for crash in [
                      sample_traces.trace1,
                      sample_traces.trace2,
                      sample_traces.trace3,
                  ]]

    print(signatures)
