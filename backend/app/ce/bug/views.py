# encoding=utf-8
import asyncio
import datetime
import json
import time

from ce_web.settings.common import RPC_SETTINGS
from ce_web.settings.scenes import scenes_dict
from libs.mongo.db import Mongo
from rpc.icafe import GetBug

from views.base_view import MABaseView

PADDLE_ICAFE_USER = RPC_SETTINGS['paddle_icafe']['username']
PADDLE_ICAFE_PASSD = RPC_SETTINGS['paddle_icafe']['password']
baseUrl = "https://console.cloud.baidu-int.com/devops/icafe/issue/{space}-{sequence}/show"

class BugManage(MABaseView):

    async def get(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().get(**kwargs)


    async def get_data(self, **kwargs):
        """
        响应请求, 实现获取数据逻辑, 并返回符合查询条件的数据
        """
        # 获取所有的bug卡片
        ptag = kwargs.get("tag", "v2.3.0-RC")
        ptag = "v2.3.0-RC"
        auto_tag = "auto_issue" # 创建一个自己的
        query = '所属计划 = 飞桨项目集/Paddle/{plan} AND auto_tag = {auto_tag}'.format(plan=ptag, auto_tag=auto_tag)
        result = await GetBug({'u': PADDLE_ICAFE_USER, 'pw': PADDLE_ICAFE_PASSD, 'iql': query}).get_data()
        bugData = result.get('cards', [])
        # 过滤下数据，太多了
        result = []
        for item in bugData:
            space = item.get('spacePrefixCode')
            sequence = item.get('sequence')
            level = "" 
            rd_owner = ""
            qa_owner = ""
            properties = item.get("properties", [])
            for arr in  properties:
                if arr.get("propertyName") == "优先级":
                    level = arr.get("displayValue")
                elif arr.get("propertyName") == "QA负责人":
                    qa_owner = arr.get("displayValue")
                elif arr.get("propertyName") == "RD负责人":
                    rd_owner = arr.get("displayValue")
            tmp = {
                "title": item.get("title"),
                "createdTime": item.get("createdTime"),
                "status": item.get("status"),
                "url": baseUrl.format(space=space, sequence=sequence),
                "level": level,
                "rd_owner": rd_owner,
                "qa_owner": qa_owner
            }
            result.append(tmp)
        return len(result), result

    async def post(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().post(**kwargs)


    async def post_data(self, **kwargs):
        """
        响应请求, 实现获取数据逻辑, 并返回符合查询条件的数据
        """
        # 图片列表
        file_list = self.request.files
        # 其他字段
        print("kwargs", kwargs)
        pass

