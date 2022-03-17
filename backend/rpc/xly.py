# -*- coding:utf8 -*-
import asyncio
import os
import sys

import aiohttp

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from ce_web.settings.common import RPC_SETTINGS

from rpc.base import BaseRpc

XLY_GATEWAY = RPC_SETTINGS['xly']['gateway']


class GetXlyTaskState(BaseRpc):
    """
    修改用户名
    """
    method = 'get'
    gateway = XLY_GATEWAY
    api = '{workspace}/ipipe/rest/v3/pipeline-builds/last-builds?_embed[]=trigger'

    params_keys = [
        {'key': 'pipelineConfId', 'type': int}
    ]

    def process_api(self, **kwargs):
        self.api = self.api.format(**kwargs)

    async def get_data(self, **kwargs):
        self.process_api(**kwargs)
        result = await self.is_valid()
        if result and str(self._status == '200'):
            return self.response_json
        return {}

if __name__ == "__main__":
    # 接口的调用示例
    loop = asyncio.get_event_loop()
    xly_content = loop.run_until_complete(
        GetXlyTaskState({"pipelineConfId": 20403}).get_data(**{"workspace": "Paddle-NLP"})
    )
    print('xly content is ', xly_content)
