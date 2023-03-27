# -*- coding:utf8 -*-
"""
程序的main方法, 启动的入口
"""
import asyncio
import datetime
import django
import os
import sys
import time

import tornado.web
from tornado.options import define, options

from ce_web.settings.common import DEPLOYMENT, WEB_SETTINGS
from ce_web.urls import urlpatterns
from libs.mysql.db import db_engines
from logger.logging_config import InitLogger
from urls import RegexURLPattern, RegexURLResolver
InitLogger().start()
from django.conf import settings
from django.core.wsgi import get_wsgi_application

def get_urlpatterns(urlpatterns):
    """
    组装路由信息
    """
    _urlpatterns = []
    for pattern in urlpatterns:
        if isinstance(pattern, RegexURLPattern):
            _urlpatterns.append(pattern.url)
        elif isinstance(pattern, RegexURLResolver):
            _urlpatterns.extend(pattern.url)
    return _urlpatterns


def debug_start_info():
    """
    debug log
    """
    print('%s' % datetime.datetime.now().strftime('%c'))
    print('Starting development server at http://%s:%s/' %
          ('127.0.0.1', options.port))
    print('Quit the server with CONTROL-C.\n')


class Application(tornado.web.Application):
    """
    自定义 app 类型，封装db engine和url模块
    """
    def __init__(self, _db_engines=None):
        self.db_engines = _db_engines
        self.handlers = get_urlpatterns(urlpatterns)

        app_settings = WEB_SETTINGS
        tornado.web.Application.__init__(self, self.handlers, **app_settings)

    def log_request(self, handler):
        """ Adds request metrics to the Prometheus export """
        super(Application, self).log_request(handler)


def define_application_config():
    """
    定义服务启动的配置信息
    """
    define("port", default=8000, help="run on the given port", type=int)
    define("db_engines", default=db_engines, help="db engines mapping", type=dict)
    define("model_classes", default=WEB_SETTINGS['model_classes'], help="model_classes mapping", type=dict)


if __name__ == "__main__":
    # 简单的启动django
    settings.configure(DEBUG=True)
    application = get_wsgi_application()
    define_application_config()
    
    tornado.options.parse_command_line()

    loop = asyncio.get_event_loop()
    app = Application(db_engines)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)

    if DEPLOYMENT == "DEV":
        debug_start_info()

    loop.run_forever()
