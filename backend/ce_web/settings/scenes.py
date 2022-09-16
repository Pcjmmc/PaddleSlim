# encoding: utf-8

# icafe与集测平台的映射关系：
inner_dict = {
    "9239063": "单机训练", # 主框架CE任务
    "8738985": "套件工具兼容性", # 模型CE任务
    "11455195": "benchmark性能测试", # benchmark
    "11455197": "编译安装",
    "11455198": "文档教程",
    "11455199": "预测部署",
    "11455200": "分布式测试"
}

# 反向映射icafe
back_dict = {
    "compile": "编译",
    "frame": "单机训练",
    "model": "模型套件",
    "infer": "预测部署",
    "dist": "分布式",
    "benchmark": "benchmark",
    "doc": "文档测试"
}
selects = list(back_dict.values())

# 反向映射icafe
publish_origin_list = [
    "pypi/bos",
    "anaconda-cloud",
    "docker-hub"
]

scenes_dict = {
    "compile": "编译安装",
    "frame": "单机训练",
    "model": "套件工具兼容性",
    "infer": "预测部署",
    "dist": "分布式测试",
    "benchmark": "benchmark性能测试",
    "doc": "文档教程"
}
secondary_type = {
    "compile": [
        "训练-Linux",
        "训练-Windows",
        "训练-Mac",
        "预测-Linux",
        "预测-Linux-Jetson",
        "预测-Mac",
        "XPU2",
        "ROCM",
        "NPU"
    ],
    "frame": [
        "api功能测试",
        "动转静",
        "动态图",
        "静态图",
        "混合精度",
        "其它（自定义op）",
    ],
    "model": [
        "功能",
        "小数据集精度",
        "收敛性",
        "全链条",
        "plsc",
        "onnx"
    ],
    "infer": [
        "原生推理_C++_API",
        "原生推理_Python_API",
        "TensorRT推理_C++_API",
        "TensorRT推理_Python_API",
        "MKLDNN推理_Python_API",
        "厂内模型_C++_API"
    ],
    "dist": [
        "分布式api功能",
        "collective",
        "ps参数服务器",
        "FleetX"
    ],
    "benchmark": [
        "api",
        "op",
        "模型训练",
        "预测部署"
    ],
    "doc": [
        "API示例代码测试(中英文)",
        "使用指南测试",
        "应用实践案例测试",
        "教程测试",
        "安装命令测试",
        "安装包检测",
        "预测示例代码测试"
    ]
}

# 套件顺序
ORDER = {
    "PaddleClas": 1,
    "PaddleDetection": 2,
    "PaddleGAN": 3,
    "PaddleNLP": 4,
    "PaddleOCR": 5,
    "PaddleSeg": 6,
    "PaddleSlim": 7,
    "PaddleRec": 8,
    "PaddleSpeech": 9,
    "Paddle2ONNX": 10,
    "PaddleHub": 11,
    "other": 12
}
# compile是一个全量的，其他块自己按环境重要程度排序
system_list = {
    'compile': [
        'Linux_Gpu_Cuda10.2', 'Linux_Gpu_Cuda11.0',
        'Linux_Gpu_Cuda10.1', 'Linux_Gpu_Cuda11.1',
        'Linux_Gpu_Cuda11.2', 'Linux_Gpu_Cuda11.3',
        'Linux_Gpu_Cuda11.6', 'Linux_Gpu_Cuda11.7',
        'Linux_Gpu(T4)_Cuda10.2', 'Linux_Gpu(T4)_Cuda11.1',
        'Linux_Gpu(T4)_Cuda11.2', 'Linux-Jetpack', 'Xpu',
        'Windows_Gpu_Cuda10.1', 'Windows_Gpu_Cuda10.2',
        'Windows_Gpu_Cuda11.2', 'Windows_Gpu_Cuda11.0',
        'Windows_Gpu_Cuda11.1', 'Windows_Gpu_Cuda11.6',
        'Linux_ROCM', 'Linux_Cpu', 'Windows_GPU_2080',
        'Windows_GPU_3080', 'Npu', 'Windows_Cpu', 'Mac'],
    'model': [
        'Linux_Gpu_Cuda10.2', 'Linux_Gpu_Cuda11.0',
        'Linux_Gpu_Cuda10.1', 'Linux_Gpu_Cuda11.1',
        'Linux_Gpu_Cuda11.2', 'Linux_Gpu_Cuda11.3',
        'Linux_Gpu_Cuda11.6', 'Linux_Gpu_Cuda11.7',
        'Linux_Gpu(T4)_Cuda10.2', 'Linux_Gpu(T4)_Cuda11.1',
        'Linux_Gpu(T4)_Cuda11.2', 'Linux-Jetpack',
        'Linux_ROCM', 'Windows_GPU_2080', 'Windows_GPU_3080', 
        'Npu', 'Mac', 'Windows_Cpu', 'Linux_Cpu', 'Xpu'
    ],
    'dist': [
        'Linux_Gpu_Cuda11.0', 'Linux_Gpu_Cuda10.2',
        'Linux_Gpu_Cuda10.1', 'Linux_Gpu_Cuda11.1',
        'Linux_Gpu_Cuda11.2', 'Linux_Gpu_Cuda11.3',
        'Linux_Gpu_Cuda11.6', 'Linux_Gpu_Cuda11.7',
        'Linux_Gpu(T4)_Cuda10.2', 'Linux_Gpu(T4)_Cuda11.1',
        'Linux_Gpu(T4)_Cuda11.2', 'Linux-Jetpack', 'Xpu',
        'Linux_ROCM', 'Linux_Cpu', 'Windows_GPU_2080',
        'Windows_GPU_3080', 'Npu', 'Windows_Cpu', 'Mac'
    ],
    'benchmark': [
        'Linux_Gpu_Cuda11.2', 'Linux_Gpu_Cuda11.0',
        'Linux_Gpu_Cuda10.2', 'Linux_Gpu_Cuda10.1',
        'Linux_Gpu_Cuda11.1', 'Linux_Gpu_Cuda11.3',
        'Linux_Gpu_Cuda11.6', 'Linux_Gpu_Cuda11.7',
        'Linux_Gpu(T4)_Cuda10.2', 'Linux_Gpu(T4)_Cuda11.1',
        'Linux_Gpu(T4)_Cuda11.2', 'Linux-Jetpack', 'Xpu',
        'Linux_ROCM', 'Linux_Cpu', 'Windows_GPU_2080',
        'Windows_GPU_3080', 'Npu', 'Windows_Cpu', 'Mac'
    ]
}
