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

class CreateCard(BaseRpc):
    """
    创建icafe卡片
    """
    method = 'post'
    gateway = PADDLE_ICAFE_GATEWAY
    api = 'v2/space/DLTP/issue/new'
    headers ={"Content-type": "application/json"}

    json_keys = [
        {'key': 'username', 'type': str},
        {'key': 'password', 'type': str},
        {'key': 'issues', 'type': list},
        {'key': 'creator', 'type': str}
    ]

    async def get_data(self, **kwargs):
        result = await self.is_valid()
        if result and str(self._status == '200'):
            # print(self._response_text)
            return self.response_json
        return {}


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

class GetCards(BaseRpc):
     """
     分页获取获取符合规则的icafe卡片
     """
     method = 'get'
     gateway = PADDLE_ICAFE_GATEWAY
     api = 'spaces/DLTP/cards'
     params_keys = [
        {'key': 'u', 'type': str},
        {'key': 'pw', 'type': str},
        {'key': 'iql', 'type': str},
        {'key': 'page', 'type': int},
        {'key': 'maxRecords', 'type': str},
        {'key': 'showChildren', 'type': str}
     ]
     async def get_data(self, **kwargs):
         result = await self.is_valid()
         if result and str(self._status == '200'):
             return self.response_json
         return {}

class ModifyCardStatus(BaseRpc):
    """
    修改icafe状态
    """
    method = 'post'
    gateway = PADDLE_ICAFE_GATEWAY
   
    api = "spaces/DLTP/cards/{card_id}"

    headers ={"Content-type": "application/x-www-form-urlencoded"}
    params_keys = [
        {'key': 'u', 'type': str},
        {'key': 'pw', 'type': str},
        {'key': 'operator', 'type': str},
        {'key' : 'isCheckStatus', 'type':bool}, 
        {'key': 'fields', 'type': list}
       
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
    """
    query = '所属计划 = 飞桨项目集/Paddle/{plan} AND auto_tag = auto_issue'.format(plan='v2.3.0-RC')
    print("query", query)
    commits = loop.run_until_complete(GetBug(
        {'u': PADDLE_ICAFE_USER,
        'pw': PADDLE_ICAFE_PASSD,
        'iql': query
        }).get_data()
    )
    print("branches  latest commit info is", commits)
    """
    field_str = "流程状态=测试完成"
    result = loop.run_until_complete(ModifyCardStatus(
        {'u': PADDLE_ICAFE_USER,
        'pw': PADDLE_ICAFE_PASSD,
        'isCheckStatus': False,
        'operator': "guozhengxin",
        'fields': [field_str] 
        }).get_data(**{"card_id":61676}))      
    print("result=", result)
