#!/bin/env python3
# -*- coding: utf-8 -*-
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
"""
/***************************************************************************
  *
  * Copyright (c) 2023 Baidu.com, Inc. All Rights Reserved
  * @file:  service_url.py
  * @author:  luozeyu01
  * @date  2023/2/24 11:17 AM
  * @brief
  *
  **************************************************************************/
"""

# 超级用户
API_BENCHMARK_SUPERUSER = ["zhengtianyu", "liuhuanling", "luozeyu01"]

CLOUD = "xly"

PLACE = {
    # "api_benchmark": CLOUD,
    "gpu": CLOUD,
    "x86": CLOUD,
    "xpu": CLOUD,
    "arm": CLOUD
}


class Cloud(object):
    """
    for xly , value is "pipeline conf id", parameters.
    """
    ##########  LINUX  ##########
    gpu = "25813"
    x86 = "25819"


class CloudMission(object):
    """
    for xly
    """
    ROUTER = {
        "gpu": Cloud.gpu,
        "x86": Cloud.x86,
    }


DOCKER_IMAGE = {
"v11.6": "registry.baidubce.com/paddlepaddle/paddle:latest-dev-cuda11.6.2-cudnn8.4.0-gcc82",
# "v11.4": "registry.baidubce.com/paddlepaddle/paddle:latest-dev-cuda11.4.1-cudnn8-gcc82",
"v11.2": "registry.baidubce.com/paddlepaddle/paddle:latest-dev-cuda11.2-cudnn8-gcc82",
# "v11.0": "registry.baidubce.com/paddlepaddle/paddle:latest-dev-cuda11.0-cudnn8-gcc82",
"v10.2": "registry.baidubce.com/paddlepaddle/paddle:latest-dev-cuda10.2-cudnn7-gcc82",
# "v10.1": "registry.baidubce.com/paddlepaddle/paddle:latest-dev-cuda10.1-cudnn7-gcc82",
}
