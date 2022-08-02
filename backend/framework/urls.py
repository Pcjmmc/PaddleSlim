# encoding: utf-8
"""
URL 配置
"""
from framework.views import TestView
from framework.job_view import JobInitView
from framework.dispatcher_view import DispatcherView
from framework.runner import RunnerView
from framework.runner_xly import RunnerXLY
from framework.mission_callback import MissionCallback
from framework.compile_callback import CompileCallback
from urls import url

urlpatterns = [
    # 传入task_type_id, 同时body中存放case detail详情； post请求
    url(r'test/?$', TestView),
    url(r'jobinit/?$', JobInitView),
    url(r'dispatcher/?$', DispatcherView),
    url(r'runner/?$', RunnerView),
    url(r'runnerxly/?$', RunnerXLY),
    url(r'missioncallback/?$', MissionCallback),
    url(r'compilecallback/?$', CompileCallback),
]
