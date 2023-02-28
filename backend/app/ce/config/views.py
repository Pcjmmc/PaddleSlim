# encoding=utf-8
import asyncio
import datetime
import json
import time

from ce_web.settings.scenes import (
    back_dict, publish_origin_list,
    scenes_dict, secondary_type, system_list
)
from libs.mongo.db import Mongo
from views.auth_view import AuthCheck
from views.base_view import MABaseView


class ScenesManage(MABaseView):

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
        tempList = [val for key, val in system_list.items()]
        systemList = list()
        for item in tempList:
            systemList = list(set(systemList + item))
        systemList.sort()
        systemList = [{'key': item, 'desc': item} for item in systemList]
        data = {
            "taskTypeList": [],
            "sendTypeList": secondary_type,
            "systemList": systemList,
            "bugTypeList": back_dict,
            "publishOriginList": publish_origin_list

        }
        result = [{'key': key, 'desc': val} for key, val in scenes_dict.items()]
        data["taskTypeList"] = result
        return len(data), data

