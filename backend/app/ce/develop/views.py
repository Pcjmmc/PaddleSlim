# !/usr/bin/env python3
# encoding=utf-8
import asyncio
import copy
import datetime
import json
import time

from ce_web.settings.common import (
    STORAGE, TC_BASE_URL, XLY_BASE_URL, XLY_BASE_URL2
)
from models.release_version import CeReleaseVersion
from models.steps import CeSteps
from rpc.github import GetBranches, GetCommit, GetTags
from services.summary import Summary
from services.tasks import TaskBuildInfo, TasksInfo

from views.base_view import MABaseView


class DevelopVersionManage(MABaseView):

    async def get(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        # 根据查询需求将版本的相关信息以及steps信息返回到前端
        version = kwargs.get("version")
        appid = kwargs.get("appid", 1)
        release_info = {"repo_info": {}, "process_data": {}, "summary": []}
        percent = 0
        total = 0
        if not version:
            return 0, release_info
        # 根据分支获取访问github获取最新的一个commit
        # 获取分支的info
        branch_info = await GetBranches().get_commit_info_by_branch(
            **{'branch': version}
        )
        latest_commit = branch_info.get("commit")
        release_info["repo_info"] = {
            "name": version,
            "branch": version,
            "commit": latest_commit
        }
        all_release_task = await TasksInfo.get_all_task_info_by_filter(
            step="develop", appid=appid)
        total = len(all_release_task)
        # 查询到来全量任务
        tids = [item.get("id") for item in all_release_task]
        # 获取任务的最新状态
        # 选择最近一周的develop新任务
        today = datetime.date.today()
        today_time = int(time.mktime(today.timetuple()))
        begin_time = today_time - 7 * 24 * 60 * 60
        build_info = await TaskBuildInfo.get_task_latest_status_by_tids(
            tids, version, begin_time)
        temp_data = [{
            "tid": item["id"],
            "tname": item["tname"],
            "description": item["description"],
            "system": item["system"],
            "task_type": item["task_type"]
        } for item in all_release_task]
        for item in temp_data:
            tid = item["tid"]
            if tid in build_info:
                item["status"] = build_info[tid].get("status")
                item["total_case"] = build_info[tid].get("total_case") or 0 
                item["failed_case"] = build_info[tid].get("failed_case") or 0
            else:
                item["status"] = "undone"
                item["total_case"] = 0
                item["failed_case"] = 0
            if item["status"] == "Passed":
                # 如果成功或者豁免就记录进入进度
                percent += 1
        # 封装process_data
        percent = '%.2f' % ((percent / total) * 100)
        release_info["process_data"].update({
            "total": total,
            "percent": float(percent)
        })
        summary = Summary.get_summary(temp_data)
        release_info["summary"] = summary
        return 0, release_info

    async def post(self, **kwargs):
        """
        调用基类的post方法
        """
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        pass

    async def put(self, **kwargs):
        """
        调用基类的put方法
        """
        return await super().post(**kwargs)

    async def put_data(self, **kwargs):
        pass

    async def delete(self, **kwargs):
        """
        调用基类的delete方法
        """
        return await super().post(**kwargs)

    async def delete_data(self, **kwargs):
        pass

