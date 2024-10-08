# DEPRECATED: fx-crash-sig

## Project status

This project is deprecated as of October 8th, 2024.

https://github.com/mozilla-services/fx-crash-sig/issues/111

The fx-crash-sig library was initially created as part of a summer internship
project to look at symbolicating and generating signatures for crash pings. It
evolved past that project in a few spurts as it was getting used in different
ways.

This project has become difficult to maintain. There isn't much of a test
suite. The API isn't conductive to symbolicating crash pings at scale. We don't
have time to improve these issues.

Given that, we're deprecating this library. We won't be maintaining it going forward.

If you use this library, we encourage you to replace fx-crash-sig code with:

1. symbolication calls:
   * https://symbolication.services.mozilla.com/
   * https://mozilla-eliot.readthedocs.io/en/latest/symbolication.html
2. signature generation:
   * use [socorro-siggen](https://github.com/willkg/socorro-siggen/)
   * use Crash Stat's [Crash Signature API](https://crash-stats.mozilla.org/api/#CrashSignature)


## Project

Symbolicates crash pings and generates signatures.

Take crash ping stack traces and:

1. Use [Mozilla Symbolication Service](https://symbolication.services.mozilla.com)
   symbolication to symbolicate crash ping stack traces
2. Use [socorro-siggen](https://github.com/willkg/socorro-siggen) library to
   generate a crash signature


Project details:

* Code: https://github.com/mozilla-services/fx-crash-sig
* Issues: https://github.com/mozilla-services/fx-crash-sig/issues
* License: MPL v2
* Documentation: This README


## Install (from [PyPI](https://pypi.org/project/fx-crash-sig/))

```sh
pip install fx-crash-sig
```

## Usage

[Example script](/fx_crash_sig/example.py):

```py
import json

from fx_crash_sig.crash_processor import CrashProcessor

with open("crashping.json") as fp:
    crash_ping = json.load(fp)

crash_processor = CrashProcessor()

signature_result = crash_processor.get_signature(crash_ping)
print(signature_result.signature)
```

Command line (using [sample.json](/sample.json)):

```sh
cat sample.json | fx-crash-sig
```

Run this for more command line help:

```python
fx-crash-sig --help
```


## Minimal crash ping structure

The legacy crash ping (the pingsender one--not the glean one) is documented
here:

https://firefox-source-docs.mozilla.org/toolkit/components/telemetry/data/crash-ping.html

These are the parts of the legacy crash ping we use:

```
- normalized_os                (optional)
- payload:
  - metadata:
    - async_shutdown_timeout   (optional)
    - ipc_channel_error        (optional)
    - oom_allocation_size      (optional)
    - moz_crash_reason         (optional)
  - stack_traces:
    - crash_info:
      - crashing_thread
      - type
    - modules[]
      - debug_file
      - debug_id
      - filename
      - base_addr
    - threads[]
      - frames[]
         - ip
         - module_index
         - trust
```

## API

### fx_crash_sig.crash_processor

* `CrashProcessor`: symbolicates and generates signatures for legacy crash
  pings
  * `__init__`
    * arg: `max_frames`: int (40)
    * arg: `api_url`: str (`https://symbolication.services.mozilla.com/symbolicate/v5`)
    * arg: `verbose`: bool
  * `get_signature`: Takes a crash ping structure, symbolicates it using
    Mozilla Symbolication Service, generates a signature, and returns the
    signature result.
    * signature
      * arg: `crash_ping`: dict
      * returns: `siggen.generator.Result`
  * `symbolicate`: Symbolicates the stack traces in a crash ping structure
    payload.
    * signature
      * arg: `crash_ping`: dict
      * returns: symbolicated stack traces
  * `get_signature_from_symbolicated`: Takes the output of `symbolicate`,
    generates a signature, and returns the signature result.
    * signature
      * arg: `symbolicated`: dict
      * returns: `siggen.generator.Result`

### fx_crash_sig.symbolicate

* `Symbolicator`: symbolicates stack traces
  * `__init__`
    * arg: `max_frames`: int (40)
    * arg: `api_url`: str (`https://symbolication.services.mozilla.com/symbolicate/v5`)
    * arg: `verbose`: bool
  * `symbolicate`: Symbolicates a single stack trace.
    * arg: `stack_trace`: dict
    * returns: symbolicated stack trace
  * `symbolicate_multi`: Symbolicates a list of stack traces.
    * arg: `stack_traces`: list of dicts
    * returns: list of symbolicated traces
