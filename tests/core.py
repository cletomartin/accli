# -*-  coding:utf-8 -*-

import yaml
from cStringIO import StringIO

from nose.tools import assert_equal, assert_raises

import bmcm.config
from bmcm.core import YAMLLoader

bmcm.config.BMCM_DATA_ROOTDIR = 'tests/data'


class TestYAMLLoader:
    def test_normal_usage(self):
        filename = 'tests/data/example.yaml'
        with open(filename, 'r') as f:
            standard = yaml.load(f)
        with open(filename, 'r') as f:
            own = yaml.load(f, Loader=YAMLLoader)
        assert_equal(standard, own)

    def test_include(self):
        test_file = open('tests/data/include.yaml', 'r')
        included_file = open('tests/data/example.yaml', 'r')
        included = yaml.load(included_file, Loader=YAMLLoader)
        values = yaml.load(test_file, Loader=YAMLLoader)
        assert_equal(values['c'], included)

    def test_trivial_inclusion_loop_detection(self):
        test_content = open('tests/data/include_loop.yaml', 'r')
        assert_raises(
            yaml.YAMLError,
            yaml.load, test_content, Loader=YAMLLoader)
