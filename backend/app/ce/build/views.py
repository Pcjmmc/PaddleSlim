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
        return count, details


class PackageManage(MABaseView):
    """
    根据日期和分支查询编包的地址
    """
    get_summary = '查询编译包的地址'

    async def get(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().get(**kwargs)

    def process_params(self, **kwargs):
        """
        对请求参数进行预处理
        """
        date_time = kwargs.get("date_time") or datetime.date.today().strftime("%Y-%m-%d")
        if kwargs.get("date_time"):
            kwargs.pop("date_time")
        time_begin, time_end = get_begin_and_time(dt=date_time, formats="%Y-%m-%d")
        kwargs["create_time__gte"] = time_begin
        kwargs["create_time__lt"] = time_end
        kwargs["branch_contains"] = kwargs.get("branch", "develop")
        return kwargs

    async def get_data(self, **kwargs):
        """
        响应请求, 实现获取数据逻辑, 返回所有的符合要求的包列表
        """
        kwargs = self.process_params(**kwargs)
        branch = kwargs.get("branch", "develop")
        if kwargs.get("branch"):
            kwargs.pop("branch")
        _, details = await CeBuildPackage.aio_filter_details_with_total_count(
            need_all=True, **kwargs, order_by="-create_time"
        )
        result = []
        for item in details:
            try:
                urls = json.loads(item.get("artifact_url")) if item.get("artifact_url", None) else []
            except:
                urls = item.get("artifact_url")
            if type(urls) != list:
                urls = [urls]
            item["artifact_url"] = urls
            bc = item.get('branch', '').split('\n')
            if len(bc) == 1 and bc[0].strip('*').strip() == branch:
                result.append(item)
            elif len(bc) > 1:
                for b in bc:
                    if '*' in b and b.strip('*').strip() == branch:
                        result.append(item)
                        break
        return len(result), result
