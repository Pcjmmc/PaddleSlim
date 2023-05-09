#!/bin/env python3
# -*- coding: utf-8 -*-
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
"""
/***************************************************************************
  *
  * Copyright (c) 2020 Baidu.com, Inc. All Rights Reserved
  * @file:  module.py
  * @author:  luozeyu01
  * @date  2023/2/24 2:02 PM
  * @brief
  *
  **************************************************************************/
"""


class Compile(object):
    """
    for xly , value is "pipeline conf id", parameters.
    """
    ##########  LINUX  ##########
    gpu = {
        "ENABLE_BENCHMARK": 'ON',
        "WITH_GPU": 'ON',
        # "CMAKE_CXX_COMPILER": '/usr/local/gcc-8.2/bin/g++',
        "ENABLE_ORT_BACKEND": 'ON',
        "ENABLE_TRT_BACKEND": 'ON',
        # "TRT_DIRECTORY": '/workspace/FastDeploy/TensorRT-8.5.2.2',
        "ENABLE_PADDLE_BACKEND": 'ON',
        "ENABLE_OPENVINO_BACKEND": 'ON',
        "ENABLE_VISION": 'ON',
        "ENABLE_TEXT": 'ON',
        "WITH_CAPI": 'ON',
        "BUILD_EXAMPLES": 'OFF',
        "WITH_TESTING": 'OFF'
    }
    x86 = {
        "ENABLE_BENCHMARK": 'ON',
        "WITH_GPU": 'OFF',
        # "CMAKE_CXX_COMPILER": '/usr/local/gcc-8.2/bin/g++',
        "ENABLE_ORT_BACKEND": 'ON',
        "ENABLE_TRT_BACKEND": 'OFF',
        "ENABLE_PADDLE_BACKEND": 'ON',
        "ENABLE_OPENVINO_BACKEND": 'ON',
        "ENABLE_VISION": 'ON',
        "ENABLE_TEXT": 'ON',
        "WITH_CAPI": 'ON',
        "BUILD_EXAMPLES": 'OFF',
        "WITH_TESTING": 'OFF',
    }


class CompileParams(object):
    """
    for xly
    """
    ROUTER = {
        "gpu": Compile.gpu,
        "x86": Compile.x86,
    }
