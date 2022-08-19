# !/usr/bin/env python3
# encoding=utf-8
import asyncio
import datetime
import json
import time

from app.ce.bug.views import get_bugs_by_filter
from ce_web.settings.common import RPC_SETTINGS
from models.icafe import CeIcafe
from rpc.icafe import GetBug

from views.base_view import MABaseView

PADDLE_ICAFE_USER = RPC_SETTINGS['paddle_icafe']['username']
PADDLE_ICAFE_PASSD = RPC_SETTINGS['paddle_icafe']['password']

class AssociatedBugManage(MABaseView):

    async def get(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        """
        响应请求, 实现获取数据逻辑, 并返回符合查询条件的数据
        """
        # 获取所有的bug卡片, 根据plan tag 和 类型来查询

        result = await CeIcafe.aio_filter_details(
            need_all=True, **kwargs
        )
        FinalBugData = []
        # 根据卡片sequence获取卡片详情 TODO
        for ret in result:
            sequence = ret.get("sequence")
            if sequence:
                query = '编号 = {sequence}'.format(sequence=sequence)
                _, bugData = await get_bugs_by_filter(query)
                FinalBugData.extend(bugData)
        return len(FinalBugData), FinalBugData
