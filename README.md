# fx-crash-sig

Get crash signature from Firefox crash trace

Take crash trace and:

1. Use [tecken](https://github.com/mozilla-services/tecken) symbolication to symbolicate crash trace

2. use [socorro-siggen](https://github.com/willkg/socorro-siggen) to get crash signature


## Install (from [PyPI](https://pypi.org/project/fx-crash-sig/))

To install:

```sh
pip install fx-crash-sig
```

(Optional) Install with google-cloud-bigquery library requirements:

```sh
pip install fx-crash-sig[bq]
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
$ cat sample.json | fx-crash-sig
EMPTY: no crashing thread identified
```

```sh
$ python example.py
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

Test docker environment:

```sh
make test
```

If you have problems with file permissions when using the Docker image, edit
your `.env` file and change the `USER_ID` and `GROUP_ID` values to match your
uid and gid.

Test against Python versions:

```sh
tox
```

Note: This requires you have Python environments set up and a virtual
environment with tox installed.


## Release process

1. Create a `release_X_Y_Z` branch
2. Update version and release date in `fx_crash_sig/__init__.py`
3. Run tests
4. Push branch to GitHub, create a PR, review it, and merge it
5. Create a signed tag, push to GitHub:
   ```sh
   git tag -s vX.Y.Z
   git push --tags REMOTE TAGNAME
   ```
6. Build package files:
   ```sh
   python setup.py sdist bdist_wheel
   ```
   Be sure to use Python 3 with a virtualenv with an updated `requirements.dev.txt` file.
7. Upload to PyPI:
   ```sh
   twine upload dist/*
   ```
