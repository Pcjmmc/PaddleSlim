# !/usr/bin/env python3
# encoding=utf-8
import asyncio
import copy
import datetime
import json
import time

from models.release_version import CeReleaseVersion
from services.tasks import PublishBuildInfo, TasksInfo
from utils.change_time import stmp_by_date

from views.base_view import MABaseView


class PublishVersionManage(MABaseView):

    async def get(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        """
        open_cache: 是否从缓存获取，默认False
        根据版本获取汇总信息
        """
        print("requests data", kwargs)
        return 0, []



class PublishTaskManage(MABaseView):

    async def get(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        """
        获取任务详情
        """
        # 根据查询需求将版本的相关信息以及steps信息返回到前端
        version = kwargs.get("version")
        # 如果是dev则返回空即可
        if version == "develop":
            return 0, []
        verison_info = await CeReleaseVersion().aio_get_object(**{"name": version})
        tag = verison_info.tag
        # 获取查询的全量任务
        query_params = copy.deepcopy(kwargs)
        query_params.pop('version')
        all_task_info = await TasksInfo.get_task_by_filter(**query_params)
        tids = [item.get("id") for item in all_task_info]
        # 如果是已封板的话; branch就会变成tag；则还算集测吗？？？tag都打了，应该不算
        build_info = await PublishBuildInfo.get_task_latest_status_by_tids(
            tids, tag
        )
        integration_data = {}
        temp_data = [{
            "tid": item["id"],
            "tname": item["tname"],
            "description": item["description"],
            "show_name": item["show_name"],
            "system": item["system"],
            "task_type": item["task_type"],
            "secondary_type": item["secondary_type"],
            "build_type_id": item["build_type_id"],
            "release_source": item["release_source"],
            "platform": item["platform"],
            "workspace": item["workspace"],
            "reponame": item["reponame"]} for item in all_task_info]
        for item in temp_data:
            # item 进展的阶段内容拼接
            system = item["system"]
            tid = item.get("tid")
            if system not in integration_data:
                integration_data[system] = list()
            item.update(build_info.get(tid, {}))
            status = item.get("status", None)
            if status == "success":
                item["test_step"] += 1
            elif status is None:
                item['status'] = 'undone'
                item['test_step'] = -1
            integration_data[system].append(item)
        data = [{"system": k, "data": v} for k, v in integration_data.items()]
        return len(data), data
