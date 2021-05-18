# DiddiParser versions

## diddiparser 1.1.0

- Added a specific console script: `diddiparser`.
- `DiddiScriptFile` now accepts strings.
   - **For doing it, change the _`func`_ argument to the new function `stringToScript()` at the constructor (`__init__`).**
 - Added a security policy and a changelog file.
 - The command line tool (now called by the console script) has been modified.
 - Added a `MANIFEST.in` file.

## diddiparser 1.0.0

- Initial version
- Parse DiddiScript files and DiddiScript setup files.
- A simple `demo()` function added.
