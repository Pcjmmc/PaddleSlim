#!/bin/env python
# -*- coding: utf-8 -*-
# @author DDDivano
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
"""
静态内容配置，包括子服务配置，服务项关联管理关系等

"""


###  子服务部署方式有两种， localbuild  OR  xly
import base64

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

# PLACE 是首要判断条件，对接前端返回内容，并check执行环境
PLACE = {
    # api_function
    "api_function": CLOUD,
    "op_function": CLOUD,
    "external_api_function": CLOUD,
    "distribution_api_function": CLOUD,
    # jit
    "jit_function": CLOUD,
    # api_benchmark

    # models
    "paddleclas": CLOUD,


    # model benchmark
    "models_benchmark": CLOUD,
}

class Cloud(object):
    """
    for xly , value is "pipeline conf id", parameters.
    """
    OP_FUNCTION = "23490", {"whoami": "DDDivano"}
    EXTERNAL_API_FUNCTION = "23686"
    DISTRIBUTION_API_FUNCTION = "23542"
    JIT_FUNCTION = "23640"
    API_BENCHMARK = ""
    PADDLE_CLAS = "23369"

    MODEL_BENCHMARK = "23601"

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
        "api_function": ["op_function", "external_api_function", "io_function", "distribution_api_function"],
        "op_function": Cloud.OP_FUNCTION,
        "external_api_function": Cloud.EXTERNAL_API_FUNCTION,
        "distribution_api_function": Cloud.DISTRIBUTION_API_FUNCTION,
        "jit_function": Cloud.JIT_FUNCTION,
        "api_benchmark": [],
        "paddleclas": Cloud.PADDLE_CLAS,
        "models_benchmark": Cloud.MODEL_BENCHMARK,
    }


class LocalMission(object):
    """
    for local testing
    """
    ROUTER = {
        "api_function": ["op_function", "external_api_function", "io_function"]

    }


DOCKER_IMAGE = {
"v11.6": "registry.baidubce.com/paddlepaddle/paddle:latest-dev-cuda11.6.2-cudnn8.4.0-gcc82",
"v11.4": "registry.baidubce.com/paddlepaddle/paddle:latest-dev-cuda11.4.1-cudnn8-gcc82",
"v11.2": "registry.baidubce.com/paddlepaddle/paddle:latest-dev-cuda11.2-cudnn8-gcc82",
"v11.0": "registry.baidubce.com/paddlepaddle/paddle:latest-dev-cuda11.0-cudnn8-gcc82",
"v10.2": "registry.baidubce.com/paddlepaddle/paddle:latest-dev-cuda10.2-cudnn7-gcc82",
"v10.1": "registry.baidubce.com/paddlepaddle/paddle:latest-dev-cuda10.1-cudnn7-gcc82",
}


COMPILE_SERVICE = "http://10.138.35.178:8082/compile"


# ALLURE 相关
REPORT_SOURCE_NAME = "pts_report.tar"
WWW_DIR = "/ssd1/pts/report/"
SOURCE_DIR = "/ssd1/pts/source/"
REPORT_SERVER = "http://10.21.226.171:8333/"