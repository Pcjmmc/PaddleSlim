# !/usr/bin/env python3
# encoding: utf-8
"""
校验是否登录
"""
import hashlib
import time
import urllib
from functools import reduce

import requests
from ce_web.settings.common import (
    APP_KEY, BASE_URL, DEFAULT_URL, EAC_HOST,
    PTOKEN, UUAP_SECRET_KEY
)
from rpc.eac import AECValiad
from exception import HTTP401Error
from models.user import User


class AuthCheck(object):
    """
    实现参数名和类型的检测
    """
    @classmethod
    def get_sign(cls, data):
        """签名"""
        str_param = ''
        i = 0
        for key in sorted(data):
            i += 1
            str_param += str(data[key])
        before_sha256 = '%s%s' % (str_param, UUAP_SECRET_KEY)
        hash_256 = hashlib.sha256()
        hash_256.update(before_sha256.encode('utf-8'))
        return hash_256.hexdigest()


    @classmethod
    async def check_auth(cls, cookies, headers):
        """
        验证是否登录
        """
        origin_url = headers.get("Originurl") or DEFAULT_URL
        my_base_url = '%s/ce/sTokenBackendValidate' % BASE_URL
        url = '%s/authorize?service=%s?originalUrl=%s&appKey=%s&version=v2'
        url = url % (EAC_HOST, urllib.parse.quote(my_base_url), urllib.parse.quote(origin_url),  APP_KEY)
        pToken = cookies.get(PTOKEN)
        sToken = cookies.get('UUAP_S_TOKEN')
        if pToken and sToken: 
            # 做进一步校验
            data = {
                "pToken": pToken,
                "sToken": sToken,
                "appKey": APP_KEY,
                "timestamp": int(time.time()),
            }
            sign = cls.get_sign(data)
            data["sign"] = sign
            res = await AECValiad(data).get_data()
            if res.get("code") == 200:
                user_info = res.get('result') or {}
                # 去查库，比对id,
                username = user_info.get("username")
                user_res = await User().aio_get_object(**{"username": username})
                # 前提是库里已有信息
                if user_res and (str(user_res.id) != cookies.get("userid", "")):
                    raise HTTP401Error
                return False, user_info

        return True, url
