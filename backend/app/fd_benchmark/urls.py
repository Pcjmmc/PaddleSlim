# encoding: utf-8
"""
URL 配置
"""

from app.fd_benchmark.fdbm_view import FDBenchmarkInitView
from app.fd_benchmark.compare.base_compare import BaseCompare
from app.fd_benchmark.query.get_missions import JobGetMission
from app.fd_benchmark.query.get_two_jobs_missions_id import TwoJobsMissionsId
from urls import url

urlpatterns = [
    # 执行页面
    url(r'fd_benchmark/fdbenchmarkinitview/?$', FDBenchmarkInitView),
    url(r'fd_benchmark/fdbenchmarkbasecompare/?$', BaseCompare),
    url(r'fd_benchmark/fdbenchmarkgetmissions/?$', JobGetMission),
    url(r'fd_benchmark/fdbenchmarkgettwojobsmissionsid/?$', TwoJobsMissionsId),
]
