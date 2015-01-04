# -*-  coding:utf-8 -*-

from nose.tools import assert_true, assert_equal
from accli.model import Invoice, Customer, LoadingError


class TestCustomer:
    def test_creation(self):
        try:
            inv = Customer({})
            assert False, "This cannot be happened"
        except CreationError as exc:
            assert_true('address' in exc.message)

    def test_creation(self):
        data = {'address': {}}
        inv = Customer(data)
        assert_equal(inv.address, {})


class TestInvoice:
    def test_creation_fail(self):
        try:
            inv = Invoice({})
            assert False, "This cannot be happened"
        except LoadingError as exc:
            assert_true('customer' in str(exc))
            assert_true('items' in str(exc))
