# -*- coding:utf-8; mode python -*-

import os
import codecs

import yaml

from accli import config
from accli.core import Command
from accli.model import Invoice, Company
from accli.utils import get_template_full_path, load_yaml
from accli.template_render import TemplateRender


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


class GenerateCmd(Command):
    def __init__(self, subparsers):
        super().__init__('generate', subparsers)

        self.parser.add_argument(
            'template_name',
            help='Name of the template to use')
        self.parser.add_argument(
            'invoice_paths', nargs='+', default=[],
            help='Paths to input invoice')
        self.parser.add_argument(
            '-d', '--data-dir', dest='data_dir',
            default=config.ACCLI_DATA_ROOTDIR,
            help='set the path to accli data root directory')
        self.parser.add_argument(
            '-t', '--template-dir', dest='template_dir',
            default='templates/mkinvoice',
            help=("set the path to template root directory. "
                  "Default 'templates/mkinvoice'"))
        self.parser.add_argument(
            '-o', '--output-dir', dest='output_dir', default=os.getcwd(),
            help='set the output path for the generated files')
        self.parser.add_argument(
            '-f', '--format', dest='format', default='tex', choices=['tex'],
            help="defines template format. Default 'tex'")
        self.parser.add_argument(
            '-r', '--list-renders', dest='list_renders', action='store_true',
            help='shows available renders.')

    def run(self, args):
        template_path = get_template_full_path(
            args.template_dir, args.template_name)

        render = TemplateRender(template_path)

        for filename in args.invoice_paths:
            invoice = Invoice(yaml.load(codecs.open(filename, 'r', 'utf8')))
            company = Company(
                load_yaml(os.path.join(args.data_dir, 'init.yaml'))['me'])
            rendered_output = render.render(invoice, company)
            # FIXME: This doesn't match with the current interfaces, only an
            #        idea
            output = TexGenerator(rendered_output).generate()

        return 0


class InvoiceCmd(Command):

    commands = [ListCmd, ShowCmd, GenerateCmd]

    def __init__(self, subparsers):
        super().__init__('invoice', subparsers)
        new_subparsers = self.parser.add_subparsers()
        for c in self.commands:
            c(new_subparsers)
