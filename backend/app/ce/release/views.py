# encoding=utf-8
import asyncio
import copy
import datetime
import json
import time

from app.ce.release.cache import ReleaseSummaryCase
from ce_web.settings.scenes import ORDER, scenes_dict, system_list
from libs.mongo.db import Mongo
from models.details import CeCases
from models.release_version import CeReleaseVersion
from rpc.github import GetBranches, GetCommit, GetTags
from services.log_url import get_log_url
from services.menu import update_menu
from services.summary import Summary
from services.tasks import TaskBuildInfo, TasksInfo
from utils.change_time import stmp_by_date

from views.auth_view import AuthCheck
from views.base_view import MABaseView

class ReleaseVersionManage(MABaseView):
    
    auth_class = AuthCheck

    async def get(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        # 根据查询需求将版本的相关信息以及steps信息返回到前端
        """
        open_cache: 是否从缓存获取，默认False
        """
        version = kwargs.get("version")
        appid = kwargs.get("appid", 1)
        latest = False
        if version == "release/undefined":
            obj = await CeReleaseVersion().aio_get_object(
                **{"activated": True}
            )
            version = obj.name if obj else None
            latest = True
        release_info = {
            "repo_info": {},
            "process_data": {},
            "summary": []
        }
        if not version:
            return 0, release_info
        # 如果命中缓存则直接从缓存获取
        with await ReleaseSummaryCase.get_pools() as redis_conn:
            # 判断key是否存在;则命中缓存
            key_format = ReleaseSummaryCase.key_format.format(version=version)
            finded = await redis_conn.exists(key_format)
            if finded:
                result = await ReleaseSummaryCase.get_value(version)
            else:
                # 如果没命中缓存则从db中查，并将结果存到缓存中，并设置超时时间todo
                result = await self.get_summary_data_from_db(version=version, appid=appid)
                # 如果是已经发完的版本：则1周过期；如果是release则8小时更新一次
                expired = 28800 if latest else 604800
                await ReleaseSummaryCase.set_value(version, json.dumps(result), expired=expired)

            return 1, result

    async def get_summary_data_from_db(self, version, appid=1):
        """
        从db中查询并且实时计算返回结果
        """
        open_cache = False
        need_backup = False
        percent = 0
        total = 0
        release_info = {
            "repo_info": {},
            "process_data": {},
            "summary": []
        }
        job_tasks = []
        res = await CeReleaseVersion().aio_get_object(**{"name": version})
        if res:
            if not res.activated:
                # 如果是已发版的，则直接从库里拿到封版的commit
                latest_commit = res.end_commit
                latest_commit_time = res.end_time
                need_backup = True
            else:
                # relase 分支是有缓存的，但是编译接口没有支持写缓存，所以编译部分的任务不走缓存
                open_cache = True
                job_tasks.append(
                    GetBranches().get_commit_info_by_branch(
                    **{'branch': version})
                )
            all_release_task = await TasksInfo.get_all_task_info_by_filter(
                step="release", appid=appid, backup=need_backup, version=version
            )
            total = len(all_release_task)
            # 查询到来全量任务
            tids = [item.get("id") for item in all_release_task]
            # 获取任务的最新状态
            # 如果是release的则走缓存,
            print("是否开启缓存", open_cache, flush=True)
            job_tasks.append(
                TaskBuildInfo.get_task_latest_status_by_tids(
                    tids, res.branch, 
                    res.get("begin_time"), end_time=res.get("end_time"),
                    open_cache=open_cache
                )
            )
            all_results = await asyncio.gather(*job_tasks)
            if len(all_results) == 2:
                branch_info = all_results[0]
                build_info = all_results[1]
                latest_commit = branch_info.get("commit")
                latest_commit_time = branch_info.get("time")
                if latest_commit_time:
                    latest_commit_time = stmp_by_date(latest_commit_time, fmt="%Y-%m-%dT%H:%M:%SZ")
                    latest_commit_time = latest_commit_time + 28800
            else:
                build_info = all_results[0]

            release_info["repo_info"] = {
                "name": res.name,
                "version_id": res.id,
                "branch": res.branch,
                "commit": latest_commit,
                "latest_commit_time": latest_commit_time,
                "tag": res.tag
            }
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
            release_info["process_data"].update(
                {"total": total, "percent": float(percent)}
            )
            summary = Summary.get_summary(temp_data)
            release_info["summary"] = summary
        return release_info

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
        open_cache = False
        if version == "release/undefined":
            obj = await CeReleaseVersion().aio_get_object(
                **{"activated": True}
            )
            version = obj.name if obj else None
        integration_data = {}
        data = []
        if not version or not task_type:
            return 0, integration_data
        if version == "develop":
            version_id = None
            branch = version
            today = datetime.date.today()
            today_time = int(time.mktime(today.timetuple()))
            begin_time = today_time - 14 * 24 * 60 * 60
            end_time = None
            step = version
            open_cache = True if task_type != "compile" else False
        else:
            res = await CeReleaseVersion().aio_get_object(**{"name": version})
            version_id = res.get("id")
            branch = res.get("branch")
            begin_time = res.get("begin_time")
            end_time = res.get("end_time", None)
            step = "release"
            if res.activated:
                open_cache = True if task_type != "compile" else False
        # 根据release 的细化来查询,改接口是负责release的，故step=release
        all_release_task = await TasksInfo.get_all_task_info_by_filter(
            step=step, task_type=task_type, appid=appid
        )
        # 查询到来全量任务
        tids = [item.get("id") for item in all_release_task]
        # 如果是已封板的话; branch就会变成tag；则还算集测吗？？？tag都打了，应该不算
        print("是否开启缓存", open_cache, flush=True)
        build_info = await TaskBuildInfo.get_task_latest_status_by_tids(
            tids, branch, begin_time, end_time=end_time, open_cache=open_cache
        )
        # 获取豁免状态
        exempt_info = {}
        temp_data = [{
            "tid": item["id"],
            "tname": item["tname"],
            "description": item["description"],
            "show_name": item["show_name"],
            "system": item["system"],
            "task_type": item["task_type"],
            "secondary_type": item["secondary_type"],
            "build_type_id": item["build_type_id"],
            "platform": item["platform"],
            "workspace": item["workspace"],
            "reponame": item["reponame"]} for item in all_release_task]
        for item in temp_data:
            tid = item["tid"]
            task_type = item["task_type"]
            platform = item["platform"]
            workspace = item["workspace"]
            # # 这里要从任务信息里获取；暂时先写成这样
            # workspace = 'paddlepaddle-whl' if task_type == 'compile' else 'paddle-release'
            if tid in build_info:
                item["status"] = build_info[tid].get("status")
                item["exit_code"] = build_info[tid].get("exit_code")
                item["left_time"] = build_info[tid].get("left_time")
                item["build_id"] = build_info[tid].get("build_id")
                item["job_id"] = build_info[tid].get("job_id")
                item["commit_id"] = build_info[tid].get("commit_id")
                item["created"] = build_info[tid].get("created")
                item["commit_time"] = build_info[tid].get("commit_time")
                item["branch"] = build_info[tid].get("branch")
                item["repo"] = build_info[tid].get("repo")
                item["artifact_url"] = build_info[tid].get("artifact_url")
                log_url = get_log_url(
                    platform,
                    workspace,
                    item.get("build_id"),
                    job_id=item.get("job_id"),
                    build_type_id=item.get("build_type_id")
                )
                item["log_url"] = log_url
            else:
                item["status"] = "undone"
            exempt_status = exempt_info.get(tid, {}).get("status", False)    
            item["exempt_status"] = True if exempt_status else False
        # 根据task_type来组装数据 todo
        if task_type == "compile":
            for item in temp_data:
                system = item["system"]
                if item.get("artifact_url"):
                    try:
                        item["artifact_url"] = json.loads(item.get("artifact_url", ""))
                    except:
                        item["artifact_url"] = []
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
                    secondary_type = secondary_type.split(",")
                except:
                    secondary_type = [secondary_type]
                if system not in integration_data:
                    integration_data[system] = dict()
                if reponame not in integration_data[system]:
                    integration_data[system][reponame] = dict()
                for _type in secondary_type:
                    if _type not in integration_data[system][reponame]:
                        integration_data[system][reponame][_type] = list()
                    # 根据二级分类更新下case成功失败数
                    case_detail = await self.get_case_detail(item["tid"], item["build_id"], _type)
                    # 保留任务的status
                    job_status = item.get("status")
                    # 用case的状态覆盖任务的状态
                    item.update(case_detail)
                    if not job_status or job_status == "undone": # 则保留任务原来的状态
                        item["status"] = "undone"
                    temp_item = copy.deepcopy(item)
                    temp_item['secondary_type'] = _type
                    integration_data[system][reponame][_type].append(temp_item)
            # 这里的排序按照套件指定的顺序排序下
            data = [{"system": k, "data": dict(sorted(v.items(), key=lambda item:ORDER.get(item[0])))} for k, v in integration_data.items()]
        else:
            for item in temp_data:
                system = item["system"]
                secondary_type = item["secondary_type"]
                try:
                    secondary_type = secondary_type.split(",")
                except:
                    secondary_type = [secondary_type]
                if system not in integration_data:
                    integration_data[system] = dict()
                for _type in secondary_type:
                    if _type not in integration_data[system]:
                        integration_data[system][_type] = list()
                    # 根据二级分类更新下case成功失败数
                    case_detail = await self.get_case_detail(item["tid"], item["build_id"], _type)
                    # 保留任务的status
                    job_status = item.get("status")
                    # 用case的状态覆盖任务的状态
                    item.update(case_detail)
                    if not job_status or job_status == "undone": # 则保留任务原来的状态
                        item["status"] = "undone"
                    temp_item = copy.deepcopy(item)
                    temp_item['secondary_type'] = _type
                    integration_data[system][_type].append(temp_item)
            data = [{"system": k, "data": v} for k, v in integration_data.items()]
        # 数组中的数据，都按照system排序
        sys = system_list.get(task_type) or system_list.get("compile")
        final_data = {item: {} for item in sys}
        for item in data:
            system = item["system"]
            data = item["data"]
            final_data[system] = data
        final_data = [{"system": k, "data": v} for k, v in final_data.items() if v]
        return len(final_data), final_data


    async def get_case_detail(self, tid, build_id, secondary_type):
        case_detail = {
            "total": 0,
            "status": "Failed",
            "passed_num": 0,
            "failed_num": 0
        }
        case_obj = await CeCases.aio_get_object(
            **{"tid": tid, "build_id" : build_id, "label": secondary_type}
        )
        if case_obj:
            case_detail = {
                "total": case_obj.total,
                "passed_num": case_obj.passed_num,
                "failed_num": case_obj.failed_num,
                "status": case_obj.status
            }

        return case_detail
