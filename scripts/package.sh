#!/usr/bin/env bash
# Build dist/csm-customer-collab.zip for upload as a skill in claude.ai or Claude Desktop.
# Runs the test suite first unless --no-tests is passed (the package test itself uses that flag).
set -euo pipefail
cd "$(dirname "$0")/.."
if [[ "${1:-}" != "--no-tests" ]]; then
  python3 -m unittest tests.test_skill
fi
mkdir -p dist
rm -f dist/csm-customer-collab.zip
(cd skills && zip -q -r -X ../dist/csm-customer-collab.zip csm-customer-collab -x '*.DS_Store')
echo "Built dist/csm-customer-collab.zip"
