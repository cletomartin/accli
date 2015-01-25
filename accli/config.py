# -*-  coding:utf-8 -*-

# Path root data

import os

ACCLI_DATA_ROOTDIR = os.getenv('ACCLI_DATA_ROOTDIR')
if ACCLI_DATA_ROOTDIR is None:
    ACCLI_DATA_ROOTDIR = 'data'
