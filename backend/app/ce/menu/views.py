# encoding=utf-8
import asyncio
import datetime
import json
import time

from ce_web.settings.common import STORAGE
from libs.mongo.db import Mongo

from views.base_view import MABaseView


class MenuManage(MABaseView):

    async def get(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().get(**kwargs)


    async def get_data(self, **kwargs):
        """
        响应请求, 实现获取数据逻辑, 并返回符合查询条件的数据
        """
        table_name = "ce_menu"
        menu_db = Mongo("paddle_quality", table_name)
        result = await menu_db.find_all()
        menuDesc = result[0] if result else {}
        content = menuDesc.get('content', "")
        content = json.loads(content)
        return len(content), content

