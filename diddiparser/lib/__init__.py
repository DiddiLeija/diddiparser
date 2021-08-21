"Standard lib for DiddiScript."

from diddiparser.lib.lang_runners import *
from diddiparser.lib.diddi_stdfuncs import *

from diddiparser.lib.lang_runners import lang_runners_all
from diddiparser.lib.diddi_stdfuncs import diddi_stdfuncs_all

__all__ = lang_runners_all + diddi_stdfuncs_all

del(lang_runners_all, diddi_stdfuncs_all)
