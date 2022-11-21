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

class HiSendMessage(BaseRpc):
    """
    创建icafe卡片
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
    # 给自己的卡片建设
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(HiSendMessage(
        {
        'touser':'guozhengxin',
        'msgtype': 'text',
        'agentid': PADDLE_HI_AGENTID,
        'text': {"content": "gzx test"}
        }).get_data(**{'access_token': PADDLE_HI_TOKEN}))      
    print("result=", result)
