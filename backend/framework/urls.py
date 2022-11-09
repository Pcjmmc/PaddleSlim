# encoding: utf-8
"""
URL 配置
"""
from framework.views import TestView
from framework.job_view import JobInitView
from framework.job_list import JobList
from framework.job_details import JobDetails
from framework.dispatcher_view import DispatcherView
from framework.settings import SettingsView
from framework.runner import RunnerView
from framework.runner_xly import RunnerXLY
from framework.mission_callback import MissionCallback
from framework.compile_callback import CompileCallback
from framework.report_generator import ReportGenerator
from framework.mission_info import MissionInfo
from framework.mission_failed import MissionFailed



from framework.compile import CompileInit
from framework.compile_search import CompileSearch

from urls import url

urlpatterns = [
    # 传入task_type_id, 同时body中存放case detail详情； post请求
    url(r'test/?$', TestView),
    url(r'jobinit/?$', JobInitView),
    url(r'joblist/?$', JobList),
    url(r'jobdetails/?$', JobDetails),
    url(r'dispatcher/?$', DispatcherView),
    url(r'getsettings/?$', SettingsView),
    url(r'runner/?$', RunnerView),
    url(r'runnerxly/?$', RunnerXLY),
    url(r'compilecallback/?$', CompileCallback),
    url(r'reportgenerator/?$', ReportGenerator),
    # 任务相关
    url(r'missionreport/?$', MissionInfo),
    url(r'missioncallback/?$', MissionCallback),
    url(r'missionfailed/?$', MissionFailed),

    # 编译相关
    url(r'compile/?$', CompileInit),
    url(r'compile_search/?$', CompileSearch),

]
