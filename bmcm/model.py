# -*-  coding:utf-8 -*-

# (C) 2013, 2014 - Loopzero Ltd.
# Code licensed under GPLv3.


class CreationError(Exception):
    pass


class ModelObject(object):
    def __init__(self, kwargs, mandatory=set()):
        assert isinstance(kwargs, dict)

        missed = mandatory - set(kwargs.keys())
        if missed:
            raise CreationError(
                'Missed mandatory attributes: %s' % repr(list(missed)))
        self.__dict__.update(kwargs)

    def set_default(self, name, value):
        if not hasattr(self, name):
            setattr(self, name, value)


class Company(ModelObject):
    def __init__(self, kwargs):
        super(Company, self).__init__(kwargs)


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


class JournalEntry(object):
    mandatory = set(['account', 'date', 'category', 'ammount'])
    entry_by_category = dict()

    def __init__(self):
        raise NotImplementError('This class should not be instantiated')

    @classmethod
    def create_from_category(kwargs):
        category = kwargs.get('category', None)
        subcategory = None

        if category is None:
            raise CreationError(
                "'category' field required for building a JournalEntry")

        if '/' in category:
            category, subcategory = e.category.split('/')

        if category not in entry_by_category.keys():
            raise CreationError(
                'Unknown JournalEntry category: %s' % repr(category))

        return self.entry_by_category.get(category)(kwargs)


class ExpenseEntry(ModelObject):
    mandatory = JournalEntry.mandatory
    JournalEntry.entry_by_category.set('expense', __class__)

    def __init__(self):
        super(ExpenseEntry, self).__init__(kwargs)


class Journal(ModelObject):
    mandatory = set(['year', 'begin_date', 'end_date', 'accounts'])

    entry_by_category = {
        'expense': ExpenseEntry,
        'transfer': TransferEntry,
        'payment': PaymentEntry
    }

    def __init__(self, kwargs):
        super(Journal, self).__init__(kwargs)
        self.set_default('description', 'Journal - Tax year %d' % self.year)
        self.set_default('entries', list())

        self.entries = self._create_entries()

    def _create_entries(self):
        retval = []
        for e in self.entries:

        return retval
