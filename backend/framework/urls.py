# encoding: utf-8
"""
URL 配置
"""
from framework.views import TestView
from framework.job_view import JobInitView
from framework.job_list import JobList
from framework.job_details import JobDetails
from framework.mission_pkg.mission_callback import MissionCallback
from framework.compile_pkg.compile_callback import CompileCallback
from framework.mission_pkg.mission_failed import MissionFailed
from framework.mission_pkg.mission_rerun import MissionRerun
from framework.report_generator import ReportGenerator



from framework.compile_pkg.compile import CompileInit
from framework.compile_pkg.compile_search import CompileSearch
from framework.compile_pkg.compile_database import CompileDatabase

from framework.module_settings import ModuleSettingsView
from framework.settings import SettingsView

from framework.feedback.feedback import FeedBackView


from urls import url

urlpatterns = [
    # 传入task_type_id, 同时body中存放case detail详情； post请求
    url(r'test/?$', TestView),
    url(r'jobinit/?$', JobInitView),
    url(r'joblist/?$', JobList),
    url(r'jobdetails/?$', JobDetails),
    # 任务相关
    url(r'missioncallback/?$', MissionCallback),
    url(r'missionfailed/?$', MissionFailed),
    url(r'missionrerun/?$', MissionRerun),
    url(r'reportgenerator/?$', ReportGenerator),

    # 编译相关
    url(r'compile/?$', CompileInit),
    url(r'compile_search/?$', CompileSearch),
    url(r'compilecallback/?$', CompileCallback),
    url(r'compile_database/?$', CompileDatabase),


    # 配置相关
    url(r'getmodulesettings/?$', ModuleSettingsView),
    url(r'getsettings/?$', SettingsView),

    # 用户相关
    url(r'feedback/?$', FeedBackView),

]
