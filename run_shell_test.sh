#!/usr/bin/env bash

set -x
set -e

./.venv/bin/directory_cleaner -c configs/taskcluster_unix.toml -v /tmp/test-directory
