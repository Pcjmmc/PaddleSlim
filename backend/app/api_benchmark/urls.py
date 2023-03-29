# encoding: utf-8
"""
URL 配置
"""
from app.api_benchmark.job import GetJob
from app.api_benchmark.compare import Compare
from app.api_benchmark.cuda import GetCuda
from app.api_benchmark.os import GetOs
from app.api_benchmark.place import GetPlace
from app.api_benchmark.version import GetVersion

from app.api_benchmark.settings import GetSettings

from app.api_benchmark.apibm_view import ApiBenchmarkInitView
from app.api_benchmark.apibm_list import ApiBenchmarkList
from app.api_benchmark.apibm_details import ApiBenchmarkDetails

from app.api_benchmark.compare_pkg.main_compare import MainCompare
from app.api_benchmark.compare_pkg.base_compare import BaseCompare

from app.api_benchmark.job_pkg.latest_routine_job import LatestRoutineJob
from app.api_benchmark.job_pkg.certain_job import CertainJob
from app.api_benchmark.job_pkg.baseline_job import BaselineJob

from app.api_benchmark.baseline_pkg.baseline_set import BaselineSet

from app.api_benchmark.apibm_pkg.apibm_rerun import ApiBenchmarkRerun
from app.api_benchmark.apibm_pkg.apibm_callback import ApiBenchmarkCallback
from urls import url

urlpatterns = [
    # 传入task_type_id, 同时body中存放case detail详情； post请求
    # url(r'getjob/?$', GetJob),
    # url(r'compare/?$', Compare),
    # url(r'getos/?$', GetOs),
    # url(r'getcuda/?$', GetCuda),
    # url(r'getversion/?$', GetVersion),
    # url(r'getplace/?$', GetPlace),

    # 暂未使用
    url(r'api_benchmark/apibmrerun/?$', ApiBenchmarkRerun),
    url(r'api_benchmark/apibmcallback/?$', ApiBenchmarkCallback),
    
    # 首页对比
    url(r'api_benchmark/maincompare/?$', MainCompare),
    
    # 执行页面
    url(r'api_benchmark/apibminitview/?$', ApiBenchmarkInitView),
    url(r'api_benchmark/apibmlist/?$', ApiBenchmarkList),
    url(r'api_benchmark/apibmdetails/?$', ApiBenchmarkDetails),
    
    # 执行页面基线设定
    url(r'api_benchmark/baselineset/?$', BaselineSet),
    
    # 执行页面、查询页面 对比
    url(r'api_benchmark/basecompare/?$', BaseCompare),
    
    # 任务获取
    url(r'api_benchmark/latestroutinejob/?$', LatestRoutineJob),
    url(r'api_benchmark/certainjob/?$', CertainJob),
    url(r'api_benchmark/baselinejob/?$', BaselineJob),
    
    # 查询页面选项获取
    url(r'api_benchmark/getsettings/?$', GetSettings),
]
