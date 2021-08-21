"Run code from other languages."

import traceback
import sys
import warnings
from typing import Dict

__all__ = ["pyrun"]


def pyrun(line: str, py_locals: Dict[str, str]) -> None:
    "equivalent of the DiddiScript `pyrun()`"
    try:
        line = line.lstrip().replace(");", "").replace("'", "")
        exec(line[len("pyrun "):len(line)-1], py_locals)
    except Warning as w:
        warnings.warn(str(w), type(w))
    except Exception:
        exc_type, value, tb = sys.exc_info()
        sys.last_type = type
        sys.last_value = value
        sys.last_traceback = tb
        traceback.print_exception(exc_type, value, sys.last_traceback)
        print()
    return None
