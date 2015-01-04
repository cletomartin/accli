#!/usr/bin/python3
# -*-  coding:utf-8 -*-

# (C) 2014 Loopzero Ltd.
# Code licensed under GPLv3

import os
import sys
import argparse

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from accli import config
from accli.core import YAMLLoader
from accli.model import Journal, MyCompany


def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--data-dir', dest='data_dir', default=config.ACCLI_DATA_ROOTDIR,
        help="set the path to accli data root directory")
    return parser


if __name__ == '__main__':
    parser = create_arg_parser()
    args, opts = parser.parse_known_args()
    config.ACCLI_DATA_ROOTDIR = args.data_dir

    mycompany = MyCompany.create_from_file('init.yaml')
    bank_accounts = mycompany.bank_accounts

    journal = Journal.create_from_file('2013.yaml')
    print(journal)

sys.exit(0)
