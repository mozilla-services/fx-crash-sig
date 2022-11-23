# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# NOTE(willkg): This tests symbolication API production servers.

from fx_crash_sig import sample_traces
from fx_crash_sig.symbolicate import Symbolicator


def is_valid_symbolication(symbolicated):
    assert isinstance(symbolicated, dict) is True
    assert "crashing_thread" in symbolicated
    assert "threads" in symbolicated


def test_symbolicate_single():
    symbolicator = Symbolicator()

    symbolicated = symbolicator.symbolicate(sample_traces.trace1)
    is_valid_symbolication(symbolicated)


def test_symbolicate_single2():
    symbolicator = Symbolicator()

    symbolicated = symbolicator.symbolicate(sample_traces.trace2)
    is_valid_symbolication(symbolicated)


def test_symbolicate_none():
    symbolicator = Symbolicator()

    symbolicated = symbolicator.symbolicate(None)
    assert symbolicated == {}


def test_symbolicate_multi():
    symbolicator = Symbolicator()

    symbolicated = symbolicator.symbolicate_multi(
        [sample_traces.trace1, sample_traces.trace2]
    )
    for s in symbolicated:
        is_valid_symbolication(s)
