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
    "paddleclas_p0_function": "PaddleClas P0级功能性",
    "paddlegan_p0_function": "PaddleGAN P0级功能性",
    "paddleocr_p0_function": "PaddleOCR P0级功能性",
    "paddle3d_p0_function": "Paddle3D P0级功能性",
    "paddlespeech_p0_function": "PaddleSpeech P0级功能性",
    "paddledetection_p0_function": "PaddleDetection P0级功能性",
    "paddleseg_p0_function": "PaddleSeg P0级功能性",
    "paddlenlp_p0_function": "PaddleNLP P0级功能性",
    "paddleslim_p0_function": "PaddleSlim P0级功能性",
    "paddlerec_p0_function": "PaddleRec P0级功能性",
    "paddleclas_p0_pretrained_eval": "PaddleClas P0级预训练模型精度",
    "paddlegan_p0_pretrained_eval": "PaddleGAN P0级预训练模型精度",
    "paddleocr_p0_pretrained_eval": "PaddleOCR P0级预训练模型精度",
    "paddle3d_p0_pretrained_eval": "Paddle3D P0级预训练模型精度",
    "paddlespeech_p0_pretrained_eval": "PaddleSpeech P0级预训练模型精度",
    "paddledetection_p0_pretrained_eval": "PaddleDetection P0级预训练模型精度",
    "paddleseg_p0_pretrained_eval": "PaddleSeg P0级预训练模型精度",
    "paddlenlp_p0_pretrained_eval": "PaddleNLP P0级预训练模型精度",
    "paddleslim_p0_pretrained_eval": "PaddleSlim P0级预训练模型精度",
    "paddlerec_p0_pretrained_eval": "PaddleRec P0级预训练模型精度",
    "paddleclas_p0_precision": "PaddleClas P0级小数据集精度",
    "paddlegan_p0_precision": "PaddleGAN P0级小数据集精度",
    "paddleocr_p0_precision": "PaddleOCR P0级小数据集精度",
    "paddle3d_p0_precision": "Paddle3D P0级小数据集精度",
    "paddlespeech_p0_precision": "PaddleSpeech P0级小数据集精度",
    "paddledetection_p0_precision": "PaddleDetection P0级小数据集精度",
    "paddleseg_p0_precision": "PaddleSeg P0级小数据集精度",
    "paddlenlp_p0_precision": "PaddleNLP P0级小数据集精度",
    "paddleslim_p0_precision": "PaddleSlim P0级小数据集精度",
    "paddlerec_p0_precision": "PaddleRec P0级小数据集精度",
    "paddleclas_all_function": "PaddleClas ALL级功能性",
    "paddlegan_all_function": "PaddleGAN ALL级功能性",
    "paddleocr_all_function": "PaddleOCR ALL级功能性",
    "paddle3d_all_function": "Paddle3D ALL级功能性",
    "paddlespeech_all_function": "PaddleSpeech ALL级功能性",
    "paddledetection_all_function": "PaddleDetection ALL级功能性",
    "paddleseg_all_function": "PaddleSeg ALL级功能性",
    "paddlenlp_all_function": "PaddleNLP ALL级功能性",
    "paddleslim_all_function": "PaddleSlim ALL级功能性",
    "paddlerec_all_function": "PaddleRec ALL级功能性",
    "paddleclas_all_pretrained_eval": "PaddleClas ALL级预训练模型精度",
    "paddlegan_all_pretrained_eval": "PaddleGAN ALL级预训练模型精度",
    "paddleocr_all_pretrained_eval": "PaddleOCR ALL级预训练模型精度",
    "paddle3d_all_pretrained_eval": "Paddle3D ALL级预训练模型精度",
    "paddlespeech_all_pretrained_eval": "PaddleSpeech ALL级预训练模型精度",
    "paddledetection_all_pretrained_eval": "PaddleDetection ALL级预训练模型精度",
    "paddleseg_all_pretrained_eval": "PaddleSeg ALL级预训练模型精度",
    "paddlenlp_all_pretrained_eval": "PaddleNLP ALL级预训练模型精度",
    "paddleslim_all_pretrained_eval": "PaddleSlim ALL级预训练模型精度",
    "paddlerec_all_pretrained_eval": "PaddleRec ALL级预训练模型精度"
    "paddleclas_all_precision": "PaddleClas ALL级小数据集精度",
    "paddlegan_all_precision": "PaddleGAN ALL级小数据集精度",
    "paddleocr_all_precision": "PaddleOCR ALL级小数据集精度",
    "paddle3d_all_precision": "Paddle3D ALL级小数据集精度",
    "paddlespeech_all_precision": "PaddleSpeech ALL级小数据集精度",
    "paddledetection_all_precision": "PaddleDetection ALL级小数据集精度",
    "paddleseg_all_precision": "PaddleSeg ALL级小数据集精度",
    "paddlenlp_all_precision": "PaddleNLP ALL级小数据集精度",
    "paddleslim_all_precision": "PaddleSlim ALL级小数据集精度",
    "paddlerec_all_precision": "PaddleRec ALL级小数据集精度"
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
                "label":"重要模型 功能性",
                "key":"p0_function",
                "desc":"执行P0优先级模型, 阶段包括训练单卡、训练多卡、评估、推理、动转静、静态图预测的功能, 具体执行模型列表见报告",
                "children":[
                    {
                        "pid":"4-1",
                        "id":"4-1-1",
                        "label":"PaddleClas P0级功能性",
                        "key":"paddleclas_p0_function",
                    },
                    {
                        "pid":"4-1",
                        "id":"4-1-2",
                        "label":"PaddleGAN P0级功能性",
                        "key":"paddlegan_p0_function"
                    },
                    {
                        "pid":"4-1",
                        "id":"4-1-3",
                        "label":"PaddleOCR P0级功能性",
                        "key":"paddleocr_p0_function"
                    },
                    {
                        "pid":"4-1",
                        "id":"4-1-4",
                        "label":"Paddle3D P0级功能性",
                        "key":"paddle3d_p0_function"
                    },
                    {
                        "pid":"4-1",
                        "id":"4-1-5",
                        "label":"PaddleSpeech P0级功能性",
                        "key":"paddlespeech_p0_function"
                    },
                    {
                        "pid":"4-1",
                        "id":"4-1-6",
                        "label":"PaddleDetection P0级功能性",
                        "key":"paddledetection_p0_function"
                    },
                    {
                        "pid":"4-1",
                        "id":"4-1-7",
                        "label":"PaddleSeg P0级功能性",
                        "key":"paddleseg_p0_function"
                    },
                    {
                        "pid":"4-1",
                        "id":"4-1-8",
                        "label":"PaddleNLP P0级功能性",
                        "key":"paddlenlp_p0_function"
                    },
                    {
                        "pid":"4-1",
                        "id":"4-1-9",
                        "label":"PaddleSlim P0级功能性",
                        "key":"paddleslim_p0_function"
                    },
                    {
                        "pid":"4-1",
                        "id":"4-1-10",
                        "label":"PaddleRec P0级功能性",
                        "key":"paddlerec_p0_function"
                    }
                ]
            },
            {
                "pid":"4",
                "id":"4-2",
                "label":"重要模型 预训练模型 评估、动态图推理、静态图预测精度",
                "key":"p0_pretrained_eval",
                "desc":"执行P0优先级模型, 阶段包括使用预训练模型 评估、推理、动转静、静态图预测的精度验证, 具体执行模型列表见报告",
                "children":[
                    {
                        "pid":"4-2",
                        "id":"4-2-1",
                        "label":"PaddleClas P0级预训练模型精度",
                        "key":"paddleclas_p0_pretrained_eval"
                    },
                    {
                        "pid":"4-2",
                        "id":"4-2-2",
                        "label":"PaddleGAN P0级预训练模型精度",
                        "key":"paddlegan_p0_pretrained_eval"
                    },
                    {
                        "pid":"4-2",
                        "id":"4-2-3",
                        "label":"PaddleOCR P0级预训练模型精度",
                        "key":"paddleocr_p0_pretrained_eval"
                    },
                    {
                        "pid":"4-2",
                        "id":"4-2-4",
                        "label":"Paddle3D P0级预训练模型精度",
                        "key":"paddle3d_p0_pretrained_eval"
                    },
                    {
                        "pid":"4-2",
                        "id":"4-2-5",
                        "label":"PaddleSpeech P0级预训练模型精度",
                        "key":"paddlespeech_p0_pretrained_eval"
                    },
                    {
                        "pid":"4-2",
                        "id":"4-2-6",
                        "label":"PaddleDetection P0级预训练模型精度",
                        "key":"paddledetection_p0_pretrained_eval"
                    },
                    {
                        "pid":"4-2",
                        "id":"4-2-7",
                        "label":"PaddleSeg P0级预训练模型精度",
                        "key":"paddleseg_p0_pretrained_eval"
                    },
                    {
                        "pid":"4-2",
                        "id":"4-2-8",
                        "label":"PaddleNLP P0级预训练模型精度",
                        "key":"paddlenlp_p0_pretrained_eval"
                    },
                    {
                        "pid":"4-2",
                        "id":"4-2-9",
                        "label":"PaddleSlim P0级预训练模型精度",
                        "key":"paddleslim_p0_pretrained_eval"
                    },
                    {
                        "pid":"4-2",
                        "id":"4-2-10",
                        "label":"PaddleRec P0级预训练模型精度",
                        "key":"paddlerec_p0_pretrained_eval"
                    }
                ]
            },
            {
                "pid":"4",
                "id":"4-3",
                "label":"重要模型 小数据精度",
                "key":"p0_precision",
                "desc":"执行P0优先级模型, 阶段包括小数据集训练单卡、训练多卡、评估、推理、动转静、静态图预测精度测试, 具体执行模型列表见报告",
                "children":[
                    {
                        "pid":"4-3",
                        "id":"4-3-1",
                        "label":"PaddleClas P0级小数据精度",
                        "key":"paddleclas_p0_precision",
                    },
                    {
                        "pid":"4-3",
                        "id":"4-3-2",
                        "label":"PaddleGAN P0级小数据精度",
                        "key":"paddlegan_p0_precision"
                    },
                    {
                        "pid":"4-3",
                        "id":"4-3-3",
                        "label":"PaddleOCR P0级小数据精度",
                        "key":"paddleocr_p0_precision"
                    },
                    {
                        "pid":"4-3",
                        "id":"4-3-4",
                        "label":"Paddle3D P0级小数据精度",
                        "key":"paddle3d_p0_precision"
                    },
                    {
                        "pid":"4-3",
                        "id":"4-3-5",
                        "label":"PaddleSpeech P0级小数据精度",
                        "key":"paddlespeech_p0_precision"
                    },
                    {
                        "pid":"4-3",
                        "id":"4-3-6",
                        "label":"PaddleDetection P0级小数据精度",
                        "key":"paddledetection_p0_precision"
                    },
                    {
                        "pid":"4-3",
                        "id":"4-3-7",
                        "label":"PaddleSeg P0级小数据精度",
                        "key":"paddleseg_p0_precision"
                    },
                    {
                        "pid":"4-3",
                        "id":"4-3-8",
                        "label":"PaddleNLP P0级小数据精度",
                        "key":"paddlenlp_p0_precision"
                    },
                    {
                        "pid":"4-3",
                        "id":"4-3-9",
                        "label":"PaddleSlim P0级小数据精度",
                        "key":"paddleslim_p0_precision"
                    },
                    {
                        "pid":"4-3",
                        "id":"4-3-10",
                        "label":"PaddleRec P0级小数据精度",
                        "key":"paddlerec_p0_precision"
                    }
                ]
            },
            {
                "pid":"4",
                "id":"4-4",
                "label":"全量模型 功能性",
                "key":"all_function",
                 "desc":"执行ALL优先级模型, 阶段包括训练单卡、训练多卡、评估、推理、动转静、静态图预测的功能, 具体执行模型列表见报告",
                "children":[
                    {
                        "pid":"4-4",
                        "id":"4-4-1",
                        "label":"PaddleClas ALL级功能性",
                        "key":"paddleclas_all_function"
                    },
                    {
                        "pid":"4-4",
                        "id":"4-4-2",
                        "label":"PaddleGAN ALL级功能性",
                        "key":"paddlegan_all_function"
                    },
                    {
                        "pid":"4-4",
                        "id":"4-4-3",
                        "label":"PaddleOCR ALL级功能性",
                        "key":"paddleocr_all_function"
                    },
                    {
                        "pid":"4-4",
                        "id":"4-4-4",
                        "label":"Paddle3D ALL级功能性",
                        "key":"paddle3d_all_function"
                    },
                    {
                        "pid":"4-4",
                        "id":"4-4-5",
                        "label":"PaddleSpeech ALL级功能性",
                        "key":"paddlespeech_all_function"
                    },
                    {
                        "pid":"4-4",
                        "id":"4-4-6",
                        "label":"PaddleDetection ALL级功能性",
                        "key":"paddledetection_all_function"
                    },
                    {
                        "pid":"4-4",
                        "id":"4-4-7",
                        "label":"PaddleSeg ALL级功能性",
                        "key":"paddleseg_all_function"
                    },
                    {
                        "pid":"4-4",
                        "id":"4-4-8",
                        "label":"PaddleNLP ALL级功能性",
                        "key":"paddlenlp_all_function"
                    },
                    {
                        "pid":"4-4",
                        "id":"4-4-9",
                        "label":"PaddleSlim ALL级功能性",
                        "key":"paddleslim_all_function"
                    },
                    {
                        "pid":"4-4",
                        "id":"4-4-10",
                        "label":"PaddleRec ALL级功能性",
                        "key":"paddlerec_all_function"
                    }
                ]
            },
            {
                "pid":"4",
                "id":"4-5",
                "label":"全量模型 预训练模型 评估、动态图推理、静态图预测精度",
                "key":"all_pretrained_eval",
                "desc":"执行ALL优先级模型, 阶段包括使用预训练模型 评估、推理、动转静、静态图预测的精度验证, 具体执行模型列表见报告",
                "children":[
                    {
                        "pid":"4-5",
                        "id":"4-5-1",
                        "label":"PaddleClas ALL级预训练模型精度",
                        "key":"paddleclas_all_pretrained_eval"
                    },
                    {
                        "pid":"4-5",
                        "id":"4-5-2",
                        "label":"PaddleGAN ALL级预训练模型精度",
                        "key":"paddlegan_all_pretrained_eval"
                    },
                    {
                        "pid":"4-5",
                        "id":"4-5-3",
                        "label":"PaddleOCR ALL级预训练模型精度",
                        "key":"paddleocr_all_pretrained_eval"
                    },
                    {
                        "pid":"4-5",
                        "id":"4-5-4",
                        "label":"Paddle3D ALL级预训练模型精度",
                        "key":"paddle3d_all_pretrained_eval"
                    },
                    {
                        "pid":"4-5",
                        "id":"4-5-5",
                        "label":"PaddleSpeech ALL级预训练模型精度",
                        "key":"paddlespeech_all_pretrained_eval"
                    },
                    {
                        "pid":"4-5",
                        "id":"4-5-6",
                        "label":"PaddleDetection ALL级预训练模型精度",
                        "key":"paddledetection_all_pretrained_eval"
                    },
                    {
                        "pid":"4-5",
                        "id":"4-5-7",
                        "label":"PaddleSeg ALL级预训练模型精度",
                        "key":"paddleseg_all_pretrained_eval"
                    },
                    {
                        "pid":"4-5",
                        "id":"4-5-8",
                        "label":"PaddleNLP ALL级预训练模型精度",
                        "key":"paddlenlp_all_pretrained_eval"
                    },
                    {
                        "pid":"4-5",
                        "id":"4-5-9",
                        "label":"PaddleSlim ALL级预训练模型精度",
                        "key":"paddleslim_all_pretrained_eval"
                    },
                    {
                        "pid":"4-5",
                        "id":"4-5-10",
                        "label":"PaddleRec ALL级预训练模型精度",
                        "key":"paddlerec_all_pretrained_eval"
                    }
                ]
            },
            {
                "pid":"4",
                "id":"4-6",
                "label":"全量模型 小数据集精度",
                "key":"all_precision",
                "desc":"执行ALL优先级模型, 阶段包括小数据集训练单卡、训练多卡、评估、推理、动转静、静态图预测精度测试, 具体执行模型列表见报告",
                "children":[
                    {
                        "pid":"4-6",
                        "id":"4-6-1",
                        "label":"PaddleClas ALL级小数据集精度",
                        "key":"paddleclas_all_precision"
                    },
                    {
                        "pid":"4-6",
                        "id":"4-6-2",
                        "label":"PaddleGAN ALL级小数据集精度",
                        "key":"paddlegan_all_precision"
                    },
                    {
                        "pid":"4-6",
                        "id":"4-6-3",
                        "label":"PaddleOCR ALL级小数据集精度",
                        "key":"paddleocr_all_precision"
                    },
                    {
                        "pid":"4-6",
                        "id":"4-6-4",
                        "label":"Paddle3D ALL级小数据集精度",
                        "key":"paddle3d_all_precision"
                    },
                    {
                        "pid":"4-6",
                        "id":"4-6-5",
                        "label":"PaddleSpeech ALL级小数据集精度",
                        "key":"paddlespeech_all_precision"
                    },
                    {
                        "pid":"4-6",
                        "id":"4-6-6",
                        "label":"PaddleDetection ALL级小数据集精度",
                        "key":"paddledetection_all_precision"
                    },
                    {
                        "pid":"4-6",
                        "id":"4-6-7",
                        "label":"PaddleSeg ALL级小数据集精度",
                        "key":"paddleseg_all_precision"
                    },
                    {
                        "pid":"4-6",
                        "id":"4-6-8",
                        "label":"PaddleNLP ALL级小数据集精度",
                        "key":"paddlenlp_all_precision"
                    },
                    {
                        "pid":"4-6",
                        "id":"4-6-9",
                        "label":"PaddleSlim ALL级小数据集精度",
                        "key":"paddleslim_all_precision"
                    },
                    {
                        "pid":"4-6",
                        "id":"4-6-10",
                        "label":"PaddleRec ALL级小数据集精度",
                        "key":"paddlerec_all_precision"
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