# fx-crash-sig

Symbolicates crash pings and generates signatures.

Take crash ping stack traces and:

1. Use [Mozilla Symbolication Service](https://symbolication.services.mozilla.com)
   symbolication to symbolicate crash ping stack traces
2. Use [socorro-siggen](https://github.com/willkg/socorro-siggen) library to
   generate a crash signature


Project details:

* Code: https://github.com/mozilla/fx-crash-sig
* Issues: https://github.com/mozilla/fx-crash-sig/issues
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

## Minimal crash ping structure

The crash ping is documented here:

https://firefox-source-docs.mozilla.org/toolkit/components/telemetry/data/crash-ping.html

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


## For development

Build:

```sh
make build
```

Lint:

```sh
make lint
make reformat
```

Test:

```sh
make test
```


## Release process

1. Create a `release_X_Y_Z` branch
2. Update version in `setup.py` and update `HISTORY.md`
3. Run tests
4. Push branch to GitHub, create a PR, review it, and merge it
5. Create a signed tag, push to GitHub:
   ```sh
   git tag -s vX.Y.Z
   git push --tags REMOTE TAGNAME
   ```
6. Build and release package files:
   ```sh
   make release
   ```
