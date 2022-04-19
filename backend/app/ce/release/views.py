# encoding=utf-8
import asyncio
import datetime
import json
import time

from ce_web.settings.common import STORAGE
from ce_web.settings.scenes import scenes_dict
from libs.mongo.db import Mongo
from models.release_version import CeReleaseVersion
from models.steps import CeSteps
from rpc.github import GetBranches, GetCommit, GetTags
from services.menu import update_menu
from services.tasks import ExemptInfo, TaskBuildInfo, TasksInfo
from utils.change_time import stmp_by_date

from views.base_view import MABaseView


class ReleaseVersionManage(MABaseView):

    async def get(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        # 根据查询需求将版本的相关信息以及steps信息返回到前端
        version = kwargs.get("version")
        appid = kwargs.get("appid", 1)
        if version == "release/undefined":
            obj = await CeReleaseVersion().aio_get_object(
                **{"activated": True}
            )
            version = obj.name if obj else None
        
        release_info = {
            "repo_info": {},
            "process_data": {}
        }
        percent = 0
        total = 0
        if not version:
            return 0, release_info
        res = await CeReleaseVersion().aio_get_object(**{"name": version})
        if res:
            release_info["repo_info"] = {
                "name": res.name,
                "version_id": res.id,
                "branch": res.branch,
                "commit": res.begin_commit,
                "tag": res.tag
            }
            version_id = res.get("id")
            # steps = await CeSteps().aio_filter_details(**{"version_id": version_id})

            # new_steps = sorted(steps, key=lambda e: e.__getitem__('order'))
            # release_info["all_steps"] = {
            #     item["rtype"]: {
            #         "content": item["content"],
            #         "status": item.get("status", "wait"),
            #         "flag": True if item.get("flag", 0) else False
            #     } for item in new_steps
            # }
            # 根据release 的细腻来查询,改接口是负责release的，故step=release
            all_release_task = await TasksInfo.get_all_task_info_by_filter(
                step="release", appid=appid
            )
            total = len(all_release_task)
            # 查询到来全量任务
            tids = [item.get("id") for item in all_release_task]
            # 获取任务的最新状态
            build_info = await TaskBuildInfo.get_task_latest_status_by_tids(
                tids, res.get("branch"), res.get("begin_time"), end_time=res.get("end_time", None)
            )
            # 获取豁免状态
            exempt_info = await ExemptInfo.get_task_exempt_status_by_tids(
                tids, version_id
            )
            temp_data = [{
                "tid": item["id"], 
                "tname": item["tname"], 
                "description": item["description"],
                "system": item["system"],
                "task_type": item["task_type"]} for item in all_release_task]
            for item in temp_data:
                tid = item["tid"]
                if tid in build_info:
                    item["status"] = build_info[tid].get("status")
                else:
                    item["status"] = "undone"
                exempt_status = exempt_info.get(tid, {}).get("status", False)    
                item["exempt_status"] = True if exempt_status else False
                if item["exempt_status"] or item["status"] == "Passed":
                    # 如果成功或者豁免就记录进入进度
                    percent += 1
            # 封装process_data
            percent = '%.2f' % ((percent/total)*100)
            release_info["process_data"].update(
                {"total": total, "percent": float(percent)}
            )
        return 0, release_info


    async def post(self, **kwargs):
        """
        调用基类的post方法
        """
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        # 根据参数初始化一次发版记录是
        """
        params: branch: 监控的分支名
        params: plan_tag: 所属计划名tag
        """
        branch = kwargs.get("version")
        tag = kwargs.get("plan_tag")
        record = {
            "name": branch,
            "branch": branch,
            "tag": tag,
            "pre_tag": None,
            "begin_time": None,
            "end_time": None,
            "begin_commit": None,
            "end_commit": None,
            "activated": True
        }
        # 获取tag的info
        tag_info = await GetTags().get_latest_tag_info()
        pre_tag = tag_info.get("name")
        record["pre_tag"] = pre_tag
        result = self.initByBranch(branch, pre_tag)
        if result:
            # 获取分支的info
            branch_info = await GetBranches().get_commit_info_by_branch(
                **{'branch': branch}
            )
            begin_commit = branch_info.get("commit")
            begin_time = branch_info.get("time")
        else:
            begin_commit = tag_info.get("commit").get("sha")
            commit = await GetCommit().get_commit_info(**{"commit": begin_commit})
            begin_time = commit.get("date")
        begin_time = stmp_by_date(begin_time, fmt="%Y-%m-%dT%H:%M:%SZ")
        commit_info = {
            "begin_commit": begin_commit,
            "begin_time": begin_time
        }
        record.update(**commit_info)
        # 创建之前要把已经存在或者activated的设置成false
        _obj = await CeReleaseVersion().aio_get_object(**{"name": branch})
        if not _obj:
            await CeReleaseVersion().aio_update(
                validated_data={"activated": False},
                params_data={"activated": True}
            )
            _, row_id = await CeReleaseVersion().aio_insert(validated_data=record)
            # _type("integration", "createtag", "regression", "release"）
            defult_list = [
                {
                    "rtype": "integration",
                    "content": "集成测试",
                    "status": "process",
                    "flag": True,
                    "order": 1
                },
                {
                    "rtype": "createtag",
                    "content": "打tag",
                    "status": "wait",
                    "flag": False,
                    "order": 2
                },
                {
                    "rtype": "regression",
                    "content": "编包验证",
                    "status": "wait",
                    "flag": False,
                    "order": 3
                },
                {
                    "rtype": "release",
                    "content": "发布",
                    "status": "wait",
                    "flag": False,
                    "order": 4
                }
            ]
            steps_list = kwargs.get("steps_list", []) or defult_list
            for item in steps_list:
                item.update({"version_id": row_id})
            await CeSteps().aio_insert(validated_data=steps_list)
            # 创建之后，要及时更新menu的release板块
            await update_menu()

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

    def initByBranch(self, branch, pre_tag):
        # 根据branch 和 tag info来决定用那个信息
        branch_list = branch.strip().split("/")[-1]
        tag_list = pre_tag.strip().split("v")[-1]
        branch_version = branch_list.split(".")
        tag_verison = tag_list.split(".")
        if branch_version and tag_verison:
            if len(branch_version) < 2:
                branch_version.append('0')
            if len(tag_verison) < 2:
                tag_verison.append('0')
            if branch_version[0] != tag_verison[0]:
                return True
            elif branch_version[1] != tag_verison[1]:
                return True
            else:
                return False
        return True

class TaskManage(MABaseView):

    async def get(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        # 根据查询需求将版本的相关信息以及steps信息返回到前端
        version = kwargs.get("version")
        appid = kwargs.get("appid", 1)
        task_type = kwargs.get("task_type")
        if version == "release/undefined":
            obj = await CeReleaseVersion().aio_get_object(
                **{"activated": True}
            )
            version = obj.name if obj else None
        integration_data = {}
        data = []
        if not version or not task_type:
            return 0, integration_data
        res = await CeReleaseVersion().aio_get_object(**{"name": version})
        if res:
            version_id = res.get("id")
            # 根据release 的细腻来查询,改接口是负责release的，故step=release
            all_release_task = await TasksInfo.get_all_task_info_by_filter(
                step="release", task_type=task_type, appid=appid
            )
            # 查询到来全量任务
            tids = [item.get("id") for item in all_release_task]
            # 获取任务的最新状态
            build_info = await TaskBuildInfo.get_task_latest_status_by_tids(
                tids, res.get("branch"), res.get("begin_time"), end_time=res.get("end_time", None)
            )
            # 获取豁免状态
            exempt_info = await ExemptInfo.get_task_exempt_status_by_tids(
                tids, version_id
            )
            temp_data = [{
                "tid": item["id"], 
                "tname": item["tname"], 
                "description": item["description"],
                "system": item["system"],
                "task_type": item["task_type"],
                "secondary_type": item["secondary_type"],
                "reponame": item["reponame"]} for item in all_release_task]
            for item in temp_data:
                tid = item["tid"]
                if tid in build_info:
                    item["status"] = build_info[tid].get("status")
                    item["left_time"] = build_info[tid].get("left_time")
                    item["build_id"] = build_info[tid].get("build_id")
                    item["commit_id"] = build_info[tid].get("commit_id")
                    item["branch"] = build_info[tid].get("branch")
                    item["repo"] = build_info[tid].get("repo")
                else:
                    item["status"] = "undone"
                exempt_status = exempt_info.get(tid, {}).get("status", False)    
                item["exempt_status"] = True if exempt_status else False
             # 根据task_type来组装数据 todo
            if task_type == "compile":
                for item in temp_data:
                    system = item["system"]
                    if system not in integration_data:
                        integration_data[system] = list()
                    integration_data[system].append(item)
                data = [{"system": k, "data": v} for k, v in integration_data.items()]
            elif task_type == "model":
                for item in temp_data:
                    system = item["system"]
                    reponame = item["reponame"]
                    secondary_type = item["secondary_type"]
                    try:
                        secondary_type = json.loads(secondary_type)
                    except:
                        secondary_type = [secondary_type]
                    if system not in integration_data:
                        integration_data[system] = dict()
                    if reponame not in integration_data[system]:
                        integration_data[system][reponame] = dict()
                    for _type in secondary_type:
                        if _type not in integration_data[system][reponame]:
                            integration_data[system][reponame][_type] = list()
                        integration_data[system][reponame][_type].append(item)
                data = [{"system": k, "data": v} for k, v in integration_data.items()]
            else:
                for item in temp_data:
                    system = item["system"]
                    secondary_type = item["secondary_type"]
                    try:
                        secondary_type = json.loads(secondary_type)
                    except:
                        secondary_type = [secondary_type]
                    if system not in integration_data:
                        integration_data[system] = dict()
                    for _type in secondary_type:
                        if _type not in integration_data[system]:
                            integration_data[system][_type] = list()
                        integration_data[system][_type].append(item)
                data = [{"system": k, "data": v} for k, v in integration_data.items()]
        # print("integration_data", integration_data)    
        return len(data), data 
