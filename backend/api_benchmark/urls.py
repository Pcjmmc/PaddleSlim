# encoding: utf-8
"""
URL 配置
"""
from api_benchmark.job import GetJob
from api_benchmark.compare import Compare
from api_benchmark.settings import GetSettings
from api_benchmark.cuda import GetCuda
from api_benchmark.os import GetOs
from api_benchmark.place import GetPlace
from api_benchmark.version import GetVersion
from urls import url

urlpatterns = [
    # 传入task_type_id, 同时body中存放case detail详情； post请求
    url(r'getjob/?$', GetJob),
    url(r'compare/?$', Compare),

    url(r'getsettings/?$', GetSettings),
    url(r'getos/?$', GetOs),
    url(r'getcuda/?$', GetCuda),
    url(r'getversion/?$', GetVersion),
    url(r'getplace/?$', GetPlace),
]
