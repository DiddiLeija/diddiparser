"""
Parse DiddiScript files.
"""

__version__ = "1.0.0"
__author__ = "Diego Ramirez (dr01191115@gmail.com) @DiddiLeija on GitHub"
__platform__ = "win32"

# import the std libraries
import sys
import io
import warnings
import traceback
import os
import subprocess
import shlex
# test if the platform is correct before importing the other libraries
if not __platform__ == sys.platform:
    sys.exit(f"this system is built for {__platform__} systems")
# platform-depending std libraries here
# (some implementations may vary)
from os import startfile

# give some exceprions
class DiddiScriptError(SyntaxError):
    pass
class FilePrefixError(DiddiScriptError):
    pass
class PrefixWarning(UserWarning):
    pass

# add here the known functions
KNOWN_FUNCS = ["pyrun",
               "ramz_goto",
               "openfile",
               "subprocess_run"]

# build the complex parser from zero
class DiddiScriptFile:
    "open a DiddiScript file and give options to parse."

    def __init__(self,
                 pathname,
                 func=io.open,
                 adapt=False,
                 py_locals=None):
        "constructor, use a 'pathname' to open the file."
        if not pathname.endswith(".diddi") and not adapt:
            raise FilePrefixError(f"Pathname '{pathname}' does not refer to a DiddiScript file")
        elif adapt is True:
            warnngs.warn("You are attempting to open"
                         " another kind of file as a DiddiScript"
                         " file. The parser will try to adapt it.", PrefixWarning)
        if py_locals is None:
            py_locals = {"__name__": "__console__", "__doc__": None}
        self.py_locals = py_locals
        self.io_file = func(pathname, "r")
        self.file = None
        self.pathname = pathname
        self.extractcode()

    def extractcode(self):
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
                continue
            if "/*" in line:
                # start block comment, stop reading
                stop = True
                continue
            # replace the single-line comments
            cmd = line.split("!#")[0].rstrip()
            # enter the command
            if len(cmd.strip()) > 0:
                if not cmd.endswith(";"):
                    raise DiddiScriptError(f"Each command line must end with ';'")
                self.file.append(cmd[:len(cmd)- 1])
            del(cmd)

    def runfile(self):
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
                    except BaseException as e:
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
                        startfile(line)
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
                    # it is known but not implemented yet
                    print(str(NotImplemented)+"\n")

    def printCommands(self):
        "print all the commands from file."
        for cmd in self.file:
            print(cmd)

    def openRamz(self, path):
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

    def __del__(self):
        if isinstance(self.io_file, io.TextIOWrapper):
            self.io_file.close()

class DiddiScriptSetup(DiddiScriptFile):
    "class for setup DiddiScripts ('ramz.diddi')"
    productDir = None
    productName = None

    def __init__(self,
                 pathname,
                 func=io.open,
                 adapt=False,
                 py_locals=None):
        "Almost the same than the inherited __init__, but also tries to run the variable stuff..."
        DiddiScriptFile.__init__(self, pathname, func, adapt, py_locals)
        for line in self.file:
            if line.startswith("RamzProductName = "):
                self.productName = line[len("RamzProductName = "):len(line)-1].replace('"', '')
            elif line.startswith("RamzProductDir = "):
                self.productDir = line[len("RamzProductDir = "):len(line)-1].replace('"', '')
        if not self.isRamzEdProduct() or not pathname.endswith("ramz.diddi"):
            raise DiddiScriptError(f"This file is not a DiddiScript setup file ('ramz.diddi')")

    def isRamzEdProduct(self):
        "verify if the Diddi file is a real project setup file."
        return True if self.file is not None and self.productName is not None and self.productDir is not None else False


def demo():
    # make a demo.
    from colorama import init, Fore, Style
    import time
    init(autoreset=True)
    dsf = DiddiScriptFile("C:/Program Files/Ramz Editions/user/samplecode.diddi")
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

def main():
    # generate an argument parser for running DiddiScript files
    import argparse
    parser = argparse.ArgumentParser(prog=__name__,
                                     description="Parse DiddiScript script files "
                                                 "and DiddiScript setup files with "
                                                 "a simple interface.")
    parser.add_argument("-v", "--version", action="version", version=__version__)
    parser.add_argument("file", nargs="?", metavar="FILE")
    parser.add_argument("-s",
                        "--is-setup",
                        default=False,
                        action="store_true",
                        dest="is_setup",
                        help="Define if the DiddiScript is a "
                             "Ramz Ed. setup file.")
    parser.add_argument("-d",
                        "--demo",
                        action="store_true",
                        default=False,
                        dest="demo",
                        help="run the DiddiParser demo.")
    parser.usage = parser.format_usage()[len("usage: ") :] + __doc__
    opts = parser.parse_args()

    # verify the args
    if opts.demo is True and opts.is_setup is True:
        parser.error("--demo and --is-setup cannot be both true")
    if not opts.file and opts.demo is False:
        parser.error("you must specify 'file' or --demo")
    if opts.file and opts.demo is True:
        parser.error("you can't specify both 'file' and --demo")
    # start to loop
    if opts.demo is True:
        demo()
        return None
    elif not os.path.exists(opts.file):
        parser.error("seems like the DiddiScript filename does not exists")
    if opt.is_setup is True:
        ds = DiddiScriptSetup(opts.file)
        print("Product Name:", ds.productName)
        print("Product location:", ds.productDir)
    else:
        ds = DiddiScriptFile(opts.file)
        ds.runfile()

if __name__ == '__main__':
    main()
