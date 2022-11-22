#!/bin/env python
# -*- coding: utf-8 -*-
# @author DDDivano
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python

"""
module 配置原始数据
"""

module_mapping = {
    "op_function":"计算OP精度测试",
    "external_api_function":"功能性API测试",
    "distribution_api_function":"分布式API功能测试",
    "jit_function":"JITAPI单独组网测试",
    "native_infer":"原生推理",
    "trt_infer":"TensorRT推理",
    "mkldnn_infer":"MKLDNN推理",
    "models_benchmark_v100_single_dp":"V100_单机性能测试",
    "models_benchmark_v100_multi_dp":"V100_多机性能测试",
    "models_benchmark_v100_dist_collective":"V100_分布式性能测试",
    "distribution_v100_accuracy_collective":"V100_分布式精度测试",
    "models_benchmark_a100_single_dp":"A100_单机性能测试",
    "models_benchmark_a100_multi_dp":"A100_多机性能测试",
    "paddleclas_p0": "PaddleClas P0级功能测试",
    "paddleclas_p1": "PaddleClas P1级功能测试",
    "paddleclas_p2": "PaddleClas P2级功能测试",
    "paddleclas_p2_1": "PaddleClas P2_1级功能测试",
    "paddleclas_p2_2": "PaddleClas P2_2级功能测试",
    "paddlegan_p0": "PaddleGAN P0级功能测试",
    "paddlegan_p1": "PaddleGAN P1级功能测试",
}


module_list = [
    {
        "id":"1",
        "label":"API功能测试",
        "key":"api_function",
        "children":[
            {
                "pid":"1",
                "id":"1-1",
                "label":"计算op精度测试",
                "key":"op_function"
            },
            {
                "pid":"1",
                "id":"1-2",
                "label":"功能性API测试",
                "key":"external_api_function"
            },
            {
                "pid":"1",
                "id":"1-4",
                "label":"分布式API测试",
                "key":"distribution_api_function"
            }
        ]
    },
    {
        "id":"2",
        "label":"动转静测试",
        "key":"jit_function",
        "children":[
            {
                "pid":"2",
                "id":"2-1",
                "label":"JITAPI单独组网测试",
                "key":"jit_function"
            },
            {
                "pid":"2",
                "id":"2-2",
                "label":"JIT模型子结构测试",
                "key":"jit_models_function"
            }
        ]
    },
    {
        "id":"3",
        "label":"预测部署",
        "key":"infer",
        "children":[
            {
                "pid":"3",
                "id":"3-1",
                "label":"原生推理",
                "key":"native_infer"
            },
            {
                "pid":"3",
                "id":"3-2",
                "label":"TensorRT推理",
                "key":"trt_infer"
            },
            {
                "pid":"3",
                "id":"3-3",
                "label":"MKLDNN推理",
                "key":"mkldnn_infer"
            }
        ]
    },
    {
        "id":"4",
        "label":"模型测试",
        "key":"models",
        "children":[
            {
                "pid":"4",
                "id":"4-1",
                "label":"PaddleClas",
                "key":"PaddleClas",
                "children":[
                    {
                        "pid":"4-1",
                        "id":"4-1-1",
                        "label":"PaddleClas P0级功能测试",
                        "key":"paddleclas_p0"
                    },
                    {
                        "pid":"4-1",
                        "id":"4-1-2",
                        "label":"PaddleClas P1级功能测试",
                        "key":"paddleclas_p1"
                    },
                    {
                        "pid": "4-1",
                        "id": "4-1-3",
                        "label": "PaddleClas P2级功能测试",
                        "key": "paddleclas_p2"
                    },
                    {
                        "pid": "4-1",
                        "id": "4-1-4",
                        "label": "PaddleClas P2_1级功能测试",
                        "key": "paddleclas_p2_1"
                    },
                    {
                        "pid": "4-1",
                        "id": "4-1-5",
                        "label": "PaddleClas P2_2级功能测试",
                        "key": "paddleclas_p2_2"
                    }
                ]
            },
            {
                "pid":"4",
                "id":"4-2",
                "label":"PaddleGAN",
                "key":"PaddleGAN",
                "children": [
                    {
                        "pid": "4-2",
                        "id": "4-2-1",
                        "label": "PaddleGAN P0级功能测试",
                        "key": "paddlegan_p0"
                    },
                    {
                        "pid": "4-2",
                        "id": "4-2-2",
                        "label": "PaddleGAN P1级功能测试",
                        "key": "paddlegan_p1"
                    }
                ]
            }
        ]
    },
    {
        "id":"5",
        "label":"模型性能测试",
        "key":"models_benchmark",
        "children":[
            {
                "pid":"5",
                "id":"5-1",
                "label":"V100",
                "key":"V100",
                "children":[
                    {
                        "pid":"5-1",
                        "id":"5-1-1",
                        "label":"单机性能测试",
                        "key":"models_benchmark_v100_single_dp"
                    },
                    {
                        "pid":"5-1",
                        "id":"5-1-2",
                        "label":"多机性能测试",
                        "key":"models_benchmark_v100_multi_dp"
                    },
                    {
                        "pid":"5-1",
                        "id":"5-1-3",
                        "label":"分布式Collective模式性能测试",
                        "key":"models_benchmark_v100_dist_collective"
                    },
                    {
                        "pid":"5-1",
                        "id":"5-1-4",
                        "label":"分布式Collective模式精度测试",
                        "key":"distribution_v100_accuracy_collective"
                    }
                ]
            },
            {
                "pid":"5",
                "id":"5-2",
                "label":"A100",
                "key":"A100",
                "children":[
                    {
                        "pid":"5-2",
                        "id":"5-2-1",
                        "label":"单机性能测试",
                        "key":"models_benchmark_a100_single_dp"
                    },
                    {
                        "pid":"5-2",
                        "id":"5-2-2",
                        "label":"多机性能测试",
                        "key":"models_benchmark_a100_multi_dp"
                    }
                ]
            }
        ]
    }
]