# -*-  coding:utf-8 -*-

from nose.tools import assert_equal, raises
from accli.model import Invoice, Customer, LoadingError


class TestCustomer:
    @raises(LoadingError)
    def test_invalid_creation(self):
        Customer({})

    def test_creation(self):
        data = {'address': {}}
        inv = Customer(data)
        assert_equal(inv.address, {})


class TestInvoice:
    @raises(LoadingError)
    def test_invalid_creation(self):
        Invoice({})
