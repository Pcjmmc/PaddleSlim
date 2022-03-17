"""
主要负责全量任务的业务逻辑处理
"""
# encoding=utf-8
import asyncio
import datetime
import json
import time

from ce_web.settings.common import STORAGE
from libs.mongo.db import Mongo
from models.exempt import CeExempt
from models.task_builds import CeTaskBuilds
from models.tasks import CeTasks


class TasksInfo(object):
    @classmethod
    async def get_all_task_info_by_step(cls, step=None):
        """
        根据条件筛选出任务的全集
        """
        if step:
            step = [step] if type(step) != list else step
            step.append("shared")
            # 将符合要求的全量任务筛选出
            task_records = await CeTasks().aio_filter_details(
                need_all=True, **{"step__in": step}
            )
        else:
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
    async def get_task_latest_status_by_tids(cls, tids, branch, begin_time, end_time=None):
        """
        根据筛选条件获取相同条件下的多个tid的执行信息
        """
        # 为了查询快写，这里分批查询一次查询10个左右
        # in查询如果太多的话会很慢的
        print("begin search", tids, branch, begin_time, end_time)
        tids = tids if type(tids) == list else [tids]
        final_result = {tid: {} for tid in tids}
        # branch这里需要入库的时候处理下
        query_params = {
            "commit_time__gt": begin_time,
            "branch": "* "+ branch
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
        result = await asyncio.gather(*job_list)
        for res in result:
            if res:
                tid = res.tid
                final_result[tid].update(res)
        return final_result

class CaseDetails(object):
    @classmethod
    async def get_task_detail_by_filter(cls, tid, build_id, job_id):
        """
        根据任务详情以及编译详情获取case的详情
        """
        table_prefix = STORAGE["ce"]["case_detail"]
        table_name = table_prefix.format(
            task_id=tid, build_id=build_id, job_id=job_id
        )     
        case_obj = Mongo("ce", table_name)
        result = await case_obj.find_all()
        # 这里需要根据类型汇总信息
        #  比如模型的需要按照模型和阶段将数据汇总起来；框架的需要根据api的名字汇总起来 TODO
        return result if result else {}


class ExemptInfo(object):
    """
    负责豁免相关的操作
    """
    @classmethod
    async def get_task_exempt_status_by_tid(cls, tid, version_id):
        """
        获取任务豁免的状态；所以放在任务栏，还需要一个豁免的表结构
        """
        result = await CeExempt().aio_filter_details(
            **{
                "tid": tid,
                "version_id": version_id
            }
        )
        # 返回json 字典形式的数据
        return {tid: result[0]} if result else {} 

    @classmethod
    async def get_task_exempt_status_by_tids(cls, tids, version_id, batch=5):
        # 获取统一版本下多个tid的豁免情况
        tids = tids if type(tids) == list else [tids]
        final_result = {tid: {} for tid in tids}
        query_params = {
            "version_id": version_id
        }
        job_list = []
        while tids:
            query_tids = tids[:batch]
            tids = tids[batch:]
            query_params["tid__in"] = query_tids
            job_list.append(
                CeExempt().aio_filter_details(
                    need_all=True,
                    **query_params
                )
            )
        result = await asyncio.gather(*job_list)
        for res in result:
            for r in res:
                tid = r["tid"]
                # 这辆需要res转换成json
                final_result[tid].update(r)
        return final_result

    @classmethod
    async def set_task_exempt_status(cls, tid, version_id, status):
        """
        获取任务豁免的状态；所以放在任务栏，还需要一个豁免的表结构
        """
        pass

    @classmethod
    async def update_task_exempt_status(cls, tid, version_id, status):
        """
        获取任务豁免的状态；所以放在任务栏，还需要一个豁免的表结构
        """
        pass
