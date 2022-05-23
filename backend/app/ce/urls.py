# -*- coding:utf8 -*-
"""
URL 配置
"""
from app.ce.bug.views import BugManage
from app.ce.commit.views import CommitDetailManage, CommitsManage
from app.ce.config.views import ScenesManage
from app.ce.detail.views import DetailManage
from app.ce.job.views import JobManage
from app.ce.menu.views import MenuManage
from app.ce.release.exempt_views import ExemptManege
from app.ce.release.views import TaskManage, ReleaseVersionManage
from app.ce.develop.views import DevelopVersionManage

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
    url(r'detail', DetailManage),
    url(r'develop/?$', DevelopVersionManage),
]
