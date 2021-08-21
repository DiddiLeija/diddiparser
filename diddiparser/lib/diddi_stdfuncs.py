"""Standard functions for DiddiScript."""

import os
import sys
import traceback
import subprocess
import shlex
from typing import Optional

# this only works under Windows systems,
# see https://github.com/DiddiLeija/diddiparser/issues/6
from os import startfile

__all__ = ["ramz_goto", "openfile", "subprocess_run"]


def ramz_goto(line: str) -> Optional[str]:
    "equivalent of `ramz_goto()`"
    line = line.lstrip().replace(");", "").replace("'", "")
    path = line[len("ramz_goto("):len(line)-1]
    expected = "c:/program files/ramz editions/%s/build/exe.win32-3.8/%s.exe"
    expected = expected % (path.lower(), path.lower())
    if os.path.exists(expected):
        # it is hosted on "C:/Program Files/Ramz Editions"
        startfile(expected)
    elif (os.path.exists(f"c:/program files/{path.lower()}/.ramz/ramz.diddi") and
          os.path.exists(f"c:/program files/{path.lower()}/build/exe.win32-3.8/{path.lower()}.exe")):
        return "USE_SETUP"
    else:
        # build a safe exception
        try:
            raise FileNotFoundError(f"Ramz Ed. app '{path}' does not exists or it is not a Ramz Ed. product")
        except Exception:
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
        startfile(line)  # try not to move this func
        print(f"Done opening {line}")
    except Exception:
        exc_type, value, tb = sys.exc_info()
        sys.last_type = type
        sys.last_value = value
        sys.last_traceback = tb
        traceback.print_exception(exc_type, value, sys.last_traceback)
        print()


def subprocess_run(line: str) -> None:
    line = line.lstrip().replace(");", "").replace("'", "")
    line = line[len("subprocess_run "):len(line)-1]
    print(f"Running '{line}'...")
    subprocess.run(shlex.split(line), shell=True)
    print()
