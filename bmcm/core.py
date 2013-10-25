# -*-  coding:utf-8 -*-

import yaml

from bmcm.config import BMCM_DATA_ROOTDIR

class YAMLLoader(yaml.loader.Loader):
    def __init__(self, stream):
        super(YAMLLoader, self).__init__(stream)
        self.root_dir = BMCM_DATA_ROOTDIR

    def include(self, filename):
        pass
