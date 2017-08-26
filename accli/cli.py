#!/usr/bin/env python3
# -*- coding:utf-8; mode python -*-

import os
import argparse

from accli.commands import InitCmd, InvoiceCmd
from accli.config import get_config_path, get_config

COMMANDS = [
    InitCmd,
    InvoiceCmd
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-c', '--cfg-path', default=get_config_path(),
        help='path to accli config file (Default: %(default)s)'
    )
    subparsers = parser.add_subparsers()
    for c in COMMANDS:
        c(subparsers)
    args = parser.parse_args()
    if 'func' not in args:
        parser.print_help()
        return 1

    needs_init = (
        not os.path.exists(args.cfg_path) and
        InitCmd != args.func.__self__.__class__
    )
    if needs_init:
        print("ERROR - config file does not exists. Run 'accli init'.")
        return 1

    # this will initialize the global config object
    get_config(args.cfg_path)
    return args.func(args)


if __name__ == "__main__":
    exit(main())
