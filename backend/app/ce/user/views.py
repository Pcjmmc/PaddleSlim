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
            "returnFields": "imageUrl,departmentName",
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
            username = user_info.get("username")
            email = user_info.get("email")
            departmentName = user_info.get("departmentName")
            res = await User().aio_get_object(**{"username": username})
            if res:
                await User().aio_update(
                    validated_data={"username": username, "email": email, "departmentName": departmentName},
                    params_data={"id": res.id}
                )
            else:
                await User().aio_insert(
                    validated_data={"username": username, "email": email, "departmentName": departmentName}
                )

            return 1, user_info
        
        return 0, {}
            