# !/usr/bin/env python3
# encoding=utf-8
import asyncio
import copy
import datetime
import json
import time

from models.release_version import CeReleaseVersion
from services.log_url import get_log_url
from services.tasks import PublishBuildInfo, TasksInfo
from utils.change_time import stmp_by_date

from views.base_view import MABaseView


class PublishSummaryManage(MABaseView):

    async def get(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        """
        汇总发布流程的整体进度；返回数据
        获取所有任务；获取所有任务的最新的一次编译，看目前所处的阶段
        任务总数
        编译阶段: 编译阶段成功的个数（编译成功：0 sucess、1:（所有状态））失败（0 failed）
        验证阶段: 成功的个数：（1: success 1:failed）
        """
        # 根据查询需求将版本的相关信息以及steps信息返回到前端
        version = kwargs.get("version")
        # 如果是dev则返回空即可
        if version == "develop":
            return 0, []
        summary = []
        verison_info = await CeReleaseVersion().aio_get_object(**{"name": version})
        tag = verison_info.tag
        # 获取查询的全量任务
        query_params = copy.deepcopy(kwargs)
        query_params.pop('version')
        all_task_info = await TasksInfo.get_task_by_filter(**query_params)
        tids = [item.get("id") for item in all_task_info]
        total = len(tids)
        compile_res = {
            'step': '编译',
            'total': total,
            'succeed': 0,
            'failed': 0,
        }
        test_res =  {
            'step': '验证',
            'total': total,
            'succeed': 0,
            'failed': 0,
        }
        # 获取每个任务最新的一次执行
        build_info = await PublishBuildInfo.get_task_latest_status_by_tids(
            tids, tag
        )
        for key, val in build_info.items():
            step = val.get('test_step', None)
            status = val.get('status', None)
            if status and step is not None:
                if int(step) == 1:
                    # 到了验证阶段的肯定是编译通过了
                    compile_res["succeed"] += 1
                    if status == 'success':
                       test_res['succeed'] += 1
                    elif status == 'failed':
                        test_res['failed'] += 1
                elif int(step) == 0:
                    # 如果在编译阶段的则根据状态来判断
                    if status == 'success':
                       compile_res['succeed'] += 1
                    elif status == 'failed':
                        compile_res['failed'] += 1
        summary.append(compile_res)
        summary.append(test_res)
        return len(summary), summary



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
            platform = item.get("platform")
            workspace = item.get("workspace")
            if system not in integration_data:
                integration_data[system] = list()
            build_data = build_info.get(tid, {})
            item.update(build_data)
            status = item.get("status", None)
            log_url = ""
            if build_data:
                log_url = get_log_url(
                    platform,
                    workspace,
                    item.get("build_id"),
                    job_id=item.get("job_id"),
                    build_type_id=item.get("build_type_id")
                )
            item["log_url"] = log_url
            if status == "success":
                # 目前的阶段已经成功，则展示挪向下一个阶段
                item["test_step"] += 1
                item['status'] = 'undone'
            elif status is None:
                item['status'] = 'undone'
                item['test_step'] = -1
            # 初始化前端控制
            item["showTestModal"] = False
            # 处理test_log
            try:
                check_info = json.loads(item.get("check_info"))
                item["check_info"] = [
                    {
                        "desc": itm[0],
                        "test_url": get_log_url(platform, workspace, itm[2]), 
                        "status": itm[3]
                    } for itm in check_info
                ]
            except Exception as e:
                print("load check info got error", e)
                item["check_info"] = []
            integration_data[system].append(item)
        data = [{"system": k, "data": v} for k, v in integration_data.items()]
        return len(data), data
