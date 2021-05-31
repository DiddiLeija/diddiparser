![DiddiScript icon](https://github.com/DiddiLeija/DiddiLeija/blob/main/diddiscript-icon-(short).png)

# The DiddiScript grammar

## About the language

DiddiParser executes Python code on DiddiScript files. These are
cross-language files, allowing us to build, for example, complex code on C, Python
and JavaScript at a time, saving the results on a variable that the parsers can
take and use by themselves.

## Simple rules

DiddiScript parser follow this rules:

- Every instruction ends with a `;`.
- Block comments must have a `/*` at the beginning and a `*/`.
- Single-line comments must begin with a `!#`.

For example, `samplecode.diddi`:

```
/*
   - Sample code

   These lines must be ignored by the interpreter. I will enter some
   dummy code. Ignore them by now.
*/

!# Run the easiest Python 3 code ever!

pyrun('print("Hello world!")');

!# Open some Ramz Editions features (use 'ramz_goto()'):

ramz_goto('DiddiCmd');         !# DiddiCmd
ramz_goto('Control de Agua');  !# DiddiOS 3

!# Open a file

openfile('C:/Program Files/Ramz Editions/people.txt');

!# Open a python "subprocess.Popen()"

subprocess_run('python -m turtledemo.minimal_hanoi');
```

## Running Python code

To use Python code, call the function `pyrun()`:

```
!# Run the easiest Python 3 code ever!

pyrun('print("Hello world!")');
```

The function above will run on Python code `print("Hello world!")`.

#### Python code rules

Go to __"Some function code rules"__, on this article.

#### Running another kind of code

Use the `[lang]run()` syntax, like we used on Python:

```
!# (these are hypotetical examples, of course)
jsrun(...);   !# JavaScript code?
javarun(...); !# Java code?
crun(...);    !# C code?
cpprun(...);  !# C++ code?
csrun(...);   !# C# code?

!# (known language implementations below)
pyrun(...);   !# Python code
```

**Allowed languages:** Python.

_\(Other languages will be available in the future. Reference to the issue [\#8](http://github.com/diddileija/diddiparser/issues/8) for discussing a possible language implementation\)._

## Redirect to _Ramz. Editions_ products

The function `ramz_goto()` will try to find a Ramz. Editions application hosted
on the `Program Files/Ramz Editions` folder, or just in the `Program Files`
folder, in this case the parser will try to find a file named `ramz.diddi` to get sure
that it is a Ramz Editions project.

Taking `samplecode.diddi` as an example:

```
ramz_goto('DiddiCmd');         !# DiddiCmd
ramz_goto('Control de Agua');  !# DiddiOS 3
```

The instructions above will try to call DiddiCmd and DiddiOS, both projects of
Ramz Editions. If they don't exist on your computer, it will just print a
simple error message like:

```
...
FileNotFoundError: The Ramz Editions file you are looking for does not exists
```

## Open other kind of files

Use `openfile()` to open a known file on any direction on the disk. For example,
`samplecode.diddi` uses this function as follows:

```
!# Open a file

openfile('C:/Program Files/Ramz Editions/people.txt');
```

## Making a shell subprocess

It uses a Python `subprocess.run(...)`. Use it as follows:

```
!# Open a python "subprocess.Popen()"

subprocess_run('python -m turtledemo.minimal_hanoi');
```

## Some function code rules

DiddiScript functions has **strict rules**. There are 2 specific rules for
those functions:

1. You can only run one command at a time (__NOTE:__ don't use `;` on the Python
   code. I mean, __never__!).

2. In the case of `subprocess_run` and `pyrun`, never use single quotes (`' '`)
   on the code. Only use single quotes for `anyDiddiscriptFunction()` (do not
   use double quotes (`" "`) for that!).

Taking this rules, doing this:

```
!# some bad examples from "pyrun"

pyrun("print("hello")")                           !# Using "" for the pyrun() argument?
pyrun('print('who I am')')                        !# Using '' for the Python command?
pyrun('print("hello", end=" "); print("world!")') !# Giving 2 commands at a time?
```

is absolutely wrong!
