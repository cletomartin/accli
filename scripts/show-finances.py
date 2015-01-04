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
from accli.model import Journal, MyCompany, Invoice, TransferEntry


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
    bank_accounts = [b['id'] for b in mycompany.bank_accounts]

    journals = Journal.create_all()
    invoices = Invoice.create_all()
    entries = [e for j in journals for e in j.entries]
    entries.extend(invoices)
    entries = sorted(entries, key=lambda e: e.date)

    balances = {}
    for b in bank_accounts:
        balances[b] = 0.0

    for e in entries:
        if isinstance(e, Invoice):
            balances['main'] += e.total_paid
        elif isinstance(e, TransferEntry):
            balances[e.orig] -= e.amount
            balances[e.account] += e.amount
        else:
            balances[e.account] += e.amount

        print(balances, e.date)

sys.exit(0)
