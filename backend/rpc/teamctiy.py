# -*- coding:utf8 -*-
import os
import sys
import asyncio
import aiohttp
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
from ce_web.settings.common import RPC_SETTINGS
from rpc.base import BaseRpc

TC_GATEWAY = RPC_SETTINGS['teamcity']['gateway']
TC_USER = RPC_SETTINGS['teamcity']['username']
TC_PASSD = RPC_SETTINGS['teamcity']['password']

class GetTcTaskState(BaseRpc):
    """
    修改用户名
    """
    method = 'get'
    gateway = TC_GATEWAY
    api = 'app/rest/builds/?locator=buildType:(id:{buildTypeId}),state:any'
    auth = aiohttp.BasicAuth(login=TC_USER, password=TC_PASSD, encoding='utf-8')

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
    content = loop.run_until_complete(
        GetTcTaskState().get_data(**{"buildTypeId": "ContinuousEvaluation_ModelEvaluation_PaddleNLP_Mac_PaddleNLPPy39MacModelTestP0d"})
    )
    print('tc content is', content)
