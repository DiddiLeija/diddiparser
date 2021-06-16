# DiddiParser - version 1.1.1

Parse DiddiScript files and run their simple syntax.

## What's DiddiScript?

Refer to [GRAMMAR.md](http://github.com/diddileija/diddiparser/blob/main/GRAMMAR.md) to learn about the DiddiScript
environment.

## DiddiParser installation

DiddiParser is a pure Python package, installable from [PyPI](http://pypi.org/project/diddiparser) with Pip:

```
pip install diddiparser
```

## Usage of DiddiParser

After installing, import the features like this examples:

### Using DiddiParser on Python scripts

```python
from diddiparser.parser import (DiddiScriptFile,
                                DiddiScriptSetup,
                                stringToScript,
                                demo)
from diddiparser import __version__, __author__
```

### Module command-line options

We created `diddiparser.main` for doing this. Use it as follows:

```
python -m diddiparser.main [args]
```

### Specific console script

You don't even need to call the `diddiparser.main` module. Just use
the linked console script:

```
diddiparser [args]
```

## More help is here!

Go to [SECURITY.md](http://github.com/diddileija/diddiparser/blob/main/SECURITY.md) to view the supported versions and security advisories. View [CHANGELOG.md](http://github.com/diddileija/diddiparser/blob/main/CHANGELOG.md) to view all the published versions. Or go to the related [wiki](http://github.com/diddileija/diddiparser/wiki/Home) to read a larger explanation of the package contents.

## Want to help?

Read the [contribution document](http://github.com/diddileija/diddiparser/blob/main/CONTRIBUTING.md) to learn how to contribute to DiddiParser. 

Also, you can view the 
[standing GitHub project about DiddiParser](http://github.com/users/diddileija/projects/2) to watch all the issues, PRs and discussions organized on the columns `To Do`, `In progress` and `Done`.
