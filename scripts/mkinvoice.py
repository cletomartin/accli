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



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('invoice_path', help="Path to invoice")
    parser.add_argument(
        '-t', '--template_dir', dest='template_dir', default='templates/loop0',
        help="Path to template directory. Default 'templates'")

    args = parser.parse_args()

    filename = args.invoice_path
    map_values = yaml.load(codecs.open(filename, "r", "utf8"))
    invoice = Invoice(map_values)

    invoice.set_default('number', 'INVALID!!!!')

    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader('.'),
        block_start_string = '<%',
        block_end_string = '%>',
        variable_start_string = '<<',
        variable_end_string = '>>',
        comment_start_string = '<#',
        comment_end_string = '#>')

    template = jinja_env.get_template(
        os.path.join(args.template_dir, 'template.tex'))
    make = jinja_env.get_template(
        os.path.join(args.template_dir, 'Makefile.template'))

    output = template.render(invoice=invoice)
    tmp_filename = '%s.tex' % invoice.number_as_str
    tmp_path = os.path.join(args.template_dir, tmp_filename)
    file(tmp_path, 'w').write(output.encode('utf-8'))
    os.system('cd %s; pdflatex %s' % (args.template_dir, tmp_filename))
    os.system('mv %s/%s.pdf .' % (args.template_dir, invoice.number_as_str))

    for ext in ['tex', 'out', 'aux', 'log']:
        os.system('rm %s/%s.%s' % (args.template_dir, invoice.number_as_str, ext))
