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

from api_benchmark.apibm_view import ApiBenchmarkInitView
from api_benchmark.apibm_list import ApiBenchmarkList
from api_benchmark.apibm_details import ApiBenchmarkDetails
from api_benchmark.compare_pkg.main_compare import MainCompare
from api_benchmark.compare_pkg.base_compare import BaseCompare
from api_benchmark.apibm_pkg.apibm_rerun import ApiBenchmarkRerun
from api_benchmark.apibm_pkg.apibm_callback import ApiBenchmarkCallback
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

    # 触发效率云流水线
    url(r'api_benchmark/apibminitview/?$', ApiBenchmarkInitView),
    url(r'api_benchmark/apibmlist/?$', ApiBenchmarkList),
    url(r'api_benchmark/apibmdetails/?$', ApiBenchmarkDetails),
    url(r'api_benchmark/basecompare/?$', BaseCompare),

    # 暂未使用
    url(r'apibmrerun/?$', ApiBenchmarkRerun),
    url(r'apibmcallback/?$', ApiBenchmarkCallback),

    # 首页对比
    url(r'api_benchmark/maincompare/?$', MainCompare),
]
