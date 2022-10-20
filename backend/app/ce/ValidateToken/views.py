# !/usr/bin/env python3
# encoding=utf-8
import asyncio
import datetime
import hashlib
import json
import time
import urllib

import tornado.web
from ce_web.settings.common import (APP_KEY, BASE_URL, DEFAULT_URL, EAC_HOST,
                                    PTOKEN, UUAP_SECRET_KEY)
from https import response as resp
from rpc.eac import GetStoken

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
    
        
    
