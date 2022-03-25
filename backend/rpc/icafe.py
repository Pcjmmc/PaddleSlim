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

PADDLE_ICAFE_GATEWAY = RPC_SETTINGS['paddle_icafe']['gateway']
PADDLE_ICAFE_USER = RPC_SETTINGS['paddle_icafe']['username']
PADDLE_ICAFE_PASSD = RPC_SETTINGS['paddle_icafe']['password']

class CreateBug(BaseRpc):
    """
    修改用户名
    """
    method = 'post'
    gateway = PADDLE_ICAFE_GATEWAY
    api = 'v2/space/DLTP/issue/new'
    
    params_keys = [
        {'key': 'username', 'type': str},
        {'key': 'password', 'type': str},
        {'key': 'title', 'type': str},
        {'key': 'detail', 'type': str},
        {'key': 'type', 'type': str},
        {'key': '所属计划', 'type': str},
        {'key': 'fields', 'type': str}
    ]


class GetBug(BaseRpc):
    """
    修改用户名
    """
    method = 'get'
    gateway = PADDLE_ICAFE_GATEWAY
    api = 'spaces/DLTP/cards'
    
    params_keys = [
        {'key': 'u', 'type': str},
        {'key': 'pw', 'type': str} ,
        {'key': 'iql', 'type': str} 
    ]
    

    async def get_data(self, **kwargs):
        result = await self.is_valid()
        if result and str(self._status == '200'):
            return self.response_json
        return {}


if __name__ == "__main__":
    # 给自己的卡片建设
    loop = asyncio.get_event_loop()
    query = '所属计划 = 飞桨项目集/Paddle/{plan} AND auto_tag = auto_issue'.format(plan='v2.3.0-RC')
    print("query", query)
    commits = loop.run_until_complete(GetBug(
        {'u': PADDLE_ICAFE_USER,
        'pw': PADDLE_ICAFE_PASSD,
        'iql': query
        }).get_data()
    )
    print("branches  latest commit info is", commits)
       