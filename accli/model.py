# -*-  coding:utf-8 -*-

# (C) 2013, 2014 - Loopzero Ltd.
# Code licensed under GPLv3.

import os

from accli.core import YAMLLoader
from accli import config


class LoadingError(Exception):
    pass


class ModelObject(object):
    def __init__(self, kwargs, mandatory=set()):
        assert isinstance(kwargs, dict)

        missed = mandatory - set(kwargs.keys())
        if missed:
            raise LoadingError(
                'Missed mandatory attributes: %s' % repr(list(missed)))
        self.__dict__.update(kwargs)

    def set_default(self, name, value):
        if not hasattr(self, name):
            setattr(self, name, value)

    def __repr__(self):
        return '{self.__class__}: {self.__dict__}'.format(self=self)

    @classmethod
    def create_from_file(cls, filepath, loader=YAMLLoader):
        fullpath = os.path.join(
            config.ACCLI_DATA_ROOTDIR, cls.accli_directory, filepath)
        if not os.path.isfile(fullpath):
            raise LoadingError("Path '%s' does not exist" % fullpath)
        return cls(loader.load(fullpath))


class Company(ModelObject):
    accli_directory = 'companies'

    def __init__(self, kwargs):
        super(Company, self).__init__(kwargs)


class MyCompany(ModelObject):
    accli_directory = ''

    def __init__(self, kwargs):
        super(MyCompany, self).__init__(kwargs)


class Customer(ModelObject):
    mandatory = set(['address'])

    def __init__(self, kwargs):
        super(Customer, self).__init__(kwargs, Customer.mandatory)


class InvoiceItem(ModelObject):
    mandatory = set(['quantity', 'price'])

    def __init__(self, kwargs):
        super(InvoiceItem, self).__init__(kwargs)
        self.total = self.quantity * self.price


class Invoice(ModelObject):
    mandatory = set(['customer', 'items'])

    def __init__(self, kwargs):
        super(Invoice, self).__init__(kwargs, Invoice.mandatory)
        self.customer = Customer(self.customer)
        self.set_default('tax_rate', 0.)
        self.set_default('currency', 'GBP')

        self.items = [InvoiceItem(x) for x in self.items]
        self.subtotal = sum([x.total for x in self.items])
        self.total = self.subtotal + self.subtotal * self.tax_rate

    @property
    def number_as_str(self):
        return "%07d" % self.number


class BankAccount(ModelObject):
    mandatory = set(['id', 'country'])
    mandatory_fields_by_country = {
        'UK': ['sort_code', 'account_number'],
        'ES': ['account_number']
    }

    def __init__(self, kwargs):
        super(BankAccount, self).__init__(kwargs)
        for i in ['description', 'swift', 'iban']:
            self.set_default(i, '')

        self.set_default('currency', 'GBP')


class JournalEntry(ModelObject):
    mandatory = set(['account', 'date', 'category', 'ammount'])

    def __init__(self, kwargs):
        super(JournalEntry, self).__init__(kwargs)

    @classmethod
    def create_from_values(cls, kwargs):
        category = kwargs.get('category', None)
        subcategory = None

        if category is None:
            raise LoadingError(
                "'category' field required for building a JournalEntry")

        if '/' in category:
            category, subcategory = category.split('/')

        candidates = JournalEntry.__subclasses__()
        for c in candidates:
            if c.category == category:
                return c(kwargs)
        else:
            raise LoadingError(
                'Unknown JournalEntry category: %s' % repr(category))


class ExpenseEntry(JournalEntry):
    mandatory = JournalEntry.mandatory
    category = 'expense'

    def __init__(self, kwargs):
        super(ExpenseEntry, self).__init__(kwargs)


class TransferEntry(JournalEntry):
    mandatory = JournalEntry.mandatory
    category = 'transfer'

    def __init__(self, kwargs):
        super(TransferEntry, self).__init__(kwargs)


class PaymentEntry(JournalEntry):
    mandatory = JournalEntry.mandatory
    category = 'payment'

    def __init__(self, kwargs):
        super(PaymentEntry, self).__init__(kwargs)


class CapitalEntry(JournalEntry):
    mandatory = JournalEntry.mandatory
    category = 'capital'

    def __init__(self, kwargs):
        super(CapitalEntry, self).__init__(kwargs)


class Journal(ModelObject):
    mandatory = set(['year', 'begin_date', 'end_date', 'accounts'])
    accli_directory = 'journals'

    def __init__(self, kwargs):
        super(Journal, self).__init__(kwargs)
        self.set_default('description', 'Journal - Tax year %d' % self.year)
        self.set_default('entries', list())

        self.entries = self._create_entries()

    def _create_entries(self):
        retval = []
        for e in self.entries:
            retval.append(JournalEntry.create_from_values(e))
        return retval
