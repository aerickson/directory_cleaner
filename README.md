# directory_cleaner

![Test Status](https://github.com/aerickson/directory_cleaner/actions/workflows/main.yml/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/aerickson/directory_cleaner/badge.svg?branch=more_tests)](https://coveralls.io/github/aerickson/directory_cleaner?branch=more_tests)

## overview

Deletes files and empty directories in a specific directory that aren't on the exception list.

- Files under an excepted directory will also be excluded from deletion.

## usage

```bash
# basic usage
directory_cleaner -c config.toml directory_to_clean

# see help output for complete options
directory_cleaner -h
```

## building

```bash
poetry build
# output will be in /dist
```

## installation
```bash
# build package (see above)

# install
pip3 install directory_cleaner-0.1.0-py3-none-any.whl
```

## TODOs

- start writing commits in the convention commit format (https://www.conventionalcommits.org/en/v1.0.0/)
- start generating a changelog with a tool like https://github.com/KeNaCo/auto-changelog
