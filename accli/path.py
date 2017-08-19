# -*-  coding:utf-8 -*-

import os
import yaml
import codecs

from distutils.spawn import find_executable  # NOQA

from accli.core import YAMLLoader


def get_all_yaml_files(root_dir):
    return [
        os.path.join(root_dir, f) for f in os.listdir(root_dir)
        if f.endswith('.yaml')
    ]


def load_yaml(filename):
    return yaml.load(codecs.open(filename, 'r', 'utf8'), YAMLLoader)
