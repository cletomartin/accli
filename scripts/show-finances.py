#!/usr/bin/env python3
# -*-  coding:utf-8 -*-

import sys
import argparse
import datetime

from accli import config
from accli.model import Journal, MyCompany, Invoice, TransferEntry


def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--from', dest='from_', nargs='?',
        help='show results from DATE. Format expected: YYYY-MM-DD')
    parser.add_argument(
        '--to', nargs='?',
        help='show results until DATE. Format expected: YYYY-MM-DD')
    parser.add_argument(
        '-d', '--data-dir', dest='data_dir', default=config.ACCLI_DATA_ROOTDIR,
        help='set the path to accli data root directory')
    return parser


def create_entries_filters(options):
    retval = []

    if options.from_ is not None:
        try:
            from_date = datetime.datetime.strptime(options.from_, '%Y-%m-%d')
            from_date = from_date.date()
            retval.append(lambda x: x.date >= from_date)
        except ValueError:
            print('Invalid value for --from option. Expected %Y-%m-%d')
            sys.exit(0)

    if options.to is not None:
        try:
            to_date = datetime.datetime.strptime(options.to, '%Y-%m-%d')
            to_date = to_date.date()
            retval.append(lambda x: x.date <= to_date)
        except ValueError:
            print('Invalid value for --to option. Expected %Y-%m-%d')
            sys.exit(0)

    return retval


if __name__ == '__main__':
    parser = create_arg_parser()
    opts, args = parser.parse_known_args()
    config.ACCLI_DATA_ROOTDIR = opts.data_dir

    mycompany = MyCompany.create_from_file('init.yaml')
    bank_accounts = [b['id'] for b in mycompany.bank_accounts]

    journals = Journal.collect_all()
    invoices = Invoice.collect_all()
    entries = [e for j in journals for e in j.entries]
    entries.extend(invoices)
    entries = sorted(entries, key=lambda e: e.date)

    balances = {}
    for b in bank_accounts:
        balances[b] = 0.0

    filters = create_entries_filters(opts)
    for f in filters:
        entries = filter(f, entries)

    for e in entries:
        if isinstance(e, Invoice):
            balances['main'] += e.total_paid
            print('invoice,{0.total_paid},invoice #{0.number},{0.date}'.format(
                e))
            continue
        elif isinstance(e, TransferEntry):
            balances[e.orig] -= e.amount
            balances[e.account] += e.amount
        else:
            balances[e.account] += e.amount
            print('{0.category},{0.amount},{0.description},{0.date}'.format(
                e))

sys.exit(0)
