# -*- coding:utf-8; mode python -*-

import os
import shutil
import subprocess as sp

from accli.config import get_config, get_config_path
from accli.core import Command
from accli.path import find_executable


def yesno(question):
    while True:
        answer = input(question + ' <y/N>: ')
        if not answer:
            return 'n'
        if answer in ['y', 'n']:
            return answer


SKELETON_REPO = 'git@gitlab.com:cleto/accli-repo.git'


class InitCmd(Command):

    def __init__(self, subparsers):
        super().__init__('init', subparsers)

    def run(self, args):
        cfg_path = get_config_path()
        first_time = not os.path.isfile(cfg_path)

        cfg = get_config(cfg_path)
        basedir = os.path.dirname(cfg_path)
        if not os.path.exists(basedir):
            os.makedirs(basedir)

        if not first_time:
            answer = yesno(
                '{} already exists. '.format(cfg_path) + ' '
                'Do you want to override it?'
            )
            if answer == 'n':
                print('OK. Nothing done.')
                return 0

        fields = ['accli_repo_path', 'accli_repo_git_url']
        print('Please provide the following config values:')
        for f in fields:
            value = input('{} [{}]: '.format(f, cfg['core'][f])).strip()
            if value:
                cfg['core'][f] = value

        repo_path = cfg['core']['accli_repo_path']
        cfg['core']['accli_repo_path'] = os.path.expanduser(repo_path)
        repo_url = cfg['core']['accli_repo_git_url'] or SKELETON_REPO
        if not os.path.exists(repo_path):
            question = 'Looks like {} does not exists. '.format(repo_path)
            if not repo_url:
                question += (
                    'Do you want to initialise it with example content?'
                )
            else:
                question += (
                    'Do you want to clone {} into it?'.format(repo_url)
                )
            answer = yesno(question)
            if answer == 'y':
                if not find_executable('git'):
                    print('ERROR - git cannot be found')
                    return 1
                sp.check_output(['git', 'clone', repo_url, repo_path])
                shutil.rmtree(os.path.join(repo_path, '.git'))
        else:
            print('{} already exists. Nothing to do.'.format(repo_path))

        cfg.write(open(cfg_path, 'w'))
        return 0
