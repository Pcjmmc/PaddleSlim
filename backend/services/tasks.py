# !/usr/bin/env python3
"""
主要负责全量任务的业务逻辑处理
"""
# encoding=utf-8
import asyncio
import datetime
import json
import time

from api.cache import BuildCacheBase
from ce_web.settings.common import STORAGE
from libs.mongo.db import Mongo
from models.publish_task_builds import PubishTaskBuilds
from models.task_builds import CeTaskBuilds
from models.tasks import CeTasks
from services.auto_create_table import create_task_backup


class TasksInfo(object):
    @classmethod
    async def get_task_by_filter(cls, backup=False, version=None, **kwargs):
        """
        根据条件原封不动筛选
        """
        if backup:
            table_name = "ce_task_" + version
            new_class = await create_task_backup(
                CeTasks.Meta.app_label, table_name
            )
            task_records = await new_class.aio_filter_details(
                need_all=True, **kwargs
            )
        else:
            task_records = await CeTasks().aio_filter_details(
                need_all=True, **kwargs
            )
        return task_records

    @classmethod
    async def get_all_task_info_by_filter(cls, step=None, task_type=None, secondary_type=None, appid=1, backup=False, version=None):
        """
        根据条件筛选出任务的全集
        """
        if step:
            step = [step] if type(step) != list else step
            step.append("shared")
            # 将符合要求的全量任务筛选出
            query_params = {"step__in": step, "appid": appid}
            if task_type:
                query_params["task_type"] = task_type
            if secondary_type:
                query_params["secondary_type"] = secondary_type
            if backup:
                print('发版记录走备份逻辑', backup)
                print('verison is', version)
                table_name = "ce_task_" + version
                new_class = await create_task_backup(
                    CeTasks.Meta.app_label, table_name
                )
                task_records = await new_class.aio_filter_details(
                    need_all=True, **query_params
                )
            else:
                print('无备份逻辑', backup)
                task_records = await CeTasks().aio_filter_details(
                    need_all=True, **query_params
                )
        else:
            if backup:
                print('发版记录走备份逻辑', backup)
                print('verison is', version)
                table_name = "ce_task_" + version
                new_class = await create_task_backup(
                    CeTasks.Meta.app_label, table_name
                )
                task_records = await new_class.aio_filter_details(
                    need_all=True, **query_params
                )
            else:
                print('无备份逻辑', backup)
                task_records = await CeTasks().aio_filter_details(need_all=True)
        return task_records


class TaskBuildInfo(object):
    @classmethod
    async def get_task_latest_status_by_tid(cls, tid, branch, begin_time, end_time=None):
        """
        根据筛选条件获取全量任务最新的执行状态;报错执行中的
        根据任务跑的分支，以及commit和commit_time是否在筛选范围内来给出最新的结果 
        end_time：对于当前正在回归的分支是没有这个时间的，只有打完tag才能出来这个时间；这个时候就设置成None就行
        tids: 支持列表多个查询
        """
        # 为了查询快写，这里分批查询一次查询10个左右
        query_params = {
            "tid": tid, 
            "commit_time__gt": begin_time,
            "branch": branch
        }
        if end_time:
            query_params.update({"commit_tim__lte": end_time})
        build_obj = await CeTaskBuilds().aio_get_object(
            **query_params, order_by="-created"
        )
        # 这里需要将object转换成字典的形式
        CeTaskBuilds.object_to_json(build_obj)
        return {tid: build_obj} if build_obj else {}

    @classmethod
    async def get_task_latest_status_by_tids(cls, tids, branch, begin_time, end_time=None, open_cache=False):
        data = {}
        if open_cache:
            data = await cls.get_task_latest_build_from_cache(tids, branch, begin_time, end_time=end_time)
        else:
            data = await cls.get_task_latest_build_from_db(tids, branch, begin_time, end_time=end_time)

        return data

    @classmethod
    async def get_task_latest_build_from_cache(cls, tids, branch, begin_time, end_time=None):
        """
        根据筛选条件获取相同条件下的多个tid的执行信息
        """
        # 这里分批查询一次并发10个左右
        tids = tids if type(tids) == list else [tids]
        print("全量tid", tids, flush=True)
        final_result = {tid: {} for tid in tids}
        results = []
        all_results = []
        # 这里优先从redis获取
        job_list = []
        db_tids = []
        for tid in tids:
            # 从redis获取数据
            branch_name = branch if branch == "develop" else "release"
            job_list.append(
                BuildCacheBase.get_all_data(tid, branch_name)
            )
            if len(job_list) >= 10:
                result = await asyncio.gather(*job_list)
                job_list = []
                results.append(result)
        result = await asyncio.gather(*job_list)
        results.append(result)
        for res in results:
            all_results.extend(res)
        for res in all_results:
            if res:
                tid = res.get("tid")
                final_result[int(tid)].update(res)
        # 缓存中没找到的走db
        for key, value in final_result.items():
            if not value:
                db_tids.append(key)
        print("从db查询", db_tids, flush=True)
        db_result = await cls.get_task_latest_build_from_db(db_tids, branch, begin_time, end_time)
        # 同时将没命中缓存的数据，同步到缓存中; 编译除外
        # for key, val in db_result.items():
        #     if val:
        #         await BuildCacheBase.set_multi(key, branch_name, data=val)
        final_result.update(db_result)
        return final_result

    @classmethod
    async def get_task_latest_build_from_db(cls, tids, branch, begin_time, end_time=None):
        """
        根据筛选条件获取相同条件下的多个tid的执行信息
        """
        # 为了查询快写，这里分批查询一次查询10个左右
        # in查询如果太多的话会很慢的
        tids = tids if type(tids) == list else [tids]
        final_result = {tid: {} for tid in tids}
        results = []
        all_results = []
        # branch这里需要入库的时候处理下
        query_params = {
            "commit_time__gte": begin_time,
            "branch": branch,
            "commit_id__ne": None
        }
        if end_time:
            query_params.update({"commit_time__lte": end_time})
        job_list = []
        for tid in tids:
            query_params["tid"] = tid
            job_list.append(
                CeTaskBuilds().aio_get_object(
                    **query_params, order_by="-created"
                )
            )
            if len(job_list) >= 10:
                result = await asyncio.gather(*job_list)
                job_list = []
                results.append(result)
        result = await asyncio.gather(*job_list)
        results.append(result)
        for res in results:
            all_results.extend(res)
        for res in all_results:
            if res:
                tid = res.tid
                final_result[tid].update(res)
        return final_result

    @classmethod
    async def get_task_status_by_tids_and_commit(cls, tids, commit):
        """
        根据筛选条件获取相同条件下的多个tid的执行信息
        """
        # 为了查询快写，这里分批查询一次查询10个左右
        # in查询如果太多的话会很慢的
        tids = tids if type(tids) == list else [tids]
        final_result = {}
        # branch这里需要入库的时候处理下
        query_params = {
            "commit_id": commit
        }
        job_list = []
        for tid in tids:
            query_params["tid"] = tid
            job_list.append(
                CeTaskBuilds().aio_get_object(
                    **query_params, order_by="-created"
                )
            )
        result = await asyncio.gather(*job_list)
        for res in result:
            if res:
                tid = res.tid
                if tid not in final_result:
                    final_result[tid] = {}
                final_result[tid].update(res)
        return final_result

    @classmethod
    async def check_commit(cls, commits):
        """
        检查commit是否被QA测试过
        """
        final_result = {commit: {} for commit in commits}
        results = []
        all_results = []
        # branch这里需要入库的时候处理下
        query_params = {}
        job_list = []
        for commit in commits:
            query_params["commit_id"] = commit
            job_list.append(
                CeTaskBuilds().aio_get_object(
                    **query_params
                )
            )
            if len(job_list) >= 10:
                result = await asyncio.gather(*job_list)
                job_list = []
                results.append(result)
        result = await asyncio.gather(*job_list)
        results.append(result)
        for res in results:
            all_results.extend(res)
        for res in all_results:
            if res:
                commit_id = res.commit_id
                final_result[commit_id].update(res)
        return final_result

class CaseDetails(object):
    @classmethod
    async def get_task_detail_by_filter(cls, tid, build_id, job_id):
        """
        根据任务详情以及编译详情获取case的详情
        """
        table_prefix = STORAGE["paddle_quality"]["case_detail"]
        table_name = table_prefix.format(
            task_id=tid, build_id=build_id, job_id=job_id
        )     
        case_obj = Mongo("paddle_quality", table_name)
        result = await case_obj.find_all()
        # 这里需要根据类型汇总信息
        #  比如模型的需要按照模型和阶段将数据汇总起来；框架的需要根据api的名字汇总起来 TODO
        return result if result else {}


class PublishBuildInfo(object):
    @classmethod
    async def get_task_latest_status_by_tids(cls, tids, tag):
        """
        根据筛选条件获取相同条件下的多个tid的执行信息
        """
        # 为了查询快写，这里分批查询一次查询10个左右
        # in查询如果太多的话会很慢的
        tids = tids if type(tids) == list else [tids]
        final_result = {tid: {} for tid in tids}
        results = []
        all_results = []
        # branch这里需要入库的时候处理下
        query_params = {
            "tag": tag,
        }
        job_list = []
        for tid in tids:
            query_params["tid"] = tid
            job_list.append(
                PubishTaskBuilds().aio_get_object(
                    **query_params, order_by="-updated"
                )
            )
            if len(job_list) >= 10:
                result = await asyncio.gather(*job_list)
                job_list = []
                results.append(result)
        result = await asyncio.gather(*job_list)
        results.append(result)
        for res in results:
            all_results.extend(res)
        for res in all_results:
            if res:
                tid = res.tid
                final_result[tid].update(res)
        return final_result
