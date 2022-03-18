# -*- coding:utf8 -*-
"""
URL 配置
"""
from app.ce.commit.views import CommitDetailManage, CommitsManage
from app.ce.config.views import ScenesManage
from app.ce.job.views import JobManage
from app.ce.menu.views import MenuManage
from app.ce.release.exempt_views import ExemptManege
from app.ce.release.views import ReleaseVersionManage

from urls import url

urlpatterns = [
    url(r'menu', MenuManage),
    url(r'release/exempt', ExemptManege),
    url(r'release/?$', ReleaseVersionManage),
    url(r'job/?$', JobManage),
    url(r'config/scenes', ScenesManage),
    url(r'commits', CommitsManage),
    url(r'commit/detail/?$', CommitDetailManage),
]
