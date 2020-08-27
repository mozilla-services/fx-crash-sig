# fx-crash-sig

Get crash signature from Firefox crash trace

Take crash trace and:

1. Use [tecken](https://github.com/mozilla-services/tecken) symbolication to symbolicate crash trace

2. use [socorro-siggen](https://github.com/willkg/socorro-siggen) to get crash signature


## Install (from [PyPI](https://pypi.org/project/fx-crash-sig/))

```sh
pip install fx-crash-sig
```

## Usage

[Example script](/example.py):

```py
from fx_crash_sig import sample_traces
from fx_crash_sig.crash_processor import CrashProcessor

crash_processor = CrashProcessor()

signature = crash_processor.get_signature(sample_traces.trace1)
```

Command line (using [sample.json](/sample.json)):

```sh
cat sample.json | fx-crash-sig
```

```sh
python example.py
```


## For develpment

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

If you have problems with file permissions when using the Docker image, edit
your `.env` file and change the `USER_ID` and `GROUP_ID` values to match your
uid and gid.
