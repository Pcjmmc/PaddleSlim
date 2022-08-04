# !/usr/bin/env python3
# encoding=utf-8
import asyncio
import datetime
import json
import time

from models.icafe import CeIcafe

from views.base_view import MABaseView


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
        return len(result), result
