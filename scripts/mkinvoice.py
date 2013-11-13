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
        help="Path to bmcm data root directory")
    parser.add_argument(
        '-t', '--template-dir', dest='template_dir',
        default='templates/mkinvoice',
        help="Path to template root directory. Default 'templates/mkinvoice'")
    parser.add_argument(
        '-f', '--format', dest='format', default='tex', choices=['tex'],
        help="Template format. Default 'tex'")

    # TBD
    # parser.add_argument(
    #     '-l', '--list-templates', dest='list_templates', action="store_true",
    #     help="List available templates")
    return parser

if __name__ == '__main__':
    parser = create_arg_parser()
    args, opts = parser.parse_known_args()

    template_path = os.path.join(args.template_dir, args.template_name)
    if not os.path.isdir(template_path):
        print "Error: Template not found: '{0}'".format(template_path)
        sys.exit(1)

    for filename in args.invoice_paths:
        if not os.path.isfile(filename):
            print "Error: Invalid invoice file: '{0}'".format(filename)
            sys.exit(1)

    config.BMCM_DATA_ROOTDIR = args.data_dir
    for filename in args.invoice_paths:
        invoice_values = yaml.load(codecs.open(filename, "r", "utf8"), YAMLLoader)
        company_values = yaml.load(
            codecs.open(os.path.join(args.data_dir,'company.yaml')), YAMLLoader)
        invoice = Invoice(invoice_values)
        company = Company(company_values)

        invoice.set_default('number', 'INVALID!!!!')

        # assuming tex format
        jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader('.'),
            block_start_string = '<%',
            block_end_string = '%>',
            variable_start_string = '<<',
            variable_end_string = '>>',
            comment_start_string = '<#',
            comment_end_string = '#>')

        # TBD: select template.* by format
        template_fullpath = os.path.join(template_path, args.format)
        template_file = os.path.join(template_fullpath, 'template.tex')
        template = jinja_env.get_template(template_file)

        output = template.render(invoice=invoice, company=company)
        tmp_basename = os.path.splitext(os.path.basename(filename))[0]
        tmp_texfile = '{0}.tex'.format(tmp_basename)
        tmp_path = os.path.join(template_fullpath, tmp_texfile)
        file(tmp_path, 'w').write(output.encode('utf-8'))
        os.system('cd %s; pdflatex %s' % (template_fullpath, tmp_texfile))
        os.system('mv %s/%s.pdf .' % (template_fullpath, tmp_basename))

        for ext in ['tex', 'out', 'aux', 'log']:
            os.system(
                'rm %s/%s.%s' % (template_fullpath, tmp_basename, ext))
