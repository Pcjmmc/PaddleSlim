# -*- coding:utf8 -*-
"""
URL 配置
"""
from app.ce.benchmark.views import BenchmarkManage
from app.ce.bug.associate_views import AssociatedBugManage
from app.ce.bug.views import BugManage, ConclusionManage
from app.ce.build.views import BuildManage
from app.ce.commit.views import CommitDetailManage, CommitsManage
from app.ce.config.views import ScenesManage
from app.ce.detail.views import DetailManage
from app.ce.develop.views import DevelopVersionManage
from app.ce.job.views import JobManage
from app.ce.menu.views import MenuManage
from app.ce.publish.result_views import PublishResultManage
from app.ce.publish.views import PublishSummaryManage, PublishTaskManage
from app.ce.release.views import ReleaseVersionManage, TaskManage
from app.ce.tools.views import BinarySearchManage
from app.ce.user.views import UserInfoManage
from app.ce.ValidateToken.views import LogoutManage, ValidateManage
from app.ce.version.views import CreateRVersion
from app.ce.requirements.views import ManageIcafe

from urls import url

urlpatterns = [
    url(r'menu', MenuManage),
    url(r'release/?$', ReleaseVersionManage),
    url(r'publish/result/?$', PublishResultManage),
    url(r'publish/?$', PublishSummaryManage),
    url(r'publish_task/?$', PublishTaskManage),
    url(r'task/?$', TaskManage),
    url(r'job/?$', JobManage),
    url(r'config/scenes', ScenesManage),
    url(r'commits', CommitsManage),
    url(r'commit/detail/?$', CommitDetailManage),
    url(r'bugs/?$', BugManage),
    url(r'conclusion/?$', ConclusionManage),
    url(r'detail', DetailManage),
    url(r'develop/?$', DevelopVersionManage),
    url(r'op-benchmark/?$', BenchmarkManage),
    url(r'builds/?$', BuildManage),
    url(r'associated/bugs', AssociatedBugManage),
    url(r'tools/binarysearch', BinarySearchManage),
    url(r'version/?$', CreateRVersion),
    url(r'sTokenBackendValidate/?$', ValidateManage),
    url(r'user/?$', UserInfoManage),
    url(r'logout/?$', LogoutManage),
    url(r'requirments/icafe/?$', ManageIcafe)
]
