# -*-  coding:utf-8 -*-

import os
import yaml

import bmcm


class YAMLLoader(yaml.loader.Loader):
    def __init__(self, stream):
        super(YAMLLoader, self).__init__(stream)
        self.root_dir = bmcm.config.BMCM_DATA_ROOTDIR
        self._filename = stream.name

    def include(self, node):
        filename = os.path.join(self.root_dir, self.construct_scalar(node))
        if self._filename == filename:
            raise yaml.YAMLError('inclusion loop detected at %s' % filename)
        with open(filename, 'r') as f:
            return yaml.load(f, YAMLLoader)


YAMLLoader.add_constructor('!include', YAMLLoader.include)
