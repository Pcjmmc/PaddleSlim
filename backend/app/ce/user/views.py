# !/usr/bin/env python3
"""
负责user信息查出
"""
# encoding=utf-8
import asyncio
import datetime
import json
import time
import uuid

from ce_web.settings.common import APP_KEY
from models.user import User
from rpc.eac import GetUserInfo

from views.auth_view import AuthCheck
from views.base_view import MABaseView


class UserInfoManage(MABaseView):

    auth_class = AuthCheck

    async def get(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().get(**kwargs)


    async def get_data(self, **kwargs):
        """
        响应请求, 实现获取数据逻辑, 并返回符合查询条件的数据
        只需要根据库信息来查询即可
        """
        user_info = {}
        username = self._cookies.get("username")
        res = await User().aio_get_object(**{"username": username})
        # 拼接出用户信息
        if res:
            user_info = {
                "username": res.username,
                "email": res.email,
                "userid": res.id,
                "departmentName": res.departmentName,
                "imageUrl": "https://eefe.baidu-int.com/avatars/{}".format(username)
            }
        return 1, user_info

class UserIdentifyCheck(MABaseView):

    auth_class = AuthCheck
    
    async def get(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().get(**kwargs)


    async def get_data(self, **kwargs):
        """
        响应请求, 实现获取数据逻辑, 并返回符合查询条件的数据
        只需要根据库信息来查询即可
        """
        identifyQA = False
        username = self._cookies.get("username")
        res = await User().aio_get_object(**{"username": username})
        # 拼接出用户信息
        if res:
            identifyQA = res.departmentName == 'AI业务测试组'
        return 1, {'identifyQA': identifyQA}