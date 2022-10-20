# !/usr/bin/env python3
# -*- coding:utf8 -*-
import os
import sys
import asyncio
import aiohttp
import urllib.parse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from ce_web.settings.common import EAC_HOST
from rpc.base import BaseRpc


class AECValiad(BaseRpc):
    """
    修改用户名
    """
    method = 'post'
    gateway = EAC_HOST
    api = 'session/validate'
    headers = {"Content-type": "application/x-www-form-urlencoded"}

    params_keys = [
        {
            'key': 'pToken',
            'type': str
        },
        {
            'key': 'sToken',
            'type': str
        },
        {
            'key': 'appKey',
            'type': str
        },
        {
            'key': 'timestamp',
            'type': str
        },
        {
            'key': 'sign',
            'type': str
        },
    ]

    async def get_data(self, **kwargs):
        result = await self.is_valid()
        if result and str(self._status == '200'):
            return self.response_json
        return {}


class GetStoken(BaseRpc):
    """
    ticket置换sToken
    """
    method = 'post'
    gateway = EAC_HOST
    api = 'sTokenDecrypt'
    headers = {"Content-type": "application/x-www-form-urlencoded"}

    params_keys = [
        {
            'key': 'encryptedSToken',
            'type': str
        },
        {
            'key': 'appKey',
            'type': str
        },
        {
            'key': 'timestamp',
            'type': str
        },
        {
            'key': 'sign',
            'type': str
        },
    ]

    async def get_data(self, **kwargs):
        result = await self.is_valid()
        if result and str(self._status == '200'):
            return self.response_json
        return {}

class GetUserInfo(BaseRpc):
    """
    ticket置换sToken
    """
    method = 'post'
    gateway = EAC_HOST
    api = 'uic/restful/v1/userInfo/getUserByUsername'
    headers = {"Content-type": "application/x-www-form-urlencoded"}

    params_keys = [
        {
            'key': 'username',
            'type': str
        },
        {
            'key': 'returnFields',
            'type': str
        },
        {
            'key': 'appKey',
            'type': str
        },
        {
            'key': 'sRandom',
            'type': str
        },
        {
            'key': 'timestamp',
            'type': str
        },
        {
            'key': 'sign',
            'type': str
        }
    ]

    async def get_data(self, **kwargs):
        result = await self.is_valid()
        if result and str(self._status == '200'):
            return self.response_json
        return {}


class Logout(BaseRpc):
    """
    ticket置换sToken
    """
    method = 'post'
    gateway = EAC_HOST
    api = 'logout'
    headers = {"Content-type": "application/x-www-form-urlencoded"}

    params_keys = [
        {
            'key': 'service',
            'type': str
        },
        {
            'key': 'appKey',
            'type': str
        }
    ]

    async def get_data(self, **kwargs):
        result = await self.is_valid()
        if result and str(self._status == '200'):
            return self.response_json
        return {}