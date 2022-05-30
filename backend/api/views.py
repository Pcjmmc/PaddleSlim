# !/usr/bin/env python3
# encoding: utf-8
"""
对外提供API逻辑，实现增删改查
"""
import asyncio
import json

from ce_web.settings.common import STORAGE
from exception import HTTP400Error
from libs.mongo.db import Mongo
from models.task_builds import CeTaskBuilds
from models.tasks import CeTasks
from models.details import CeCases

from api.forms import AddCaseForm
from views.base_view import MABaseView


class CaseDetailView(MABaseView):
    """
    完成模型kpi的快速存储
    """
    # 定义post类型检查类
    post_form_class = AddCaseForm

    async def post(self, **kwargs):
        return await super().post(**kwargs)

    async def post_data(self, **kwargs):
        """
        build_type_id: (获取任务的唯一id)，效率云对应AGILE_PIPELINE_CONF_ID
        build_id: 构建id，效率云对应AGILE_PIPELINE_BUILD_ID
        repo: repo名#被测对象，框架Paddle，模型对应repo
        branch: branch分支信息
        commit_id: commit 信息
        commit_time: commit 的提交信息
        build_time: 编包的时间
        job_id: 多阶段的job build id ,任务并行追加逻辑
        left_time: status=running中的剩余时间
        status: 任务状态
        exit_code: 任务本次执行的退出
        duration: 任务执行时长
        case_detail: case的执行详情
        """
        remote_ip = self.request.remote_ip
        #print("remote_ip=", remote_ip)
        #TODO 后续设计机器管理能力，统计支持CE/集测的资源情况
        #特殊情况：1）PDC相关的可能需要加个字段区分出来PDC
        #           2）复用研发CCE集群/windows集群的资源
        build_type_id = kwargs.get("build_type_id")
        build_id = kwargs.get("build_id")
        status = kwargs.get("status")
        #print("status=",status)
        # task 入库逻辑
        task_obj = await CeTasks.aio_get_object(
            **{"build_type_id": build_type_id}
        )
        if not task_obj:
            # 不存在任务则抛出异常
            raise HTTP400Error("找不到任务，请先录入任务！")
        else:
            tid = task_obj.id
            task_type = task_obj.task_type
            secondary_type = task_obj.secondary_type
            try:
                details = json.loads(kwargs.get("case_detail"))
            except:
                details = []
            total = 0
            passed_num = 0
            #print("details=",deatails)
            if task_type in ['model', 'benchmark', 'dist']:
                #TODO和模型相关的需要按照模型维度聚合入库
                model_detail = dict()
                for item in details:
                    model_name = item["model_name"]
                    if model_name not in model_detail.keys():
                        model_detail[model_name] = item["kpi_status"]
                    else:
                        model_detail[model_name] = model_detail[model_name] if item["kpi_status"] == "Passed" else "Failed"
                #遍历model_detail,获取模型级别passed_num
                total = len(model_detail.keys())
                for key, val in model_detail.items():
                    if val == "Passed":
                        passed_num += 1
            else:
                total = len(details)
                for item in details:
                    if "status" in item.keys() and item["status"].upper() == "Passed".upper():
                       passed_num += 1
                       #改为统一入库，一次插入
                       #await model_result.insert(item)
            failed_num = total - passed_num
            #增加task_build级别case数量信息
            case_info = { 
                "total_case": total,
                "passed_case": passed_num,
                "failed_case": failed_num
            }
            task_data = kwargs.copy()
            task_data.update(case_info)
            #build信息入库
            await CeTaskBuilds.create_or_update_build(
                tid, build_id, validated_data=task_data
            )
            # case详细入库mysql 
            await CeCases.create_or_update_build(tid, build_id, status, total, passed_num, failed_num, secondary_type)
            case_obj = await CeCases.aio_get_object(
                 **{"tid": tid, "build_id" : build_id}
            )
            
            mongo_cfg = STORAGE["mongo"]['paddle_quality']
            table_name = mongo_cfg["case_detail"].format(
                task_id=tid, build_id=build_id, label_id=case_obj.id
            )
            print("table_name=", table_name)
            #TOTO插入case之前需要先判断之前是否存在对应表名
            model_result = Mongo("paddle_quality", table_name)
            #测试是否删除成功
            await model_result.delete_coll()
            #print("del ok")
            #tmp_mongo = await model_result.find_all()
            #print("tmp_mongo=",tmp_mongo)
            if details:
                await model_result.insert_many(details)
                model_result.close() 