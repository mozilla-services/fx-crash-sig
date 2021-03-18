# fx-crash-sig

Symbolicates crash pings and generates signatures.

Take crash ping stack traces and:

1. Use [tecken](https://github.com/mozilla-services/tecken) symbolication to symbolicate crash ping stack traces

2. use [socorro-siggen](https://github.com/willkg/socorro-siggen) to get crash signature


## Install

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

## Minimal crash ping structure

These are the parts of the crash ping we use:

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
