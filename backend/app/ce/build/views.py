# !/usr/bin/env python3
# encoding: utf-8
"""
主要的查询逻辑和数据组合
"""
import asyncio
import datetime
import json
import time

from ce_web.settings.common import STORAGE
from models.task_builds import CeTaskBuilds
from utils.change_time import get_begin_and_time

from views.base_view import MABaseView


class BuildManage(MABaseView):
    """
    根据时间查询任务的编译历史
    """
    get_summary = '获取所有任务'

    async def get(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().get(**kwargs)

    def process_params(self, **kwargs):
        """
        对请求参数进行预处理
        """
        begin_time = kwargs.get("begin_time") or datetime.date.today().strftime("%Y-%m-%d")
        end_time = kwargs.get("end_time") or datetime.date.today().strftime("%Y-%m-%d")
        time_begin, _ = get_begin_and_time(dt=begin_time, formats="%Y-%m-%d")
        _, time_end = get_begin_and_time(dt=end_time, formats="%Y-%m-%d")
        kwargs["created__gte"] = time_begin
        kwargs["created__lt"] = time_end
        return kwargs

    async def get_data(self, **kwargs):
        """
        响应请求, 实现获取数据逻辑, 并返回符合查询条件的数据
        """
        kwargs = self.process_params(**kwargs)
        # print("request params is", kwargs)
        count, details = await CeTaskBuilds.aio_filter_details_with_total_count(**kwargs, order_by="-created")
        for item in details:
            try:
                item["artifact_url"] = json.loads(item["artifact_url"])
            except:
                item["artifact_url"] = []
        return count, details

