# !/usr/bin/env python3
"""
实现打tag相关的逻辑
"""
# encoding=utf-8
import asyncio
import datetime
import json
import time

from ce_web.settings.common import STORAGE
from libs.mongo.db import Mongo

from views.base_view import MABaseView


class CreateTagManage(MABaseView):


    async def post(self, **kwargs):
        """
        调用基类的post方法，负责豁免的创建
        """
        return await super().post(**kwargs)


    async def post_data(self, **kwargs):
        """
        需要修改当前releaseVersion表中activated的tag名字保持跟前端（github的一致）；
        同时将当前的activated设置成False；
        将name修改成tag名；
        同时更新release表中该虚拟分支的end_time
        调用github接口打tag
        """
        pass
