# -*-  coding:utf-8 -*-

# (C) 2013, Loopzero Ltd.
# Code licensed under GPLv3


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
