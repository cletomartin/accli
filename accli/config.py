# -*-  coding:utf-8 -*-

# Path root data

import os

from configparser import RawConfigParser

ACCLI_DATA_ROOTDIR = os.getenv('ACCLI_DATA_ROOTDIR')
if ACCLI_DATA_ROOTDIR is None:
    ACCLI_DATA_ROOTDIR = 'data'


__CONFIG = None

def get_config_path():
    return (
        os.getenv('ACCLI_CONFIG_PATH') or
        os.path.join(os.path.expanduser('~/.accli'))
    )

def get_config(config_path=None):
    global __CONFIG
    if __CONFIG is not None:
        return __CONFIG

    __CONFIG = RawConfigParser(
        defaults={
            'accli_repo_git_url': None,
            'accli_repo_path': os.path.expanduser('~/accli-repo')
        },
        default_section='core',
        allow_no_value=True
    )
    if not os.path.isfile(get_config_path()):
        return __CONFIG
    __CONFIG.read(get_config_path())
    return __CONFIG
