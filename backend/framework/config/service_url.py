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
    ######## 框架基础
    "api_function": CLOUD,
    "op_function": CLOUD,
    "external_api_function": CLOUD,
    "distribution_api_function": CLOUD,
    # jit
    "jit_function": CLOUD,
    # api_benchmark

    # infer:
    "native_infer": CLOUD,
    "trt_infer": CLOUD,
    "mkldnn_infer": CLOUD,
    
    # models
    "paddleclas": CLOUD,
    # model benchmark
    "models_benchmark_v100_single_dp": LOCAL,
    "models_benchmark_v100_multi_dp": LOCAL,
    "models_benchmark_v100_dist_collective": LOCAL,
    "models_benchmark_a100_single_dp": LOCAL,
    "models_benchmark_a100_multi_dp": LOCAL,

    # dist collective
    "distribution_v100_accuracy_collective": LOCAL,
}

class Cloud(object):
    """
    for xly , value is "pipeline conf id", parameters.
    """
    ##########  LINUX  ##########
    OP_FUNCTION = "23490", {"whoami": "DDDivano"}
    EXTERNAL_API_FUNCTION = "23686"
    DISTRIBUTION_API_FUNCTION = "23542"
    JIT_FUNCTION = "23640"
    API_BENCHMARK = ""
    PADDLE_CLAS = "23369"
    MODEL_BENCHMARK = "23601"

    # 原生推理
    NATIVE_INFER = "24293"
    # TRT推理
    TRT_INFER = "24296"
    # MKLDNN推理
    MKLDNN_INFER = "24297"

    ##########  WINDOWS  ##########
    WIN_OP_FUNCTION = ""
    ##########  DARWIN  ##########
    MAC_OP_FUNCTION = ""

class Local(object):
    """
    Framework
    """
    ##########  LINUX  ##########
    API_FUNCTION = ""
    API_BENCHMARK = ""

    # Benchmark 知识库 https://ku.baidu-int.com/knowledge/HFVrC7hq1Q/t7n0qKWNJW/QMxJ7wiFu-/WPNAbgcfv0R4MK?source=1
    # V100 单机性能测试（分布式策略：DP，默认模型优先级：S_P0）
    MODELS_BENCHMARK_V100_SINGLE_DP = "http://10.138.35.185:8989/auto_test/", \
                                      {"device_type": "V100", "cards_type_list": "N1C1,N1C8", "run_mode_list": "DP",
                                       "model_priority_list": "S_P0", "test_name": "V100单机性能测试"}
    # V100 多机性能测试（分布式策略：DP，默认模型优先级：M_P0）
    MODELS_BENCHMARK_V100_MULTI_DP = "http://10.138.35.185:8989/auto_test/", \
                                     {"device_type": "V100", "cards_type_list": "N1C1,N1C8,N4C32",
                                      "run_mode_list": "DP", "model_priority_list": "M_P0",
                                      "test_name": "V100多机性能测试"}
    # V100 分布式Collective模式（分布式策略：Collective）（只看性能的模型）
    MODELS_BENCHMARK_V100_DIST_COLLECTIVE = "http://10.138.35.185:8989/auto_test/", \
                                            {"device_type": "V100", "cards_type_list": "N1C1,N1C8,N4C32",
                                             "run_mode_list": "Collective", "model_priority_list": "M_P5",
                                             "test_name": "V100分布式Collective模式（分布式策略：Collective）性能测试"}
    # A100 单机性能测试（分布式策略：DP，默认模型优先级：S_P0）
    MODELS_BENCHMARK_A100_SINGLE_DP = "http://10.138.35.185:8989/auto_test/", \
                                      {"device_type": "A100", "cards_type_list": "N1C1,N1C8",
                                       "run_mode_list": "DP", "model_priority_list": "S_P0",
                                       "test_name": "A100单机性能测试"
                                       }
    # A100 多机性能测试（分布式策略：DP，默认模型优先级：M_P0）
    MODELS_BENCHMARK_A100_MULTI_DP = "http://10.138.35.185:8989/auto_test/", \
                                     {"device_type": "A100", "cards_type_list": "N1C1,N1C8,N4C32",
                                      "run_mode_list": "DP", "model_priority_list": "M_P0",
                                      "test_name": "A100多机性能测试"}
    # 分布式精度测试 V100 分布式Collective模式（分布式策略：Collective）
    DISTRIBUTION_V100_ACCURACY_COLLECTIVE = "http://10.138.35.185:8989/auto_test/", \
                                            {"device_type": "V100", "cards_type_list": "N1C1,N1C8,N4C32",
                                             "run_mode_list": "Collective", "model_priority_list": "D_P0",
                                             "email_index": "ips,convergence", "test_name": "V100分布式Collective精度测试"}
    ##########  WINDOWS  ##########

    ##########  DARWIN  ##########


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

        "native_infer": Cloud.NATIVE_INFER,
        "trt_infer": Cloud.TRT_INFER,
        "mkldnn_infer": Cloud.MKLDNN_INFER,

        "paddleclas": Cloud.PADDLE_CLAS,
        "models_benchmark": Cloud.MODEL_BENCHMARK,
    }


class LocalMission(object):
    """
    for local testing
    """
    ROUTER = {
        "models_benchmark_v100_single_dp": Local.MODELS_BENCHMARK_V100_SINGLE_DP,
        "models_benchmark_v100_multi_dp": Local.MODELS_BENCHMARK_V100_MULTI_DP,
        "models_benchmark_v100_dist_collective": Local.MODELS_BENCHMARK_V100_DIST_COLLECTIVE,
        "models_benchmark_a100_single_dp": Local.MODELS_BENCHMARK_A100_SINGLE_DP,
        "models_benchmark_a100_multi_dp": Local.MODELS_BENCHMARK_A100_MULTI_DP,
        "distribution_v100_accuracy_collective": Local.DISTRIBUTION_V100_ACCURACY_COLLECTIVE,
    }


DOCKER_IMAGE = {
"v11.6": "registry.baidubce.com/paddlepaddle/paddle:latest-dev-cuda11.6.2-cudnn8.4.0-gcc82",
"v11.4": "registry.baidubce.com/paddlepaddle/paddle:latest-dev-cuda11.4.1-cudnn8-gcc82",
"v11.2": "registry.baidubce.com/paddlepaddle/paddle:latest-dev-cuda11.2-cudnn8-gcc82",
"v11.0": "registry.baidubce.com/paddlepaddle/paddle:latest-dev-cuda11.0-cudnn8-gcc82",
"v10.2": "registry.baidubce.com/paddlepaddle/paddle:latest-dev-cuda10.2-cudnn7-gcc82",
"v10.1": "registry.baidubce.com/paddlepaddle/paddle:latest-dev-cuda10.1-cudnn7-gcc82",
}

DOCKER_INFER_IMAGE = {
"v11.7": "registry.baidubce.com/paddlepaddle/paddle_manylinux_devel:cuda11.7-cudnn8.4-trt8.4-gcc8.2",
"v11.6": "registry.baidubce.com/paddlepaddle/paddle_manylinux_devel:cuda11.6-cudnn8.4.0-trt8.4.0.6-gcc82",
"v11.2": "registry.baidubce.com/paddlepaddle/paddle_manylinux_devel:cuda11.2-cudnn8.2.1-trt8.0.3.4-gcc82",
# "v11.2": "registry.baidubce.com/paddlepaddle/paddle_manylinux_devel:cuda11.2-cudnn8.1-trt8.0-gcc8.2",
"v11.1": "registry.baidubce.com/paddlepaddle/paddle_manylinux_devel:cuda11.1-cudnn8.1-gcc82-trt7",
"v10.2": "registry.baidubce.com/paddlepaddle/paddle_manylinux_devel:cuda10.2-cudnn7.6-trt7.0-gcc8.2",
}


COMPILE_SERVICE = "http://10.138.35.178:8082/compile"


# ALLURE 相关 , 需提前准备环境
REPORT_SOURCE_NAME = "pts_report.tar"
WWW_DIR = "/ssd1/pts/report/"
SOURCE_DIR = "/ssd1/pts/source/"
ALLURE = "/ssd1/pts/tools/allure/bin/allure"
REPORT_SERVER = "http://paddletest.baidu-int.com:8333/"
