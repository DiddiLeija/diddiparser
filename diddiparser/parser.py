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
import traceback
import os
import subprocess
import shlex
from typing import Optional, Callable

# test if the platform is correct before importing the other libraries
if sys.platform != "win32":
    # http://github.com/diddiparser/issues/6
    sys.exit(f"this system is built for {__platform__} systems")
from os import startfile

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

# add here the known functions
KNOWN_FUNCS = ["pyrun",
               "ramz_goto",
               "openfile",
               "subprocess_run"]

# build the complex parser from zero
class DiddiScriptFile:
    "open a DiddiScript file and give options to parse."

    def __init__(self,
                 pathname: str,
                 func: Optional[Callable] = None,
                 adapt: bool = False,
                 py_locals: Optional[dict] = None) -> None:
        "constructor, use a 'pathname' to open the file."
        if func is None:
            # you will need io.open, maybe a SuffixError
            # must be raised
            if not pathname.endswith(".diddi") and not adapt:
                raise FileSuffixError(f"Pathname '{pathname}' does not refer to a DiddiScript file")
            elif adapt is True:
                warnngs.warn("You are attempting to open"
                             " another kind of file as a DiddiScript"
                             " file. The parser will try to adapt it.", SuffixWarning)
            # use io.open for the file streaming
            func = io.open
            self.io_file = func(pathname, "r")
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
            if stop and not "*/" in line:
                # it's still being a block comment, keep going
                continue
            elif stop and "*/" in line:
                # block comment ends
                stop = False
                line = line[line.find("*/") + 2:].lstrip() # try to extract something after the comment block
            if "/*" in line:
                # start block comment, stop reading
                stop = True
                if "*/" in line:
                    # it just covers one line, but it will be parsed as commonly
                    stop = False
                line = line[:line.find("/*")].lstrip() # try to extract something before the comment block
            # replace the single-line comments
            cmd = line.split("!#")[0].rstrip()
            # enter the command
            if len(cmd.strip()) > 0:
                if not cmd.endswith(";"):
                    raise DiddiScriptError(f"Each command line must end with ';'")
                self.file.append(cmd[:len(cmd)- 1])
            del(cmd)

    def runfile(self) -> None:
        "'compile' the file defined on the __init__ and run."
        if self.file is None or len(self.file) == 0:
            raise DiddiScriptError(f"The command list is empty")
        for line in self.file:
            if line.lstrip().split("(")[0] in KNOWN_FUNCS:
                if line.lstrip().split("(")[0] == "pyrun":
                    # python code is here
                    try:
                        line = line.lstrip().replace(");", "").replace("'", "")
                        exec(line[len("pyrun "):len(line)-1], self.py_locals)
                    except Exception as e:
                        type, value, tb = sys.exc_info()
                        sys.last_type = type
                        sys.last_value = value
                        sys.last_traceback = tb
                        traceback.print_exception(type, value, sys.last_traceback)
                    print()
                elif line.lstrip().split("(")[0] == "ramz_goto":
                    # go to a ramz ed. product
                    line = line.lstrip().replace(");", "").replace("'", "")
                    line = line[len("ramz_goto("):len(line)-1]
                    self.openRamz(line)
                elif line.lstrip().split("(")[0] == "openfile":
                    # start a file
                    line = line.lstrip().replace(");", "").replace("'", "")
                    line = line[len("openfile "):len(line)-1]
                    try:
                        startfile(line) # try not to move this func
                        print(f"Done opening {line}")
                    except Exception as e:
                        type, value, tb = sys.exc_info()
                        sys.last_type = type
                        sys.last_value = value
                        sys.last_traceback = tb
                        traceback.print_exception(type, value, sys.last_traceback)
                    print()
                elif line.lstrip().split("(")[0] == "subprocess_run":
                    line = line.lstrip().replace(");", "").replace("'", "")
                    line = line[len("subprocess_run "):len(line)-1]
                    print(f"Running '{line}'...")
                    subprocess.run(shlex.split(line), shell=True)
                    print()
                else:
                    # it is known - but not implemented yet
                    # (this can include unknown language implementation)
                    print("<Function not implemented: '%s'>"%line)

    def printCommands(self) -> None:
        "print all the commands from file."
        for cmd in self.file:
            print(cmd)

    def openRamz(self, path: str) -> None:
        "redirect to a Ramz Editions app."
        if os.path.exists(f"c:/program files/ramz editions/{path.lower()}/build/exe.win32-3.8/{path.lower()}.exe"):
            # it is hosted on "C:/Program Files/Ramz Editions"
            startfile(f"c:/program files/ramz editions/{path.lower()}/build/exe.win32-3.8/{path.lower()}.exe")
        elif os.path.exists(f"c:/program files/{path.lower()}/.ramz/ramz.diddi") and os.path.exists(f"c:/program files/{path.lower()}/build/exe.win32-3.8/{path.lower()}.exe"):
            # not hosted in the "Ramz Editions" folder, but its "ramz.diddi" reveals it is from Ramz Editions at all
            setup_file = DiddiScriptSetup(f"c:/program files/{path.lower()}/.ramz/ramz.diddi")
            startfile(f"c:/program files/{path.lower()}/build/exe.win32-3.8/{path.lower()}.exe")
        else:
            # build a safe exception
            try:
                raise FileNotFoundError(f"Ramz Ed. app '{path}' does not exists or it is not a Ramz Ed. product")
            except Exception as e:
                type, value, tb = sys.exc_info()
                sys.last_type = type
                sys.last_value = value
                sys.last_traceback = tb
                traceback.print_exception(type, value, sys.last_traceback)
                print()

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

    def __init__(self,
                 pathname: str,
                 func: Optional[Callable] = None,
                 adapt: bool = False,
                 py_locals: Optional[dict] = None):
        "Almost the same than the inherited __init__, but also tries to run the variable stuff..."
        DiddiScriptFile.__init__(self, pathname, func, adapt, py_locals)
        for line in self.file:
            if line.startswith("RamzProductName = "):
                self.productName = line[len("RamzProductName = "):len(line)-1].replace('"', '')
            elif line.startswith("RamzProductDir = "):
                self.productDir = line[len("RamzProductDir = "):len(line)-1].replace('"', '')
        if not self.isRamzEdProduct() or not pathname.endswith("ramz.diddi"):
            raise DiddiScriptError(f"This file is not a DiddiScript setup file ('ramz.diddi')")

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
    dsf = DiddiScriptFile(file_string, func=stringToScript) # implement this func
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


