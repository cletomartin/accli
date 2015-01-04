# -*-  coding:utf-8 -*-

# (C) 2014 Loopzero Ltd.
# Code licensed under GPLv3

import os
from os.path import isfile, join


def get_all_yaml_files(root_dir):
    return [
        join(root_dir, f) for f in os.listdir(root_dir) if f.endswith('.yaml')
    ]
