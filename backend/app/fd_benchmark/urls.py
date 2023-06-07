# encoding: utf-8
"""
URL 配置
"""

from app.fd_benchmark.fdbm_view import FDBenchmarkInitView
from app.fd_benchmark.compare.base_compare import BaseCompare
from urls import url

urlpatterns = [
    # 执行页面
    url(r'fd_benchmark/fdbenchmarkinitview/?$', FDBenchmarkInitView),
    url(r'fd_benchmark/fdbenchmarkbasecompare/?$', BaseCompare),
]
