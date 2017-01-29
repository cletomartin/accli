#!/usr/bin/env python3
# -*- coding:utf-8; mode python -*-

import argparse

from accli.commands import InitCmd, InvoiceCmd

COMMANDS = [
    InitCmd,
    InvoiceCmd
]


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    for c in COMMANDS:
        c(subparsers)
    args = parser.parse_args()
    if 'func' not in args:
        parser.print_help()
        return 1
    return args.func(args)


if __name__ == "__main__":
    exit(main())
