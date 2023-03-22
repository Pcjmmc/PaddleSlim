# encoding： utf-8
"""
日志初始化模块
"""
import json
import logging
import os
import sys
import traceback
from logging import config

import yaml
from ce_web.settings.common import LOG_PATH

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
YAML_CFG_PATH = os.path.join(BASE_DIR, 'logging.yaml')


class InitLogger(object):
    """
    日志 启动引擎
    """
    def __init__(self):
        self.loader = yaml.load(open(YAML_CFG_PATH, 'r'), Loader=yaml.FullLoader)
        # 对self.load值做替换
        var_name = 'LOG_PATH'
        content = json.dumps(self.loader)
        content = content.replace("${{{0}}}".format(var_name), str(LOG_PATH))
        self.loader=json.loads(content)

    def start(self):
        """
        开始加载日志logger
        """
        #判断下如果是debug
        if 'DEPLOYMENT_TYPE' in os.environ:
            envs = os.environ['DEPLOYMENT_TYPE'].lower()
            self.loader["loggers"]["ce"] = self.loader["loggers"][envs]
        else:
            self.loader["loggers"]["ce"] = self.loader["loggers"]["dev"]
        config.dictConfig(self.loader)