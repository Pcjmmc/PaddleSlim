# encoding=utf-8
import asyncio
import datetime
import json
import time

from ce_web.settings.common import STORAGE
from libs.mongo.db import Mongo

from views.auth_view import AuthCheck
from views.base_view import MABaseView


class MenuManage(MABaseView):

    auth_class = AuthCheck

    async def get(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().get(**kwargs)


    async def get_data(self, **kwargs):
        """
        响应请求, 实现获取数据逻辑, 并返回符合查询条件的数据
        """
        # print("get menu data by appid", kwargs)
        content = {
            "report": {
                "desc": '报告',
                "icon": 'ios-grid',
                "sub": {
                    "single": {"desc": '单个报告'},
                    "frame": {"desc": '框架天级'},
                    "model": {"desc": '模型天级'},
                    "frelease": {"desc": 'release回测'},
                    "fbenchmark": {"desc": 'api benchmark'},
                    "package": {"desc": '编包查询'}
                },
            "notMenu": False
            }
        }
        appid = kwargs.get("appid", 1)
        appname = kwargs.get("appname", "飞桨核心框架")
        table_name = "ce_menu_{appid}".format(appid=appid)
        menu_db = Mongo("paddle_quality", table_name)
        result = await menu_db.find_all()
        if result:
            menuDesc = result[0] if result else {}
            content = menuDesc.get('content', "")
            content = json.loads(content)
        return len(content), content

