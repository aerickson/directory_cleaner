#!/usr/bin/env bash

set -x
set -e

./.venv/bin/directory_cleaner -c configs/taskcluster_unix.toml -v --remove-empty-directories -d /tmp/test-directory

./.venv/bin/directory_cleaner -c configs/taskcluster_unix.toml -v --remove-empty-directories /tmp/test-directory

# set +x

# echo "Should say: "
# echo "     Cleaned directory '/tmp/test-directory'. Removed 4 files and 1 directories."
