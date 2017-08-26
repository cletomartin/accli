# -*-  coding:utf-8 -*-

# Path root data

import os

from configparser import RawConfigParser


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
            'accli-repo-git-url': None,
            'accli-repo-path': os.path.expanduser('~/accli-repo')
        },
        default_section='general',
        allow_no_value=True
    )
    cfg_path = config_path or get_config_path()
    if not os.path.isfile(cfg_path):
        return __CONFIG
    __CONFIG.read(cfg_path)
    return __CONFIG


def get_accli_repo_path():
    config = get_config()
    return config.get('general', 'accli-repo-path')
