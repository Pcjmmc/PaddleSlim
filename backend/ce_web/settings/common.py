#!/usr/bin/env python
# encoding: utf-8
"""
load and parse yaml config by DEPLOYMENT_TYPE
"""
import os
import logging
import logging.config
import time
import yaml
from ce_web.settings.rpc_config import *
#  a util func use for connect path. eg:
#  >>> path('/a', 'b', 'c')
#  >>> '/a/b/c'
path = lambda root, *a: os.path.join(root, *a)
# some basic path settings
SETTING_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SETTING_DIR)
BASE_DIR = os.path.dirname(PROJECT_ROOT)

# Development type setting
class DeploymentType(object):
    """
    定义开发环境变量
    """
    PRODUCTION = "PRODUCTION"
    DEV = "DEV"


if 'DEPLOYMENT_TYPE' in os.environ:
    DEPLOYMENT = os.environ['DEPLOYMENT_TYPE'].upper()
    DEBUG = False
else:
    DEPLOYMENT = DeploymentType.DEV
    DEBUG = True

# ##########################
# load storage config
# ##########################
try:
    f = open(path(SETTING_DIR, 'storage.yaml'))
    STORAGE = yaml.safe_load(f)[DEPLOYMENT]
except Exception as e:
    STORAGE = {}
finally:
    f.close()


# 其他设置
WEB_SETTINGS = {
    'cookie_secret': 'SgJbCDM9SVm4N6qXVzEDMeZv3XNNNkb/o+pJT0MDReR+zHDN2PdNA6WjWK+iO1bGuaTiS1a5TJSq1kTOnaA0eg==',
    'xsrf_cookies': False,
    'model_classes': {},
    'debug': DEBUG,
}

# key word
BLACK_KEYWORD = "Win_"

if __name__ == '__main__':
    print(STORAGE)
    print(BUILDTASK)