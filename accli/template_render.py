# -*-  coding:utf-8 -*-

import os
import tempfile

import jinja2

from accli.exc import MultipleTemplatesError


class TemplateRender(object):
    def __init__(self, tmpl_path, selector=None):
        '''
        TemplateRender constructor, that initializes the render environment to
        be ready for rendering a template on demand.

        The constructor allows two arguments> tmpl_path and selector.

        * tmpl_path: A path to the template. This argument is mandatory
        * selector: Only use it when the template you want to use has more
                    than one render possibilities.        
        '''

        self._tmpl_root_path = tmpl_path
        self._selector = selector
        self._jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self._tmpl__root_path),
            block_start_string='<%',
            block_end_string='%>',
            variable_start_string='<<',
            variable_end_string='>>',
            comment_start_string='<#',
            comment_end_string='#>')

    def render(self, invoice, company):
        if self._selector is None:
            dirs = [dir_entry for dir_entry in os.listdir(self._tmpl_root_path)
                    if os.path.isdir(dir_entry)]

            if len(dirs) != 1:
                raise MultipleTemplatesError(
                    'The template has several formats. Please, use a selector')

            self._selector = dirs[0]

        template_fullpath = os.path.join(self._tmpl_root_path,
                                         self._selector)

        template_file = os.path.join(
            self._selector, 'template.{}'.format(self._selector))
        template = self._jinja_env.get_template(template_file)

        output = template.render(invoice=invoice, company=company)

        tmp_dir = tempfile.mkdtemp()
        tmp_filename = os.path.join(
            tmp_dir, 'output.{}'.format(self._selector))
        template_tree = os.walk(template_fullpath)

        try:
            for root, _, files in template_tree:
                for f in files:
                    os.system('ln -sf %s %s' % (
                        os.path.join(os.path.abspath(root), f),
                        os.path.join(tmp_dir, f)))
            open(tmp_filename, mode='w', encoding='utf-8').write(output)

        finally:
            pass
