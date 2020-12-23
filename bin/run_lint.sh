#!/bin/bash

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Usage: bin/run_lint.sh [--reformat]
#
# Runs linting and code reformatting.
#
# This should be called from inside a container.

set -e

BLACKARGS=("--line-length=88" "--target-version=py36" fx_crash_sig tests)

if [[ $1 == "--reformat" ]]; then
    echo ">>> reformat"
    black "${BLACKARGS[@]}"

else
    echo ">>> flake8 ($(python --version))"
    flake8 fx_crash_sig tests

    echo ">>> black"
    black --check "${BLACKARGS[@]}"
fi
