# encoding=utf-8
import asyncio
import datetime
import json
import time

from ce_web.settings.scenes import scenes_dict
from libs.mongo.db import Mongo

from views.base_view import MABaseView


class ScenesManage(MABaseView):

    async def get(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().get(**kwargs)


    async def get_data(self, **kwargs):
        """
        响应请求, 实现获取数据逻辑, 并返回符合查询条件的数据
        """
        result = [{'key': key, 'desc': val} for key, val in scenes_dict.items()]
        return len(result), result
