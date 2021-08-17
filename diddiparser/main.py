# Add a docstring as we mentioned on PR #15.
"""
Parse DiddiScript files and DiddiScript Setup files.

For the console script, use one of this option
combinations:

diddiparser [file]
diddiparser [file] --is_setup
diddiparser --demo
"""

# Add the console scripts here, as suggested on issue #1.

from diddiparser import __version__
from diddiparser.parser import (DiddiScriptFile,
                                DiddiScriptSetup,
                                demo)
import os
import argparse


def get_parser() -> argparse.ArgumentParser:
    # generate an argument parser for running DiddiScript files
    parser = argparse.ArgumentParser(prog=__name__,
                                     description="Parse DiddiScript script files "
                                                 "and DiddiScript setup files with "
                                                 "a simple command-line interface.")
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
                        help="Run the DiddiParser demo.")
    parser.add_argument("--use-extensions",
                        action="store_true",
                        default=False,
                        dest="extensions",
                        help="Make DiddiParser to find an extensions file on the current directory")
    parser.usage = parser.format_usage()[len("usage: "):] + __doc__
    return parser


def verify_args(parser, opts) -> None:
    # verify the args
    if opts.demo is True and opts.is_setup is True:
        parser.error("--demo and --is-setup cannot be both true")
    if not opts.file and opts.demo is False:
        parser.error("you must specify 'file' or --demo")
    if opts.file and opts.demo is True:
        parser.error("you can't specify both 'file' and --demo")
    if opts.extensions is True and opts.demo is True:
        parser.error("Could not run extensions on demo")


def parse_args(parser: argparse.ArgumentParser) -> None:
    opts = parser.parse_args()
    verify_args(parser, opts)
    # start to loop
    if opts.extensions is True:
        # run extensions to modify the functions
        if not os.path.exists("diddi_extensions.py"):
            parser.error("Extensions file ('diddi_extensions.py') not found")
        import runpy
        try:
            runpy.run_path("diddi_extensions.py")  # some modifications must be implemented here?
        except Exception as exc:
            parser.error("Could not run extensions due to %s: %r" % (type(exc).__name__, str(exc)))
    if opts.demo is True:
        demo()
        return None
    elif not os.path.exists(opts.file):
        parser.error("seems like the DiddiScript filename does not exists")
    if opts.is_setup is True:
        ds = DiddiScriptSetup(opts.file)
        print("Product Name:", ds.productName)
        print("Product location:", ds.productDir)
    else:
        ds = DiddiScriptFile(opts.file)
        ds.runfile()


def main() -> None:
    parser = get_parser()
    parse_args(parser)


if __name__ == '__main__':
    main()
