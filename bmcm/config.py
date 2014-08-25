# -*-  coding:utf-8 -*-

# Path root data

import os

BMCM_DATA_ROOTDIR = os.getenv('BMCM_DATA_ROOTDIR')
if BMCM_DATA_ROOTDIR is None:
    BMCM_DATA_ROOTDIR =  '../management'
