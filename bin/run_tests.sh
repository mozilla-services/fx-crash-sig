#!/bin/bash

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# Usage: bin/run_tests.sh

echo ">>>Running pytest..."
pytest tests/
echo ""

echo ">>> Testing fx-crash-sig command..."
cat sample.json | fx-crash-sig
