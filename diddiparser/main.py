# Add a docstring as we mentioned on PR #15.
"""
Parse DiddiScript files and DiddiScript Setup files.

For the console script, use one of this options:

diddiparser [file]
diddiparser [file] --is_setup
diddiparser --demo
"""

# Add the console scripts here, as suggested on issue #1.

from diddiparser import __version__
from diddiparser.parser import (DiddiScriptFile, 
                                DiddiScriptSetup, 
                                demo)

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
