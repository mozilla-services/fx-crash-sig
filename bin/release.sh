#!/bin/bash

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Usage: bin/release.sh
#
# Update the version in setup.py, create a signed tag, then run this script to
# generate the release files.
#
# This requires a PyPI token set up in .pypirc with repository "fxcrashsig".
# To create a token, see:
#
# https://pypi.org/manage/account/token/
#
# To configure .pypirc, see:
#
# https://packaging.python.org/en/latest/specifications/pypirc/

set -euo pipefail


CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "${CURRENT_BRANCH}" != "main" ]];
then
    echo "You need to be in the main branch to run this."
    echo "Exiting."
    exit 1
fi

LAST_TAG=$(git tag --list | sort -u | tail -n 1)
LAST_TAG_SHA=$(git rev-parse ${LAST_TAG})
MAIN_SHA=$(git rev-parse main)

if [[ "${LAST_TAG_SHA}" != "${MAIN_SHA}" ]];
then
    echo "Last tag (${LAST_TAG}) sha (${LAST_TAG_SHA}) does not match main (${MAIN_SHA})."
    echo "Did you create a signed tag?"
    echo "Exiting."
    exit 1
fi

rm -rf dist/

python -m build
twine upload --repository fxcrashsig dist/*
