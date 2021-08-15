"""Standard functions for DiddiScript."""

import sys
import traceback
import warnings
import subprocess
import shlex
from typing import Optional

# this only works under Windows systems,
# see https://github.com/DiddiLeija/diddiparser/issues/6
from os import startfile

def pyrun(line: str) -> None:
    "equivalent of the DiddiScript `pyrun()`"
    try:
        line = line.lstrip().replace(");", "").replace("'", "")
        exec(line[len("pyrun "):len(line)-1], self.py_locals)
    except Warning as e:
        warnings.warn(str(e), type(e))
    except Exception as e:
        type, value, tb = sys.exc_info()
        sys.last_type = type
        sys.last_value = value
        sys.last_traceback = tb
        traceback.print_exception(type, value, sys.last_traceback)
        print()
    return None

def ramz_goto(line: str) -> Optional[str]:
    "equivalent of `ramz_goto()`"
    line = line.lstrip().replace(");", "").replace("'", "")
    path = line[len("ramz_goto("):len(line)-1]
    if os.path.exists(f"c:/program files/ramz editions/{path.lower()}/build/exe.win32-3.8/{path.lower()}.exe"):
        # it is hosted on "C:/Program Files/Ramz Editions"
        startfile(f"c:/program files/ramz editions/{path.lower()}/build/exe.win32-3.8/{path.lower()}.exe")
    elif os.path.exists(f"c:/program files/{path.lower()}/.ramz/ramz.diddi") and os.path.exists(f"c:/program files/{path.lower()}/build/exe.win32-3.8/{path.lower()}.exe"):
        return "USE_SETUP"
    else:
        # build a safe exception
        try:
            raise FileNotFoundError(f"Ramz Ed. app '{path}' does not exists or it is not a Ramz Ed. product")
        except:
            exc_type, value, tb = sys.exc_info()
            sys.last_type = exc_type
            sys.last_value = value
            sys.last_traceback = tb
            traceback.print_exception(exc_type, value, sys.last_traceback)
            print()
    return None

def openfile(line: str) -> None:
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

def subprocess_run(line: str) -> None:
    elif line.lstrip().split("(")[0] == "subprocess_run":
        line = line.lstrip().replace(");", "").replace("'", "")
        line = line[len("subprocess_run "):len(line)-1]
        print(f"Running '{line}'...")
        subprocess.run(shlex.split(line), shell=True)
        print()
