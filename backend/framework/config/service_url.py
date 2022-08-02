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
CLOUD = "xly"
LOCAL = "local"


PLACE = {
    "api_function": CLOUD,
    "op_function": CLOUD,
    "paddleclas": CLOUD,
}



class Cloud(object):
    """
    for xly , value is "pipeline conf id"
    """
    API_FUNCTION = ""
    OP_FUNCTION = "23490"
    API_BENCHMARK = ""
    PADDLE_CLAS = "23369"

class Local(object):
    """
    Framework
    """
    API_FUNCTION = ""
    API_BENCHMARK = ""


class CloudMission(object):
    """
    for xly
    """
    ROUTER = {
        "api_function": ["op_function", "external_api_function", "io_function"],
        "op_function": Cloud.OP_FUNCTION,
        "api_benchmark": [],
        "paddleclas": Cloud.PADDLE_CLAS
    }


class LocalMission(object):
    """
    for local testing
    """
    ROUTER = {
        "api_function": ["op_function", "external_api_function", "io_function"]

    }