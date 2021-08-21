"Standard lib for DiddiScript."

from diddiparser.lib import lang_runners
from diddiparser.lib import diddi_stdfuncs

from diddiparser.lib.lang_runners import __all__ as lang_runners_all
from diddiparser.lib.diddi_stdfuncs import __all__ as diddi_stdfuncs_all

__all__ = lang_runners_all + diddi_stdfuncs_all

# add here the known functions
STD_FUNCS = tuple(__all__)

KNOWN_FUNCS = {"pyrun": lang_runners.pyrun,
               "ramz_goto": diddi_stdfuncs.ramz_goto,
               "openfile": diddi_stdfuncs.openfile,
               "subprocess_run": diddi_stdfuncs.subprocess_run}

__all__.append("KNOWN_FUNCS")
