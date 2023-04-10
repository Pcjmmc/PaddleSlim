#!/bin/env python
# -*- coding: utf-8 -*-
# @author DDDivano
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python
"""
静态内容配置，包括子服务配置，服务项关联管理关系等

"""


###  子服务部署方式有两种， localbuild  OR  xly
import os
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
    #重要模型功能性
    "paddleclas_p0_function": CLOUD,
    "paddlegan_p0_function": CLOUD,
    "paddleocr_p0_function": CLOUD,
    "paddle3d_p0_function": CLOUD,
    "paddlespeech_p0_function": CLOUD,
    "paddledetection_p0_function": CLOUD,
    "paddleseg_p0_function": CLOUD,
    "paddlenlp_p0_function": CLOUD,
    "paddleslim_p0_function": CLOUD,
    "paddlerec_p0_function": CLOUD,

    #重要模型 预训练模型评估、推理、预测精度
    "paddleclas_p0_pretrained_eval": CLOUD,
    "paddlegan_p0_pretrained_eval": CLOUD,
    "paddleocr_p0_pretrained_eval": CLOUD,
    "paddle3d_p0_pretrained_eval": CLOUD,
    "paddlespeech_p0_pretrained_eval": CLOUD,
    "paddledetection_p0_pretrained_eval": CLOUD,
    "paddleseg_p0_pretrained_eval": CLOUD,
    "paddlenlp_p0_pretrained_eval": CLOUD,
    "paddleslim_p0_pretrained_eval": CLOUD,
    "paddlerec_p0_pretrained_eval": CLOUD,

    #重要模型 小数据集精度
    "paddleclas_p0_precision": CLOUD,
    "paddlegan_p0_precision": CLOUD,
    "paddleocr_p0_precision": CLOUD,
    "paddle3d_p0_precision": CLOUD,
    "paddlespeech_p0_precision": CLOUD,
    "paddledetection_p0_precision": CLOUD,
    "paddleseg_p0_precision": CLOUD,
    "paddlenlp_p0_precision": CLOUD,
    "paddleslim_p0_precision": CLOUD,
    "paddlerec_p0_precision": CLOUD,

    #全量模型功能性
    "paddleclas_all_function": CLOUD,
    "paddlegan_all_function": CLOUD,
    "paddleocr_all_function": CLOUD,
    "paddle3d_all_function": CLOUD,
    "paddlespeech_all_function": CLOUD,
    "paddledetection_all_function": CLOUD,
    "paddleseg_all_function": CLOUD,
    "paddlenlp_all_function": CLOUD,
    "paddleslim_all_function": CLOUD,
    "paddlerec_all_function": CLOUD,

    #全量模型 预训练模型评估、推理、预测精度
    "paddleclas_all_pretrained_eval": CLOUD,
    "paddlegan_all_pretrained_eval": CLOUD,
    "paddleocr_all_pretrained_eval": CLOUD,
    "paddle3d_all_pretrained_eval": CLOUD,
    "paddlespeech_all_pretrained_eval": CLOUD,
    "paddledetection_all_pretrained_eval": CLOUD,
    "paddleseg_all_pretrained_eval": CLOUD,
    "paddlenlp_all_pretrained_eval": CLOUD,
    "paddleslim_all_pretrained_eval": CLOUD,
    "paddlerec_all_pretrained_eval": CLOUD,

    #全量模型 小数据集精度
    "paddleclas_all_precision": CLOUD,
    "paddlegan_all_precision": CLOUD,
    "paddleocr_all_precision": CLOUD,
    "paddle3d_all_precision": CLOUD,
    "paddlespeech_all_precision": CLOUD,
    "paddledetection_all_precision": CLOUD,
    "paddleseg_all_precision": CLOUD,
    "paddlenlp_all_precision": CLOUD,
    "paddleslim_all_precision": CLOUD,
    "paddlerec_all_precision": CLOUD,
    
    # model benchmark
    "models_benchmark_v100_single_dp": LOCAL,
    "models_benchmark_v100_single_dp_test": LOCAL,
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
    MODEL_BENCHMARK = "23601"

    # 原生推理
    NATIVE_INFER = "24293"
    # TRT推理
    TRT_INFER = "24296"
    # MKLDNN推理
    MKLDNN_INFER = "24297"

    # 模型
    #重要模型功能性
    PaddleClas_P0_Function = "25246", {"reponame": "PaddleClas", 
        "priority": "P0", 
        "mode": "function", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}
    PaddleGAN_P0_Function = "25246", {"reponame": "PaddleGAN", 
        "priority": "P0", 
        "mode": "function", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}
    PaddleOCR_P0_Function = "25246", {"reponame": "PaddleOCR", 
        "models_branch": "dygraph", 
        "priority": "P0", 
        "mode": "function", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}
    Paddle3D_P0_Function = "25246", {"reponame": "Paddle3D", 
        "priority": "P0", 
        "mode": "function", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}
    PaddleSpeech_P0_Function = "25246", {"reponame": "PaddleSpeech", 
        "priority": "P0", 
        "mode": "function", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}
    PaddleDetection_P0_Function = "25246", {"reponame": "PaddleDetection", 
        "priority": "P0", 
        "mode": "function", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}
    PaddleSeg_P0_Function = "25246", {"reponame": "PaddleSeg", 
        "priority": "P0", 
        "mode": "function", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}
    PaddleNLP_P0_Function = "25246", {"reponame": "PaddleNLP", 
        "priority": "P0", 
        "mode": "function", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}
    PaddleSlim_P0_Function = "25246", {"reponame": "PaddleSlim", 
        "priority": "P0Precision", 
        "mode": "function", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}
    PaddleRec_P0_Function = "25246", {"reponame": "PaddleRec", 
        "models_branch": "master", 
        "priority": "P0Precision", 
        "mode": "function", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}

    #重要模型 预训练模型评估、推理、预测精度
    PaddleClas_P0_Pretrained_Eval = "25246", {"reponame": "PaddleClas", 
        "priority": "P0", 
        "mode": "precison", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step":"eval:pretrained+infer:pretrained+export:pretrained+predict:pretrained"}
    PaddleGAN_P0_Pretrained_Eval = "25246", {"reponame": "PaddleGAN", 
        "priority": "P0", 
        "mode": "precison", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step":"eval:pretrained+infer:pretrained+export:pretrained+predict:pretrained"}
    PaddleOCR_P0_Pretrained_Eval = "25246", {"reponame": "PaddleOCR", 
        "models_branch": "dygraph", 
        "priority": "P0", 
        "mode": "precison", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step":"eval:pretrained+infer:pretrained+export:pretrained+predict:pretrained"}
    Paddle3D_P0_Pretrained_Eval = "25246", {"reponame": "Paddle3D", 
        "priority": "P0", 
        "mode": "precison", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step":"eval:pretrained+infer:pretrained+export:pretrained+predict:pretrained"}
    PaddleSpeech_P0_Pretrained_Eval = "25246", {"reponame": "PaddleSpeech", 
        "priority": "P0", 
        "mode": "precison", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step":"eval:pretrained+infer:pretrained+export:pretrained+predict:pretrained"}
    PaddleDetection_P0_Pretrained_Eval = "25246", {"reponame": "PaddleDetection", 
        "priority": "P0", 
        "mode": "precison", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step":"eval:pretrained+infer:pretrained+export:pretrained+predict:pretrained"}
    PaddleSeg_P0_Pretrained_Eval = "25246", {"reponame": "PaddleSeg", 
        "priority": "P0", 
        "mode": "precison", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step":"eval:pretrained+infer:pretrained+export:pretrained+predict:pretrained"}
    PaddleNLP_P0_Pretrained_Eval = "25246", {"reponame": "PaddleNLP", 
        "priority": "P0", 
        "mode": "precison", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step":"eval:pretrained+infer:pretrained+export:pretrained+predict:pretrained"}
    PaddleSlim_P0_Pretrained_Eval = "25246", {"reponame": "PaddleSlim", 
        "priority": "P0Precision", 
        "mode": "precison", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step":"eval:pretrained+infer:pretrained+export:pretrained+predict:pretrained"}
    PaddleRec_P0_Pretrained_Eval = "25246", {"reponame": "PaddleRec", 
        "models_branch": "master", 
        "priority": "P0Precision", 
        "mode": "precison", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step":"eval:pretrained+infer:pretrained+export:pretrained+predict:pretrained"}

    #重要模型 小数据集精度
    PaddleClas_P0_Precision = "25246", {"reponame": "PaddleClas", 
        "priority": "P0", 
        "mode": "precision", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}
    PaddleGAN_P0_Precision = "25246", {"reponame": "PaddleGAN", 
        "priority": "P0", 
        "mode": "precision", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}
    PaddleOCR_P0_Precision = "25246", {"reponame": "PaddleOCR", 
        "models_branch": "dygraph", 
        "priority": "P0", 
        "mode": "precision", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}
    Paddle3D_P0_Precision = "25246", {"reponame": "Paddle3D", 
        "priority": "P0", 
        "mode": "precision", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}
    PaddleSpeech_P0_Precision = "25246", {"reponame": "PaddleSpeech", 
        "priority": "P0", 
        "mode": "precision", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}
    PaddleDetection_P0_Precision = "25246", {"reponame": "PaddleDetection", 
        "priority": "P0", 
        "mode": "precision", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}
    PaddleSeg_P0_Precision = "25246", {"reponame": "PaddleSeg", 
        "priority": "P0", 
        "mode": "precision", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}
    PaddleNLP_P0_Precision = "25246", {"reponame": "PaddleNLP", 
        "priority": "P0", 
        "mode": "precision", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}
    PaddleSlim_P0_Precision = "25246", {"reponame": "PaddleSlim", 
        "priority": "P0Precision", 
        "mode": "precision", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}
    PaddleRec_P0_Precision = "25246", {"reponame": "PaddleRec", 
        "models_branch": "master", 
        "priority": "P0Precision", 
        "mode": "precision", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}

    #全量模型功能性
    PaddleClas_ALL_Function = "25246", {"reponame": "PaddleClas", 
        "priority": "ALL", 
        "mode": "function", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}
    PaddleGAN_ALL_Function = "25246", {"reponame": "PaddleGAN", 
        "priority": "ALL", 
        "mode": "function", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}
    PaddleOCR_ALL_Function = "25246", {"reponame": "PaddleOCR", 
        "models_branch": "dygraph", 
        "priority": "ALL", 
        "mode": "function", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}
    Paddle3D_ALL_Function = "25246", {"reponame": "Paddle3D", 
        "priority": "ALL", 
        "mode": "function", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}
    PaddleSpeech_ALL_Function = "25246", {"reponame": "PaddleSpeech", 
        "priority": "ALL", 
        "mode": "function", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}
    PaddleDetection_ALL_Function = "25246", {"reponame": "PaddleDetection", 
        "priority": "ALL", 
        "mode": "function", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}
    PaddleSeg_ALL_Function = "25246", {"reponame": "PaddleSeg", 
        "priority": "ALL", 
        "mode": "function", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}
    PaddleNLP_ALL_Function = "25246", {"reponame": "PaddleNLP", 
        "priority": "ALL", 
        "mode": "function", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}
    PaddleSlim_ALL_Function = "25246", {"reponame": "PaddleSlim", 
        "priority": "ALLPrecision", 
        "mode": "function", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}
    PaddleRec_ALL_Function = "25246", {"reponame": "PaddleRec", 
        "models_branch": "master", 
        "priority": "ALLPrecision", 
        "mode": "function", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}

    #全量模型 预训练模型评估、推理、预测精度
    PaddleClas_ALL_Pretrained_Eval = "25246", {"reponame": "PaddleClas", 
        "priority": "ALL", 
        "mode": "precison", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step":"eval:pretrained+infer:pretrained+export:pretrained+predict:pretrained"}
    PaddleGAN_ALL_Pretrained_Eval = "25246", {"reponame": "PaddleGAN", 
        "priority": "ALL", 
        "mode": "precison", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step":"eval:pretrained+infer:pretrained+export:pretrained+predict:pretrained"}
    PaddleOCR_ALL_Pretrained_Eval = "25246", {"reponame": "PaddleOCR", 
        "models_branch": "dygraph", 
        "priority": "ALL", 
        "mode": "precison", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step":"eval:pretrained+infer:pretrained+export:pretrained+predict:pretrained"}
    Paddle3D_ALL_Pretrained_Eval = "25246", {"reponame": "Paddle3D", 
        "priority": "ALL", 
        "mode": "precison", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step":"eval:pretrained+infer:pretrained+export:pretrained+predict:pretrained"}
    PaddleSpeech_ALL_Pretrained_Eval = "25246", {"reponame": "PaddleSpeech", 
        "priority": "ALL", 
        "mode": "precison", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step":"eval:pretrained+infer:pretrained+export:pretrained+predict:pretrained"}
    PaddleDetection_ALL_Pretrained_Eval = "25246", {"reponame": "PaddleDetection", 
        "priority": "ALL", 
        "mode": "precison", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step":"eval:pretrained+infer:pretrained+export:pretrained+predict:pretrained"}
    PaddleSeg_ALL_Pretrained_Eval = "25246", {"reponame": "PaddleSeg", 
        "priority": "ALL", 
        "mode": "precison", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step":"eval:pretrained+infer:pretrained+export:pretrained+predict:pretrained"}
    PaddleNLP_ALL_Pretrained_Eval = "25246", {"reponame": "PaddleNLP", 
        "priority": "ALL", 
        "mode": "precison", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step":"eval:pretrained+infer:pretrained+export:pretrained+predict:pretrained"}
    PaddleSlim_ALL_Pretrained_Eval = "25246", {"reponame": "PaddleSlim", 
        "priority": "ALLPrecision", 
        "mode": "precison", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step":"eval:pretrained+infer:pretrained+export:pretrained+predict:pretrained"}
    PaddleRec_ALL_Pretrained_Eval = "25246", {"reponame": "PaddleRec", 
        "models_branch": "master", 
        "priority": "ALLPrecision", 
        "mode": "precison", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step":"eval:pretrained+infer:pretrained+export:pretrained+predict:pretrained"}

    #全量模型 小数据集精度
    PaddleClas_ALL_Precision = "25246", {"reponame": "PaddleClas", 
        "priority": "ALL", 
        "mode": "precision", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}
    PaddleGAN_ALL_Precision = "25246", {"reponame": "PaddleGAN", 
        "priority": "ALL", 
        "mode": "precision", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}
    PaddleOCR_ALL_Precision = "25246", {"reponame": "PaddleOCR", 
        "models_branch": "dygraph", 
        "priority": "ALL", 
        "mode": "precision", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}
    Paddle3D_ALL_Precision = "25246", {"reponame": "Paddle3D", 
        "priority": "ALL", 
        "mode": "precision", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}
    PaddleSpeech_ALL_Precision = "25246", {"reponame": "PaddleSpeech", 
        "priority": "ALL", 
        "mode": "precision", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}
    PaddleDetection_ALL_Precision = "25246", {"reponame": "PaddleDetection", 
        "priority": "ALL", 
        "mode": "precision", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}
    PaddleSeg_ALL_Precision = "25246", {"reponame": "PaddleSeg", 
        "priority": "ALL", 
        "mode": "precision", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}
    PaddleNLP_ALL_Precision = "25246", {"reponame": "PaddleNLP", 
        "priority": "ALL", 
        "mode": "precision", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}
    PaddleSlim_ALL_Precision = "25246", {"reponame": "PaddleSlim", 
        "priority": "ALLPrecision", 
        "mode": "precision", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}
    PaddleRec_ALL_Precision = "25246", {"reponame": "PaddleRec", 
        "models_branch": "master", 
        "priority": "ALLPrecision", 
        "mode": "precision", 
        "system": "linux", 
        "binary_search_flag": "True", 
        "step": "train:all+eval:all+infer:all+export:all+predict:all"}

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
    MODELS_BENCHMARK_V100_SINGLE_DP_TEST = "http://10.138.35.185:8989/auto_test/", \
        {"device_type": "V100", "cards_type_list": "N1C1,N1C8", "run_mode_list": "DP",
         "model_priority_list": "S_P0", "test_name": "V100单机性能测试（Demo）", "test_demo": True}
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
        # infer
        "native_infer": Cloud.NATIVE_INFER,
        "trt_infer": Cloud.TRT_INFER,
        "mkldnn_infer": Cloud.MKLDNN_INFER,

        # module
        #重要模型功能性
        "paddleclas_p0_function": Cloud.PaddleClas_P0_Function,
        "paddlegan_p0_function": Cloud.PaddleGAN_P0_Function,
        "paddleocr_p0_function": Cloud.PaddleOCR_P0_Function,
        "paddle3d_p0_function": Cloud.Paddle3D_P0_Function,
        "paddlespeech_p0_function": Cloud.PaddleSpeech_P0_Function,
        "paddledetection_p0_function": Cloud.PaddleDetection_P0_Function,
        "paddleseg_p0_function": Cloud.PaddleSeg_P0_Function,
        "paddlenlp_p0_function": Cloud.PaddleNLP_P0_Function,
        "paddleslim_p0_function": Cloud.PaddleSlim_P0_Function,
        "paddlerec_p0_function": Cloud.PaddleRec_P0_Function,

        #重要模型 预训练模型评估、推理、预测精度
        "paddleclas_p0_pretrained_eval": Cloud.PaddleClas_P0_Pretrained_Eval,
        "paddlegan_p0_pretrained_eval": Cloud.PaddleGAN_P0_Pretrained_Eval,
        "paddleocr_p0_pretrained_eval": Cloud.PaddleOCR_P0_Pretrained_Eval,
        "paddle3d_p0_pretrained_eval": Cloud.Paddle3D_P0_Pretrained_Eval,
        "paddlespeech_p0_pretrained_eval": Cloud.PaddleSpeech_P0_Pretrained_Eval,
        "paddledetection_p0_pretrained_eval": Cloud.PaddleDetection_P0_Pretrained_Eval,
        "paddleseg_p0_pretrained_eval": Cloud.PaddleSeg_P0_Pretrained_Eval,
        "paddlenlp_p0_pretrained_eval": Cloud.PaddleNLP_P0_Pretrained_Eval,
        "paddleslim_p0_pretrained_eval": Cloud.PaddleSlim_P0_Pretrained_Eval,
        "paddlerec_p0_pretrained_eval": Cloud.PaddleRec_P0_Pretrained_Eval,

        #重要模型 小数据集精度
        "paddleclas_p0_precision": Cloud.PaddleClas_P0_Precision,
        "paddlegan_p0_precision": Cloud.PaddleGAN_P0_Precision,
        "paddleocr_p0_precision": Cloud.PaddleOCR_P0_Precision,
        "paddle3d_p0_precision": Cloud.Paddle3D_P0_Precision,
        "paddlespeech_p0_precision": Cloud.PaddleSpeech_P0_Precision,
        "paddledetection_p0_precision": Cloud.PaddleDetection_P0_Precision,
        "paddleseg_p0_precision": Cloud.PaddleSeg_P0_Precision,
        "paddlenlp_p0_precision": Cloud.PaddleNLP_P0_Precision,
        "paddleslim_p0_precision": Cloud.PaddleSlim_P0_Precision,
        "paddlerec_p0_precision": Cloud.PaddleRec_P0_Precision,

        #全量模型功能性
        "paddleclas_all_function": Cloud.PaddleClas_ALL_Function,
        "paddlegan_all_function": Cloud.PaddleGAN_ALL_Function,
        "paddleocr_all_function": Cloud.PaddleOCR_ALL_Function,
        "paddle3d_all_function": Cloud.Paddle3D_ALL_Function,
        "paddlespeech_all_function": Cloud.PaddleSpeech_ALL_Function,
        "paddledetection_all_function": Cloud.PaddleDetection_ALL_Function,
        "paddleseg_all_function": Cloud.PaddleSeg_ALL_Function,
        "paddlenlp_all_function": Cloud.PaddleNLP_ALL_Function,
        "paddleslim_all_function": Cloud.PaddleSlim_ALL_Function,
        "paddlerec_all_function": Cloud.PaddleRec_ALL_Function,

        #全量模型 预训练模型评估、推理、预测精度
        "paddleclas_all_pretrained_eval": Cloud.PaddleClas_ALL_Pretrained_Eval,
        "paddlegan_all_pretrained_eval": Cloud.PaddleGAN_ALL_Pretrained_Eval,
        "paddleocr_all_pretrained_eval": Cloud.PaddleOCR_ALL_Pretrained_Eval,
        "paddle3d_all_pretrained_eval": Cloud.Paddle3D_ALL_Pretrained_Eval,
        "paddlespeech_all_pretrained_eval": Cloud.PaddleSpeech_ALL_Pretrained_Eval,
        "paddledetection_all_pretrained_eval": Cloud.PaddleDetection_ALL_Pretrained_Eval,
        "paddleseg_all_pretrained_eval": Cloud.PaddleSeg_ALL_Pretrained_Eval,
        "paddlenlp_all_pretrained_eval": Cloud.PaddleNLP_ALL_Pretrained_Eval,
        "paddleslim_all_pretrained_eval": Cloud.PaddleSlim_ALL_Pretrained_Eval,
        "paddlerec_all_pretrained_eval": Cloud.PaddleRec_ALL_Pretrained_Eval,

        #全量模型 小数据集精度
        "paddleclas_all_precision": Cloud.PaddleClas_ALL_Precision,
        "paddlegan_all_precision": Cloud.PaddleGAN_ALL_Precision,
        "paddleocr_all_precision": Cloud.PaddleOCR_ALL_Precision,
        "paddle3d_all_precision": Cloud.Paddle3D_ALL_Precision,
        "paddlespeech_all_precision": Cloud.PaddleSpeech_ALL_Precision,
        "paddledetection_all_precision": Cloud.PaddleDetection_ALL_Precision,
        "paddleseg_all_precision": Cloud.PaddleSeg_ALL_Precision,
        "paddlenlp_all_precision": Cloud.PaddleNLP_ALL_Precision,
        "paddleslim_all_precision": Cloud.PaddleSlim_ALL_Precision,
        "paddlerec_all_precision": Cloud.PaddleRec_ALL_Precision
    }


class LocalMission(object):
    """
    for local testing
    """
    ROUTER = {
        # benchmark
        "models_benchmark_v100_single_dp": Local.MODELS_BENCHMARK_V100_SINGLE_DP,
        "models_benchmark_v100_single_dp_test": Local.MODELS_BENCHMARK_V100_SINGLE_DP_TEST,
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


if 'DEPLOYMENT_TYPE' in os.environ and os.environ['DEPLOYMENT_TYPE'].upper() == 'GRAY':
    # ALLURE 相关 , 需提前准备环境
    REPORT_SOURCE_NAME = "/home/work/afs/pts/pts_report.tar"
    WWW_DIR = "/home/work/afs/pts/report/"
    SOURCE_DIR = "/home/work/afs/pts/source/"
    ALLURE = "/home/work/allure/bin/allure"
    REPORT_SERVER = "http://paddleboard.baidu-int.com:8081/report/"
elif 'DEPLOYMENT_TYPE' in os.environ:
    # ALLURE 相关 , 需提前准备环境
    REPORT_SOURCE_NAME = "pts_report.tar"
    WWW_DIR = "/ssd1/pts/report/"
    SOURCE_DIR = "/ssd1/pts/source/"
    ALLURE = "/ssd1/pts/tools/allure/bin/allure"
    REPORT_SERVER = "http://10.144.31.29:8333/"
else:
    # ALLURE 相关 , 需提前准备环境
    REPORT_SOURCE_NAME = "pts_report.tar"
    WWW_DIR = "/ssd1/pts/report/"
    SOURCE_DIR = "/ssd1/pts/source/"
    ALLURE = "/ssd1/pts/tools/allure/bin/allure"
    REPORT_SERVER = "http://10.144.31.29:8333/"

