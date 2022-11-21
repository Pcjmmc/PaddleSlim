# !/usr/bin/env python3
# -*- coding:utf8 -*-
import os
import sys
import asyncio
import aiohttp
import urllib.parse
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from ce_web.settings.common import RPC_SETTINGS
from rpc.base import BaseRpc

PADDLE_HI_GATEWAY = RPC_SETTINGS['paddle_hi']['gateway']
PADDLE_HI_TOKEN = RPC_SETTINGS['paddle_hi']['access_token']
PADDLE_HI_AGENTID = RPC_SETTINGS['paddle_hi']['agentid']
PADDLE_HI_CORPID = RPC_SETTINGS['paddle_hi']['corpid']
PADDLE_HI_CORPSECRET = RPC_SETTINGS['paddle_hi']['corpsecret']

class HiGetToken(BaseRpc):
    """
    获取token
    """
    method = 'get'
    gateway = PADDLE_HI_GATEWAY
    api = "api/gettoken"
    params_keys = [
        {'key': 'corpid', 'type': str},
        {'key': 'corpsecret', 'type': str},
    ]
    
    async def get_data(self, **kwargs):
        result = await self.is_valid()
        if result and str(self._status == '200'):
            return self.response_json
        return {}

    
     
class HiSendMessage(BaseRpc):
    """
    发送消息
    """
    method = 'post'
    gateway = PADDLE_HI_GATEWAY
    api = 'api/message/send?access_token={access_token}'
    #headers ={"Content-type": "application/json"}

    json_keys = [
        {'key': 'touser', 'type': str},
        {'key': 'msgtype', 'type': str},
        {'key': 'agentid', 'type': str},
        {'key': 'text', 'type': dict}
    ]

    #icafe用get形式实现post请求，需要额外设置header和api
    def set_api(self, **kwargs):
        self.api = self.api.format(**kwargs)

    async def get_data(self, **kwargs):
        self.set_api(**kwargs)
        result = await self.is_valid()
        if result and str(self._status == '200'):
            # print(self._response_text)
            return self.response_json
        return {}

if __name__ == "__main__":
    # 测试给自己发消息
    loop = asyncio.get_event_loop()
    """
    result = loop.run_until_complete(HiSendMessage(
        {
        'touser':'guozhengxin',
        'msgtype': 'text',
        'agentid': PADDLE_HI_AGENTID,
        'text': {"content": "gzx test"}
        }).get_data(**{'access_token': PADDLE_HI_TOKEN}))      
    """
    result = loop.run_until_complete(HiGetToken({
        'corpid': PADDLE_HI_CORPID,
        'corpsecret': PADDLE_HI_CORPSECRET
     }).get_data())
    print("result=", result)
