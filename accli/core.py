# -*-  coding:utf-8 -*-

import os
import yaml
import codecs

from accli import config


class YAMLLoader(yaml.loader.Loader):
    def __init__(self, stream):
        super().__init__(stream)
        self.root_dir = config.ACCLI_DATA_ROOTDIR
        self._filename = stream.name

    def include(self, node):
        filename = os.path.join(self.root_dir, self.construct_scalar(node))
        if self._filename == filename:
            raise yaml.YAMLError('inclusion loop detected at %s' % filename)
        with open(filename, 'r') as f:
            return yaml.load(f, YAMLLoader)

    @staticmethod
    def load(filename):
        return yaml.load(codecs.open(filename, 'r', 'utf8'), YAMLLoader)


YAMLLoader.add_constructor('!include', YAMLLoader.include)


class Command(object):
    def __init__(self, name, subparsers):
        self.name = name
        self.parser = subparsers.add_parser(name)
        self.parser.set_defaults(func=self.run)

    def run(self, args):
        self.parser.print_help()
        return 1
