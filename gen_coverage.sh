#!/usr/bin/env bash

#set -x
set -e

pytest --cov=tc_directory_cleaner --cov-report=html
