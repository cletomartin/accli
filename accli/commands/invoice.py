# -*- coding:utf-8; mode python -*-

from accli.core import Command


class ListCmd(Command):
    def __init__(self, subparsers):
        super().__init__('list', subparsers)
        self.parser.add_argument(
            '-f', '--format', choices=['json', 'plain'], default='plain',
            help='output format'
        )

    def run(self, args):
        print(args)
        return 0


class ShowCmd(Command):
    def __init__(self, subparsers):
        super().__init__('show', subparsers)
        self.parser.add_argument(
            '-f', '--format', choices=['json', 'plain'], default='plain',
            help='output format'
        )
        self.parser.add_argument(
            'invoice', help='invoice to show'
        )

    def run(self, args):
        print(args)
        return 0


class InvoiceCmd(Command):

    commands = [ListCmd, ShowCmd]

    def __init__(self, subparsers):
        super().__init__('invoice', subparsers)
        new_subparsers = self.parser.add_subparsers()
        for c in self.commands:
            c(new_subparsers)
