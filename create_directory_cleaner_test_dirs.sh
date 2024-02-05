#!/usr/bin/env bash

set -e
set -x

BASE_DIR="/tmp/test-directory"

mkdir -p $BASE_DIR
touch $BASE_DIR/Downloads

mkdir -p $BASE_DIR/tasks
mkdir -p $BASE_DIR/tasks/task_123
mkdir -p $BASE_DIR/tasks/task_3546
touch $BASE_DIR/tasks/task_123/test_file1
touch $BASE_DIR/tasks/task_3546/test_file_999

mkdir -p $BASE_DIR/cache/test1
mkdir -p $BASE_DIR/cache/test2
touch $BASE_DIR/cache/test1/file1
touch $BASE_DIR/cache/test2/file2

touch $BASE_DIR/junk1
touch $BASE_DIR/junk2
