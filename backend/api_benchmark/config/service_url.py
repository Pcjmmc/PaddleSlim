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

CLOUD = "xly"

PLACE = {
    "api_benchmark": CLOUD
}


class Cloud(object):
    """
    for xly , value is "pipeline conf id", parameters.
    """
    ##########  LINUX  ##########
    API_BENCHMARK = "24448"


class CloudMission(object):
    """
    for xly
    """
    ROUTER = {
        "api_benchmark": Cloud.API_BENCHMARK
    }


DOCKER_IMAGE = {
"v11.6": "registry.baidubce.com/paddlepaddle/paddle:latest-dev-cuda11.6.2-cudnn8.4.0-gcc82",
# "v11.4": "registry.baidubce.com/paddlepaddle/paddle:latest-dev-cuda11.4.1-cudnn8-gcc82",
"v11.2": "registry.baidubce.com/paddlepaddle/paddle:latest-dev-cuda11.2-cudnn8-gcc82",
# "v11.0": "registry.baidubce.com/paddlepaddle/paddle:latest-dev-cuda11.0-cudnn8-gcc82",
"v10.2": "registry.baidubce.com/paddlepaddle/paddle:latest-dev-cuda10.2-cudnn7-gcc82",
# "v10.1": "registry.baidubce.com/paddlepaddle/paddle:latest-dev-cuda10.1-cudnn7-gcc82",
}

# 测试选项
framework_map = {'1': 'paddle', '0': 'torch'}
enable_backward_map = {'1': 'True', '0': 'False'}
place_map = {'1': 'False', '0': 'True'}

# TEST_OPTION = {
#     'comment': None,
#     'with_gpu': None,
#     'enable_backward': None,
#     'framework': None,
#     'wheel_link': None,
#     'cuda': None,
#     'python': None
# }

# 配置选取
yaml_type_map = {'1': 'default', '0': 'diy'}
yaml_info_map = {'0': 'case_0', '1': 'case_1', '2': 'case_2', '3': 'all'}

# YAML_CONFIG = {
#     'yaml_type': None,
#     'test_index': None
# }
