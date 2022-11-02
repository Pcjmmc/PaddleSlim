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
        data = {
            "username": self._cookies.get("username"),
            "returnFields": "imageUrl,departmentName,email",
            "timestamp": int(time.time()),
            "appKey": APP_KEY,
            "sRandom": str(uuid.uuid1())
        }
        sign = AuthCheck.get_sign(data)
        data["sign"] = sign
        res = await GetUserInfo(data).get_data()
        if res.get("code") == 200:
            # 如果不存在则新增，存在则更新
            user_info = res.get('result') or {}
            # 将user_info 的头像替换成hi头像
            username = user_info.get("username")
            user_info["imageUrl"]="https://eefe.baidu-int.com/avatars/{}".format(username)
            email = user_info.get("email")
            departmentName = user_info.get("departmentName")
            _res = await User().aio_get_object(**{"username": username})
            if _res:
                userid = _res.id
                await User().aio_update(
                    validated_data={"username": username, "email": email, "departmentName": departmentName},
                    params_data={"id": userid}
                )
            else:
                _, userid = await User().aio_insert(
                    validated_data={"username": username, "email": email, "departmentName": departmentName}
                )
            user_info.update({"userid": userid})
            return 1, user_info
        
        return 0, {}
            
