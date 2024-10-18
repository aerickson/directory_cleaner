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

mkdir -p $BASE_DIR/caches/test1
mkdir -p $BASE_DIR/caches/test2
touch $BASE_DIR/caches/test1/file1
touch $BASE_DIR/caches/test2/file2

mkdir -p $BASE_DIR/misc
touch $BASE_DIR/misc/test.txt

touch $BASE_DIR/junk1
touch $BASE_DIR/junk2

cp -r /System/Applications/Utilities/Terminal.app $BASE_DIR
xattr -r -w com.apple.quarantine "0081;5f8e2361;Safari;1234ABC-5678-DEF0" $BASE_DIR/Terminal.app
