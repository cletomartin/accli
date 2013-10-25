# -*-  coding:utf-8 -*-

import yaml
from cStringIO import StringIO

from nose.tools import assert_equal

from bmcm.core import YAMLLoader


class TestYAMLLoader:
    def test_normal_usage(self):
        data = StringIO('example: 1')
        assert_equal({'example': 1}, yaml.load(data, Loader=YAMLLoader))
