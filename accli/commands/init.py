# -*- coding:utf-8; mode python -*-

from accli.core import Command


class InitCmd(Command):

    def __init__(self, subparsers):
        super().__init__('init', subparsers)

    def run(self, args):
        return 0
