# encoding: utf-8
"""
URL 配置
"""
from api.cache_views import BuildCacheView
from api.publish_views import PublishCacheView, UploadResultManage
from api.publish_binary import PublishBinaryInfo
from api.views import CaseDetailView
from api.hook_xly import HookxlyView
from urls import url

urlpatterns = [
    # 传入task_type_id, 同时body中存放case detail详情； post请求
    url(r'case/?$', CaseDetailView),
    url(r'xlyhook/?$', HookxlyView),
    url(r'cache/build/?$', BuildCacheView),
    url(r'publish/result/?$', UploadResultManage),
    url(r'publish/?$', PublishCacheView),
    url(r'publish/binary/?$', PublishBinaryInfo)
]
