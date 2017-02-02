# -*-  coding:utf-8 -*-

import os
from os.path import join


def get_all_yaml_files(root_dir):
    return [
        join(root_dir, f) for f in os.listdir(root_dir) if f.endswith('.yaml')
    ]
