# directory_cleaner

## overview

Deletes files in a directory that aren't on the exception list.

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

# installation
```bash
# build package (see above)

# install
pip3 install directory_cleaner-0.1.0-py3-none-any.whl
```
