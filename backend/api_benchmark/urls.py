# encoding: utf-8
"""
URL 配置
"""
from api_benchmark.version import GetVersion
from api_benchmark.compare import Compare

from urls import url

urlpatterns = [
    # 传入task_type_id, 同时body中存放case detail详情； post请求
    url(r'getversion/?$', GetVersion),
    url(r'compare/?$', Compare),

]
