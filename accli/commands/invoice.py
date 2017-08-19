# -*- coding:utf-8; mode python -*-

import os
import tempfile

from subprocess import check_output

from accli import config
from accli.core import Command
from accli.model import Invoice, Company
from accli.path import load_yaml, find_executable
from accli.template import render_template, get_template_full_path


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
            help='Name of the template to use'
        )
        self.parser.add_argument(
            'invoice_paths', nargs='+', default=[],
            help='paths to input invoice'
        )
        self.parser.add_argument(
            '-d', '--data-dir', dest='data_dir',
            default=config.ACCLI_DATA_ROOTDIR,
            help='path to accli data root directory'
        )
        self.parser.add_argument(
            '-t', '--template-dir', dest='template_dir',
            help=("path to invoice template directory. "
                  "Default '<data-dir>/templates/invoice'")
        )
        self.parser.add_argument(
            '-o', '--output-dir', dest='output_dir', default=os.getcwd(),
            help='the output path for the generated files'
        )
        self.parser.add_argument(
            '-f', '--format', dest='format', default='tex', choices=['tex'],
            help="template format. Default 'tex'"
        )

    def run(self, args):
        deps = ['rubber', 'pdflatex']
        for d in deps:
            if find_executable(d) is None:
                print(
                    'ERROR - {} are needed to generate PDFs. '
                    'Please installed them'.format(deps)
                )
                return 1

        if args.template_dir is None:
            args.template_dir = os.path.join(
                args.data_dir, 'templates', 'invoice'
            )
        template_path = get_template_full_path(
            args.template_dir, args.template_name
        )

        for filename in args.invoice_paths:
            invoice = Invoice(load_yaml(filename))
            company = Company(
                load_yaml(os.path.join(args.data_dir, 'init.yaml'))
            )
            rendered_output = render_template(
                template_path, invoice=invoice, company=company
            )

            # TODO: we only support PDF conversion from Tex for the
            # time being. This should be changed by a more general
            # mechanism that allows different kind of inputs and
            # outputs.
            output_filename = (
                os.path.splitext(os.path.basename(filename))[0] + '.pdf'
            )
            with tempfile.NamedTemporaryFile() as f:
                f.file.write(rendered_output.encode())
                cmd = "cat {} | rubber-pipe -I {} -d > {}".format(
                    f.name, os.path.dirname(template_path), output_filename
                )
                check_output(cmd, shell=True)
            print('File {} generated'.format(output_filename))
        return 0


class InvoiceCmd(Command):

    commands = [ListCmd, ShowCmd, GenerateCmd]

    def __init__(self, subparsers):
        super().__init__('invoice', subparsers)
        new_subparsers = self.parser.add_subparsers()
        for c in self.commands:
            c(new_subparsers)
