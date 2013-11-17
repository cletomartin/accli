#!/usr/bin/python
# -*-  coding:utf-8 -*-

# (C) 2013, Loopzero Ltd.
# Code licensed under GPLv3

import argparse
import sys
import os
import jinja2
import datetime
import codecs
import yaml
import tempfile

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import bmcm.config as config
from bmcm.core import YAMLLoader
from bmcm.model import Invoice, Company


def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'template_name',
        help="Name of the template to use. Use <name> of '<template-dir>/<name>")
    parser.add_argument(
        'invoice_paths', nargs='+', default=[], help="Paths to input invoice")
    parser.add_argument(
        '-d', '--data-dir', dest='data_dir', default=config.BMCM_DATA_ROOTDIR,
        help="set the path to bmcm data root directory")
    parser.add_argument(
        '-t', '--template-dir', dest='template_dir',
        default='templates/mkinvoice',
        help="set the path to template root directory. Default 'templates/mkinvoice'")
    parser.add_argument(
        '-f', '--format', dest='format', default='tex', choices=['tex'],
        help="defines template format. Default 'tex'")
    parser.add_argument(
        '-r', '--list-renders', dest='list_renders', action='store_true',
        help="shows available renders.")

    # TBD
    # parser.add_argument(
    #     '-l', '--list-templates', dest='list_templates', action="store_true",
    #     help="List available templates")
    return parser


class TemplateRender(object):
    def __init__(self, tmpl_root_path):
        self._tmpl_root_path  = tmpl_root_path

    def generate(self, input_file):
        raise NotImplemented

    def support(self, ext):
        return ext in self.extensions


class TexTemplateRender(TemplateRender):
    name = 'TexRender'
    description = 'Render from TeX template to PDF'
    extensions = ['tex']

    def __init__(self, tmpl_root_path):
        super(TexTemplateRender, self).__init__(tmpl_root_path)
        self._jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader('.'),
            block_start_string = '<%',
            block_end_string = '%>',
            variable_start_string = '<<',
            variable_end_string = '>>',
            comment_start_string = '<#',
            comment_end_string = '#>')

    def generate(self, invoice, company, output_filename):
        template_fullpath = os.path.join(self._tmpl_root_path, 'tex')
        template_file = os.path.join(template_fullpath, 'template.tex')
        template = self._jinja_env.get_template(template_file)

        output = template.render(invoice=invoice, company=company)

        tmp_dir = tempfile.mkdtemp()
        tmp_filename = os.path.join(tmp_dir, 'output.tex')
        template_tree = os.walk(template_fullpath)

        try:
            for root, _, files in template_tree:
                for f in files:
                    os.system('ln -sf %s %s' % (
                        os.path.join(os.path.abspath(root), f),
                        os.path.join(tmp_dir, f)))
            file(tmp_filename, 'w').write(output.encode('utf-8'))
            os.system('cd %s; pdflatex output.tex' % tmp_dir)
            os.system('cd %s; mv output.pdf %s' % (tmp_dir, output_filename))
        finally:
            #os.system('rm -rf %s' % tmp_dir)
            pass

RENDERS = [
    TexTemplateRender
]


def get_renders_by_extension(ext):
    return [x for x in RENDERS if ext in x.extensions]


def load_yaml(filename):
    try:
        return yaml.load(codecs.open(filename, "r", "utf8"), YAMLLoader)
    except Exception as exc:
        print "[Error]: {0}".format(exc.message)
        sys.exit(1)


def show_renders():
    if not RENDERS:
        print 'No renders available!'
        return

    for r in RENDERS:
        print '%s: %s' % (r.name, r.description)


if __name__ == '__main__':
    parser = create_arg_parser()
    args, opts = parser.parse_known_args()

    if args.list_renders:
        show_renders()
        sys.exit(0)

    template_path = os.path.join(args.template_dir, args.template_name)
    if not os.path.isdir(template_path):
        print "[Error]: Template not found: '{0}'".format(template_path)
        sys.exit(1)

    for filename in args.invoice_paths:
        if not os.path.isfile(filename):
            print "[Error]: Invalid invoice file: '{0}'".format(filename)
            sys.exit(1)

    render = get_renders_by_extension(args.format)
    if not render:
        print "[Error]: not render found for: '{0}'".format(args.format)
        sys.exit(1)
    elif len(render) > 1:
        print "[Error]: too many renders: '{0}'".format(args.format)
        sys.exit(1)

    render = render[0](template_path)
    config.BMCM_DATA_ROOTDIR = args.data_dir

    for filename in args.invoice_paths:
        invoice = Invoice(load_yaml(filename))
        company = Company(load_yaml(os.path.join(args.data_dir, 'company.yaml')))
        invoice.set_default('number', 'XXXXXXXXX')
        output_filename = os.path.splitext(os.path.basename(filename))[0] + '.pdf'
        output_filename = os.path.join(os.path.abspath('.'), output_filename)
        render.generate(invoice, company, output_filename)

sys.exit(0)
