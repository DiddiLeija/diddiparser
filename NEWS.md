# DiddiParser versions

## diddiparser 1.3

- The stdlib is now `diddiparser.lib`
- Bug fixes

## diddiparser 1.2.1

- Created `diddiparser.__main__`
  - Now, you can call the console script using `python -m diddiparser`.
- New feature: _function definitions_.
  - You can define functions using a [DiddiScript extensions file](https://github.com/DiddiLeija/diddiparser/wiki/Extensions-file).
- New feature: _`examples` folder on the GitHub source_.
  - See some examples of the DiddiParser usage. See it [here](https://github.com/DiddiLeija/diddiparser/tree/main/examples).
- Bug fixes
  - `diddiparser.parser` had some bug fixes.
  - `diddiparser.main` (and the console script) had some bug fixes.

## diddiparser 1.1.1

- Bug fixes
  - The block commentaries have been fixed. Reference to PR [\#21](http://github.com/diddileija/diddiparser/pull/21).

## diddiparser 1.1.0

- Added a specific console script: `diddiparser`.
- `DiddiScriptFile` and its subclasses now accept strings.
   - **For doing it, change the _`func`_ argument to the new function `stringToScript()` at the constructor (`__init__`).**
 - Added a security policy and a changelog file.
 - The command line tool (now called by the console script) has been modified.
 - Added a `MANIFEST.in` file.

## diddiparser 1.0.0

- Initial version
- Parse DiddiScript files and DiddiScript setup files.
- A simple `demo()` function added.
