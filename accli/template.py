# -*- coding:utf-8; mode python -*-

import os
import jinja2

from accli.exc import TemplateNotFoundError


def render_template(tmpl_path, **kwargs):
    if tmpl_path.endswith('.tex'):
        jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(os.path.dirname(tmpl_path)),
            block_start_string='<%',
            block_end_string='%>',
            variable_start_string='<<',
            variable_end_string='>>',
            comment_start_string='<#',
            comment_end_string='#>'
        )
    else:
        jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(os.path.dirname(tmpl_path))
        )
    template = jinja_env.get_template(os.path.basename(tmpl_path))
    return template.render(**kwargs)


def get_template_full_path(templates_dir, template_name):
    template_path = os.path.join(templates_dir, template_name)

    if not os.path.isdir(template_path):
        raise TemplateNotFoundError()

    for path, list_dirs, list_files in os.walk(template_path):
        for filename in list_files:
            if filename.startswith('template.'):
                return os.path.join(path, filename)

    raise TemplateNotFoundError
