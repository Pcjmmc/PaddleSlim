# encoding: utf-8
"""
URL 配置
"""
from api.cache_views import BuildCacheView
from api.publish_views import PublishCacheView
from api.views import CaseDetailView
from urls import url

urlpatterns = [
    # 传入task_type_id, 同时body中存放case detail详情； post请求
    url(r'case/?$', CaseDetailView),
    url(r'cache/build/?$', BuildCacheView),
    url(r'publish/?$', PublishCacheView)
]
