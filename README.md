# devpi-private-mirrors

[![PyPI version shields.io](https://img.shields.io/pypi/v/devpi-private-mirrors.svg)](https://pypi.python.org/pypi/devpi-private-mirrors/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/devpi-private-mirrors.svg)](https://pypi.python.org/pypi/devpi-private-mirrors/)
[![PyPI download month](https://img.shields.io/pypi/dm/devpi-private-mirrors.svg)](https://pypi.python.org/pypi/devpi-private-mirrors/)

Plugin prevent mixing packages using both private and public mirrors at the same time.

## Installation

```sh
pip install devpi-private-base
```

There is no configuration needed as devpi-server will automatically discover the plugin
through calling hooks using the setuptools entry points mechanism.

## Motivation

Sometimes you need to use private mirrors, but still want access to pypi.

With base devpi only option is to specify both as private index bases,
but in that case you got mix of packages and their versions between
private and public mirrors.

Which leads to security and compatibility issues.

This plugin allows mark some indexes as private and hide all packages from them
from public indexes.

## Usage

Create local index with `stage_private_base` type with several mirrors

```
devpi index -c root/dev type=stage_private_base bases=root/private1,root/private2,root/pypi
```

Set `private_base` option for all private bases

```
devpi root/private1 private_base=True
devpi root/private2 private_base=True
```

Now private mirrors will not be mixed with public.

Note: private indexes can be mixed with each other (for example, if you have some version
of package in private1 and some in private2, you will get both versions).
