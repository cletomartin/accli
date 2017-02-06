# -*-  coding:utf-8 -*-

import os
from os.path import join
import yaml
import codecs

from exc import TemplateNotFoundError


def get_all_yaml_files(root_dir):
    return [
        join(root_dir, f) for f in os.listdir(root_dir) if f.endswith('.yaml')
    ]


def get_template_full_path(templates_dir, template_name):
    template_path = join(templates_dir, template_name)

    if not os.isdir(template_path):
        raise TemplateNotFoundError()

    for path, list_dirs, list_files in os.walk(template_path):
        for filename in list_files:
            if filename.startswith('template.'):
                return join(path, filename)

    raise TemplateNotFoundError


def load_yaml(filename):
    try:
        return yaml.load(codecs.open(filename, 'r', 'utf8'), YAMLLoader)
    except Exception as exc:
        print('[Error]: {0}'.format(exc))
        sys.exit(1)
