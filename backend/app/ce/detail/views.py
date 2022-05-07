# !/usr/bin/env python3
# encoding=utf-8
import asyncio
import datetime
import json
import time

from ce_web.settings.common import STORAGE
from libs.mongo.db import Mongo
from models.steps import CeSteps
from models.details import CeCases

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
        # 支持模型的多个任务，一个secondary_type； 以及框架的一个任务，多个secondary_type
        result = {}
        tid = kwargs.get("tid")
        build_id = kwargs.get("build_id")
        task_type = kwargs.get("task_type")
        secondary_type = kwargs.get("secondary_type")
        secondary_type = secondary_type.split(",")
        for sed_type in secondary_type:
            if sed_type not in result:
                result[sed_type] = {"summary_data": [], "case_detail": None}
            summary_data, res = await self.get_single_data(
                tid, build_id, task_type, sed_type
            )
            result[sed_type]["summary_data"] = [summary_data]
            result[sed_type]["case_detail"] = res
        return len(result), result

    async def get_single_data(self, tid, build_id, task_type, secondary_type,):
        """
        根据查询条件：
        任务类型（task_type）， 
        任务id（tid），
        编译id（build_id）
        得到此次编译的详情组装数据并返回
        """
        # 初始化mong实例
        mongo_cfg = STORAGE["mongo"]["paddle_quality"]
        table_prefix = mongo_cfg["case_detail"]
        secondary_type = secondary_type.split(",")
        details = { key: {} for key in secondary_type }
        case_obj = await CeCases.aio_get_object(
            **{"tid": tid, "build_id" : build_id, "label": secondary_type}
        )
        if not case_obj:
            return 0, {}
        summary_data = {
            'total': case_obj.total,
            'passed_num': case_obj.passed_num,
            'failed_num': case_obj.failed_num
        }
        label_id = case_obj.id
        table_name = table_prefix.format(task_id=tid, build_id=build_id, label_id=label_id)
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
            details = await model_result.find_all()
            for item in details:
                item.pop("_id")

        # 主动关闭mongodb的链接
        model_result.close()
        return summary_data, details


    def pop_object_id(self, data: list):
        """
        删除objectId 对象没办法被json序列化
        """
        for item in data:
            item.pop("_id") 
        return data
        