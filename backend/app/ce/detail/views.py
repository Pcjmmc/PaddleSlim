# !/usr/bin/env python3
# encoding=utf-8
import asyncio
import datetime
import json
import time

from ce_web.settings.common import STORAGE
from libs.mongo.db import Mongo
from models.steps import CeSteps

from views.base_view import MABaseView


class DetailManage(MABaseView):
    """
    获取每个任务每次编译的详情
    """
    get_summary = "获取case的详情"
    # 需要从mongodb中查询

    async def get(self, **kwargs):
        """
        调用基类的get方法
        """
        return await super().get(**kwargs)

    async def get_data(self, **kwargs):
        """
        根据查询条件：任务类型（task_type）， 任务id（tid），编译id（build_id）得到此次编译的详情组装数据并返回
        """
        # 初始化mong实例
        mongo_cfg = STORAGE["mongo"]["paddle_quality"]
        task_type = kwargs.get("task_type")
        table_prefix = mongo_cfg["case_detail"]
        table_name = table_prefix.format(task_id=kwargs.get("tid"), build_id=kwargs.get("build_id"))
        model_result = Mongo("paddle_quality", table_name)
        if task_type == "model":
            details = await model_result.find_all()
            self.pop_object_id(details)
            result = dict()
            # 如果类型是模型，则在后段对模型数据进行归类和组装
            for item in details:
                model_name = item.get("model_name")
                if model_name not in result:
                    result[model_name] = {"kpis": dict(), "status": "Passed"}
                step_name = item.get("step_name")
                if step_name not in result[model_name]["kpis"]:
                    result[model_name]["kpis"][step_name]= {"step_name": step_name, "status": "Passed", "data": list()}
                result[model_name]["kpis"][step_name]["data"].append(item)
                if item.get("kpi_status", "Failed").lower() == "failed":
                    result[model_name]["status"] = "Failed"
                    result[model_name]["kpis"][step_name]["status"] = "Failed"

            for key, val in result.items():
                val["kpis"] = [value for item, value in val["kpis"].items()]
            details = result
        else:
            # 如果是功能测试，提前将数据准备好
            total = uncertain = succeed = failed = 0
            job_task = []
            # 查询成功的数据和count
            job_task.append(model_result.get_data_and_count_by_condition({"status": "passed"}))
            # 查询失败的数据和count
            job_task.append(model_result.get_data_and_count_by_condition({"status" : {"$in": ["broken", "failed"]}}))
            # 查询不确定的数据和count
            job_task.append(model_result.get_data_and_count_by_condition({"status" : "unknown"}))
            # 查询总数
            job_task.append(model_result.get_count_by_condition({"status" : {"$ne": "skipped"}}))
            func_res = await asyncio.gather(*job_task)

            succeed, succeed_data = func_res[0]
            failed, failed_data = func_res[1]
            uncertain, uncertained_data = func_res[2]
            total = func_res[3]
            details = {
                "summary_data": [
                    {
                        'total': total,
                        'uncertain': uncertain,
                        'succeed': succeed,
                        'failed': failed
                    } 
                ],
                "succeed_data": self.pop_object_id(succeed_data),
                "failed_data": self.pop_object_id(failed_data),
                "uncertained_data": self.pop_object_id(uncertained_data)
            }
        # 主动关闭mongodb的链接
        model_result.close()
        return len(details), details


    def pop_object_id(self, data: list):
        """
        删除objectId 对象没办法被json序列化
        """
        for item in data:
            item.pop("_id") 
        return data
        