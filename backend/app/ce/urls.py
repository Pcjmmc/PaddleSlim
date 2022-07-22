# -*- coding:utf8 -*-
"""
URL 配置
"""
from app.ce.benchmark.views import BenchmarkManage
from app.ce.bug.views import BugManage, ConclusionManage
from app.ce.commit.views import CommitDetailManage, CommitsManage
from app.ce.config.views import ScenesManage
from app.ce.detail.views import DetailManage
from app.ce.develop.views import DevelopVersionManage
from app.ce.job.views import JobManage
from app.ce.menu.views import MenuManage
from app.ce.release.exempt_views import ExemptManege
from app.ce.release.views import ReleaseVersionManage, TaskManage

from urls import url

urlpatterns = [
    url(r'menu', MenuManage),
    url(r'release/exempt', ExemptManege),
    url(r'release/?$', ReleaseVersionManage),
    url(r'task/?$', TaskManage),
    url(r'job/?$', JobManage),
    url(r'config/scenes', ScenesManage),
    url(r'commits', CommitsManage),
    url(r'commit/detail/?$', CommitDetailManage),
    url(r'bugs', BugManage),
    url(r'conclusion/?$', ConclusionManage),
    url(r'detail', DetailManage),
    url(r'develop/?$', DevelopVersionManage),
    url(r'op-benchmark/?$', BenchmarkManage),
]
