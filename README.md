# Valexa
[![Build Status](https://travis-ci.org/GroupeChemia/valexa.svg?branch=master)](https://travis-ci.org/GroupeChemia/valexa)

## Generate an executable
This project use [Pyinstaller](https://www.pyinstaller.org/).

Run the following command to generate an executable.

```
pipenv run pyinstaller -y valexa.spec
```

This will generate the bundle in a subdirectory called `dist`.