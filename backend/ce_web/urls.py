# -*- coding:utf8 -*-
"""
URL 配置
"""

from urls import url, include

urlpatterns = [
    # url(r'/oauth/', include(app.user.urls')), # 认证登录相关的信息。后续需要的话
    url(r'/ce/', include('app.ce.urls')),
    url(r'/api', include('api.urls')),
    url(r'/framework', include('app.framework.urls')),
    url(r'/benchmark', include('api_benchmark.urls'))
]
