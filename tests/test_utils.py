# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

import pytest

from fx_crash_sig.crash_processor import deep_get


@pytest.mark.parametrize(
    "structure, path, expected",
    [
        ({}, "a.b.c", None),
        ({"a": 5}, "a", 5),
        ({"a": {"b": 5}}, "a.b", 5),
    ],
)
def test_deep_get(path, structure, expected):
    assert deep_get(structure, path) == expected
