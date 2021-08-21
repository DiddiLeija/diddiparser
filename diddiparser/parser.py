"The main parsing tools."

# use an __all__ sequence to control the "import *"
__all__ = ["stringToScript",
           "DiddiScriptError",
           "FileSuffixError",
           "SuffixWarning",
           "stringToScript",
           "KNOWN_FUNCS",
           "DiddiScriptFile",
           "DiddiScriptSetup",
           "demo"]

# import the std libraries
import sys
import io
import warnings
from typing import Optional, Callable, Dict

# test if the platform is correct before importing the other libraries
if sys.platform != "win32":
    # http://github.com/diddiparser/issues/6
    sys.exit("This package only accepts win32 platforms")
from os import startfile

from diddiparser.lib import KNOWN_FUNCS, STD_FUNCS


# give some exceptions
class DiddiScriptError(SyntaxError):
    pass


class FileSuffixError(DiddiScriptError):
    pass


class SuffixWarning(UserWarning):
    pass


# convert from string to a good stream, maybe used when using string scripts instead of pathnames
def stringToScript(diddi_str: str) -> list:
    return diddi_str.splitlines()


# enable definitions for your code
def define_func(name: str, func: Callable) -> None:
    "define functions for a period"
    if name in STD_FUNCS:
        raise SyntaxError(f"You can't rewrite std function: '{name}'")
    KNOWN_FUNCS[name] = func


# build the complex parser from zero
class DiddiScriptFile:
    "open a DiddiScript file and give options to parse."

    def __init__(
               self,
               pathname: str,
               func: Optional[Callable] = None,
               adapt: bool = False,
               py_locals: Optional[Dict[str, str]] = None
    ) -> None:
        "constructor, use a 'pathname' to open the file."
        if func is None or func == io.open:
            # you will need io.open, maybe a SuffixError must be raised
            if not pathname.endswith(".diddi") and not adapt:
                raise FileSuffixError(f"Pathname '{pathname}' does not refer to a DiddiScript file")
            elif adapt is True:
                warnings.warn("You are attempting to open "
                              "another kind of file as a DiddiScript "
                              "file. The parser will try to adapt it.", SuffixWarning)
            else:
                pass
            # use io.open for the file streaming
            self.io_file = io.open(pathname, "r")
        else:
            # only use the function and ignore anything else
            self.io_file = func(pathname)
        # set the Python __locals__ for the Python code
        if py_locals is None:
            py_locals = {"__name__": "__console__", "__doc__": None}
        self.py_locals = py_locals
        self.file = None
        self.pathname = pathname
        self.extractcode()

    def extractcode(self) -> None:
        "delete the comments."
        self.file = []
        stop = False
        for line in self.io_file:
            line = line.rstrip()
            # look for block comments
            if stop and "*/" not in line:
                # it's still being a block comment, keep going
                continue
            elif stop and "*/" in line:
                # block comment ends
                stop = False
                line = line[line.find("*/") + 2:].lstrip()  # try to extract something after the comment block
            if "/*" in line:
                # start block comment, stop reading
                stop = True
                if "*/" in line:
                    # it just covers one line, but it will be parsed as commonly
                    stop = False
                line = line[:line.find("/*")].lstrip()  # try to extract something before the comment block
            # replace the single-line comments
            cmd = line.split("!#")[0].rstrip()
            # enter the command
            if len(cmd.strip()) > 0:
                if not cmd.endswith(";"):
                    raise DiddiScriptError("Each command line must end with ';'")
                self.file.append(cmd[:len(cmd) - 1])
            del(cmd)

    def runfile(self) -> None:
        "'compile' the file defined on the __init__ and run."
        if self.file is None or len(self.file) == 0:
            raise DiddiScriptError("The command list is empty")
        for line in self.file:
            if line.lstrip().split("(")[0] in KNOWN_FUNCS:
                func = KNOWN_FUNCS[line.lstrip().split("(")[0]]
                if func == KNOWN_FUNCS["pyrun"]:
                    # patch "pyrun()" to include the Python locals
                    # on the code.
                    response = func(line.split("(")[1], self.py_locals)
                else:
                    response = func(line.split("(")[1])
                if response == "USE_SETUP" and line.lstrip().split("(")[0] == "ramz_goto":
                    # patch for the ramz.diddi usage.
                    path = line.lstrip().replace(");", "").replace("'", "")
                    path = path[len("ramz_goto("):len(line)-1]
                    DiddiScriptSetup.__init__(f"c:/program files/{path.lower()}/.ramz/ramz.diddi")
                    startfile(f"c:/program files/{path.lower()}/build/exe.win32-3.8/{path.lower()}.exe")
                    continue

    def printCommands(self) -> None:
        "print all the commands from file."
        for cmd in self.file:
            print(cmd)

    def __del__(self) -> None:
        if isinstance(self.io_file, io.TextIOWrapper):
            # if TextIOWrapper is used, close it with the known "close()"
            self.io_file.close()
        else:
            # any idea of how to close any other file stream?
            pass


class DiddiScriptSetup(DiddiScriptFile):
    "class for setup DiddiScripts ('ramz.diddi')"
    productDir = None
    productName = None

    def __init__(
               self,
               pathname: str,
               func: Optional[Callable] = None,
               adapt: bool = False,
               py_locals: Optional[Dict[str, str]] = None
    ) -> None:
        "Almost the same than the inherited __init__, but also tries to run the variable stuff..."
        DiddiScriptFile.__init__(self, pathname, func, adapt, py_locals)
        for line in self.file:
            if line.startswith("RamzProductName = "):
                self.productName = line[len("RamzProductName = "):len(line) - 1].replace('"', '')
            elif line.startswith("RamzProductDir = "):
                self.productDir = line[len("RamzProductDir = "):len(line) - 1].replace('"', '')
        if not self.isRamzEdProduct() or not pathname.endswith("ramz.diddi"):
            raise DiddiScriptError("This file is not a DiddiScript setup file ('ramz.diddi' is missing!)")

    def isRamzEdProduct(self) -> None:
        "verify if the Diddi file is a real project setup file."
        return True if self.file is not None and self.productName is not None and self.productDir is not None else False


def demo() -> None:
    # make a simple demo.
    # you need Colorama to run it with
    # a pretty colored output.

    # add a string, instead of calling the file with io.open()
    file_string = """
/*
   - Sample code

   These lines must be ignored by the interpreter. I will enter some
   dummy code. Ignore them by now.
*/

!# Run the easiest Python 3 code ever!

pyrun('print("Hello world!")');

!# Open a file

openfile('C:/Program Files/Ramz Editions/people.txt');

!# Open a python "subprocess.Popen()"

subprocess_run('python -m turtledemo.minimal_hanoi');"""
    # run the demo
    from colorama import init, Fore, Style
    import time
    init(autoreset=True)
    dsf = DiddiScriptFile(file_string, func=stringToScript)  # implement this func
    print("Running demo... please wait...")
    time.sleep(1)
    print(Fore.GREEN+Style.BRIGHT+"File opened succesfully!")
    print(Fore.BLUE+Style.BRIGHT+"=-"*30 + "=")
    print(Fore.GREEN+Style.BRIGHT+"EXTRACTED COMMANDS:\n")
    dsf.printCommands()
    print(Fore.BLUE+Style.BRIGHT+"=-"*30 + "=")
    print(Fore.GREEN+Style.BRIGHT+"OUTPUT:\n")
    dsf.runfile()
    print(Fore.BLUE+Style.BRIGHT+"=-"*30 + "=")
    print(Fore.GREEN+Style.BRIGHT+"DONE!")
