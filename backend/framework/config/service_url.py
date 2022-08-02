#!/bin/env python
# -*- coding: utf-8 -*-
# @author DDDivano
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
"""
静态内容配置，包括子服务配置，服务项关联管理关系等

"""


###  子服务部署方式有两种， localbuild  OR  xly
"""
类配置好处是IDE方便丶出来
LOCAL = {
    "FRAMEWORK": {
        "API_FUNCTION": "http://127.0.0.1:8005/framework/runner"
    }
}
API = "http://127.0.0.1:8005/framework/runner"
"""



class Framework(object):
    """
    Framework
    """
    API_FUNCTION = "http://127.0.0.1:8005/framework/runner"
    API_BENCHMARK = ""

class Local(Framework):
    """
    Framework
    """
    pass
