# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


def deep_get(data, path, default=None):
    """Retrieves a node in the structure by dotted path

    :arg data: structure of Python dicts
    :arg path: dotted path string to the item in question
    :arg default: default value to return if the item doesn't exist

    :returns: the item in question or default

    """
    item = data
    path = path.split(".")
    for part in path:
        if isinstance(item, dict) and part in item:
            item = item[part]
        else:
            return default

    return item
