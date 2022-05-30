# encoding: utf-8
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
        "ROCM"
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

# 环境列表
system_list = {
    # compile是一个全量的，其他块自己按环境重要程度排序
    'compile': [ 
        'Linux_Gpu_Cuda10.2', 'Linux_Gpu_Cuda11.0',
        'Linux_Gpu_Cuda10.1', 'Linux_Gpu_Cuda11.1', 
        'Linux_Gpu_Cuda11.2','Linux_Gpu_Cuda11.3',
        'Linux_Gpu(T4)_Cuda10.2', 'Linux_Gpu(T4)_Cuda11.1',
        'Linux_Gpu(T4)_Cuda11.2', 'Linux-Jetpack', 'Xpu',
        'Linux_ROCM', 'Linux_Cpu', 'Windows_GPU_2080',
        'Windows_GPU_3080', 'Npu', 'Windows_Cpu', 'Mac'],
    'model': [
        'Linux_Gpu_Cuda10.2', 'Linux_Gpu_Cuda11.0',
        'Linux_Gpu_Cuda10.1', 'Linux_Gpu_Cuda11.1', 
        'Linux_Gpu_Cuda11.2','Linux_Gpu_Cuda11.3',
        'Linux_Gpu(T4)_Cuda10.2', 'Linux_Gpu(T4)_Cuda11.1',
        'Linux_Gpu(T4)_Cuda11.2', 'Linux-Jetpack', 'Xpu',
        'Linux_ROCM', 'Linux_Cpu', 'Windows_GPU_2080',
        'Windows_GPU_3080', 'Npu', 'Mac', 'Windows_Cpu'
    ],
    'dist': [
        'Linux_Gpu_Cuda11.0', 'Linux_Gpu_Cuda10.2',
        'Linux_Gpu_Cuda10.1', 'Linux_Gpu_Cuda11.1', 
        'Linux_Gpu_Cuda11.2','Linux_Gpu_Cuda11.3',
        'Linux_Gpu(T4)_Cuda10.2', 'Linux_Gpu(T4)_Cuda11.1',
        'Linux_Gpu(T4)_Cuda11.2', 'Linux-Jetpack', 'Xpu',
        'Linux_ROCM', 'Linux_Cpu', 'Windows_GPU_2080',
        'Windows_GPU_3080', 'Npu', 'Windows_Cpu', 'Mac'
    ],
    'benchmark': [
        'Linux_Gpu_Cuda11.2', 'Linux_Gpu_Cuda11.0', 
        'Linux_Gpu_Cuda10.2', 'Linux_Gpu_Cuda10.1', 
        'Linux_Gpu_Cuda11.1', 'Linux_Gpu_Cuda11.3',
        'Linux_Gpu(T4)_Cuda10.2', 'Linux_Gpu(T4)_Cuda11.1',
        'Linux_Gpu(T4)_Cuda11.2', 'Linux-Jetpack', 'Xpu',
        'Linux_ROCM', 'Linux_Cpu', 'Windows_GPU_2080',
        'Windows_GPU_3080', 'Npu', 'Windows_Cpu', 'Mac'
    ]
}
