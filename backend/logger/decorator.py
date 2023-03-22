"""
定义case执行的装饰器
"""
# encoding: utf-8
import time
import asyncio
import copy
import json
import logging
import os
from functools import wraps

from logger.logging_config import InitLogger

InitLogger().start()

logger = logging.getLogger("ce")

def BaseLoggerInfo(func):
    @wraps(func)
    async def inner(*args, **kwargs):
        obj = args[0]
        headers = obj.headers
        fronted_url = headers.get("Originurl").split("#")[-1]
        begin_time = int(time.time())
        res = await func(*args, **kwargs)
        # 将结果返回给allure报告
        end_time = int(time.time())
        logger_data = {
            "banckend_func": obj.__class__.__name__,
            "method": obj.request.method,
            "uid": obj._cookies.get("userid"),
            # 前端访问页面路径
            "fronted_url": fronted_url,
            "response_time": end_time - begin_time
        }
        logger.info(logger_data)
    return inner


