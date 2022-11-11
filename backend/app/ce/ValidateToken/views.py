# !/usr/bin/env python3
# encoding=utf-8
import asyncio
import datetime
import hashlib
import json
import time
import urllib
import uuid

import tornado.web
from ce_web.settings.common import (APP_KEY, BASE_URL, DEFAULT_URL, EAC_HOST,
                                    PTOKEN, UUAP_SECRET_KEY)
from https import response as resp
from models.user import User
from rpc.eac import GetStoken, GetUserInfo

from views.auth_view import AuthCheck
from views.base_view import MABaseView


class ValidateManage(tornado.web.RequestHandler):

    async def get(self):
        """
        响应请求, 实现获取数据逻辑, 并返回符合查询条件的数据
        """
        kwargs = {name: self.get_argument(name) for name in self.request.arguments}
        # 获取所有的bug卡片, 根据plan tag 和 类型来查询
        originalUrl = kwargs.get('originalUrl')
        ticket = kwargs.get('ticket')
        # 将ticket 设置到cookie，并存在前端
        # 置换成sToken再种植到cookie
        data = {
            "encryptedSToken": ticket,
            "appKey": APP_KEY,
            "timestamp": int(time.time()),
        }
        sign = AuthCheck.get_sign(data)
        data["sign"] = sign
        res = await GetStoken(data).get_data()
        if res.get("code") == 200:
            UUAP_S_TOKEN = res.get("result")
            self.set_cookie('UUAP_S_TOKEN', UUAP_S_TOKEN)
        return self.redirect(originalUrl)


class LogoutManage(tornado.web.RequestHandler):

    async def get(self, **kwargs):
        """
        响应请求, 实现登出操作TODO
        """
        originalUrl = self.request.headers.get("Originurl") or DEFAULT_URL
        # 获取所有的bug卡片, 根据plan tag 和 类型来查询
        url = '%s/logout?service=%s&appKey=%s&version=v2'
        url = url % (EAC_HOST, urllib.parse.quote(originalUrl),  APP_KEY)
        # 清理cookie
        self.clear_cookie(PTOKEN)
        # 返回40001
        return resp.return_redirect_response(self, resp.HTTP_4001_INTERNAL_SERVER_ERROR, new_url=url)

class CheckManage(tornado.web.RequestHandler):

    async def get(self, **kwargs):
        """
        调用基类的get方法
        """
        _cookies = self.request.cookies
        cookies = {}
        for name in _cookies:
            cookies[name] = self.get_cookie(name)
        need_redirect, sed_params = await AuthCheck.check_auth(
            cookies, self.request.headers
        )
        if need_redirect:
            # 返回正常，让前端重新location
            return resp.return_redirect_response(self, resp.HTTP_4001_INTERNAL_SERVER_ERROR, new_url=sed_params)
        else:
            # 将user info种植到cookie中
            username = sed_params.get("username")
            data = {
                "username": username,
                "returnFields": "imageUrl,departmentName,email",
                "timestamp": int(time.time()),
                "appKey": APP_KEY,
                "sRandom": str(uuid.uuid1())
            }
            sign = AuthCheck.get_sign(data)
            data["sign"] = sign
            res = await GetUserInfo(data).get_data()
            if type(res) == dict and res.get("code") == 200:
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
                self.set_cookie('userid', str(userid))
                self.set_cookie('avater', user_info["imageUrl"])
                self.set_cookie('username', username)
            return resp.return_success_response(self, data={}, all_count=1)

