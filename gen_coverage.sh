#!/usr/bin/env bash

#set -x
set -e

# .coveragerc sets options
pytest -vv --cov=directory_cleaner --cov-report=html


echo ""
echo "to view the report, run:"
echo "  open htmlcov/index.html"
